"""Identidad visual comun de la version Canva (estilo de la imagen de referencia)."""

from pathlib import Path

from pptx_kit import FONT_HEAD, corners, image_fit, line, rect, text

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
CANVA = Path(__file__).resolve().parent
FONDO = str(CANVA / "fondo.png")
LOGO_BLANCO = str(ASSETS / "logo_carrera_sistemas_blanco.png")
LOGO_EMI = str(ASSETS / "logo_universidad.png")

BG = "#07172D"
SURFACE = "#0D2748"
PANEL = "#0A1F3D"
PAPER = "#F3F7FC"
BLUE = "#0B5EA8"
BLUE_LIGHT = "#2F7BFF"
BLUE_TEXT = "#4F9BFF"
YELLOW = "#FFD21F"
LINE = "#6D8FB2"
MUTED = "#9FB4CC"

MARGIN = 96


def header(slide, title: str, logo: bool = True) -> None:
    """Encabezado: cuadro amarillo + titulo en mayusculas + filete + logo."""
    rect(slide, MARGIN, 80, 18, 18, fill=YELLOW, name="Marca titulo")
    text(slide, MARGIN + 34, 62, 1330, 56, title.upper(), size=44, bold=True,
         font=FONT_HEAD, anchor="middle", name="Titulo")
    rect(slide, MARGIN, 140, 1920 - 2 * MARGIN, 2, fill=BLUE_LIGHT, fill_alpha=0.35,
         name="Filete")
    if logo:
        image_fit(slide, LOGO_BLANCO, 1920 - MARGIN - 230, 58, 230, 70, name="Logo carrera")


def panel(slide, x, y, w, h, fill=PANEL, border=BLUE_LIGHT, border_alpha=0.45,
          brackets=True, bracket_color=YELLOW, bracket_size=34, radius=None):
    """Panel oscuro con borde azul fino y esquineros amarillos."""
    rect(slide, x, y, w, h, fill=fill, line=border, line_w=1.5, line_alpha=border_alpha,
         radius=radius)
    if brackets:
        corners(slide, x - 10, y - 10, w + 20, h + 20, size=bracket_size,
                color=bracket_color, width=3)


def badge(slide, x, y, label: str, size=40, fill=YELLOW, color="#07172D"):
    rect(slide, x, y, size, size * 0.72, fill=fill)
    text(slide, x, y, size, size * 0.72, label, size=size * 0.36, bold=True,
         font=FONT_HEAD, color=color, align="center", anchor="middle", wrap=False)
