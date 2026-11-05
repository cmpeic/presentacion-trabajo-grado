"""Antecedentes · cómo funciona el product matching (láminas nuevas del autor).

- Antecedente 02 (la extracción automática): cinco láminas «Anatomía de una página
  retailer», una por comercio (Amazon, MediaMarkt, Falabella, Mercado Libre, Best Buy),
  con la página esquematizada, sus siete partes numeradas, qué parte llega al dataset y
  qué información útil trae el título.
- Antecedente 03 (la comparación manual): «Validación de correspondencia», el catálogo
  del fabricante frente a la publicación, criterio por criterio, y los cuatro estados.

Las páginas son esquemas dibujados con formas (no capturas): el nombre del comercio va
como texto y los productos como ilustraciones planas. Los datos de cada producto son los
de los ejemplos del autor. Se diseñan directamente en claro (colores literales).
"""

from __future__ import annotations

from pptx.enum.shapes import MSO_SHAPE

from pptx_kit import (FONT_HEAD, FONT_MONO, _no_shadow, _style_fill, _style_line, add_slide,
                      arrow_shape, colores_literales, ellipse, line, notes, px, rect, text,
                      triangle)
from theme import header
from componentes import text_width, wrap_lines

TXT = "Barlow"
TINTA = "#0B1F3A"
TINTA_2 = "#4E5F78"
AZUL = "#0B5EA8"
AZUL_C = "#2F7BFF"
ORO = "#9A6B00"
AMARILLO = "#FFD21F"
VERDE = "#1F8A5E"
ROJO = "#C42F48"
TARJETA = "#F4F7FB"
BORDE = "#C3D2E3"
CHIP = "#E6EEF8"
FILETE = "#E3EAF3"
BLANCO = "#FFFFFF"

# caja de la página esquematizada y columnas
MX, MY, MW, MH = 96, 262, 1110, 620
IMG = (200, 384, 380, 470)          # zona de la imagen del producto
IX, IW = 610, 556                   # columna de información
MARCA_X = 1186                      # marcadores numerados
LX, LW = 1236, 588                  # leyenda


# ------------------------------------------------------------------ primitivas
def _forma(s, kind, x, y, w, h, fill=None, line_c=None, lw=1.5, alpha=1.0, rot=0):
    shp = s.shapes.add_shape(kind, px(x), px(y), px(w), px(h))
    _style_fill(shp, fill, alpha)
    _style_line(shp, line_c, lw)
    _no_shadow(shp)
    if rot:
        shp.rotation = rot
    return shp


def ovalo(s, x, y, w, h, fill=None, line_c=None, lw=1.5, alpha=1.0):
    return _forma(s, MSO_SHAPE.OVAL, x, y, w, h, fill, line_c, lw, alpha)


def estrella(s, cx, cy, r, color=AMARILLO, alpha=1.0):
    return _forma(s, MSO_SHAPE.STAR_5_POINT, cx - r, cy - r, 2 * r, 2 * r, color, None, 1, alpha)


def t(s, x, y, w, h, contenido, size=20, color=TINTA, bold=False, font=TXT, **kw):
    # siempre con ajuste de línea: las cajas son anchas y así Canva y LibreOffice
    # alinean igual (LibreOffice centra los cuadros sin ajuste)
    kw.pop("wrap", None)
    return text(s, x, y, w, h, contenido, size=size, color=color, bold=bold, font=font,
                wrap=True, **kw)


def marcador(s, cx, cy, n):
    ellipse(s, cx, cy, 16, fill=AMARILLO, line=BLANCO, line_w=2)
    t(s, cx - 16, cy - 16, 32, 32, str(n), size=18, bold=True, font=FONT_HEAD,
      align="center", anchor="middle", wrap=False)


def guia(s, x0, y, x1):
    """Línea punteada del elemento a su marcador."""
    if x1 - x0 > 12:
        line(s, x0, y, x1, y, color="#9FB4CC", width=1.5, dash="sysDot")


# ------------------------------------------------------------------ íconos
def icono(s, tipo, x, y, c=AZUL):
    """Ícono plano de 48 px dibujado con formas."""
    if tipo == "marca":
        r_ = rect(s, x + 11, y + 11, 26, 26, fill=c, radius=5)
        r_.rotation = 45
        ellipse(s, x + 24, y + 16, 3.5, fill=BLANCO)
    elif tipo == "titulo":
        rect(s, x + 11, y + 6, 26, 36, fill=None, line=c, line_w=3, radius=4)
        for k, w_ in enumerate((14, 14, 9)):
            rect(s, x + 17, y + 15 + k * 8, w_, 3, fill=c)
    elif tipo == "codigo":
        xx = x + 7
        for w_ in (3, 2, 4, 2, 3, 2, 4, 3):
            rect(s, xx, y + 10, w_, 28, fill=c)
            xx += w_ + 1.6
    elif tipo == "precio":
        ellipse(s, x + 24, y + 24, 17, fill=c)
        t(s, x + 7, y + 7, 34, 34, "$", size=24, bold=True, font=FONT_HEAD, color=BLANCO,
          align="center", anchor="middle", wrap=False)
    elif tipo == "variantes":
        for i in range(2):
            for j in range(2):
                rect(s, x + 9 + i * 16, y + 9 + j * 16, 13, 13, fill=None, line=c, line_w=2.5,
                     radius=3)
    elif tipo == "atributos":
        for k in range(3):
            ellipse(s, x + 12, y + 14 + k * 10, 2.6, fill=c)
            rect(s, x + 19, y + 12.5 + k * 10, 20, 3, fill=c)
    elif tipo == "imagen":
        rect(s, x + 7, y + 10, 34, 28, fill=None, line=c, line_w=3, radius=4)
        ellipse(s, x + 32, y + 18, 3.5, fill=c)
        triangle(s, x + 11, y + 22, 18, 13, color=c)
    elif tipo == "monitor":
        rect(s, x + 4, y + 6, 40, 28, fill=None, line=c, line_w=3.5, radius=3)
        rect(s, x + 21, y + 34, 6, 6, fill=c)
        rect(s, x + 13, y + 40, 22, 4, fill=c, radius=2)
    elif tipo == "fabrica":
        rect(s, x + 4, y + 24, 40, 18, fill=None, line=c, line_w=3)
        for k in range(3):
            triangle(s, x + 4 + k * 13, y + 13, 14, 12, color=c, rotation=0)
        rect(s, x + 34, y + 6, 7, 18, fill=c)
    elif tipo == "tienda":
        rect(s, x + 6, y + 22, 36, 20, fill=None, line=c, line_w=3)
        for k in range(4):
            ovalo(s, x + 4 + k * 10, y + 10, 11, 14, fill=c)
        rect(s, x + 4, y + 8, 40, 8, fill=c)
    elif tipo == "balanza":
        rect(s, x + 22.5, y + 8, 3, 32, fill=c)
        rect(s, x + 8, y + 12, 32, 3, fill=c)
        rect(s, x + 14, y + 40, 20, 3.5, fill=c, radius=1.5)
        ovalo(s, x + 2, y + 22, 16, 8, fill=c)
        ovalo(s, x + 30, y + 22, 16, 8, fill=c)


