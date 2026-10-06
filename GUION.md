# Guion de defensa — Trabajo de grado

Guion hablado, sincronizado con la composición. **Duración total: 23:25 (1.405 s).**

Cada bloque lleva el minuto exacto en que la lámina entra en pantalla y su
permanencia. El texto está dimensionado a **unas 2,4 palabras por segundo**, que
es un ritmo de defensa tranquilo: si lo lee a esa velocidad, termina con la
lámina, no antes ni después.

- **Negrita** = cifra o nombre que conviene pronunciar con énfasis.
- Las cifras son las mismas que están en pantalla; no hay ninguna que no se vea.
- Todos los resultados corresponden a la **corrida oficial v7.5**.

| Segmento | Entra | Dura |
|---|---|---|
| Carátula | 0:00 | 17 s |
| Introducción | 0:16 | 42 s |
| Antecedentes | 0:59 | 66 s |
| Planteamiento del problema | 2:05 | 45 s |
| Formulación · Objetivo · Hipótesis | 2:50 | 48 s |
| Identificación de variables y matriz | 3:28 | 10 s |
| Esquema del marco teórico | 3:38 | 36 s |
| Marco práctico — 56 láminas | 4:15 | 19:10 |

---

## Carátula · 0:00 · 17 s

> Buenos días. Soy **Pablo Enrique Cañez Larico**. Presento el trabajo de grado
> «Modelo de Procesamiento de Lenguaje Natural en la validación de
> correspondencia de productos del ecosistema **Philips**», desarrollado en el
> área de operaciones de la empresa **Agilsoft**. Mi tutor es el ingeniero
> Víctor Rodríguez Estévez.

---

## Introducción · 0:16 · 42 s

**0:19 — imagen 1 · el ecosistema de comercios**

> El comercio electrónico publica el mismo producto en miles de tiendas, y cada
> tienda lo describe a su manera.

**0:29 — imagen 2 · el volumen de datos**

> Philips necesita saber qué está publicado de su marca en cada país. Eso exige
> cruzar millones de publicaciones contra un catálogo oficial.

**0:39 — imagen 3 · el enfoque**

> Ese cruce es un problema de lenguaje natural: dos textos que hablan del mismo
> objeto sin escribirlo igual.

**0:49 — imagen 4 · el operador**

> Hoy ese cruce lo resuelve una persona, publicación por publicación. Ahí empieza
> este trabajo.

---

## Antecedentes · 0:59 · 66 s

**1:05 — 01 · la empresa y los comercios**

> Agilsoft opera para Philips el monitoreo de sus productos en comercios de
> decenas de países.

**1:15 — 02 · la extracción automática**

> Un equipo de web scraping extrae automáticamente las publicaciones de cada
> retailer: título, precio, imagen y enlace.

**1:25 — 03 · la comparación manual**

> Lo que la extracción no resuelve es la correspondencia. Un analista abre la
> publicación y el catálogo, y decide si son el mismo producto.

**1:35 — 04 · el reparto del trabajo**

> El lote diario se reparte entre los analistas del turno. Cada uno arrastra su
> propio criterio.

**1:45 — 05 · los cuatro estados**

> La decisión no es binaria: el analista clasifica en **Match**, **NIC**,
> **Hidden** o **Delete**, según qué encontró y qué faltaba.

**1:55 — 06 · el control de calidad**

> Un área de Quality Assurance revisa una muestra y corrige. Es el único control
> que existe sobre la consistencia del criterio.

---

## Planteamiento del problema · 2:05 · 45 s

**2:05 — el tablero completo (5 s)**

> El problema tiene cuatro causas y cada una produce un efecto medible.

**2:10 — causa y efecto 01**

> Criterio no formalizado produce decisiones inconsistentes. Dos analistas pueden
> clasificar el mismo par de manera opuesta.

**2:20 — causa y efecto 02**

> El volumen de publicaciones crece continuamente y el tiempo de respuesta aumenta.

**2:30 — causa y efecto 03**

> La inspección es puramente visual: fatiga del operador y riesgo de error humano.

**2:40 — causa y efecto 04**

> Ausencia de trazabilidad en la decisión: no queda registro de *por qué* se aceptó
> o rechazó un par.

---

## Formulación · Objetivo · Hipótesis · 2:50 · 38 s

**2:50 — formulación del problema**

