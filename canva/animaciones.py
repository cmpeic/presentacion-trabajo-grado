"""Graficas animadas (GIF) que se colocan sobre las laminas ya importadas en Canva.

Canva no garantiza conservar las animaciones de PowerPoint al importar, asi que las
graficas que deben moverse se generan como GIF y se insertan encima de su version
estatica, en la misma posicion:

- barras: cada barra registrada con registrar_barra() crece desde la izquierda. El GIF
  es transparente salvo en el area de las barras, de modo que rotulos y cifras siguen
  siendo texto editable; debajo queda la barra estatica como respaldo.
- red neuronal: pulsos que recorren la red de la portada y del cierre (bucle continuo).

Uso: lo llama construir.py; deja los GIF en canva/animaciones/ y un manifiesto con
la pagina, el archivo y la caja (left, top, width, height) de cada uno.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
OUT = HERE / "animaciones"

FRAME_MS = 40
DUR_MS = 900
PASO_MS = 90
PAUSA_MS = 12000  # la grafica queda completa y vuelve a crecer cada ~13 s


def _c3(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _ease(p: float) -> float:
    p = max(0.0, min(1.0, p))
    return 1 - (1 - p) ** 3


def gif_barras(barras: list[dict], out: Path, marcador="#0B1F3A") -> dict:
    """GIF transparente con las barras creciendo. Devuelve la caja en px del lienzo."""
    x0 = math.floor(min(b["x"] for b in barras)) - 1
    y0 = math.floor(min(b["y"] - (8 if b.get("marker") is not None else 0) for b in barras)) - 1
    x1 = math.ceil(max(b["x"] + b["w"] for b in barras)) + 1
    y1 = math.ceil(max(b["y"] + b["h"] + (8 if b.get("marker") is not None else 0)
                       for b in barras)) + 1
    W, H = x1 - x0, y1 - y0
    colores = []

    def idx(c):
        c = _c3(c)
        if c not in colores:
            colores.append(c)
        return colores.index(c) + 1  # 0 = transparente

    for b in barras:
        idx(b["track"] or b["fondo"])
        idx(b["color"])
    idx(marcador)
    paleta = [255, 255, 255] + [v for c in colores for v in c]
    paleta += [0] * (768 - len(paleta))

    total = (len(barras) - 1) * PASO_MS + DUR_MS
    tiempos = list(range(0, total + FRAME_MS, FRAME_MS))
    frames, duraciones = [], []
    for t in tiempos:
        im = Image.new("P", (W, H), 0)
        im.putpalette(paleta)
        d = ImageDraw.Draw(im)
        for k, b in enumerate(barras):
            bx, by = round(b["x"] - x0), round(b["y"] - y0)
            bw, bh = round(b["w"]), round(b["h"])
            d.rectangle([bx, by, bx + bw - 1, by + bh - 1], fill=idx(b["track"] or b["fondo"]))
            e = _ease((t - k * PASO_MS) / DUR_MS)
            fw = round(bw * min(1.0, b["frac"]) * e)
            if fw >= 1:
                d.rectangle([bx, by, bx + fw - 1, by + bh - 1], fill=idx(b["color"]))
            if b.get("marker") is not None:
                mx = round(b["x"] - x0 + b["w"] * b["marker"])
                d.rectangle([mx - 1, by - 6, mx + 1, by + bh + 5], fill=idx(marcador))
        frames.append(im)
        duraciones.append(FRAME_MS)
    duraciones[-1] = PAUSA_MS
    out.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=duraciones, loop=0,
                   transparency=0, disposal=2, optimize=False)
    return dict(left=x0, top=y0, width=W, height=H)


def gif_red(out: Path, cx: float, cy: float, r: float, fondo="#F1F5FA") -> dict:
    """Red neuronal con pulsos (bucle sin cortes) dentro del circulo de la portada."""
    S = 2  # se dibuja al doble y se reduce para suavizar bordes
    R = r + 50
    W = int(2 * R)
    n_frames = 60
    capas = [3, 5, 5, 2]
    xs = [-0.62, -0.2, 0.22, 0.62]
    nodos = []
    for li, n in enumerate(capas):
        col = []
        for j in range(n):
            yy = (j - (n - 1) / 2) * (0.27 if n > 3 else 0.32)
            col.append((xs[li] * r, yy * r))
        nodos.append(col)
    aristas = [(li, a, b) for li in range(len(capas) - 1)
               for a in range(capas[li]) for b in range(capas[li + 1])]
    azul, azul_claro, aro = _c3("#2F7BFF"), _c3("#9DBDF5"), _c3("#2F7BFF")
    blanco = (255, 255, 255)
    frames = []
    for f in range(n_frames):
        ph = f / n_frames
        big = Image.new("RGBA", (W * S, W * S), (255, 255, 255, 0))
        d = ImageDraw.Draw(big)
        c = W * S / 2
        d.ellipse([c - (r + 44) * S, c - (r + 44) * S, c + (r + 44) * S, c + (r + 44) * S],
                  outline=_c3("#0B5EA8") + (90,), width=2 * S)
        d.ellipse([c - r * S, c - r * S, c + r * S, c + r * S], fill=_c3(fondo) + (255,),
                  outline=aro + (255,), width=5 * S)
        for (li, a, b) in aristas:
            (ax, ay), (bx, by) = nodos[li][a], nodos[li + 1][b]
            d.line([c + ax * S, c + ay * S, c + bx * S, c + by * S], fill=azul_claro + (255,),
                   width=2 * S)
        # pulsos: la senal avanza capa por capa (un tercio del ciclo por capa)
        for k, (li, a, b) in enumerate(aristas):
            t = (ph * 3 - li) % 3
            if t >= 1 or (k * 0.37) % 1 > 0.62:  # solo una parte de las aristas lleva pulso
                continue
            (ax, ay), (bx, by) = nodos[li][a], nodos[li + 1][b]
            px_, py_ = ax + (bx - ax) * t, ay + (by - ay) * t
            rr = 6 * S * (0.6 + 0.4 * math.sin(math.pi * t))
            d.ellipse([c + px_ * S - rr, c + py_ * S - rr, c + px_ * S + rr, c + py_ * S + rr],
                      fill=(255, 210, 31, 255))
        for li, col in enumerate(nodos):
            brillo = max(0.0, 1 - ((ph * 3 - li) % 3) * 2.5)  # la capa brilla al recibir
            for (nx, ny) in col:
                rn = 17 * S
                g = 5 * S * brillo
                if brillo > 0:
                    d.ellipse([c + nx * S - rn - g, c + ny * S - rn - g, c + nx * S + rn + g,
                               c + ny * S + rn + g], fill=_c3("#FFD21F") + (int(150 * brillo),))
                d.ellipse([c + nx * S - rn, c + ny * S - rn, c + nx * S + rn, c + ny * S + rn],
                          fill=azul + (255,))
                d.ellipse([c + nx * S - rn * 0.45 - 5 * S, c + ny * S - rn * 0.45 - 5 * S,
                           c + nx * S - rn * 0.45 + 3 * S, c + ny * S - rn * 0.45 + 3 * S],
                          fill=(255, 255, 255, 150))
        im = big.resize((W, W), Image.LANCZOS)
        # fondo blanco (el de la lamina) donde no hay dibujo; fuera del aro, transparente
        base = Image.new("RGBA", (W, W), blanco + (255,))
        base.alpha_composite(im)
        frames.append(base)
    pal = frames[0].convert("RGB").quantize(colors=255, method=Image.MEDIANCUT)
    salida = []
    mask = Image.new("L", (W, W), 0)
    ImageDraw.Draw(mask).ellipse([W / 2 - (r + 47), W / 2 - (r + 47), W / 2 + (r + 47),
                                  W / 2 + (r + 47)], fill=255)
    # los tonos casi blancos de la paleta pasan a blanco puro (el de la lamina)
    pv = pal.getpalette()[:768]
    for i in range(0, len(pv), 3):
        if min(pv[i:i + 3]) >= 246:
            pv[i:i + 3] = [255, 255, 255]
    pal.putpalette(pv)
    for fr in frames:
        q = fr.convert("RGB").quantize(palette=pal, dither=Image.Dither.NONE)
        q2 = Image.new("P", (W, W), 255)
        q2.putpalette(q.getpalette())
        q2.paste(q, (0, 0), mask)
        salida.append(q2)
    out.parent.mkdir(parents=True, exist_ok=True)
    salida[0].save(out, save_all=True, append_images=salida[1:], duration=FRAME_MS, loop=0,
                   transparency=255, disposal=2, optimize=False)
    return dict(left=round(cx - W / 2), top=round(cy - W / 2), width=W, height=W)


def generar(prs, paginas_barras: set[int] | None = None) -> list[dict]:
    """Genera los GIF de todas las laminas con barras registradas o red animada."""
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.gif"):
        old.unlink()
    manifiesto = []
    for i, slide in enumerate(prs.slides, 1):
        barras = getattr(slide, "_barras", None)
        if barras and (paginas_barras is None or i in paginas_barras):
            nombre = f"barras_{i:02d}.gif"
            caja = gif_barras(barras, OUT / nombre)
            manifiesto.append(dict(pagina=i, archivo=nombre, tipo="barras", **caja))
        red = getattr(slide, "_red", None)
        if red:
            nombre = f"red_{i:02d}.gif"
            caja = gif_red(OUT / nombre, *red)
            manifiesto.append(dict(pagina=i, archivo=nombre, tipo="red", **caja))
    (OUT / "manifiesto.json").write_text(json.dumps(manifiesto, indent=1, ensure_ascii=False),
                                         encoding="utf-8")
    return manifiesto
