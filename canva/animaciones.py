"""Graficas animadas que se colocan sobre las laminas ya importadas en Canva.

Canva no garantiza conservar las animaciones de PowerPoint al importar y no acepta
GIF por URL, asi que las graficas que deben moverse se generan como video WebM (VP9)
con canal alfa y se insertan encima de su version estatica, en la misma posicion:

- barras: cada barra registrada con registrar_barra() crece desde la izquierda. El
  video es transparente salvo en el area de las barras, de modo que rotulos y cifras
  siguen siendo texto editable; debajo queda la barra estatica como respaldo.
- red neuronal: pulsos que recorren la red de la portada y del cierre (bucle continuo).

Uso: lo llama construir.py; deja los videos en canva/animaciones/ y un manifiesto con
la pagina, el archivo y la caja (left, top, width, height) de cada uno. Requiere ffmpeg.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
OUT = HERE / "animaciones"

FPS = 25
FRAME_MS = 1000 // FPS
DUR_MS = 900
PASO_MS = 90
PAUSA_MS = 15000  # la grafica queda completa (si Canva repite el video, vuelve a crecer)
VUELTAS_RED = 5   # la red es un bucle de 2,4 s; el video dura cinco vueltas


def _c3(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _codificar(frames: list, out: Path) -> None:
    """Escribe los cuadros RGBA (a FPS) como WebM VP9 con transparencia."""
    import shutil
    import subprocess
    import tempfile

    w, h = frames[0].size
    W, H = w + w % 2, h + h % 2  # yuva420p exige lados pares
    tmp = Path(tempfile.mkdtemp(prefix="anim_"))
    try:
        for i, fr in enumerate(frames):
            if (W, H) != (w, h):
                lienzo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                lienzo.paste(fr, (0, 0))
                fr = lienzo
            fr.save(tmp / f"{i:05d}.png")
        out.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i",
                        str(tmp / "%05d.png"), "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p",
                        "-b:v", "0", "-crf", "28", "-auto-alt-ref", "0", "-an", str(out)],
                       check=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _ease(p: float) -> float:
    p = max(0.0, min(1.0, p))
    return 1 - (1 - p) ** 3


def video_barras(barras: list[dict], out: Path, marcador="#0B1F3A") -> dict:
    """Video transparente con las barras creciendo. Devuelve la caja en px del lienzo."""
    x0 = math.floor(min(b["x"] for b in barras)) - 1
    y0 = math.floor(min(b["y"] - (8 if b.get("marker") is not None else 0) for b in barras)) - 1
    x1 = math.ceil(max(b["x"] + b["w"] for b in barras)) + 1
    y1 = math.ceil(max(b["y"] + b["h"] + (8 if b.get("marker") is not None else 0)
                       for b in barras)) + 1
    W, H = x1 - x0, y1 - y0
    total = (len(barras) - 1) * PASO_MS + DUR_MS
    frames = []
    for t in range(0, total + FRAME_MS, FRAME_MS):
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        for k, b in enumerate(barras):
            bx, by = round(b["x"] - x0), round(b["y"] - y0)
            bw, bh = round(b["w"]), round(b["h"])
            # solo se tapa la parte rellena de la barra estatica (con el color de la pista):
            # el resto queda transparente, asi las cifras escritas sobre la pista se ven
            full = max(1, round(bw * min(1.0, b["frac"])))
            d.rectangle([bx, by, bx + full - 1, by + bh - 1],
                        fill=_c3(b["track"] or b["fondo"]) + (255,))
            fw = round(bw * min(1.0, b["frac"]) * _ease((t - k * PASO_MS) / DUR_MS))
            if fw >= 1:
                d.rectangle([bx, by, bx + fw - 1, by + bh - 1], fill=_c3(b["color"]) + (255,))
            if b.get("marker") is not None:
                mx = round(b["x"] - x0 + b["w"] * b["marker"])
                d.rectangle([mx - 1, by - 6, mx + 1, by + bh + 5], fill=_c3(marcador) + (255,))
        frames.append(im)
    frames += [frames[-1]] * (PAUSA_MS // FRAME_MS)
    _codificar(frames, out)
    return dict(left=x0, top=y0, width=W + W % 2, height=H + H % 2)


def video_red(out: Path, cx: float, cy: float, r: float, fondo="#F1F5FA") -> dict:
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
    amarillo = _c3("#FFD21F")
    c = W * S / 2
    # mascara: el video solo cubre el circulo (borde exterior del aro), con borde suave
    mask_big = Image.new("L", (W * S, W * S), 0)
    re = (r + 3) * S
    ImageDraw.Draw(mask_big).ellipse([c - re, c - re, c + re, c + re], fill=255)
    mask = mask_big.resize((W, W), Image.LANCZOS)
    frames = []
    for f in range(n_frames):
        ph = f / n_frames
        big = Image.new("RGBA", (W * S, W * S), _c3(fondo) + (255,))
        d = ImageDraw.Draw(big)
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
                      fill=amarillo + (255,))
        # halos (capa aparte, compuesta con transparencia)
        halo = Image.new("RGBA", big.size, (0, 0, 0, 0))
        dh = ImageDraw.Draw(halo)
        for li, col in enumerate(nodos):
            brillo = max(0.0, 1 - ((ph * 3 - li) % 3) * 2.5)  # la capa brilla al recibir
            if brillo <= 0:
                continue
            for (nx, ny) in col:
                g = 17 * S + 6 * S * brillo
                dh.ellipse([c + nx * S - g, c + ny * S - g, c + nx * S + g, c + ny * S + g],
                           fill=amarillo + (int(170 * brillo),))
        big.alpha_composite(halo)
        d = ImageDraw.Draw(big)
        brillo_capa = Image.new("RGBA", big.size, (0, 0, 0, 0))
        db = ImageDraw.Draw(brillo_capa)
        for col in nodos:
            for (nx, ny) in col:
                rn = 17 * S
                d.ellipse([c + nx * S - rn, c + ny * S - rn, c + nx * S + rn, c + ny * S + rn],
                          fill=azul + (255,))
                db.ellipse([c + nx * S - rn * 0.45 - 5 * S, c + ny * S - rn * 0.45 - 5 * S,
                            c + nx * S - rn * 0.45 + 3 * S, c + ny * S - rn * 0.45 + 3 * S],
                           fill=(255, 255, 255, 150))
        big.alpha_composite(brillo_capa)
        d = ImageDraw.Draw(big)
        d.ellipse([c - r * S, c - r * S, c + r * S, c + r * S], outline=aro + (255,),
                  width=5 * S)
        fr = big.resize((W, W), Image.LANCZOS)
        fr.putalpha(mask)
        frames.append(fr)
    _codificar(frames * VUELTAS_RED, out)
    return dict(left=round(cx - W / 2), top=round(cy - W / 2), width=W + W % 2,
                height=W + W % 2)


def generar(prs, paginas_barras: set[int] | None = None) -> list[dict]:
    """Genera los videos de todas las laminas con barras registradas o red animada."""
    OUT.mkdir(parents=True, exist_ok=True)
    for old in list(OUT.glob("*.gif")) + list(OUT.glob("*.webm")):
        old.unlink()
    manifiesto = []
    for i, slide in enumerate(prs.slides, 1):
        barras = getattr(slide, "_barras", None)
        if barras and (paginas_barras is None or i in paginas_barras):
            nombre = f"barras_{i:02d}.webm"
            caja = video_barras(barras, OUT / nombre)
            manifiesto.append(dict(pagina=i, archivo=nombre, tipo="barras", **caja))
        red = getattr(slide, "_red", None)
        if red:
            nombre = f"red_{i:02d}.webm"
            caja = video_red(OUT / nombre, *red)
            manifiesto.append(dict(pagina=i, archivo=nombre, tipo="red", **caja))
    (OUT / "manifiesto.json").write_text(json.dumps(manifiesto, indent=1, ensure_ascii=False),
                                         encoding="utf-8")
    return manifiesto
