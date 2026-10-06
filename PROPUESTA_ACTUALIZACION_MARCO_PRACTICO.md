# Propuesta de actualización del Marco Práctico

## Objetivo de la actualización

Reorganizar el desarrollo práctico para que la defensa siga la secuencia de las redacciones 4.2 a 4.6, mantenga la trazabilidad de cada objetivo específico y cierre con la aceptación de la hipótesis dentro del alcance del estudio. La propuesta reduce las 49 láminas prácticas a 34 láminas principales. Las láminas técnicas restantes pueden conservarse como anexos para preguntas.

## Distribución general sugerida

| Bloque | Tiempo | Láminas | Función narrativa |
|---|:---:|:---:|---|
| OE1. Proceso actual y metodologías | 4:15–6:15 | 1–5 | Establecer la línea base operativa y justificar el enfoque de desarrollo. |
| OE2. Organización del conjunto de datos | 6:15–8:45 | 6–11 | Explicar el origen, estructura, depuración y principales características del corpus. |
| OE3. Pipeline de procesamiento textual | 8:45–10:05 | 12–15 | Mostrar cómo el texto heterogéneo se convierte en información comparable sin perder códigos técnicos. |
| OE4. Modelos algorítmicos | 10:05–14:30 | 16–23 | Presentar las tres familias de modelos y la arquitectura híbrida final. |
| OE5. Evaluación técnica | 14:30–18:05 | 24–29 | Comparar los modelos con protocolos, métricas y conjuntos claramente diferenciados. |
| OE6. Contraste operativo e hipótesis | 18:05–21:05 | 30–34 | Relacionar calidad, tiempo, uso controlado y aceptación de la hipótesis. |

## Desarrollo propuesto por lámina

### OE1. Analizar el proceso actual

| N.º | Título sugerido | Contenido imprescindible | Recurso visual |
|---:|---|---|---|
| 1 | Metodologías seleccionadas | Escala común y resultado de CRISP-DM y Kanban. | Comparación resumida con la opción seleccionada. |
| 2 | Actores y responsabilidades | Web Scraping, Product Matching y QA. | Flujo horizontal de responsabilidades. |
| 3 | Proceso manual AS-IS | Recepción, revisión, búsqueda, decisión y control QA. | BPMN AS-IS simplificado. |
| 4 | Proceso asistido TO-BE | Recuperación, puntuación, compuertas y revisión humana. | BPMN TO-BE con el modelo destacado. |
| 5 | Línea base operativa | 440 productos por analista, 4.400 por equipo y tiempos por complejidad. | Distribución de tiempos y capacidad. |

### OE2. Organizar el conjunto de datos

| N.º | Título sugerido | Contenido imprescindible | Recurso visual |
|---:|---|---|---|
| 6 | Origen y trazabilidad de los datos | Exportaciones históricas, fuentes recibidas, almacenamiento en `data/raw` e integridad. | Mapa de fuentes y contratos. |
| 7 | Los 36 atributos del portal | Identidad, texto del fabricante, publicación retailer, geografía y calidad. | Agrupación por función, no listado completo. |
| 8 | Depuración y unidad de análisis | 129.507 filas iniciales, filtros, 127.093 válidas y unidad canónica. | Embudo de depuración. |
| 9 | Estructura del conjunto de estudio | Pares, publicaciones, productos oficiales y fuentes auxiliares. | Diagrama de entidades y cardinalidades. |
| 10 | Partición temporal | Entrenamiento enero–octubre, validación noviembre y prueba diciembre. | Línea temporal con separación estricta. |
| 11 | Hallazgos del análisis exploratorio | Repetición histórica, códigos dentro del texto, sufijos y presencia multilingüe. | Tres hallazgos con una consecuencia de diseño por cada uno. |

### OE3. Definir el pipeline textual

| N.º | Título sugerido | Contenido imprescindible | Recurso visual |
|---:|---|---|---|
| 12 | Diseño del pipeline común | Cinco preparadores de fuente y una secuencia común de transformación. | Arquitectura de entrada común. |
| 13 | Normalización técnica | Unicode, minúsculas, unidades, puntuación útil y limpieza controlada. | Antes y después de un título real. |
| 14 | Extracción de códigos | Separación de códigos, EAN y sufijos sin destruir la señal original. | Despiece visual del título. |
| 15 | Calidad y reproducibilidad | Idempotencia, banderas de calidad y columnas generadas. | Contrato de salida del pipeline. |

### OE4. Diseñar los modelos algorítmicos

