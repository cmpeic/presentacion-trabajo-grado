"""Convierte las primitivas extraidas del HTML (marco practico) en laminas PPTX."""

import json
from pathlib import Path
from urllib.parse import unquote, urlparse

import numpy as np
from PIL import Image
from scipy import ndimage

from pptx_kit import (FONT_BODY, FONT_HEAD, FONT_MONO, add_slide, ellipse, image, image_fit,
                      line, notes, rect, text, triangle)
from theme import FONDO, header

SINGLE_LINE_WRAP = False  # True solo para previsualizar con LibreOffice
GLYPHS = {"▶": "►", "▸": "►", "◀": "◄"}

FONT_MAP = {"cambria": FONT_HEAD, "bahnschrift": "Barlow", "consolas": FONT_MONO,
            "arial": "Barlow"}


def _font(css_family: str) -> str:
    first = css_family.split(",")[0].strip().strip('"\'').lower()
    return FONT_MAP.get(first, "Barlow")


def _src_path(src: str) -> str:
    u = urlparse(src)
    return unquote(u.path)


def _box(slide, it):
    x, y, w, h = it["x"], it["y"], it["w"], it["h"]
    sides = it["sides"]
    present = [s for s in sides if s]
    uniform = (len(present) == 4 and len({(s["w"], s["color"]) for s in present}) == 1)
    radius = it.get("radius") or None
    if radius and radius < 1.5:
        radius = None
    if uniform:
        s = present[0]
        bw = s["w"]
        dash = {"dashed": "dash", "dotted": "sysDot"}.get(s.get("style"))
        rect(slide, x + bw / 2, y + bw / 2, max(1, w - bw), max(1, h - bw),
             fill=it["fill"], fill_alpha=it["fillAlpha"] or 1, line=s["color"], line_w=bw,
             line_alpha=s["alpha"], radius=radius, dash=dash)
        return
    if it["fill"]:
        rect(slide, x, y, w, h, fill=it["fill"], fill_alpha=it["fillAlpha"], radius=radius)
    top, right, bottom, left = sides
    dashed = {k: v for k, v in zip("trbl", sides) if v and v.get("style") in ("dashed", "dotted")}
    for k, v in dashed.items():
        dash = "dash" if v["style"] == "dashed" else "sysDot"
        o = v["w"] / 2
        seg = {"t": (x, y + o, x + w, y + o), "b": (x, y + h - o, x + w, y + h - o),
               "l": (x + o, y, x + o, y + h), "r": (x + w - o, y, x + w - o, y + h)}[k]
        line(slide, *seg, color=v["color"], width=v["w"], alpha=v["alpha"], dash=dash)
    top, right, bottom, left = [None if (v and v.get("style") in ("dashed", "dotted")) else v
                                for v in sides]
    if top:
        rect(slide, x, y, w, top["w"], fill=top["color"], fill_alpha=top["alpha"])
    if bottom:
        rect(slide, x, y + h - bottom["w"], w, bottom["w"], fill=bottom["color"],
             fill_alpha=bottom["alpha"])
    if left:
        rect(slide, x, y, left["w"], h, fill=left["color"], fill_alpha=left["alpha"])
    if right:
        rect(slide, x + w - right["w"], y, right["w"], h, fill=right["color"],
             fill_alpha=right["alpha"])


def _img(slide, it):
    path = _src_path(it["src"])
    if not Path(path).exists():
        return
    x, y, w, h = it["x"], it["y"], it["w"], it["h"]
    fit = it.get("fit") or "fill"
    alpha = it.get("opacity", 1)
    if fit == "contain" or fit == "scale-down":
        image_fit(slide, path, x, y, w, h, alpha=alpha)
    elif fit == "cover":
        iw, ih = Image.open(path).size
        box_r, img_r = w / h, iw / ih
        if img_r > box_r:  # recortar lados
            frac = 1 - box_r / img_r
            crop = (frac / 2, 0, frac / 2, 0)
        else:
            frac = 1 - img_r / box_r
            crop = (0, frac / 2, 0, frac / 2)
        image(slide, path, x, y, w, h, alpha=alpha, crop=crop)
    else:
        image(slide, path, x, y, w, h, alpha=alpha)


