"""OE1 · Analizar el proceso actual (láminas 35-44 de la versión editada por el autor).

Escala de valoración, comparación de metodologías (ciencia de datos y gestión),
actores, diagramas del autor (flujo lógico, BPMN AS-IS en dos partes, BPMN
propuesto y subproceso) y estimación de tiempos manuales. Los diagramas del autor
se insertan en Canva sobre el marco que deja esta lámina (ver DIAGRAMAS).
"""

from pathlib import Path

from pptx_kit import (add_slide, animar, ellipse, image, image_fit, notes, rect,
                      registrar_barra, text)
from theme import ASSETS, FONDO, YELLOW
from componentes import (BLUE_LIGHT, CHIP, CONTENT_TOP, DARK, FONT_HEAD, FONT_TXT, MUTED, PAPER,
                         RED, bar, card, flecha, label, numbadge, subencabezado, tag,
                         text_width)

OE1 = "OE1 · Analizar el proceso actual"
AZUL = "#0B5EA8"
NARANJA = "#F08A3C"

# Diagramas del autor: archivo local de respaldo (si existe) y relación de aspecto del
# recorte que el autor dejó en Canva. construir.py los reemplaza por la imagen original
# de Canva (update_fill) tras importar.
DIAGRAMAS = {}


# ------------------------------------------------------------------ escala 1-5
def p_escala(prs, nota):
    s = add_slide(prs, bg_image=FONDO)
    subencabezado(s, OE1 + " · Criterios de evaluación", "Escala de valoración de los criterios")
    filas = [("1", "Muy deficiente", "Carencias severas: compromete la viabilidad.", RED, PAPER),
             ("2", "Deficiente", "Limitaciones importantes para su aplicación.", NARANJA, DARK),
             ("3", "Aceptable", "Cumple los requisitos mínimos.", YELLOW, DARK),
             ("4", "Bueno", "Supera lo esperado: aporta ventajas claras.", BLUE_LIGHT, PAPER),
             ("5", "Excelente", "Desempeño excepcional y alta adecuación al proyecto.", AZUL,
              PAPER)]
    gap = 24
    cw = (1728 - 4 * gap) / 5
    y0, ch = CONTENT_TOP + 10, 590
    for k, (n, nom, interp, col, tcol) in enumerate(filas):
        x = 96 + k * (cw + gap)
        card(s, x, y0, cw, ch, accent=col)
        # número en círculo
        cx, cy, r = x + cw / 2, y0 + 112, 70
        ellipse(s, cx, cy, r, fill=col)
        t = text(s, cx - r, cy - r, 2 * r, 2 * r, n, size=72, bold=True, font=FONT_HEAD,
                 color=tcol, align="center", anchor="middle")
        animar(s, t, "zoom", delay_ms=150 + k * 140, dur_ms=500)
        # nivel: barras escalonadas
        bw, bg_, bx0 = 26, 10, cx - (5 * 26 + 4 * 10) / 2
        for j in range(5):
            hh = 18 + j * 12
            on = j <= k
            rect(s, bx0 + j * (bw + bg_), y0 + 286 - hh, bw, hh,
                 fill=col if on else CHIP, line=None)
        text(s, x + 16, y0 + 314, cw - 32, 48, nom, size=34, bold=True, font=FONT_HEAD,
             align="center")
        rect(s, x + cw / 2 - 34, y0 + 378, 68, 4, fill=col)
        text(s, x + 24, y0 + 404, cw - 48, 170, interp, size=26, font=FONT_TXT, align="center",
             line_spacing=1.35)
    # escala continua al pie
    yb = y0 + ch + 40
    label(s, 96, yb, 1400, "Cada alternativa se puntúa de 1 a 5 en cada criterio", size=18,
          color=MUTED)
    seg = 1728 / 5
    for k, (_, _, _, col, _) in enumerate(filas):
        r_ = rect(s, 96 + k * seg, yb + 36, seg - 4, 14, fill=col)
        animar(s, r_, "wipe", delay_ms=700 + k * 90, dur_ms=400)
    text(s, 96, yb + 58, 400, 30, "menor adecuación", size=20, font=FONT_TXT, color=MUTED)
    text(s, 1824 - 400, yb + 58, 400, 30, "mayor adecuación", size=20, font=FONT_TXT,
         color=MUTED, align="right")
    notes(s, nota)
    return s


