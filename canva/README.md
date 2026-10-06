# Versión Canva de la presentación

Esta carpeta genera `presentacion_trabajo_grado_canva.pptx`, un PPTX de 90 láminas
(1920×1080). Está pensado para importarse en Canva como diseño editable: los textos
quedan como texto, las cajas como formas y los íconos como imágenes. Cada lámina
lleva sus notas del orador tomadas de `GUION.md`.

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
| `practico.py` | Láminas 35-90: convierte en formas y texto nativos las primitivas extraídas de `index.html`. |
| `guion.py` | Notas del orador por lámina, a partir de `GUION.md`. |
| `extraer/` | Playwright: abre `index.html`, avanza el timeline a cada lámina y extrae cajas, textos, imágenes y decoraciones. |
| `build/ext/` | Resultado de la extracción (JSON y PNG de decoraciones). Permite reconstruir el PPTX sin Node. |
| `construir.py` | Arma el PPTX final. |

## Reconstruir

```bash
# Solo si cambió index.html (requiere Node, Playwright y las fuentes TTF en ~/.fonts)
cd canva/extraer && npm install && node run_extract.js ../build/ext 35 90 && cd ../..

# Armar el PPTX
python3 canva/construir.py
```

Para importarlo en Canva: subir el PPTX en *Crear un diseño → Importar archivo*, o
importarlo desde la URL pública del archivo en GitHub.