MARKERS = {"▪": "square", "■": "square", "●": "dot", "•": "dot", "►": "right", "▶": "right",
           "▸": "right", "▼": "down", "▾": "down"}


def _marker_shape(slide, it):
    """Dibuja como forma nativa un texto que es solo un marcador geometrico."""
    runs = [r for r in it["runs"] if not r.get("br")]
    if len(runs) != 1:
        return False
    glyph = runs[0]["text"].strip()
    if glyph not in MARKERS:
        return False
    r = runs[0]
    size = r["size"]
    bx, by, bw, bh = it["bbox"]
    lh = it["lineHeight"]
    cx, cy = bx + size * 0.3, by + (it.get("firstH") or lh) / 2
    kind = MARKERS[glyph]
    col, a = r["color"], r.get("alpha", 1)
    if kind == "square":
        side = size * 0.36
        rect(slide, cx - side / 2, cy - side / 2, side, side, fill=col, fill_alpha=a,
             name="Marcador")
    elif kind == "dot":
        ellipse(slide, cx, cy, size * 0.17, fill=col, fill_alpha=a)
    else:
        # triangulo centrado en el glifo original (la rotacion es sobre el centro)
        tw, th = size * 0.78, size * 0.68
        gcx = bx + min(bw, size) / 2
        triangle(slide, gcx - tw / 2, cy - th / 2, tw, th, color=col,
                 rotation=90 if kind == "right" else 180, alpha=a, name="Flecha")
    return True


def _frag_spec(r, size=None):
    t = r["text"]
    for a, b in GLYPHS.items():
        t = t.replace(a, b)
    spec = {"text": t, "size": size or r["size"], "bold": r.get("weight", 400) >= 600,
            "italic": r.get("italic", False), "font": _font(r.get("font", "")),
            "color": r["color"], "alpha": r.get("alpha", 1)}
    if r.get("spacing"):
        spec["spacing"] = r["spacing"] * 0.75
    return spec


def _text_frags(slide, it):
    """Caja con fuentes mezcladas: un cuadro sin ajuste por linea y por fragmento."""
    frags = it["frags"]
    if it.get("pseudoPrefix") and it["runs"] and it["runs"][0].get("pseudo"):
        cx = it["content"][0]
        f0 = frags[0]
        pre = {"type": "text", "runs": [it["runs"][0]], "align": "left",
               "bbox": [cx, f0["y"], it["runs"][0]["size"] * 1.2, f0["h"]],
               "content": [cx, f0["y"], it["runs"][0]["size"] * 1.2, f0["h"]], "lines": 1,
               "lineHeight": f0["h"], "fontSize": it["runs"][0]["size"], "firstH": f0["h"]}
        _text(slide, pre)
    for f in frags:
        spec = _frag_spec(f)
        w = f["w"] * 1.06 + 8
        ls = (f["h"] / f["size"]) if f["size"] else 1.2
        text(slide, f["x"], f["y"], w, f["h"] + 2, [[spec]], size=f["size"], line_spacing=ls,
             wrap=SINGLE_LINE_WRAP)