> ¿De qué manera la aplicación de un modelo de Procesamiento de Lenguaje Natural
> incide en la consistencia de la calidad del matching y en el tiempo de validación?

**3:06 — objetivo general**

> Diseñar e implementar un modelo basado en Procesamiento de Lenguaje Natural para
> validar la correspondencia de productos entre publicaciones de comercios electrónicos
> y los catálogos oficiales de Philips.

**3:22 — hipótesis de investigación**

> La aplicación de un modelo de Procesamiento de Lenguaje Natural mejora la consistencia
> de la calidad del matching y reduce el tiempo de validación respecto al proceso manual actual.

---

## 1.5.2 Identificación de las variables · 3:28

> Para contrastar esta hipótesis se definen tres variables:
> Como **variable independiente**, el **Modelo de Procesamiento de Lenguaje Natural** aplicado a la correspondencia de productos.
> Y como **variables dependientes**, los dos efectos medibles del problema: la **consistencia de la calidad del matching** y el **tiempo de validación**.

---

## Matriz de operacionalización de variables (Tabla 2) · 3:34

> La operacionalización descompone cada variable en dimensiones e indicadores concretos.
> La variable independiente se evalúa mediante la **arquitectura algorítmica** y su capacidad frente al ruido textual.
> La consistencia de la calidad se mide a través del **rendimiento predictivo** —con métricas de **Accuracy, Precisión, Recall y F1-score**— y la **estabilidad operativa** frente a la tasa de error humano.
> Y el tiempo de validación se cuantifica mediante la **eficiencia temporal en segundos**, comparando la latencia del modelo frente al promedio manual y evaluando el porcentaje de reducción alcanzado.

---

## Esquema del marco teórico · 3:38 · 36 s

*Doce temas de tres segundos. Léalo corrido, marcando la pausa en cada punto.*

> El marco teórico se organiza en doce temas. **(3:38)** Metodologías de
> desarrollo y **(3:41)** notación de modelado de procesos, que sostienen el
> método. **(3:44)** Fundamentos computacionales y **(3:47)** minería de texto y
> procesamiento de lenguaje natural, que son el núcleo. **(3:50)** Modelos de
> representación de texto, **(3:53)** correspondencia de entidades y **(3:56)**
> modelos de clasificación, que definen la solución. **(3:59)** Métricas de
> similitud, **(4:02)** evaluación de modelos y **(4:05)** medición de
> eficiencia, que permiten contrastar la hipótesis. Y por último **(4:08)**
> sistemas de apoyo a la decisión y **(4:11)** desarrollo web, para la entrega.

---
---

# Marco práctico

## Objetivo específico 1 — Analizar el proceso actual

### 4:15 · Lámina 01 — Escala de valoración de los criterios · 16 s

> Toda elección metodológica de este trabajo se decidió con la misma escala de
> uno a cinco, definida **antes** de comparar. Esto evita justificar a posteriori
> la opción que ya se prefería.

### 4:31 · Lámina 02 — Metodologías de ciencia de datos · 18 s

> Sobre cinco criterios, **CRISP-DM** obtiene **23 puntos** frente a **14** de KDD
> y **14** de SEMMA. Gana por dos razones concretas: comprensión del negocio e
> iteratividad, que es exactamente lo que exigía un problema definido por
> criterios operativos.

### 4:49 · Lámina 03 — Metodologías ágiles · 18 s

> Para la gestión, **Kanban** obtiene **30 puntos** frente a **21** de Scrum y
> **21** de XP. Pesó el seguimiento continuo sin sprints obligatorios y el bajo
> requerimiento de roles formales: el desarrollo lo ejecuta una sola persona.

### 5:07 · Lámina 04 — Actores del proceso · 18 s

> Tres actores. El equipo de **web scraping** entrega registros estructurados.
> Los **analistas de Product Matching** validan a mano contra el catálogo y
> producen la clasificación operativa. **Quality Assurance** supervisa y corrige.

### 5:25 · Lámina 05 — Diagrama de flujo lógico · 16 s

> Este es el criterio que hoy vive en la cabeza del analista, formalizado por
> primera vez. Nótese que la decisión no es «¿corresponde o no?»: es una cadena
> de preguntas que termina en **Match**, **NIC**, **Hidden** o **Delete**.

### 5:41 · Lámina 06 — BPMN del proceso actual · 16 s

> El proceso AS-IS. Todo el trabajo de decisión ocurre en un solo carril: el del
> analista. No hay ningún punto donde el sistema aporte evidencia.

