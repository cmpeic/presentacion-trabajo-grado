"""Grupo g3: OE4 · modelos, protocolo, medidas de similitud y arquitectura (P08-P11)."""

from pptx_kit import FONT_MONO, add_slide, arrow_shape, ellipse, line, notes, rect, text
from theme import BLUE_TEXT, FONDO, LINE, MUTED, PAPER, YELLOW
from componentes import (BLUE_LIGHT, CHIP, DARK, FONT_HEAD, FONT_TXT, PANEL_2, RED, _Eq, bar,
                         card, chip, ecuacion, flecha, flecha_abajo, label,
                         medida_ecuacion, numbadge, subencabezado, tag, text_width)

OE4 = "OE4 · Diseñar los modelos"


# ----------------------------------------------------------------- utilidades
def _h(s, x, y, w, h, contenido, size=26, color=PAPER, align="left", anchor="top", ls=1.15):
    """Texto en Montserrat negrita (títulos y cifras)."""
    text(s, x, y, w, h, contenido, size=size, bold=True, font=FONT_HEAD, color=color,
         align=align, anchor=anchor, line_spacing=ls)


def _b(s, x, y, w, h, contenido, size=21, color=PAPER, bold=False, align="left",
       anchor="top", ls=1.25):
    """Texto en Barlow (cuerpo)."""
    text(s, x, y, w, h, contenido, size=size, font=FONT_TXT, color=color, bold=bold,
         align=align, anchor=anchor, line_spacing=ls)


def _tag_w(s, size=18, pad=14):
    """Ancho que ocupará `tag(...)` con el mismo texto y tamaño."""
    return text_width(s.upper(), size, FONT_HEAD, True, spacing=1.2) + 2 * pad + 6


def _chip_w(s, size=20, pad=12):
    return text_width(s, size, FONT_MONO) + 2 * pad + 4


def _sep_v(s, x, y, h, alpha=0.25):
    rect(s, x, y, 1.5, h, fill=BLUE_LIGHT, fill_alpha=alpha)


def _sep_h(s, x, y, w, alpha=0.25):
    rect(s, x, y, w, 1.5, fill=BLUE_LIGHT, fill_alpha=alpha)


def _flecha_baja(s, cx, y, largo=22, ancho=16, color=MUTED):
    """Flecha de bloque hacia abajo (la forma, no el glifo «↓»), de y a y + largo."""
    shp = arrow_shape(s, cx - largo / 2, y + (largo - ancho) / 2, largo, ancho, color=color)
    shp.rotation = 90


def _par(s, x, y, h, a, b, color, size=24):
    """«A → B» con la flecha dibujada como forma (el glifo «→» se ve diminuto)."""
    wa = text_width(a, size, FONT_HEAD, True)
    wb = text_width(b, size, FONT_HEAD, True)
    _h(s, x, y, wa + 8, h, a, size=size, color=color, anchor="middle")
    ax = x + wa + 10
    flecha(s, ax, y + h / 2, ax + 26, color=color, h=16)
    _h(s, ax + 34, y, wb + 8, h, b, size=size, color=color, anchor="middle")


# ======================================================================= P08
def _caja_letra(s, x, y, letra, color, w=50, h=40):
    rect(s, x, y, w, h, fill=CHIP, line=color, line_w=1.5, radius=6)
    _h(s, x, y, w, h, letra, size=21, color=color, align="center", anchor="middle")


def _nodo(s, cx, cy, txt, color, r=31):
    ellipse(s, cx, cy, r, fill=CHIP, line=color, line_w=2)
    _b(s, cx - r, cy - r, 2 * r, 2 * r, txt, size=19, color=PAPER, align="center",
       anchor="middle", ls=1.0)


