"""Grupo g6: OE6 · contraste con el proceso manual, contrastación de la hipótesis y cierre
(P19-P23, láminas originales 82-90)."""

import re

from pptx_kit import add_slide, corners, ellipse, image_fit, line, notes, rect, text
from theme import (ASSETS, BLUE_TEXT, FONDO, LINE, LOGO_BLANCO, LOGO_EMI, MARGIN, MUTED,
                   PAPER, SURFACE, YELLOW)
from componentes import (BLUE_LIGHT, CHIP, CONTENT_TOP, DARK, FONT_HEAD, FONT_TXT, PANEL_2,
                         RED, card, chip, ecuacion, flecha, label,
                         medida_ecuacion, numbadge, subencabezado, tag, text_width)

OE6 = "OE6 · Contrastar con el proceso manual"
HIP = "OE6 · Contrastación de la hipótesis"
MAQUINA = LINE          # tiempo de máquina: dato neutro, distinto del trabajo humano
EQ = " ="               # signo igual con aire tras un subíndice


# ---------------------------------------------------------------- utilidades
def _frases(s):
    return [f for f in re.split(r"(?<=\.)\s+", s.strip()) if f]


def _cabecera(s, x, y, w, n, titulo, sub=None, color=YELLOW, size=28):
    """Número + título de tarjeta (Montserrat) + subtítulo (Barlow)."""
    numbadge(s, x, y, n, size=40, fill=color,
             color=DARK if color in (YELLOW, MAQUINA) else PAPER)
    text(s, x + 58, y - 2, w - 58, 40, titulo, size=size, bold=True, font=FONT_HEAD,
         anchor="middle")
    if sub:
        text(s, x + 58, y + 40, w - 58, 30, sub, size=20, font=FONT_TXT, color=MUTED)


def _eq_fit(partes, maxw, size):
    """Tamaño de ecuación que cabe en maxw (sin bajar de 24 px)."""
    while size > 24 and medida_ecuacion(partes, size)[0] > maxw:
        size -= 1
    return size


def _eq_centro(s, x, w, cy, partes, size, res_color=YELLOW):
    """Ecuación centrada horizontalmente en [x, x+w] con su eje en cy."""
    size = _eq_fit(partes, w, size)
    ecuacion(s, x, cy, partes, size=size, align="center", w=w, res_color=res_color)
    return size


def _derivacion(s, x, w, ay1, lhs, rhs, resultado, esz=32, bsize=60, color=YELLOW,
                gap=22):
    """Ecuación en dos líneas: «lhs = rhs» y debajo «= resultado» en grande, con los
    signos igual alineados. Devuelve la y inferior del bloque."""
    sp = esz * 0.18
    e2 = esz * 1.5                      # signo igual de la segunda línea, más visible
    wl = medida_ecuacion(lhs, esz)[0]
    weq = medida_ecuacion([EQ], esz)[0]
    weq2 = medida_ecuacion(["="], e2)[0]
    wr, up, dn = medida_ecuacion(rhs, esz)
    bw = text_width(resultado, bsize, FONT_HEAD, True) + 8
    x_eq = wl + sp + weq - medida_ecuacion(["="], esz)[0]   # x del signo «=» en la línea 1
    tot = max(wl + sp + weq + sp + wr, x_eq + weq2 + sp * 1.5 + bw)
    x0 = x + max(0, (w - tot) / 2)
    ecuacion(s, x0, ay1, lhs + [EQ] + rhs, size=esz)
    ay2 = ay1 + dn + gap + bsize * 0.62
    ecuacion(s, x0 + x_eq - 2, ay2, ["="], size=e2)
    text(s, x0 + x_eq + weq2 + sp * 1.5, ay2 - bsize * 0.72, bw, bsize * 1.44, resultado,
         size=bsize, bold=True, font=FONT_HEAD, color=color, anchor="middle", wrap=False)
    return ay2 + bsize * 0.62


def _alto_derivacion(rhs, esz=32, bsize=60, gap=22):
    _, up, dn = medida_ecuacion(rhs, esz)
    return up + dn + gap + bsize * 1.24


