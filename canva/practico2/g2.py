"""Grupo g2: OE2 · estructura y hallazgos del conjunto; OE3 · pipeline textual (P04-P07)."""

from pptx_kit import FONT_MONO, add_slide, ellipse, line, notes, rect, text, triangle
from theme import BLUE_TEXT, FONDO, MUTED, PANEL, PAPER, YELLOW
from componentes import (BLUE_LIGHT, CHIP, DARK, FONT_HEAD, FONT_TXT, PANEL_2, RED, bar, card,
                         chip, flecha, flecha_abajo, label, numbadge, subencabezado, tag,
                         text_width)

OE2 = "OE2 · Organizar el conjunto de datos"
OE3 = "OE3 · Pipeline de procesamiento textual"


# ----------------------------------------------------------------- utilidades
def _tag_w(s, size=18, pad=14):
    """Ancho que ocupará `tag(...)` con el mismo texto y tamaño."""
    return text_width(s.upper(), size, FONT_HEAD, True, spacing=1.2) + 2 * pad + 6


def _chip_fijo(s, x, y, w, h, txt, size=19, mono=True, color=YELLOW, fill=CHIP,
               border=BLUE_LIGHT, border_alpha=0.45):
    """Chip de ancho fijo con el texto centrado (ancho medido: cabe sin ajuste)."""
    font = FONT_MONO if mono else FONT_TXT
    rect(s, x, y, w, h, fill=fill, line=border, line_w=1, line_alpha=border_alpha, radius=6)
    text(s, x, y, w, h, txt, size=size, font=font, color=color, align="center",
         anchor="middle", wrap=False)


def _num(s, x, y, w, valor, size=48, color=YELLOW, align="left"):
    """Cifra en Montserrat negrita."""
    text(s, x, y, w, size * 1.25, valor, size=size, bold=True, font=FONT_HEAD, color=color,
         align=align, line_spacing=1.0)


def _txt(s, x, y, w, h, contenido, size=22, color=PAPER, bold=False, align="left",
         anchor="top", ls=1.2):
    text(s, x, y, w, h, contenido, size=size, font=FONT_TXT, color=color, bold=bold,
         align=align, anchor=anchor, line_spacing=ls)


def _titulo(s, x, y, w, h, contenido, size=26, color=PAPER, align="left", anchor="top"):
    text(s, x, y, w, h, contenido, size=size, bold=True, font=FONT_HEAD, color=color,
         align=align, anchor=anchor, line_spacing=1.15)


def _mono_runs(partes, size, base=PAPER):
    """Párrafo en Roboto Mono con tramos coloreados: [(texto, color), ...]."""
    return [[{"text": t, "color": c or base} for t, c in partes]]


def _segmentos_flecha(s, x, y, h, trozos, size, font=FONT_TXT, color=PAPER,
                      color_flecha=MUTED, gap=10, largo=26, alto=16):
    """Línea de texto cuyas «→» se dibujan como forma (Barlow y Roboto Mono no tienen el
    glifo). `trozos` es una lista de str o de listas de (texto, color); entre cada trozo va
    una flecha. Cada trozo es un cuadro de ancho medido. Devuelve el ancho total."""
    cx = x
    if len(trozos) == 1 and isinstance(trozos[0], str):
        text(s, x, y, 600, h, trozos[0], size=size, font=font, color=color, anchor="middle")
        return text_width(trozos[0], size, font)
    for k, tr in enumerate(trozos):
        partes = [(tr, None)] if isinstance(tr, str) else tr
        cadena = "".join(t for t, _ in partes)
        w = text_width(cadena, size, font)
        # holgura mínima: LibreOffice centra los cuadros sin ajuste de línea
        text(s, cx, y, w + 4, h, [[{"text": t, "color": c or color} for t, c in partes]],
             size=size, font=font, color=color, anchor="middle", wrap=False)
        cx += w + 2
        if k < len(trozos) - 1:
            flecha(s, cx + gap, y + h / 2, cx + gap + largo, color=color_flecha, h=alto)
            cx += 2 * gap + largo
    return cx - x


def _resalta(cadena, simbolos='/"', color=YELLOW):
    """Parte una cadena y colorea los símbolos de sintaxis (barra y comillas)."""
    partes, cur = [], ""
    for ch in cadena:
        if ch in simbolos:
            if cur:
                partes.append((cur, None))
                cur = ""
            partes.append((ch, color))
        else:
            cur += ch
    if cur:
        partes.append((cur, None))
    return partes