def _esquema_modelo(s, k, sx, sy, color):
    """Mini esquema de qué mira cada modelo (300 x 150 px)."""
    ya, yb = sy + 14, sy + 96
    ca, cb = ya + 20, yb + 20
    cm = (ca + cb) / 2
    nx = sx + 266
    if k < 2:                                    # cada texto por su lado
        _caja_letra(s, sx, ya, "A", YELLOW)
        _caja_letra(s, sx, yb, "B", BLUE_TEXT)
        for cy, patron in ((ca, (1, 0, 0, 1, 0, 0, 0, 1)), (cb, (0, 1, 0, 1, 0, 0, 1, 0))):
            flecha(s, sx + 56, cy, sx + 86, color=LINE, h=14)
            if k == 0:                           # vector disperso de n-gramas
                for i, on in enumerate(patron):
                    rect(s, sx + 94 + i * 13, cy - 10, 10, 20,
                         fill=BLUE_LIGHT if on else CHIP, line=None if on else BLUE_LIGHT,
                         line_w=1, line_alpha=0.35)
                x_fin = sx + 94 + 8 * 13 - 3
            else:                                # encoder congelado
                rect(s, sx + 94, cy - 20, 104, 40, fill=PANEL_2, line=LINE, line_w=1.5,
                     radius=6)
                _b(s, sx + 94, cy - 20, 104, 40, "encoder", size=19, color=MUTED,
                   align="center", anchor="middle", ls=1.0)
                x_fin = sx + 198
            line(s, x_fin + 6, cy, nx - 34, cm + (-10 if cy == ca else 10), color=LINE,
                 width=2, arrow=True)
        _nodo(s, nx, cm, "cos", color)
    else:                                        # una sola secuencia
        rect(s, sx - 8, ya - 10, 66, (yb + 40) - ya + 20, fill=None, line=YELLOW, line_w=2,
             radius=8)
        _caja_letra(s, sx, ya, "A", YELLOW)
        _caja_letra(s, sx, yb, "B", BLUE_TEXT)
        flecha(s, sx + 64, cm, sx + 92, color=YELLOW, h=16)
        bx, bw, bh = sx + 98, 120, 112
        rect(s, bx, cm - bh / 2, bw, bh, fill=PANEL_2, line=YELLOW, line_w=1.5,
             line_alpha=0.6, radius=6)
        x1, x2 = bx + 24, bx + bw - 24
        y1, y2 = cm - 26, cm + 26
        line(s, x1, y1, x2, y1, color=LINE, width=2)
        line(s, x1, y2, x2, y2, color=LINE, width=2)
        line(s, x1, y1, x2, y2, color=YELLOW, width=3)
        line(s, x1, y2, x2, y1, color=YELLOW, width=3)
        for xx in (x1, x2):
            ellipse(s, xx, y1, 7, fill=YELLOW)
            ellipse(s, xx, y2, 7, fill=BLUE_LIGHT)
        line(s, bx + bw + 4, cm, nx - 34, cm, color=YELLOW, width=2, arrow=True)
        _nodo(s, nx, cm, "score", color)


MODELOS = [
    # nombre, subtítulo, mira, color, esquema, cifra, métrica, rol, fondo rol, texto rol
    ("TF-IDF", "n-gramas de caracteres", "nada", BLUE_TEXT, "Vectores dispersos · coseno",
     "91,16%", "Recall@10", "Recuperador", BLUE_LIGHT, PAPER),
    ("Embeddings", "encoders congelados", "lo propio", RED, "Cada texto por separado",
     "8,84%", "Recall@1", "Fracaso legítimo", RED, PAPER),
    ("Cross-encoder", "fine-tuneado", "todo", YELLOW, "Una secuencia · atención cruzada",
     "97,41%", "F1 de pares", "Validador", YELLOW, DARK),
]

TOKENS_A = ["[CLS]", "philips", "neopix", "150", "npx150/int", "[SEP]"]
TOKENS_B = ["proyector", "philips", "neopix", "150", "npx150/90", "[SEP]"]