def estado_icono(s, tipo, cx, cy, r=20, fondo=None):
    """Íconos de los cuatro estados y de los veredictos (círculo de radio r)."""
    if tipo == "ok":
        ellipse(s, cx, cy, r, fill=fondo or VERDE)
        line(s, cx - r * 0.42, cy + r * 0.02, cx - r * 0.1, cy + r * 0.34, color=BLANCO,
             width=r * 0.2)
        line(s, cx - r * 0.12, cy + r * 0.34, cx + r * 0.45, cy - r * 0.3, color=BLANCO,
             width=r * 0.2)
    elif tipo == "nada":
        ellipse(s, cx, cy, r, fill="#9FB4CC")
        rect(s, cx - r * 0.45, cy - r * 0.09, r * 0.9, r * 0.18, fill=BLANCO)
    elif tipo == "mas":
        ellipse(s, cx, cy, r, fill=AZUL_C)
        rect(s, cx - r * 0.45, cy - r * 0.09, r * 0.9, r * 0.18, fill=BLANCO)
        rect(s, cx - r * 0.09, cy - r * 0.45, r * 0.18, r * 0.9, fill=BLANCO)
    elif tipo == "nic":
        ellipse(s, cx, cy, r, fill=None, line=AZUL, line_w=r * 0.16)
        line(s, cx - r * 0.62, cy - r * 0.62, cx + r * 0.62, cy + r * 0.62, color=AZUL,
             width=r * 0.16)
    elif tipo == "hidden":
        ovalo(s, cx - r, cy - r * 0.55, 2 * r, r * 1.1, fill=None, line_c=AZUL, lw=r * 0.12)
        ellipse(s, cx, cy, r * 0.28, fill=AZUL)
        line(s, cx - r * 0.8, cy + r * 0.7, cx + r * 0.8, cy - r * 0.7, color=AZUL,
             width=r * 0.14)
    elif tipo == "delete":
        rect(s, cx - r * 0.55, cy - r * 0.45, r * 1.1, r * 1.2, fill=None, line=AZUL,
             line_w=r * 0.13, radius=3)
        rect(s, cx - r * 0.75, cy - r * 0.68, r * 1.5, r * 0.14, fill=AZUL)
        rect(s, cx - r * 0.2, cy - r * 0.86, r * 0.4, r * 0.18, fill=AZUL)
        for k in (-1, 0, 1):
            rect(s, cx + k * r * 0.28 - r * 0.05, cy - r * 0.25, r * 0.1, r * 0.8, fill=AZUL)


# ------------------------------------------------------------------ productos
def tv(s, cx, cy, W):
    H = W * 0.62
    ellipse(s, cx - W * 0.28, cy, W * 0.32, fill="#C45BF5", fill_alpha=0.16)
    ellipse(s, cx + W * 0.28, cy, W * 0.32, fill="#38B6FF", fill_alpha=0.16)
    rect(s, cx - W / 2, cy - H / 2, W, H, fill="#101524", radius=6)
    sx, sy, sw, sh = cx - W / 2 + 6, cy - H / 2 + 6, W - 12, H - 40
    rect(s, sx, sy, sw, sh, fill="#2A1E5C")
    r0 = sh * 0.42
    for (fx, fy, fr, col, a) in ((0.24, 0.55, 1.0, "#E5487D", 0.8), (0.62, 0.42, 1.1, "#3FA9F5", 0.7),
                                 (0.45, 0.62, 0.8, "#9B5CF6", 0.75), (0.84, 0.66, 0.6, "#FFB547", 0.65)):
        rr = min(r0 * fr, sh * 0.48)
        ccx = min(max(sx + sw * fx, sx + rr), sx + sw - rr)
        ccy = min(max(sy + sh * fy, sy + rr), sy + sh - rr)
        ellipse(s, ccx, ccy, rr, fill=col, fill_alpha=a)
    t(s, sx + 10, sy + 8, 140, 24, "PHILIPS", size=18, bold=True, font=FONT_HEAD, color=BLANCO,
      wrap=False)
    t(s, sx, sy + sh / 2 - 18, sw, 40, "AMBILIGHT tv", size=max(22, W * 0.085), bold=True,
      font=FONT_HEAD, color=BLANCO, align="center", anchor="middle", wrap=False)
    rect(s, sx, sy + sh, sw, 28, fill="#0B0F1A")
    t(s, sx, sy + sh, sw, 28, "QLED  ·  Roku TV", size=18, bold=True, font=FONT_HEAD,
      color=BLANCO, align="center", anchor="middle", wrap=False)
    for k in (-1, 1):
        r_ = rect(s, cx + k * W * 0.36 - 3, cy + H / 2 - 2, 6, 30, fill="#1A1F2E")
        r_.rotation = 25 * k


def afeitadora(s, cx, cy):
    rect(s, cx + 10, cy - 100, 170, 250, fill="#D8EA3E", radius=6)
    rect(s, cx + 24, cy - 84, 112, 64, fill=BLANCO, radius=4)
    t(s, cx + 32, cy - 80, 100, 26, "PHILIPS", size=18, bold=True, font=FONT_HEAD, color=AZUL,
      wrap=False)
    t(s, cx + 32, cy - 54, 100, 26, "OneBlade", size=18, bold=True, font=FONT_HEAD,
      color=TINTA, wrap=False)
    t(s, cx + 70, cy + 30, 108, 100, [["Recorta"], ["Perfila"], ["Afeita"]], size=20, bold=True,
      font=FONT_HEAD, color=TINTA, line_spacing=1.15)
    rect(s, cx - 140, cy - 166, 112, 40, fill="#C9DE32", radius=6)
    rect(s, cx - 132, cy - 158, 96, 14, fill="#DDE2E7")
    rect(s, cx - 106, cy - 128, 44, 14, fill="#4A525C")
    rect(s, cx - 122, cy - 116, 76, 300, fill="#2E353F", radius=34)
    rect(s, cx - 120, cy - 70, 9, 210, fill="#C9DE32", radius=4)
    ellipse(s, cx - 84, cy + 40, 11, fill=None, line="#9AA3AE", line_w=2.5)