# ------------------------------------------------------- comparación de métodos
def _comparacion(prs, nota, eyebrow, titulo, metodos, criterios, ganador):
    s = add_slide(prs, bg_image=FONDO)
    subencabezado(s, eyebrow, titulo)
    y0 = CONTENT_TOP + 6
    x0, w0 = 96, 1728
    ccrit = 560
    colw = (w0 - ccrit - 40) / len(metodos)
    nrows = len(criterios)
    hh = 70
    tot_h = 128
    rh = (1010 - y0 - hh - tot_h - 20) / nrows
    card(s, x0, y0, w0, 1010 - y0, accent=None)
    # columna ganadora resaltada
    gi = metodos.index(ganador)
    gx = x0 + ccrit + 20 + gi * colw
    rect(s, gx + 6, y0 + 8, colw - 12, 1010 - y0 - 16, fill="#FFF8DB", line=YELLOW, line_w=2.5)
    # encabezado
    label(s, x0 + 32, y0 + 24, ccrit - 40, "Criterio", size=18, color=MUTED)
    for j, m in enumerate(metodos):
        cx = x0 + ccrit + 20 + j * colw
        text(s, cx, y0 + 14, colw, 40, m, size=28, bold=True, font=FONT_HEAD, align="center",
             color=AZUL if m != ganador else DARK)
        if m == ganador:
            tw = text_width("SELECCIONADA", 14, FONT_HEAD, True, 1.2) + 34
            tag(s, cx + (colw - tw) / 2, y0 + 50, "Seleccionada", size=14, h=26)
    rect(s, x0 + 24, y0 + hh + 12, w0 - 48, 1.5, fill="#D6E1EE")
    # filas
    for i, (crit, vals) in enumerate(criterios):
        ry = y0 + hh + 20 + i * rh
        if i:
            rect(s, x0 + 24, ry, w0 - 48, 1, fill="#E3EAF3")
        text(s, x0 + 32, ry, ccrit - 40, rh, crit, size=25, bold=True, font=FONT_TXT,
             anchor="middle", line_spacing=1.15)
        for j, v in enumerate(vals):
            cx = x0 + ccrit + 20 + j * colw
            col = YELLOW if metodos[j] == ganador else BLUE_LIGHT
            r, g = 10, 9
            dots_w = 5 * 2 * r + 4 * g
            dx = cx + (colw - dots_w - 64) / 2
            for d in range(5):
                ellipse(s, dx + r + d * (2 * r + g), ry + rh / 2, r,
                        fill=col if d < v else "#E3EAF3")
            text(s, dx + dots_w + 18, ry, 46, rh, str(v), size=30, bold=True, font=FONT_HEAD,
                 anchor="middle", color=DARK if metodos[j] == ganador else AZUL)
    # totales con barras
    ty = 1010 - tot_h - 6
    rect(s, x0 + 24, ty, w0 - 48, 2, fill=AZUL)
    text(s, x0 + 32, ty + 10, ccrit - 40, tot_h - 20, "Total", size=30, bold=True,
         font=FONT_HEAD, anchor="middle")
    maxpos = 5 * nrows
    for j, m in enumerate(metodos):
        cx = x0 + ccrit + 20 + j * colw
        tot = sum(v[1][j] for v in criterios)
        col = YELLOW if m == ganador else BLUE_LIGHT
        t = text(s, cx, ty + 14, colw, 56, f"{tot}", size=46, bold=True, font=FONT_HEAD,
                 align="center", color=DARK if m == ganador else AZUL)
        animar(s, t, "zoom", dur_ms=500)
        bw = colw - 80
        bar(s, cx + 40, ty + 82, bw, 14, tot / maxpos, color=col)
        text(s, cx + 40, ty + 98, bw, 24, f"de {maxpos} puntos", size=18, font=FONT_TXT,
             color=MUTED, align="center")
    notes(s, nota)
    return s


