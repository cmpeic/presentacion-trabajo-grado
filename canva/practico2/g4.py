"""Grupo g4: OE4 · el recuperador y la duda del modelo; OE5 · Recall@1 en test (P12-P14)."""

from pptx_kit import add_slide, corners, notes, rect, text
from theme import FONDO, LINE, MUTED, PAPER, YELLOW
from componentes import (BLUE_LIGHT, CHIP, DARK, FONT_HEAD, FONT_MONO, FONT_TXT, PANEL_2, RED,
                         bar, card, chip, ecuacion, flecha, label, medida_ecuacion, numbadge,
                         subencabezado, tag, text_width, wrap_lines)

OE4 = "OE4 · Diseñar los modelos"
OE5 = "OE5 · Evaluar el desempeño"


# ----------------------------------------------------------------- utilidades
def _tag_w(s, size=16, pad=14):
    """Ancho que ocupará `tag(...)` con el mismo texto y tamaño."""
    return text_width(s.upper(), size, FONT_HEAD, True, spacing=1.2) + 2 * pad + 6


def _flechita(s, x, cy, size, color):
    """Flecha pequeña dibujada como forma (sustituye al glifo «→»). Devuelve su ancho."""
    aw, ah = size * 1.1, size * 0.66
    flecha(s, x, cy, x + aw, color=color, h=ah)
    return aw


def _seg(s, x, y, partes, h=30, gap=8):
    """Línea mixta medida: cada tramo en su propio cuadro (una familia por cuadro).

    `partes`: lista de (texto, fuente, tamaño, color, negrita). Un tramo «→» con
    fuente None se dibuja como flecha (forma). Devuelve la x final.
    """
    cx = x
    for txt, font, size, color, bold in partes:
        if font is None:
            cx += _flechita(s, cx, y + h / 2, size, color) + gap
            continue
        w = text_width(txt, size, font, bold)
        text(s, cx, y, w + 30, h, txt, size=size, font=font, color=color, bold=bold,
             anchor="middle", line_spacing=1.0)
        cx += w + gap
    return cx


def _equilibrar(txt, size, width, font=FONT_TXT):
    """Parte `txt` en el mínimo de líneas que caben en `width`, con líneas parejas."""
    mejor = wrap_lines(txt, size, width, font)
    w = width
    while w > 120:
        w -= 4
        cand = wrap_lines(txt, size, w, font)
        if len(cand) > len(mejor):
            break
        mejor = cand
    return mejor


def _runs(s, x, y, w, h, tramos, size, font, anchor="middle", align="left", bold=False):
    """Cuadro de una sola familia con tramos de colores: [(texto, color), ...]."""
    text(s, x, y, w, h, [[{"text": t, "color": c} for t, c in tramos]], size=size, font=font,
         bold=bold, anchor=anchor, align=align, line_spacing=1.0)


def _titulo_col(s, x, y, n, titulo, w, color=YELLOW):
    """Número de paso + título de columna."""
    numbadge(s, x, y, n, size=40, fill=color)
    text(s, x + 56, y, w - 56, 40, titulo, size=26, bold=True, font=FONT_HEAD,
         anchor="middle")


