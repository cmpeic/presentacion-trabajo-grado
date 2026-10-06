"""Previsualiza con LibreOffice las láminas de un grupo del marco práctico rediseñado.

Uso: python3 canva/practico2/preview.py g1 [g2 ...]
Salida: canva/build/preview/<grupo>/pNN.png y hoja.png
"""

import importlib
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CANVA = HERE.parent
sys.path.insert(0, str(CANVA))
sys.path.insert(0, str(HERE))

import pptx_kit  # noqa: E402
from guion import notas  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402


def preview(grupo: str):
    pptx_kit.OPT_DIR = str(CANVA / "build" / "img")
    mod = importlib.import_module(grupo)
    importlib.reload(mod)
    prs = pptx_kit.new_presentation()
    mod.construir(prs, notas())
    out = CANVA / "build" / "preview" / grupo
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("*.png"):
        old.unlink()
    pptx_path = out / f"{grupo}.pptx"
    prs.save(pptx_path)
    profile = f"file:///tmp/lo_profile_{grupo}"
    subprocess.run(["soffice", f"-env:UserInstallation={profile}", "--headless",
                    "--convert-to", "pdf", str(pptx_path), "--outdir", str(out)],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                   timeout=300)
    subprocess.run(["pdftoppm", "-r", "72", "-png", str(out / f"{grupo}.pdf"), str(out / "p")],
                   check=True)
    pngs = sorted(out.glob("p-*.png"))
    W, H = 960, 540
    cols = 2
    rows = (len(pngs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * W, rows * (H + 18)), "white")
    d = ImageDraw.Draw(sheet)
    for k, p in enumerate(pngs):
        im = Image.open(p).convert("RGB").resize((W, H))
        x, y = (k % cols) * W, (k // cols) * (H + 18)
        sheet.paste(im, (x, y + 18))
        d.text((x + 4, y + 3), f"{grupo} lamina {k + 1}", fill="black")
    sheet.save(out / "hoja.png")
    print(f"{grupo}: {len(pngs)} laminas -> {out}")


if __name__ == "__main__":
    for g in sys.argv[1:]:
        preview(g)
