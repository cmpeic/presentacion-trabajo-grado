"""Construye el PPTX listo para importar en Canva.

Uso:
    node canva/extraer/run_extract.js canva/build/ext 35 43   # tras cambiar index.html
    python3 canva/construir.py                # versión condensada (por defecto)
    python3 canva/construir.py --completa     # versión de 90 láminas convertidas

Versión condensada (por defecto):
- Láminas 1-34: primera_parte.py (carátula a marco teórico).
- Láminas 35-43: convertidas desde index.html (practico.py), OE1 y las 36 columnas.
- Desde la lámina 44: marco práctico rediseñado y condensado (practico2/g1..g6).
"""

import argparse
import importlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "practico2"))

from guion import notas  # noqa: E402
from practico import add_practical_slide  # noqa: E402
from pptx_kit import new_presentation  # noqa: E402
import primera_parte  # noqa: E402

GRUPOS = ["g1", "g2", "g3", "g4", "g5", "g6"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ext", default=str(HERE / "build" / "ext"))
    ap.add_argument("--out", default=str(HERE / "presentacion_trabajo_grado_canva.pptx"))
    ap.add_argument("--completa", action="store_true",
                    help="convierte las 90 láminas originales sin condensar")
    ap.add_argument("--preview", action="store_true",
                    help="ajusta el texto de una línea para previsualizar con LibreOffice")
    a = ap.parse_args()
    ext = Path(a.ext)
    import pptx_kit
    pptx_kit.OPT_DIR = str(HERE / "build" / "img")
    if a.preview:
        import practico
        practico.SINGLE_LINE_WRAP = True
    n = notas()
    prs = new_presentation()
    primera_parte.construir(prs, n)
    ultima = 90 if a.completa else 43
    for i in range(35, ultima + 1):
        add_practical_slide(prs, ext / f"s{i:02d}.json", ext / f"s{i:02d}_deco.png",
                            ext / "deco", n[i])
    if not a.completa:
        for g in GRUPOS:
            if g == "g6":
                g6 = importlib.import_module("g6")
                mcnemar = importlib.import_module("mcnemar")
                g6.p19(prs, n)
                g6.p20(prs, n)
                g6.p21(prs, n)
                mcnemar.p_mcnemar(prs, n)  # lámina agregada por el autor
                g6.p22(prs, n)
                g6.p23(prs, n)
            else:
                importlib.import_module(g).construir(prs, n)
    prs.core_properties.title = "Presentación de trabajo de grado"
    prs.core_properties.author = "Pablo Enrique Cañez Larico"
    prs.save(a.out)
    print(f"{len(prs.slides)} laminas -> {a.out}")


if __name__ == "__main__":
    main()