# ------------------------------------------------------------------- P12
CASOS = [
    {
        "n": "1", "titulo": "El código cruza el idioma", "estado": ("Lo resuelve", YELLOW, DARK),
        "sub": "Consulta en cirílico, candidatos en inglés",
        "consulta": [("монітор philips 27\" ", PAPER), ("27e2n1100l/00", YELLOW),
                     (" black/va/100 гц", PAPER)],
        "filas": [
            ([("27E2N1100L/00", YELLOW)],
             [("philips monitor ", MUTED), ("27e2n1100l", YELLOW), (" full hd lcd monitor", MUTED)],
             0.691793, "0,691793", "ok"),
            ([("27E2N1110/00", PAPER)], [("philips monitor 27e2n1110 full hd lcd monitor", MUTED)],
             0.344748, "0,344748", None),
            ([("27E2N1500L/00", PAPER)], [("philips monitor 27e2n1500l quad hd monitor", MUTED)],
             0.316991, "0,316991", None),
        ],
        "cifra": ("×2", YELLOW, "frente al 2.º"),
        "mensaje": "El correcto queda primero con el doble de puntuación: el código es la "
                   "parte que ambos textos comparten.",
    },
    {
        "n": "2", "titulo": "Solo cambia el sufijo",
        "estado": ("No puede cerrar solo", RED, PAPER),
        "sub": "Misma clase de consulta: los dos primeros son el mismo texto",
        "consulta": [("монітор philips ", PAPER), ("27m2c5500w/00", YELLOW)],
        "filas": [
            ([("27M2C5500W/", PAPER), ("00", YELLOW)],
             [("philips curved gaming monitor 27m2c5500w quad hd", PAPER)],
             0.668532, "0,668532", "ok"),
            ([("27M2C5500W/", PAPER), ("01", RED)],
             [("philips curved gaming monitor 27m2c5500w quad hd", PAPER)],
             0.614145, "0,614145", "rival"),
            ([("32M2C5500W/00", PAPER)], [("philips gaming monitor 32m2c5500w quad hd", MUTED)],
             0.456400, "0,456400", None),
        ],
        "cifra": ("0,054387", RED, "de separación"),
        # cortes a mano: «/00 de /01» no debe quedar partido entre líneas
        "mensaje": ["Una bolsa de n-gramas no separa /00 de /01:",
                    "hace falta un segundo modelo que lea", "los dos textos juntos."],
    },
]


def _esquema_recuperador(s, y, h=70):
    """Franja superior: consulta → recuperador → catálogo → candidatos."""
    pasos = [("Consulta", "publicación de retailer", False),
             ("Recuperador", "TF-IDF char_wb 4-6 · texto enriquecido", True),
             ("Catálogo", "4.316 productos", False),
             ("Devuelve", "candidatos ordenados por score", False)]
    ag = 64                                    # hueco para cada flecha
    anchos = [text_width(v, 22, FONT_TXT, d) + 48 for _, v, d in pasos]
    extra = (1728 - 3 * ag - sum(anchos)) / 4
    x = 96
    for k, (lab, val, dest) in enumerate(pasos):
        bw = anchos[k] + extra
        rect(s, x, y, bw, h, fill=PANEL_2 if not dest else CHIP, line=YELLOW if dest else BLUE_LIGHT,
             line_w=2 if dest else 1.5, line_alpha=1 if dest else 0.4)
        label(s, x + 22, y + 8, bw - 40, lab, size=18, color=YELLOW if dest else MUTED)
        text(s, x + 22, y + 34, bw - 30, 30, val, size=22, font=FONT_TXT,
             color=PAPER, bold=dest, anchor="middle", line_spacing=1.0)
        if k < 3:
            flecha(s, x + bw + 12, y + h / 2, x + bw + ag - 12, h=26)
        x += bw + ag


