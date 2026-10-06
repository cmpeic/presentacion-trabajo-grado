# Guía para rediseñar el marco práctico (láminas 44-90 → 23 láminas)

El autor pidió: mejorar el diseño de la lámina 44 en adelante, reducir a lo
necesario según el proyecto y mejorar los esquemas. Las láminas nuevas usan el
mismo estilo que las láminas 1-34 (fondo azul con retícula, encabezado con
cuadro amarillo, paneles oscuros con borde azul fino, esquineros amarillos).

## Fuentes de contenido (no inventar nada)

- `canva/practico2/contenido_original.md`: todos los textos y cifras de las
  láminas 44-90 y su nota del orador.
- Capturas del original: `/tmp/claude-0/-home-user-TESIS-PCANEZ/01135701-0272-5f86-89bd-c0f636550cdc/scratchpad/shots/sNN.png`.
- `GUION.md` (raíz del repo): guion completo y anexo de cifras.

**Regla de fidelidad:** cada cifra, código, nombre de columna y nombre de
retailer que aparezca en una lámina nueva debe existir tal cual en
`contenido_original.md`, con el mismo formato (coma decimal, punto de miles,
signo de porcentaje). Se puede acortar la redacción, pero no cambiar el sentido.
Si una cifra no se puede comprobar, no se usa. Español con tildes correctas.

## Esquema de fusión (23 láminas nuevas)

| ID | Grupo | Lámina nueva (título orientativo) | Origen |
|---|---|---|---|
| P01 | g1 | Atributos que deciden y filtros de calidad | 44 + 45 |
| P02 | g1 | Siete fuentes del corpus: contrato y escala | 46, 47, 48, 49, 50 + 57 |
| P03 | g1 | De 36 columnas a dos vistas comparables | 51 + 52 + 53 |
| P04 | g2 | Del volcado del portal a la unidad de análisis (incluye «lo ambiguo se marca») | 54 + 55 |
| P05 | g2 | Los tres hallazgos que condicionan todo | 56 |
| P06 | g2 | Cinco fuentes, un solo pipeline (con el título real que lo atraviesa) | 58 + 59 |
| P07 | g2 | Qué se destruye, qué se conserva, qué se gana | 60 |
| P08 | g3 | Qué puede mirar cada modelo (con los cuadrantes de atención cruzada) | 61 + 62 |
| P09 | g3 | Protocolo sin fuga y 17 configuraciones evaluadas | 63 + 69 |
| P10 | g3 | Siete medidas de similitud, tres funciones | 64 |
| P11 | g3 | Arquitectura: la cascada y la escalera de decisión | 65 + 66 |
| P12 | g4 | El recuperador en dos casos reales | 67 + 68 |
| P13 | g4 | Dónde duda el modelo: el margen y los cuatro falsos positivos | 70 + 71 + 72 |
| P14 | g4 | Recall@1 sobre las 147 consultas de test | 73 |
| P15 | g5 | Clasificación de pares y negativos difíciles | 74 + 75 |
| P16 | g5 | Matriz de confusión y techo del recuperador | 76 + 77 |
| P17 | g5 | Evidencia externa: gold y benchmark multipaís | 78 + 80 |
| P18 | g5 | Casos reales fuera del dataset: cuándo automatiza y cuándo se abstiene | 79 + 81 |
| P19 | g6 | Tiempo de validación: línea base manual frente a latencia del modelo (ecuaciones) | 82 + 83 + 87 (tiempos) |
| P20 | g6 | Escenario operativo asistido (tabla + ecuaciones de reducción) | 84 + 87 (reducciones) |
| P21 | g6 | Consistencia de la calidad (ecuaciones de las métricas + evidencia externa y de uso) | 85 + 86 |
| P22 | g6 | Contrastación de la hipótesis (matriz + veredicto) | 88 + 89 |
| P23 | g6 | Gracias (cierre con el estilo de la carátula) | 90 |

Al fusionar se conserva el mensaje central de cada lámina de origen (ver su nota
del orador). Lo que se recorta son repeticiones, detalles de implementación y
texto largo: priorizar cifras clave y esquemas.

