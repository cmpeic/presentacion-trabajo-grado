"""Comprueba que cada cifra de las láminas de un grupo exista en el contenido original.

Uso: python3 canva/practico2/check_cifras.py g1 [g2 ...]
Lista las cifras (números con punto de miles, coma decimal o porcentaje) que
aparecen en las láminas generadas y no figuran en contenido_original.md ni en
GUION.md.
"""

import importlib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CANVA = HERE.parent
sys.path.insert(0, str(CANVA))
sys.path.insert(0, str(HERE))

import pptx_kit  # noqa: E402
from guion import notas  # noqa: E402

FUENTE = (HERE / "contenido_original.md").read_text(encoding="utf-8") + \
    (HERE / "cifras_autor.md").read_text(encoding="utf-8") + \
    (CANVA.parent / "GUION.md").read_text(encoding="utf-8")
FUENTE_N = FUENTE.replace(" ", " ")
NUM = re.compile(r"[−-]?\d[\d.,]*\s?%?")


def textos(prs):
    for i, slide in enumerate(prs.slides, 1):
        for sh in slide.shapes:
            if sh.has_text_frame and sh.text_frame.text.strip():
                yield i, sh.text_frame.text


def check(grupo):
    pptx_kit.OPT_DIR = str(CANVA / "build" / "img")
    mod = importlib.import_module(grupo)
    prs = pptx_kit.new_presentation()
    mod.construir(prs, notas())
    faltan = []
    for i, t in textos(prs):
        for m in NUM.findall(t.replace(" ", " ")):
            tok = m.strip().rstrip(".,")
            if len(tok.replace("%", "").replace(" ", "")) <= 1:
                continue
            base = tok.replace(" %", "%")
            variantes = {tok, base, base.replace("%", " %"), base.replace("−", "-"),
                         base.replace("-", "−")}
            if not any(v in FUENTE_N for v in variantes):
                faltan.append((i, tok, t[:60].replace("\n", " ")))
    if faltan:
        print(f"{grupo}: {len(faltan)} cifras sin respaldo")
        for i, tok, ctx in faltan:
            print(f"  lámina {i}: {tok!r}  en «{ctx}»")
    else:
        print(f"{grupo}: todas las cifras tienen respaldo")


if __name__ == "__main__":
    for g in sys.argv[1:]:
        check(g)