### 5:57 · Lámina 07 — BPMN del proceso propuesto · 16 s

> El proceso propuesto. Aparece un carril de sistema automático que resuelve lo
> evidente y **prioriza** lo dudoso. El analista no desaparece: recibe menos
> casos y mejor preparados.

### 6:13 · Lámina 08 — Tiempos del proceso manual · 22 s

> La línea base, medida. Un caso fácil toma **15 a 30 segundos**; uno difícil,
> **60 a 120**. El promedio operativo es de **65 segundos** por producto, con una
> cuota de **440 productos** diarios por analista y **10 operadores** por turno:
> **4.400 productos por día**. Contra esta cifra se contrastará el resultado.

---

## Objetivo específico 2 — Organizar el conjunto de datos

### 6:35 · Lámina 09 — Las 36 columnas por rol · 18 s

> El dataset principal trae **36 columnas**. Agrupadas por rol se ve la
> estructura real: trazabilidad del snapshot, lado fabricante, lado retailer,
> geografía y calidad del match. Solo dos de esos grupos contienen el texto que
> el modelo va a leer.

### 6:53 · Lámina 10 — Las señales que deciden · 20 s

> Aquí está la asimetría del problema. El nombre del fabricante promedia **42
> caracteres**; el del retailer, **61**, y el **90,19%** contiene un token con
> forma de código. El identificador del retailer no es confiable: **8.528** casos
> aparecen reutilizados entre comercios distintos.

### 7:13 · Lámina 11 — Atributos de calidad y una trampa · 16 s

> Tres banderas sirven de filtro: **Invalid**, **IsDeleted** y
> **MatchConfidence**. La cuarta, **LinkIsValid**, parece un filtro y no lo es:
> describe el estado del enlace, no la validez de la correspondencia. Usarla
> habría descartado datos buenos.

### 7:29 · Lámina 12 — Fuente Hidden · 18 s

> Hidden aporta **15.355 filas** con solo cuatro columnas. Su contrato es de una
> sola clase: el pipeline se detiene si aparece un estado distinto de *Hidden*.
> Un contrato verificable vale más que una comprobación manual.

### 7:47 · Lámina 13 — Fuente NIC · 24 s

> NIC aporta **47.333 filas** y es la fuente más compleja: cinco columnas de
> contrato base más ocho de etiquetado heurístico. El **83%** queda como
> *unknown_review*. Por eso NIC no entra como verdad fuerte, sino con peso
> reducido — una decisión metodológica, no una limitación técnica.

### 8:11 · Lámina 14 — Catálogos oficiales · 22 s

> El catálogo oficial es la referencia contra la que se compara todo. Ucrania y
> Bélgica comparten contrato de **11 columnas**. La llave real es el
> **ProductId** con barra, como *BAR700/00*. Los dos campos de precio están en
> cero en todo el snapshot: por eso no se usan.

### 8:33 · Lámina 15 — Pares negativos · 18 s

> Es la única fuente que llega ya en forma de par etiquetado: **896 filas** con
> los dos textos y su etiqueta. Y trae el tipo de negativo — **sufijo distinto**
> y **reacondicionado** —, que es justamente lo que después va a costar más.

### 8:51 · Lámina 16 — Retailer de prueba · 20 s

> Esta fuente no tiene archivo físico hoy. Aun así el contrato es verificable,
> porque el código que lo consume lo declara y lo valida antes de leer. Es la
> diferencia entre documentar un supuesto y hacerlo comprobable.

### 9:11 · Lámina 17 — Selección de campos textuales · 20 s

> De las **36 columnas** originales se seleccionan **siete campos textuales**:
> cinco del fabricante y dos del retailer. Estos campos forman dos vistas
> comparables: *manufacturer text* y *retailer text*.

### 9:31 · Lámina 18 — Selección en las otras fuentes · I · 20 s

> Hidden y NIC aportan un único campo de texto, sin mezclarlo con nada. El
> catálogo compone marca, nombre y descripción, y extrae los códigos aparte.
> Cada regla está verificada en su módulo de preparación.

### 9:51 · Lámina 19 — Selección en las otras fuentes · II · 20 s

> El lote de prueba reutiliza el mismo compositor de texto que Match — esto es
> deliberado: evita que el modelo vea en producción un texto formado de otra
> manera que en entrenamiento. Los pares negativos llegan ya compuestos.