# ======================================================================= P04
def p04(prs, notas):
    """Láminas 54 + 55: del volcado a la unidad de análisis; lo ambiguo se marca."""
    s = add_slide(prs, bg_image=FONDO)
    subencabezado(s, OE2 + " · Estructurar el conjunto",
                  "Del volcado del portal a la unidad de análisis")

    # ---------------- izquierda: embudo volcado -> válido -> unidad canónica
    lx, lw = 96, 780
    top = 276
    label(s, lx, top, lw, "Filtrar y definir la identidad", size=18, color=YELLOW)
    y1, hs = top + 36, 132
    etapas = [("Volcado del portal", "129.507", "filas × 36 columnas", "12 snapshots de 2025",
               1.0),
              ("Conjunto de estudio válido", "127.093", None, None, 127093 / 129507)]
    conectores = [("Filtro base de calidad", ["Invalid", "IsDeleted", "MatchConfidence"],
                   "−2.414", None),
                  ("Unidad canónica", ["país + retailer + RetailerProductId"], None,
                   "llave de respaldo en 465 filas (0,37%)")]
    hc = 96
    y = y1
    for k, (rot, valor, l1, l2, frac) in enumerate(etapas):
        card(s, lx, y, lw, hs, accent=BLUE_LIGHT, accent_side="left")
        label(s, lx + 32, y + 18, 420, rot, size=18, color=MUTED)
        _num(s, lx + 32, y + 48, 280, valor, size=52, color=PAPER)
        if l1:
            _txt(s, lx + 330, y + 46, lw - 360, 30, l1, size=24)
            _txt(s, lx + 330, y + 78, lw - 360, 28, l2, size=20, color=MUTED)
        else:
            tag(s, lx + 330, y + 56, "98,14% conservado", size=18, h=38)
        bar(s, lx + 32, y + hs - 16, lw - 64, 6, frac, color=BLUE_LIGHT)
        # conector
        crot, chips, delta, nota_c = conectores[k]
        cy = y + hs
        flecha_abajo(s, lx + 62, cy + 8, cy + hc - 8, w=26)
        label(s, lx + 112, cy + 10, 420, crot, size=18, color=MUTED)
        cx = lx + 112
        for nm in chips:
            cx += chip(s, cx, cy + 42, nm, size=18) + 12
        if delta:
            text(s, lx + lw - 232, cy + 38, 200, 44, delta, size=30, bold=True, font=FONT_HEAD,
                 color=RED, align="right", anchor="middle")
        if nota_c:
            lw_rot = text_width(crot.upper(), 18, FONT_HEAD, True, spacing=1.5)
            _txt(s, lx + 112 + lw_rot + 10, cy + 8, lw - 112 - lw_rot - 40, 28,
                 "· " + nota_c, size=20, color=MUTED)
        y = cy + hc

    # unidad de análisis (resultado, con esquineros)
    y3 = y + 10
    h3 = 1000 - y3
    card(s, lx, y3, lw, h3, accent=YELLOW, brackets=True)
    pad3 = (h3 - 150) / 2
    label(s, lx + 32, y3 + pad3, 500, "Unidad de análisis", size=18, color=YELLOW)
    kp = [("111.269", "pares distintos"), ("110.706", "publicaciones retailer"),
          ("17.416", "productos oficiales")]
    colw = (lw - 64) / 3
    for k, (v, et) in enumerate(kp):
        kx = lx + 32 + k * colw
        if k:
            rect(s, kx - 16, y3 + pad3 + 46, 1.5, 100, fill=BLUE_LIGHT, fill_alpha=0.35)
        _num(s, kx, y3 + pad3 + 40, colw - 20, v, size=52, color=YELLOW)
        _txt(s, kx, y3 + pad3 + 114, colw - 24, 32, et, size=22)

    # ---------------- derecha: lo ambiguo se marca, no se borra
    rx, rw = 916, 908
    label(s, rx, top, rw, "Lo ambiguo se marca, no se borra", size=18, color=YELLOW)
    # etiquetas con texto oscuro: contraste ≥ 4,5:1 también sobre rojo y azul
    fen = [("8", "filas · 0,01%", "Duplicado exacto", "las 36 columnas idénticas",
            "Eliminar", RED, DARK, RED),
           ("26.592", "filas · 20,92%", "Repetición histórica", "el mismo par hasta en 11 meses",
            "Colapsar o ponderar", YELLOW, DARK, YELLOW),
           ("36,49%", "máximo · llave gruesa", "Co-ocurrencia por reuso",
            "llave gruesa, sin Retailer", "No es duplicado", BLUE_LIGHT, DARK, BLUE_TEXT)]
    rh, rg = 104, 12
    for k, (num, sub, nombre, desc, dec, col, tcol, ncol) in enumerate(fen):
        yy = y1 + k * (rh + rg)
        rect(s, rx, yy, rw, rh, fill=PANEL, line=BLUE_LIGHT, line_w=1.5, line_alpha=0.4)
        rect(s, rx, yy, 6, rh, fill=col)
        _num(s, rx + 30, yy + 12, 210, num, size=40, color=ncol)
        _txt(s, rx + 30, yy + 64, 210, 26, sub, size=18, color=MUTED)
        tw = _tag_w(dec)
        _titulo(s, rx + 256, yy + 18, rw - 256 - tw - 48, 34, nombre, size=24)
        _txt(s, rx + 256, yy + 56, rw - 256 - tw - 48, 30, desc, size=20, color=MUTED)
        tag(s, rx + rw - 28 - tw, yy + (rh - 38) / 2, dec, fill=col, color=tcol, size=18, h=38)

    sy = y1 + 3 * (rh + rg) + 8
    label(s, rx, sy, rw, "Se marca con su severidad", size=18, color=YELLOW)
    cy0 = sy + 36
    card(s, rx, cy0, rw, 1000 - cy0, accent=None)
    sev = [(["Id reutilizado entre retailers"], "severidad media", 8528, "8.528", False),
           (["Nombre", "varios oficiales"], "severidad media", 1227, "1.227", False),
           (["Id retailer", "varios oficiales"], "severidad alta", 889, "889", True),
           (["Unidad canónica", "varios oficiales"], "severidad alta · 1.001 filas", 263, "263",
            True)]
    n = len(sev)
    paso = (1000 - cy0 - 24) / n
    for k, (nombre, sv, v, vs, alta) in enumerate(sev):
        yy = cy0 + 14 + k * paso
        col = RED if alta else BLUE_LIGHT
        # la «→» del original se dibuja como forma (Barlow no tiene el glifo)
        _segmentos_flecha(s, rx + 30, yy, 28, nombre, 21, gap=8, largo=22, alto=14)
        _txt(s, rx + 30, yy + 29, 380, 26, sv, size=20, color=RED if alta else MUTED)
        bx, bw = rx + 420, rw - 420 - 140
        bar(s, bx, yy + 18, bw, 14, v / 8528, color=col)
        _num(s, rx + rw - 130, yy + 6, 100, vs, size=28, color=PAPER, align="right")

    notes(s, " ".join(notas[i] for i in (54, 55)))


