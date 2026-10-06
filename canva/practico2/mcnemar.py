"""Lámina agregada por el autor: contrastación estadística de la calidad (McNemar exacta).

Cifras del autor (ver cifras_autor.md), verificadas con la prueba binomial exacta:
tabla 106 / 3 / 50 / 2 sobre 161 pares comunes, 53 discordancias, p = 5,52 × 10⁻¹².
"""

from pptx_kit import add_slide, notes, rect, text
from theme import FONDO, MUTED, PAPER, YELLOW
from componentes import (BLUE_LIGHT, CHIP, CONTENT_TOP, DARK, FONT_HEAD, FONT_TXT, PANEL,
                         PANEL_2, bar, card, ecuacion, label, subencabezado, tag, text_width)

NOTA = ("Para contrastar estadísticamente la calidad del matching se aplicó la prueba exacta "
        "de McNemar, bilateral, sobre los 161 pares comunes. La hipótesis nula dice que TF-IDF "
        "y el Transformer tienen la misma probabilidad de acierto. Lo que decide son las 53 "
        "discordancias: en 50 acierta solo el Transformer y en 3 solo TF-IDF. El estadístico "
        "exacto es T igual a 3 y el valor p bilateral es 5,52 por diez a la menos doce, muy por "
        "debajo de 0,05. Se rechaza la hipótesis nula: la diferencia favorece al Transformer, que "
        "sube la exactitud de 67,70 % a 96,89 %, una mejora de 29,19 puntos porcentuales.")