def freidora(s, cx, cy):
    ovalo(s, cx - 150, cy + 150, 300, 40, fill="#E3EAF3")
    rect(s, cx - 140, cy - 160, 280, 330, fill="#1F2125", radius=46)
    rect(s, cx - 140, cy - 160, 280, 76, fill="#2C2F35", radius=30)
    t(s, cx - 80, cy - 150, 160, 24, "PHILIPS", size=18, bold=True, font=FONT_HEAD,
      color=BLANCO, align="center", wrap=False)
    rect(s, cx - 72, cy - 112, 144, 84, fill="#0E0F12", radius=10)
    t(s, cx - 72, cy - 108, 144, 52, "180", size=36, bold=True, font=FONT_HEAD,
      color="#FF9A2E", align="center", anchor="middle", wrap=False)
    for k in range(6):
        rect(s, cx - 56 + k * 22, cy - 46, 10, 6, fill="#FF9A2E", radius=2)
    rect(s, cx - 140, cy - 4, 280, 3, fill="#3A3E45")
    rect(s, cx - 26, cy + 14, 52, 132, fill="#33373E", radius=12)


def hue(s, cx, cy):
    ellipse(s, cx + 40, cy - 60, 120, fill="#E58BF5", fill_alpha=0.18)
    rect(s, cx - 176, cy - 160, 214, 230, fill="#1E1B33", radius=8)
    t(s, cx - 160, cy - 140, 180, 26, "PHILIPS", size=18, bold=True, font=FONT_HEAD,
      color=BLANCO, wrap=False)
    t(s, cx - 160, cy - 112, 180, 44, "hue", size=36, bold=True, font=FONT_HEAD,
      color=BLANCO, wrap=False)
    t(s, cx - 160, cy - 62, 180, 50, [["White and Color"], ["Ambiance"]], size=18, font=TXT,
      color=BLANCO, line_spacing=1.1)
    for k, col in enumerate(("#FF5A5F", "#FFB547", "#F7E04B", "#4FC08D", "#3FA9F5", "#9B5CF6")):
        rect(s, cx - 160 + k * 24, cy + 16, 24, 6, fill=col)
    rect(s, cx - 166, cy + 96, 112, 100, fill="#F7F8FA", line=BORDE, line_w=1.5, radius=18)
    ellipse(s, cx - 110, cy + 146, 22, fill=None, line="#36C5D8", line_w=4)
    for k, bx in enumerate((cx - 8, cx + 66, cx + 140)):
        by = cy + 54 + (k % 2) * 10
        ellipse(s, bx, by, 38, fill="#F0B5F7")
        ellipse(s, bx - 8, by - 10, 18, fill="#FBE3FD", fill_alpha=0.8)
        rect(s, bx - 20, by + 30, 40, 26, fill="#F4F5F7", line=BORDE, line_w=1)
        rect(s, bx - 14, by + 56, 28, 28, fill="#B9C0C9", radius=4)
        for j in range(2):
            rect(s, bx - 14, by + 64 + j * 9, 28, 2, fill="#8E97A3")


def cepillo(s, cx, cy):
    rect(s, cx - 186, cy - 120, 176, 270, fill="#1D4FA8", radius=8)
    ellipse(s, cx - 70, cy + 70, 80, fill="#5FA8FF", fill_alpha=0.25)
    rect(s, cx - 172, cy - 106, 124, 64, fill=BLANCO, radius=4)
    t(s, cx - 164, cy - 102, 116, 26, "PHILIPS", size=18, bold=True, font=FONT_HEAD,
      color=AZUL, wrap=False)
    t(s, cx - 164, cy - 76, 116, 26, "sonicare", size=18, bold=True, font=FONT_HEAD,
      color=TINTA, wrap=False)
    t(s, cx - 172, cy - 26, 160, 26, "ProtectiveClean", size=18, font=TXT, color=BLANCO,
      wrap=False)
    t(s, cx - 172, cy + 2, 160, 40, "5100", size=30, bold=True, font=FONT_HEAD, color=BLANCO,
      wrap=False)
    rect(s, cx + 96, cy - 96, 82, 252, fill=BLANCO, line=BORDE, line_w=1.5, radius=38)
    rect(s, cx + 4, cy + 150, 78, 22, fill="#EEF1F5", line=BORDE, line_w=1, radius=8)
    rect(s, cx + 22, cy - 128, 42, 290, fill=BLANCO, line=BORDE, line_w=1.5, radius=20)
    rect(s, cx + 31, cy - 176, 24, 54, fill=BLANCO, line=BORDE, line_w=1.5, radius=10)
    for k, col in enumerate(("#3E8EDE", "#4FC08D", "#3E8EDE")):
        rect(s, cx + 34, cy - 170 + k * 8, 18, 6, fill=col, radius=2)
    rect(s, cx + 37, cy - 40, 12, 30, fill="#DCE3EA", radius=5)


PRODUCTOS = {"tv": lambda s: tv(s, IMG[0] + IMG[2] / 2, IMG[1] + 210, 350),
             "afeitadora": lambda s: afeitadora(s, IMG[0] + IMG[2] / 2, IMG[1] + 240),
             "freidora": lambda s: freidora(s, IMG[0] + IMG[2] / 2, IMG[1] + 230),
             "hue": lambda s: hue(s, IMG[0] + IMG[2] / 2, IMG[1] + 220),
             "cepillo": lambda s: cepillo(s, IMG[0] + IMG[2] / 2, IMG[1] + 230)}


