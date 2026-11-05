"""Laminas 1-34: caratula, introduccion, antecedentes, problema, formulacion,
objetivo, hipotesis, variables, matriz y esquema del marco teorico.

Composicion basada en la imagen de referencia: fondo azul profundo con reticula,
encabezado con cuadro amarillo, paneles oscuros con borde azul fino y esquineros
amarillos. Solo se usan los textos e imagenes del proyecto.
"""

from pptx_kit import (FONT_HEAD, add_slide, arrow_shape, corners, ellipse, image_fit, line,
                      notes, rect, text)
from theme import (ASSETS, BLUE_LIGHT, BLUE_TEXT, FONDO, LINE, LOGO_BLANCO, LOGO_EMI,
                   MARGIN, MUTED, PANEL, PAPER, SURFACE, YELLOW, badge, header, panel)

A = ASSETS
FONT_TXT = "Barlow"

INTRO = [
    (A / "introduccion/int_1.png", "01 · El ecosistema de comercios"),
    (A / "introduccion/int_2.png", "02 · El volumen de datos"),
    (A / "introduccion/int_3.png", "03 · El enfoque de PLN"),
    (A / "introduccion/int_4.png", "04 · El operador y el problema"),
]
ANTECEDENTES = [
    (A / "antecedentes/ant_1.png", "La empresa y los comercios"),
    (A / "antecedentes/ant_2.png", "La extracción automática"),
    (A / "antecedentes/ant_3.png", "La comparación manual"),
    (A / "antecedentes/ant_4.png", "El reparto del trabajo"),
    (A / "antecedentes/ant_5.png", "Los cuatro estados"),
    (A / "antecedentes/ant_6.png", "El control de calidad"),
]
CAUSA_EFECTO = [
    ("Criterio no formalizado", "Decisiones inconsistentes"),
    ("Volumen creciente", "Mayor tiempo de respuesta"),
    ("Inspección visual", "Fatiga y riesgo de error humano"),
    ("Ausencia de trazabilidad", "Sin registro del porqué"),
]
TEORIA = [
    "Metodologías de desarrollo tecnológico",
    "Notación de modelado de procesos de negocio",
    "Fundamentos computacionales y entorno de ciencia de datos",
    "Minería de texto y procesamiento de lenguaje natural",
    "Modelos de representación de texto en el NLP",
    "Correspondencia de entidades",
    "Modelos de clasificación",
    "Métricas de similitud",
    "Evaluación de modelos",
    "Medición de eficiencia",
    "Sistemas de apoyo a la decisión",
    "Desarrollo web",
]

TOP, BOTTOM = 190, 1010  # zona de contenido bajo el encabezado


def _glow(slide, cx, cy, r):
    ellipse(slide, cx, cy, r, fill="#12305E", fill_alpha=0.55)
    ellipse(slide, cx, cy, r * 0.72, fill="#1A3F78", fill_alpha=0.35)


def _caption(slide, x, y, w, label):
    rect(slide, x, y, w, 64, fill="#07172D", fill_alpha=0.82, line=BLUE_LIGHT, line_w=1,
         line_alpha=0.4)
    rect(slide, x, y, 8, 64, fill=YELLOW)
    text(slide, x + 32, y, w - 48, 64, label, size=30, bold=True, font=FONT_HEAD,
         anchor="middle")


# ---------------------------------------------------------------- 1 caratula
TITULO_TESIS = ("Modelo de Procesamiento de Lenguaje Natural en la validación de "
                "correspondencia de productos del ecosistema Philips")
AUTOR = "Est. Cañez Larico Pablo Enrique"
TUTOR = "Tutor: Ing. Víctor Rodríguez Estévez"


def constelacion(cx, cy):
    """Nodos y aristas de la constelacion que rodea el circulo de la red."""
    nodes = [(cx - 196, cy - 284), (cx + 14, cy - 360), (cx + 220, cy - 210), (cx + 244, cy + 130),
             (cx - 228, cy - 10), (cx - 198, cy + 280), (cx + 64, cy + 338)]
    return nodes, [(0, 4), (0, 1), (1, 2), (2, 3), (4, 5), (5, 6), (3, 6)]