# ======================================================================= P05
def p05(prs, notas):
    """Lámina 56: los tres hallazgos del análisis exploratorio y su consecuencia."""
    s = add_slide(prs, bg_image=FONDO)
    subencabezado(s, OE2 + " · Análisis exploratorio",
                  "Los tres hallazgos que condicionan todo lo demás")
    cw, gap = 560, 24
    top, ch = 276, 556
    dy, dh = 886, 120
    # los tres títulos a 24 px caben en una línea (el más largo mide 446 px de 460)
    titulos = ["Una fila no es un producto", "El código vive dentro del texto libre",
               "Lo que parece ruido es sintaxis"]
    consecuencias = [["La división train/test se hace por par,", "nunca por fila."],
                     ["Los identificadores no se comparan como",
                      "cadenas: se buscan dentro del título."],
                     ["Una limpieza estándar destruiría la señal",
                      "y borraría mercados enteros."]]
    xs = [96 + k * (cw + gap) for k in range(3)]
    for k, x in enumerate(xs):
        card(s, x, top, cw, ch, accent=YELLOW)
        numbadge(s, x + 28, top + 28, str(k + 1), size=40)
        _titulo(s, x + 80, top + 28, cw - 100, 40, titulos[k], size=24, anchor="middle")
        # consecuencia
        flecha_abajo(s, x + cw / 2, top + ch + 8, dy - 6, w=26)
        rect(s, x, dy, cw, dh, fill=PANEL_2, line=YELLOW, line_w=1.5, line_alpha=0.7)
        rect(s, x, dy, 6, dh, fill=YELLOW)
        label(s, x + 28, dy + 14, cw - 56, "Consecuencia", size=18, color=YELLOW)
        _txt(s, x + 28, dy + 44, cw - 56, 66, consecuencias[k], size=24, ls=1.15)
    iw = cw - 56

    # --- 1. una fila no es un producto: 42 -> 1
    x = xs[0]
    vy = top + 122
    chip(s, x + 28, vy, "NPX150/INT", size=20)
    gy = vy + 54
    cel, cg = 16, 6
    for i in range(42):
        r, c = divmod(i, 7)
        rect(s, x + 28 + c * (cel + cg), gy + r * (cel + cg), cel, cel, fill=BLUE_LIGHT,
             fill_alpha=0.85)
    gw, gh = 7 * cel + 6 * cg, 6 * cel + 5 * cg
    _txt(s, x + 28, gy + gh + 10, 260, 28, "42 filas · llave gruesa", size=20, color=MUTED)
    flecha(s, x + 28 + gw + 34, gy + gh / 2, x + 28 + gw + 130, h=30)
    qx, qs = x + 28 + gw + 160, 84
    rect(s, qx, gy + (gh - qs) / 2, qs, qs, fill=YELLOW, radius=6)
    text(s, qx, gy + (gh - qs) / 2, qs, qs, "1", size=48, bold=True, font=FONT_HEAD, color=DARK,
         align="center", anchor="middle", wrap=False)
    _txt(s, qx - 40, gy + gh + 10, qs + 80, 28, "producto", size=20, color=MUTED,
         align="center")
    # secundarias
    sy = top + 362
    _num(s, x + 28, sy, 170, "20,92%", size=36, color=YELLOW)
    _txt(s, x + 200, sy + 8, iw - 172, 30, "filas en pares repetidos", size=22)
    bar(s, x + 28, sy + 52, iw, 10, 0.2092, color=YELLOW)
    sy2 = sy + 84
    _num(s, x + 28, sy2, 170, "11", size=36, color=YELLOW)
    _txt(s, x + 200, sy2 + 8, iw - 172, 30, "meses distintos para un par", size=22)
    paso = iw / 12
    for m in range(12):
        cxm = x + 28 + paso * m + paso / 2
        if m < 11:
            ellipse(s, cxm, sy2 + 64, 9, fill=YELLOW)
        else:
            ellipse(s, cxm, sy2 + 64, 9, fill=CHIP, line=BLUE_LIGHT, line_w=1.5)

    # --- 2. el código vive dentro del texto libre
    x = xs[1]
    _num(s, x + 28, top + 116, iw, "90,19%", size=72, color=YELLOW)
    _txt(s, x + 28, top + 206, iw, 30, "títulos con token tipo código", size=22)
    by, bh = top + 266, 108
    rect(s, x + 28, by, iw, bh, fill=CHIP, line=BLUE_LIGHT, line_w=1, line_alpha=0.45,
         radius=6)
    linea1 = [("Philips — ", None), ("P21 / 5W", YELLOW), (" | GU 10;", None)]
    linea2 = [('12 V; 4000 K; 55"', None)]
    text(s, x + 48, by + 16, iw - 40, bh - 24,
         [[{"text": t, "color": c or PAPER} for t, c in linea1],
          [{"text": t, "color": c or PAPER} for t, c in linea2]],
         size=24, font=FONT_MONO, line_spacing=1.35)
    sy = top + 436
    _num(s, x + 28, sy, 170, "58,97%", size=36, color=YELLOW)
    _txt(s, x + 200, sy + 8, iw - 172, 30, "reproducen el id oficial", size=22)
    bar(s, x + 28, sy + 52, iw, 10, 0.5897, color=YELLOW)

    # --- 3. lo que parece ruido es sintaxis
    x = xs[2]
    simb = [("/", "65,70%", "separa variantes de código", 0.6570),
            ('"', "11,02%", "comillas que marcan pulgadas", 0.1102),
            ("Ж", "13,60%", "texto en alfabeto no latino", 0.1360)]
    for k, (sm, v, et, fr) in enumerate(simb):
        yy = top + 122 + k * 146
        ts = 84
        rect(s, x + 28, yy, ts, ts, fill=CHIP, line=YELLOW, line_w=1.5, line_alpha=0.7,
             radius=6)
        text(s, x + 28, yy, ts, ts, sm, size=46, bold=True, font=FONT_MONO, color=YELLOW,
             align="center", anchor="middle", wrap=False)
        _num(s, x + 136, yy - 4, 180, v, size=34, color=YELLOW)
        _txt(s, x + 136, yy + 42, iw - 108, 28, et, size=21)
        bar(s, x + 136, yy + 76, iw - 108, 8, fr, color=YELLOW)

    notes(s, notas[56])


