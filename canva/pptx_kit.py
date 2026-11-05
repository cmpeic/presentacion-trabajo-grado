"""Utilidades para construir laminas 1920x1080 en PPTX para importarlas a Canva.

Todas las coordenadas se expresan en pixeles del lienzo de 1920x1080; el modulo
las convierte a EMU (1 px = 9525 EMU, 96 ppp). Los tamanos de letra tambien se
expresan en pixeles y se convierten a puntos (1 px = 0,75 pt).
"""

from __future__ import annotations

from contextlib import contextmanager

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Pt
from lxml import etree

W, H = 1920, 1080

FONT_HEAD = "Montserrat"
FONT_BODY = "Inter"
FONT_MONO = "Roboto Mono"


def px(v: float) -> Emu:
    return Emu(int(round(v * 9525)))


def rgb(hex_color: str) -> RGBColor:
    return RGBColor.from_string(hex_color.lstrip("#").upper())


# ------------------------------------------------------------------ tema claro
# Las laminas se disenaron sobre fondo oscuro. Con TEMA = "claro" cada color se
# traduce al emitirlo: los rellenos azul noche pasan a tintes claros, los colores
# de acento se conservan y el color de cada texto se decide segun lo que tiene
# detras (modelo de pintura por lamina), de modo que el blanco sobre azul sigue
# siendo blanco y el blanco sobre una tarjeta clara pasa a tinta oscura.
TEMA = "claro"
PAGINA = "#FFFFFF"
TINTA = "#0B1F3A"
TINTA_2 = "#4E5F78"
ORO_LINEA = "#E8B000"

_RELLENOS = {
    "#07172D": "#FFFFFF", "#0A1F3D": "#F4F7FB", "#0B2242": "#F4F7FB", "#0C2445": "#EBF1F8",
    "#0D2748": "#F1F5FA", "#0F2C52": "#E6EEF8", "#12305E": "#E3ECF8", "#1A3F78": "#D6E4F6",
    "#1B3A66": "#E1EAF5",
}
_LINEAS = {"#6D8FB2": "#C3D2E3", "#F3F7FC": "#C3D2E3", "#FFFFFF": "#C3D2E3"}
_TEXTOS = {"#4F9BFF": "#1A5FCF", "#2F7BFF": "#1A5FCF", "#E0566B": "#C42F48",
           "#3DBE8B": "#1F8A5E", "#9FB4CC": TINTA_2, "#6D8FB2": TINTA_2}