def _caso(s, x, y, w, h, c):
    card(s, x, y, w, h, accent=c["estado"][1])
    pad = 28
    # encabezado: número + título + estado, y debajo el subtítulo del caso
    numbadge(s, x + pad, y + 22, c["n"], size=40, fill=c["estado"][1], color=c["estado"][2])
    text(s, x + pad + 56, y + 22, w - 2 * pad - 56, 40, c["titulo"], size=28, bold=True,
         font=FONT_HEAD, anchor="middle")
    est = c["estado"][0]
    tag(s, x + w - pad - _tag_w(est, 18), y + 24, est, fill=c["estado"][1],
        color=c["estado"][2], size=18, h=36)
    text(s, x + pad + 56, y + 64, w - 2 * pad - 56, 28, c["sub"], size=20, font=FONT_TXT,
         color=MUTED, anchor="middle")
    # consulta
    qy, qh = y + 104, 80
    rect(s, x + pad, qy, w - 2 * pad, qh, fill=CHIP, line=BLUE_LIGHT, line_w=1, line_alpha=0.35)
    rect(s, x + pad, qy, 5, qh, fill=BLUE_LIGHT)
    label(s, x + pad + 22, qy + 8, w - 2 * pad - 40, "Consulta · Ucrania",
          size=18, color=MUTED)
    _runs(s, x + pad + 22, qy + 37, w - 2 * pad - 30, 34, c["consulta"], 24, FONT_MONO)
    # candidatos
    cx0 = x + pad + 56
    cw = w - 2 * pad - 56
    vmax = 0.70
    r0, rp = y + 206, 100
    for k, (cod, desc, v, vs, rol) in enumerate(c["filas"]):
        ry = r0 + k * rp
        color = YELLOW if rol == "ok" else RED if rol == "rival" else BLUE_LIGHT
        numbadge(s, x + pad, ry - 1, str(k + 1), size=40,
                 fill=YELLOW if rol == "ok" else CHIP,
                 color=DARK if rol == "ok" else PAPER)
        _runs(s, cx0, ry, cw - 170, 36, cod, 26, FONT_MONO)
        text(s, cx0 + cw - 170, ry, 170, 36, vs, size=28, bold=True, font=FONT_HEAD,
             color=YELLOW if rol == "ok" else PAPER, align="right", anchor="middle")
        _runs(s, cx0, ry + 39, cw - 150, 28, desc, 20, FONT_TXT)
        if rol:
            t = "correcto" if rol == "ok" else "mismo texto"
            tag(s, cx0 + cw - _tag_w(t, 18, 10), ry + 38, t, fill=color,
                color=DARK if rol == "ok" else PAPER, size=18, pad=10, h=30)
        bar(s, cx0, ry + 74, cw, 14, v / vmax, color=color)
    # veredicto: cifra y rótulo alineados a la izquierda; mensaje en líneas parejas
    vy = r0 + 2 * rp + 88 + 14
    vh = y + h - 20 - vy
    rect(s, x + pad, vy, w - 2 * pad, vh, fill=PANEL_2, line=c["cifra"][1], line_w=1.5,
         line_alpha=0.6)
    cifra, ccol, csub = c["cifra"]
    fw = max(text_width(cifra, 48, FONT_HEAD, True), text_width(csub.upper(), 18, FONT_HEAD, True,
                                                                spacing=1.5)) + 8
    fx = x + pad + 24
    by_ = vy + (vh - 84) / 2
    text(s, fx, by_, fw + 24, 56, cifra, size=48, bold=True, font=FONT_HEAD, color=ccol,
         anchor="middle", align="left", line_spacing=1.0)
    label(s, fx, by_ + 56, fw + 24, csub, size=18, color=PAPER)
    tx = fx + fw + 28
    rect(s, tx - 14, vy + 18, 1.5, vh - 36, fill=BLUE_LIGHT, fill_alpha=0.4)
    mw = x + w - pad - tx - 24
    msj = c["mensaje"]
    if isinstance(msj, list):
        assert all(text_width(ln, 22, FONT_TXT) <= mw - 8 for ln in msj), msj
        lineas = msj
    else:
        lineas = _equilibrar(msj, 22, mw - 8)
    text(s, tx + 6, vy, mw, vh, lineas, size=22, font=FONT_TXT, color=PAPER, anchor="middle",
         line_spacing=1.25)


def p12(prs, notas):
    """Láminas 67 + 68: el recuperador TF-IDF en un caso que resuelve y otro que no."""
    s = add_slide(prs, bg_image=FONDO)
    subencabezado(s, OE4 + " · Recuperador TF-IDF", "El recuperador en dos casos reales")
    _esquema_recuperador(s, 278)
    py, gap = 374, 24
    pw = (1728 - gap) / 2
    for k, c in enumerate(CASOS):
        _caso(s, 96 + k * (pw + gap), py, pw, 1010 - py, c)
    corners(s, 86, py - 10, 1748, 1010 - py + 20, size=34, width=3)
    notes(s, " ".join(notas[i] for i in (67, 68)))


# ------------------------------------------------------------------- P13
MARGENES = [("SCF091/46", "SCF227/22", "0,99931", 0.0, "0,0000000"),
            ("27M2N3200S/00", "27M2N3200A/00", "0,99973", 0.0000021, "0,0000021"),
            ("25M2N3200U/00", "25M2N3200W/00", "0,99970", 0.0000070, "0,0000070"),
            ("SCF080/24", "SCF080/08", "0,99812", 0.0000074, "0,0000074")]
UMBRAL_MARGEN = 0.00015

# fragmentos del título real: la «…» inicial indica que el título sigue por delante
FALSOS = [("Conflicto de sufijo", "0,9990564", "… 221v8/00 fhd va 75hz 221v8/00/01",
           "dos códigos en un mismo título"),
          ("Sufijo distinto", "0,9989917", "… 4000 series 24b2n4200/00/rh",
           "sufijo /RH = otra referencia"),
          ("Reacondicionado", "0,9989718", "… täydellinen hoito kompakti gc7844/20",
           "el original y el R1 comparten texto"),
          ("Sufijo distinto", "0,9990379", "… 85pus8510 … barra de sonido tab4000",
           "televisor + barra de sonido en un paquete")]