# ======================================================================= P06
def p06(prs, notas):
    """Láminas 58 + 59: cinco preparadores, un pipeline; un título real lo atraviesa."""
    s = add_slide(prs, bg_image=FONDO)
    subencabezado(s, OE3 + " · Normalización del texto", "Cinco fuentes, un solo pipeline")
    cyc = 448  # eje vertical del esquema
    fh, fg = 44, 14
    stack_top = 310  # las dos pilas arrancan a la misma altura: rótulos alineados
    rot_y = stack_top - 38

    # fuentes
    fx, fw = 96, 286
    fuentes = ["prepare_match", "prepare_hidden", "prepare_nic", "prepare_catalog",
               "prepare_retailer_input"]
    ftot = len(fuentes) * fh + (len(fuentes) - 1) * fg
    fy0 = stack_top
    label(s, fx, rot_y, fw + 40, "Cinco preparadores", size=18, color=MUTED)
    busx = fx + fw + 28
    for k, nm in enumerate(fuentes):
        yy = fy0 + k * (fh + fg)
        _chip_fijo(s, fx, yy, fw, fh, nm, size=19, color=PAPER)
        line(s, fx + fw, yy + fh / 2, busx, yy + fh / 2, color=BLUE_LIGHT, width=2)
    line(s, busx, fy0 + fh / 2, busx, fy0 + ftot - fh / 2, color=BLUE_LIGHT, width=2)

    # bloque central
    px0, pw, ph = 476, 1012, 336
    py0 = cyc - ph / 2
    flecha(s, busx, cyc, px0 - 8, h=30)
    card(s, px0, py0, pw, ph, accent=YELLOW, fill=PANEL_2, brackets=True)
    _titulo(s, px0 + 32, py0 + 24, 600, 40, "El pipeline genérico único", size=28, color=YELLOW)
    vtxt = "19 pasos · v1.3.1"
    vw = text_width(vtxt, 20, FONT_MONO) + 28
    _chip_fijo(s, px0 + pw - 32 - vw, py0 + 25, vw, 38, vtxt, size=20, color=YELLOW)
    # la cadena muestra solo las funciones principales, no los 19 pasos
    label(s, px0 + 32, py0 + 78, 600, "Funciones principales", size=18, color=MUTED)
    filas = [["as_text", "decode_html", "normalize_unicode", "normalize_technical"],
             ["extract_codes", "canonicalize_code", "quality_flags"]]
    sh, sgap = 44, 44
    ry = [py0 + 112, py0 + 200]
    ends = []
    for r, pasos in enumerate(filas):
        xx = px0 + 32
        primeros = None
        for j, nm in enumerate(pasos):
            w = text_width(nm, 19, FONT_MONO) + 28
            _chip_fijo(s, xx, ry[r], w, sh, nm, size=19, color=YELLOW, fill=CHIP)
            if primeros is None:
                primeros = (xx, w)
            if j < len(pasos) - 1:
                triangle(s, xx + w + sgap / 2 - 7, ry[r] + sh / 2 - 8, 14, 16, color=MUTED,
                         rotation=90)
            last = (xx, w)
            xx += w + sgap
        ends.append((primeros, last))
    # conector en serpentina entre la fila 1 y la fila 2
    (f1, l1), (f2, _) = ends
    xr = l1[0] + l1[1] / 2
    xl = f2[0] + f2[1] / 2
    ym = (ry[0] + sh + ry[1]) / 2
    line(s, xr, ry[0] + sh, xr, ym, color=MUTED, width=2)
    line(s, xr, ym, xl, ym, color=MUTED, width=2)
    line(s, xl, ym, xl, ry[1] - 2, color=MUTED, width=2, arrow=True)
    _txt(s, px0 + 32, py0 + 264, pw - 64, 60,
         [["Lo único propio de cada fuente es qué columnas leer. De ahí en adelante, las "
           "mismas funciones — eso elimina el ",
           {"text": "training-serving skew", "color": YELLOW, "italic": True}, "."]],
         size=22, color=PAPER, ls=1.2)

    # salidas
    ox, ow = 1576, 248
    salidas = [("*_text", True), ("*_codes", True), ("*_token_count", True),
               ("banderas de calidad", False)]
    otot = len(salidas) * fh + (len(salidas) - 1) * fg
    oy0 = stack_top
    obus = ox - 26
    flecha(s, px0 + pw + 8, cyc, obus, h=30)
    label(s, ox, rot_y, ow, "Salidas", size=18, color=MUTED)
    for k, (nm, mono) in enumerate(salidas):
        yy = oy0 + k * (fh + fg)
        _chip_fijo(s, ox, yy, ow, fh, nm, size=19 if mono else 20, mono=mono, color=YELLOW)
        line(s, obus, yy + fh / 2, ox, yy + fh / 2, color=BLUE_LIGHT, width=2)
    line(s, obus, oy0 + fh / 2, obus, oy0 + otot - fh / 2, color=BLUE_LIGHT, width=2)
    _txt(s, ox - 8, oy0 + otot + 12, ow + 16, 54,
         ["127.093 filas × 53 columnas", "33,14 MiB"], size=20, color=MUTED, align="center")

    # ---------------- un título real atravesando el pipeline
    ty = 646
    label(s, 96, ty, 1000, "Un título real atravesando el pipeline", size=18, color=YELLOW)
    etapas = [("Crudo", "como llega del portal",
               _resalta('Philips — P21 / 5W | GU 10; 12 V; 4000 K; 55"'), BLUE_LIGHT),
              ("Unicode NFKC", "+ casefold",
               _resalta('philips — p21 / 5w | gu 10; 12 v; 4000 k; 55"'), BLUE_LIGHT),
              ("Normalización técnica", "10 reglas de dominio",
               _resalta('philips p21/5w gu10 12v 4000k 55"'), BLUE_LIGHT),
              ("Códigos aparte", "nunca dentro del texto", None, YELLOW)]
    rh, rg = 64, 10
    for k, (et, sub, partes, acc) in enumerate(etapas):
        yy = ty + 36 + k * (rh + rg)
        rect(s, 96, yy, 1728, rh, fill=PANEL_2, line=BLUE_LIGHT, line_w=1, line_alpha=0.3)
        rect(s, 96, yy, 6, rh, fill=acc)
        text(s, 124, yy + 9, 330, 26, et.upper(), size=19, bold=True, font=FONT_HEAD,
             color=YELLOW if k == 3 else PAPER, spacing=1)
        _txt(s, 124, yy + 35, 330, 24, sub, size=18, color=MUTED)
        if partes is not None:
            text(s, px0 + 4, yy, 1824 - px0 - 32, rh, _mono_runs(partes, 26), size=26,
                 font=FONT_MONO, color=PAPER, anchor="middle")
            continue
        # text → … · codes → […]: las flechas se dibujan (Roboto Mono no tiene «→»)
        xx = px0 + 4
        xx += _segmentos_flecha(s, xx, yy, rh,
                                [[("text", MUTED)], _resalta('philips gu10 12v 4000k 55"')],
                                26, font=FONT_MONO, gap=12, largo=28, alto=18)
        sep = text_width("   ·   ", 26, FONT_MONO)
        text(s, xx, yy, sep + 8, rh, "   ·   ", size=26, font=FONT_MONO, color=MUTED,
             anchor="middle", wrap=False)
        xx += sep
        _segmentos_flecha(s, xx, yy, rh, [[("codes", MUTED)], [("[p21/5w]", YELLOW)]],
                          26, font=FONT_MONO, gap=12, largo=28, alto=18)
    _txt(s, 96, ty + 36 + 4 * (rh + rg) + 4, 1728, 30,
         "La barra, las comillas y el alfabeto se conservan: son sintaxis del dominio. "
         "La normalización es idempotente, verificada sobre 254.186 textos.",
         size=21, color=MUTED)

    notes(s, " ".join(notas[i] for i in (58, 59)))


