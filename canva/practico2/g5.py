"""Grupo g5: OE5 · clasificación de pares, matriz y techo, evidencia externa (P15-P18)."""

from pptx_kit import add_slide, line, notes, rect, text
from theme import FONDO, LINE, MUTED, PAPER, YELLOW
from componentes import (BLUE_LIGHT, CHIP, DARK, FONT_HEAD, FONT_MONO, FONT_TXT, RED,
                         bar, card, chip, ecuacion, flecha, label, medida_ecuacion, numbadge,
                         subencabezado, tag, text_width, wrap_lines)

OE5 = "OE5 · Evaluar el desempeño"
TOP, BOTTOM = 282, 1010


# ----------------------------------------------------------------- utilidades
def _tag_w(s, size=16, pad=14):
    """Ancho que ocupará `tag(...)` con el mismo texto y tamaño."""
    return text_width(s.upper(), size, FONT_HEAD, True, spacing=1.2) + 2 * pad + 6


def _seg(s, x, y, partes, h=30, gap=8):
    """Línea mixta medida: cada tramo en su propio cuadro (una familia por cuadro).

    `partes`: lista de (texto, fuente, tamaño, color, negrita). Devuelve la x final.
    """
    cx = x
    for txt, font, size, color, bold in partes:
        w = text_width(txt, size, font, bold)
        text(s, cx, y, w + 30, h, txt, size=size, font=font, color=color, bold=bold,
             anchor="middle", line_spacing=1.0)
        cx += w + gap
    return cx


def _runs(s, x, y, w, h, tramos, size, font, anchor="top", align="left", bold=False,
          line_spacing=1.25):
    """Cuadro de una sola familia con tramos de colores: [(texto, color), ...]."""
    text(s, x, y, w, h, [[{"text": t, "color": c} for t, c in tramos]], size=size, font=font,
         bold=bold, anchor=anchor, align=align, line_spacing=line_spacing)


def _valor(s, x, y, w, valor, size=32, color=PAPER, align="left", h=None):
    text(s, x, y, w, h or size * 1.3, valor, size=size, bold=True, font=FONT_HEAD, color=color,
         align=align, anchor="middle", line_spacing=1.0)


def _divisor(s, x, y, w, alpha=0.35):
    rect(s, x, y, w, 1.5, fill=BLUE_LIGHT, fill_alpha=alpha)


# ------------------------------------------------------------------- P15
MODELOS = [
    # n, nombre, umbral, F1, F1 txt, FP, FP txt, precisión·recall, color, nota
    ("1", "TF-IDF", "0,5238", 72.04, "72,04%", 35.38, "35,38%",
     "Precisión 74,44% · Recall 69,79%", BLUE_LIGHT, "rechaza de más"),
    ("2", "Embeddings", "0,378", 73.42, "73,42%", 83.08, "83,08%",
     "Precisión 61,70% · Recall 90,63%", RED, "acepta casi todo"),
    ("3", "Cross-encoder", "0,998844", 97.41, "97,41%", 4.62, "4,62%",
     "Precisión 96,91% · Recall 97,92%", YELLOW, None),
]

NEGATIVOS = [
    ("Sufijo distinto", "41 pares", [("NPX150/INT", True), ("frente a", False),
                                     ("NPX150/90", True)],
     [("Embeddings", 90.24, "90,24%"), ("TF-IDF", 36.59, "36,59%"),
      ("Cross-encoder", 4.88, "4,88%")]),
    ("Reacondicionado", "24 pares", [("sufijo", False), ("R1", True)],
     [("Embeddings", 70.83, "70,83%"), ("TF-IDF", 33.33, "33,33%"),
      ("Cross-encoder", 4.17, "4,17%")]),
]


