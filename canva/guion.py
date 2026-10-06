"""Extrae del GUION.md las notas del orador para cada una de las 90 laminas."""

import re
from pathlib import Path

GUION = Path(__file__).resolve().parent.parent / "GUION.md"


def _plain(s: str) -> str:
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"(?<!\w)\*(.+?)\*(?!\w)", r"\1", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def _quote_after(lines, start):
    """Une las lineas '>' que siguen a la posicion start."""
    out = []
    i = start + 1
    while i < len(lines) and not lines[i].startswith(">"):
        if lines[i].startswith("#") or lines[i].startswith("**"):
            return ""
        i += 1
    while i < len(lines) and lines[i].startswith(">"):
        out.append(lines[i].lstrip("> ").rstrip())
        i += 1
    return _plain(" ".join(out))


def notas() -> dict[int, str]:
    lines = GUION.read_text(encoding="utf-8").splitlines()
    res: dict[int, str] = {}

    def find(pattern):
        for i, l in enumerate(lines):
            if re.search(pattern, l):
                return i
        raise KeyError(pattern)

    res[1] = _quote_after(lines, find(r"^## Carátula"))
    for k, pat in enumerate([r"imagen 1 ·", r"imagen 2 ·", r"imagen 3 ·", r"imagen 4 ·"]):
        res[2 + k] = _quote_after(lines, find(r"^\*\*0:\d\d — " + pat))
    res[6] = "Mosaico de antecedentes: vista general de los seis antecedentes antes del detalle."
    for k in range(6):
        res[7 + k] = _quote_after(lines, find(r"^\*\*1:\d\d — 0%d ·" % (k + 1)))
    res[13] = _quote_after(lines, find(r"el tablero completo"))
    for k in range(4):
        res[14 + k] = _quote_after(lines, find(r"causa y efecto 0%d\*\*" % (k + 1)))
    res[18] = _quote_after(lines, find(r"— formulación del problema\*\*"))
    res[19] = _quote_after(lines, find(r"— objetivo general\*\*"))
    res[20] = _quote_after(lines, find(r"— hipótesis de investigación\*\*"))
    res[21] = _quote_after(lines, find(r"^## 1\.5\.2 Identificación"))
    res[22] = _quote_after(lines, find(r"^## Matriz de operacionalización"))

    # Marco teorico: un parrafo continuo con marcas (m:ss) para los 12 temas.
    mt = _quote_after(lines, find(r"^## Esquema del marco teórico"))
    partes = re.split(r"\(\d:\d\d\)", mt)
    intro, temas = partes[0].strip(), [p.strip() for p in partes[1:]]
    for k, frag in enumerate(temas[:12]):
        res[23 + k] = (intro + " " + frag).strip() if k == 0 else frag

    for i, l in enumerate(lines):
        m = re.match(r"^### .*Lámina (\d\d) — ", l)
        if m:
            res[34 + int(m.group(1))] = _quote_after(lines, i)
    return res


if __name__ == "__main__":
    n = notas()
    for k in sorted(n):
        print(k, n[k][:90])
    print(len(n))