# ======================================================================= P07
def p07(prs, notas):
    """Lámina 60: qué se destruye, qué se conserva y qué se gana con el pipeline."""
    s = add_slide(prs, bg_image=FONDO)
    subencabezado(s, OE3 + " · Efecto de la limpieza",
                  "Qué se destruye, qué se conserva, qué se gana")
    cw, gap = 557, 28
    top, ch = 276, 440
    cols = [
        dict(tag="Eliminado", tfill=RED, tcol=DARK, titulo="Se destruye lo que sí es ruido",
             sub="marcado heredado del portal", unidad="Entidades HTML",
             vals=[("575", 1.0, RED), ("0", 0.0, RED)]),
        dict(tag="Intacto", tfill=BLUE_LIGHT, tcol=DARK, titulo="Se conserva lo que es señal",
             sub="0 filas perdidas · 0 excluidos", unidad="Filas no latinas",
             vals=[("30.919", 1.0, BLUE_LIGHT), ("30.919", 1.0, BLUE_LIGHT)]),
        dict(tag="+32 puntos", tfill=YELLOW, tcol=DARK, titulo="Se gana con los códigos aparte",
             sub="la vista enriched", unidad="Recall@1 en validación · %",
             vals=[("51,17", 0.5117, BLUE_LIGHT), ("83,18", 0.8318, YELLOW)]),
    ]
    for k, c in enumerate(cols):
        x = 96 + k * (cw + gap)
        foco = k == 2
        card(s, x, top, cw, ch, accent=YELLOW if foco else c["tfill"], brackets=foco)
        tag(s, x + 28, top + 30, c["tag"], fill=c["tfill"], color=c["tcol"], size=18, h=38)
        _titulo(s, x + 28, top + 84, cw - 56, 38, c["titulo"], size=26)
        _txt(s, x + 28, top + 122, cw - 56, 30, c["sub"], size=21, color=MUTED)
        rect(s, x + 28, top + 166, cw - 56, 1.5, fill=BLUE_LIGHT, fill_alpha=0.3)
        label(s, x + 28, top + 180, cw - 56, c["unidad"], size=18, color=MUTED,
              align="center")
        # mini gráfico antes / después (escala: valor inicial o 100%)
        hmax, bw = 112, 120
        yb = top + 274 + hmax
        bxs = [x + cw / 2 - bw - 52, x + cw / 2 + 52]
        for j, (v, fr, col) in enumerate(c["vals"]):
            bx = bxs[j]
            _num(s, bx - 50, top + 220, bw + 100, v, size=34,
                 color=YELLOW if (foco and j == 1) else PAPER, align="center")
            rect(s, bx, yb - hmax, bw, hmax, fill=CHIP)
            hh = max(3, hmax * fr)
            rect(s, bx, yb - hh, bw, hh, fill=col)
            _txt(s, bx - 20, yb + 8, bw + 40, 26, "antes" if j == 0 else "después", size=18,
                 color=MUTED, align="center")
        flecha(s, bxs[0] + bw + 18, yb - hmax / 2, bxs[1] - 18, h=26,
               color=YELLOW if foco else MUTED)

    # cobertura de códigos extraídos
    py = top + ch + 28
    ph = 1004 - py
    card(s, 96, py, 1728, ph, accent=None)
    label(s, 128, py + 20, 1000, "Cobertura de códigos extraídos · % de filas", size=18,
          color=YELLOW)
    cob = [("manufacturer_codes", "100%", 1.0), ("retailer_codes", "99,98%", 0.9998),
           ("manufacturer_eans", "97,17%", 0.9717), ("retailer_title_codes", "90,53%", 0.9053)]
    paso = (ph - 70) / len(cob)
    for k, (nm, v, fr) in enumerate(cob):
        yy = py + 60 + k * paso
        text(s, 128, yy, 360, 30, nm, size=21, font=FONT_MONO, color=YELLOW)
        bar(s, 500, yy + 8, 1100, 14, fr, color=BLUE_LIGHT)
        _num(s, 1640, yy - 2, 152, v, size=28, color=PAPER, align="right")

    notes(s, notas[60])


def construir(prs, notas):
    p04(prs, notas)
    p05(prs, notas)
    p06(prs, notas)
    p07(prs, notas)