def p08(prs, notas):
    """Láminas 61 + 62: qué puede mirar cada modelo y los cuadrantes de atención cruzada."""
    s = add_slide(prs, bg_image=FONDO)
    subencabezado(s, OE4 + " · Modelos algorítmicos",
                  "¿Qué puede mirar cada modelo al comparar dos textos?")
    # --- izquierda: tres modelos ------------------------------------------
    x, w, rh, gap = 96, 944, 228, 20
    for k, (nom, sub, mira, col, cap, cifra, met, rol, rfill, rcol) in enumerate(MODELOS):
        y = 276 + k * (rh + gap)
        card(s, x, y, w, rh, accent=col if col != BLUE_TEXT else BLUE_LIGHT,
             accent_side="left")
        numbadge(s, x + 28, y + 26, str(k + 1), size=44,
                 fill=YELLOW if k == 2 else (RED if k == 1 else BLUE_LIGHT),
                 color=DARK if k == 2 else PAPER)
        _h(s, x + 88, y + 24, 230, 40, nom, size=28)
        _b(s, x + 88, y + 62, 230, 30, sub, size=20, color=MUTED)
        label(s, x + 28, y + 118, 260, "Mira", size=18, color=MUTED)
        _h(s, x + 28, y + 142, 270, 56, mira, size=40, color=col)
        _sep_v(s, x + 312, y + 24, rh - 48)
        _esquema_modelo(s, k, x + 340, y + 22, col)
        _b(s, x + 316, y + 182, 330, 30, cap, size=20, color=MUTED, align="center")
        _sep_v(s, x + 656, y + 24, rh - 48)
        kx = x + 684
        _h(s, kx, y + 22, 240, 66, cifra, size=52, color=RED if k == 1 else YELLOW)
        label(s, kx, y + 92, 240, met, size=18, color=PAPER)
        tag(s, kx, y + 152, rol, fill=rfill, color=rcol, size=18, h=36)
    # --- derecha: lectura conjunta del modelo 3 ---------------------------
    px_, pw = 1072, 752
    py, ph = 276, 3 * rh + 2 * gap
    card(s, px_, py, pw, ph, accent=None, brackets=True)
    ix, iw = px_ + 28, pw - 56
    label(s, ix, py + 20, iw, "Modelo 3 · la lectura conjunta", color=YELLOW)
    # A y B entran juntos: una sola secuencia (marco con pestaña)
    fx0, fx1 = ix - 10, ix + iw + 10
    fty = py + 56
    rect(s, fx0, fty, fx1 - fx0, 104, fill=None, line=YELLOW, line_w=1.5, line_alpha=0.8,
         radius=6)
    tab = "Una sola secuencia"
    tag(s, fx1 - _tag_w(tab), py + 18, tab, size=18, h=31)
    for r, (letra, toks, col) in enumerate((("A", TOKENS_A, YELLOW),
                                            ("B", TOKENS_B, BLUE_TEXT))):
        ty = fty + 10 + r * 46
        _h(s, ix + 4, ty, 30, 38, letra, size=24, color=col, anchor="middle")
        cx = ix + 40
        for t in toks:
            especial = t.startswith("[")
            codigo = t.startswith("npx")
            cw = chip(s, cx, ty, t, size=18, h=38, pad=10,
                      color=DARK if codigo else (MUTED if especial else col),
                      fill=YELLOW if codigo else CHIP,
                      border=YELLOW if codigo else (LINE if especial else col))
            cx += cw + 8
    # ejes de la matriz: filas = consulta, columnas = atendido
    ay = fty + 104 + 16
    _flecha_baja(s, ix + 15, ay + 2, largo=22, ancho=14)
    label(s, ix + 40, ay, 140, "Consulta", size=18, color=MUTED)
    ax_ = ix + 40 + text_width("CONSULTA", 18, FONT_HEAD, True, spacing=1.5) + 22
    label(s, ax_, ay, 30, "·", size=18, color=MUTED)
    ax_ += 26
    label(s, ax_, ay, 140, "Atendido", size=18, color=MUTED)
    ax_ += text_width("ATENDIDO", 18, FONT_HEAD, True, spacing=1.5) + 12
    flecha(s, ax_, ay + 13.5, ax_ + 26, color=MUTED, h=14)
    # matriz de atención 2 x 2
    my = ay + 36
    hw, cw_, ch_, g = 44, (iw - 44 - 12) / 2, 124, 12
    c1, c2 = ix + hw, ix + hw + cw_ + g
    label(s, c1, my, cw_, "A · producto oficial", size=18, color=YELLOW)
    label(s, c2, my, cw_, "B · publicación retailer", size=18, color=BLUE_TEXT)
    celdas = {
        (0, 0): (("A", "A"), ["Se lee a sí mismo. Es lo único que ve el Modelo 2."], False),
        (0, 1): (("A", "B"), ["Cada token del catálogo consulta el título del retailer."],
                 True),
        (1, 0): (("B", "A"), [[{"text": "Y al revés: el sufijo "},
                               {"text": "/90", "bold": True, "color": YELLOW},
                               {"text": " se confronta con "},
                               {"text": "/INT", "bold": True, "color": YELLOW},
                               {"text": "."}]], True),
        (1, 1): (("B", "B"), ["La publicación se lee a sí misma."], False),
    }
    for r, letra in enumerate("AB"):
        ry = my + 34 + r * (ch_ + g)
        _h(s, ix, ry, hw - 8, ch_, letra, size=30, color=YELLOW if r == 0 else BLUE_TEXT,
           anchor="middle")
        for c in range(2):
            (a, b), cuerpo, cruce = celdas[(r, c)]
            cx = c1 if c == 0 else c2
            rect(s, cx, ry, cw_, ch_, fill=CHIP if cruce else PANEL_2,
                 line=YELLOW if cruce else BLUE_LIGHT, line_w=2 if cruce else 1.2,
                 line_alpha=1 if cruce else 0.35)
            _par(s, cx + 20, ry + 14, 34, a, b, YELLOW if cruce else PAPER)
            if cruce:
                tag(s, cx + cw_ - 20 - _tag_w("Cruce"), ry + 15, "Cruce", size=18, h=32)
            _b(s, cx + 20, ry + 56, cw_ - 40, ch_ - 64, cuerpo, size=20,
               color=PAPER if cruce else MUTED)
    # falso positivo por sufijo distinto
    fy = my + 34 + 2 * ch_ + g + 26
    label(s, ix, fy, iw, "Falso positivo por sufijo distinto", size=18, color=YELLOW)
    fps = [("TF-IDF", 36.59, "36,59%", BLUE_LIGHT, PAPER),
           ("Embeddings", 90.24, "90,24%", RED, RED),
           ("Cross-encoder", 4.88, "4,88%", YELLOW, YELLOW)]
    bx, bw = ix + 176, iw - 176 - 118
    for k, (nom, v, vs, col, tcol) in enumerate(fps):
        yy = fy + 38 + k * 44
        _b(s, ix, yy, 170, 34, nom, size=20, color=PAPER, anchor="middle")
        bar(s, bx, yy + 7, bw, 20, v / 100, color=col)
        _h(s, bx + bw + 8, yy, 110, 34, vs, size=24, color=tcol, align="right",
           anchor="middle")
    notes(s, " ".join(notas[i] for i in (61, 62)))