def _panel_f1(s, x, y, w, h):
    card(s, x, y, w, h, accent=YELLOW, brackets=True)
    pad = 32
    iw = w - 2 * pad
    xm, wm = x + pad, 330
    xf, wf = xm + wm + 24, 250
    xp = xf + wf + 56
    wp = x + w - pad - xp
    label(s, xm, y + 26, wm, "Modelo · umbral", color=MUTED)
    label(s, xf, y + 26, wf, "F1 de pares", color=PAPER)
    label(s, xp, y + 26, wp, "Falsos positivos", color=PAPER)
    r0, rh = y + 70, 142
    for k, (n, nom, umb, f1, f1s, fp, fps, pr, col, nota_) in enumerate(MODELOS):
        ry = r0 + k * rh
        if k:
            _divisor(s, xm, ry - 1, iw, alpha=0.2)
        cbad = PAPER if col != YELLOW else DARK
        numbadge(s, xm, ry + 18, n, size=40, fill=col, color=cbad)
        text(s, xm + 56, ry + 16, wm - 56, 44, nom, size=28, bold=True, font=FONT_HEAD,
             anchor="middle")
        ex = _seg(s, xm, ry + 68, [("umbral", FONT_TXT, 20, MUTED, False)], h=32)
        chip(s, ex, ry + 69, umb, size=19, h=30, pad=10)
        text(s, xm, ry + 104, wm + 10, 28, pr, size=19, font=FONT_TXT, color=MUTED,
             anchor="middle")
        # F1
        fcol = YELLOW if col == YELLOW else PAPER
        _valor(s, xf, ry + 14, wf, f1s, size=40, color=fcol)
        bar(s, xf, ry + 76, wf, 20, f1 / 100, color=YELLOW if col == YELLOW else BLUE_LIGHT)
        # mismo F1, comportamiento opuesto: la etiqueta va bajo el F1 que «engaña»
        if nota_:
            tag(s, xf, ry + 103, nota_, fill=RED, color=PAPER, size=20, h=34, pad=10)
        # falsos positivos
        pcol = YELLOW if col == YELLOW else RED
        _valor(s, xp, ry + 14, wp, fps, size=40, color=pcol)
        bar(s, xp, ry + 76, wp, 20, fp / 100, color=pcol)
    # corchete: F1 casi igual en los modelos 1 y 2
    bx = xf + wf + 14
    c1, c2 = r0 + 14 + 26, r0 + rh + 14 + 26
    rect(s, bx, c1, 3, c2 - c1, fill=YELLOW)
    rect(s, bx - 10, c1 - 1.5, 13, 3, fill=YELLOW)
    rect(s, bx - 10, c2 - 1.5, 13, 3, fill=YELLOW)
    text(s, bx + 6, (c1 + c2) / 2 - 22, 36, 44, "≈", size=34, bold=True, font=FONT_TXT,
         color=YELLOW, anchor="middle")
    # ecuación y lectura
    ey = r0 + 3 * rh + 4
    _divisor(s, x + pad, ey, iw, alpha=0.45)
    eq = [("var", "F1"), "=", ("frac", ["2", "·", ("var", "P"), "·", ("var", "R")],
                               [("var", "P"), "+", ("var", "R")])]
    ew, up, dn = medida_ecuacion(eq, size=34)
    zona = y + h - ey
    ax = ey + (zona - (up + dn)) / 2 + up
    ecuacion(s, x + pad + 8, ax, eq, size=34)
    tx = x + pad + ew + 56
    rect(s, tx - 28, ey + 24, 1.5, zona - 48, fill=BLUE_LIGHT, fill_alpha=0.35)
    text(s, tx, ey + 18, x + w - pad - tx, zona - 36,
         [[{"text": "Un solo número promedia precisión y recall. ", "color": PAPER},
           {"text": "Los modelos 1 y 2 parecen equivalentes y sus matrices son opuestas.",
            "color": PAPER, "bold": True}],
          [{"text": "Aquí la superioridad del cross-encoder sí es contundente.",
            "color": YELLOW, "bold": True}]],
         size=23, font=FONT_TXT, anchor="middle", line_spacing=1.3)