def p_crisp(prs, nota):
    return _comparacion(
        prs, nota, "Metodología de ciencia de datos",
        "Comparación de metodologías de ciencia de datos", ["CRISP-DM", "KDD", "SEMMA"],
        [("Comprensión del negocio", [5, 2, 2]),
         ("Iteratividad del proceso analítico", [5, 3, 3]),
         ("Detalle en la preparación de datos", [4, 3, 4]),
         ("Madurez y adopción en la industria", [5, 3, 2]),
         ("Flexibilidad para modelos de IA", [4, 3, 3])],
        "CRISP-DM")


def p_agiles(prs, nota):
    return _comparacion(
        prs, nota, "Metodología de gestión de proyectos", "Comparación de metodologías ágiles",
        ["SCRUM", "KANBAN", "XP"],
        [("Gestión visual del flujo de trabajo", [4, 5, 3]),
         ("Flexibilidad ante cambios técnicos", [4, 5, 4]),
         ("Roles formales mínimos", [2, 5, 3]),
         ("Control de codificación e integración", [4, 5, 4]),
         ("Desarrollo incremental de interfaz y APIs", [4, 5, 4]),
         ("Seguimiento continuo sin sprints", [3, 5, 3])],
        "KANBAN")


# ------------------------------------------------------------------- actores
def p_actores(prs, nota):
    s = add_slide(prs, bg_image=FONDO)
    subencabezado(s, "Identificación de los actores del proceso de validación",
                  "Actores del proceso de validación")
    actores = [
        ("Equipo de Web Scraping", "Extrae datos de productos desde retailers internacionales.",
         "Registros estructurados.", ASSETS / "antecedentes/ant_2.png", BLUE_LIGHT),
        ("Analistas de Product Matching",
         "Validan a mano la correspondencia contra el catálogo oficial.",
         "Clasificación operativa: Match, NIC, Hidden, Delete.",
         ASSETS / "antecedentes/ant_3.png", YELLOW),
        ("Quality Assurance (QA)", "Supervisa la calidad de las decisiones del equipo.",
         "Validación final y corrección.", ASSETS / "antecedentes/ant_6.png", AZUL),
    ]
    gap = 90
    cw = (1728 - 2 * gap) / 3
    y0, ch = CONTENT_TOP + 10, 1010 - CONTENT_TOP - 10
    for k, (nom, fun, res, img, col) in enumerate(actores):
        x = 96 + k * (cw + gap)
        card(s, x, y0, cw, ch, accent=col)
        rect(s, x + 24, y0 + 28, cw - 48, 230, fill="#EAF1FA")
        im = image_fit(s, str(img), x + 40, y0 + 38, cw - 80, 210, trim=True)
        animar(s, im, "fade", delay_ms=150 + k * 260, dur_ms=600)
        numbadge(s, x + 24, y0 + 28, f"{k + 1}", size=46,
                 fill=col, color=DARK if col == YELLOW else PAPER)
        text(s, x + 28, y0 + 282, cw - 56, 80, nom, size=30, bold=True, font=FONT_HEAD,
             line_spacing=1.15)
        label(s, x + 28, y0 + 372, cw - 56, "Función principal", size=17, color=MUTED)
        text(s, x + 28, y0 + 400, cw - 56, 110, fun, size=25, font=FONT_TXT, line_spacing=1.3)
        # resultado
        ry = y0 + ch - 150
        rect(s, x + 24, ry, cw - 48, 126, fill="#FFF8DB" if col == YELLOW else "#EAF1FA",
             line=col, line_w=1.5)
        rect(s, x + 24, ry, 6, 126, fill=col)
        label(s, x + 48, ry + 14, cw - 90, "Resultado generado", size=16, color=MUTED)
        text(s, x + 48, ry + 42, cw - 90, 76, res, size=24, bold=True, font=FONT_TXT,
             line_spacing=1.2)
        if k < 2:
            flecha(s, x + cw + 14, y0 + 143, x + cw + gap - 14, color=YELLOW, h=36)
    notes(s, nota)
    return s


