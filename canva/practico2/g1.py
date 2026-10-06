"""Grupo g1: OE2 · atributos, fuentes del corpus y selección de campos (P01-P03)."""

from pptx_kit import add_slide, notes, rect, text
from theme import BLUE_TEXT, FONDO, LINE, MUTED, PAPER, YELLOW
from componentes import (BLUE_LIGHT, CHIP, CONTENT_TOP, FONT_HEAD, FONT_MONO, FONT_TXT,
                         PANEL_2, RED, bar, card, chip, flecha, flecha_abajo, label,
                         subencabezado, tag, text_width)

OE2 = "OE2 · Organizar el conjunto de datos"


def p01(prs, notas):
    """Láminas 44 + 45: señales que deciden la correspondencia y filtros de calidad."""
    s = add_slide(prs, bg_image=FONDO)
    subencabezado(s, OE2 + " · Identificar atributos",
                  "Las señales que deciden y los filtros de calidad")
    # --- izquierda: cuatro tarjetas de señales -------------------------------
    senales = [
        ("Identificadores", [("ManufacturerProductId", "17.416 oficiales", YELLOW),
                             ("RetailerProductId", "8.528 reutilizados", RED)]),
        ("Nombres", [("ManufacturerProductName", "42 caracteres de media", YELLOW),
                     ("RetailerProductName", ["61 caracteres de media", "90,19% con código"],
                      YELLOW)]),
        ("Descripción y códigos", [("ManufacturerProductDescription", "5,35% nulos", YELLOW),
                                   ("ExtraInfo", "67,20% EAN", YELLOW)]),
        ("Contexto", [("Brand", "82,80% presente", YELLOW),
                      ("ManufacturerProductMappingCountry", "65 países", YELLOW)]),
    ]
    x0, y0 = 96, CONTENT_TOP + 8
    cw, ch, gap = 492, 355, 24          # 276 + 2·355 + 24 = 1010: borde común con LinkIsValid
    for k, (titulo, filas) in enumerate(senales):
        x = x0 + (k % 2) * (cw + gap)
        y = y0 + (k // 2) * (ch + gap)
        card(s, x, y, cw, ch, accent=YELLOW if k == 0 else BLUE_LIGHT)
        text(s, x + 28, y + 24, cw - 56, 40, titulo, size=28, bold=True, font=FONT_HEAD)
        for j, (campo, valor, col) in enumerate(filas):
            yy = y + 88 + j * 116
            chip(s, x + 28, yy, campo, size=18 if len(campo) > 26 else 19)
            lineas = valor if isinstance(valor, list) else [valor]
            text(s, x + 28, yy + 44, cw - 56, 42 * len(lineas) + 8, lineas, size=32,
                 bold=True, font=FONT_HEAD, color=col, line_spacing=1.1)
    # --- derecha: embudo de filtros de calidad -------------------------------
    rx, rw = 96 + 2 * cw + gap + 40, 1824 - (96 + 2 * cw + gap + 40)
    label(s, rx, y0, rw, "Filtro base de calidad", size=18, color=YELLOW)
    filtros = [("Invalid", '"false"', "2.136 registros inválidos"),
               ("IsDeleted", '"false"', "2.355 registros eliminados"),
               ("MatchConfidence", "100", "129.473 con 100 · 34 con −100")]
    fy, fh, fgap = y0 + 44, 138, 34
    for k, (campo, valor, efecto) in enumerate(filtros):
        y = fy + k * (fh + fgap)
        rect(s, rx, y, rw, fh, fill=PANEL_2, line=BLUE_LIGHT, line_w=1.5, line_alpha=0.45)
        rect(s, rx, y, 6, fh, fill=YELLOW)
        text(s, rx + 28, y + 20, rw - 56, 40, campo, size=28, bold=True, font="Roboto Mono",
             color=YELLOW)
        w = text_width(campo, 28, "Roboto Mono", True)
        text(s, rx + 28 + w + 14, y + 22, 200, 40, "= " + valor, size=26, font="Roboto Mono",
             color=PAPER)
        text(s, rx + 28, y + 76, rw - 56, 40, efecto, size=24, font=FONT_TXT, color=MUTED)
        if k < len(filtros) - 1:
            flecha_abajo(s, rx + rw / 2, y + fh + 2, y + fh + fgap - 2, w=24)
    # trampa: LinkIsValid
    ty = fy + 3 * (fh + fgap) - 4
    th = 1010 - ty
    rect(s, rx, ty, rw, th, fill=CHIP, line=RED, line_w=2, line_alpha=0.9)
    ly = ty + 38
    text(s, rx + 28, ly, 200, 40, "LinkIsValid", size=28, bold=True, font="Roboto Mono",
         color=PAPER)
    lw = text_width("LinkIsValid", 28, "Roboto Mono", True)
    chip(s, rx + 28 + lw + 16, ly + 2, '"true" / "false"', size=20, h=36)
    tag(s, rx + rw - 28 - text_width("NO ES FILTRO", 18, FONT_HEAD, True, 1.2) - 34,
        ly + 2, "No es filtro", fill=RED, color=PAPER, size=18, h=36)
    text(s, rx + 28, ty + 104, rw - 56, 40,
         "Solo indica el estado del enlace, no la validez del match",
         size=24, font=FONT_TXT, color=PAPER)
    notes(s, " ".join(notas[i] for i in (44, 45)))


# ---------------------------------------------------------------- utilidades
def _linea(s, x, y, partes, h=32, gap=10):
    """Línea mixta medida: texto Barlow y chips de código en cuadros separados.

    `partes`: lista de str (texto Barlow 21 px), ("b", str, color) texto en
    negrita, ("h", str) rótulo Montserrat del contrato, ("chip", str) o
    ("flecha",) flecha de bloque pequeña. Devuelve la x final.
    """
    cx = x
    for p in partes:
        if isinstance(p, str) or p[0] in ("b", "h"):
            if isinstance(p, str):
                s_, font, size, bold, col = p, FONT_TXT, 21, False, PAPER
            elif p[0] == "b":
                s_, font, size, bold, col = p[1], FONT_TXT, 21, True, p[2]
            else:
                s_, font, size, bold, col = p[1], FONT_HEAD, 20, True, BLUE_TEXT
            w = text_width(s_, size, font, bold)
            text(s, cx, y, w + 40, h, s_, size=size, font=font, bold=bold, color=col,
                 anchor="middle")
            cx += w + gap
        elif p[0] == "flecha":
            flecha(s, cx, y + h / 2, cx + 24, h=16)
            cx += 24 + gap
        else:
            chh = min(30, h - 2)
            cw = chip(s, cx, y + (h - chh) / 2, p[1], size=18, h=chh, pad=10)
            cx += cw + gap
    return cx


# ------------------------------------------------------------------- P02
# nombre, subtítulo (lámina 57), cifra, valor, destacado, contrato, rasgo del contrato
FUENTES = [
    ("Match", "pares históricos validados", "127.093", 127093, True,
     "36 columnas · 12 snapshots de 2025", None),
    ("NIC", "no está en catálogo", "28.712", 28712, False,
     "47.333 filas del archivo · 5 + 8 columnas",
     [("b", "83%", YELLOW), ("chip", "unknown_review"), ("flecha",),
      "entra con peso reducido"]),
    ("Hidden", "publicación ocultada", "11.077", 11077, False,
     "15.355 filas del archivo · 4 columnas",
     [("chip", "final_status"), "siempre Hidden: una sola clase"]),
    ("Catálogo oficial", "productos UA", "4.316", 4316, True,
     "11 columnas · Ucrania y Bélgica",
     ["Llave real:", ("chip", "ProductId"), ("chip", "BAR700/00")]),
    ("Retailer de prueba", "gold externo · 14 países", "1.856", 1856, False,
     [("h", "Sin archivo físico en"), ("chip", "data/raw/retailer_test/")],
     [("chip", "validate_columns()"), "valida el contrato antes de leer"]),
    ("Pares negativos", "800 elegibles", "896", 896, False,
     "7 columnas · única fuente con pares ya etiquetados",
     [("chip", "sufijo_distinto"), ("chip", "reacondicionado_r1")]),
    ("Acciones de validación", "decisión humana registrada", "180", 180, False,
     "Sin campos de texto", ["Etiquetas sobre publicaciones"]),
]


def p02(prs, notas):
    """Láminas 46-50 + 57: las siete fuentes, su contrato y su escala."""
    s = add_slide(prs, bg_image=FONDO)
    subencabezado(s, OE2 + " · Extraer productos",
                  "Siete fuentes del corpus: contrato y escala")
    px_, py, pw, ph = 96, 276, 1728, 626
    card(s, px_, py, pw, ph, accent=None, brackets=True)
    xn, wn = 128, 300            # fuente
    xb, wb = 448, 540            # barra
    xv, wv = 996, 170            # cifra
    xd = 1196                    # divisor
    xc, wc = 1226, 1792 - 1226   # contrato
    label(s, xn, py + 20, wn, "Fuente", color=MUTED)
    label(s, xb, py + 20, wb + wv + 10, "Volumen en el corpus · a escala", color=MUTED)
    label(s, xc, py + 20, wc, "Contrato del archivo", color=MUTED)
    rect(s, xd, py + 22, 1.5, ph - 44, fill=BLUE_LIGHT, fill_alpha=0.35)
    top, rh = py + 58, 80
    vmax = FUENTES[0][3]
    for k, (nombre, sub, cifra, valor, dest, contrato, rasgo) in enumerate(FUENTES):
        y = top + k * rh
        if k:
            rect(s, xn, y - 1, xd - xn - 24, 1, fill=BLUE_LIGHT, fill_alpha=0.18)
            rect(s, xc, y - 1, wc, 1, fill=BLUE_LIGHT, fill_alpha=0.18)
        col = YELLOW if dest else BLUE_LIGHT
        text(s, xn, y + 9, wn, 32, nombre, size=24, bold=True, font=FONT_HEAD)
        text(s, xn, y + 42, wn, 28, sub, size=20, font=FONT_TXT, color=MUTED)
        bar(s, xb, y + 28, wb, 24, valor / vmax, color=col)
        text(s, xv, y + 15, wv, 50, cifra, size=34, bold=True, font=FONT_HEAD,
             color=YELLOW if dest else PAPER, align="right", anchor="middle")
        cab = [("h", contrato)] if isinstance(contrato, str) else contrato
        if rasgo is None:
            _linea(s, xc, y + 25, cab, h=30)
        else:
            _linea(s, xc, y + 6, cab, h=30)
            _linea(s, xc, y + 43, rasgo, h=30)
    # consecuencia
    cy, ch = py + ph + 26, 1010 - (py + ph + 26)
    rect(s, px_, cy, pw, ch, fill=PANEL_2, line=BLUE_LIGHT, line_w=1.5, line_alpha=0.4)
    rect(s, px_, cy, 6, ch, fill=YELLOW)
    tw_ = tag(s, px_ + 32, cy + (ch - 36) / 2, "Consecuencia", size=18, h=36)
    msg = "La desproporción obliga a recuperar candidatos, no a comparar todo contra todo"
    text(s, px_ + 32 + tw_ + 24, cy, pw - tw_ - 88, ch, msg, size=26, bold=True,
         font=FONT_HEAD, anchor="middle")
    notes(s, " ".join(notas[i] for i in (46, 47, 48, 49, 50, 57)))


# ------------------------------------------------------------------- P03
def _grupo(s, x, y, w, h, titulo, campos, filas, accent=YELLOW):
    """Caja de un lado (fabricante o retailer) con sus campos como chips."""
    rect(s, x, y, w, h, fill=PANEL_2, line=BLUE_LIGHT, line_w=1.5, line_alpha=0.4)
    rect(s, x, y, 6, h, fill=accent)
    label(s, x + 26, y + 14, w - 52, titulo, size=18, color=accent)
    for j, fila in enumerate(filas):
        cx = x + 26
        for i in fila:
            cx += chip(s, cx, y + 50 + j * 44, campos[i], size=20, h=36, pad=12) + 10


def _vista(s, x, cy, nombre, size=26, borde=YELLOW):
    w = text_width(nombre, size, FONT_MONO) + 48
    rect(s, x, cy - 34, w, 68, fill=CHIP, line=borde, line_w=2.5, radius=6)
    text(s, x, cy - 34, w, 68, nombre, size=size, font=FONT_MONO, color=YELLOW,
         align="center", anchor="middle", wrap=False)
    return w


def _kpi_inline(s, x, y, valor, l1, l2):
    """Cifra grande con rótulo de dos líneas a su derecha."""
    vw = text_width(valor, 72, FONT_HEAD, True) + 8
    text(s, x, y, vw, 88, valor, size=72, bold=True, font=FONT_HEAD, color=YELLOW,
         anchor="middle", wrap=False)
    text(s, x + vw + 14, y + 16, 260, 60, [l1.upper(), l2.upper()], size=18, bold=True,
         font=FONT_HEAD, color=PAPER, spacing=1.5, line_spacing=1.25)


def p03(prs, notas):
    """Láminas 51 + 52 + 53: selección de campos textuales y vistas comparables."""
    s = add_slide(prs, bg_image=FONDO)
    subencabezado(s, OE2 + " · Seleccionar campos", "De 36 columnas a dos vistas comparables")
    px_, py, pw, ph = 96, 276, 1728, 438
    card(s, px_, py, pw, ph, accent=None, brackets=True)
    xa, xb, xc = 136, 528, 1346
    ky = py + 14
    _kpi_inline(s, xa, ky, "36", "columnas", "originales")
    _kpi_inline(s, xb, ky, "7", "campos", "textuales")
    _kpi_inline(s, xc, ky, "2", "vistas", "comparables")
    rect(s, px_ + 32, py + 112, pw - 64, 1, fill=BLUE_LIGHT, fill_alpha=0.3)
    # 36 columnas: retícula 6x6 con las 7 seleccionadas
    sq, g = 34, 9
    fy, fh = py + 138, 142
    ry, rh = fy + fh + 26, 98
    gy = fy + (fh + 26 + rh - (6 * sq + 5 * g)) / 2
    elegidas = {1: YELLOW, 8: YELLOW, 10: YELLOW, 15: YELLOW, 22: YELLOW,  # fabricante
                27: BLUE_LIGHT, 32: BLUE_LIGHT}                               # retailer
    for i in range(36):
        x = xa + (i % 6) * (sq + g)
        y = gy + (i // 6) * (sq + g)
        if i in elegidas:
            rect(s, x, y, sq, sq, fill=elegidas[i], radius=4)
        else:
            rect(s, x, y, sq, sq, fill=CHIP, line=BLUE_LIGHT, line_w=1, line_alpha=0.35,
                 radius=4)
    gw = 6 * sq + 5 * g
    # 7 campos en dos lados
    bw = 1236 - xb
    fab = ["Brand", "ManufacturerProductName", "ExtraInfo", "ManufacturerProductDescription",
           "ManufacturerProductId"]
    _grupo(s, xb, fy, bw, fh, "Fabricante · 5 campos", fab, [(0, 1, 2), (3, 4)])
    _grupo(s, xb, ry, bw, rh, "Retailer · 2 campos", ["RetailerProductName",
                                                       "RetailerProductId"], [(0, 1)],
           accent=BLUE_LIGHT)
    # reparto: retícula → dos lados
    mid = gy + (6 * sq + 5 * g) / 2
    c1, c2 = fy + fh / 2, ry + rh / 2
    flecha(s, xa + gw + 22, mid, xb - 40, h=26)
    rect(s, xb - 40, c1, 4, c2 - c1, fill=YELLOW)
    rect(s, xb - 40, c1 - 2, 40, 4, fill=YELLOW)
    rect(s, xb - 40, c2 - 2, 40, 4, fill=YELLOW)
    # dos vistas
    flecha(s, xb + bw + 14, c1, xc - 14, h=26)
    flecha(s, xb + bw + 14, c2, xc - 14, h=26, color=BLUE_LIGHT)
    _vista(s, xc, c1, "manufacturer_text")
    _vista(s, xc, c2, "retailer_text", borde=BLUE_LIGHT)
    # otras seis fuentes
    label(s, 96, py + ph + 20, 800, "Selección textual en las otras seis fuentes",
          color=YELLOW)
    verif = "Cada regla está verificada en su módulo de preparación"
    vw = text_width(verif, 20, FONT_TXT) + 12
    text(s, 1824 - vw, py + ph + 17, vw, 30, verif, size=20, font=FONT_TXT, color=MUTED,
         align="right", anchor="middle")
    cy0 = py + ph + 56
    chh = 1010 - cy0
    n, gap = 5, 20
    cw = (1728 - (n - 1) * gap) / n
    tarjetas = [
        ("Hidden · NIC", BLUE_LIGHT, ("chip", "product_name", "· único"),
         ("chip", "retailer_text_raw"),
         [("t", "NIC: 8 etiquetas", PAPER), ("flecha",), ("t", "metadata", PAPER)]),
        ("Catálogo oficial", BLUE_LIGHT, ("t", "Marca + nombres + descripción"),
         ("chip", "catalog_text_raw"),
         [("chip", "ExtraInfo"), ("flecha",), ("t", "códigos", PAPER)]),
        ("Retailer de prueba", YELLOW, ("chip", "ProductName"),
         ("chip", "build_retailer_text"), [("tb", "Mismo compositor de Match", YELLOW)]),
        ("Pares negativos", LINE, ("chip", "retailer_text"), ("chip", "manufacturer_text"),
         [("t", "Ya compuestos: sin selección", MUTED)]),
        ("Acciones de validación", LINE, ("t", "Sin campos de texto"),
         ("m", "Etiquetas sobre publicaciones"),
         [("tb", "No alimenta el modelo textual", MUTED)]),
    ]
    for k, (nombre, acc, a, b, pie) in enumerate(tarjetas):
        x = 96 + k * (cw + gap)
        card(s, x, cy0, cw, chh, accent=acc)
        text(s, x + 22, cy0 + 20, cw - 44, 32, nombre, size=22, bold=True, font=FONT_HEAD)
        yy, paso = cy0 + 64, 66
        for j, it in enumerate((a, b)):
            y = yy + j * paso
            if it[0] == "chip":
                w_ = chip(s, x + 22, y, it[1], size=18, h=32, pad=10)
                if len(it) > 2:
                    text(s, x + 22 + w_ + 10, y, cw - 54 - w_, 32, it[2], size=20,
                         font=FONT_TXT, color=MUTED, anchor="middle")
            else:
                text(s, x + 22, y, cw - 44, 32, it[1], size=21, font=FONT_TXT,
                     color=MUTED if it[0] == "m" else PAPER, anchor="middle")
        if nombre == "Pares negativos":       # signo «+» dibujado, en el eje de las flechas
            cyp = yy + 32 + (paso - 32) / 2
            rect(s, x + 40 - 9, cyp - 2, 18, 4, fill=YELLOW)
            rect(s, x + 40 - 2, cyp - 9, 4, 18, fill=YELLOW)
        elif a[0] != "t" or b[0] == "chip":
            flecha_abajo(s, x + 40, yy + 36, yy + paso - 3, w=18)
        rect(s, x + 22, cy0 + chh - 62, cw - 44, 1, fill=BLUE_LIGHT, fill_alpha=0.25)
        py2 = cy0 + chh - 48
        cx = x + 22
        for it in pie:
            if it[0] == "chip":
                cx += chip(s, cx, py2, it[1], size=18, h=32, pad=10) + 10
            elif it[0] == "flecha":
                flecha(s, cx, py2 + 16, cx + 24, h=16)
                cx += 24 + 10
            else:
                tw_ = text_width(it[1], 20, FONT_TXT, it[0] == "tb")
                text(s, cx, py2, cw - 44 - (cx - x - 22), 32, it[1], size=20, font=FONT_TXT,
                     bold=it[0] == "tb", color=it[2], anchor="middle")
                cx += tw_ + 10
    notes(s, " ".join(notas[i] for i in (51, 52, 53)))


def construir(prs, notas):
    p01(prs, notas)
    p02(prs, notas)
    p03(prs, notas)
