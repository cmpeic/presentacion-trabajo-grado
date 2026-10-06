"""Componentes de diseño para las láminas rediseñadas (estilo de la referencia).

Todas las medidas en píxeles del lienzo 1920x1080. El ancho de los textos se
mide con las mismas fuentes TTF que usa Canva (Montserrat, Barlow, Roboto Mono),
así las ecuaciones y los chips se arman con posiciones exactas.

Zona de contenido de una lámina del marco práctico: x 96..1824, y 268..1010
(debajo de `subencabezado`).
"""

from __future__ import annotations

import os
from functools import lru_cache

from PIL import ImageFont

from pptx_kit import (FONT_HEAD, FONT_MONO, arrow_shape, corners, ellipse, line, rect,
                      text, triangle)
from theme import (BG, BLUE, BLUE_LIGHT, BLUE_TEXT, LINE, MARGIN, MUTED, PANEL, PAPER,
                   SURFACE, YELLOW, header)

FONT_TXT = "Barlow"
RED = "#E0566B"          # resultado desfavorable
GREEN = "#3ECF8E"        # resultado favorable (uso puntual)
PANEL_2 = "#0C2445"      # superficie alterna
CHIP = "#0F2C52"         # fondo de chips y pistas de barras
DARK = "#07172D"

CONTENT_TOP = 268
CONTENT_BOTTOM = 1010
CONTENT_LEFT = MARGIN
CONTENT_RIGHT = 1920 - MARGIN
CONTENT_W = CONTENT_RIGHT - CONTENT_LEFT

_FONT_FILES = {
    ("Montserrat", False): "montserrat-600.ttf",
    ("Montserrat", True): "montserrat-700.ttf",
    ("Barlow", False): "Barlow-400.ttf",
    ("Barlow", True): "Barlow-700.ttf",
    ("Roboto Mono", False): "robotomono-400.ttf",
    ("Roboto Mono", True): "robotomono-700.ttf",
}
_FONTS_DIR = os.environ.get("FONTS_DIR", os.path.join(os.path.expanduser("~"), ".fonts"))


@lru_cache(maxsize=256)
def _pil_font(font: str, bold: bool, size: int):
    fname = _FONT_FILES.get((font, bold)) or _FONT_FILES[("Barlow", bold)]
    return ImageFont.truetype(os.path.join(_FONTS_DIR, fname), size)


@lru_cache(maxsize=16)
def _cmap(font: str):
    try:
        from fontTools.ttLib import TTFont
    except ImportError:  # sin fontTools no se comprueba la cobertura
        return None
    fname = _FONT_FILES.get((font, False))
    if not fname:
        return None
    return set(TTFont(os.path.join(_FONTS_DIR, fname)).getBestCmap())


def fuente_con_glifos(s: str, preferida: str = FONT_TXT) -> str:
    """Devuelve la fuente preferida si tiene todos los glifos de `s`; si no, otra que los tenga."""
    for f in (preferida, "Roboto Mono", "Montserrat", "Barlow"):
        cm = _cmap(f)
        if cm is None:
            return preferida
        if all(ord(c) in cm or c in " \u00a0" for c in s):
            return f
    return preferida


def text_width(s: str, size: float, font: str = FONT_TXT, bold: bool = False,
               spacing: float = 0.0) -> float:
    """Ancho en px de una línea de texto (con espaciado de letras en px)."""
    if not s:
        return 0.0
    f = _pil_font(font, bold, max(1, int(round(size))))
    w = f.getlength(s) * (size / round(size) if round(size) else 1)
    return w + spacing * max(0, len(s) - 1)


def wrap_lines(s: str, size: float, width: float, font: str = FONT_TXT, bold: bool = False):
    """Parte un texto en líneas que caben en `width` (medido con la fuente real)."""
    words, lines, cur = s.split(), [], ""
    for wd in words:
        cand = (cur + " " + wd).strip()
        if text_width(cand, size, font, bold) <= width or not cur:
            cur = cand
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