# ------------------------------------------------------- diagramas del autor
def _marcador(aspecto: float) -> str:
    """PNG de reserva con el aspecto del diagrama; en Canva se reemplaza por el original."""
    import pptx_kit
    from PIL import Image, ImageDraw

    from componentes import _pil_font

    out = Path(pptx_kit.OPT_DIR or "/tmp") / f"marcador_{aspecto:.4f}.png"
    if not out.exists():
        w = 1600
        h = round(w / aspecto)
        im = Image.new("RGB", (w, h), (244, 247, 251))
        d = ImageDraw.Draw(im)
        for x in range(0, w, 28):
            d.line([x, 0, x + 14, 0], fill=(195, 210, 227), width=4)
            d.line([x, h - 2, x + 14, h - 2], fill=(195, 210, 227), width=4)
        for y in range(0, h, 28):
            d.line([0, y, 0, y + 14], fill=(195, 210, 227), width=4)
            d.line([w - 2, y, w - 2, y + 14], fill=(195, 210, 227), width=4)
        f = _pil_font("Montserrat", True, 44)
        t = "Diagrama del autor"
        d.text(((w - d.textlength(t, font=f)) / 2, h / 2 - 30), t, font=f, fill=(78, 95, 120))
        out.parent.mkdir(parents=True, exist_ok=True)
        im.save(out)
    return str(out)


def p_diagrama(prs, nota, clave, eyebrow, titulo, respaldo=None, aspecto=1.6):
    """Lámina con un diagrama del autor a todo el ancho, en un marco blanco.

    En el PPTX va la imagen local de respaldo (o un marco vacío); en Canva se reemplaza
    por la imagen original del autor con su mismo recorte."""
    s = add_slide(prs, bg_image=FONDO)
    subencabezado(s, eyebrow, titulo)
    y0 = CONTENT_TOP - 4
    h = 1010 - y0
    card(s, 96, y0, 1728, h, accent=None, fill="#FFFFFF")
    # caja del diagrama: máxima con el aspecto del recorte del autor
    bw, bh = 1728 - 48, h - 40
    if bw / bh > aspecto:
        dw, dh = bh * aspecto, bh
    else:
        dw, dh = bw, bw / aspecto
    dx, dy = 96 + (1728 - dw) / 2, y0 + (h - dh) / 2
    if respaldo and Path(respaldo).exists():
        pic = image_fit(s, str(respaldo), dx, dy, dw, dh, name=f"Diagrama {clave}")
    else:
        pic = image(s, _marcador(aspecto), dx, dy, dw, dh, name=f"Diagrama {clave}")
    DIAGRAMAS[clave] = dict(pagina=s._num, left=dx, top=dy, width=dw, height=dh)
    s._diagrama = clave
    animar(s, pic, "fade", dur_ms=700)
    notes(s, nota)
    return s


