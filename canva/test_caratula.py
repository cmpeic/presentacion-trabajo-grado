"""Prueba de importacion: caratula en PPTX y en HTML estatico."""
import sys
sys.path.insert(0, ".")
from pptx_kit import *

A = "../assets/"
prs = new_presentation()
s = add_slide(prs, bg_image="fondo.png")
# Logos
rect(s, 96, 80, 400, 196, fill="#FFFFFF", radius=18)
image_fit(s, A + "logo_universidad.png", 112, 92, 368, 172)
image_fit(s, A + "logo_carrera_sistemas_blanco.png", 548, 128, 300, 104)
# Etiqueta
corners(s, 150, 360, 470, 74, size=22, width=3)
text(s, 150, 360, 470, 74, "TRABAJO DE GRADO", size=26, color="#FFD21F", bold=True,
     font=FONT_HEAD, align="center", anchor="middle", spacing=4)
# Titulo
text(s, 150, 470, 1130, 260,
     "Modelo de Procesamiento de Lenguaje Natural en la validación de correspondencia de productos del ecosistema Philips",
     size=56, bold=True, font=FONT_HEAD, line_spacing=1.12)
text(s, 150, 770, 1130, 50, "Caso de estudio: área de Agilsoft SRL.", size=30, color="#4F9BFF", bold=True)
line(s, 150, 900, 1770, 900, "#6D8FB2", 1.5, alpha=0.45)
text(s, 150, 930, 1000, 60, "Est. Cañez Larico Pablo Enrique", size=40, bold=True, font=FONT_HEAD)
text(s, 1170, 942, 600, 40, "Tutor: Ing. Víctor Rodríguez Estévez", size=26, color="#9FB4CC", align="right")
# Circulo con red neuronal
for (x1, y1, x2, y2) in [(1220, 250, 1330, 470), (1220, 250, 1520, 150), (1520, 150, 1780, 330),
                         (1780, 330, 1870, 600), (1330, 470, 1300, 760), (1300, 760, 1560, 840)]:
    line(s, x1, y1, x2, y2, "#2F7BFF", 1.5, alpha=0.45)
for (cx, cy) in [(1220, 250), (1520, 150), (1780, 330), (1870, 600), (1330, 470), (1300, 760), (1560, 840)]:
    ellipse(s, cx, cy, 6, fill="#4F9BFF")
ellipse(s, 1560, 480, 250, fill=None, line="#0B5EA8", line_w=2, line_alpha=0.5)
ellipse(s, 1560, 480, 205, fill="#0D2748", line="#2F7BFF", line_w=5)
image_fit(s, A + "introduccion/int_3.png", 1415, 335, 290, 290)
notes(s, "Prueba de importación de la carátula.")
prs.save("test_caratula.pptx")
print("pptx ok")
