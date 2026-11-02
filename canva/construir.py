"""Construye el PPTX listo para importar en Canva.

Uso:
    python3 canva/construir.py                # versión en fondo blanco (por defecto)
    python3 canva/construir.py --completa     # 90 láminas originales convertidas (fondo oscuro)

Versión por defecto (69 láminas, el orden de la versión editada por el autor en Canva):
- 1-34: primera_parte.py (carátula a marco teórico).
- 35-45: practico2/g0.py (OE1: escala, metodologías, actores, diagramas del autor,
  tiempos manuales y las 36 columnas por rol).
- 46-69: marco práctico rediseñado (practico2/g1..g6 y la lámina de McNemar).

Además escribe las animaciones de entrada del PPTX, genera los GIF de las gráficas
animadas (canva/animaciones/) y el manifiesto con su posición para insertarlos en Canva.
Las notas del orador que el autor editó en Canva se toman de practico2/notas_autor.json.
"""

import argparse
import importlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "practico2"))

from guion import notas  # noqa: E402
import pptx_kit  # noqa: E402
from pptx_kit import new_presentation  # noqa: E402
import primera_parte  # noqa: E402

GRUPOS = ["g1", "g2", "g3", "g4", "g5", "g6"]
NOTAS_AUTOR = HERE / "practico2" / "notas_autor.json"
DIAGRAMAS_AUTOR = HERE / "practico2" / "diagramas_autor.json"


def oe1(prs, n):
    """Láminas 35-45 en el orden que dejó el autor en Canva."""
    import g0
    g0.construir(prs, n)
    return g0.DIAGRAMAS


def marco_practico(prs, n):
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ext", default=str(HERE / "build" / "ext"))
    ap.add_argument("--out", default=str(HERE / "presentacion_trabajo_grado_canva.pptx"))
    ap.add_argument("--completa", action="store_true",
                    help="convierte las 90 láminas originales (fondo oscuro, sin condensar)")
    ap.add_argument("--preview", action="store_true",
                    help="ajusta el texto de una línea para previsualizar con LibreOffice")
    ap.add_argument("--sin-gif", action="store_true", help="no regenera los GIF animados")
    a = ap.parse_args()
    pptx_kit.OPT_DIR = str(HERE / "build" / "img")
    n = notas()
    prs = new_presentation()

    if a.completa:
        from practico import add_practical_slide
        import practico
        pptx_kit.TEMA = "oscuro"
        practico.SINGLE_LINE_WRAP = a.preview
        ext = Path(a.ext)
        primera_parte.construir(prs, n)
        for i in range(35, 91):
            add_practical_slide(prs, ext / f"s{i:02d}.json", ext / f"s{i:02d}_deco.png",
                                ext / "deco", n[i])
    else:
        primera_parte.construir(prs, n)
        diagramas = oe1(prs, n)
        marco_practico(prs, n)
        # notas del orador tal como las dejó el autor en Canva
        if NOTAS_AUTOR.exists():
            autor = json.loads(NOTAS_AUTOR.read_text(encoding="utf-8"))
            for i, slide in enumerate(prs.slides, 1):
                t = autor.get(str(i))
                if t:
                    slide.notes_slide.notes_text_frame.text = t
        anim = pptx_kit.escribir_animaciones(prs)
        print(f"animaciones de entrada en {anim} láminas")
        if not a.sin_gif:
            import animaciones
            man = animaciones.generar(prs)
            autor = json.loads(DIAGRAMAS_AUTOR.read_text(encoding="utf-8")) \
                if DIAGRAMAS_AUTOR.exists() else {}
            for clave, d in diagramas.items():
                d["media"] = autor.get(clave, {}).get("media")
            (animaciones.OUT / "diagramas.json").write_text(
                json.dumps(diagramas, indent=1, ensure_ascii=False), encoding="utf-8")
            print(f"{len(man)} GIF animados -> {animaciones.OUT}")

    prs.core_properties.title = "Presentación de trabajo de grado"
    prs.core_properties.author = "Pablo Enrique Cañez Larico"
    prs.save(a.out)
    print(f"{len(prs.slides)} laminas -> {a.out}")


if __name__ == "__main__":
    main()