def _segmento(s, x, y, w, h, color, rotulo=None, rcolor=DARK, size=20, dash=False):
    """Segmento de barra con rótulo centrado (solo si cabe)."""
    if dash:
        rect(s, x, y, w, h, fill=None, line=color, line_w=2, dash="dash")
    else:
        rect(s, x, y, w, h, fill=color)
    if rotulo and text_width(rotulo, size, FONT_HEAD, True) + 24 <= w:
        text(s, x, y, w, h, rotulo, size=size, bold=True, font=FONT_HEAD, color=rcolor,
             align="center", anchor="middle")


def _tile(s, x, y, w, h, rotulo, valor, color=PAPER, vsize=30):
    """Mosaico pequeño: rótulo en mayúsculas + cifra."""
    rect(s, x, y, w, h, fill=CHIP, line=BLUE_LIGHT, line_w=1, line_alpha=0.3)
    label(s, x + 18, y + 14, w - 36, rotulo, size=18, color=MUTED, spacing=1.2)
    text(s, x + 18, y + 42, w - 36, vsize * 1.3, valor, size=vsize, bold=True,
         font=FONT_HEAD, color=color)


# ------------------------------------------------------------------- P19
def p19(prs, notas):
    """Láminas 82 + 83 + 87 (tiempos): línea base manual frente a la latencia del modelo."""
    s = add_slide(prs, bg_image=FONDO)
    subencabezado(s, OE6 + " · Tiempo de validación",
                  "Tiempo unitario: manual frente al modelo")
    y0, ch, gap = CONTENT_TOP + 8, 336, 32
    cw = (1728 - gap) / 2
    xa, xb = 96, 96 + cw + gap
    pad = 32
    iw = cw - 2 * pad

    # --- tarjeta 1: línea base manual ---------------------------------------
    card(s, xa, y0, cw, ch, accent=BLUE_LIGHT)
    _cabecera(s, xa + pad, y0 + 30, iw, "1", "Línea base manual",
              "2 semanas operativas · unidad: publicación-semana", color=BLUE_LIGHT)
    eq = [("sub", "t", "manual"), EQ,
          ("frac", ["27.120 + 35.460"], ["1.826 + 1.942"]), "=",
          ("frac", ["62.580"], ["3.768"]), "=", ("res", "16,608 s")]
    _eq_centro(s, xa + pad, iw, y0 + 174, eq, 36)
    tw = (iw - 20) / 2
    ty = y0 + ch - 108
    _tile(s, xa + pad, ty, tw, 84, "Semana 24–27 ago", "14,852 s", vsize=28)
    _tile(s, xa + pad + tw + 20, ty, tw, 84, "Semana 31 ago–3 sep", "18,260 s", vsize=28)

    # --- tarjeta 2: latencia del sistema v7.5 --------------------------------
    card(s, xb, y0, cw, ch, accent=YELLOW)
    _cabecera(s, xb + pad, y0 + 30, iw, "2", "Latencia del sistema v7.5",
              "corrida completa · unidad: consulta")
    eq = [("sub", "t", "modelo"), EQ, ("frac", ["15.411,8"], ["2.365"]), "=",
          ("res", "6,5166 s")]
    _eq_centro(s, xb + pad, iw, y0 + 174, eq, 36)
    tw3 = (iw - 40) / 3
    for k, (r, v) in enumerate([("Consultas", "2.365"), ("Ejecución", "15.411,8 s"),
                                ("Máquina", "4,28 h")]):
        _tile(s, xb + pad + k * (tw3 + 20), ty, tw3, 84, r, v, vsize=28)

    # --- panel focal: comparación unitaria (síntesis de las dos tarjetas) -------
    by = y0 + ch + 36
    bh = 1010 - by
    card(s, 96, by, 1728, bh, accent=None, brackets=True)
    label(s, 128, by + 26, 900, "Comparación unitaria · a escala", size=18, color=YELLOW)
    xn, xbar, wbar, xv = 128, 340, 560, 924
    r1, r2, rh = by + 102, by + 214, 60
    frac = 6.5166 / 16.608
    for yy, nombre in ((r1, "Manual"), (r2, "Modelo v7.5")):
        text(s, xn, yy, 200, rh, nombre, size=26, bold=True, font=FONT_HEAD, anchor="middle")
    rect(s, xbar, r1, wbar, rh, fill=BLUE_LIGHT)
    text(s, xv, r1, 210, rh, "16,608 s", size=34, bold=True, font=FONT_HEAD, anchor="middle")
    rect(s, xbar, r2, wbar * frac, rh, fill=YELLOW)
    _segmento(s, xbar + wbar * frac + 6, r2, wbar * (1 - frac) - 6, rh, YELLOW,
              "−10,092 s", rcolor=YELLOW, size=26, dash=True)
    text(s, xv, r2, 210, rh, "6,5166 s", size=34, bold=True, font=FONT_HEAD, color=YELLOW,
         anchor="middle")
    text(s, xbar + wbar * frac + 6, r2 + rh + 10, wbar * (1 - frac) - 6, 30,
         "diferencia unitaria", size=20, font=FONT_TXT, color=MUTED, align="center")
    # guía: fin de la barra manual
    rect(s, xbar + wbar - 1.5, r1 + rh, 3, r2 - r1 - rh, fill=BLUE_LIGHT, fill_alpha=0.5)
    # divisor
    xd = 1160
    rect(s, xd, by + 28, 1.5, bh - 56, fill=BLUE_LIGHT, fill_alpha=0.35)
    # reducción unitaria: derivación con resultado grande
    rx, rw = xd + 36, 1792 - (xd + 36)
    label(s, rx, by + 26, rw, "Reducción unitaria", size=18, color=YELLOW)
    rhs = [("frac", ["16,608 − 6,5166"], ["16,608"]), "× 100"]
    hb = _alto_derivacion(rhs, 34, 72)
    _, up, _ = medida_ecuacion(rhs, 34)
    ay = by + 60 + (bh - 60 - hb) / 2 + up
    _derivacion(s, rx, rw, ay, [("sub", "R", "unitaria")], rhs, "60,76%", esz=34, bsize=72)

    f87 = _frases(notas[87])
    aclaracion = ("La diferencia unitaria de 10,092 segundos se calculó con los promedios "
                  "sin redondear.")
    notes(s, " ".join([notas[82], notas[83], aclaracion] + f87[:2]))