def _col_par(s, x, y, w, h):
    """Columna 1: un mismo par medido por las funciones de similitud."""
    card(s, x, y, w, h, accent=BLUE_LIGHT)
    pad = 24
    iw = w - 2 * pad
    _titulo_col(s, x + pad, y + 24, "1", "El score se dispara", iw, color=BLUE_LIGHT)
    yy = y + 88
    for lab, txt, col in (("Retailer · ucraniano",
                           "пустушка avent ultra soft 6-18 міс. дизайн для дівчат 2 шт.", PAPER),
                          ("Catálogo · español",
                           "philips chupete ultrasuave y flexible 6-18 meses ultra soft-fopspeen",
                           YELLOW)):
        label(s, x + pad, yy, iw, lab, size=18, color=MUTED)
        lineas = wrap_lines(txt, 20, iw - 8, FONT_MONO)
        text(s, x + pad, yy + 30, iw, 26 * len(lineas), lineas, size=20, font=FONT_MONO,
             color=col, line_spacing=1.25)
        yy += 30 + 26 * len(lineas) + 12
    # referencia elegida frente a la correcta (mismo código de color que la columna 2:
    # amarillo = correcto, rojo = elegido por error)
    x2_ = x + pad + 190
    label(s, x + pad, yy, 180, "Elegido", size=18, color=MUTED)
    label(s, x2_, yy, iw - 190, "El correcto era", size=18, color=MUTED)
    chip(s, x + pad, yy + 28, "SCF227/22", size=20, h=34, color=RED)
    chip(s, x2_, yy + 28, "SCF091/18", size=20, h=34, color=YELLOW)
    # barras de similitud (escala 0-1)
    by = yy + 28 + 34 + 22
    bp = 54
    medidas = [("TF-IDF coseno", "0,1643", 0.1643, BLUE_LIGHT),
               ("Jaccard", "0,0870", 0.0870, BLUE_LIGHT),
               ("Embeddings", "0,4899", 0.4899, BLUE_LIGHT),
               ("Cross-encoder", "0,99927", 0.99927, RED)]
    for k, (nom, vs, v, col) in enumerate(medidas):
        ry = by + k * bp
        label(s, x + pad, ry, iw - 120, nom, size=18, color=PAPER if col == RED else MUTED)
        text(s, x + pad + iw - 140, ry - 6, 140, 34, vs, size=26, bold=True, font=FONT_HEAD,
             color=RED if col == RED else PAPER, align="right", anchor="middle")
        bar(s, x + pad, ry + 30, iw, 12, v, color=col)
    ty = by + 3 * bp + 42 + 18
    # líneas medidas: «cross-encoder» no se parte en el guion
    lineas = wrap_lines("Ningún token compartido, pero el cross-encoder se dispara: acierta el "
                        "concepto y falla el modelo exacto.", 22, iw - 10, FONT_TXT)
    text(s, x + pad, ty, iw, y + h - 20 - ty, lineas, size=22, font=FONT_TXT, color=PAPER,
         line_spacing=1.25)