# ------------------------------------------------------------------ comercio
def barra_comercio(s, d):
    x, y, w = MX, MY, MW
    rect(s, x, y, w, 70, fill=d["barra"])
    rect(s, x, y + 70, w, 30, fill=d["nav"])
    wm = d["marca_comercio"]
    if wm == "amazon":
        t(s, x + 26, y, 220, 70, "amazon", size=36, bold=True, font=FONT_HEAD, color=BLANCO,
          anchor="middle", wrap=False)
    elif wm == "mediamarkt":
        t(s, x + 26, y, 260, 70, "MediaMarkt", size=32, bold=True, font=FONT_HEAD,
          color=BLANCO, anchor="middle", italic=True, wrap=False)
    elif wm == "falabella":
        rect(s, x + 26, y + 15, 40, 40, fill="#AAD500", radius=8)
        t(s, x + 26, y + 15, 40, 40, "f", size=28, bold=True, font=FONT_HEAD, color=BLANCO,
          align="center", anchor="middle", wrap=False)
        t(s, x + 76, y, 220, 70, "falabella.com", size=26, bold=True, font=FONT_HEAD,
          color=BLANCO, anchor="middle", wrap=False)
    elif wm == "mercadolibre":
        t(s, x + 26, y + 6, 240, 60, [["mercado"], ["libre"]], size=24, bold=True,
          font=FONT_HEAD, color="#2D3277", line_spacing=0.92)
    elif wm == "bestbuy":
        t(s, x + 26, y + 6, 150, 60, [["BEST"], ["BUY"]], size=24, bold=True, font=FONT_HEAD,
          color=BLANCO, line_spacing=0.92)
        rect(s, x + 110, y + 40, 26, 16, fill="#FFE000")
    sx, sw = x + 330, 540
    rect(s, sx, y + 15, sw, 40, fill=BLANCO, radius=8)
    if d.get("buscar"):
        t(s, sx + 18, y + 15, sw - 90, 40, d["buscar"], size=18, color="#8A96A8",
          anchor="middle", wrap=False)
    rect(s, sx + sw - 54, y + 15, 54, 40, fill=d["lupa"], radius=8)
    ellipse(s, sx + sw - 30, y + 32, 8, fill=None, line=TINTA, line_w=3)
    line(s, sx + sw - 24, y + 38, sx + sw - 17, y + 45, color=TINTA, width=3)
    ic = d["iconos"]
    ux = x + w - 150
    ellipse(s, ux, y + 26, 8, fill=None, line=ic, line_w=2.5)
    rect(s, ux - 13, y + 38, 26, 14, fill=None, line=ic, line_w=2.5, radius=6)
    cx_ = x + w - 80
    rect(s, cx_ - 14, y + 24, 30, 16, fill=None, line=ic, line_w=2.5)
    line(s, cx_ - 22, y + 18, cx_ - 14, y + 24, color=ic, width=2.5)
    ellipse(s, cx_ - 8, y + 47, 3.5, fill=ic)
    ellipse(s, cx_ + 10, y + 47, 3.5, fill=ic)
    for k in range(7):
        rect(s, x + 30 + k * 152, y + 82, 104, 6, fill=d["nav_txt"], fill_alpha=0.55, radius=3)


def miniaturas(s, col):
    for k in range(4):
        y = MY + 124 + k * 80
        rect(s, MX + 20, y, 66, 66, fill=BLANCO, line=AZUL_C if k == 0 else BORDE,
             line_w=2.5 if k == 0 else 1.5, radius=8)
        if k < 3:
            rect(s, MX + 36, y + 14 + k * 3, 34, 38 - k * 6, fill=col, radius=4,
                 fill_alpha=1 - 0.25 * k)
        else:
            ellipse(s, MX + 53, y + 33, 18, fill="#2B2F36")
            triangle(s, MX + 47, y + 25, 16, 16, color=BLANCO, rotation=90)


def estrellas(s, x, cy, valor, r=11):
    for k in range(5):
        lleno = valor - k
        estrella(s, x + r + k * (2 * r + 4), cy, r,
                 color=AMARILLO if lleno >= 0.75 else ("#F2C94C" if lleno >= 0.25 else "#D6DDE6"),
                 alpha=1.0 if lleno >= 0.75 or lleno < 0.25 else 0.6)
    return 5 * (2 * r + 4)


# ------------------------------------------------------------------ encabezado
def encabezado(s, codigo, eyebrow, titulo, subtitulo):
    header(s, "Antecedentes")
    with colores_literales():
        rect(s, 96, 164, 96, 46, fill=AMARILLO, radius=6)
        t(s, 96, 164, 96, 46, codigo, size=24, bold=True, font=FONT_HEAD, align="center",
          anchor="middle", wrap=False)
        t(s, 214, 158, 1200, 28, eyebrow.upper(), size=18, bold=True, font=FONT_HEAD,
          color=ORO, spacing=1.6, wrap=False)
        t(s, 214, 184, 1000, 54, titulo, size=40, bold=True, font=FONT_HEAD, wrap=False)
        t(s, 1124, 184, 700, 54, subtitulo, size=30, bold=True, font=FONT_HEAD, color=AZUL,
          align="right", anchor="middle", wrap=False)


# ------------------------------------------------------------------ anatomía
LEYENDA = [("marca", "Marca"), ("titulo", "Título"), ("codigo", "Código"),
           ("precio", "Estado / precio"), ("variantes", "Variantes"),
           ("atributos", "Atributos"), ("imagen", "Imagen")]
CAMPOS = {"marca": (None, "dentro del título"), "titulo": ("RetailerProductName", None),
          "codigo": ("RetailerProductId", None), "precio": ("Stock · Price", None),
          "variantes": (None, "solo en la página"), "atributos": (None, "solo en la página"),
          "imagen": ("RetailerProductImageUrl", None)}


def _chips(s, x, y, tokens, h=44, size=20, gap=10, estilo="titulo"):
    for tok, es_codigo in tokens:
        font = FONT_MONO if es_codigo else FONT_HEAD
        w = text_width(tok, size, font, not es_codigo) + 30
        if estilo == "titulo":
            fill, borde, col = ("#FFE680", AMARILLO, TINTA) if es_codigo else (CHIP, AZUL_C, AZUL)
        else:
            fill, borde, col = BLANCO, BORDE, TINTA_2
        rect(s, x, y, w, h, fill=fill, line=borde, line_w=2, radius=10)
        t(s, x, y, w, h, tok, size=size, bold=not es_codigo, font=font, color=col,
          align="center", anchor="middle", wrap=False)
        x += w + gap
    return x