# ------------------------------------------------------------------ encabezados
def subencabezado(slide, eyebrow: str, titulo: str, seccion: str = "Marco práctico"):
    """Encabezado de lámina + antetítulo amarillo + título de la lámina."""
    header(slide, seccion)
    text(slide, MARGIN, 166, 1728, 30, eyebrow.upper(), size=20, bold=True, font=FONT_HEAD,
         color=YELLOW, spacing=2, name="Antetitulo")
    text(slide, MARGIN, 196, 1728, 56, titulo, size=40, bold=True, font=FONT_HEAD,
         name="Titulo de lamina")


# ------------------------------------------------------------------- bloques
def card(slide, x, y, w, h, accent: str | None = BLUE_LIGHT, fill=PANEL, brackets=False,
         accent_side="top"):
    """Tarjeta oscura con borde azul fino y franja de acento (arriba o izquierda)."""
    rect(slide, x, y, w, h, fill=fill, line=BLUE_LIGHT, line_w=1.5, line_alpha=0.4)
    if accent:
        if accent_side == "top":
            rect(slide, x, y, w, 5, fill=accent)
        else:
            rect(slide, x, y, 6, h, fill=accent)
    if brackets:
        corners(slide, x - 10, y - 10, w + 20, h + 20, size=34, width=3)


def label(slide, x, y, w, s, size=18, color=MUTED, align="left", spacing=1.5, bold=True):
    """Rótulo corto en mayúsculas (Montserrat)."""
    text(slide, x, y, w, size * 1.5, s.upper(), size=size, bold=bold, font=FONT_HEAD,
         color=color, spacing=spacing, align=align)


def body(slide, x, y, w, h, s, size=24, color=PAPER, align="left", bold=False,
         anchor="top", line_spacing=1.3):
    text(slide, x, y, w, h, s, size=size, font=FONT_TXT, color=color, align=align,
         bold=bold, anchor=anchor, line_spacing=line_spacing)


def kpi(slide, x, y, w, valor: str, etiqueta: str, color=YELLOW, size=60, sub: str | None = None,
        align="left"):
    """Cifra grande + rótulo. Devuelve la altura usada."""
    text(slide, x, y, w, size * 1.25, valor, size=size, bold=True, font=FONT_HEAD,
         color=color, align=align)
    yy = y + size * 1.22
    label(slide, x, yy, w, etiqueta, size=18, color=PAPER, align=align)
    hh = size * 1.22 + 30
    if sub:
        text(slide, x, yy + 30, w, 30, sub, size=20, font=FONT_TXT, color=MUTED, align=align)
        hh += 32
    return hh


def chip(slide, x, y, s, size=20, mono=True, color=YELLOW, fill=CHIP, border=BLUE_LIGHT,
         pad=12, h=None) -> float:
    """Chip con texto (por defecto código en Roboto Mono). Devuelve su ancho."""
    font = FONT_MONO if mono else FONT_TXT
    w = text_width(s, size, font) + 2 * pad + 4
    hh = h or size * 1.7
    rect(slide, x, y, w, hh, fill=fill, line=border, line_w=1, line_alpha=0.45, radius=6)
    text(slide, x, y, w, hh, s, size=size, font=font, color=color, align="center",
         anchor="middle", wrap=False)
    return w


def tag(slide, x, y, s, fill=YELLOW, color=DARK, size=16, pad=14, h=34) -> float:
    """Etiqueta rellena en mayúsculas (decisión, estado). Devuelve su ancho."""
    w = text_width(s.upper(), size, FONT_HEAD, True, spacing=1.2) + 2 * pad + 6
    rect(slide, x, y, w, h, fill=fill, radius=4)
    text(slide, x, y, w, h, s.upper(), size=size, bold=True, font=FONT_HEAD, color=color,
         align="center", anchor="middle", spacing=1.2, wrap=False)
    return w


def numbadge(slide, x, y, n: str, size=44, fill=YELLOW, color=DARK):
    rect(slide, x, y, size, size, fill=fill, radius=4)
    text(slide, x, y, size, size, n, size=size * 0.46, bold=True, font=FONT_HEAD, color=color,
         align="center", anchor="middle", wrap=False)