# ======================================================================= P09
def _ecuacion_config(s, x, ay, w, size=40):
    """8 × 2 + 3 × 2 + 1 = 23 con una llave bajo cada término y el modelo que aporta.

    Los operadores quedan a la misma distancia de los términos; la separación se
    elige para que los rótulos de los modelos no se toquen.
    """
    terminos = [("8 × 2", "TF-IDF", BLUE_TEXT), ("3 × 2", "Embeddings", RED),
                ("1", "Cross-encoder", YELLOW)]
    eq = _Eq(size=size)
    tws = [eq.measure([t])[0] for t, _, _ in terminos]
    lws = [text_width(n, 18, FONT_HEAD, True) for _, n, _ in terminos]
    g = 40.0
    for k in range(2):
        g = max(g, (lws[k] + lws[k + 1]) / 2 + 34 - (tws[k] + tws[k + 1]) / 2)
    res_w = eq.measure([("res", "23")], size * 1.1)[0]
    total = sum(tws) + 3 * g + res_w
    cx = x + max(0, (w - total) / 2) + max(0, (lws[0] - tws[0]) / 2)
    for k, (t, nom, col) in enumerate(terminos):
        tw = tws[k]
        ecuacion(s, cx, ay, [t], size=size)
        mid = cx + tw / 2
        bw_ = max(tw, 40)
        by = ay + size * 0.78
        rect(s, mid - bw_ / 2, by, bw_, 3, fill=col)
        rect(s, mid - bw_ / 2, by - 8, 3, 11, fill=col)
        rect(s, mid + bw_ / 2 - 3, by - 8, 3, 11, fill=col)
        rect(s, mid - 1.5, by, 3, 12, fill=col)
        _h(s, mid - lws[k] / 2 - 20, by + 18, lws[k] + 40, 30, nom, size=18, color=col,
           align="center")
        cx += tw
        op = "=" if k == 2 else "+"
        ecuacion(s, cx, ay, [op], size=size, align="center", w=g)
        cx += g
    ecuacion(s, cx, ay, [("res", "23")], size=size * 1.1)


RECALL = [
    ("Palabras 1-1", "word unigrama", 0.2593, "0,2593", 0.7523, "0,7523"),
    ("Palabras 1-3", "word trigrama", 0.2383, "0,2383", 0.7406, "0,7406"),
    ("Caracteres 3-5", "char_wb", 0.4953, "0,4953", 0.8060, "0,8060"),
    ("Caracteres 4-6", "char_wb · seleccionada", 0.5116, "0,5116", 0.8317, "0,8317"),
    ("Híbrido w25", "word 1-2 + char 3-5", 0.4929, "0,4929", 0.8177, "0,8177"),
    ("BM25", "ponderación probabilística", None, "—", 0.6985, "0,6985"),
]