def _ancho_chips(tokens, size, gap=10):
    return sum(text_width(tok, size, FONT_MONO if c else FONT_HEAD, not c) + 30 + gap
               for tok, c in tokens)


def anatomia(prs, d, nota, num=None):
    s = add_slide(prs)
    if num:
        s._num = num
    encabezado(s, d["codigo"], "Antecedente 02 · La extracción automática",
                "Anatomía de una página retailer", d["subtitulo"])
    with colores_literales():
        # ---- página esquematizada
        rect(s, MX, MY, MW, MH, fill=BLANCO, line=BORDE, line_w=2, radius=14)
        barra_comercio(s, d)
        miniaturas(s, d["color_producto"])
        PRODUCTOS[d["producto"]](s)
        y = MY + 116
        marcas = {}
        # marca
        t(s, IX, y, IW - 20, 36, d["marca"], size=28 if len(d["marca"]) < 12 else 22,
          bold=True, font=FONT_HEAD, color=AZUL_C, anchor="middle", wrap=False)
        wm = text_width(d["marca"], 28 if len(d["marca"]) < 12 else 22, FONT_HEAD, True)
        marcas["marca"] = (y + 18, IX + wm + 10)
        y += 40
        # título
        lineas = wrap_lines(d["titulo"], 24, IW - 20, FONT_HEAD, True)
        t(s, IX, y, IW - 10, 30 * len(lineas), [[ln] for ln in lineas], size=24, bold=True,
          font=FONT_HEAD, line_spacing=1.2)
        wt = max(text_width(ln, 24, FONT_HEAD, True) for ln in lineas)
        marcas["titulo"] = (y + 15 * len(lineas), IX + wt + 10)
        y += 30 * len(lineas) + 6
        # calificación
        xx = IX
        if d.get("nota_valor"):
            t(s, xx, y, 60, 28, d["nota_valor"], size=20, bold=True, font=FONT_HEAD,
              anchor="middle", wrap=False)
            xx += text_width(d["nota_valor"], 20, FONT_HEAD, True) + 10
        xx += estrellas(s, xx, y + 14, d["estrellas"]) + 8
        t(s, xx, y, 160, 28, d["opiniones"], size=19, color=AZUL_C, anchor="middle",
          wrap=False)
        y += 36
        # código
        if d.get("codigo_txt"):
            t(s, IX, y, IW - 20, 26, d["codigo_txt"], size=18, font=FONT_MONO, color=TINTA_2,
              anchor="middle", wrap=False)
            wc = text_width(d["codigo_txt"], 18, FONT_MONO)
        else:
            rect(s, IX, y + 6, 330, 9, fill="#D6DDE6", radius=4)
            rect(s, IX, y + 19, 230, 6, fill="#E3EAF3", radius=3)
            wc = 330
        marcas["codigo"] = (y + 13, IX + wc + 10)
        y += 34 if d.get("envio") else 38
        # estado y precio
        ph = 94 + (28 if d.get("envio") else 0)
        rect(s, IX, y, IW - 10, ph, fill=BLANCO, line=BORDE, line_w=1.5, radius=12)
        t(s, IX + 20, y + 10, 220, 26, d["estado"], size=20, bold=True, color=VERDE,
          wrap=False)
        t(s, IX + 20, y + 36, 260, 46, d["precio"], size=34, bold=True, font=FONT_HEAD,
          anchor="middle", wrap=False)
        bw = text_width(d["cta"], 19, FONT_HEAD, True) + 76
        bx = IX + IW - 30 - bw
        rect(s, bx, y + 24, bw, 48, fill=d["cta_color"], radius=8)
        cc = d.get("cta_txt", TINTA)
        rect(s, bx + 16, y + 40, 20, 12, fill=None, line=cc, line_w=2)
        ellipse(s, bx + 21, y + 58, 2.5, fill=cc)
        ellipse(s, bx + 32, y + 58, 2.5, fill=cc)
        t(s, bx + 46, y + 24, bw - 56, 48, d["cta"], size=19, bold=True, font=FONT_HEAD,
          color=cc, anchor="middle", wrap=False)
        if d.get("envio"):
            t(s, IX + 20, y + 88, IW - 50, 26, d["envio"], size=18, bold=True, color=VERDE,
              wrap=False)
        marcas["precio"] = (y + ph / 2, None)
        y += ph + 12
        # variantes
        t(s, IX, y, IW - 20, 26, d["var_label"], size=19, bold=True, wrap=False)
        y += 30
        xx = IX
        if d.get("colores"):
            for k, col in enumerate(d["colores"]):
                if k == 0:
                    ellipse(s, xx + 21, y + 19, 21, fill=None, line=AZUL_C, line_w=3)
                ellipse(s, xx + 21, y + 19, 14, fill=col, line=BORDE, line_w=1.5)
                xx += 54
        else:
            for txt_, sel in d["variantes"]:
                w = text_width(txt_, 19, FONT_HEAD, sel) + 34
                rect(s, xx, y, w, 38, fill=CHIP if sel else BLANCO,
                     line=AZUL_C if sel else BORDE, line_w=2.5 if sel else 1.5, radius=8)
                t(s, xx, y, w, 38, txt_, size=19, bold=sel, font=FONT_HEAD,
                  color=AZUL if sel else TINTA_2, align="center", anchor="middle", wrap=False)
                xx += w + 12
        marcas["variantes"] = (y + 19, xx + 6)
        y += 50
        # atributos
        rh = 29 if len(d["atributos"]) <= 3 else (25 if d.get("envio") else 27)
        y0a = y
        for k, (clave, valor) in enumerate(d["atributos"]):
            yy = y + k * rh
            rect(s, IX, yy + rh - 1, IW - 10, 1, fill=FILETE)
            t(s, IX, yy, 250, rh, clave, size=18, bold=True, anchor="middle", wrap=False)
            t(s, IX + 260, yy, IW - 270, rh, valor, size=18, color=TINTA_2, anchor="middle",
              wrap=False)
        marcas["atributos"] = (y0a + rh * len(d["atributos"]) / 2, None)
        yfin = y0a + rh * len(d["atributos"])
        assert yfin <= MY + MH - 8, (d["codigo"], yfin)
        # marcadores numerados
        for n, (clave, _) in enumerate(LEYENDA[:6], 1):
            cy, xg = marcas[clave]
            if xg:
                guia(s, xg, cy, MARCA_X - 20)
            marcador(s, MARCA_X, cy, n)
        marcador(s, IMG[0] + IMG[2] - 14, IMG[1] + IMG[3] - 16, 7)

        # ---- leyenda: qué parte llega al dataset
        t(s, LX, MY - 2, LW, 28, "QUÉ PARTE LLEGA AL DATASET", size=18, bold=True,
          font=FONT_HEAD, color=ORO, spacing=1.6, wrap=False)
        ih, gap = 76, 8.5
        for n, (clave, nombre) in enumerate(LEYENDA, 1):
            yy = MY + 34 + (n - 1) * (ih + gap)
            campo, nota_campo = CAMPOS[clave]
            rect(s, LX, yy, LW, ih, fill=TARJETA, line=BORDE, line_w=1.5, radius=12)
            marcador(s, LX + 30, yy + ih / 2, n)
            rect(s, LX + 60, yy + 12, 52, 52, fill=BLANCO, line=BORDE, line_w=1.5, radius=10)
            icono(s, clave, LX + 62, yy + 14)
            t(s, LX + 128, yy + 8, LW - 150, 32, nombre, size=24, bold=True, font=FONT_HEAD,
              anchor="middle", wrap=False)
            if campo:
                w = text_width(campo, 18, FONT_MONO) + 22
                rect(s, LX + 128, yy + 42, w, 26, fill=CHIP, line=AZUL_C, line_w=1, radius=6)
                t(s, LX + 128, yy + 42, w, 26, campo, size=18, font=FONT_MONO, color=AZUL,
                  align="center", anchor="middle", wrap=False)
            else:
                t(s, LX + 128, yy + 40, LW - 150, 28, nota_campo, size=18, italic=True,
                  color=TINTA_2, anchor="middle", wrap=False)

        # ---- banda: información útil en el título
        by, bh = 902, 108
        rect(s, 96, by, 1728, bh, fill=TARJETA, line=AZUL_C, line_w=1.5, radius=14)
        icono(s, "monitor", 120, by + 30)
        t(s, 188, by + 14, 250, 80, [["El título trae"], ["la información útil"]], size=22,
          bold=True, font=FONT_HEAD, line_spacing=1.15, anchor="middle")
        x0 = 452
        rect(s, x0 - 16, by + 20, 2, bh - 40, fill=BORDE)
        disp = 1824 - 24 - x0
        size = 20
        ficha_lbl = "Solo en la ficha:"
        while size > 18:
            w_tot = (_ancho_chips(d["tokens_titulo"], size) + 20 +
                     text_width(ficha_lbl, 18, TXT, True) + 14 + _ancho_chips(d["tokens_ficha"], size))
            if w_tot <= disp:
                break
            size -= 1
        xx = _chips(s, x0, by + 32, d["tokens_titulo"], size=size)
        xx += 10
        t(s, xx, by + 32, text_width(ficha_lbl, 18, TXT, True) + 8, 44, ficha_lbl, size=18,
          bold=True, color=TINTA_2, anchor="middle")
        xx += text_width(ficha_lbl, 18, TXT, True) + 14
        xfin = _chips(s, xx, by + 32, d["tokens_ficha"], size=size, estilo="ficha")
        assert xfin <= 1824 - 14, (d["codigo"], xfin)
    notes(s, nota)
    return s