def _c3(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _hex(c) -> str:
    return "#%02X%02X%02X" % tuple(max(0, min(255, int(round(v)))) for v in c)


def _lum(c) -> float:
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = c
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def _mezcla(a, b, t: float):
    """t*a + (1-t)*b."""
    return tuple(t * x + (1 - t) * y for x, y in zip(a, b))


@contextmanager
def colores_literales():
    """Dentro del bloque los colores se emiten tal cual (laminas disenadas ya en claro)."""
    global TEMA
    previo, TEMA = TEMA, "literal"
    try:
        yield
    finally:
        TEMA = previo


def color_relleno(c: str | None, w: float = 999, h: float = 999) -> str | None:
    if TEMA != "claro" or c is None:
        return c
    c = c.upper()
    if c in _RELLENOS:
        return _RELLENOS[c]
    if c == "#FFD21F" and min(w, h) <= 6:
        return ORO_LINEA  # filetes y esquineros amarillos: dorado legible sobre blanco
    c3 = _c3(c)
    if _lum(c3) < 0.05:  # cualquier otro azul noche -> tinte claro del mismo tono
        return _hex(_mezcla(c3, (255, 255, 255), 0.07))
    return c


def color_linea(c: str | None) -> str | None:
    if TEMA != "claro" or c is None:
        return c
    c = c.upper()
    if c in _LINEAS:
        return _LINEAS[c]
    if c == "#FFD21F":
        return ORO_LINEA
    if _lum(_c3(c)) < 0.05:
        return "#C3D2E3"
    return c


def color_trazo(slide, c: str | None, x, y, w, h) -> str | None:
    """Color de un trazo fino (raya de fraccion, flecha, filete) segun lo que tiene detras.

    En el tema oscuro estos trazos eran blancos; sobre un fondo claro pasan a tinta,
    y sobre un fondo oscuro o saturado (azul, rojo) siguen blancos."""
    if TEMA != "claro" or c is None:
        return c
    r, g, b = _c3(c)
    if min(r, g, b) >= 230:  # blanco o casi blanco
        fondo = fondo_en(slide, x + w / 2, y + h / 2)
        return TINTA if _lum(fondo) >= 0.36 else c
    return color_relleno(c, w, h)


def _registrar(slide, x, y, w, h, fill, alpha):
    """Anota un relleno opaco o translucido en el modelo de pintura de la lamina."""
    if TEMA != "claro" or fill is None or w <= 0 or h <= 0:
        return
    pint = getattr(slide, "_pintura", None)
    if pint is None:
        pint = slide._pintura = []
    cx, cy = x + w / 2, y + h / 2
    debajo = fondo_en(slide, cx, cy)
    efectivo = _mezcla(_c3(fill), debajo, alpha) if alpha < 1 else _c3(fill)
    pint.append((x, y, w, h, efectivo))


def fondo_en(slide, x, y):
    for (rx, ry, rw, rh, c) in reversed(getattr(slide, "_pintura", []) or []):
        if rx <= x <= rx + rw and ry <= y <= ry + rh:
            return c
    return _c3(getattr(slide, "_fondo", PAGINA))


def color_texto(slide, c: str, x, y, w, h, size, align="left", anchor="top") -> str:
    if TEMA != "claro":
        return c
    sx = x + w / 2 if align == "center" else (x + w - 12 if align == "right" else x + 12)
    sy = {"top": y + size * 0.6, "middle": y + h / 2, "bottom": y + h - size * 0.6}[anchor]
    if _lum(fondo_en(slide, sx, sy)) < 0.36:  # detras hay un color oscuro o saturado
        return c
    c = c.upper()
    if c in _TEXTOS:
        return _TEXTOS[c]
    c3 = _c3(c)
    r, g, b = c3
    if r > 200 and g > 150 and b < 120:  # amarillo de acento -> dorado legible
        return "#9A6B00" if size < 34 else "#AD7A00"
    L = _lum(c3)
    if L > 0.5:
        return TINTA
    if L > 0.25:
        return TINTA_2
    return c


def _set_alpha(color_parent, alpha: float) -> None:
    """Agrega <a:alpha> al srgbClr dentro de color_parent (fill o line)."""
    if alpha is None or alpha >= 1:
        return
    srgb = color_parent.find(qn("a:srgbClr"))
    if srgb is None:
        srgb = color_parent.find(".//" + qn("a:srgbClr"))
    if srgb is None:
        return
    for old in srgb.findall(qn("a:alpha")):
        srgb.remove(old)
    el = etree.SubElement(srgb, qn("a:alpha"))
    el.set("val", str(int(round(alpha * 100000))))


def new_presentation() -> Presentation:
    prs = Presentation()
    prs.slide_width = px(W)
    prs.slide_height = px(H)
    return prs


ANCLAS: dict[str, int] = {}  # clave -> número de lámina, para referencias cruzadas


def anclar(slide, clave: str) -> None:
    """Registra el número de esta lámina bajo una clave."""
    ANCLAS[clave] = slide._num


def lamina(clave: str) -> int | str:
    """Número de la lámina anclada con `clave` (debe construirse antes de citarla).

    Al previsualizar un grupo suelto la lámina citada puede no existir: devuelve «??»."""
    if clave not in ANCLAS:
        print(f"aviso: lámina sin anclar «{clave}» (se escribe ??)")
        return "??"
    return ANCLAS[clave]


def add_slide(prs: Presentation, bg: str = "#07172D", bg_image: str | None = None):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide._num = len(prs.slides)
    slide._pintura = []
    slide._anim = []
    if TEMA == "claro":
        bg, bg_image = PAGINA, None  # todo el documento va sobre fondo blanco
    slide._fondo = bg
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = rgb(bg)
    if bg_image:
        pic = slide.shapes.add_picture(bg_image, 0, 0, px(W), px(H))
        pic.name = "Fondo"
    return slide


def notes(slide, text: str) -> None:
    slide.notes_slide.notes_text_frame.text = text


def _style_fill(shape, fill: str | None, fill_alpha: float = 1.0) -> None:
    if fill is None:
        shape.fill.background()
    else:
        shape.fill.solid()
        shape.fill.fore_color.rgb = rgb(fill)
        if fill_alpha < 1:
            sp_pr = shape._element.spPr
            _set_alpha(sp_pr.find(qn("a:solidFill")), fill_alpha)


def _style_line(shape, line: str | None, width: float = 1.0, alpha: float = 1.0,
                dash: str | None = None) -> None:
    if line is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = rgb(line)
        shape.line.width = Pt(width * 0.75)
        ln = shape._element.spPr.find(qn("a:ln"))
        if alpha < 1:
            _set_alpha(ln.find(qn("a:solidFill")), alpha)
        if dash:
            d = etree.SubElement(ln, qn("a:prstDash"))
            d.set("val", dash)


def _no_shadow(shape) -> None:
    sp_pr = shape._element.spPr
    if sp_pr.find(qn("a:effectLst")) is None:
        etree.SubElement(sp_pr, qn("a:effectLst"))
    # el estilo por defecto de python-pptx apunta a la sombra del tema (effectRef 2);
    # sobre fondo blanco se ve como un halo gris, asi que se anula desde el estilo
    eref = shape._element.find(".//" + qn("a:effectRef"))
    if eref is not None:
        eref.set("idx", "0")


def rect(slide, x, y, w, h, fill=None, line=None, line_w=1.0, fill_alpha=1.0,
         line_alpha=1.0, radius: float | None = None, name: str | None = None,
         dash: str | None = None):
    kind = MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE
    shp = slide.shapes.add_shape(kind, px(x), px(y), px(w), px(h))
    if radius:
        shp.adjustments[0] = min(0.5, radius / min(w, h))
    fill = color_trazo(slide, fill, x, y, w, h) if min(w, h) <= 6 else color_relleno(fill, w, h)
    _registrar(slide, x, y, w, h, fill, fill_alpha)
    _style_fill(shp, fill, fill_alpha)
    _style_line(shp, color_linea(line), line_w, line_alpha, dash)
    _no_shadow(shp)
    shp.text_frame.text = ""
    if name:
        shp.name = name
    return shp


def ellipse(slide, cx, cy, r, fill=None, line=None, line_w=1.0, fill_alpha=1.0,
            line_alpha=1.0, name: str | None = None):
    shp = slide.shapes.add_shape(MSO_SHAPE.OVAL, px(cx - r), px(cy - r), px(2 * r), px(2 * r))
    fill = color_relleno(fill, 2 * r, 2 * r)
    if r > 30:  # solo los circulos grandes cuentan como fondo de un texto
        _registrar(slide, cx - r * 0.7, cy - r * 0.7, r * 1.4, r * 1.4, fill, fill_alpha)
    _style_fill(shp, fill, fill_alpha)
    _style_line(shp, color_linea(line), line_w, line_alpha)
    _no_shadow(shp)
    if name:
        shp.name = name
    return shp


def line(slide, x1, y1, x2, y2, color="#6D8FB2", width=1.0, alpha=1.0, arrow=False,
         dash: str | None = None):
    conn = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, px(x1), px(y1), px(x2), px(y2))
    conn.line.color.rgb = rgb(color_linea(color))
    conn.line.width = Pt(width * 0.75)
    ln = conn._element.spPr.find(qn("a:ln"))
    if alpha < 1:
        _set_alpha(ln.find(qn("a:solidFill")), alpha)
    if dash:
        d = etree.SubElement(ln, qn("a:prstDash"))
        d.set("val", dash)
    if arrow:
        tail = etree.SubElement(ln, qn("a:tailEnd"))
        tail.set("type", "triangle")
        tail.set("w", "med")
        tail.set("len", "med")
    return conn