def p09(prs, notas):
    """Láminas 63 + 69: protocolo temporal sin fuga y configuraciones del recuperador."""
    s = add_slide(prs, bg_image=FONDO)
    subencabezado(s, OE4 + " · Protocolo experimental",
                  "Protocolo sin fuga: lo que decide no es el algoritmo")
    # --- izquierda: protocolo temporal ------------------------------------
    x, w = 96, 620
    label(s, x, 276, w, "Protocolo fijado antes de evaluar", color=YELLOW)
    fases = [
        ("Train", BLUE_LIGHT, PAPER, "2025-01 … 10", None,
         "Ajusta las transformaciones. Nada más.", 104),
        ("Validation", YELLOW, DARK, "2025-11", "428 consultas",
         "Selecciona configuración y umbral.", 184),
        ("Test", YELLOW, DARK, "2025-12", "147 consultas",
         "Se abre una sola vez, al cerrar.", 104),
    ]
    y = 312
    for k, (nom, tfill, tcol, periodo, consultas, rol, h) in enumerate(fases):
        card(s, x, y, w, h, accent=tfill, accent_side="left")
        tw = tag(s, x + 28, y + 20, nom, fill=tfill, color=tcol, size=18, h=36)
        _h(s, x + 28 + tw + 18, y + 16, 240, 44, periodo, size=28, anchor="middle")
        if consultas:
            _h(s, x + w - 28 - 260, y + 16, 260, 44, consultas, size=28, color=YELLOW,
               align="right", anchor="middle")
        _b(s, x + 28, y + 62, w - 56, 30, rol, size=21, color=MUTED)
        if k == 1:
            # lo que se fija en validación, rotulado con el modelo al que pertenece
            sel = [("TF-IDF", BLUE_TEXT, "char_4_6_enriched"),
                   ("Cross-encoder", YELLOW, "umbral 0,998844")]
            cx = x + 28
            for nom_m, col_m, valor in sel:
                label(s, cx, y + 100, 260, nom_m, size=18, color=col_m)
                cx += chip(s, cx, y + 128, valor, size=19, h=36, pad=12) + 28
        y += h
        if k < 2:
            flecha_abajo(s, x + w / 2, y + 2, y + 24, w=22)
            y += 24
    # 23 configuraciones declaradas: 8 x 2 + 3 x 2 + 1
    cy0 = y + 24
    ch = 1000 - cy0
    card(s, x, cy0, w, ch, accent=None, fill=PANEL_2)
    label(s, x + 28, cy0 + 18, w - 56, "Configuraciones declaradas", color=MUTED)
    _ecuacion_config(s, x + 28, cy0 + 104, w - 56)
    # --- derecha: Recall@1 en validación ----------------------------------
    px_, pw = 752, 1072
    card(s, px_, 276, pw, 724, accent=None, brackets=True)
    ix, iw = px_ + 32, pw - 64
    label(s, ix, 298, iw, "Recuperador · 17 configuraciones evaluadas · Recall@1 en validación",
          color=YELLOW)
    # leyenda: rótulo y subtítulo en un mismo cuadro, con el «·» centrado
    lx = ix
    for col, nom, sub in ((LINE, "Texto básico", "solo el nombre"),
                          (BLUE_LIGHT, "Texto enriquecido", "nombre + códigos + EAN")):
        rect(s, lx, 344, 18, 18, fill=col, radius=3)
        tw = (text_width(nom, 20, FONT_TXT, True) + text_width("  ·  " + sub, 20, FONT_TXT)
              + 24)
        _b(s, lx + 28, 336, tw, 32, [[{"text": nom, "bold": True},
                                      {"text": "  ·  " + sub, "color": MUTED}]],
           size=20, anchor="middle")
        lx += 28 + tw + 36
    bx, bw = ix + 270, 560
    y0, rh = 390, 72
    rect(s, bx - 2, y0 - 6, 2, 6 * rh - 4, fill=BLUE_LIGHT, fill_alpha=0.5)
    for k, (nom, sub, vb, sb, ve, se) in enumerate(RECALL):
        y = y0 + k * rh
        sel = k == 3
        if sel:
            rect(s, ix - 12, y - 4, iw + 24, rh - 4, fill=YELLOW, fill_alpha=0.10)
            rect(s, ix - 12, y - 4, 4, rh - 4, fill=YELLOW)
        _h(s, ix, y + 2, 260, 30, nom, size=22, color=YELLOW if sel else PAPER)
        _b(s, ix, y + 32, 260, 26, sub, size=18, color=MUTED)
        if vb is None:
            _b(s, bx + 10, y + 1, 60, 30, sb, size=20, color=MUTED, anchor="middle")
        else:
            bar(s, bx, y + 6, bw, 20, vb, color=LINE, track=None)
            _b(s, bx + bw * vb + 10, y + 1, 90, 30, sb, size=20, color=MUTED, anchor="middle")
        bar(s, bx, y + 32, bw, 20, ve, color=YELLOW if sel else BLUE_LIGHT, track=None)
        vx = bx + bw * ve + 10
        _h(s, vx, y + 27, 100, 30, se, size=21, color=YELLOW if sel else PAPER,
           anchor="middle")
        if sel:
            chip(s, vx + 100, y + 25, "test 0,8571", size=18, h=32, pad=10, mono=False)
    # lo que vale cada decisión
    dy = y0 + 6 * rh + 14
    _sep_h(s, ix, dy, iw)
    label(s, ix, dy + 18, iw, "Lo que vale cada decisión · puntos de Recall@1", color=MUTED)
    decis = [("Enriquecer el texto con los códigos", 32, "+32 puntos", YELLOW),
             ("Elegir el mejor analizador dentro de una columna", 5, "5 puntos", BLUE_LIGHT)]
    dbx, dbw = ix + 480, 340
    for k, (nom, v, vs, col) in enumerate(decis):
        yy = dy + 58 + k * 48
        _b(s, ix, yy, 470, 36, nom, size=21, anchor="middle")
        bar(s, dbx, yy + 7, dbw, 22, v / 32, color=col, track=None)
        _h(s, dbx + dbw * v / 32 + 14, yy, 180, 36, vs, size=26,
           color=YELLOW if k == 0 else PAPER, anchor="middle")
    notes(s, " ".join(notas[i] for i in (63, 69)))