COMERCIOS = [
    dict(codigo="02A", subtitulo="Amazon · Philips TV", marca_comercio="amazon",
         barra="#131921", nav="#232F3E", nav_txt="#9FB4CC", lupa="#FEBD69", iconos=BLANCO,
         producto="tv", color_producto="#7A4FE0", marca="PHILIPS",
         titulo="PHILIPS 55 pulgadas 4K QLED Roku TV, serie 7985, Ambilight, HDR",
         nota_valor="4.4", estrellas=4.4, opiniones="(40)", codigo_txt=None,
         estado="Disponible", precio="US$390.64", cta="Agregar al Carrito", cta_color="#FFD21F",
         var_label="Tamaño de pantalla:", variantes=[('50"', False), ('65"', False), ('55"', True)],
         atributos=[("Tecnología de pantalla", "QLED"), ("Resolución", "4K UHD (2160p)"),
                    ("Frecuencia de actualización", "60 Hz")],
         tokens_titulo=[('55"', False), ("4K QLED", False), ("Roku TV", False),
                        ("Ambilight", False), ("HDR", False)],
         tokens_ficha=[("60 Hz", False)],
         nota=("Así se ve lo que el equipo de scraping extrae. Una página de Amazon tiene siete "
               "partes: marca, título, código del retailer, estado y precio, variantes, "
               "atributos e imagen. Al dataset llegan el título, el código, el stock, el precio "
               "y la imagen; la marca, las variantes y los atributos solo sobreviven si están "
               "escritos en el título. Por eso el título es la señal principal: aquí trae 55 "
               "pulgadas, 4K QLED, Roku TV, Ambilight y HDR. Los 60 Hz, en cambio, solo están "
               "en la ficha.")),
    dict(codigo="02B", subtitulo="MediaMarkt · Philips OneBlade", marca_comercio="mediamarkt",
         barra="#DF0000", nav="#3A3A3A", nav_txt="#D9D9D9", lupa="#F2F2F2", iconos=BLANCO,
         buscar="Buscar productos, marcas...", producto="afeitadora", color_producto="#C9DE32",
         marca="PHILIPS", titulo="Philips OneBlade QP2724/10 recorta, perfila y afeita",
         nota_valor="4,6", estrellas=4.6, opiniones="(2.347)",
         codigo_txt="SKU: QP2724/10  |  EAN: 8710103990520",
         estado="En stock", precio="49,99 €", cta="Añadir al carrito", cta_color="#DF0000",
         cta_txt=BLANCO, var_label="Versión:", variantes=[("QP2724/10", True), ("QP2824/10", False)],
         atributos=[("Tipo de producto", "Recortadora corporal"), ("Tecnología", "OneBlade"),
                    ("Uso", "Recorta, perfila y afeita"), ("Autonomía", "Hasta 45 min")],
         tokens_titulo=[("OneBlade", False), ("QP2724/10", True), ("Recorta", False),
                        ("Perfila", False), ("Afeita", False)],
         tokens_ficha=[("45 min", False)],
         nota=("La misma anatomía en MediaMarkt, con una OneBlade. Este título trae el código "
               "del modelo, QP2724/10, que es la señal más fuerte para encontrar el producto en "
               "el catálogo, además de los tres usos. La autonomía de 45 minutos solo aparece "
               "en la ficha.")),
    dict(codigo="02C", subtitulo="Falabella · Philips Airfryer", marca_comercio="falabella",
         barra="#343E48", nav="#4A5561", nav_txt="#C9D1DA", lupa="#FFD21F", iconos=BLANCO,
         producto="freidora", color_producto="#2C2F35", marca="PHILIPS",
         titulo="Freidora de aire Philips Airfryer Essential HD9252/91",
         nota_valor=None, estrellas=4.5, opiniones="(1.245)", codigo_txt="SKU: 4528061",
         estado="Disponible", precio="S/ 399.00", cta="Agregar al Carro", cta_color="#FFD21F",
         var_label="Capacidad:", variantes=[("2.6 L", False), ("4.1 L", True), ("6.2 L", False)],
         atributos=[("Tipo", "Airfryer digital"), ("Capacidad", "4.1 L"),
                    ("Tecnología", "Rapid Air")],
         tokens_titulo=[("Freidora de aire", False), ("Airfryer", False), ("Essential", False),
                        ("HD9252/91", True)],
         tokens_ficha=[("Digital", False), ("4.1 L", False), ("Rapid Air", False)],
         nota=("En Falabella, una Airfryer. El título trae la categoría, la línea Essential y el "
               "código HD9252/91. Pero la capacidad de 4,1 litros y la tecnología Rapid Air no "
               "están en el título: solo en la ficha, que no llega al dataset. El código del "
               "comercio, 4528061, tampoco es el de Philips.")),
    dict(codigo="02D", subtitulo="Mercado Libre · Philips Hue", marca_comercio="mercadolibre",
         barra="#FFE600", nav="#F4F4F4", nav_txt="#B9C0C9", lupa="#F4F4F4", iconos="#2D3277",
         producto="hue", color_producto="#E9A6F2", marca="Signify · Philips Hue",
         titulo="Kit Philips Hue White and Color Ambiance E27",
         nota_valor="4.8", estrellas=4.8, opiniones="(2.356)",
         codigo_txt="Código: 9290024685  (EAN: 8719514291355)",
         estado="Disponible", precio="S/ 899.00", cta="Comprar ahora", cta_color="#3483FA",
         cta_txt=BLANCO, envio="Envío gratis · Llega mañana",
         var_label="Modelo / Pack:", variantes=[("Kit (3 focos + Hue Bridge)", True),
                                                ("Foco individual", False)],
         atributos=[("Tecnología", "Hue (Smart)"), ("Base / Casquillo", "E27"),
                    ("Color de luz", "White & Color Ambiance"), ("Tipo de foco", "LED")],
         tokens_titulo=[("Kit", False), ("Hue", False), ("White and Color Ambiance", False),
                        ("E27", False)],
         tokens_ficha=[("Smart", False), ("LED", False)],
         nota=("En Mercado Libre, un kit Philips Hue. Aquí la marca aparece como Signify, el "
               "fabricante detrás de Philips. El título describe el kit, la gama White and "
               "Color Ambiance y el casquillo E27; que es inteligente y LED solo figura en la "
               "ficha.")),
    dict(codigo="02E", subtitulo="Best Buy · Philips Sonicare", marca_comercio="bestbuy",
         barra="#0046BE", nav="#003B9E", nav_txt="#9DB8E8", lupa="#FFE000", iconos=BLANCO,
         buscar="Buscar en Best Buy", producto="cepillo", color_producto="#DCE3EA",
         marca="PHILIPS", titulo="Philips Sonicare ProtectiveClean 5100 electric toothbrush",
         nota_valor="4.6", estrellas=4.6, opiniones="(8,245)", codigo_txt="SKU: 6423037",
         estado="Disponible", precio="US$129.99", cta="Agregar al carrito", cta_color="#FFE000",
         var_label="Color: Blanco", colores=["#FFFFFF", "#1E1E1E", "#F7C6D9", "#1B2F6B"],
         atributos=[("Tipo", "Cepillo eléctrico"), ("Serie", "ProtectiveClean"),
                    ("Modelo", "5100"), ("Recargable", "Sí")],
         tokens_titulo=[("Sonicare", False), ("ProtectiveClean", False), ("5100", False),
                        ("electric toothbrush", False)],
         tokens_ficha=[("Recargable", False)],
         nota=("En Best Buy, un cepillo Sonicare. El título está en inglés y trae la línea, la "
               "serie y el modelo, ProtectiveClean 5100; que es recargable solo figura en la "
               "ficha. Cinco comercios, cinco diseños distintos y la misma anatomía: lo que "
               "todos comparten es el título, y de él depende la correspondencia.")),
]