def _col_margen(s, x, y, w, h):
    """Columna 2 (foco): el margen entre el 1.º y el 2.º frente al umbral exigido."""
    card(s, x, y, w, h, accent=YELLOW, brackets=True)
    pad = 28
    iw = w - 2 * pad
    _titulo_col(s, x + pad, y + 24, "2", "El margen delata la duda", iw)
    # ecuación del margen
    ey, eh = y + 88, 92
    rect(s, x + pad, ey, iw, eh, fill=CHIP, line=BLUE_LIGHT, line_w=1, line_alpha=0.35)
    eq = [("var", "margen"), "=", ("sub", "s", "1"), " −", ("sub", "s", "2")]
    ew, _, _ = medida_ecuacion(eq, size=38)
    ecuacion(s, x + pad + 28, ey + eh / 2 - 2, eq, size=38)
    text(s, x + pad + 28 + ew + 36, ey, iw - ew - 92, eh,
         "score del 1.º menos score del 2.º candidato", size=20, font=FONT_TXT, color=MUTED,
         anchor="middle", line_spacing=1.2)
    label(s, x + pad, ey + eh + 20, iw, "Los cuatro errores de ranking más graves", size=18,
          color=MUTED)
    # filas: cuatro errores
    vw = 168
    bw = iw - vw - 16
    ry0 = ey + eh + 62
    pitch = 80
    for k, (ok, elig, sc, m, ms) in enumerate(MARGENES):
        ry = ry0 + k * pitch
        _seg(s, x + pad, ry, [(ok, FONT_MONO, 20, YELLOW, False),
                              ("eligió", FONT_TXT, 20, MUTED, False),
                              (elig, FONT_MONO, 20, RED, False)], h=28)
        text(s, x + pad + iw - 190, ry, 190, 28, "score " + sc, size=20, font=FONT_TXT,
             color=MUTED, align="right", anchor="middle")
        bar(s, x + pad, ry + 38, bw, 18, m / UMBRAL_MARGEN, color=RED)
        if m == 0:
            rect(s, x + pad, ry + 35, 3, 24, fill=RED)
        text(s, x + pad + bw + 16, ry + 28, vw, 38, ms, size=26, bold=True, font=FONT_HEAD,
             color=RED, align="right", anchor="middle")
    # umbral exigido
    uy = ry0 + 4 * pitch + 8
    rect(s, x + pad, uy - 16, iw, 1.5, fill=BLUE_LIGHT, fill_alpha=0.4)
    text(s, x + pad, uy, bw, 28, "Umbral: margen mínimo para decidir sin humano", size=20,
         font=FONT_TXT, bold=True, color=YELLOW, anchor="middle")
    bar(s, x + pad, uy + 38, bw, 18, 1.0, color=YELLOW)
    text(s, x + pad + bw + 16, uy + 28, vw, 38, "0,0001500", size=26, bold=True,
         font=FONT_HEAD, color=YELLOW, align="right", anchor="middle")
    # conclusión
    cy = uy + 84
    tw_ = tag(s, x + pad, cy + 6, "A revisión", fill=YELLOW, color=DARK, size=18, h=36)
    text(s, x + pad + tw_ + 18, cy - 4, iw - tw_ - 18, y + h - 16 - cy + 4,
         "El score no avisa —todos pasan de 0,998—, el margen sí: la compuerta exige score y "
         "margen.", size=22, font=FONT_TXT, color=PAPER, line_spacing=1.25)


def _col_falsos(s, x, y, w, h):
    """Columna 3: los cuatro falsos positivos que cruzan el umbral del cross-encoder."""
    card(s, x, y, w, h, accent=RED)
    pad = 24
    iw = w - 2 * pad
    _titulo_col(s, x + pad, y + 24, "3", "Lo que sobrevive", iw, color=RED)
    # cifra
    ky = y + 84
    _runs(s, x + pad, ky, iw, 64, [("4", RED), (" de 113", PAPER)], 54, FONT_HEAD, bold=True)
    text(s, x + pad, ky + 66, iw, 28, "negativos del test cruzan el umbral 0,998844", size=20,
         font=FONT_TXT, color=MUTED, anchor="middle")
    # cuatro casos
    iy0 = ky + 112
    pitch = 116
    for k, (tipo, sc, frag, causa) in enumerate(FALSOS):
        iy = iy0 + k * pitch
        rect(s, x + pad, iy - 10, iw, 1.5, fill=BLUE_LIGHT, fill_alpha=0.3)
        tag(s, x + pad, iy + 2, tipo, fill=CHIP, color=PAPER, size=18, pad=10, h=32)
        text(s, x + pad + iw - 140, iy + 2, 140, 32, sc, size=20, bold=True, font=FONT_HEAD,
             color=RED, align="right", anchor="middle")
        text(s, x + pad, iy + 40, iw + 10, 28, frag, size=19, font=FONT_MONO, color=YELLOW,
             anchor="middle")
        text(s, x + pad, iy + 70, iw, 28, causa, size=21, font=FONT_TXT, color=PAPER,
             anchor="middle")
    ty = iy0 + 4 * pitch - 6
    rect(s, x + pad, ty - 4, iw, 1.5, fill=BLUE_LIGHT, fill_alpha=0.3)
    text(s, x + pad, ty + 6, iw, y + h - 14 - ty - 6,
         "En los cuatro, el texto sí describe el producto: difiere la referencia comercial exacta.",
         size=21, font=FONT_TXT, color=PAPER, line_spacing=1.25)