def arrow_shape(slide, x, y, w, h, color="#FFD21F", alpha=1.0, name: str | None = None):
    """Flecha de bloque rellena apuntando a la derecha."""
    shp = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, px(x), px(y), px(w), px(h))
    _style_fill(shp, color_trazo(slide, color, x, y, w, h), alpha)
    _style_line(shp, None)
    _no_shadow(shp)
    if name:
        shp.name = name
    return shp


def triangle(slide, x, y, w, h, color="#FFD21F", rotation=0, alpha=1.0, name=None):
    """Triangulo isosceles relleno; rotation=90 apunta a la derecha, 180 hacia abajo."""
    shp = slide.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, px(x), px(y), px(w), px(h))
    shp.rotation = rotation
    _style_fill(shp, color_trazo(slide, color, x, y, w, h), alpha)
    _style_line(shp, None)
    _no_shadow(shp)
    if name:
        shp.name = name
    return shp


def corners(slide, x, y, w, h, size=34, color="#FFD21F", width=3.0, which="tl,tr,bl,br",
            alpha=1.0):
    """Esquineros en L (marcas de encuadre) dibujados con rectangulos finos."""
    parts = set(which.split(","))
    t = width
    segs = []
    if "tl" in parts:
        segs += [(x, y, size, t), (x, y, t, size)]
    if "tr" in parts:
        segs += [(x + w - size, y, size, t), (x + w - t, y, t, size)]
    if "bl" in parts:
        segs += [(x, y + h - size, t, size), (x, y + h - t, size, t)]
    if "br" in parts:
        segs += [(x + w - t, y + h - size, t, size), (x + w - size, y + h - t, size, t)]
    for (sx, sy, sw, sh) in segs:
        rect(slide, sx, sy, sw, sh, fill=color, fill_alpha=alpha, name="Esquinero")