# ------------------------------------------------------------------ validación
CRITERIOS = [("Marca", "Philips = PHILIPS", "ok"),
             ("Modelo / serie", "serie 7985 en ambos", "ok"),
             ("Tamaño", '55" = 55 pulgadas: misma medida, otra escritura', "ok"),
             ("Tecnología", "QLED · Roku TV · UHD 2160p", "ok"),
             ("Código", "ninguno de los dos títulos lo trae", "nada"),
             ("Características", "el retailer agrega Ambilight y HDR", "mas")]
ESTADOS = [("ok", "MATCH", "Corresponde a un producto del catálogo"),
           ("nic", "NIC", "Philips, pero fuera del catálogo o sin identificadores suficientes"),
           ("hidden", "HIDDEN", "Competidor, marcas mezcladas o reglas comerciales distintas"),
           ("delete", "DELETE", "La publicación fue dada de baja")]
NOTA_VALIDACION = (
    "Con esa información, el analista compara la publicación con el catálogo del fabricante, "
    "criterio por criterio: marca, modelo, tamaño, tecnología, código y características. Aquí "
    "coinciden la marca, la serie, el tamaño y la tecnología, aunque estén escritos distinto: "
    "55 pulgadas es lo mismo que 55\". El código no aparece en ninguno de los dos títulos, y el "
    "retailer agrega Ambilight y HDR, que no contradicen al catálogo. La decisión es Match. Si "
    "el producto fuera Philips pero no estuviera en el catálogo sería NIC; si fuera de un "
    "competidor, Hidden; y si la publicación estuviera dada de baja, Delete.")


