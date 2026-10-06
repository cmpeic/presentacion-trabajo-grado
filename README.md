# Presentación dinámica — Trabajo de grado

Composición HyperFrames 1920×1080 preparada para editar por etapas.

## Editar

Haga doble clic en `ABRIR_EDITOR.cmd`. El archivo inicia HyperFrames Studio y abre:

```text
http://localhost:4567/#project/presentacion-trabajo-grado
```

No abra `index.html` como editor: ese archivo es el código fuente. Al abrirlo directamente solo se muestra una vista estática de la carátula.

## Presentar

Haga doble clic en `PRESENTAR.cmd`. Levanta un servidor local y abre el reproductor a pantalla completa:

```text
http://localhost:4600/presentar.html
```

El reproductor escala la composición a cualquier pantalla o proyector sin recortarla. Controles:

| Control | Acción |
|---|---|
| `Enter` / `Clic izquierdo` | **Avanzar a la siguiente lámina** (con transición fluida) |
| `Espacio` / `→` / `AvPág` | Avanzar a la siguiente lámina (en modo manual) |
| `←` / `Backspace` / `RePág` / `Clic derecho` | **Retroceder a la lámina anterior** |
| `M` | **Alternar Modo**: Manual (por defecto para defensa) vs Automático (por tiempos) |
| `1`–`9` | Saltar a un capítulo principal |
| `Inicio` / `Fin` | Ir a la primera / última lámina |
| `F` | Pantalla completa |

La barra inferior incluye contador de lámina (ej. `Lámina 15 / 90`), selector de modo, control de capítulos y se oculta automáticamente. `servidor.js` es el servidor estático (Node, sin dependencias) y también puede iniciarse a mano con `node servidor.js 4600`.

## Contenido actual

- Carátula con logos oficiales de EMI e Ingeniería de Sistemas.
- Introducción con una imagen principal, previsualización permanente de las otras imágenes y 10 segundos de exposición por imagen.
- Antecedentes con mosaico inicial de 6 segundos y enfoque ampliado de 10 segundos para cada una de las 6 imágenes numeradas.
- Planteamiento del problema con un tablero inicial de 5 segundos y 4 enfoques causa–efecto de 10 segundos, con rótulos y flechas de relación.
- Formulación del problema, objetivo general, hipótesis, identificación de variables y matriz de operacionalización.
- Esquema del marco teórico con 12 temas, imagen principal, título y guía numerada; 3 segundos por tema.
- Marco práctico con 56 láminas repartidas en 11 segmentos navegables:

| Segmento | Láminas | Objetivo |
|---|---:|---|
| Análisis actual | 1–8 | OE1 — proceso manual, BPMN y tiempos |
| Identificar atributos | 9–11 | OE2 — columnas, señales y calidad |
| Extraer productos | 12–16 | OE2 — fuentes históricas y contratos de datos |
| Seleccionar campos | 17–19 | OE2 — campos textuales por fuente |
| Estructurar conjunto | 20–21 | OE2 — unidad canónica y ambigüedades |
| Análisis exploratorio | 22–23 | OE2 — hallazgos y escala del corpus |
| Pipeline textual | 24–26 | OE3 |
| **Modelos algorítmicos** | **27–38** | OE4 — 12 láminas |
| Evaluación técnica | 39–43 | OE5 |
| **Evidencia externa** | **44–47** | Gold externo y benchmark multipaís |
| **Contraste operativo e hipótesis** | **48–56** | OE6 — línea base, latencia, métricas, ecuaciones, contrastación y cierre |

Las láminas de objetivos son esquemáticas —tablas, tarjetas de cifra, barras y
matrices—, sin bloques extensos de prosa. OE2 utiliza exclusivamente elementos
nativos de la presentación, sin imágenes. Toda cifra se cita literal de
`docs/objetivos/`.

Todas las cifras de resultados corresponden a la **corrida oficial v7.5**
(2.365 publicaciones, 19 países, 42 retailers, 54,21 % de automatización,
94,54 % de coincidencia selectiva y 70 desacuerdos externos). Las corridas
anteriores no se mezclan.

Las láminas 33–38, 42–43 y 44–47 muestran **títulos de producto reales** tomados
de los CSV de `reports/`: la consulta tal como el retailer la publicó, los
candidatos que el modelo recuperó con su puntuación, el score y el margen del
cross-encoder, y si la decisión fue correcta. Los títulos se copian verbatim
—incluidos los que están en cirílico, húngaro o finés— porque son la evidencia.

Duración total actual: 23 minutos y 25 segundos (1.405 s). El ritmo se gobierna
con `pacingMultiplier` al inicio del script del timeline: cambiar ese número
reescala todas las posiciones de una sola vez.

## Guion de defensa

[`GUION.md`](GUION.md) trae el texto hablado de cada lámina con su minuto exacto,
dimensionado a 2,4 palabras por segundo. Incluye un anexo con las cifras para el
turno de preguntas y tres preguntas probables ya respondidas.

## Sustituir una imagen

En `index.html`, localice el contenedor con `data-image-slot` y agregue dentro:

```html
<img src="assets/nombre-de-la-imagen.png" alt="" />
```

Las reglas CSS de `.image-slot img` adaptan automáticamente la imagen con `object-fit: cover`. Para mostrar una imagen completa sin recorte, cambie esa regla puntual a `object-fit: contain`.

## Comandos HyperFrames

```powershell
npx.cmd hyperframes lint
npx.cmd hyperframes validate
npx.cmd hyperframes inspect --samples 15
npx.cmd hyperframes preview
npx.cmd hyperframes render --output trabajo-grado.mp4 --quality high
```

La composición fue validada con HyperFrames: lint sin errores, contraste WCAG AA aprobado e inspección de layout sin errores ni advertencias.