def _panel_negativos(s, x, y, w, h):
    card(s, x, y, w, h, accent=RED)
    pad = 30
    iw = w - 2 * pad
    label(s, x + pad, y + 26, iw, "Negativos difíciles", color=YELLOW)
    text(s, x + pad, y + 54, iw, 30, "Tasa de falsos positivos en variantes casi idénticas",
         size=21, font=FONT_TXT, color=MUTED, anchor="middle")
    nw, vw = 160, 104
    bw = iw - nw - vw - 16
    gy = y + 100
    for titulo, pares, chips_, filas in NEGATIVOS:
        text(s, x + pad, gy, iw, 38, titulo, size=26, bold=True, font=FONT_HEAD,
             anchor="middle")
        text(s, x + pad, gy, iw, 38, pares, size=22, bold=True, font=FONT_HEAD, color=MUTED,
             align="right", anchor="middle")
        cx = x + pad
        for t, es_chip in chips_:
            if es_chip:
                cx += chip(s, cx, gy + 46, t, size=20, h=34, pad=10) + 10
            else:
                cx = _seg(s, cx, gy + 48, [(t, FONT_TXT, 21, MUTED, False)], h=30) + 2
        for j, (nom, v, vs) in enumerate(filas):
            ry = gy + 94 + j * 50
            mejor = nom == "Cross-encoder"
            col = YELLOW if mejor else RED
            text(s, x + pad, ry, nw, 34, nom, size=21, font=FONT_TXT,
                 bold=mejor, color=PAPER, anchor="middle")
            bar(s, x + pad + nw, ry + 7, bw, 20, v / 100, color=col)
            _valor(s, x + w - pad - vw, ry, vw, vs, size=26, color=col, align="right", h=34)
        gy += 94 + 3 * 50 + 20
    _divisor(s, x + pad, y + h - 100, iw, alpha=0.3)
    text(s, x + pad, y + h - 86, iw, 58,
         "Es la variabilidad de criterio que el planteamiento del problema identifica: "
         "confundir variantes casi idénticas.",
         size=21, font=FONT_TXT, color=PAPER, anchor="middle", line_spacing=1.25)


def p15(prs, notas):
    """Láminas 74 + 75: clasificación de pares y negativos difíciles."""
    s = add_slide(prs, bg_image=FONDO)
    subencabezado(s, OE5 + " · Clasificación de pares",
                  "Clasificación de pares: el F1 sin la matriz engaña")
    lw, g = 1060, 28
    _panel_f1(s, 96, TOP, lw, BOTTOM - TOP)
    _panel_negativos(s, 96 + lw + g, TOP, 1728 - lw - g, BOTTOM - TOP)
    notes(s, " ".join(notas[i] for i in (74, 75)))


# ------------------------------------------------------------------- P16
def _celda(s, x, y, w, h, valor, rotulo, col, abrev, fill_alpha=0.12, extra=None):
    rect(s, x, y, w, h, fill=col, fill_alpha=fill_alpha, line=col, line_w=2, line_alpha=0.85)
    text(s, x + 14, y + 10, 60, 26, abrev, size=18, bold=True, font=FONT_HEAD, color=col,
         anchor="middle")
    text(s, x, y + 18, w, 80, valor, size=64, bold=True, font=FONT_HEAD,
         color=YELLOW if col == YELLOW else (RED if col == RED else PAPER), align="center",
         anchor="middle", line_spacing=1.0)
    text(s, x, y + 96, w, 28, rotulo.upper(), size=18, bold=True, font=FONT_HEAD,
         color=PAPER, align="center", anchor="middle", spacing=1.5)
    if extra:
        text(s, x, y + 124, w, 28, extra, size=20, font=FONT_TXT, color=MUTED, align="center",
             anchor="middle", line_spacing=1.0)