# -------------------------------------------------------------- tiempos manuales
def p_tiempos(prs, nota):
    s = add_slide(prs, bg_image=FONDO)
    subencabezado(s, OE1 + " · Línea base",
                  "Estimación de los tiempos del proceso de validación manual")
    y0 = CONTENT_TOP + 6
    h = 1010 - y0
    lw = 1080
    # --- complejidad: rangos de tiempo sobre un eje 0-120 s
    card(s, 96, y0, lw, h, accent=BLUE_LIGHT)
    label(s, 128, y0 + 26, lw - 64,
          "Estimación de tiempos de validación por nivel de complejidad", size=18, color=YELLOW)
    niveles = [("Baja", "Identificador exacto (SKU, EAN o modelo). Decisión inmediata.",
                15, 30, "15 a 30 segundos", BLUE_LIGHT),
               ("Media", "Sin SKU exacto. Exige revisar características técnicas y "
                "marcas mixtas.", 30, 60, "30 a 60 segundos", YELLOW),
               ("Alta", "Ambigüedad semántica, descripción incompleta o idioma local. "
                "Exige comparar imágenes.", 60, 120, "60 a 120 segundos", RED)]
    ax0 = 96 + 230
    axw = lw - 230 - 48
    rh = 176
    for k, (niv, cond, a, b, rot, col) in enumerate(niveles):
        ry = y0 + 76 + k * rh
        tag(s, 128, ry + 8, niv, fill=col, color=DARK if col == YELLOW else PAPER, size=18,
            h=38)
        text(s, ax0, ry, axw, 64, cond, size=23, font=FONT_TXT, line_spacing=1.25)
        by = ry + 82
        rect(s, ax0, by, axw, 30, fill=CHIP)
        x_a, x_b = ax0 + axw * a / 120, ax0 + axw * b / 120
        registrar_barra(s, x_a, by, x_b - x_a, 30, 1.0, col)
        r_ = rect(s, x_a, by, x_b - x_a, 30, fill=col)
        animar(s, r_, "wipe", delay_ms=200 + k * 200, dur_ms=700)
        text(s, x_b + 12 if b < 100 else x_a - 312, by - 2, 300, 34, rot, size=24, bold=True,
             font=FONT_HEAD, align="left" if b < 100 else "right",
             color="#0B5EA8" if col != RED else RED)
        if k < 2:
            rect(s, 128, ry + rh - 18, lw - 64, 1, fill="#E3EAF3")
    # eje
    ey = y0 + 76 + 3 * rh + 6
    rect(s, ax0, ey, axw, 2, fill="#9FB4CC")
    for t in (0, 30, 60, 90, 120):
        xt = ax0 + axw * t / 120
        rect(s, xt - 1, ey - 6, 2, 14, fill="#9FB4CC")
        text(s, xt - 40, ey + 12, 80, 28, f"{t} s", size=20, font=FONT_TXT, color=MUTED,
             align="center")
    # --- capacidad operativa
    rx, rw = 96 + lw + 32, 1728 - lw - 32
    card(s, rx, y0, rw, h, accent=YELLOW)
    label(s, rx + 32, y0 + 26, rw - 64, "Capacidad operativa manual", size=18, color=YELLOW)
    text(s, rx + 32, y0 + 54, rw - 64, 34, "Equipo de Product Matching · valor actual (AS-IS)",
         size=21, font=FONT_TXT, color=MUTED)
    filas = [("440 productos", "Cuota de validación diaria por analista"),
             ("~ 65 segundos", "Tiempo promedio por producto"),
             ("10 operadores", "Analistas por turno")]
    for k, (v, et) in enumerate(filas):
        yy = y0 + 112 + k * 132
        t = text(s, rx + 32, yy, rw - 64, 58, v, size=44, bold=True, font=FONT_HEAD,
                 color="#0B5EA8")
        animar(s, t, "fade", delay_ms=300 + k * 180)
        text(s, rx + 32, yy + 60, rw - 64, 32, et, size=22, font=FONT_TXT, color=MUTED)
        rect(s, rx + 32, yy + 112, rw - 64, 1, fill="#E3EAF3")
    # total
    ty = 1010 - 186
    rect(s, rx + 24, ty, rw - 48, 162, fill=YELLOW)
    label(s, rx + 48, ty + 18, rw - 96, "Capacidad total del equipo", size=17, color=DARK)
    t = text(s, rx + 48, ty + 48, rw - 96, 62, "4.400 productos / día", size=42, bold=True,
             font=FONT_HEAD, color=DARK)
    animar(s, t, "zoom", delay_ms=900, dur_ms=500)
    text(s, rx + 48, ty + 112, rw - 96, 34, "440 productos × 10 operadores", size=22,
         font=FONT_TXT, color=DARK)
    notes(s, nota)
    return s