def p13(prs, notas):
    """Láminas 70 + 71 + 72: score engañoso, margen como señal de duda y falsos positivos."""
    s = add_slide(prs, bg_image=FONDO)
    subencabezado(s, OE4 + " · Cross-encoder",
                  "Dónde duda el modelo: el margen y los falsos positivos")
    y, h = 282, 1010 - 282
    w1, w2, w3, g = 480, 680, 480, 44
    x1, x2, x3 = 96, 96 + w1 + g, 96 + w1 + w2 + 2 * g
    _col_par(s, x1, y, w1, h)
    _col_margen(s, x2, y, w2, h)
    _col_falsos(s, x3, y, w3, h)
    # sin flechas entre columnas: son tres casos distintos del test, no una secuencia
    # (la columna 1 y la primera fila de la columna 2 son consultas diferentes)
    notes(s, " ".join(notas[i] for i in (70, 71, 72)))


# ------------------------------------------------------------------- P14
RECALL = [
    # nombre (tramos), detalle, valor, texto, color
    ([("Cascada exacto", FONT_HEAD, 22, PAPER, True), ("→", None, 22, PAPER, None),
      ("transformer", FONT_HEAD, 22, PAPER, True)], "128 de 147 · MRR 0,8783",
     0.8707, "87,07%", YELLOW),
    ([("Cascada exacto", FONT_HEAD, 22, PAPER, True), ("→", None, 22, PAPER, None),
      ("TF-IDF", FONT_HEAD, 22, PAPER, True)], "127 de 147", 0.8639, "86,39%",
     BLUE_LIGHT),
    ([("TF-IDF", FONT_HEAD, 22, PAPER, True), ("char_4_6_enriched", FONT_MONO, 21, YELLOW, False)],
     "Recall@10 91,16% · el mejor recuperador", 0.8571, "85,71%", BLUE_LIGHT),
    ([("Baseline de coincidencia exacta", FONT_HEAD, 22, PAPER, True)], "solo reglas de código",
     0.8503, "85,03%", BLUE_LIGHT),
    ([("Transformer solo", FONT_HEAD, 22, PAPER, True)], "sin recuperador previo", 0.8231,
     "82,31%", BLUE_LIGHT),
    ([("Embeddings congelados", FONT_HEAD, 22, PAPER, True)], "13 de 147 · MRR 0,1352", 0.0884,
     "8,84%", RED),
]
TECHO = 0.9184