def _panel_matriz(s, x, y, w, h):
    card(s, x, y, w, h, accent=YELLOW, brackets=True)
    pad = 32
    iw = w - 2 * pad
    label(s, x + pad, y + 28, iw, "Cross-encoder · 344 pares de test", color=YELLOW)
    # matriz
    rhw, g = 196, 12
    cw = (iw - rhw - g) / 2
    ch = 160
    mx = x + pad + rhw
    my = y + 112
    for j, t in enumerate(("Predicho: correspondencia", "Predicho: no corresponde")):
        label(s, mx + j * (cw + g), my - 36, cw, t, size=18, color=MUTED, align="center")
    filas = [("Real:", "corresponde", "231 pares",
              [("222", "Verdaderos positivos", YELLOW, "VP", None),
               ("9", "Falsos negativos", RED, "FN", None)]),
             ("Real: no", "corresponde", "113 pares",
              [("4", "Falsos positivos", RED, "FP", "los 4 títulos de la lámina 56"),
               ("109", "Verdaderos negativos", BLUE_LIGHT, "VN", None)])]
    for i, (r1, r2, n, celdas) in enumerate(filas):
        ry = my + i * (ch + g)
        text(s, x + pad, ry + ch / 2 - 46, rhw - 16, 56, [r1.upper(), r2.upper()], size=18,
             bold=True, font=FONT_HEAD, color=PAPER, spacing=1.5, line_spacing=1.2)
        text(s, x + pad, ry + ch / 2 + 14, rhw - 16, 30, n, size=21, font=FONT_TXT,
             color=MUTED, anchor="middle")
        for j, (v, r, col, ab, ex) in enumerate(celdas):
            _celda(s, mx + j * (cw + g), ry, cw, ch, v, r, col, ab, extra=ex)
    # tasas de error con su ecuación
    ey = my + 2 * ch + g + 26
    _divisor(s, x + pad, ey, iw, alpha=0.45)
    eqs = [
        [("var", "Tasa FP"), "=", ("frac", ["FP"], ["FP + VN"]), "=",
         ("frac", ["4"], ["113"]), "=", ("res", "3,5%")],
        [("var", "Tasa FN"), "=", ("frac", ["FN"], ["FN + VP"]), "=",
         ("frac", ["9"], ["231"]), "=", ("res", "3,9%")],
    ]
    zona = y + h - ey
    ew0 = max(medida_ecuacion(eq, size=32)[0] for eq in eqs)
    paso = zona / 2
    for k, eq in enumerate(eqs):
        ax = ey + paso * k + paso / 2 + 4
        ecuacion(s, x + pad + 8, ax, eq, size=32)
    lx = x + pad + ew0 + 64
    lw_ = x + w - pad - lx
    rect(s, lx - 30, ey + 24, 1.5, zona - 48, fill=BLUE_LIGHT, fill_alpha=0.35)
    cy = ey + (zona - 196) / 2
    label(s, lx, cy, lw_, "Umbral fijado en validación", size=18, color=MUTED)
    text(s, lx, cy + 30, lw_, 56, "0,998844", size=44, bold=True, font=FONT_HEAD, color=YELLOW,
         anchor="middle", line_spacing=1.0)
    text(s, lx, cy + 96, lw_, 100,
         "Se aplicó al test sin retocarlo: es la única forma de que la cifra signifique algo.",
         size=22, font=FONT_TXT, color=PAPER, line_spacing=1.25)


TECHO = [
    ("Consultas de test", "publicaciones a resolver", 147, LINE, "147"),
    ("Con el correcto en el pool", "techo · 91,8%", 135, YELLOW, "135"),
    ("En las cinco primeras", "Recall@5 · 87,8%", 129, BLUE_LIGHT, "129"),
    ("En primera posición", "Recall@1 · 82,3% · MRR 0,8515", 121, BLUE_LIGHT, "121"),
]


def _panel_techo(s, x, y, w, h):
    card(s, x, y, w, h, accent=BLUE_LIGHT)
    pad = 30
    iw = w - 2 * pad
    label(s, x + pad, y + 28, iw, "Techo del recuperador · 147 consultas", color=YELLOW)
    vw = 84
    bw = iw - vw - 14
    bx = x + pad
    r0, pitch = y + 74, 86
    filas = TECHO + [("Imposibles", "la verdad nunca entró al pool", 12, RED, "12")]
    for k, (nom, det, v, col, vs) in enumerate(filas):
        ry = r0 + k * pitch
        ex = _seg(s, bx, ry, [(nom, FONT_HEAD, 21, PAPER, True)], h=30, gap=12)
        text(s, ex, ry, bx + bw - ex, 30, det, size=20, font=FONT_TXT, color=MUTED,
             anchor="middle")
        if k < len(TECHO):
            bar(s, bx, ry + 40, bw, 24, v / 147, color=col)
        else:
            # los 12 imposibles: el tramo entre el techo y el total
            rect(s, bx, ry + 40, bw, 24, fill=CHIP)
            rect(s, bx + bw * 135 / 147, ry + 40, bw * 12 / 147, 24, fill=RED)
        _valor(s, bx + bw + 8, ry + 30, vw + 6, vs, size=32,
               color=RED if col == RED else (YELLOW if col == YELLOW else PAPER),
               align="right", h=44)
    tx = bx + bw * 135 / 147
    line(s, tx, r0 + 30, tx, r0 + 4 * pitch + 74, color=YELLOW, width=2, alpha=0.9,
         dash="dash")
    # ecuación del techo + consecuencia
    ey = r0 + 5 * pitch + 4
    _divisor(s, x + pad, ey, iw, alpha=0.45)
    eq = [("var", "Techo"), "=", ("frac", ["135"], ["147"]), "=", ("res", "91,8%")]
    ew, up, dn = medida_ecuacion(eq, size=32)
    ax = ey + 20 + up
    ecuacion(s, x + pad + 8, ax, eq, size=32)
    text(s, x + pad, ax + dn + 14, iw, y + h - (ax + dn + 14) - 20,
         [[{"text": "De los 26 fallos en primera posición, 12 son irrecuperables: ",
            "color": PAPER},
           {"text": "hay que ensanchar la recuperación.", "color": YELLOW, "bold": True}]],
         size=22, font=FONT_TXT, anchor="middle", line_spacing=1.25)