def bar(slide, x, y, w, h, frac: float, color=BLUE_LIGHT, track=CHIP, marker: float | None = None):
    """Barra horizontal: pista + relleno proporcional (+ marca opcional)."""
    rect(slide, x, y, w, h, fill=track)
    if frac > 0:
        rect(slide, x, y, max(2, w * min(1.0, frac)), h, fill=color)
    if marker is not None:
        mx = x + w * marker
        rect(slide, mx - 1.5, y - 6, 3, h + 12, fill=PAPER)


def flecha(slide, x0, y, x1, color=YELLOW, h=28, alpha=1.0):
    """Flecha de bloque horizontal de x0 a x1 centrada en y."""
    arrow_shape(slide, x0, y - h / 2, x1 - x0, h, color=color, alpha=alpha)


def flecha_abajo(slide, cx, y0, y1, color=YELLOW, w=28):
    """Flecha hacia abajo (triángulo + vástago)."""
    rect(slide, cx - 3, y0, 6, max(1, y1 - y0 - w * 0.6), fill=color)
    triangle(slide, cx - w / 2, y1 - w * 0.7, w, w * 0.7, color=color, rotation=180)


def nota(slide, s, y=966, size=21, color=MUTED, x=MARGIN, w=1728):
    """Nota al pie de la lámina (una o dos líneas)."""
    text(slide, x, y, w, 44, s, size=size, font=FONT_TXT, color=color, line_spacing=1.25)