def red_neuronal(s, cx, cy, r):
    """Circulo con la red neuronal y constelacion de nodos (portada y cierre)."""
    nodes, aristas = constelacion(cx, cy)
    for a, b in aristas:
        line(s, *nodes[a], *nodes[b], color=BLUE_LIGHT, width=1.5, alpha=0.45)
    for (nx, ny) in nodes:
        ellipse(s, nx, ny, 7, fill=BLUE_TEXT)
    ellipse(s, cx, cy, r + 44, line="#0B5EA8", line_w=2, line_alpha=0.35)
    ellipse(s, cx, cy, r, fill=SURFACE, line=BLUE_LIGHT, line_w=5, name="Circulo red")
    image_fit(s, str(A / "introduccion/int_3.png"), cx - r * 0.66, cy - r * 0.66, r * 1.32,
              r * 1.32, name="Red neuronal", trim=True)


def caratula(prs, nota):
    import pptx_kit
    from componentes import wrap_lines
    from theme import LOGO_AZUL, logo, pie, rotulo_central

    if pptx_kit.TEMA != "claro":
        return _caratula_oscura(prs, nota)
    s = add_slide(prs)
    logo(s, LOGO_EMI, 120, 44, 132, name="Logo EMI")
    logo(s, LOGO_AZUL, 1800, 58, 104, align="right", name="Logo carrera")
    rotulo_central(s, "TRABAJO DE GRADO", 110, size=34, spacing=6, pad=56, regla=2)
    rect(s, 120, 224, 1680, 1.5, fill="#D6E1EE")
    # titulo en mayusculas
    tsize, tw = 50, 1060
    lineas = wrap_lines(TITULO_TESIS.upper(), tsize, tw, FONT_HEAD, True)
    th = len(lineas) * tsize * 1.2
    ty = 300
    rect(s, 150, ty + 6, 10, th - 12, fill=YELLOW, name="Acento titulo")
    text(s, 194, ty, tw + 40, th, [[ln] for ln in lineas], size=tsize, bold=True,
         font=FONT_HEAD, line_spacing=1.2, name="Titulo")
    text(s, 194, ty + th + 34, 1060, 46, "Caso de estudio: área de Agilsoft SRL.", size=32,
         color="#0B5EA8", bold=True, font=FONT_TXT, name="Caso de estudio")
    red_neuronal(s, 1500, 560, 200)
    # autor y tutor
    rect(s, 120, 880, 1680, 1.5, fill="#D6E1EE")
    text(s, 120, 904, 1100, 64, AUTOR.upper(), size=42, bold=True, font=FONT_HEAD,
         anchor="middle", name="Autor")
    text(s, 1180, 904, 620, 64, TUTOR, size=28, color=MUTED, align="right", anchor="middle",
         font=FONT_TXT, name="Tutor")
    pie(s)
    notes(s, nota)
    return s