def p16(prs, notas):
    """Láminas 76 + 77: matriz de confusión del cross-encoder y techo del recuperador."""
    s = add_slide(prs, bg_image=FONDO)
    subencabezado(s, OE5 + " · Cross-encoder en test",
                  "Matriz de confusión y techo del recuperador")
    lw, g = 1000, 28
    _panel_matriz(s, 96, TOP, lw, BOTTOM - TOP)
    _panel_techo(s, 96 + lw + g, TOP, 1728 - lw - g, BOTTOM - TOP)
    notes(s, " ".join(notas[i] for i in (76, 77)))


# ------------------------------------------------------------------- P17
GOLD = [("M1", "TF-IDF", 0.615, "0,615", YELLOW),
        ("M2", "Embeddings", 0.183, "0,183", RED),
        ("M3", ["Unión +", "reordenador"], 0.615, "0,615", YELLOW)]

PAISES = [
    ("Kuwait · Xcite", "173 consultas · 67,6% automatizadas", 100.0, "100,0%", False),
    ("Sudáfrica · Makro", "353 consultas · 45,3% automatizadas", 98.1, "98,1%", False),
    ("Vietnam · ShopeeVN + LazadaVN", "293 consultas · 62,1% automatizadas", 96.2, "96,2%",
     False),
    ("Alemania · AmazonDE + MediamarktDE", "360 consultas · 23 errores", 87.6, "87,6%", True),
    ("Estados Unidos · AmazonUS", "124 consultas · 18 errores", 80.9, "80,9%", True),
]


def _panel_gold(s, x, y, w, h):
    card(s, x, y, w, h, accent=BLUE_LIGHT)
    pad = 30
    iw = w - 2 * pad
    label(s, x + pad, y + 28, iw, "Gold externo", color=YELLOW)
    text(s, x + pad, y + 58, iw, 64, "213 consultas anotadas a mano, fuera del entrenamiento",
         size=22, font=FONT_TXT, color=PAPER, line_spacing=1.2)
    label(s, x + pad, y + 118, iw, "Recall@1 · escala 0–1", color=MUTED)
    # columnas proporcionales (pista = 1,0)
    base, hm = y + 400, 236
    colw = 112
    gap = (iw - 3 * colw) / 2
    for k, (m, nom, v, vs, col) in enumerate(GOLD):
        cx = x + pad + k * (colw + gap)
        rect(s, cx, base - hm, colw, hm, fill=CHIP)
        rect(s, cx, base - hm * v, colw, hm * v, fill=col)
        _valor(s, cx - 30, base - hm * v - 54, colw + 60, vs, size=34,
               color=YELLOW if col == YELLOW else RED, align="center", h=44)
        lx0 = max(x + pad, cx - gap / 2 + 4)
        lx1 = min(x + w - pad, cx + colw + gap / 2 - 4)
        text(s, lx0, base + 10, lx1 - lx0, 34, m, size=26, bold=True, font=FONT_HEAD,
             color=YELLOW if col == YELLOW else RED, align="center", anchor="middle")
        text(s, lx0, base + 44, lx1 - lx0, 56, nom, size=20, font=FONT_TXT, color=MUTED,
             align="center", line_spacing=1.15)
    # diferencia M3 − M1
    ey = base + 104
    _divisor(s, x + pad, ey, iw, alpha=0.45)
    # Δ en redonda (texto normal): en cursiva parecía un triángulo rectángulo
    eq = ["Δ", "=", "0,615", "−", "0,615", "=", ("res", "0,0")]
    ew, up, dn = medida_ecuacion(eq, size=34)
    ax = ey + 20 + up
    ecuacion(s, x + pad + 4, ax, eq, size=34)
    gy = ax + dn + 10
    text(s, x + pad, gy, iw, 52,
         ["Diferencia M3 − M1 · bootstrap de 10.000 muestras",
          "IC 95% [−0,047; +0,047] · p = 1,0"], size=20, font=FONT_TXT, color=MUTED,
         line_spacing=1.2)
    my = gy + 62
    text(s, x + pad, my, iw, 58,
         "El reordenador no recupera mejor: decide cuándo automatizar", size=23, bold=True,
         font=FONT_HEAD, color=YELLOW, line_spacing=1.2)