def _text(slide, it):
    if _marker_shape(slide, it):
        return
    if it.get("frags"):
        _text_frags(slide, it)
        return
    runs = it["runs"]
    if it.get("anon") and it.get("pseudoPrefix") and len(runs) > 1 and runs[0].get("pseudo"):
        # el ::before de un flex es su propio item: va al inicio del contenido
        cx, cy, cw, ch = it["content"]
        pre = dict(it, runs=[runs[0]], pseudoPrefix=False, anon=False, lines=1,
                   bbox=[cx, it["bbox"][1], runs[0]["size"] * 1.2, it["bbox"][3]])
        _text(slide, pre)
        it = dict(it, runs=runs[1:], pseudoPrefix=False)
        runs = it["runs"]
    paragraphs, cur = [], []
    for r in runs:
        if r.get("br"):
            paragraphs.append(cur)
            cur = []
            continue
        t = r["text"]
        for a, b in GLYPHS.items():
            t = t.replace(a, b)
        if r.get("pseudo") and t.endswith(" "):
            t = t.rstrip() + "\u2002"  # separacion visible tras marcadores CSS
        spec = {
            "text": t,
            "size": r["size"],
            "bold": r.get("weight", 400) >= 600,
            "italic": r.get("italic", False),
            "font": _font(r.get("font", "")),
            "color": r["color"],
            "alpha": r.get("alpha", 1),
        }
        if r.get("spacing"):
            spec["spacing"] = r["spacing"] * 0.75
        if r.get("sub"):
            spec["baseline"] = -25
        if r.get("sup"):
            spec["baseline"] = 30
        cur.append(spec)
    paragraphs.append(cur)
    paragraphs = [p if p else [{"text": "", "size": it["fontSize"]}] for p in paragraphs]

    bx, by, bw, bh = it["bbox"]
    cx, cy, cw, ch = it["content"]
    lh = it["lineHeight"]
    fs = it["fontSize"]
    nlines = it["lines"]
    first_h = it.get("firstH") or min(bh, fs * 1.25)
    # con interlineado menor que la letra, Canva no sube el texto: no compensar
    y = by - max(0.0, (lh - first_h) / 2)
    h = max(bh, nlines * lh) + 2
    align = it["align"] if it["align"] in ("left", "center", "right", "justify") else "left"
    single = nlines == 1 and len(paragraphs) == 1
    if single:
        slack = bw * 0.08 + 10
        if align == "center":
            x, w = bx - slack / 2, bw + slack
        elif align == "right":
            x, w = bx - slack, bw + slack
        else:
            x, w = bx, bw + slack
            if it.get("pseudoPrefix") and not it.get("anon"):
                w += bx - cx
                x = cx
        wrap = SINGLE_LINE_WRAP
    elif it.get("anon"):
        # item anonimo de un flex/grid: su ancho es el de sus propias lineas
        x, w = bx, bw * 1.03 + 4
        if align == "center":
            x = bx - (w - bw) / 2
        elif align == "right":
            x = bx - (w - bw)
        wrap = True
    else:
        x, w = cx, cw + 2
        if bx < x - 1:  # texto que desborda el contenedor
            x = bx
        if bx + bw > x + w:
            w = bx + bw - x + 2
        wrap = True
    ls = lh / fs if fs else 1.2
    text(slide, x, y, w, h, paragraphs, size=fs, line_spacing=ls, align=align, wrap=wrap)


def _deco_components(png_path: Path, out_dir: Path, tag: str):
    """Recorta la capa de decoraciones en componentes conexos."""
    im = Image.open(png_path).convert("RGBA")
    a = np.array(im)[:, :, 3]
    mask = a > 8
    if mask.sum() < 20:
        return []
    lab, n = ndimage.label(ndimage.binary_dilation(mask, iterations=6))
    comps = []
    for k, sl in enumerate(ndimage.find_objects(lab)):
        if sl is None:
            continue
        sub = mask[sl] & (lab[sl] == k + 1)
        if sub.sum() < 20:
            continue
        y0, y1 = max(0, sl[0].start - 2), min(a.shape[0], sl[0].stop + 2)
        x0, x1 = max(0, sl[1].start - 2), min(a.shape[1], sl[1].stop + 2)
        crop = im.crop((x0, y0, x1, y1))
        p = out_dir / f"{tag}_deco_{k:02d}.png"
        crop.save(p, optimize=True)
        comps.append((str(p), x0, y0, x1 - x0, y1 - y0))
    return comps


def add_practical_slide(prs, json_path: Path, deco_png: Path, deco_dir: Path, nota: str,
                        titulo: str = "Marco práctico"):
    data = json.loads(Path(json_path).read_text(encoding="utf-8"))
    slide = add_slide(prs, bg_image=FONDO)
    header(slide, titulo)
    texts = []
    for it in data["items"]:
        if it["type"] == "box":
            if it["tag"] == "SECTION" and it["w"] >= 1900 and it["h"] >= 1060:
                continue  # fondo de la escena
            _box(slide, it)
        elif it["type"] == "img":
            _img(slide, it)
        elif it["type"] == "text":
            texts.append(it)
    deco_dir.mkdir(parents=True, exist_ok=True)
    for (p, x, y, w, h) in _deco_components(deco_png, deco_dir, Path(json_path).stem):
        image(slide, p, x, y, w, h, name="Decoracion")
    for it in texts:
        _text(slide, it)
    notes(slide, nota)
    return slide