## Reglas de diseño

- Encabezado: `subencabezado(s, antetitulo, titulo)` de `componentes.py`. El
  antetítulo indica el objetivo específico y el tema, por ejemplo
  `OE2 · Organizar el conjunto de datos`. El título es una frase corta (cabe en
  una línea de 1728 px a 40 px, unos 60 caracteres como máximo).
- Zona de contenido: x 96..1824, y 268..1010. Márgenes interiores de 24 a 32 px.
- Una idea focal por lámina: una cifra grande, un diagrama o una tabla clara.
- Texto corrido: como máximo unas 60 palabras por lámina, sin contar rótulos ni
  cifras. Tamaño mínimo 18 px (20 px o más para texto que se lee); el cuerpo,
  entre 22 y 26 px.
- Tipografía: títulos de tarjeta en Montserrat negrita (26-32 px), cifras
  grandes en Montserrat negrita amarilla (48-80 px), cuerpo en Barlow, código e
  identificadores en Roboto Mono amarillo (`chip`).
- Color: amarillo = lo destacado, elegido o favorable; azul (`BLUE_LIGHT`) =
  dato neutro; rojo (`RED`) = error o desfavorable; `MUTED` = texto
  secundario. Fondo de tarjetas `PANEL`/`PANEL_2`, pistas de barra `CHIP`.
- Esquineros amarillos (`corners` o `card(..., brackets=True)`) solo en el panel
  principal de cada lámina, como mucho uno o dos.
- Esquemas: flechas de bloque (`flecha`, `flecha_abajo`), cajas con número
  (`numbadge`), barras proporcionales (`bar`), etiquetas de estado (`tag`).
  Las proporciones de las barras deben corresponder a los valores reales.
- Ecuaciones: siempre con `ecuacion(...)` (fracciones y sumatorias reales),
  nunca escritas en línea como «(a + b) / c».
- **Una sola familia de fuente por cuadro de texto**: Canva aplica una fuente
  por cuadro al importar. Mezclar negrita y colores dentro de un cuadro está
  bien; mezclar Montserrat, Barlow y Roboto Mono, no. Usar cuadros separados.
- `wrap=False` solo en cuadros pequeños con ancho medido (chips, ecuaciones). En
  el resto usar cuadros con ancho suficiente: LibreOffice, que se usa para
  previsualizar, centra los cuadros sin ajuste de línea.
- Íconos opcionales del proyecto en `assets/` (por ejemplo,
  `assets/marco-teorico/*.png`), con `image_fit(..., trim=True)`.

## Estructura de cada módulo

Archivo `canva/practico2/gN.py`:

```python
"""Grupo gN: <tema>."""
from pptx_kit import add_slide, notes, rect, text, image_fit, line, ellipse
from theme import FONDO, YELLOW, BLUE_LIGHT, PAPER, MUTED, PANEL, SURFACE, LINE
from componentes import *  # subencabezado, card, kpi, chip, tag, bar, flecha, ecuacion, ...

def p01(prs, notas):
    s = add_slide(prs, bg_image=FONDO)
    subencabezado(s, "OE2 · Organizar el conjunto de datos", "Atributos que deciden ...")
    ...
    notes(s, " ".join(notas[i] for i in (44, 45)))

def construir(prs, notas):
    p01(prs, notas); p02(prs, notas); ...
```

`notas` es el dict de `canva/guion.py` (`notas()[n]` = nota de la lámina original
n). La nota de una lámina fusionada concatena, en orden, las notas de sus
láminas de origen.

## Previsualizar

```bash
python3 canva/practico2/preview.py gN
```

Genera `canva/build/preview/gN/pNN.png` (una por lámina) y
`canva/build/preview/gN/hoja.png`. Abre las PNG con Read, revisa cada lámina con
ojo crítico (texto cortado o desbordado, solapes, alineaciones, jerarquía,
espacio vacío mal usado, coherencia con la referencia) y corrige. Repite hasta
que estén limpias.