# ======================================================================= P10
def _ecuacion_sigma(s, x, ay, size=36, w=None):
    """score = σ(logit) = 1 / (1 + e^−logit) con el mismo aire a ambos lados de cada «=».

    «σ» solo existe en Roboto Mono; «(logit)» va en Barlow pegado a la σ, para que
    el término no se vea en otra fuente ni desplace el segundo «=». Con `w`, la
    ecuación se centra en ese ancho.
    """
    gap = size * 0.4
    frac = ("frac", ["1"], ["1", "+", ("sup", "e", "−logit")])
    w_sig = text_width("σ", size, FONT_MONO)
    w_log = text_width("(logit)", size, FONT_TXT)
    trozos = [["score"], ["="], None, ["="], [frac]]
    anchos = [w_sig + 1 + w_log if t is None else medida_ecuacion(t, size)[0] for t in trozos]
    total = sum(anchos) + gap * (len(trozos) - 1) - size * 0.1
    cx = x + (w - total) / 2 if w else x
    for t, aw in zip(trozos, anchos):
        if t is None:                          # σ(logit)
            ecuacion(s, cx, ay, ["σ"], size=size)
            ecuacion(s, cx + w_sig + 1, ay, ["(logit)"], size=size)
        else:
            if t[0] is frac:                   # la barra arranca 0,1·size dentro de su caja
                cx -= size * 0.1
            ecuacion(s, cx, ay, t, size=size)
        cx += aw + gap


def p10(prs, notas):
    """Lámina 64: siete medidas de similitud con tres funciones distintas."""
    s = add_slide(prs, bg_image=FONDO)
    subencabezado(s, OE4 + " · Medidas de similitud",
                  "Siete medidas de similitud, tres funciones distintas")
    # nodo de origen
    nx, nw, ny, nh = 96, 184, 276, 566
    card(s, nx, ny, nw, nh, accent=YELLOW, fill=PANEL_2)
    _h(s, nx, ny + nh / 2 - 96, nw, 110, "7", size=104, color=YELLOW, align="center",
       anchor="middle", ls=1.0)
    _h(s, nx + 12, ny + nh / 2 + 22, nw - 24, 70, ["MEDIDAS DE", "SIMILITUD"], size=18,
       color=PAPER, align="center", ls=1.3)
    carriles = [
        ("Decide", YELLOW, DARK, "1", 236),
        ("Contrasta", BLUE_LIGHT, PAPER, "1", 128),
        ("Explica", LINE, DARK, "5", 166),
    ]
    lx0, lx1 = 324, 1824
    xo = 1300                                    # columna de salida
    cc = lx0 + 300                               # columna de medidas
    y = 276
    gap = 18
    for k, (fn, col, tcol, n, h) in enumerate(carriles):
        card(s, lx0, y, lx1 - lx0, h, accent=col, accent_side="left",
             brackets=(k == 0))
        cy = y + h / 2
        flecha(s, nx + nw + 6, cy, lx0 - 8, color=col, h=24)
        _h(s, lx0 + 22, cy - 50, 76, 100, n, size=80, color=YELLOW if k == 0 else
           (BLUE_TEXT if k == 1 else PAPER), align="center", anchor="middle", ls=1.0)
        tag(s, lx0 + 104, cy - 18, fn, fill=col, color=tcol, size=18, h=36)
        _sep_v(s, cc - 28, y + 22, h - 44)
        _sep_v(s, xo - 32, y + 22, h - 44)
        flecha(s, xo - 76, cy, xo - 44, color=col, h=20)
        ow = lx1 - xo - 32
        if k == 0:
            chip(s, cc, y + 26, "coseno sobre TF-IDF", size=22, h=42, pad=14)
            partes = ["cos(A, B)", " = ", ("frac", ["A · B"], ["||A|| ||B||"])]
            ecuacion(s, cc, y + 152, partes, size=40)
            _h(s, xo, y + 46, ow, 80, "El ranking top-10 y el corte por umbral", size=28)
            _b(s, xo, y + 138, ow, 40, "Solo una medida decide.", size=22, color=YELLOW,
               bold=True)
        elif k == 1:
            chip(s, cc, cy - 21, "BM25 Okapi", size=22, h=42, pad=14, color=PAPER)
            _h(s, xo, y + 18, ow, h - 36, "Segundo ranking independiente de control",
               size=26, anchor="middle")
        else:
            medidas = ["Jaccard", "Levenshtein", "fuzzy ratio", "token_sort", "token_set",
                       "BoW overlap", "BoW Dice"]
            cx, cy2 = cc, y + 32
            for m in medidas:
                wch = _chip_w(m, 19, pad=10)
                if cx + wch > xo - 92:
                    cx, cy2 = cc, cy2 + 52
                chip(s, cx, cy2, m, size=19, h=40, pad=10, color=PAPER)
                cx += wch + 10
            _h(s, xo, y + 28, ow, 70, "Auditoría por par y features candidatas", size=26)
            tag(s, xo, y + h - 64, "Nunca deciden solas", fill=RED, color=PAPER, size=18,
                h=36)
        y += h + gap
    # el score del cross-encoder
    by = y + 4
    bh = 1010 - by
    card(s, 96, by, 1728, bh, accent=BLUE_LIGHT, accent_side="left", fill=PANEL_2)
    tag(s, 128, by + 26, "Cross-encoder", fill=YELLOW, color=DARK, size=18, h=36)
    _h(s, 128, by + 74, 560, 40, "Su score no es una similitud simétrica", size=24)
    x_h = 128 + text_width("Su score no es una similitud simétrica", 24, FONT_HEAD, True)
    _ecuacion_sigma(s, x_h + 32, by + bh / 2, size=36, w=1320 - 32 - (x_h + 32))
    _b(s, 1320, by + 20, 476, bh - 40, "Una probabilidad no calibrada de que el par sea "
       "correspondencia.", size=22, color=MUTED, anchor="middle")
    notes(s, notas[64])