# ------------------------------------------------------------------- P20
def p20(prs, notas):
    """Láminas 84 + 87 (reducciones): escenario operativo asistido."""
    s = add_slide(prs, bg_image=FONDO)
    subencabezado(s, OE6 + " · Escenario asistido",
                  "Escenario operativo asistido · 2.365 publicaciones")
    py, ph = CONTENT_TOP + 8, 412
    card(s, 96, py, 1728, ph, accent=None, brackets=True)
    xn = 128
    xb, wb = 330, 930
    xt, wt = xb + wb + 20, 150
    xs = xt + wt + 26
    xd, wd = xs + 26, 1792 - (xs + 26)
    rh = 52
    # cabeceras de columna
    label(s, xt, py + 24, wt, "Total", size=18, color=MUTED, align="right")
    label(s, xd, py + 24, wd, "Diferencia", size=18, color=YELLOW)
    rect(s, xs, py + 26, 1.5, ph - 52, fill=BLUE_LIGHT, fill_alpha=0.35)

    def fila(y, nombre, segs, total, tcol=PAPER):
        text(s, xn, y, 190, rh, nombre, size=24, bold=True, font=FONT_HEAD, anchor="middle")
        cx = xb
        for (f, col, rot, rcol) in segs:
            _segmento(s, cx, y, wb * f, rh, col, rot, rcolor=rcol)
            cx += wb * f
        text(s, xt, y, wt, rh, total, size=30, bold=True, font=FONT_HEAD, color=tcol,
             align="right", anchor="middle")

    # sección A: casos
    label(s, xn, py + 24, 900, "Casos que revisa el operador", size=18, color=MUTED)
    ya1, ya2 = py + 66, py + 66 + rh + 16
    fila(ya1, "Manual", [(1.0, BLUE_LIGHT, "2.365 casos humanos", DARK)], "2.365")
    fa = 1083 / 2365
    fila(ya2, "Asistido", [(fa, BLUE_LIGHT, "1.083 casos humanos", DARK),
                           (1 - fa, YELLOW, "54,21% cobertura automática", DARK)], "1.083")
    text(s, xd, ya2, wd, rh, "−1.282 casos", size=26, bold=True, font=FONT_HEAD,
         color=YELLOW, anchor="middle")
    # separador
    sy = ya2 + rh + 26
    rect(s, xn, sy, xs - xn - 24, 1, fill=BLUE_LIGHT, fill_alpha=0.25)
    # sección B: horas
    label(s, xn, sy + 18, 900, "Horas del lote", size=18, color=MUTED)
    yb1, yb2 = sy + 60, sy + 60 + rh + 16
    fila(yb1, "Manual", [(1.0, BLUE_LIGHT, "10,91 h humanas", DARK)], "10,91 h")
    fh, fm = 5.00 / 10.91, 4.28 / 10.91
    fila(yb2, "Asistido", [(fh, BLUE_LIGHT, "5,00 h humanas", DARK),
                           (fm, MAQUINA, "+4,28 h de máquina", DARK)], "9,28 h")
    # resto de la pista (ahorro total), rotulado
    _segmento(s, xb + wb * (fh + fm) + 6, yb2, wb * (1 - fh - fm) - 6, rh, YELLOW,
              "−1,63 h", rcolor=YELLOW, size=22, dash=True)
    text(s, xd, yb2 + rh / 2 - 36, wd, 72, ["−5,91 h humanas", "−1,63 h total"], size=26,
         bold=True, font=FONT_HEAD, color=YELLOW, anchor="middle", line_spacing=1.2)

    # --- ecuaciones de reducción -------------------------------------------------
    ey = py + ph + 30
    eh = 1010 - ey
    gap = 24
    ew = (1728 - 2 * gap) / 3
    tarjetas = [
        ("1", "Reducción humana", "horas humanas", YELLOW, ("R", "humana"),
         [("frac", ["10,9114 − 4,9967"], ["10,9114"]), "× 100"], "54,21%"),
        ("2", "Reducción total", "tiempo secuencial", BLUE_LIGHT, ("R", "total"),
         [("frac", ["10,9114 − 9,2778"], ["10,9114"]), "× 100"], "14,97%"),
        ("3", "Tiempo de máquina", "ejecución completa", MAQUINA, ("t", "máquina"),
         [("frac", ["15.411,8 s"], ["3.600"])], "4,28 h"),
    ]
    for k, (n, tit, sub, col, lhs, rhs, res) in enumerate(tarjetas):
        x = 96 + k * (ew + gap)
        card(s, x, ey, ew, eh, accent=col)
        _cabecera(s, x + 28, ey + 28, ew - 56, n, tit, color=col, size=26)
        label(s, x + 28 + 58, ey + 70, ew - 120, sub, size=18, color=MUTED)
        top = ey + 112
        hb = _alto_derivacion(rhs, 32, 56)
        _, up, _ = medida_ecuacion(rhs, 32)
        ay = top + (ey + eh - 16 - top - hb) / 2 + up
        _derivacion(s, x + 24, ew - 48, ay, [("sub",) + lhs], rhs, res, esz=32, bsize=56,
                    color=PAPER if col == MAQUINA else YELLOW)

    f87 = _frases(notas[87])
    notes(s, " ".join([notas[84]] + f87[2:]))