def _panel_mejor(s, x, y, w, h):
    card(s, x, y, w, h, accent=YELLOW, brackets=True)
    pad = 32
    iw = w - 2 * pad
    label(s, x + pad, y + 28, iw, "Mejor resultado observado", size=18, color=YELLOW)
    text(s, x + pad, y + 60, iw, 100, "87,07%", size=80, bold=True, font=FONT_HEAD, color=YELLOW,
         anchor="middle", line_spacing=1.0)
    # mini esquema de la cascada
    cy = y + 178
    label(s, x + pad, cy + 8, 140, "Cascada", size=18, color=MUTED)
    cx = x + pad + 120
    cw1 = chip(s, cx, cy, "exacto", size=22, mono=False, color=PAPER, h=40, pad=16)
    flecha(s, cx + cw1 + 10, cy + 20, cx + cw1 + 52, h=22)
    chip(s, cx + cw1 + 62, cy, "transformer", size=22, mono=False, color=YELLOW, h=40, pad=16,
         border=YELLOW)
    text(s, x + pad, cy + 52, iw, 30, "128 de 147 consultas · MRR 0,8783", size=22,
         font=FONT_TXT, color=MUTED, anchor="middle")
    # ecuación
    ey = cy + 116
    rect(s, x + pad, ey, iw, 1.5, fill=BLUE_LIGHT, fill_alpha=0.4)
    eq1 = [("var", "Recall@1"), "=", ("frac", ["aciertos en 1.ª posición"], ["consultas de test"])]
    ew1, up1, dn1 = medida_ecuacion(eq1, size=30)
    a1 = ey + 30 + up1
    ecuacion(s, x + pad, a1, eq1, size=30)
    lead, _, _ = medida_ecuacion([("var", "Recall@1")], size=30)
    eq2 = ["=", ("frac", ["128"], ["147"]), "=", ("res", "87,07%")]
    _, up2, dn2 = medida_ecuacion(eq2, size=30)
    a2 = a1 + dn1 + up2 + 20
    ecuacion(s, x + pad + lead + 30 * 0.18, a2, eq2, size=30)
    # contraste con la segunda cascada
    my = a2 + dn2 + 32
    rect(s, x + pad, my, iw, 1.5, fill=BLUE_LIGHT, fill_alpha=0.4)
    l1 = "Frente a exacto"
    # el espaciado de letras del rótulo se exporta en pt (1,5 pt = 2 px): se mide con 2 px
    w1 = text_width(l1.upper(), 18, FONT_HEAD, True, spacing=2.0)
    label(s, x + pad, my + 20, w1 + 20, l1, size=18, color=MUTED)
    aw = _flechita(s, x + pad + w1 + 12, my + 20 + 12, 18, MUTED)
    label(s, x + pad + w1 + aw + 24, my + 20, 120, "TF-IDF", size=18, color=MUTED)
    text(s, x + pad, my + 52, iw, 34, "Difieren en 3 consultas", size=26, bold=True,
         font=FONT_HEAD, color=PAPER, anchor="middle")
    eq3 = [("var", "p"), "=", ("res", "1,0")]
    e3w, _, _ = medida_ecuacion(eq3, size=32)
    ecuacion(s, x + pad, my + 116, eq3, size=32)
    text(s, x + pad + e3w + 18, my + 100, iw - e3w - 18, 34, "McNemar exacto", size=22,
         font=FONT_TXT, color=MUTED, anchor="middle")
    tag(s, x + pad, my + 152, "No es superioridad demostrada", fill=CHIP, color=PAPER, size=18,
        h=36, pad=12)


def _panel_ranking(s, x, y, w, h):
    card(s, x, y, w, h, accent=BLUE_LIGHT)
    pad = 32
    iw = w - 2 * pad
    vw = 150
    bw = iw - vw - 20
    label(s, x + pad, y + 26, iw, "Recall@1 por configuración · escala 0–100%",
          size=18, color=MUTED)
    r0 = y + 72
    pitch = (h - 72 - 30) / 7
    # techo del pool
    filas = [([("Techo del pool de candidatos", FONT_HEAD, 22, MUTED, True)],
              "12 consultas sin la verdad entre los 20 candidatos", TECHO, "91,84%", LINE)] + RECALL
    # el techo se marca solo en su fila (como en el original): no limita a las
    # configuraciones que no usan el pool de 20 candidatos
    for k, (nom, det, v, vs, col) in enumerate(filas):
        ry = r0 + k * pitch
        ex = _seg(s, x + pad, ry, nom, h=32, gap=10)
        text(s, ex + 6, ry, x + pad + bw - ex - 6, 32, det, size=20, font=FONT_TXT, color=MUTED,
             anchor="middle")
        if k == 0:
            rect(s, x + pad, ry + 42, bw, 26, fill=CHIP)
            rect(s, x + pad, ry + 42, bw * v, 26, fill=LINE, fill_alpha=0.45)
            rect(s, x + pad, ry + pitch - 10, iw, 1.5, fill=BLUE_LIGHT, fill_alpha=0.35)
        else:
            bar(s, x + pad, ry + 42, bw, 26, v, color=col)
        text(s, x + pad + bw + 20, ry + 30, vw, 50, vs, size=32, bold=True, font=FONT_HEAD,
             color=MUTED if k == 0 else (RED if col == RED else YELLOW if col == YELLOW
                                         else PAPER),
             align="right", anchor="middle")


def p14(prs, notas):
    """Lámina 73: Recall@1 sobre las 147 consultas de test."""
    s = add_slide(prs, bg_image=FONDO)
    subencabezado(s, OE5 + " · Recuperación", "Recall@1 sobre las 147 consultas de test")
    y, h = 282, 1010 - 282
    w1, g = 540, 28
    _panel_mejor(s, 96, y, w1, h)
    _panel_ranking(s, 96 + w1 + g, y, 1728 - w1 - g, h)
    notes(s, notas[73])


def construir(prs, notas):
    p12(prs, notas)
    p13(prs, notas)
    p14(prs, notas)