### 10:11 · Lámina 20 — De volcado a unidad de análisis · 20 s

> El volcado trae **129.507 filas**. El filtro base conserva **127.093**, el
> **98,14%**: el dataset ya venía limpio a nivel de banderas. El trabajo real fue
> definir la identidad — la unidad canónica de publicación — y llegar a **110.706
> publicaciones** y **17.416 productos oficiales**.

### 10:31 · Lámina 21 — Lo ambiguo se marca, no se borra · 22 s

> Hay tres cosas que parecen duplicados y no lo son. Duplicado exacto: **8
> filas**, se eliminan. Repetición histórica del mismo par entre meses: **20,92%**,
> no se borra, se colapsa. Y co-ocurrencia por usar la llave equivocada, que no
> es duplicado en absoluto. Lo ambiguo se marca con su severidad.

### 10:53 · Lámina 22 — Los tres hallazgos que condicionan todo · 20 s

> Tres hallazgos que cambian el diseño. Uno: una fila no es un producto, así que
> **la división train/test se hace por par, nunca por fila**. Dos: el código vive
> dentro del texto libre, en el **90,19%** de los títulos. Tres: lo que parece
> ruido es sintaxis — la barra y las comillas significan algo.

### 11:13 · Lámina 23 — Las siete fuentes a escala · 18 s

> Siete fuentes, muy desiguales. Match aporta **127.093** pares; el catálogo,
> apenas **4.316** productos. Esa desproporción es la que obliga a una
> arquitectura de recuperación y no de comparación exhaustiva.

---

## Objetivo específico 3 — Pipeline de procesamiento textual

### 11:31 · Lámina 24 — Cinco fuentes, un solo pipeline · 20 s

> Cinco preparadores distintos, un solo pipeline de **19 pasos**. Lo único propio
> de cada fuente es qué columnas leer; de ahí en adelante son las mismas
> funciones. Eso elimina el *training-serving skew*: el texto de producción se
> forma exactamente igual que el de entrenamiento.

### 11:51 · Lámina 25 — Un título real atravesando el pipeline · 20 s

> Un título real. Del crudo con entidades y mayúsculas, a la normalización
> Unicode, a las diez reglas técnicas de dominio, y finalmente los códigos
> separados del texto. **La barra, las comillas y el alfabeto se conservan**: son
> sintaxis, no ruido. La normalización es idempotente, verificado sobre 254.186
> textos.

### 12:11 · Lámina 26 — Qué se destruye, qué se conserva, qué se gana · 20 s

> **575** entidades HTML eliminadas: eso sí era ruido. **30.919** filas en
> alfabeto no latino conservadas íntegras: cero pérdidas, porque una limpieza
> estándar habría borrado mercados enteros. Y separar los códigos del texto sube
> el Recall@1 de **51 a 83 por ciento**: **32 puntos**.

---

## Objetivo específico 4 — Diseñar los modelos

### 12:31 · Lámina 27 — Qué puede mirar cada modelo · 22 s

> La pregunta que ordena los tres modelos es qué puede *mirar* cada uno. TF-IDF
> no mira nada: es geometría de vectores. Los embeddings miran cada texto por
> separado. El cross-encoder mira **los dos textos juntos** en una sola
> secuencia. Esa diferencia explica todos los resultados que siguen.

### 12:53 · Lámina 28 — Los dos cruces que nadie más tiene · 22 s

> Al leer los dos textos juntos aparecen dos cuadrantes de atención que ningún
> otro modelo tiene: cada token del catálogo consulta el título del retailer y
> viceversa. Ahí es donde el sufijo **/90** se confronta con **/INT**. El falso
> positivo por sufijo distinto cae de **36 y 90 por ciento** a **4,88%**.

### 13:15 · Lámina 29 — 23 configuraciones definidas antes de evaluar · 20 s

> El protocolo se fijó antes de mirar resultados. Entrenamiento hasta octubre,
> validación en noviembre con **428 consultas**, y test en diciembre con **147**,
> que **se abre una sola vez, al cerrar**. Veintitrés configuraciones declaradas
> de antemano.

### 13:35 · Lámina 30 — Siete medidas, tres funciones · 20 s

> Siete medidas de similitud, pero con funciones distintas. Solo **una decide**:
> el coseno sobre TF-IDF. Una **contrasta**: BM25. Y cinco **explican** — sirven
> para auditar un par, nunca para decidir solas. Distinguir esto evita el error
> de promediar métricas que miden cosas diferentes.

