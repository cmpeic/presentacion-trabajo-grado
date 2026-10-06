# Versión Canva de la presentación

Esta carpeta genera `presentacion_trabajo_grado_canva.pptx` (1920×1080). Está
pensado para importarse en Canva como diseño editable: los textos quedan como
texto, las cajas como formas y los íconos como imágenes. Cada lámina lleva sus
notas del orador tomadas de `GUION.md`.

La versión por defecto tiene 67 láminas. El marco práctico, desde la lámina 44,
está rediseñado y condensado: 47 láminas originales pasan a 23, más la lámina
de contrastación estadística (McNemar) que agregó el autor. Con `--completa` se
obtiene la conversión directa de las 90 láminas originales.

## Estilo

Sigue la imagen de referencia de la presentación:

- fondo azul profundo con retícula (`fondo.png`);
- encabezado con cuadro amarillo, título en mayúsculas, filete azul y logo blanco;
- paneles oscuros con borde azul fino y esquineros amarillos.

Las fuentes son Montserrat (títulos), Barlow (texto) y Roboto Mono (código), todas
disponibles en Canva. Barlow reemplaza a Bahnschrift y Montserrat a Cambria.

## Estructura

| Archivo | Función |
|---|---|
| `pptx_kit.py` | Primitivas en píxeles: rectángulos, texto, imágenes, esquineros y transparencias. |
| `theme.py` | Paleta, encabezado, paneles y distintivos numerados. |
| `primera_parte.py` | Láminas 1-34: carátula, introducción, antecedentes, problema, formulación, objetivo, hipótesis, variables, matriz y marco teórico. |
| `practico.py` | Láminas 35-43 (y 35-90 con `--completa`): convierte en formas y texto nativos las primitivas extraídas de `index.html`. |
| `componentes.py` | Componentes del rediseño: tarjetas, cifras, chips, barras, flechas y ecuaciones con fracciones, sumatorias y exponentes. |
| `practico2/` | Marco práctico rediseñado (`g1.py` a `g6.py`), la lámina de McNemar (`mcnemar.py`), la guía de diseño, el contenido original de referencia, `check_cifras.py` (cada cifra debe existir en el original) y `preview.py`. |
| `guion.py` | Notas del orador por lámina, a partir de `GUION.md`. |
| `extraer/` | Playwright: abre `index.html`, avanza el timeline a cada lámina y extrae cajas, textos, imágenes y decoraciones. |
| `build/ext/` | Resultado de la extracción (JSON y PNG de decoraciones). Permite reconstruir el PPTX sin Node. |
| `construir.py` | Arma el PPTX final. |

## Reconstruir

```bash
# Solo si cambió index.html (requiere Node, Playwright y las fuentes TTF en ~/.fonts)
cd canva/extraer && npm install && node run_extract.js ../build/ext 35 90 && cd ../..

# Armar el PPTX (versión condensada; --completa para las 90 láminas)
python3 canva/construir.py

# Previsualizar o verificar cifras de un grupo del marco práctico
python3 canva/practico2/preview.py g3
python3 canva/practico2/check_cifras.py g1 g2 g3 g4 g5 g6 mcnemar
```

Para importarlo en Canva: subir el PPTX en *Crear un diseño → Importar archivo*, o
importarlo desde la URL pública del archivo en GitHub.