def _panel_bench(s, x, y, w, h):
    card(s, x, y, w, h, accent=YELLOW, brackets=True)
    pad = 32
    iw = w - 2 * pad
    label(s, x + pad, y + 28, iw, "Benchmark multipaís v7.5 · 19 países · retailers no vistos",
          color=YELLOW)
    kp = [("2.365", "Publicaciones", "evaluadas", PAPER),
          ("54,2%", "Automatizadas", "1.282 de 2.365", PAPER),
          ("94,5%", "Precisión", "de lo automatizado", YELLOW),
          ("70", "Desacuerdos", "externos", RED)]
    kw = iw / 4
    for k, (v, r, sub, col) in enumerate(kp):
        kx = x + pad + k * kw
        if k:
            rect(s, kx - 16, y + 76, 1.5, 110, fill=BLUE_LIGHT, fill_alpha=0.35)
        text(s, kx, y + 66, kw - 24, 70, v, size=56, bold=True, font=FONT_HEAD, color=col,
             anchor="middle", line_spacing=1.0)
        label(s, kx, y + 138, kw - 24, r, size=18, color=PAPER)
        text(s, kx, y + 164, kw - 24, 28, sub, size=20, font=FONT_TXT, color=MUTED,
             anchor="middle")
    _divisor(s, x + pad, y + 204, iw, alpha=0.45)
    label(s, x + pad, y + 220, iw, "Precisión de lo automatizado por retailer", color=MUTED)
    vw = 130
    bw = iw - vw - 16
    bx = x + pad
    r0, pitch = y + 262, 74
    mx = bx + bw * 0.945
    line(s, mx, y + 250, mx, r0 + 4 * pitch + 66, color=PAPER, width=2, alpha=0.6,
         dash="dash")
    text(s, mx - 200, y + 218, 190, 28, "global 94,5%", size=19, font=FONT_TXT,
         color=PAPER, align="right", anchor="middle")
    for k, (nom, det, v, vs, peor) in enumerate(PAISES):
        ry = r0 + k * pitch
        col = RED if peor else YELLOW
        ex = _seg(s, bx, ry, [(nom, FONT_HEAD, 22, PAPER, True)], h=30, gap=12)
        ex = _seg(s, ex, ry, [(det, FONT_TXT, 20, MUTED, False)], h=30, gap=12)
        if peor:
            tag(s, ex - 2, ry - 2, "Marketplace", fill=RED, color=PAPER, size=20, h=34, pad=8)
        bar(s, bx, ry + 40, bw, 22, v / 100, color=col, marker=0.945)
        _valor(s, bx + bw + 8, ry + 28, vw + 8, vs, size=30, color=col, align="right", h=44)
    text(s, x + pad, y + h - 88, iw, 60,
         [[{"text": "Los dos peores son los marketplaces más grandes: ", "color": PAPER},
           {"text": "títulos de vendedores terceros, sin código.", "color": PAPER,
            "bold": True}],
          [{"text": "La degradación tiene una causa identificable, no es ruido.",
            "color": YELLOW, "bold": True}]],
         size=22, font=FONT_TXT, anchor="middle", line_spacing=1.2)