### 13:55 · Lámina 31 — La cascada · 20 s

> La arquitectura es una cascada. El catálogo tiene **4.316 productos** por
> consulta; TF-IDF los reduce a **20 candidatos**, con la verdad dentro el
> **91,84%** de las veces. Sobre esos veinte, el cross-encoder decide. Ninguno de
> los dos puede hacer el trabajo del otro.

### 14:15 · Lámina 32 — La escalera de decisión · 22 s

> Y el sistema completo es una escalera. Las capas cero a tres son reglas
> deterministas y resuelven **1.274 de las 1.282 decisiones automáticas** — el
> **99,4%**, sin GPU. El modelo interviene en la capa cuatro. Y la capa cinco es
> la abstención: **1.083 publicaciones** que llegan al revisor ya ordenadas.

### 14:37 · Lámina 33 — El recuperador en marcha · 24 s

> Un caso real. La consulta es una publicación ucraniana de un monitor. El
> catálogo está en inglés. Aun así el producto correcto queda **primero, con
> 0,69**, el doble que el segundo. Los n-gramas de caracteres cruzan el idioma
> porque el **código es la parte que ambos textos comparten**.

### 15:01 · Lámina 34 — El caso que no puede cerrar solo · 24 s

> Y aquí el límite. Misma clase de consulta, pero los dos primeros candidatos son
> **el mismo texto**: solo cambia **/00** por **/01**. La separación es de cinco
> centésimas. Una bolsa de n-gramas no puede resolver esto, y por eso hace falta
> un segundo modelo que lea los dos textos juntos.

### 15:25 · Lámina 35 — 17 configuraciones evaluadas · 24 s

> Las diecisiete configuraciones del recuperador. Lean por columnas, no por
> filas: pasar de texto básico a texto enriquecido con los códigos vale **32
> puntos** de Recall@1. Elegir el mejor analizador dentro de una columna vale
> cinco. **La decisión de qué texto indexar pesó más que la de qué algoritmo
> usar.**

### 15:49 · Lámina 36 — Un mismo par por las cinco funciones · 24 s

> El mismo par, medido por las cinco funciones. Un título en ucraniano y uno en
> español, sin un solo token compartido: TF-IDF da **0,16**, Jaccard **0,09**.
> El cross-encoder da **0,99927** — entiende que hablan del mismo tipo de
> producto. Pero se equivoca de referencia: acierta el concepto y falla el modelo
> exacto.

### 16:13 · Lámina 37 — El margen delata la duda · 22 s

> Y esa duda es detectable. En los cuatro errores de ranking más graves, la
> distancia entre el primer y el segundo candidato va de **cero a siete
> millonésimas**. El score no avisa: todos pasan de 0,998. **El margen sí.** Por
> eso la compuerta exige score *y* margen, y estos casos van a revisión.

### 16:35 · Lámina 38 — Los cuatro falsos positivos · 24 s

> Los cuatro falsos positivos que sobreviven, con su título real. Un título con
> dos códigos; un sufijo **/RH** que designa otra referencia; un producto
> reacondicionado que comparte texto con el original; y un paquete de televisor
> más barra de sonido. Ninguno es caprichoso: en los cuatro, el texto **sí**
> describe el producto.

---

## Objetivo específico 5 — Evaluar el desempeño

### 16:59 · Lámina 39 — Recall@1 sobre las 147 consultas · 22 s

> Recuperación sobre el test. La mejor cascada acierta en primera posición el
> **87,07%**. Pero las dos mejores difieren en **tres consultas** y el test de
> McNemar da **p igual a 1**. Por eso se reporta como el mejor resultado
> observado, **no como superioridad demostrada**.

### 17:21 · Lámina 40 — El F1 sin la matriz engaña · 20 s

> Clasificación de pares. Los modelos uno y dos parecen equivalentes por F1 —
> **72%** contra **73%** — y sus matrices son opuestas: uno rechaza de más, el
> otro acepta casi todo. El cross-encoder llega a **97,41%** con **4,62%** de
> falsos positivos. Aquí la superioridad sí es contundente.

### 17:41 · Lámina 41 — Los negativos difíciles · 20 s