def text(slide, x, y, w, h, content, size=28, color="#F3F7FC", bold=False,
         font: str = FONT_BODY, align="left", anchor="top", line_spacing=1.2,
         italic=False, spacing: float | None = None, name: str | None = None,
         wrap=True, alpha: float = 1.0):
    """Caja de texto. `content` puede ser str o lista de parrafos.

    Cada parrafo puede ser str o lista de runs; cada run es str o dict con
    claves text, color, bold, size, font, italic.
    """
    tb = slide.shapes.add_textbox(px(x), px(y), px(w), px(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.margin_left = tf.margin_right = 0
    tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = {"top": MSO_ANCHOR.TOP, "middle": MSO_ANCHOR.MIDDLE,
                          "bottom": MSO_ANCHOR.BOTTOM}[anchor]
    paragraphs = content if isinstance(content, list) else [content]
    for i, para in enumerate(paragraphs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER,
                       "right": PP_ALIGN.RIGHT, "justify": PP_ALIGN.JUSTIFY}[align]
        # Canva interpreta el interlineado PPTX multiplicado por 1,2
        p.line_spacing = round(line_spacing / 1.2, 3)
        runs = para if isinstance(para, list) else [para]
        for run_spec in runs:
            spec = run_spec if isinstance(run_spec, dict) else {"text": run_spec}
            r = p.add_run()
            r.text = spec["text"]
            f = r.font
            f.size = Pt(spec.get("size", size) * 0.75)
            f.bold = spec.get("bold", bold)
            f.italic = spec.get("italic", italic)
            f.name = spec.get("font", font)
            f.color.rgb = rgb(color_texto(slide, spec.get("color", color), x, y, w, h,
                                          spec.get("size", size), align, anchor))
            sp = spec.get("spacing", spacing)
            rpr = r._r.get_or_add_rPr()
            if sp:
                rpr.set("spc", str(int(sp * 100)))
            if spec.get("baseline"):
                rpr.set("baseline", str(int(spec["baseline"] * 1000)))
            a = spec.get("alpha", alpha)
            if a is not None and a < 0.999:
                _set_alpha(rpr.find(qn("a:solidFill")), max(0.0, a))
    if name:
        tb.name = name
    return tb


_OPT_CACHE: dict[str, str] = {}
OPT_DIR = None  # carpeta para copias optimizadas; None = usar originales


def _optimized(path: str, max_side: int = 1100, trim: bool = False) -> str:
    """Copia reducida y optimizada de imagenes pesadas (cache por ruta).

    En PNG con transparencia limpia una franja del borde (algunos iconos traen
    lineas semitransparentes en el canto) y, con trim=True, recorta el margen
    transparente para que el dibujo llene su caja.
    """
    import hashlib
    import os

    if OPT_DIR is None:
        return path
    ck = (path, trim)
    if ck in _OPT_CACHE:
        return _OPT_CACHE[ck]
    if os.path.getsize(path) < 350_000 and not trim:
        _OPT_CACHE[ck] = path
        return path
    from PIL import Image as _Im

    os.makedirs(OPT_DIR, exist_ok=True)
    key = hashlib.sha1(f"{path}|{trim}".encode()).hexdigest()[:10]
    out = os.path.join(OPT_DIR, f"{os.path.splitext(os.path.basename(path))[0]}_{key}.png")
    if not os.path.exists(out):
        im = _Im.open(path)
        if im.mode == "RGBA":
            import numpy as np

            arr = np.array(im)
            band = max(8, int(0.012 * max(im.size)))
            arr[:band, :, 3] = 0
            arr[-band:, :, 3] = 0
            arr[:, :band, 3] = 0
            arr[:, -band:, 3] = 0
            im = _Im.fromarray(arr, "RGBA")
            if trim:
                ys, xs = np.where(arr[:, :, 3] > 12)
                if len(xs):
                    pad = int(0.02 * max(im.size))
                    box = (max(0, xs.min() - pad), max(0, ys.min() - pad),
                           min(im.width, xs.max() + pad), min(im.height, ys.max() + pad))
                    im = im.crop(box)
        w0, h0 = im.size
        side = 760 if abs(w0 - h0) < 0.1 * max(w0, h0) else max_side
        im.thumbnail((side, side), _Im.LANCZOS)
        im.save(out, optimize=True)
    _OPT_CACHE[ck] = out
    return out


def image(slide, path, x, y, w=None, h=None, name: str | None = None, alpha: float = 1.0,
          crop: tuple | None = None, trim: bool = False):
    path = _optimized(str(path), trim=trim)
    pic = slide.shapes.add_picture(path, px(x), px(y), px(w) if w else None, px(h) if h else None)
    if crop:
        pic.crop_left, pic.crop_top, pic.crop_right, pic.crop_bottom = crop
    if alpha < 0.999:
        blip = pic._element.find(".//" + qn("a:blip"))
        amf = etree.SubElement(blip, qn("a:alphaModFix"))
        amf.set("amt", str(int(alpha * 100000)))
    if name:
        pic.name = name
    return pic


def image_fit(slide, path, x, y, w, h, name: str | None = None, alpha: float = 1.0,
              trim: bool = False):
    """Inserta la imagen completa (contain) centrada dentro de la caja.

    Con trim=True se descarta antes el margen transparente del PNG.
    """
    from PIL import Image

    real = _optimized(str(path), trim=trim) if trim else str(path)
    iw, ih = Image.open(real).size
    scale = min(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    return image(slide, path, x + (w - dw) / 2, y + (h - dh) / 2, dw, dh, name=name, alpha=alpha,
                 trim=trim)


# ------------------------------------------------------------------ animaciones
# Animaciones de entrada nativas de PowerPoint (aparecen solas al mostrar la
# lamina, escalonadas). Se escriben al final con escribir_animaciones(prs).
_NS_P = 'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
MAX_ANIM = 14  # por lamina: lo justo para que se note el movimiento sin demorar


def animar(slide, shape, kind: str = "fade", delay_ms: int | None = None, dur_ms: int = 600):
    """Programa una animacion de entrada para `shape` (fade, wipe o zoom)."""
    lista = getattr(slide, "_anim", None)
    if lista is None:
        lista = slide._anim = []
    if len(lista) >= MAX_ANIM:
        return
    if delay_ms is None:
        delay_ms = 150 + 110 * len(lista)
    lista.append((shape.shape_id, kind, int(delay_ms), int(dur_ms)))


def _efecto(i, spid, kind, delay, dur):
    tgt = f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>'
    vis = (f'<p:set><p:cBhvr><p:cTn id="{i + 1}" dur="1" fill="hold"><p:stCondLst>'
           f'<p:cond delay="0"/></p:stCondLst></p:cTn>{tgt}<p:attrNameLst>'
           f'<p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to>'
           f'<p:strVal val="visible"/></p:to></p:set>')
    if kind == "wipe":
        pid, sub, n = 22, 8, 2
        body = (f'<p:animEffect transition="in" filter="wipe(left)"><p:cBhvr>'
                f'<p:cTn id="{i + 2}" dur="{dur}"/>{tgt}</p:cBhvr></p:animEffect>')
    elif kind == "zoom":
        pid, sub, n = 53, 16, 4
        anims = ""
        for k, attr in enumerate(("ppt_w", "ppt_h")):
            anims += (f'<p:anim calcmode="lin" valueType="num"><p:cBhvr>'
                      f'<p:cTn id="{i + 2 + k}" dur="{dur}" fill="hold"/>{tgt}<p:attrNameLst>'
                      f'<p:attrName>{attr}</p:attrName></p:attrNameLst></p:cBhvr><p:tavLst>'
                      f'<p:tav tm="0"><p:val><p:fltVal val="0"/></p:val></p:tav>'
                      f'<p:tav tm="100000"><p:val><p:strVal val="#{attr}"/></p:val></p:tav>'
                      f'</p:tavLst></p:anim>')
        body = anims + (f'<p:animEffect transition="in" filter="fade"><p:cBhvr>'
                        f'<p:cTn id="{i + 4}" dur="{dur}"/>{tgt}</p:cBhvr></p:animEffect>')
    else:  # fade
        pid, sub, n = 10, 0, 2
        body = (f'<p:animEffect transition="in" filter="fade"><p:cBhvr>'
                f'<p:cTn id="{i + 2}" dur="{dur}"/>{tgt}</p:cBhvr></p:animEffect>')
    xml = (f'<p:par><p:cTn id="{i}" presetID="{pid}" presetClass="entr" presetSubtype="{sub}" '
           f'fill="hold" nodeType="withEffect"><p:stCondLst><p:cond delay="{delay}"/>'
           f'</p:stCondLst><p:childTnLst>{vis}{body}</p:childTnLst></p:cTn></p:par>')
    return xml, i + n + 1


def escribir_animaciones(prs, transicion: bool = True) -> int:
    """Escribe <p:timing> (y una transicion suave) en cada lamina. Devuelve cuantas animo."""
    total = 0
    P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
    for slide in prs.slides:
        sld = slide._element
        for old in sld.findall(P + "timing") + sld.findall(P + "transition"):
            sld.remove(old)
        ext = sld.find(P + "extLst")
        if transicion:
            tr = etree.fromstring(f'<p:transition {_NS_P} spd="med"><p:fade/></p:transition>')
            (ext.addprevious(tr) if ext is not None else sld.append(tr))
        lista = getattr(slide, "_anim", None) or []
        if not lista:
            continue
        nid, pars = 5, []
        for spid, kind, delay, dur in lista:
            x, nid = _efecto(nid, spid, kind, delay, dur)
            pars.append(x)
        xml = (f'<p:timing {_NS_P}><p:tnLst><p:par><p:cTn id="1" dur="indefinite" '
               f'restart="never" nodeType="tmRoot"><p:childTnLst><p:seq concurrent="1" '
               f'nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>'
               f'<p:par><p:cTn id="3" fill="hold"><p:stCondLst><p:cond delay="indefinite"/>'
               f'<p:cond evt="onBegin" delay="0"><p:tn val="2"/></p:cond></p:stCondLst>'
               f'<p:childTnLst><p:par><p:cTn id="4" fill="hold"><p:stCondLst>'
               f'<p:cond delay="0"/></p:stCondLst><p:childTnLst>' + "".join(pars) +
               f'</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par></p:childTnLst>'
               f'</p:cTn><p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/>'
               f'</p:tgtEl></p:cond></p:prevCondLst><p:nextCondLst><p:cond evt="onNext" '
               f'delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq>'
               f'</p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>')
        el = etree.fromstring(xml)
        tr = sld.find(P + "transition")
        if tr is not None:
            tr.addnext(el)
        elif ext is not None:
            ext.addprevious(el)
        else:
            sld.append(el)
        total += 1
    return total