def _caratula_oscura(prs, nota):
    s = add_slide(prs, bg_image=FONDO)
    rect(s, MARGIN, 76, 404, 196, fill="#FFFFFF", radius=18, name="Tarjeta logo EMI")
    image_fit(s, str(LOGO_EMI), MARGIN + 18, 90, 368, 168, name="Logo EMI", trim=True)
    image_fit(s, LOGO_BLANCO, 552, 124, 300, 100, name="Logo carrera", trim=True)
    # etiqueta
    corners(s, 150, 360, 470, 72, size=22, width=3)
    text(s, 150, 360, 470, 72, "TRABAJO DE GRADO", size=26, color=YELLOW, bold=True,
         font=FONT_HEAD, align="center", anchor="middle", spacing=4)
    # titulo en tres lineas, como en la referencia
    text(s, 150, 470, 1220, 190,
         [["Modelo de Procesamiento de Lenguaje"],
          ["Natural en la validación de correspondencia"],
          ["de productos del ecosistema Philips"]],
         size=50, bold=True, font=FONT_HEAD, line_spacing=1.22, name="Titulo")
    text(s, 150, 708, 1120, 46, "Caso de estudio: área de Agilsoft SRL.", size=32,
         color=BLUE_TEXT, bold=True, font=FONT_TXT)
    rect(s, 150, 884, 1620, 2, fill=LINE, fill_alpha=0.45)
    text(s, 150, 912, 1000, 64, "Est. Cañez Larico Pablo Enrique", size=42, bold=True,
         font=FONT_HEAD, anchor="middle", name="Autor")
    text(s, 1170, 912, 600, 64, "Tutor: Ing. Víctor Rodríguez Estévez", size=28,
         color=MUTED, align="right", anchor="middle", font=FONT_TXT)
    # red neuronal en circulo
    cx, cy, r = 1636, 480, 182
    nodes = [(1440, 196), (1650, 120), (1856, 270), (1880, 610), (1408, 470), (1438, 760),
             (1700, 818)]
    for a, b in [(0, 4), (0, 1), (1, 2), (2, 3), (4, 5), (5, 6), (3, 6)]:
        line(s, *nodes[a], *nodes[b], color=BLUE_LIGHT, width=1.5, alpha=0.45)
    for (nx, ny) in nodes:
        ellipse(s, nx, ny, 7, fill=BLUE_TEXT)
    ellipse(s, cx, cy, r + 44, line="#0B5EA8", line_w=2, line_alpha=0.55)
    ellipse(s, cx, cy, r, fill=SURFACE, line=BLUE_LIGHT, line_w=5)
    image_fit(s, str(A / "introduccion/int_3.png"), cx - 120, cy - 120, 240, 240,
              name="Red neuronal", trim=True)
    notes(s, nota)


# ------------------------------------------------------------- 2-5 introduccion
def introduccion(prs, k, nota):
    s = add_slide(prs, bg_image=FONDO)
    header(s, "Introducción")
    mx, my, mw, mh = MARGIN, TOP + 10, 1240, 800
    panel(s, mx, my, mw, mh, bracket_size=56)
    _glow(s, mx + mw / 2, my + 360, 330)
    img, label = INTRO[k]
    image_fit(s, str(img), mx + 150, my + 70, mw - 300, 560, trim=True)
    _caption(s, mx + 40, my + mh - 104, mw - 80, label)
    tx, tw = 1376, 448
    th = (mh - 3 * 20) / 4
    for j, (timg, _) in enumerate(INTRO):
        ty = my + j * (th + 20)
        active = j == k
        rect(s, tx, ty, tw, th, fill=PANEL, line=YELLOW if active else BLUE_LIGHT,
             line_w=3 if active else 1.5, line_alpha=1 if active else 0.45)
        image_fit(s, str(timg), tx + 40, ty + 22, tw - 140, th - 44,
                  alpha=1 if active else 0.45, trim=True)
        badge(s, tx + tw - 58, ty + th - 42, f"{j + 1:02d}", size=44,
              fill=YELLOW if active else "#1B3A66", color="#07172D" if active else PAPER)
    notes(s, nota)


