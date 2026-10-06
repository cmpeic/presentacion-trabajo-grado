"""Construye el PPTX de 90 laminas listo para importar en Canva.

Uso:
    node canva/extraer/run_extract.js canva/build/ext 35 90   # una vez, o tras cambiar index.html
    python3 canva/construir.py

Laminas 1-34 se componen en primera_parte.py; laminas 35-90 se convierten desde
las primitivas extraidas de index.html (practico.py).
"""

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from guion import notas  # noqa: E402
from practico import add_practical_slide  # noqa: E402
from pptx_kit import new_presentation  # noqa: E402
import primera_parte  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ext", default=str(HERE / "build" / "ext"))
    ap.add_argument("--out", default=str(HERE / "presentacion_trabajo_grado_canva.pptx"))
    ap.add_argument("--desde", type=int, default=1)
    ap.add_argument("--hasta", type=int, default=90)
    ap.add_argument("--preview", action="store_true",
                    help="ajusta el texto de una linea para previsualizar con LibreOffice")
    a = ap.parse_args()
    ext = Path(a.ext)
    import pptx_kit
    pptx_kit.OPT_DIR = str(HERE / "build" / "img")
    if a.preview:
        import practico
        practico.SINGLE_LINE_WRAP = True
    n = notas()
    prs = new_presentation()
    if a.desde <= 34:
        primera_parte.construir(prs, n)
    for i in range(max(35, a.desde), a.hasta + 1):
        add_practical_slide(prs, ext / f"s{i:02d}.json", ext / f"s{i:02d}_deco.png",
                            ext / "deco", n[i])
    prs.core_properties.title = "Presentación de trabajo de grado"
    prs.core_properties.author = "Pablo Enrique Cañez Larico"
    prs.save(a.out)
    print(f"{len(prs.slides)} laminas -> {a.out}")


if __name__ == "__main__":
    main()
