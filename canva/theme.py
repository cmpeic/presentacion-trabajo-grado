"""Identidad visual comun de la version Canva (estilo de la imagen de referencia)."""

from pathlib import Path

import pptx_kit
from pptx_kit import FONT_HEAD, corners, image, image_fit, line, rect, text

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
CANVA = Path(__file__).resolve().parent
FONDO = str(CANVA / "fondo.png")
LOGO_BLANCO = str(ASSETS / "logo_carrera_sistemas_blanco.png")
LOGO_AZUL = str(ASSETS / "logo_carrera_sistemas_azul.png")
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


def logo(slide, path: str, x: float, y: float, h: float, align: str = "left", name=None):
    """Logo recortado a su contenido, con alto fijo y alineado a la izquierda o derecha."""
    from PIL import Image

    real = pptx_kit._optimized(str(path), trim=True)
    iw, ih = Image.open(real).size
    w = h * iw / ih
    if align == "right":
        x -= w
    elif align == "center":
        x -= w / 2
    image(slide, path, x, y, w, h, name=name, trim=True)
    return w


def _ancho(s: str, size: float, spacing: float) -> float:
    from componentes import text_width
    return text_width(s, size, FONT_HEAD, True, spacing)


def rotulo_central(slide, s: str, cy: float, size=30, spacing=4.0, color=None, pad=44,
                   regla=1.5):
    """Rotulo centrado entre dos filetes dorados (como «TRABAJO DE GRADO» de la portada)."""
    color = color or pptx_kit.TINTA
    tw = _ancho(s, size, spacing)
    w = tw + 2 * pad
    x = (1920 - w) / 2
    h = size * 1.5
    rect(slide, x, cy - h / 2 - 8, w, regla, fill=pptx_kit.ORO_LINEA, name="Filete superior")
    rect(slide, x, cy + h / 2 + 6, w, regla, fill=pptx_kit.ORO_LINEA, name="Filete inferior")
    text(slide, x - 40, cy - h / 2, w + 80, h, s, size=size, bold=True, font=FONT_HEAD,
         color=color, align="center", anchor="middle", spacing=spacing, wrap=False,
         name="Seccion")


def pie(slide) -> None:
    """Banda inferior con los colores de la EMI y numero de lamina."""
    rect(slide, 0, 1070, 1920, 10, fill=BLUE, name="Banda azul")
    rect(slide, 0, 1070, 360, 10, fill=YELLOW, name="Banda amarilla")
    n = getattr(slide, "_num", None)
    if n:
        text(slide, 1824 - 120, 1030, 120, 28, f"{n:02d}", size=18, bold=True, font=FONT_HEAD,
             color=pptx_kit.TINTA_2, align="right", anchor="middle", name="Numero")


def header(slide, title: str, logo_on: bool = True) -> None:
    """Encabezado: logo EMI a la izquierda, logo de la carrera a la derecha y la seccion
    centrada entre filetes dorados; filete gris debajo y banda EMI al pie."""
    if pptx_kit.TEMA == "claro":
        logo(slide, LOGO_EMI, MARGIN, 30, 82, name="Logo EMI")
        logo(slide, LOGO_AZUL, 1920 - MARGIN, 38, 66, align="right", name="Logo carrera")
        rotulo_central(slide, title.upper(), 72, size=28 if len(title) < 34 else 24)
        rect(slide, MARGIN, 138, 1920 - 2 * MARGIN, 1.5, fill="#D6E1EE", name="Filete")
        pie(slide)
        return
    rect(slide, MARGIN, 80, 18, 18, fill=YELLOW, name="Marca titulo")
    text(slide, MARGIN + 34, 62, 1330, 56, title.upper(), size=44, bold=True,
         font=FONT_HEAD, anchor="middle", name="Titulo")
    rect(slide, MARGIN, 140, 1920 - 2 * MARGIN, 2, fill=BLUE_LIGHT, fill_alpha=0.35,
         name="Filete")
    if logo_on:
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