def p_mcnemar(prs, notas=None):
    s = add_slide(prs, bg_image=FONDO)
    subencabezado(s, "OE6 · Contrastación de la hipótesis · Prueba de McNemar",
                  "Contrastación estadística de la calidad del matching")
    y0 = CONTENT_TOP + 12

    # ------------------------------------------------ prueba e hipótesis (izq.)
    lx, lw, lh = 96, 700, 310
    ly = y0 + 30
    card(s, lx, ly, lw, lh, accent=YELLOW)
    label(s, lx + 32, ly + 22, lw - 64, "Prueba", size=18, color=YELLOW)
    text(s, lx + 32, ly + 50, lw - 64, 44, "McNemar exacta bilateral", size=32, bold=True,
         font=FONT_HEAD)
    text(s, lx + 32, ly + 94, lw - 64, 34, "sobre 161 pares comunes · Transformer = Modelo 3",
         size=23, font=FONT_TXT, color=MUTED)
    hip = [("H₀c", "TF-IDF y Transformer tienen la misma probabilidad de acierto.", BLUE_LIGHT,
            PAPER),
           ("H₁c", "Sus probabilidades de acierto son diferentes.", YELLOW, DARK)]
    for k, (h, t, col, tcol) in enumerate(hip):
        yy = ly + 142 + k * 84
        rect(s, lx + 32, yy, lw - 64, 72, fill=PANEL_2, line=col, line_w=1.5, line_alpha=0.6)
        rect(s, lx + 32, yy, 84, 72, fill=col)
        text(s, lx + 32, yy, 84, 72, h, size=26, bold=True, font=FONT_HEAD, color=tcol,
             align="center", anchor="middle")
        text(s, lx + 136, yy, lw - 64 - 120, 72, t, size=23, font=FONT_TXT, anchor="middle",
             line_spacing=1.2)

    # ------------------------------------------------ tabla de contingencia (der.)
    mx, mw = 836, 1824 - 836
    label(s, mx, y0 - 4, mw, "Resultado sobre los 161 pares", size=18, color=YELLOW)
    cx0, cw0, cw, hh, rh = mx, 300, (mw - 300) / 2, 62, 124
    ty = y0 + 30
    for j, t in enumerate(["Transformer correcto", "Transformer incorrecto"]):
        x = cx0 + cw0 + j * cw
        rect(s, x, ty, cw, hh, fill="#0B5EA8", line=BLUE_LIGHT, line_w=1, line_alpha=0.5)
        text(s, x, ty, cw, hh, t, size=22, bold=True, font=FONT_HEAD, align="center",
             anchor="middle")
    celdas = [("TF-IDF correcto", [("106", None), ("3", "b")]),
              ("TF-IDF incorrecto", [("50", "c"), ("2", None)])]
    for i, (fila, vals) in enumerate(celdas):
        y = ty + hh + i * rh
        rect(s, cx0, y, cw0, rh, fill="#0B5EA8", fill_alpha=0.55, line=BLUE_LIGHT, line_w=1,
             line_alpha=0.5)
        text(s, cx0 + 24, y, cw0 - 40, rh, fila, size=24, bold=True, font=FONT_HEAD,
             anchor="middle")
        for j, (v, letra) in enumerate(vals):
            x = cx0 + cw0 + j * cw
            disc = letra is not None
            fuerte = letra == "c"
            rect(s, x, y, cw, rh, fill=CHIP if disc else PANEL,
                 line=YELLOW if disc else BLUE_LIGHT, line_w=3 if disc else 1,
                 line_alpha=1 if disc else 0.5)
            text(s, x, y, cw, rh, v, size=64 if fuerte else 54, bold=True, font=FONT_HEAD,
                 color=YELLOW if fuerte else (PAPER if disc else MUTED), align="center",
                 anchor="middle")
            if disc:
                rect(s, x + cw - 56, y + 12, 40, 36, fill=YELLOW, radius=4)
                text(s, x + cw - 56, y + 12, 40, 36, letra, size=24, bold=True, font=FONT_TXT,
                     color=DARK, align="center", anchor="middle", italic=True)
    text(s, mx, ty + hh + 2 * rh + 12, mw, 30,
         "Las celdas b y c son las discordancias: solo uno de los dos modelos acierta.",
         size=20, font=FONT_TXT, color=MUTED)

    # ------------------------------------------------ resultados (abajo)
    ry, rh2, gap = ly + lh + 58, 196, 24
    rw = (1728 - 3 * gap) / 4
    tiles = ["Estadístico exacto", "Valor p bilateral", "Exactitud", "Mejora"]
    for k, t in enumerate(tiles):
        x = 96 + k * (rw + gap)
        card(s, x, ry, rw, rh2, accent=YELLOW if k == 3 else BLUE_LIGHT)
        label(s, x + 26, ry + 22, rw - 52, t, size=18, color=YELLOW)
    # 1. estadístico
    x = 96
    ecuacion(s, x + 26, ry + 104, [("var", "T"), "=", "min(b, c)\u00a0", "=", ("res", "3")], size=32)
    text(s, x + 26, ry + 150, rw - 52, 34, "con 53 discordancias", size=22, font=FONT_TXT,
         color=MUTED)
    # 2. valor p
    x = 96 + (rw + gap)
    ecuacion(s, x + 26, ry + 104, [("var", "p"), "=", ("sup", "5,52 × 10", "−12"), "<", "0,05"],
             size=30)
    text(s, x + 26, ry + 150, rw - 52, 34, "diferencia significativa", size=22,
         font=FONT_TXT, color=MUTED)
    # 3. exactitud con barras
    x = 96 + 2 * (rw + gap)
    for j, (mod, val, frac, col) in enumerate([("TF-IDF", "67,70%", 0.6770, BLUE_LIGHT),
                                                ("Transformer", "96,89%", 0.9689, YELLOW)]):
        yy = ry + 64 + j * 66
        text(s, x + 26, yy, 200, 28, mod, size=20, bold=True, font=FONT_TXT, color=PAPER)
        text(s, x + rw - 26 - 130, yy, 130, 28, val, size=22, bold=True, font=FONT_HEAD,
             color=col, align="right")
        bar(s, x + 26, yy + 34, rw - 52, 14, frac, color=col)
    # 4. mejora
    x = 96 + 3 * (rw + gap)
    text(s, x + 26, ry + 58, rw - 52, 80, "29,19", size=66, bold=True, font=FONT_HEAD,
         color=YELLOW)
    text(s, x + 26, ry + 146, rw - 52, 34, "puntos porcentuales", size=22, font=FONT_TXT,
         color=MUTED)

    # ------------------------------------------------ decisión
    dy = ry + rh2 + 22
    dh = 1010 - dy
    rect(s, 96, dy, 1728, dh, fill=YELLOW)
    ecuacion(s, 96, dy + dh / 2, [("var", "p"), "=", ("sup", "5,52 × 10", "−12"), "<", "0,05"],
             size=28, color=DARK, res_color=DARK, align="right", w=1728 - 32)
    w_tag = text_width("DECISIÓN", 20, FONT_HEAD, True, 2) + 40
    text(s, 96 + 28, dy, w_tag, dh, "DECISIÓN", size=20, bold=True, font=FONT_HEAD, color=DARK,
         spacing=2, anchor="middle")
    text(s, 96 + 28 + w_tag + 10, dy, 1728 - w_tag - 80, dh,
         "Se rechaza H₀c: la diferencia favorece al Transformer.", size=26, bold=True,
         font=FONT_HEAD, color=DARK, anchor="middle")
    notes(s, NOTA)


def construir(prs, notas=None):
    p_mcnemar(prs, notas)
