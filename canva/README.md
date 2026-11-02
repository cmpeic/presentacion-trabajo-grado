# Versión Canva de la presentación

Esta carpeta genera `presentacion_trabajo_grado_canva.pptx` (1920×1080). Está
pensado para importarse en Canva como diseño editable: los textos quedan como
texto, las cajas como formas y los íconos como imágenes. Cada lámina lleva sus
notas del orador tomadas de `GUION.md`.

La versión por defecto tiene 69 láminas, en el orden que dejó el autor en Canva:
incluye sus diagramas (flujo lógico, BPMN AS-IS en dos partes, BPMN propuesto y
subproceso), la lámina de tiempos manuales y la contrastación estadística
(McNemar). Con `--completa` se obtiene la conversión directa de las 90 láminas
originales en el estilo oscuro anterior.

## Estilo

Fondo blanco en todo el documento:

- encabezado con el logo de la EMI a la izquierda, el logo de la carrera a la
  derecha y la sección centrada entre filetes dorados;
- banda azul y amarilla de la EMI al pie, con el número de lámina;
- carátula y cierre con título y nombre en mayúsculas.

Las láminas se diseñan con la paleta original y `pptx_kit` traduce cada color al
emitirlo (`TEMA = "claro"`): los rellenos azul noche pasan a tintes claros y el
color de cada texto se decide según lo que tiene detrás, así el blanco sobre azul
sigue siendo blanco y el blanco sobre una tarjeta clara pasa a tinta oscura.

## Movimiento

- Animaciones de entrada nativas del PPTX (barras y flechas que entran, cifras que
  aparecen) y transición suave entre láminas.
- Gráficas animadas en `animaciones/`: cada gráfica de barras tiene un video WebM transparente con las
  barras creciendo y la carátula y el cierre tienen la red neuronal con pulsos.
  `manifiesto.json` indica la lámina y la caja exacta donde va cada video; se
  insertan sobre la lámina importada en Canva (las barras estáticas quedan debajo
  como respaldo).
- `animaciones/diagramas.json` indica dónde van los diagramas del autor, que se
  reemplazan en Canva por sus imágenes originales.

Las fuentes son Montserrat (títulos), Barlow (texto) y Roboto Mono (código), todas
disponibles en Canva. Barlow reemplaza a Bahnschrift y Montserrat a Cambria.

## Estructura

| Archivo | Función |
|---|---|
| `pptx_kit.py` | Primitivas en píxeles: rectángulos, texto, imágenes, esquineros y transparencias. |
| `theme.py` | Paleta, encabezado, paneles y distintivos numerados. |
| `primera_parte.py` | Láminas 1-34: carátula, introducción, antecedentes, problema, formulación, objetivo, hipótesis, variables, matriz y marco teórico. |
| `practico.py` | Solo con `--completa` (láminas 35-90, estilo oscuro): convierte en formas y texto nativos las primitivas extraídas de `index.html`. |
| `componentes.py` | Componentes del rediseño: tarjetas, cifras, chips, barras, flechas y ecuaciones con fracciones, sumatorias y exponentes. |
| `practico2/` | OE1 rediseñado (`g0.py`: escala, metodologías, actores, diagramas del autor, tiempos y columnas), marco práctico (`g1.py` a `g6.py`), la lámina de McNemar (`mcnemar.py`), la guía de diseño, el contenido original de referencia, `check_cifras.py` (cada cifra debe existir en el original) y `preview.py`. |
| `guion.py` | Notas del orador por lámina, a partir de `GUION.md`. |
| `extraer/` | Playwright: abre `index.html`, avanza el timeline a cada lámina y extrae cajas, textos, imágenes y decoraciones. |
| `build/ext/` | Resultado de la extracción (JSON y PNG de decoraciones). Permite reconstruir el PPTX sin Node. |
| `animaciones.py` | Genera los videos animados con transparencia (barras que crecen, red neuronal) y su manifiesto; requiere ffmpeg. |
| `construir.py` | Arma el PPTX final, sus animaciones y los videos. |

## Reconstruir

```bash
# Solo si cambió index.html (requiere Node, Playwright y las fuentes TTF en ~/.fonts)
cd canva/extraer && npm install && node run_extract.js ../build/ext 35 90 && cd ../..

# Armar el PPTX en fondo blanco, con animaciones y videos (--completa: 90 láminas, estilo oscuro)
python3 canva/construir.py

# Previsualizar o verificar cifras de un grupo del marco práctico
python3 canva/practico2/preview.py g3
python3 canva/practico2/check_cifras.py g1 g2 g3 g4 g5 g6 mcnemar
```

Para importarlo en Canva: subir el PPTX en *Crear un diseño → Importar archivo*, o
importarlo desde la URL pública del archivo en GitHub.