> Y esta es la cifra que cuenta la historia. Sobre variantes casi idénticas del
> mismo producto, los embeddings fallan el **90%** de las veces y TF-IDF el
> **36%**. El cross-encoder, el **4,88%**. Esto es exactamente la variabilidad de
> criterio que el planteamiento del problema identificaba.

### 18:01 · Lámina 42 — La matriz de confusión · 22 s

> La matriz completa sobre los **344 pares** de test: **222** aciertos positivos,
> **109** negativos correctos, **4** falsos positivos y **9** falsos negativos. El
> umbral se fijó en validación y **se aplicó al test sin retocarlo** — es la
> única forma de que la cifra signifique algo.

### 18:23 · Lámina 43 — El techo del recuperador · 22 s

> Y una limitación que conviene decir antes de que la pregunten. De los 26 fallos
> de primera posición, **12 son irrecuperables**: el candidato correcto nunca
> entró al pool. Mejorar el reordenador no los arregla; hay que ensanchar la
> recuperación.

---

## Evidencia fuera del dataset

### 18:45 · Lámina 44 — Gold externo, los tres modelos · 22 s

> **213 consultas** anotadas a mano, fuera del entrenamiento. Y aquí el resultado
> es honesto: modelo uno y modelo tres **empatan** en Recall@1. El bootstrap de
> diez mil muestras da una diferencia de **exactamente cero**. El aporte del
> reordenador no es recuperar mejor: es decidir **cuándo automatizar**.

### 19:07 · Lámina 45 — Bélgica, dos publicaciones reales · 24 s

> Dos publicaciones belgas reales. La primera se resuelve bien. La segunda vende
> **un televisor y una barra de sonido**: no corresponde a un solo producto del
> catálogo. El score es altísimo, pero el margen de **0,0022** delata la
> ambigüedad y el sistema se abstiene. **Se abstiene por la razón correcta.**

### 19:31 · Lámina 46 — Benchmark multipaís v7.5 · 24 s

> La prueba de generalización: **2.365 publicaciones**, **19 países**, ningún
> retailer visto en el entrenamiento. **54,2%** automatizado con **94,5%** de
> precisión. Los dos peores resultados son los dos marketplaces más grandes,
> donde el título lo escribe un vendedor tercero. **La degradación tiene una
> causa identificable.**

### 19:55 · Lámina 47 — Con código y sin código · 24 s

> Y esta lámina explica por qué. Dos publicaciones, mismo umbral, scores casi
> idénticos. La primera lleva el código en el título y acierta. La segunda dice
> solo «Philips Air Fryer, 7,2 litros» — que describe varias freidoras del
> catálogo — y el modelo elige una plausible con total confianza. **Es el límite
> del método.**

---

## Objetivo específico 6 — Contrastar con el proceso manual

### 20:19 · Lámina 48 — Línea base manual observada · 20 s

> La línea base reúne dos semanas operativas. Se registraron **62.580 segundos**
> para **3.768 publicaciones-semana**. El promedio combinado es **16,608
> segundos por publicación-semana**.

### 20:39 · Lámina 49 — Latencia del sistema v7.5 · 20 s

> La corrida v7.5 procesó **2.365 consultas** en **15.411,8 segundos**. La
> latencia promedio fue **6,5166 segundos por consulta**, equivalente a una
> reducción unitaria del **60,76%** frente a la línea base manual.

### 20:59 · Lámina 50 — Escenario operativo asistido · 20 s

> En el mismo lote, el proceso manual proyecta **10,91 horas humanas**. Con el
> modelo, el operador revisa 1.083 casos y utiliza **5,00 horas humanas**. La
> reducción del trabajo humano es **54,21%**; si máquina y persona se consideran
> secuenciales, la reducción total es **14,97%**.

### 21:19 · Lámina 51 — Consistencia durante la evaluación y el uso · 20 s

> La evaluación interna del Modelo 3 alcanza **96,89% de exactitud** y **97,41%
> de F1**. En el benchmark externo, la coincidencia selectiva es **94,54%**. Los
> **70 casos** son desacuerdos externos; durante el uso controlado se registraron
> **cero errores**.

### 21:39 · Lámina 52 — Resultados de la consistencia de la calidad · 25 s

> Con **94 verdaderos positivos**, **62 verdaderos negativos**, **3 falsos
> positivos** y **2 falsos negativos**, la exactitud es **96,89%**, la precisión
> **96,91%**, el recall **97,92%**, el F1 **97,41%** y la tasa de error **3,11%**.
> En el uso controlado, la tasa de error observada es **cero**.