# ======================================================================= P11
ESCALERA = [
    ("0", "El enrutador de estados indica publicación ocultada", "Hidden", 188, "188"),
    ("1", "El código de la consulta no existe en el catálogo del país", "NIC", 890, "890"),
    ("2", "El enrutador de estados indica ausencia de catálogo", "NIC", 83, "83"),
    ("3", "Regla exacta de código y el título no es multipack", "Match", 113, "113"),
    ("4", "TF-IDF recupera · el cross-encoder puntúa · compuerta de score, margen y código",
     "Match", 8, "8"),
    ("5", "Todo lo demás: llega al revisor con los candidatos ya ordenados", "Review", 1083,
     "1.083"),
]
DECISION = {"Hidden": (LINE, DARK), "NIC": (BLUE_LIGHT, PAPER), "Match": (YELLOW, DARK),
            "Review": (None, PAPER)}      # Review: abstención, en contorno (no decide)


def _tag_contorno(s, x, y, txt, color=PAPER, size=18, h=34):
    """Etiqueta sin relleno, solo contorno: la abstención no es una decisión."""
    w = _tag_w(txt, size)
    rect(s, x, y, w, h, fill=CHIP, line=color, line_w=1.5, radius=4)
    text(s, x, y, w, h, txt.upper(), size=size, bold=True, font=FONT_HEAD, color=color,
         align="center", anchor="middle", spacing=1.2, wrap=False)
    return w