| N.º | Título sugerido | Contenido imprescindible | Recurso visual |
|---:|---|---|---|
| 16 | Dos tareas dentro del product matching | Recuperación de candidatos y validación de pares. | División del problema en dos etapas. |
| 17 | Modelo 1: TF-IDF | N-gramas de caracteres, texto enriquecido y función de recuperador. | Consulta y ranking top-10. |
| 18 | Modelo 2: embeddings | Dos codificadores por tres vistas, sin ajuste de pesos, usados para complementar candidatos. | Espacio vectorial y seis configuraciones. |
| 19 | Modelo 3: cross-encoder | Lectura conjunta, entrenamiento supervisado y clasificación binaria del par. | Secuencia conjunta retailer–catálogo. |
| 20 | Pares de entrenamiento y negativos difíciles | Exactos, sufijos distintos, reacondicionados y combinaciones. | Taxonomía de negativos. |
| 21 | Cascada de candidatos | TF-IDF top-10 más embeddings top-10, unión de hasta 20 y reranking. | Embudo con techo del 91,84 %. |
| 22 | Política operacional | Score mínimo, margen mínimo, contradicciones técnicas y abstención `Review`. | Compuertas de decisión con los umbrales documentados. |
| 23 | Sistema integrado Human-in-the-Loop | Reglas, enrutador, recuperación, Transformer y revisión humana. | Arquitectura completa y responsabilidades. |

### OE5. Evaluar el desempeño técnico

| N.º | Título sugerido | Contenido imprescindible | Recurso visual |
|---:|---|---|---|
| 24 | Protocolos y denominadores | Diferenciar clasificación de pares, ranking de consultas y operación. | Tres columnas con unidad y conjunto de prueba. |
| 25 | Comparación de clasificación | Accuracy, precisión, recall, F1 y FPR de los tres modelos. | Barras comparativas con denominador visible. |
| 26 | Matriz de confusión del Modelo 3 | TP, TN, FP y FN sobre los 344 pares. | Matriz de confusión legible. |
| 27 | Desempeño en negativos difíciles | Sufijos y reacondicionados frente a TF-IDF y embeddings. | Comparación de FPR por cohorte. |
| 28 | Recuperación y techo del pool | Recall@1, Recall@5, MRR y 12 consultas irrecuperables. | Embudo 147, 135 y 121. |
| 29 | Evidencia externa | Gold de 213 consultas y benchmark v7.5 de 2.365 publicaciones. | Dos pruebas separadas y sus alcances. |

### OE6. Contrastar con el proceso manual

| N.º | Título sugerido | Contenido imprescindible | Recurso visual |
|---:|---|---|---|
| 30 | Línea base manual observada | Tiempo agregado de 16,608 segundos por publicación-semana y contexto de los registros. | Línea base con fuente y unidad. |
| 31 | Latencia del sistema | 6,5166 segundos por consulta en v7.5 y tiempo total de ejecución. | Comparación unitaria manual–modelo. |
| 32 | Escenario operativo asistido | Horas humanas liberadas, tiempo de máquina y escenario de capacidad. | Dos procesos sobre el mismo lote. |
| 33 | Consistencia durante la evaluación y el uso | 96,89 % de exactitud del Modelo 3, 94,54 % de coincidencia selectiva y cero errores registrados durante el uso controlado. | Separar evaluación retrospectiva de uso controlado. |
| 34 | Contraste y aceptación de la hipótesis | Evidencia de VD₁, evidencia de VD₂, conclusión y alcance. | La misma cadena VI–VD utilizada en la lámina de hipótesis, ahora completada con resultados. |

## Criterios de exposición

- Cada lámina debe responder una sola pregunta y conservar únicamente el dato necesario para defender la decisión tomada.
- Las tablas completas, ecuaciones generales, listados de columnas, configuraciones descartadas y casos adicionales deben pasar al anexo.
- Cada porcentaje debe mostrar su denominador o el conjunto al que pertenece.
- La evaluación retrospectiva y el uso controlado deben presentarse como evidencias distintas.
- El cierre debe reutilizar la estructura visual de la hipótesis para mostrar cómo cada variable dependiente recibió evidencia.

## Nueva descripción del bloque 5

| Bloque | Rango de tiempo | Propósito y contenido |
|---|:---:|---|
| **5. Formulación, objetivo, hipótesis y variables** | **2:50–3:37** | Pregunta de investigación, objetivo general, relación VI–VD de la hipótesis, identificación de variables y matriz de operacionalización. |