### 22:04 · Lámina 53 — Resultados del tiempo de validación · 25 s

> La línea base manual resulta de dividir **62.580 segundos entre 3.768
> publicaciones-semana**: **16,608 segundos**. La latencia del modelo es
> **15.411,8 entre 2.365**: **6,5166 segundos**. La reducción unitaria es
> **60,76%**, la reducción de horas humanas **54,21%** y la reducción secuencial
> total **14,97%**.

### 22:29 · Lámina 54 — Matriz de contrastación · 20 s

> La variable independiente se materializa en el Modelo 3, la cascada v7.5 y el
> esquema *Human in the Loop*. Para la primera variable dependiente, la evidencia
> interna, externa y de uso muestra mejora de consistencia. Para la segunda, la
> latencia y las horas humanas demuestran reducción del tiempo.

### 22:49 · Lámina 55 — Contrastación de la hipótesis · 20 s

> Por tanto, **el modelo de Procesamiento de Lenguaje Natural mejora la
> consistencia de la calidad del matching y reduce el tiempo de validación, en
> comparación con el proceso manual, en el área de operaciones de Agilsoft
> SRL**. Se acepta la hipótesis dentro del alcance del estudio.

### 23:09 · Lámina 56 — Gracias · 15 s

> Muchas gracias por su atención. Quedo atento a sus preguntas.

---
---

# Anexo · cifras para el turno de preguntas

Números que conviene tener a mano y que **no** están en pantalla o están en una
sola lámina.

| Tema | Cifra |
|---|---|
| Filtro base | 129.507 → 127.093 (98,14%) |
| Unidad canónica | país + retailer + RetailerProductId · 110.706 publicaciones |
| Llave de respaldo | 465 filas (0,37%) |
| Split | train ene–oct · validación nov (428) · test dic (147) |
| Umbral del cross-encoder | 0,998844 — fijado en validación |
| Matriz de test | TP 222 · FN 9 · FP 4 · TN 109 |
| Recall@1 del reordenador | 82,31% · Recall@5 87,76% · MRR 0,8515 |
| Techo del pool | 135 de 147 (91,84%) |
| Gold externo | 213 consultas · M1 0,615 · M2 0,183 · M3 0,615 |
| Bootstrap M1 vs M3 | diferencia 0,0 · IC [−0,047; +0,047] · p = 1,0 |
| Evaluación interna M3 | TP 94 · TN 62 · FP 3 · FN 2 · Accuracy 96,89% · Precision 96,91% · Recall 97,92% · F1 97,41% · Error 3,11% |
| Benchmark v7.5 | 2.365 · 19 países · 42 retailers · 54,21% · 94,54% · 70 desacuerdos |
| Escalera v7.5 | Hidden 188 · NIC 973 · Match 121 · Review 1.083 |
| Línea base manual | 62.580 s / 3.768 publicaciones-semana = 16,608 s |
| Latencia v7.5 | 15.411,8 s / 2.365 consultas = 6,5166 s |
| Reducción | 60,76% unitaria · 54,21% humana · 14,97% secuencial |
| Uso controlado | 0 errores registrados |
| Motivo dominante de error | código de la consulta ausente del catálogo |

## Tres preguntas probables y su respuesta

**«¿Por qué el modelo 2 fracasa tan claramente?»**
> Porque compara sentido y aquí el sentido no distingue. Dos variantes del mismo
> monitor significan casi lo mismo; lo que las separa es un sufijo de dos
> caracteres. Un encoder congelado que promedia vectores no puede verlo. No es un
> error de implementación: es un fracaso legítimo que delimita el problema.

**«¿El sistema reemplaza al analista?»**
> No, y está diseñado para no hacerlo. Se abstiene en el 45,8% de los casos y la
> capa de *No Match* automático está deshabilitada: el sistema nunca afirma que
> algo no corresponde. Lo que hace es quitar de la mesa lo que tiene evidencia
> verificable y entregar el resto priorizado.

**«¿Los resultados se sostienen fuera del dataset?»**
> Parcialmente, y lo digo con la cifra. En el gold externo el reordenador no
> mejora la recuperación respecto de TF-IDF: empatan. Donde sí aporta es en la
> decisión de automatizar, con 94,5% de precisión sobre 19 países y 42 retailers
> nunca vistos. La degradación que aparece tiene una causa identificada: títulos
> sin código.