# ------------------------------------------------------------ 36 columnas por rol
def p_columnas(prs, nota):
    """Lámina 43 original: las 36 columnas agrupadas por rol (OE2)."""
    from componentes import chip

    s = add_slide(prs, bg_image=FONDO)
    subencabezado(s, "OE2 · Organizar el conjunto de datos · Identificar atributos",
                  "Las 36 columnas, agrupadas por rol")
    texto = {"Brand", "ManufacturerProductName", "ExtraInfo", "ManufacturerProductDescription",
             "ManufacturerProductId", "RetailerProductName", "RetailerProductId"}
    filtro = {"Invalid", "IsDeleted", "MatchConfidence"}
    grupos = [
        ("Lado fabricante · producto oficial",
         ["Manufacturer", "Brand", "ManufacturerProductId", "ManufacturerProductName",
          "ManufacturerProductDescription", "ManufacturerProductUrl",
          "ManufacturerProductImageUrl", "ExtraInfo"], YELLOW),
        ("Lado retailer · publicación",
         ["Retailer", "RetailerProductName", "RetailerProductId", "RetailerProductUrl",
          "RetailerProductImageUrl", "Stock", "Price"], YELLOW),
        ("Trazabilidad / snapshot",
         ["source_year", "source_month", "source_file", "MappingId", "CreatedDate"], BLUE_LIGHT),
        ("Geografía", ["ManufacturerProductMappingCountry"], BLUE_LIGHT),
        ("Calidad del match", ["Invalid", "IsDeleted", "MatchConfidence", "LinkIsValid"],
         BLUE_LIGHT),
    ]
    y0 = CONTENT_TOP + 4
    gap = 28
    cajas = [(96, y0, 850, 380), (96 + 850 + gap, y0, 1728 - 850 - gap, 380),
             (96, y0 + 380 + gap, 560, 266), (96 + 560 + gap, y0 + 380 + gap, 520, 266),
             (96 + 560 + 520 + 2 * gap, y0 + 380 + gap, 1728 - 1080 - 2 * gap, 266)]
    for k, ((nom, cols, acc), (x, y, w, h)) in enumerate(zip(grupos, cajas)):
        card(s, x, y, w, h, accent=acc)
        text(s, x + 28, y + 24, w - 56, 40, nom, size=28, bold=True, font=FONT_HEAD)
        if acc == YELLOW:
            tw = text_width("TEXTO QUE LEE EL MODELO", 14, FONT_HEAD, True, 1.2) + 34
            tag(s, x + w - 28 - tw, y + 28, "Texto que lee el modelo", size=14, h=28)
        cx, cy = x + 28, y + 84
        for c in cols:
            cw_ = text_width(c, 20, "Roboto Mono") + 28
            if cx + cw_ > x + w - 24:
                cx, cy = x + 28, cy + 50
            if c in texto:
                chip(s, cx, cy, c, size=20, color=DARK, fill="#FFE680", border=YELLOW)
            elif c in filtro:
                chip(s, cx, cy, c, size=20, color="#0B5EA8", fill="#E6EEF8", border=BLUE_LIGHT)
            else:
                chip(s, cx, cy, c, size=20, color=MUTED, fill="#F4F7FB", border="#C3D2E3")
            cx += cw_ + 12
    # leyenda
    ly = 1010 - 40
    lx = 96
    for etq, fill, border in (("Campo textual del modelo (7)", "#FFE680", YELLOW),
                              ("Filtro base de calidad (3)", "#E6EEF8", BLUE_LIGHT),
                              ("Contexto y trazabilidad", "#F4F7FB", "#C3D2E3")):
        rect(s, lx, ly + 6, 26, 22, fill=fill, line=border, line_w=1.5, radius=4)
        text(s, lx + 36, ly, 420, 34, etq, size=21, font=FONT_TXT, color=MUTED,
             anchor="middle")
        lx += text_width(etq, 21, FONT_TXT) + 90
    notes(s, nota)
    return s


# --------------------------------------------------------------- orden del autor
def construir(prs, n):
    """Láminas 35-45 en el orden que dejó el autor en Canva (versión de 69 láminas)."""
    import json

    from theme import ASSETS as A

    ruta = Path(__file__).resolve().parent / "diagramas_autor.json"
    dg = json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else {}

    def diagrama(nota, clave, eyebrow, titulo, respaldo=None):
        p_diagrama(prs, nota, clave, OE1 + " · " + eyebrow, titulo, respaldo=respaldo,
                   aspecto=dg.get(clave, {}).get("aspecto", 1.6))

    p_escala(prs, n[35])
    p_crisp(prs, n[36])
    p_agiles(prs, n[37])
    p_actores(prs, n[38])
    diagrama(n[39], "flujo", "Criterio de clasificación",
             "Diagrama de flujo lógico para la clasificación operativa de productos",
             A / "marco-practico" / "ob_1.png")
    diagrama(n[40], "asis_1", "BPMN AS-IS · parte 1 de 2",
             "Representación del proceso actual mediante diagrama BPMN AS-IS")
    diagrama(n[40], "asis_2", "BPMN AS-IS · parte 2 de 2",
             "Representación del proceso actual mediante diagrama BPMN AS-IS")
    diagrama(n[41], "tobe", "BPMN propuesto",
             "Representación del proceso propuesto mediante diagrama BPMN")
    diagrama(n[40], "subproceso", "Subproceso del modelo",
             "Subproceso: determinación automática del estado de la publicación")
    p_tiempos(prs, n[42])
    p_columnas(prs, n[43])