# ------------------------------------------------------------ 6-12 antecedentes
def _mosaico(s, dim=False):
    gx, gy, gw, gh = MARGIN, TOP + 10, 1728, 800
    cw, ch = (gw - 2 * 32) / 3, (gh - 32) / 2
    for j, (img, _) in enumerate(ANTECEDENTES):
        x = gx + (j % 3) * (cw + 32)
        y = gy + (j // 3) * (ch + 32)
        rect(s, x, y, cw, ch, fill=PANEL, fill_alpha=0.6 if dim else 1, line=BLUE_LIGHT,
             line_w=1.5, line_alpha=0.2 if dim else 0.45)
        if not dim:
            corners(s, x - 8, y - 8, cw + 16, ch + 16, size=26, color=BLUE_LIGHT, width=2.5,
                    alpha=0.8)
        image_fit(s, str(img), x + 60, y + 64, cw - 120, ch - 110, alpha=0.18 if dim else 1,
                  trim=True)
        if not dim:
            badge(s, x + 18, y + 16, f"{j + 1:02d}", size=40)
    return gx, gy, gw, gh


def antecedentes_mosaico(prs, nota):
    s = add_slide(prs, bg_image=FONDO)
    header(s, "Antecedentes")
    _mosaico(s)
    notes(s, nota)


def antecedentes_foco(prs, k, nota):
    s = add_slide(prs, bg_image=FONDO)
    header(s, "Antecedentes")
    _mosaico(s, dim=True)
    fx, fy, fw, fh = 330, 232, 1260, 740
    panel(s, fx, fy, fw, fh, fill="#0B2242", border=BLUE_LIGHT, border_alpha=0.8,
          bracket_size=56)
    _glow(s, fx + fw / 2, fy + 320, 300)
    img, label = ANTECEDENTES[k]
    image_fit(s, str(img), fx + 140, fy + 90, fw - 280, 480, trim=True)
    badge(s, fx + 28, fy + 26, f"{k + 1:02d}", size=64)
    _caption(s, fx + 40, fy + fh - 104, fw - 80, f"{k + 1:02d} · {label}")
    notes(s, nota)


# --------------------------------------------------------- 13-17 planteamiento
def _par(s, x, y, w, h, j, big=False, dim=False):
    rect(s, x, y, w, h, fill=PANEL, fill_alpha=0.6 if dim else 1, line=BLUE_LIGHT,
         line_w=1.5, line_alpha=0.2 if dim else 0.45)
    a = 0.18 if dim else 1
    lab = 28 if big else 20
    lab_h = lab * 1.5
    top_pad = 24 if big else 18
    img_s = min(h - (top_pad + lab_h + 24) - (130 if big else 26), (w - 300) / 2)
    gap = (w - 2 * img_s) / 3 if not big else (w - 2 * img_s) / 4
    cx1 = x + gap + img_s / 2 if not big else x + gap + img_s / 2
    cx2 = x + w - gap - img_s / 2
    iy = y + top_pad + lab_h + (18 if big else 8)
    if not dim:
        text(s, cx1 - 200, y + top_pad, 400, lab_h, f"CAUSA {j + 1:02d}", size=lab, bold=True,
             font=FONT_HEAD, color=YELLOW, spacing=1.5, align="center")
        text(s, cx2 - 200, y + top_pad, 400, lab_h, f"EFECTO {j + 1:02d}", size=lab,
             bold=True, font=FONT_HEAD, color=MUTED, spacing=1.5, align="center")
    image_fit(s, str(A / f"causa-efecto/causa_{j + 1}.png"), cx1 - img_s / 2, iy, img_s, img_s,
              alpha=a, trim=True)
    image_fit(s, str(A / f"causa-efecto/efecto_{j + 1}.png"), cx2 - img_s / 2, iy, img_s,
              img_s, alpha=a, trim=True)
    # flecha amarilla rellena entre ambos circulos
    ax0, ax1 = cx1 + img_s / 2 + (40 if big else 22), cx2 - img_s / 2 - (40 if big else 22)
    ah = 46 if big else 30
    arrow_shape(s, ax0, iy + img_s / 2 - ah / 2, ax1 - ax0, ah, color=YELLOW, alpha=a)
    if big:
        c, e = CAUSA_EFECTO[j]
        ty = iy + img_s + 30
        text(s, cx1 - 300, ty, 600, 50, c, size=34, bold=True, font=FONT_HEAD, align="center")
        text(s, cx2 - 300, ty, 600, 50, e, size=34, bold=True, font=FONT_HEAD, align="center")


def _tablero(s, dim=False):
    gx, gy = MARGIN, TOP + 10
    cw, ch = (1728 - 32) / 2, (800 - 32) / 2
    for j in range(4):
        _par(s, gx + (j % 2) * (cw + 32), gy + (j // 2) * (ch + 32), cw, ch, j, dim=dim)


def problema_tablero(prs, nota):
    s = add_slide(prs, bg_image=FONDO)
    header(s, "Planteamiento del problema")
    _tablero(s)
    notes(s, nota)


def problema_foco(prs, k, nota):
    s = add_slide(prs, bg_image=FONDO)
    header(s, "Planteamiento del problema")
    _tablero(s, dim=True)
    fx, fy, fw, fh = 300, 236, 1320, 736
    corners(s, fx - 10, fy - 10, fw + 20, fh + 20, size=56, width=3)
    _par(s, fx, fy, fw, fh, k, big=True)
    notes(s, nota)


# ----------------------------------------------- 18-19 formulacion / objetivo
def enunciado(prs, titulo, cuerpo, nota):
    s = add_slide(prs, bg_image=FONDO)
    header(s, titulo)
    px_, py_, pw_, ph_ = 190, 300, 1540, 560
    panel(s, px_, py_, pw_, ph_, bracket_size=60)
    rect(s, px_, py_ + 60, 8, ph_ - 120, fill=YELLOW)
    cuerpo = cuerpo.replace("Agilsoft SRL", "Agilsoft\u00a0SRL")
    text(s, px_ + 90, py_ + 60, pw_ - 180, ph_ - 120, cuerpo, size=42, font=FONT_TXT,
         line_spacing=1.5, anchor="middle")
    notes(s, nota)


# ------------------------------------------------------------------ 20 hipotesis
def hipotesis(prs, nota):
    s = add_slide(prs, bg_image=FONDO)
    header(s, "Hipótesis")
    text(s, MARGIN, 182, 900, 34, "HIPÓTESIS DE INVESTIGACIÓN", size=22, bold=True,
         font=FONT_HEAD, color=YELLOW, spacing=2.5)
    rect(s, MARGIN, 232, 8, 150, fill=YELLOW)
    text(s, MARGIN + 34, 228, 1690, 160,
         "El desarrollo del modelo de Procesamiento de Lenguaje Natural aplicado al ecosistema "
         "Philips mejora la consistencia de la calidad del matching y reduce el tiempo de "
         "validación en Agilsoft SRL.", size=38, bold=True, font=FONT_HEAD, line_spacing=1.3)
    # mapa de variables
    vy, vh = 440, 450
    panel(s, MARGIN, vy, 560, vh, fill=SURFACE, bracket_size=40)
    rect(s, MARGIN, vy + 60, 8, vh - 120, fill=YELLOW)
    text(s, MARGIN + 50, vy + 130, 480, 34, "VARIABLE INDEPENDIENTE", size=22, bold=True,
         font=FONT_HEAD, color=YELLOW, spacing=2)
    text(s, MARGIN + 50, vy + 172, 480, 70, "Modelo de PLN", size=52, bold=True,
         font=FONT_HEAD)
    text(s, MARGIN + 50, vy + 262, 470, 90, "Aplicado a la correspondencia de productos",
         size=28, color=MUTED, font=FONT_TXT, line_spacing=1.3)
    outs = [("VD₁ · CALIDAD", "Consistencia del matching",
             "Exactitud, precisión, recall y F1-score", "MEJORA"),
            ("VD₂ · EFICIENCIA", "Tiempo de validación",
             "Segundos por caso y reducción porcentual", "REDUCE")]
    ox, ow, oh = 1000, 824, 210
    line(s, MARGIN + 572, vy + vh / 2, MARGIN + 720, vy + vh / 2, color=YELLOW, width=4)
    for j, (lab, tit, meta, verb) in enumerate(outs):
        oy = vy + j * (oh + 30)
        rect(s, ox, oy, ow, oh, fill=SURFACE, line=BLUE_LIGHT, line_w=1.5, line_alpha=0.45)
        rect(s, ox, oy, 8, oh, fill=BLUE_LIGHT)
        text(s, ox + 46, oy + 34, 700, 32, lab, size=22, bold=True, font=FONT_HEAD,
             color=BLUE_TEXT, spacing=2)
        text(s, ox + 46, oy + 74, 740, 64, tit, size=44, bold=True, font=FONT_HEAD)
        text(s, ox + 46, oy + 144, 740, 40, meta, size=26, color=MUTED, font=FONT_TXT)
        ay = oy + oh / 2
        line(s, MARGIN + 720, vy + vh / 2, ox - 24, ay, color=YELLOW, width=4, arrow=True)
        text(s, 720, ay - 64 if j == 0 else ay + 14, 220, 40, verb, size=22, bold=True,
             font=FONT_HEAD, color=YELLOW, spacing=2, align="center")
    rect(s, MARGIN, 930, 1728, 76, fill=SURFACE, line=BLUE_LIGHT, line_w=1.5, line_alpha=0.45)
    text(s, MARGIN + 36, 930, 220, 76, "CONTRASTE", size=22, bold=True, font=FONT_HEAD,
         color=YELLOW, spacing=2, anchor="middle")
    text(s, MARGIN + 260, 930, 1440, 76,
         "Rendimiento predictivo, registros del uso del modelo y eficiencia temporal",
         size=28, font=FONT_TXT, anchor="middle")
    notes(s, nota)


# ----------------------------------------------------------------- 21 variables
def variables(prs, nota):
    s = add_slide(prs, bg_image=FONDO)
    header(s, "1.5.2 Identificación de las variables")
    cy, ch = 250, 680
    cw = (1728 - 60) / 2
    for j, (lab, fill_lab, col_lab) in enumerate([("VARIABLE INDEPENDIENTE (VI)", YELLOW, "#07172D"),
                                                  ("VARIABLES DEPENDIENTES (VD)", "#0B5EA8", PAPER)]):
        x = MARGIN + j * (cw + 60)
        panel(s, x, cy, cw, ch, fill=SURFACE, bracket_size=48)
        rect(s, x, cy + 60, 10, ch - 120, fill=fill_lab)
        rect(s, x + 60, cy + 70, 580, 58, fill=fill_lab)
        text(s, x + 60, cy + 70, 580, 58, lab, size=24, bold=True, font=FONT_HEAD,
             color=col_lab, align="center", anchor="middle", spacing=1.5)
    x = MARGIN
    text(s, x + 60, cy + 200, cw - 120, 380,
         "Modelo de Procesamiento de Lenguaje Natural aplicado a la correspondencia de "
         "productos.", size=42, bold=True, font=FONT_HEAD, line_spacing=1.3)
    x = MARGIN + cw + 60
    for j, (cod, txt) in enumerate([("VD₁", "Consistencia de la calidad del matching."),
                                    ("VD₂", "Tiempo de validación.")]):
        yy = cy + 200 + j * 190
        text(s, x + 60, yy, 130, 60, cod, size=42, bold=True, font=FONT_HEAD, color=YELLOW)
        text(s, x + 200, yy, cw - 260, 170, txt, size=42, bold=True, font=FONT_HEAD,
             line_spacing=1.3)
    notes(s, nota)


# ------------------------------------------------------------------- 22 matriz
def matriz(prs, nota):
    from componentes import PANEL_2, ecuacion, tag

    s = add_slide(prs, bg_image=FONDO)
    header(s, "Matriz de operacionalización de variables")
    x0, y0 = MARGIN, 172
    cols = [446, 282, 520, 480]
    xs = [x0]
    for c in cols:
        xs.append(xs[-1] + c)
    tw = sum(cols)
    hh = 52
    rect(s, x0, y0, tw, hh, fill="#0B5EA8")
    for j, t in enumerate(["VARIABLE", "DIMENSIÓN", "INDICADOR", "SUBINDICADOR"]):
        text(s, xs[j] + 24, y0, cols[j] - 30, hh, t, size=20, bold=True, font=FONT_HEAD,
             anchor="middle", spacing=2)
    y = y0 + hh

    def variable(yy, h, tipo, nombre, color):
        from componentes import wrap_lines

        rect(s, x0, yy, 8, h, fill=color)
        n = len(wrap_lines(nombre, 22, cols[0] - 70, FONT_HEAD, True))
        bloque = 36 + 12 + n * 22 * 1.22
        top = yy + (h - bloque) / 2
        tag(s, x0 + 28, top, tipo, fill=color if color == YELLOW else "#0B5EA8",
            color="#07172D" if color == YELLOW else PAPER, size=18, h=36)
        text(s, x0 + 28, top + 48, cols[0] - 50, n * 22 * 1.22 + 6, nombre, size=22, bold=True,
             font=FONT_HEAD, line_spacing=1.22)

    def celda(j, yy, h, contenido, size=23, color=PAPER, anchor="middle"):
        text(s, xs[j] + 24, yy + 14, cols[j] - 44, h - 28, contenido, size=size,
             font=FONT_TXT, color=color, anchor=anchor, line_spacing=1.25)

    def vinetas(j, yy, h, items):
        n = len(items)
        step = 34
        top = yy + (h - n * step) / 2
        for k, it in enumerate(items):
            ellipse(s, xs[j] + 30, top + k * step + 16, 4.5, fill=YELLOW)
            text(s, xs[j] + 46, top + k * step, cols[j] - 60, step, it, size=21, font=FONT_TXT,
                 anchor="middle")

    def indicador(yy, h, texto, partes, dy=22):
        text(s, xs[2] + 24, yy + 18, cols[2] - 44, 32, texto, size=20, font=FONT_TXT,
             color=MUTED)
        ecuacion(s, xs[2] + 24, yy + h / 2 + dy, partes, size=28, color=YELLOW,
                 res_color=YELLOW)

    def fondo(yy, h, k):
        rect(s, x0, yy, tw, h, fill=PANEL if k % 2 == 0 else PANEL_2)

    # VI
    h = 176
    fondo(y, h, 0)
    variable(y, h, "Variable independiente",
             "Modelo de Procesamiento de Lenguaje Natural aplicado a la correspondencia de "
             "productos", YELLOW)
    celda(1, y, h, "Arquitectura algorítmica.")
    celda(2, y, h, "Modelo de correspondencia basado en NLP.")
    vinetas(3, y, h, ["Nivel de similitud calculado", "Capacidad de generalización",
                      "Tolerancia y procesamiento de ruido textual."])
    y += h
    rect(s, x0, y, tw, 1.5, fill=BLUE_LIGHT, fill_alpha=0.45)
    # VD1 (dos filas)
    h1 = h2 = 176
    fondo(y, h1 + h2, 1)
    variable(y, h1 + h2, "Variable dependiente", "Consistencia de la calidad del matching.",
             BLUE_LIGHT)
    rect(s, xs[1], y + h1, tw - cols[0], 1, fill=LINE, fill_alpha=0.35)
    celda(1, y, h1, "Rendimiento predictivo algorítmico.")
    indicador(y, h1, "Porcentaje de exactitud en la clasificación binaria:",
              [("var", "Accuracy"), "=", ("frac", ["TP + TN"], ["Total"]), "× 100"])
    vinetas(3, y, h1, ["Precisión", "Recall", "F1-score"])
    celda(1, y + h1, h2, "Estabilidad operativa frente al factor humano.")
    indicador(y + h1, h2, "Tasa de error de validación:",
              [("var", "Error"), "=", ("frac", ["FP + FN"], ["Total"]), "× 100"])
    vinetas(3, y + h1, h2, ["Tasa de error por ambigüedad léxica.",
                            "Nivel de error por fatiga operativa.",
                            "Concordancia inter-evaluador."])
    y += h1 + h2
    rect(s, x0, y, tw, 1.5, fill=BLUE_LIGHT, fill_alpha=0.45)
    # VD2
    h = 198
    fondo(y, h, 0)
    variable(y, h, "Variable dependiente", "Tiempo de validación", BLUE_LIGHT)
    celda(1, y, h, "Eficiencia temporal")
    indicador(y, h, "Tiempo de procesamiento operativo en segundos:",
              [("bar", "t"), "=", ("frac", [("sum", "i=1", "n"), ("sub", "t", "i")], ["n"])],
              dy=34)
    vinetas(3, y, h, ["Tiempo de latencia algorítmica del modelo.",
                      "Tiempo promedio de validación manual.",
                      "Mejora porcentual de reducción de tiempo."])
    y += h
    for xv in xs[1:-1]:
        rect(s, xv, y0 + hh, 1, y - y0 - hh, fill=LINE, fill_alpha=0.3)
    rect(s, x0, y0, tw, y - y0, line=BLUE_LIGHT, line_w=1.5, line_alpha=0.55)
    corners(s, x0 - 10, y0 - 10, tw + 20, y - y0 + 20, size=40, width=3)
    text(s, x0, y + 18, 1000, 30, "Tabla 2: Matriz de operacionalización de variables",
         size=20, bold=True, color=YELLOW, font=FONT_TXT)
    text(s, x0 + tw - 600, y + 18, 600, 30, "Fuente: Elaboración propia, 2026", size=20,
         color=MUTED, italic=True, align="right", font=FONT_TXT)
    notes(s, nota)


# ------------------------------------------------------------ 23-34 marco teorico
def marco_teorico(prs, k, nota):
    s = add_slide(prs, bg_image=FONDO)
    header(s, "Esquema del marco teórico")
    mx, my, mw, mh = MARGIN, TOP + 10, 760, 800
    panel(s, mx, my, mw, mh, bracket_size=56)
    _glow(s, mx + mw / 2, my + mh / 2, 300)
    image_fit(s, str(A / f"marco-teorico/{k + 1:02d}_mt.png"), mx + 90, my + 110, mw - 180,
              mh - 220, trim=True)
    rx, rw = 940, 884
    text(s, rx, 236, 400, 44, f"{k + 1:02d} / 12", size=34, bold=True, font=FONT_HEAD,
         color=YELLOW, spacing=2)
    rect(s, rx, 292, 90, 5, fill=YELLOW)
    text(s, rx, 324, rw, 300, TEORIA[k], size=58, bold=True, font=FONT_HEAD,
         line_spacing=1.15)
    # guia numerada 6 x 2
    gw, gh, gap = (rw - 5 * 16) / 6, 150, 16
    for j in range(12):
        gx = rx + (j % 6) * (gw + gap)
        gy = 690 + (j // 6) * (gh + gap)
        active = j == k
        rect(s, gx, gy, gw, gh, fill=PANEL, line=YELLOW if active else BLUE_LIGHT,
             line_w=3 if active else 1.5, line_alpha=1 if active else 0.4)
        image_fit(s, str(A / f"marco-teorico/{j + 1:02d}_mt.png"), gx + 26, gy + 14, gw - 52,
                  gh - 60, alpha=1 if active else 0.4, trim=True)
        text(s, gx, gy + gh - 40, gw, 32, f"{j + 1:02d}", size=20, bold=True,
             font=FONT_HEAD, color=YELLOW if active else MUTED, align="center")
    notes(s, nota)


def construir(prs, notas):
    """Agrega las laminas 1-34 en orden."""
    caratula(prs, notas[1])
    for k in range(4):
        introduccion(prs, k, notas[2 + k])
    import antecedentes_pm

    antecedentes_mosaico(prs, notas[6])
    for k in range(6):
        antecedentes_foco(prs, k, notas[7 + k])
        if k == 1:    # tras «02 · La extracción automática»: anatomía de cinco páginas
            antecedentes_pm.construir_extraccion(prs)
        elif k == 2:  # tras «03 · La comparación manual»: validación de correspondencia
            antecedentes_pm.construir_validacion(prs)
    problema_tablero(prs, notas[13])
    for k in range(4):
        problema_foco(prs, k, notas[14 + k])
    enunciado(prs, "Formulación del problema",
              "El procedimiento manual de validación de correspondencia de productos del "
              "ecosistema Philips en el área de operaciones de la empresa Agilsoft SRL "
              "presenta variabilidad en los criterios de validación, lo que genera "
              "inconsistencias en la calidad del matching e incremento en el tiempo de "
              "validación.", notas[18])
    enunciado(prs, "Objetivo general",
              "Desarrollar un modelo de Procesamiento de Lenguaje Natural en la validación de "
              "correspondencia de productos del ecosistema Philips, orientado a mejorar la "
              "calidad del matching y reducir el tiempo de validación en el área de "
              "operaciones de la empresa Agilsoft SRL.", notas[19])
    hipotesis(prs, notas[20])
    variables(prs, notas[21])
    matriz(prs, notas[22])
    for k in range(12):
        marco_teorico(prs, k, notas[23 + k])