# ------------------------------------------------------------------- P21
def p21(prs, notas):
    """Láminas 85 + 86: consistencia de la calidad en la evaluación, el benchmark y el uso."""
    s = add_slide(prs, bg_image=FONDO)
    subencabezado(s, OE6 + " · Consistencia de la calidad",
                  "Consistencia de la calidad: evaluación, benchmark y uso")
    y0 = CONTENT_TOP + 8
    lx, lw, lh = 96, 1180, 1010 - y0
    card(s, lx, y0, lw, lh, accent=None, brackets=True)
    _cabecera(s, lx + 32, y0 + 28, lw - 64, "1", "Evaluación interna · Modelo 3",
              "161 pares evaluados")
    # --- ecuaciones de las métricas: se miden primero para repartir el ancho ---
    esz = 34
    filas = [
        ("Accuracy", [("frac", ["94 + 62"], ["161"]), "× 100", "=", ("res", "96,89%")], None),
        ("Precisión", [("frac", ["94"], ["94 + 3"]), "× 100", "=", ("res", "96,91%")], None),
        ("Recall", [("frac", ["94"], ["94 + 2"]), "× 100", "=", ("res", "97,92%")], None),
        ("F1-score", ["2 ×", ("frac", ["96,91 × 97,92"], ["96,91 + 97,92"]), "=",
                      ("res", "97,41%")], None),
        ("Error", [("frac", ["3 + 2"], ["161"]), "× 100", "=", ("res", "3,11%")], RED),
    ]
    nw = max(medida_ecuacion([("var", n)], esz)[0] for n, _, _ in filas)
    rw_eq = max(medida_ecuacion(["="] + r, esz)[0] for _, r, _ in filas)
    ex0 = lx + lw - 32 - (nw + esz * 0.18 + rw_eq)

    # --- matriz 2x2 con la orientación de la lámina 59 -------------------------
    # filas = real, columnas = predicho: VP | FN arriba, FP | VN abajo
    rlw, tg = 150, 12                       # ancho de los rótulos de fila, separación
    mx = lx + 32
    cx0 = mx + rlw
    tw = (ex0 - 56 - cx0 - tg) / 2
    th = 156
    gw = 2 * tw + tg
    ctop, cbot = y0 + 120, y0 + lh - 24
    bloque = 27 + 6 + 30 + 12 + 2 * th + tg + 34 + 46 + 28
    by_ = ctop + (cbot - ctop - bloque) / 2
    label(s, cx0, by_, gw, "Predicho", size=18, color=MUTED, align="center")
    rect(s, cx0, by_ + 30, gw, 1.5, fill=BLUE_LIGHT, fill_alpha=0.45)
    hy = by_ + 33
    label(s, mx, hy + 2, rlw - 10, "Real", size=18, color=MUTED)
    for j, cat in enumerate(("Corresponde", "No corresponde")):
        text(s, cx0 + j * (tw + tg), hy, tw, 30, cat, size=20, font=FONT_TXT, color=PAPER,
             align="center", anchor="middle")
    my = hy + 30 + 12
    celdas = [("94", ["verdaderos", "positivos"], YELLOW, "VP"),
              ("2", ["falsos", "negativos"], RED, "FN"),
              ("3", ["falsos", "positivos"], RED, "FP"),
              ("62", ["verdaderos", "negativos"], YELLOW, "VN")]
    for i, cat in enumerate(("Corresponde", "No corresponde")):
        text(s, mx, my + i * (th + tg), rlw - 10, th, cat, size=20, font=FONT_TXT,
             color=PAPER, anchor="middle")
    for k, (v, r, col, ab) in enumerate(celdas):
        x = cx0 + (k % 2) * (tw + tg)
        y = my + (k // 2) * (th + tg)
        rect(s, x, y, tw, th, fill=CHIP, line=col, line_w=1.5, line_alpha=0.6)
        rect(s, x, y, tw, 5, fill=col)
        text(s, x + 18, y + 18, tw - 70, 66, v, size=56, bold=True, font=FONT_HEAD, color=col)
        text(s, x + tw - 58, y + 20, 42, 26, ab, size=18, bold=True, font=FONT_HEAD,
             color=col, align="right", anchor="middle")
        text(s, x + 18, y + 90, tw - 30, 52, r, size=20, font=FONT_TXT, color=PAPER,
             line_spacing=1.15)
    sy = my + 2 * th + tg + 34 + 23
    _eq_centro(s, cx0, gw, sy, ["94 + 62 + 3 + 2", EQ, ("res", "161")], 32)
    label(s, cx0, sy + 30, gw, "pares", size=18, color=MUTED, align="center")

    # --- ecuaciones de las métricas -------------------------------------------
    rect(s, ex0 - 28, y0 + 136, 1.5, lh - 172, fill=BLUE_LIGHT, fill_alpha=0.35)
    xeq = ex0 + nw
    top = y0 + 120
    step = (y0 + lh - 24 - top) / len(filas)
    for k, (nombre, resto, rcol) in enumerate(filas):
        ay = top + step * k + step / 2
        w_n = medida_ecuacion([("var", nombre)], esz)[0]
        ecuacion(s, xeq - w_n, ay, [("var", nombre)], size=esz)
        ecuacion(s, xeq + esz * 0.18, ay, ["="] + resto, size=esz,
                 res_color=rcol or YELLOW)
        if k < len(filas) - 1:
            rect(s, ex0, top + step * (k + 1) - 0.75, lx + lw - 32 - ex0, 1.5,
                 fill=BLUE_LIGHT, fill_alpha=0.22)

    # --- columna derecha: benchmark externo y uso controlado -------------------
    rx = lx + lw + 30
    rw = 1824 - rx
    c1h = 388
    card(s, rx, y0, rw, c1h, accent=BLUE_LIGHT)
    _cabecera(s, rx + 28, y0 + 28, rw - 56, "2", "Benchmark externo · v7.5",
              "2.365 publicaciones · 19 países", color=BLUE_LIGHT, size=26)
    text(s, rx + 28, y0 + 120, rw - 56, 90, "94,54%", size=72, bold=True, font=FONT_HEAD,
         color=YELLOW)
    label(s, rx + 28, y0 + 210, rw - 56, "Coincidencia selectiva", size=18, color=PAPER)
    bx, bwid, byy = rx + 28, rw - 56, y0 + 266
    fr = 70 / 1282
    rect(s, bx, byy, bwid * (1 - fr), 30, fill=YELLOW)
    rect(s, bx + bwid * (1 - fr) + 3, byy, bwid * fr - 3, 30, fill=RED)
    vw = text_width("70 / 1.282", 26, FONT_HEAD, True) + 6
    text(s, bx, byy + 46, vw, 40, "70 / 1.282", size=26, bold=True, font=FONT_HEAD,
         color=RED, anchor="middle", wrap=False)
    text(s, bx + vw + 14, byy + 46, bwid - vw - 14, 40, "desacuerdos automatizados",
         size=21, font=FONT_TXT, color=PAPER, anchor="middle")

    c2y = y0 + c1h + 26
    c2h = 1010 - c2y
    card(s, rx, c2y, rw, c2h, accent=YELLOW)
    _cabecera(s, rx + 28, c2y + 28, rw - 56, "3", "Uso controlado", size=26)
    zy = c2y + 92
    text(s, rx + 28, zy, 120, 130, "0", size=112, bold=True, font=FONT_HEAD,
         color=YELLOW, anchor="middle")
    text(s, rx + 160, zy + 24, rw - 188, 84, ["ERRORES", "REGISTRADOS"], size=26, bold=True,
         font=FONT_HEAD, color=PAPER, anchor="middle", line_spacing=1.2)
    ty_ = c2y + c2h - 66
    tw_ = tag(s, rx + 28, ty_, "Aceptado", size=18, h=38)
    label(s, rx + 28 + tw_ + 16, ty_ + 7, rw - tw_ - 72, "Registro de uso", size=18,
          color=MUTED)
    notes(s, " ".join(notas[i] for i in (85, 86)))


# ------------------------------------------------------------------- P22
def p22(prs, notas):
    """Láminas 88 + 89: matriz de contrastación y veredicto de la hipótesis."""
    s = add_slide(prs, bg_image=FONDO)
    subencabezado(s, HIP + " · Resultado final", "Matriz de contrastación de la hipótesis")
    y0 = CONTENT_TOP + 8
    dhs, dg = (272, 214), 28           # VD₁ lleva además la prueba de McNemar
    vh = sum(dhs) + dg
    # --- VI -----------------------------------------------------------------
    vx, vw = 96, 470
    card(s, vx, y0, vw, vh, accent=YELLOW)
    rect(s, vx + 32, y0 + 34, 70, 44, fill=YELLOW, radius=4)
    text(s, vx + 32, y0 + 34, 70, 44, "VI", size=22, bold=True, font=FONT_HEAD, color=DARK,
         align="center", anchor="middle")
    label(s, vx + 118, y0 + 44, vw - 150, "Variable independiente", size=18, color=MUTED)
    text(s, vx + 32, y0 + 100, vw - 64, 56, "Modelo de PLN", size=40, bold=True,
         font=FONT_HEAD)
    for k, ev in enumerate(["Modelo 3", "Cascada v7.5", "Human in the Loop"]):
        chip(s, vx + 32, y0 + 186 + k * 62, ev, size=24, mono=False, color=PAPER, h=48,
             pad=18)
    tag(s, vx + 32, y0 + vh - 70, "Aplicado", size=18, h=38)

    # --- VD₁ y VD₂ -------------------------------------------------------------
    dx = vx + vw + 110
    dw = 1824 - dx
    vds = [("VD₁", "Consistencia de la calidad", "Mejora",
            [("96,89%", "interna"), ("94,54%", "externa"), ("0", "errores de uso")]),
           ("VD₂", "Tiempo de validación", "Reduce",
            [("6,5166 s", "por consulta"), ("−54,21%", "horas humanas"),
             ("−14,97%", "tiempo total")])]
    centros = []
    for j, (cod, tit, verbo, kpis) in enumerate(vds):
        dh = dhs[j]
        y = y0 + j * (dhs[0] + dg)
        centros.append(y + dh / 2)
        card(s, dx, y, dw, dh, accent=BLUE_LIGHT, accent_side="left")
        rect(s, dx + 32, y + 26, 78, 44, fill=BLUE_LIGHT, radius=4)
        text(s, dx + 32, y + 26, 78, 44, cod, size=22, bold=True, font=FONT_HEAD,
             color=PAPER, align="center", anchor="middle")
        text(s, dx + 128, y + 26, dw - 360, 44, tit, size=30, bold=True, font=FONT_HEAD,
             anchor="middle")
        tw_ = text_width(verbo.upper(), 18, FONT_HEAD, True, 1.2) + 34
        tag(s, dx + dw - 32 - tw_, y + 30, verbo, size=18, h=38)
        kw = (dw - 64) / 3
        for k, (v, r) in enumerate(kpis):
            kx = dx + 32 + k * kw
            if k:
                rect(s, kx - 14, y + 102, 1.5, 88, fill=BLUE_LIGHT, fill_alpha=0.3)
            text(s, kx, y + 94, kw - 28, 60, v, size=46, bold=True, font=FONT_HEAD,
                 color=YELLOW)
            label(s, kx, y + 156, kw - 28, r, size=18, color=PAPER)
        if j == 0:
            # evidencia estadística de VD₁ (lámina de McNemar)
            rect(s, dx + 32, y + 202, dw - 64, 1.5, fill=BLUE_LIGHT, fill_alpha=0.3)
            ay = y + 238
            lw_ = text_width("McNemar exacta:", 24, FONT_TXT) + 8
            text(s, dx + 32, ay - 18, lw_, 36, "McNemar exacta:", size=24, font=FONT_TXT,
                 color=MUTED, anchor="middle", wrap=False)
            ecuacion(s, dx + 32 + lw_ + 6, ay,
                     [("var", "p"), "=", ("sup", "5,52 × 10", "−12"), "<", "0,05"], size=28)
    # conector VI → VD
    cy = y0 + vh / 2
    xm = vx + vw + 46
    rect(s, vx + vw, cy - 2, xm - vx - vw, 4, fill=YELLOW)
    rect(s, xm - 2, centros[0], 4, centros[1] - centros[0], fill=YELLOW)
    for c in centros:
        flecha(s, xm, c, dx - 8, h=28)

    # --- veredicto ------------------------------------------------------------
    ry = y0 + vh + 36
    rh = 1010 - ry
    card(s, 96, ry, 1728, rh, accent=None, brackets=True, fill=PANEL_2)
    bw = 380
    rect(s, 96, ry, bw, rh, fill=YELLOW)
    text(s, 96 + 32, ry, bw - 64, rh, ["Hipótesis", "aceptada"], size=44, bold=True,
         font=FONT_HEAD, color=DARK, anchor="middle", line_spacing=1.1)
    text(s, 96 + bw + 40, ry + 24, 1728 - bw - 80, rh - 48,
         "El modelo de Procesamiento de Lenguaje Natural mejora la consistencia de la "
         "calidad del matching y reduce el tiempo de validación, en comparación con el "
         "proceso manual, en el área de operaciones de Agilsoft SRL.", size=28, bold=True,
         font=FONT_HEAD, anchor="middle", line_spacing=1.3)
    notes(s, " ".join(notas[i] for i in (88, 89)))


# ------------------------------------------------------------------- P23
def p23(prs, notas):
    """Lámina 90: cierre con el estilo de la carátula."""
    s = add_slide(prs, bg_image=FONDO)
    rect(s, MARGIN, 76, 404, 196, fill="#FFFFFF", radius=18, name="Tarjeta logo EMI")
    image_fit(s, str(LOGO_EMI), MARGIN + 18, 90, 368, 168, name="Logo EMI", trim=True)
    image_fit(s, LOGO_BLANCO, 552, 124, 300, 100, name="Logo carrera", trim=True)
    # gracias
    text(s, 140, 330, 1100, 200, "Gracias", size=168, bold=True, font=FONT_HEAD,
         color=YELLOW, name="Gracias")
    rect(s, 150, 548, 300, 8, fill=YELLOW)
    text(s, 150, 600, 1180, 150,
         [["Modelo de Procesamiento de Lenguaje Natural en la validación"],
          ["de correspondencia de productos del ecosistema Philips"]],
         size=34, bold=True, font=FONT_HEAD, line_spacing=1.3, name="Titulo")
    text(s, 150, 736, 1120, 40, "Quedo atento a sus preguntas.", size=30, font=FONT_TXT,
         color=BLUE_TEXT, bold=True)
    rect(s, 150, 884, 1620, 2, fill=LINE, fill_alpha=0.45)
    text(s, 150, 912, 1000, 64, "Est. Cañez Larico Pablo Enrique", size=42, bold=True,
         font=FONT_HEAD, anchor="middle", name="Autor")
    text(s, 1170, 912, 600, 64, "Tutor: Ing. Víctor Rodríguez Estévez", size=28,
         color=MUTED, align="right", anchor="middle", font=FONT_TXT)
    # red neuronal en círculo (como la carátula)
    cx, cy, r = 1636, 480, 182
    nodes = [(1440, 196), (1650, 120), (1856, 270), (1880, 610), (1408, 470), (1438, 760),
             (1700, 818)]
    for a, b in [(0, 4), (0, 1), (1, 2), (2, 3), (4, 5), (5, 6), (3, 6)]:
        line(s, *nodes[a], *nodes[b], color=BLUE_LIGHT, width=1.5, alpha=0.45)
    for (nx, ny) in nodes:
        ellipse(s, nx, ny, 7, fill=BLUE_TEXT)
    ellipse(s, cx, cy, r + 44, line="#0B5EA8", line_w=2, line_alpha=0.55)
    ellipse(s, cx, cy, r, fill=SURFACE, line=BLUE_LIGHT, line_w=5)
    image_fit(s, str(ASSETS / "introduccion/int_3.png"), cx - 120, cy - 120, 240, 240,
              name="Red neuronal", trim=True)
    notes(s, notas[90])


def construir(prs, notas):
    p19(prs, notas)
    p20(prs, notas)
    p21(prs, notas)
    p22(prs, notas)
    p23(prs, notas)