def _tarjeta_producto(s, x, y, w, h, icono_tipo, rotulo, marca, marca_color, titulo, tsize):
    rect(s, x, y, w, h, fill=BLANCO, line=AZUL_C, line_w=2, radius=16)
    rect(s, x + 24, y + 20, 56, 56, fill=CHIP, radius=12)
    icono(s, icono_tipo, x + 28, y + 24)
    t(s, x + 96, y + 20, w - 120, 56, rotulo, size=20, bold=True, font=FONT_HEAD,
      spacing=2, anchor="middle", wrap=False)
    t(s, x + 28, y + 96, w - 56, 46, marca, size=34, bold=True, font=FONT_HEAD,
      color=marca_color, anchor="middle", wrap=False)
    lineas = wrap_lines(titulo, tsize, w - 56, TXT, True)
    t(s, x + 28, y + 148, w - 56, 30 * len(lineas), [[ln] for ln in lineas], size=tsize,
      bold=True, font=TXT, line_spacing=1.2)
    tv(s, x + w / 2, y + h - 138, 300)


def validacion(prs, nota=NOTA_VALIDACION, num=None):
    s = add_slide(prs)
    if num:
        s._num = num
    encabezado(s, "03", "Antecedente 03 · La comparación manual",
               "Validación de correspondencia", "Catálogo frente a publicación")
    with colores_literales():
        y0, h0 = 262, 486
        _tarjeta_producto(s, 96, y0, 520, h0, "fabrica", "CATÁLOGO DEL FABRICANTE", "PHILIPS",
                          AZUL_C, 'Philips 55" QLED Roku TV serie 7985, UHD 2160p', 24)
        _tarjeta_producto(s, 1304, y0, 520, h0, "tienda", "PUBLICACIÓN DEL RETAILER", "amazon",
                          TINTA, "PHILIPS 55 pulgadas 4K QLED Roku TV, serie 7985, UHD "
                          "2160p, Ambilight, HDR", 22)
        # centro: criterio por criterio
        cx0, cw0 = 656, 608
        rect(s, cx0, y0, cw0, h0, fill=TARJETA, line=BORDE, line_w=1.5, radius=16)
        rect(s, cx0 + 24, y0 + 16, 52, 52, fill=BLANCO, line=BORDE, line_w=1.5, radius=10)
        icono(s, "balanza", cx0 + 26, y0 + 18)
        t(s, cx0 + 92, y0 + 16, cw0 - 120, 52, "CRITERIO POR CRITERIO", size=20, bold=True,
          font=FONT_HEAD, color=ORO, spacing=2, anchor="middle", wrap=False)
        rh = 66
        for k, (crit, veredicto, est) in enumerate(CRITERIOS):
            yy = y0 + 86 + k * rh
            rect(s, cx0 + 16, yy, cw0 - 32, rh - 6, fill=BLANCO, line=BORDE, line_w=1, radius=10)
            estado_icono(s, est, cx0 + 50, yy + (rh - 6) / 2, r=17)
            t(s, cx0 + 82, yy + 4, cw0 - 110, 28, crit, size=21, bold=True, font=FONT_HEAD,
              anchor="middle", wrap=False)
            t(s, cx0 + 82, yy + 31, cw0 - 110, 26, veredicto, size=18, color=TINTA_2,
              anchor="middle", wrap=False)
        # flechas hacia el centro
        arrow_shape(s, 618, y0 + h0 / 2 - 18, 34, 36, color=AZUL_C)
        flecha = arrow_shape(s, 1268, y0 + h0 / 2 - 18, 34, 36, color=AZUL_C)
        flecha.rotation = 180
        # decisión
        ccy = y0 + h0 + 36
        ellipse(s, 960, ccy, 26, fill=BLANCO, line=AZUL_C, line_w=4)
        line(s, 948, ccy + 1, 956, ccy + 9, color=AZUL_C, width=4)
        line(s, 956, ccy + 9, 972, ccy - 8, color=AZUL_C, width=4)
        line(s, 960, y0 + h0, 960, ccy - 26, color=AZUL_C, width=2, dash="sysDot")
        cwd, gap = (1728 - 3 * 24) / 4, 24
        ty, th = 848, 150
        line(s, 96 + cwd / 2, ty - 26, 96 + 3 * (cwd + gap) + cwd / 2, ty - 26, color=AZUL_C,
             width=2, dash="sysDot")
        line(s, 960, ccy + 26, 960, ty - 26, color=AZUL_C, width=2, dash="sysDot")
        for k, (ic, nombre, desc) in enumerate(ESTADOS):
            x = 96 + k * (cwd + gap)
            line(s, x + cwd / 2, ty - 26, x + cwd / 2, ty, color=AZUL_C, width=2, dash="sysDot")
            elegido = k == 0
            rect(s, x, ty, cwd, th, fill=AZUL if elegido else BLANCO,
                 line=AMARILLO if elegido else BORDE, line_w=4 if elegido else 1.5, radius=16)
            if elegido:
                estado_icono(s, "ok", x + 54, ty + 50, r=26, fondo=AMARILLO)
                w_tag = text_width("ESTE CASO", 16, FONT_HEAD, True, 1.2) + 30
                rect(s, x + cwd - w_tag - 16, ty - 16, w_tag, 32, fill=AMARILLO, radius=6)
                t(s, x + cwd - w_tag - 16, ty - 16, w_tag, 32, "ESTE CASO", size=16, bold=True,
                  font=FONT_HEAD, align="center", anchor="middle", spacing=1.2, wrap=False)
            else:
                estado_icono(s, ic, x + 54, ty + 50, r=24)
            t(s, x + 96, ty + 24, cwd - 110, 52, nombre, size=30, bold=True, font=FONT_HEAD,
              color=BLANCO if elegido else TINTA, anchor="middle", wrap=False)
            t(s, x + 26, ty + 86, cwd - 46, 56, desc, size=18,
              color=BLANCO if elegido else TINTA_2, line_spacing=1.2)
    notes(s, nota)
    return s


# ------------------------------------------------------------------ orden en el mazo
def construir_extraccion(prs, numeros=None):
    """Las cinco anatomías (van después del antecedente 02)."""
    for k, d in enumerate(COMERCIOS):
        anatomia(prs, d, d["nota"], num=numeros[k] if numeros else None)


def construir_validacion(prs, numero=None):
    """La validación de correspondencia (va después del antecedente 03)."""
    validacion(prs, num=numero)