def p17(prs, notas):
    """Láminas 78 + 80: gold externo y benchmark multipaís v7.5."""
    s = add_slide(prs, bg_image=FONDO)
    subencabezado(s, OE5 + " · Evidencia fuera del dataset",
                  "Evidencia externa: gold y benchmark multipaís")
    lw, g = 600, 28
    _panel_gold(s, 96, TOP, lw, BOTTOM - TOP)
    _panel_bench(s, 96 + lw + g, TOP, 1728 - lw - g, BOTTOM - TOP)
    notes(s, " ".join(notas[i] for i in (78, 80)))


# ------------------------------------------------------------------- P18
CASOS = [
    {"origen": "Coolbluebe · Bélgica",
     "titulo": [("Philips Ambilight 43\" ", PAPER), ("PUS8550", YELLOW), (" QLED (2025)", PAPER)],
     "rasgo": ("Publicado tal cual", LINE, DARK), "explica": None,
     "elegido": ("43PUS8550/12", YELLOW), "score": "0,994589",
     "tercero": ("Margen", "0,010567", PAPER),
     "decision": ("Revisión", BLUE_LIGHT, PAPER), "resultado": ("Candidato correcto", PAPER),
     "accent": BLUE_LIGHT},
    {"origen": "Coolbluebe · Bélgica",
     "titulo": [("Philips 55\" ", PAPER), ("PUS7800", YELLOW),
                (" QLED 4K (2025) + Philips ", PAPER), ("TAB5309", YELLOW)],
     "rasgo": ("Compuesta", RED, PAPER),
     "explica": "Televisor + barra de sonido: no es un solo producto",
     "elegido": ("TAB5309/10", YELLOW), "score": "0,996685",
     "tercero": ("Margen", "0,002209", YELLOW),
     "decision": ("Revisión", BLUE_LIGHT, PAPER),
     "resultado": ("Se abstiene por la razón correcta", YELLOW), "gold": "NIC",
     "accent": YELLOW},
    {"origen": "AmazonDE · Alemania",
     "titulo": [("Philips TV Philips ", PAPER), ("32PFS5603/12", YELLOW),
                (" 80\u00a0cm (32\u00a0Zoll) Full-HD Fernseher (Triple Tuner), Weiß", PAPER)],
     "rasgo": ("Código completo", YELLOW, DARK), "explica": None,
     "elegido": ("32PFS5603/12", YELLOW), "score": "0,999573",
     "tercero": ("Gold", "32PFS5603/12", YELLOW),
     "decision": ("Match", YELLOW, DARK), "resultado": ("Automatizado y correcto", YELLOW),
     "accent": YELLOW},
    {"origen": "Makro · Sudáfrica", "titulo": [("Philips Air Fryer (7.2\u00a0L)", PAPER)],
     "rasgo": ("Ningún código", RED, PAPER),
     "explica": "Describe varias freidoras del catálogo",
     "elegido": ("NA341/00", YELLOW), "score": "0,999650",
     "tercero": ("Gold", "HD9285/90", RED),
     "decision": ("Match", RED, PAPER), "resultado": ("Automatizado y errado", RED),
     "accent": RED},
]