def p11(prs, notas):
    """Láminas 65 + 66: la cascada (capa 4) dentro de la escalera de decisión."""
    s = add_slide(prs, bg_image=FONDO)
    subencabezado(s, OE4 + " · Arquitectura",
                  "La cascada dentro de la escalera de decisión")
    # --- izquierda: escalera -----------------------------------------------
    x, w = 96, 1024
    label(s, x, 276, w, "Escalera de decisión · medida sobre 2.365 publicaciones",
          color=YELLOW)
    y0, rh, gap = 314, 82, 10
    bx, bw = x + 744, 136
    for k, (n, cond, dec, v, vs) in enumerate(ESCALERA):
        y = y0 + k * (rh + gap)
        modelo = k == 4
        rect(s, x, y, w, rh, fill=CHIP if modelo else PANEL_2,
             line=YELLOW if modelo else BLUE_LIGHT, line_w=2 if modelo else 1.2,
             line_alpha=1 if modelo else 0.35)
        if k == 5:                               # abstención: insignia en contorno
            rect(s, x + 18, y + (rh - 44) / 2, 44, 44, fill=CHIP, line=PAPER, line_w=1.5,
                 radius=4)
            _h(s, x + 18, y + (rh - 44) / 2, 44, 44, n, size=20, color=PAPER, align="center",
               anchor="middle", ls=1.0)
        else:
            bfill = YELLOW if modelo else BLUE_LIGHT
            numbadge(s, x + 18, y + (rh - 44) / 2, n, size=44, fill=bfill,
                     color=DARK if modelo else PAPER)
        _b(s, x + 80, y + 4, 516, rh - 8, cond, size=21, anchor="middle",
           color=PAPER if k != 5 else MUTED)
        fill, tcol = DECISION[dec]
        ty = y + (rh - 34) / 2
        if fill is None:
            _tag_contorno(s, x + 608, ty, dec)
            rect(s, bx, y + rh / 2 - 10, bw, 20, fill=CHIP)
            rect(s, bx, y + rh / 2 - 10, bw * v / 1083, 20, fill=PAPER, fill_alpha=0.15,
                 line=PAPER, line_w=1.5)
        else:
            tag(s, x + 608, ty, dec, fill=fill, color=tcol, size=18, h=34)
            bar(s, bx, y + rh / 2 - 10, bw, 20, v / 1083, color=fill)
        _h(s, bx + bw + 8, y, w - (bx - x) - bw - 26, rh, vs, size=30,
           color=YELLOW if dec == "Match" else PAPER, align="right", anchor="middle")
    yb = y0 + 6 * (rh + gap) - gap
    # --- derecha: zoom de la capa 4, la cascada --------------------------
    cx0, cw = 1200, 624
    cy0, chh = 276, yb - 276
    y4 = y0 + 4 * (rh + gap)
    line(s, x + w + 4, y4, cx0, cy0 + 1, color=YELLOW, width=1.5, alpha=0.7, dash="dash")
    line(s, x + w + 4, y4 + rh, cx0, cy0 + chh - 1, color=YELLOW, width=1.5, alpha=0.7,
         dash="dash")
    card(s, cx0, cy0, cw, chh, accent=None, brackets=True)
    label(s, cx0 + 28, cy0 + 20, cw - 56, "Capa 4 · la cascada", color=YELLOW)
    etapas = [
        ("Catálogo del país", "4.316", ["productos oficiales por consulta"], 540, BLUE_LIGHT),
        ("Recuperación TF-IDF", "top 20", ["candidatos con la verdad dentro",
                                           "el 91,84% de las veces — el techo del pool"],
         470, BLUE_LIGHT),
        ("Validación cruzada", "1 decisión", ["exige margen y soporte de código"], 400, YELLOW),
    ]
    flechas = [("Modelo 1", "recuperar barato"), ("Modelo 3", "validar caro")]
    ey, ag = cy0 + 58, 30
    mid = cx0 + cw / 2
    for k, (tit, cifra, sub, ew, col) in enumerate(etapas):
        ex = mid - ew / 2
        eh = 76 + 24 * len(sub)
        rect(s, ex, ey, ew, eh, fill=PANEL_2, line=col, line_w=1.5,
             line_alpha=1 if col == YELLOW else 0.5, radius=6)
        _h(s, ex, ey + 8, ew, 26, tit, size=20, color=PAPER, align="center")
        _h(s, ex, ey + 32, ew, 44, cifra, size=40, color=YELLOW, align="center",
           anchor="middle", ls=1.0)
        _b(s, ex + 16, ey + 74, ew - 32, 24 * len(sub), sub, size=19, color=MUTED,
           align="center", ls=1.25)
        ey += eh
        if k < 2:
            flecha_abajo(s, mid, ey + 2, ey + ag - 2, w=20)
            m, d = flechas[k]
            _h(s, mid + 24, ey + 2, 130, ag - 4, m, size=18, color=YELLOW, anchor="middle")
            _b(s, mid - 24 - 200, ey + 2, 200, ag - 4, d, size=19, color=MUTED,
               align="right", anchor="middle")
            ey += ag
    # por qué hace falta la cascada (mensaje central de la lámina 65)
    _sep_h(s, cx0 + 28, ey + 16, cw - 56, alpha=0.4)
    _b(s, cx0 + 28, ey + 28, cw - 56, cy0 + chh - ey - 40,
       [[{"text": "Ninguno de los dos puede hacer el trabajo del otro:", "bold": True,
          "color": PAPER},
         {"text": " el recuperador no distingue variantes casi homónimas y el validador es "
                  "demasiado caro para recorrer 4.316 productos por consulta."}]],
       size=20, color=MUTED, ls=1.25)
    # --- franja inferior: reglas y abstención -----------------------------
    fy = yb + 24
    fh = 1010 - fy
    card(s, 96, fy, 1728, fh, accent=YELLOW, accent_side="left", fill=PANEL_2)
    vw = text_width("99,4%", 64, FONT_HEAD, True) + 10
    _h(s, 128, fy, vw, fh, "99,4%", size=64, color=YELLOW, anchor="middle", ls=1.0)
    _b(s, 128 + vw + 20, fy + 10, 760 - vw, fh - 20,
       [[{"text": "1.274 de las 1.282", "bold": True, "color": PAPER},
         {"text": " decisiones automáticas salen de las capas 0–3: reglas deterministas, "
                  "sin GPU."}]], size=22, color=MUTED, anchor="middle")
    _sep_v(s, 940, fy + 20, fh - 40, alpha=0.4)
    _h(s, 972, fy + 20, 330, 36, "No Match automático", size=24)
    tag(s, 972 + text_width("No Match automático", 24, FONT_HEAD, True) + 18, fy + 20,
        "Deshabilitado", fill=RED, color=PAPER, size=18, h=34)
    _b(s, 972, fy + 62, 820, fh - 72, "El sistema nunca afirma la ausencia de "
       "correspondencia sin verdad que la respalde.", size=21, color=MUTED)
    notes(s, " ".join(notas[i] for i in (65, 66)))


def construir(prs, notas):
    p08(prs, notas)
    p09(prs, notas)
    p10(prs, notas)
    p11(prs, notas)