# ------------------------------------------------------------------ ecuaciones
class _Eq:
    """Diseña una ecuación en una línea con fracciones, sumatorias y barras.

    Elementos admitidos en la lista `partes`:
      "texto"                         texto normal
      ("res", "96,89%")               resultado resaltado (amarillo, negrita)
      ("frac", num, den)              fracción; num y den son listas de partes
      ("sum", "i=1", "n")             sumatoria con límites
      ("bar", "t")                    letra con barra (media)
      ("sub", "t", "i")               subíndice
      ("sup", "10", "−12")            potencia (exponente)
      ("var", "Accuracy")             nombre de variable en cursiva
    """

    def __init__(self, size=34, color=PAPER, res_color=YELLOW, font=FONT_TXT):
        self.size, self.color, self.res_color, self.font = size, color, res_color, font

    # cada medida devuelve (ancho, alto_arriba, alto_abajo) respecto del eje
    def measure(self, partes, size=None):
        size = size or self.size
        w = up = dn = 0.0
        for p in partes:
            pw, pu, pd = self._measure_one(p, size)
            w += pw
            up, dn = max(up, pu), max(dn, pd)
        gaps = max(0, len(partes) - 1) * size * 0.24
        return w + gaps, up, dn

    def _measure_one(self, p, size):
        if isinstance(p, str):
            return (text_width(p, size, fuente_con_glifos(p, self.font)), size * 0.62,
                    size * 0.62)
        kind = p[0]
        if kind == "res":
            return text_width(p[1], size * 1.05, FONT_HEAD, True), size * 0.66, size * 0.66
        if kind == "var":
            return text_width(p[1], size, self.font) * 1.06 + size * 0.1, size * 0.62, size * 0.62
        if kind == "frac":
            fs = size * 0.86
            nw, nu, nd = self.measure(p[1], fs)
            dw, du, dd = self.measure(p[2], fs)
            w = max(nw, dw) + size * 0.5
            return w, nu + nd + size * 0.14, du + dd + size * 0.14
        if kind == "sum":
            return size * 1.45, size * 1.75, size * 1.45
        if kind == "bar":
            return text_width(p[1], size, self.font) + 2, size * 0.75, size * 0.62
        if kind == "sub":
            return (text_width(p[1], size, self.font) + text_width(p[2], size * 0.62, self.font)
                    + 2, size * 0.62, size * 0.75)
        if kind == "sup":
            return (text_width(p[1], size, self.font) + text_width(p[2], size * 0.7, self.font)
                    + 6, size * 0.9, size * 0.62)
        raise ValueError(p)

    def draw(self, slide, x, axis_y, partes, size=None, color=None):
        size = size or self.size
        color = color or self.color
        cx = x
        for i, p in enumerate(partes):
            pw, _, _ = self._measure_one(p, size)
            self._draw_one(slide, cx, axis_y, p, size, color, pw)
            cx += pw + size * 0.24
        return cx - x - size * 0.24

    def _txt(self, slide, x, axis_y, s, size, color, font=None, bold=False, italic=False):
        font = fuente_con_glifos(s, font or self.font)
        w = text_width(s, size, font, bold) * 1.06 + 6
        h = size * 1.25
        text(slide, x - 2, axis_y - h / 2, w, h, s, size=size, font=font, color=color,
             bold=bold, italic=italic, anchor="middle", line_spacing=1.0, wrap=False)

    def _draw_one(self, slide, x, axis_y, p, size, color, pw):
        if isinstance(p, str):
            self._txt(slide, x, axis_y, p, size, color)
            return
        kind = p[0]
        if kind == "res":
            self._txt(slide, x, axis_y, p[1], size * 1.05, self.res_color, font=FONT_HEAD,
                      bold=True)
        elif kind == "var":
            self._txt(slide, x, axis_y, p[1], size, color, italic=True)
        elif kind == "frac":
            fs = size * 0.86
            nw, nu, nd = self.measure(p[1], fs)
            dw, du, dd = self.measure(p[2], fs)
            rect(slide, x + size * 0.1, axis_y - 1.5, pw - size * 0.2, 3, fill=color)
            self.draw(slide, x + (pw - nw) / 2, axis_y - size * 0.08 - nd - fs * 0.05, p[1], fs,
                      color)
            self.draw(slide, x + (pw - dw) / 2, axis_y + size * 0.1 + du + fs * 0.05, p[2], fs,
                      color)
        elif kind == "sum":
            big = size * 1.8
            sw = text_width("Σ", big, fuente_con_glifos("Σ", self.font))
            self._txt(slide, x + (size * 1.45 - sw) / 2, axis_y, "Σ", big, color)
            small = size * 0.58
            # limites por encima y por debajo del glifo, sin tocarlo
            text(slide, x - 20, axis_y - size * 0.72 - small * 1.3, size * 1.45 + 40,
                 small * 1.25, p[2], size=small, font=self.font, color=color, align="center",
                 line_spacing=1.0)
            text(slide, x - 20, axis_y + size * 0.66, size * 1.45 + 40, small * 1.25, p[1],
                 size=small, font=self.font, color=color, align="center", line_spacing=1.0)
        elif kind == "bar":
            tw = text_width(p[1], size, self.font)
            self._txt(slide, x, axis_y, p[1], size, color, italic=True)
            rect(slide, x + size * 0.16, axis_y - size * 0.52, tw + size * 0.02, 2.5, fill=color)
        elif kind == "sub":
            tw = text_width(p[1], size, self.font)
            self._txt(slide, x, axis_y, p[1], size, color, italic=True)
            self._txt(slide, x + tw + 1, axis_y + size * 0.3, p[2], size * 0.62, color,
                      italic=True)
        elif kind == "sup":
            tw = text_width(p[1], size, self.font)
            self._txt(slide, x, axis_y, p[1], size, color)
            self._txt(slide, x + tw + 3, axis_y - size * 0.4, p[2], size * 0.7, color)


def ecuacion(slide, x, axis_y, partes, size=34, color=PAPER, res_color=YELLOW,
             align="left", w: float | None = None):
    """Dibuja una ecuación con formato matemático. Devuelve (ancho, alto)."""
    eq = _Eq(size=size, color=color, res_color=res_color)
    ew, up, dn = eq.measure(partes)
    if align == "center" and w:
        x = x + (w - ew) / 2
    elif align == "right" and w:
        x = x + w - ew
    eq.draw(slide, x, axis_y, partes)
    return ew, up + dn


def medida_ecuacion(partes, size=34):
    ew, up, dn = _Eq(size=size).measure(partes)
    return ew, up, dn