def _caso(s, x, y, w, h, c):
    card(s, x, y, w, h, accent=c["accent"], accent_side="left")
    pad = 28
    label(s, x + pad, y + 16, w - 2 * pad, c["origen"], color=MUTED)
    my, mh = y + 52, h - 52 - 20
    # A) publicación
    aw = 310
    ax0 = x + pad
    rect(s, ax0, my, aw, mh, fill=CHIP, line=BLUE_LIGHT, line_w=1, line_alpha=0.35,
         radius=6)
    label(s, ax0 + 16, my + 12, aw - 32, "Título publicado", size=18, color=MUTED)
    _runs(s, ax0 + 16, my + 44, aw - 32, mh - 100, c["titulo"], size=20, font=FONT_MONO,
          line_spacing=1.25)
    fondo = my + mh - 14
    if c["rasgo"]:
        rt, rf, rc = c["rasgo"]
        # 20 px en negrita: texto grande, contraste suficiente sobre el rojo
        tag(s, ax0 + 16, fondo - 34, rt, fill=rf, color=rc, size=20, h=34, pad=8)
        fondo -= 46
    if c["explica"]:
        lineas = wrap_lines(c["explica"], 20, aw - 46, FONT_TXT)
        eh = len(lineas) * 25
        rect(s, ax0 + 16, fondo - eh, 3, eh, fill=RED)
        text(s, ax0 + 28, fondo - eh, aw - 44, eh, c["explica"], size=20, font=FONT_TXT,
             color=PAPER, line_spacing=1.25, anchor="middle")
    # B) lo que eligió el modelo
    bx = x + pad + aw + 42
    flecha(s, x + pad + aw + 8, my + mh / 2, bx - 8, h=22)
    bwid = 172
    filas = [("Elegido", c["elegido"][0], "chip", c["elegido"][1]),
             ("Score", c["score"], "num", PAPER),
             (c["tercero"][0], c["tercero"][1],
              "chip" if "/" in c["tercero"][1] else "num", c["tercero"][2])]
    for j, (r, v, kind, col) in enumerate(filas):
        yy = my + j * (mh / 3)
        label(s, bx, yy + 2, bwid, r, size=18, color=MUTED)
        if kind == "chip":
            chip(s, bx, yy + 30, v, size=20, h=34, pad=10, color=col,
                 border=RED if col == RED else BLUE_LIGHT)
        else:
            _valor(s, bx, yy + 28, bwid, v, size=28, color=col, h=38)
    # C) decisión
    cx = bx + bwid + 40
    flecha(s, bx + bwid + 4, my + mh / 2, cx - 8, h=22)
    cw = x + w - pad - cx
    dt, df, dc = c["decision"]
    label(s, cx, my + 2, cw, "Decisión", size=18, color=MUTED)
    tag(s, cx, my + 34, dt, fill=df, color=dc, size=20, h=44, pad=16)
    rtxt, rcol = c["resultado"]
    text(s, cx, my + 96, cw, 90, rtxt, size=22, bold=True, font=FONT_HEAD, color=rcol,
         line_spacing=1.2)
    if c.get("gold"):
        label(s, cx, my + mh - 70, cw, "Gold", size=18, color=MUTED)
        chip(s, cx, my + mh - 40, c["gold"], size=20, h=34, pad=10)


def p18(prs, notas):
    """Láminas 79 + 81: casos reales fuera del dataset."""
    s = add_slide(prs, bg_image=FONDO)
    subencabezado(s, OE5 + " · Evidencia fuera del dataset",
                  "Casos reales: cuándo automatiza y cuándo se abstiene")
    g = 28
    cw = (1728 - g) / 2
    hy = 274
    cabeceras = [("Bélgica · dos publicaciones reales", "el margen delata la ambigüedad"),
                 ("Retailers no vistos · mismo umbral", "scores casi idénticos, dos desenlaces")]
    for k, (t1, t2) in enumerate(cabeceras):
        x = 96 + k * (cw + g)
        ex = _seg(s, x, hy, [(t1, FONT_HEAD, 24, PAPER, True)], h=34, gap=14)
        text(s, ex, hy, x + cw - ex, 34, t2, size=21, font=FONT_TXT, color=MUTED,
             anchor="middle")
    y0 = hy + 46
    fy = BOTTOM - 32            # conclusión de la lámina 81, bajo las cuatro tarjetas
    vg = 16
    ch = (fy - 14 - y0 - vg) / 2
    for k, c in enumerate(CASOS):
        col, row = k // 2, k % 2
        _caso(s, 96 + col * (cw + g), y0 + row * (ch + vg), cw, ch, c)
    text(s, 96, fy, 1728, 32,
         [[{"text": "Sin código, el modelo elige una freidora plausible con total confianza: ",
            "color": PAPER},
           {"text": "es el límite del método, y marca dónde sigue haciendo falta el operador.",
            "color": YELLOW, "bold": True}]],
         size=22, font=FONT_TXT, anchor="middle", line_spacing=1.0)
    notes(s, " ".join(notas[i] for i in (79, 81)))


def construir(prs, notas):
    p15(prs, notas)
    p16(prs, notas)
    p17(prs, notas)
    p18(prs, notas)
