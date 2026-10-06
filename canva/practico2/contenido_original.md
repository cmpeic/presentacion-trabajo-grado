# Contenido original de las láminas 44-90 (texto extraído de index.html)
Cada bloque lista los textos visibles en orden de lectura (arriba→abajo, izquierda→derecha). La captura del original está en `shots/sNN.png`. Las notas del orador vienen de GUION.md.

## Lámina 44 — OE2 · Identificar atributos · Lámina 10 · Las señales que deciden
Textos: IDENTIFICAR ATRIBUTOS · 02 / 03 | Las señales que deciden la correspondencia | 17.416 oficiales | 42 caracteres | ManufacturerProductId | ManufacturerProductName | Identificadores | Nombres | RetailerProductId | 8.528 reutilizados | RetailerProductName | 61 · 90,19% código | Descripción y códigos | ManufacturerProductDescription | 5,35% nulos | Brand | 82,80% presente | Contexto | ExtraInfo | 67,20% EAN | ManufacturerProductMappingCountry | 65 países

Nota del orador: Aquí está la asimetría del problema. El nombre del fabricante promedia 42 caracteres; el del retailer, 61, y el 90,19% contiene un token con forma de código. El identificador del retailer no es confiable: 8.528 casos aparecen reutilizados entre comercios distintos.

## Lámina 45 — OE2 · Identificar atributos · Lámina 11 · Atributos de calidad y una trampa
Textos: IDENTIFICAR ATRIBUTOS · 03 / 03 | Los atributos de calidad y una trampa concreta | Invalid | IsDeleted | MatchConfidence | "false" | "false" | 100 | 2.136 registros inválidos | 2.355 registros eliminados | 129.473 con 100 · 34 con −100 | LinkIsValid | "true" / "false" · Solo indicador del estado del enlace | NO ES FILTRO

Nota del orador: Tres banderas sirven de filtro: Invalid, IsDeleted y MatchConfidence. La cuarta, LinkIsValid, parece un filtro y no lo es: describe el estado del enlace, no la validez de la correspondencia. Usarla habría descartado datos buenos.

## Lámina 46 — OE2 · Extraer productos · Lámina 12 · Fuente Hidden
Textos: EXTRAER PRODUCTOS · 01 / 05 | data/raw/hidden/ · Contrato mínimo | 15.355 filas · 4 columnas | final_combined_data_hidden.csv | product_name | comment | Pila Bvp007 20W 4000K | Marked RPI as hidden | El único texto: título de la publicación | Motivo de negocio · solo 2 frases distintas | final_status | source_dataset | Hidden | dataset_1 | Estado constante por contrato de una sola clase | Trazabilidad de la subfuente

Nota del orador: Hidden aporta 15.355 filas con solo cuatro columnas. Su contrato es de una sola clase: el pipeline se detiene si aparece un estado distinto de Hidden. Un contrato verificable vale más que una comprobación manual.

## Lámina 47 — OE2 · Extraer productos · Lámina 13 · Fuente NIC
Textos: EXTRAER PRODUCTOS · 02 / 05 | data/raw/nic/ · Contrato etiquetado | 47.333 filas · 5 + 8 columnas | final_combined_data_nic.csv + dataset_nic_etiquetado.csv | Contrato base | Etiquetado heurístico | nic_source_row_number | Fila de origen | product_name | Título de la publicación | nic_label | 83% unknown_review | extra_info | EAN desnudo · 8720169365247 | nic_review_required | yes/no | nic_label_source | Regla que produjo la etiqueta | comment | Motivo de negocio | nic_confidence | high/low | source_dataset | Subfuente 1, 2 o 3 | nic_candidate_labels | Etiquetas alternativas | nic_match_rules | Reglas coincidentes | final_status | Estado NIC | nic_label_reason | Justificación textual

Nota del orador: NIC aporta 47.333 filas y es la fuente más compleja: cinco columnas de contrato base más ocho de etiquetado heurístico. El 83% queda como unknown_review. Por eso NIC no entra como verdad fuerte, sino con peso reducido — una decisión metodológica, no una limitación técnica.

## Lámina 48 — OE2 · Extraer productos · Lámina 14 · Catálogos oficiales
Textos: EXTRAER PRODUCTOS · 03 / 05 | data/raw/official_catalogs/ · Producto oficial | 11 columnas | Catálogos de Ucrania y Bélgica · mismo contrato | Identidad | Llaves de correspondencia | Contenido oficial | BrandName · Philips | ProductId · BAR700/00 | ProductName | OwnerName · Philips | ExtraInfo · EAN | ProductImageDescription | Id · GUID interno | El código con barra es la llave real | El código viene dentro del nombre | Precio no utilizado | Imagen y URL | ManufacturerSuggestedRetailerPrice | ProductImageUrl · Imagen Philips | MinimumAdvertisedPrice | ProductUrl · El dominio se audita | Ambos permanecen en 0.0

Nota del orador: El catálogo oficial es la referencia contra la que se compara todo. Ucrania y Bélgica comparten contrato de 11 columnas. La llave real es el ProductId con barra, como BAR700/00. Los dos campos de precio están en cero en todo el snapshot: por eso no se usan.

## Lámina 49 — OE2 · Extraer productos · Lámina 15 · Pares negativos
Textos: EXTRAER PRODUCTOS · 04 / 05 | data/raw/negative_match/ · Pares ya formados | 896 filas · 7 columnas | training_pairs_from_code_logs.csv | Lado retailer | Lado fabricante | retailer_text | manufacturer_text | Multiprocesadora Philips HR7304/90 1000W… | PowerChop 5000 HR7304/90 Procesador… | retailer_code · HR7304/90 | manufacturer_code · HR7304/90 | negative_type | label | source_file | exact_match · sufijo_distinto · reacondicionado_r1 | Etiqueta binaria · 1 | 60 archivos · ~49 retailers

Nota del orador: Es la única fuente que llega ya en forma de par etiquetado: 896 filas con los dos textos y su etiqueta. Y trae el tipo de negativo — sufijo distinto y reacondicionado —, que es justamente lo que después va a costar más.

## Lámina 50 — OE2 · Extraer productos · Lámina 16 · Retailer de prueba
Textos: EXTRAER PRODUCTOS · 05 / 05 | data/raw/retailer_test/ · Contrato operativo | Registro | Contexto | Producto | Medios | Id | ManufacturerName | ProductId | ProductImageUrl | RetailerName | CompetitorName | ProductName | ProductUrl | Obligatorios y no vacíos | Fabricante y competidor | Imagen y enlace auditado | ExtraInfo | Actualmente no existe un archivo físico en | data/raw/retailer_test/ | . | prepare_retailer_input.py | declara el contrato y | validate_columns() | lo valida antes de la lectura.

Nota del orador: Esta fuente no tiene archivo físico hoy. Aun así el contrato es verificable, porque el código que lo consume lo declara y lo valida antes de leer. Es la diferencia entre documentar un supuesto y hacerlo comprobable.

## Lámina 51 — OE2 · Seleccionar campos · Lámina 17 · La selección, formalizada
Textos: SELECCIONAR CAMPOS · 01 / 03 | Selección de campos textuales | ORIGEN | CAMPOS SELECCIONADOS | SALIDA | Fabricante | Brand · ManufacturerProductName · ManufacturerProductDescription · ManufacturerProductId · ExtraInfo | manufacturer_text | Retailer | RetailerProductName · RetailerProductId | retailer_text | 36 | 7 | 2 | COLUMNAS ORIGINALES | CAMPOS TEXTUALES | VISTAS COMPARABLES

Nota del orador: De las 36 columnas originales se seleccionan siete campos textuales: cinco del fabricante y dos del retailer. Estos campos forman dos vistas comparables: manufacturer text y retailer text.

## Lámina 52 — OE2 · Seleccionar campos · Lámina 18 · Selección en las otras fuentes
Textos: SELECCIONAR CAMPOS · 02 / 03 | Selección textual en las otras seis fuentes · I | Hidden | NIC | Catálogo oficial | product_name · único | product_name · único | BrandName | ProductName | ProductImageDescription | product_name → retailer_text_raw | product_name → retailer_text_raw | Marca + nombres + descripción → catalog_text_raw | Sin mezclar campos | 8 etiquetas → metadata | ExtraInfo → códigos | VERIFICADO EN | VERIFICADO EN | VERIFICADO EN | prepare_hidden.py | prepare_nic.py | prepare_catalog.py

Nota del orador: Hidden y NIC aportan un único campo de texto, sin mezclarlo con nada. El catálogo compone marca, nombre y descripción, y extrae los códigos aparte. Cada regla está verificada en su módulo de preparación.

## Lámina 53 — OE2 · Seleccionar campos · Lámina 19 · Selección en las otras fuentes
Textos: SELECCIONAR CAMPOS · 03 / 03 | Selección textual en las otras seis fuentes · II | Retailer de prueba | Pares negativos | Acciones de validación | ProductName · único | retailer_text | manufacturer_text | Sin campos de texto | ProductName → build_retailer_text | Textos ya compuestos | No alimenta el modelo textual | Mismo compositor de Match | Sin paso de selección | Etiquetas sobre publicaciones | VERIFICADO EN | VERIFICADO EN | VERIFICADO EN | prepare_retailer_input.py | training_pairs_from_code_logs.csv | gold_externo.py

Nota del orador: El lote de prueba reutiliza el mismo compositor de texto que Match — esto es deliberado: evita que el modelo vea en producción un texto formado de otra manera que en entrenamiento. Los pares negativos llegan ya compuestos.

## Lámina 54 — OE2 · Estructurar conjunto · Lámina 20 · De volcado a unidad de análisis
Textos: ESTRUCTURAR EL CONJUNTO · 01 / 02 | Del volcado del portal a la unidad de análisis | 129.507 | Volcado del portal · 12 snapshots de 2025 | filas × 36 columnas | ▼ Invalid = false  ∧  IsDeleted = false  ∧  MatchConfidence = 100  →  −2.414 | 127.093 | Conjunto de estudio válido | 98,14% conservado | ▼ unidad canónica = país + retailer + RetailerProductId  ·  llave de respaldo en 465 filas (0,37%) | 111.269 | 110.706 | 17.416 | pares distintos | publicaciones retailer | productos oficiales

Nota del orador: El volcado trae 129.507 filas. El filtro base conserva 127.093, el 98,14%: el dataset ya venía limpio a nivel de banderas. El trabajo real fue definir la identidad — la unidad canónica de publicación — y llegar a 110.706 publicaciones y 17.416 productos oficiales.

## Lámina 55 — OE2 · Estructurar conjunto · Lámina 21 · Lo ambiguo se marca, no se borra
Textos: ESTRUCTURAR EL CONJUNTO · 02 / 02 | Lo ambiguo se marca, no se borra | 8 | 26.592 | 36,49% | filas · 0,01% | filas · 20,92% | máximo · llave gruesa | Duplicado exacto / | Repetición histórica / | Co-ocurrencia por reuso / | las 36 columnas idénticas | el mismo par hasta en 11 meses | llave gruesa, sin Retailer | ELIMINAR | COLAPSAR O PONDERAR | NO ES DUPLICADO | Id reutilizado entre retailers | 8.528 | severidad media | Nombre → varios oficiales | 1.227 | severidad media | Id retailer → varios oficiales | 889 | severidad alta | Unidad canónica → varios oficiales | 263 | severidad alta · 1.001 filas

Nota del orador: Hay tres cosas que parecen duplicados y no lo son. Duplicado exacto: 8 filas, se eliminan. Repetición histórica del mismo par entre meses: 20,92%, no se borra, se colapsa. Y co-ocurrencia por usar la llave equivocada, que no es duplicado en absoluto. Lo ambiguo se marca con su severidad.

## Lámina 56 — OE2 · Análisis exploratorio · Lámina 22 · Los tres hallazgos que condicionan todo
Textos: ANÁLISIS EXPLORATORIO · 01 / 02 | Los tres hallazgos que condicionan todo lo demás | Una fila no es un producto | El código vive dentro del texto libre | Lo que parece ruido es sintaxis | 20,92% | / | separa variantes de código | Filas en pares repetidos | Títulos con token tipo código | 90,19% | 65,70% | 11 | Meses distintos para un par | Reproducen el id oficial | 58,97% | 11,02% | Comillas que marcan pulgadas | NPX150/INT | · llave gruesa | 42 → 1 | Id oficial con | / | 13,60% | Texto en alfabeto no latino | 87,66% · 73,75% | · retailer numérico | La división train/test se hace por par, nunca por fila. | Los identificadores no se comparan como cadenas: se buscan dentro del título. | Una limpieza estándar destruiría la señal y borraría mercados enteros.

Nota del orador: Tres hallazgos que cambian el diseño. Uno: una fila no es un producto, así que la división train/test se hace por par, nunca por fila. Dos: el código vive dentro del texto libre, en el 90,19% de los títulos. Tres: lo que parece ruido es sintaxis — la barra y las comillas significan algo.

## Lámina 57 — OE2 · Análisis exploratorio · Lámina 23 · Las siete fuentes a escala
Textos: ANÁLISIS EXPLORATORIO · 02 / 02 | Las siete fuentes del corpus, a escala | Match | 127.093 | pares históricos validados | NIC | 28.712 | no está en catálogo | Hidden | 11.077 | publicación ocultada | Catálogo oficial | 4.316 | productos UA | Retailer de prueba | 1.856 | gold externo · 14 países | Pares negativos | 896 | 800 elegibles | Acciones de validación | 180 | decisión humana registrada

Nota del orador: Siete fuentes, muy desiguales. Match aporta 127.093 pares; el catálogo, apenas 4.316 productos. Esa desproporción es la que obliga a una arquitectura de recuperación y no de comparación exhaustiva.

## Lámina 58 — OE3 · Pipeline textual · Lámina 24 · Cinco fuentes, un solo pipeline
Textos: PIPELINE DE PROCESAMIENTO TEXTUAL · 01 / 03 | Cinco fuentes, un solo pipeline | prepare_match | *_text | El pipeline genérico único | prepare_hidden | *_codes | as_text | decode_html | normalize_unicode | normalize_technical | *_token_count | prepare_nic | extract_codes | canonicalize_code | quality_flags | 19 pasos · v1.3.1 | banderas de calidad | prepare_catalog | Lo único propio de cada fuente es qué columnas leer. De ahí en adelante, las mismas funciones — eso elimina el training-serving skew. | 127.093 × 53 · 33,14 MiB | prepare_retailer_input

Nota del orador: Cinco preparadores distintos, un solo pipeline de 19 pasos. Lo único propio de cada fuente es qué columnas leer; de ahí en adelante son las mismas funciones. Eso elimina el training-serving skew: el texto de producción se forma exactamente igual que el de entrenamiento.

## Lámina 59 — OE3 · Pipeline textual · Lámina 25 · Un título real atravesando el pipeline
Textos: PIPELINE DE PROCESAMIENTO TEXTUAL · 02 / 03 | Un título real atravesando el pipeline | CRUDO | Philips — P21 / 5W | GU 10; 12 V; 4000 K; 55" | como llega del portal | UNICODE NFKC | philips — p21 / 5w | gu 10; 12 v; 4000 k; 55" | + casefold | NORMALIZACIÓN TÉCNICA | philips p21/5w gu10 12v 4000k 55" | 10 reglas de dominio | CÓDIGOS APARTE | text → philips gu10 12v 4000k 55"  ·  codes → [p21/5w] | nunca dentro del texto | La barra, las comillas y el alfabeto se conservan: son sintaxis del dominio. La normalización es idempotente — verificada sobre 254.186 textos.

Nota del orador: Un título real. Del crudo con entidades y mayúsculas, a la normalización Unicode, a las diez reglas técnicas de dominio, y finalmente los códigos separados del texto. La barra, las comillas y el alfabeto se conservan: son sintaxis, no ruido. La normalización es idempotente, verificado sobre 254.186 textos.

## Lámina 60 — OE3 · Pipeline textual · Lámina 26 · Qué se destruye, qué se conserva, qué se gana
Textos: PIPELINE DE PROCESAMIENTO TEXTUAL · 03 / 03 | Qué se destruye, qué se conserva, qué se gana | 575 → 0 | 30.919 → 30.919 | 51,17 → 83,18 | entidades HTML | filas no latinas | Recall@1 en validación · % | Se destruye lo que sí es ruido / | Se conserva lo que es señal / | Se gana con los códigos aparte / | marcado heredado del portal | 0 filas perdidas · 0 excluidos | la vista enriched | ELIMINADO | INTACTO | +32 PUNTOS | 100% | manufacturer_codes | retailer_codes | 99,98% | 97,17% | manufacturer_eans | 90,53% | retailer_title_codes

Nota del orador: 575 entidades HTML eliminadas: eso sí era ruido. 30.919 filas en alfabeto no latino conservadas íntegras: cero pérdidas, porque una limpieza estándar habría borrado mercados enteros. Y separar los códigos del texto sube el Recall@1 de 51 a 83 por ciento: 32 puntos.

## Lámina 61 — OE4 · Modelos algorítmicos · Lámina 27 · Qué puede mirar cada modelo
Textos: MODELOS ALGORÍTMICOS · 01 / 06 | ¿Qué puede mirar cada modelo al comparar dos textos? | 1 | 2 | 3 | TF-IDF / n-gramas de caracteres | Embeddings / encoders congelados | Cross-encoder / fine-tuneado | — solo geometría de vectores dispersos. Coseno sobre n-gramas. | — los dos textos juntos en una sola secuencia. Atención cruzada token a token. | lo propio | — cada texto por separado. Self-attention, mean pooling y coseno. | Mira | nada | Mira | Mira | todo | 91,16% | 8,84% | 97,41% | RECALL@10 | RECALL@1 | F1 DE PARES | RECUPERADOR | FRACASO LEGÍTIMO | VALIDADOR

Nota del orador: La pregunta que ordena los tres modelos es qué puede mirar cada uno. TF-IDF no mira nada: es geometría de vectores. Los embeddings miran cada texto por separado. El cross-encoder mira los dos textos juntos en una sola secuencia. Esa diferencia explica todos los resultados que siguen.

## Lámina 62 — OE4 · Modelos algorítmicos · Lámina 28 · Los dos cruces que nadie más tiene
Textos: MODELOS ALGORÍTMICOS · 02 / 06 | La lectura conjunta: los dos cruces que nadie más tiene | [CLS] | philips | neopix | 150 | npx150/int | [SEP] | proyector | philips | neopix | 150 | npx150/90 | [SEP] | CONSULTA ↓ | A · PRODUCTO OFICIAL | B · PUBLICACIÓN RETAILER | ATENDIDO → | A → A | A → B | A | El producto oficial se lee a sí mismo. Es lo único que ve el Modelo 2. | Cada token del catálogo consulta el título del retailer. | B → A | B → B | B | Y al revés: el sufijo /90 se confronta con /INT. | La publicación se lee a sí misma. | Los cuadrantes cruzados son la diferencia: el falso positivo por sufijo distinto cae de 36,59% y 90,24% a 4,88%.

Nota del orador: Al leer los dos textos juntos aparecen dos cuadrantes de atención que ningún otro modelo tiene: cada token del catálogo consulta el título del retailer y viceversa. Ahí es donde el sufijo /90 se confronta con /INT. El falso positivo por sufijo distinto cae de 36 y 90 por ciento a 4,88%.

## Lámina 63 — OE4 · Modelos algorítmicos · Lámina 29 · 23 configuraciones definidas antes de evaluar
Textos: MODELOS ALGORÍTMICOS · 03 / 06 | 23 configuraciones definidas antes de evaluar | TRAIN | VALIDATION | TEST | 2025-01 … 10 | 2025-11 · 428 consultas | 2025-12 · 147 consultas | Ajusta las transformaciones. Nada más. | Selecciona configuración y umbral. | Se abre una sola vez, al cerrar. | Modelo 1 · TF-IDF | Modelo 2 · Embeddings | Modelo 3 · Cross-encoder | 8 configuraciones × 2 vistas. Gana char_4_6_enriched. | 3 encoders × 2 vistas, todos congelados. Sin entrenamiento. | Una configuración. Checkpoint por eval_loss: gana la primera época. Umbral 0,998844.

Nota del orador: El protocolo se fijó antes de mirar resultados. Entrenamiento hasta octubre, validación en noviembre con 428 consultas, y test en diciembre con 147, que se abre una sola vez, al cerrar. Veintitrés configuraciones declaradas de antemano.

## Lámina 64 — OE4 · Modelos algorítmicos · Lámina 30 · Siete medidas, tres funciones
Textos: MODELOS ALGORÍTMICOS · 04 / 06 | Siete medidas de similitud, tres funciones distintas | EXPLICA | CONTRASTA | DECIDE | 5 | 1 | 1 | auditoría por par y features candidatas — nunca deciden solas | segundo ranking independiente de control | el ranking top-10 y el corte por umbral | Jaccard | Levenshtein | fuzzy ratio | token_sort | token_set | coseno sobre TF-IDF | BM25 Okapi | BoW overlap | BoW Dice | El score del cross-encoder no es una similitud simétrica: es σ(logit), una probabilidad no calibrada de que el par sea correspondencia.

Nota del orador: Siete medidas de similitud, pero con funciones distintas. Solo una decide: el coseno sobre TF-IDF. Una contrasta: BM25. Y cinco explican — sirven para auditar un par, nunca para decidir solas. Distinguir esto evita el error de promediar métricas que miden cosas diferentes.

## Lámina 65 — OE4 · Modelos algorítmicos · Lámina 31 · La cascada
Textos: MODELOS ALGORÍTMICOS · 05 / 06 | La cascada: recuperar barato, validar caro | ▶ | ▶ | Catálogo del país | Recuperación TF-IDF | Validación cruzada | 4.316 | top 20 | 1 decisión | productos oficiales candidatos para cada consulta | candidatos con la verdad dentro el 91,84% de las veces — el techo del pool | reordena, puntúa y exige margen y soporte de código antes de afirmar Match | MODELO 1 | MODELO 3 | Ninguno de los dos puede hacer el trabajo del otro: el recuperador no distingue variantes casi homónimas y el validador es demasiado caro para recorrer 4.316 productos por consulta.

Nota del orador: La arquitectura es una cascada. El catálogo tiene 4.316 productos por consulta; TF-IDF los reduce a 20 candidatos, con la verdad dentro el 91,84% de las veces. Sobre esos veinte, el cross-encoder decide. Ninguno de los dos puede hacer el trabajo del otro.

## Lámina 66 — OE4 · Modelos algorítmicos · Lámina 32 · La escalera de decisión
Textos: MODELOS ALGORÍTMICOS · 06 / 06 | La escalera de decisión, medida sobre 2.365 publicaciones | 188 | 0 | El enrutador de estados indica publicación ocultada | HIDDEN | 890 | 1 | El código de la consulta no existe en el catálogo del país | NIC | El enrutador de estados indica ausencia de catálogo | 83 | 2 | NIC | 3 | Regla exacta de código y el título no es multipack | MATCH | 113 | 4 | TF-IDF recupera · el cross-encoder puntúa · compuerta de score, margen y código | MATCH | 8 | 5 | Todo lo demás — llega al revisor con los candidatos ya ordenados | REVIEW | 1.083 | Las capas 0–3 resuelven 1.274 de las 1.282 decisiones automáticas — el 99,4% y no necesitan GPU. No Match automático permanece deshabilitado: el sistema nunca afirma la ausencia de correspondencia sin verdad que la respalde.

Nota del orador: Y el sistema completo es una escalera. Las capas cero a tres son reglas deterministas y resuelven 1.274 de las 1.282 decisiones automáticas — el 99,4%, sin GPU. El modelo interviene en la capa cuatro. Y la capa cinco es la abstención: 1.083 publicaciones que llegan al revisor ya ordenadas.

## Lámina 67 — OE4 · Modelos algorítmicos · Lámina 33 · El recuperador en marcha
Textos: MODELOS ALGORÍTMICOS · 07 / 12 | El recuperador en marcha: una consulta real y lo que devuelve | CONSULTA · PUBLICACIÓN DE RETAILER · UCRANIA | монітор philips 27" 27e2n1100l/00 black/va/100 гц | código presente: 27E2N1100L/00 | catálogo: 4.316 productos | TF-IDF char_wb 4-6 · texto enriquecido | 1 | 27E2N1100L/00 | philips monitor 27e2n1100l full hd lcd monitor | 0,691793 | 2 | 27E2N1110/00 | philips monitor 27e2n1110 full hd lcd monitor | 0,344748 | 3 | 27E2N1500L/00 | philips monitor 27e2n1500l quad hd monitor | 0,316991 | 24E2N1100LB/00 | 0,314381 | 4 | philips monitor 24e2n1100lb full hd lcd monitor | 5 | 27E2N2500/00 | philips monitor 27e2n2500 quad hd monitor | 0,157108 | El correcto queda primero y con el doble de puntuación que el segundo. Consulta en cirílico, catálogo en inglés: los n-gramas de caracteres cruzan el idioma porque el código es la parte que comparten.

Nota del orador: Un caso real. La consulta es una publicación ucraniana de un monitor. El catálogo está en inglés. Aun así el producto correcto queda primero, con 0,69, el doble que el segundo. Los n-gramas de caracteres cruzan el idioma porque el código es la parte que ambos textos comparten.

## Lámina 68 — OE4 · Modelos algorítmicos · Lámina 34 · El caso que no puede cerrar solo
Textos: MODELOS ALGORÍTMICOS · 08 / 12 | El caso que el recuperador no puede cerrar solo | CONSULTA · EL SUFIJO ES LO ÚNICO QUE CAMBIA | монітор philips 27m2c5500w/00 | correcto: 27M2C5500W/00 | competidor: 27M2C5500W/01 | separación: 0,054387 | 27M2C5500W/00 | philips curved gaming monitor 27m2c5500w quad hd | 0,668532 | 1 | 2 | 27M2C5500W/01 | philips curved gaming monitor 27m2c5500w quad hd | 0,614145 | 3 | 32M2C5500W/00 | philips gaming monitor 32m2c5500w quad hd | 0,456400 | 4 | 32M2C5500W/01 | philips gaming monitor 32m2c5500w quad hd | 0,397797 | 5 | 27M2C5501/00 | philips curved fast va gaming monitor 27m2c5501 | 0,388397 | Los dos primeros son el mismo texto: solo cambia /00 por /01. Una bolsa de n-gramas no puede separar eso — por esto hace falta un segundo modelo que lea los dos textos juntos.

Nota del orador: Y aquí el límite. Misma clase de consulta, pero los dos primeros candidatos son el mismo texto: solo cambia /00 por /01. La separación es de cinco centésimas. Una bolsa de n-gramas no puede resolver esto, y por eso hace falta un segundo modelo que lea los dos textos juntos.

## Lámina 69 — OE4 · Modelos algorítmicos · Lámina 35 · 17 configuraciones evaluadas
Textos: MODELOS ALGORÍTMICOS · 09 / 12 | 17 configuraciones evaluadas: lo que decide no es el algoritmo | TEXTO BÁSICO | TEXTO ENRIQUECIDO | Representación | solo el nombre | nombre + códigos + EAN | Palabras 1-1 | 0,2593 | 0,7523 | word unigrama | Palabras 1-3 | 0,2383 | 0,7406 | word trigrama | Caracteres 3-5 | 0,4953 | 0,8060 | char_wb | Caracteres 4-6 | 0,8317 | 0,5116 | char_wb · seleccionada | test 0,8571 | Híbrido w25 | 0,4929 | 0,8177 | word 1-2 + char 3-5 | BM25 | — | 0,6985 | ponderación probabilística | Recall@1 en validación. La columna manda sobre la fila: enriquecer el texto con los códigos vale +32 puntos; elegir el mejor analizador dentro de una columna vale 5. La decisión de qué texto indexar pesó más que la de qué algoritmo usar.

Nota del orador: Las diecisiete configuraciones del recuperador. Lean por columnas, no por filas: pasar de texto básico a texto enriquecido con los códigos vale 32 puntos de Recall@1. Elegir el mejor analizador dentro de una columna vale cinco. La decisión de qué texto indexar pesó más que la de qué algoritmo usar.

## Lámina 70 — OE4 · Modelos algorítmicos · Lámina 36 · Un mismo par por las cinco funciones
Textos: MODELOS ALGORÍTMICOS · 10 / 12 | Un mismo par, medido por las cinco funciones | PUBLICACIÓN DEL RETAILER · UCRANIANO | CANDIDATO DEL CATÁLOGO · ESPAÑOL | пустушка avent ultra soft 6-18 міс. дизайн для дівчат 2 шт. | philips chupete ultrasuave y flexible 6-18 meses ultra soft-fopspeen | código truncado: scf0… | SCF227/22 | el correcto era SCF091/18 | 0,1643 | 0,0870 | 0,4899 | 0,99927 | TF-IDF COSENO | JACCARD | EMBEDDINGS | CROSS-ENCODER | Las medidas de superficie ven dos textos casi ajenos — idiomas distintos, ningún token compartido. El cross-encoder entiende que hablan del mismo tipo de producto y se dispara a 0,99927. Pero se equivoca de referencia: acierta el concepto y falla el modelo exacto.

Nota del orador: El mismo par, medido por las cinco funciones. Un título en ucraniano y uno en español, sin un solo token compartido: TF-IDF da 0,16, Jaccard 0,09. El cross-encoder da 0,99927 — entiende que hablan del mismo tipo de producto. Pero se equivoca de referencia: acierta el concepto y falla el modelo exacto.

## Lámina 71 — OE4 · Modelos algorítmicos · Lámina 37 · El margen delata la duda
Textos: MODELOS ALGORÍTMICOS · 11 / 12 | El margen: la señal que delata la duda del modelo | SCF091/46 · eligió SCF227/22 | 0,0000000 | score 0,99931 | 27M2N3200S/00 · eligió 27M2N3200A/00 | 0,0000021 | score 0,99973 | 25M2N3200U/00 · eligió 25M2N3200W/00 | 0,0000070 | score 0,99970 | SCF080/24 · eligió SCF080/08 | 0,0000074 | score 0,99812 | Umbral de automatización exigido | 0,0001500 | margen mínimo para decidir sin humano | Los cuatro errores de ranking más graves tienen un margen entre el 1.º y el 2.º de cero a siete millonésimas. El score no avisa —todos pasan de 0,998— pero el margen sí: por eso la compuerta exige score y margen, y estos casos van a revisión en vez de automatizarse.

Nota del orador: Y esa duda es detectable. En los cuatro errores de ranking más graves, la distancia entre el primer y el segundo candidato va de cero a siete millonésimas. El score no avisa: todos pasan de 0,998. El margen sí. Por eso la compuerta exige score y margen, y estos casos van a revisión.

## Lámina 72 — OE4 · Modelos algorítmicos · Lámina 38 · Los cuatro falsos positivos
Textos: MODELOS ALGORÍTMICOS · 12 / 12 | Los cuatro falsos positivos que sobreviven, con nombre y apellido | CONFLICTO DE SUFIJO · SCORE 0,9990564 | SUFIJO DISTINTO · SCORE 0,9989917 | монітор philips 21.5" v-line 221v8/00 fhd va 75hz 221v8/00/01 | philips 24b2n4200 4000 series 24b2n4200/00/rh | sufijo /RH = otra referencia | dos códigos en un mismo título | REACONDICIONADO · SCORE 0,9989718 | SUFIJO DISTINTO · SCORE 0,9990379 | philips höyrysilitysrauta täydellinen hoito kompakti gc7844/20 | philips qled 85pus8510 85" 4k ambilight smart tv titan os barra de sonido tab4000 | el original y el R1 comparten texto | televisor + barra de sonido en un paquete | Cuatro de 113 negativos del test cruzan el umbral de 0,9988440. Ninguno es un error caprichoso: los cuatro son casos donde el texto publicado sí describe el producto, y lo que difiere es la referencia comercial exacta.

Nota del orador: Los cuatro falsos positivos que sobreviven, con su título real. Un título con dos códigos; un sufijo /RH que designa otra referencia; un producto reacondicionado que comparte texto con el original; y un paquete de televisor más barra de sonido. Ninguno es caprichoso: en los cuatro, el texto sí describe el producto.

## Lámina 73 — OE5 · Evaluación técnica · Lámina 39 · Recall@1 sobre las 147 consultas
Textos: EVALUACIÓN CON MÉTRICAS DE CLASIFICACIÓN · 01 / 03 | Recuperación · Recall@1 sobre 147 consultas de test | Techo del pool de candidatos | 91,84% | 12 consultas sin la verdad entre los 20 candidatos | Cascada exacto → transformer | 87,07% | 128 de 147 · MRR 0,8783 | Cascada exacto → TF-IDF | 86,39% | 127 de 147 | TF-IDF char_4_6_enriched | 85,71% | Recall@10 91,16% · el mejor recuperador | Baseline de coincidencia exacta | 85,03% | solo reglas de código | Transformer solo | 82,31% | sin recuperador previo | Embeddings congelados | 8,84% | 13 de 147 · MRR 0,1352 | Las dos mejores cascadas difieren en 3 consultas. McNemar exacto: p = 1,0 — se reporta como el mejor resultado puntual observado, no como superioridad demostrada.

Nota del orador: Recuperación sobre el test. La mejor cascada acierta en primera posición el 87,07%. Pero las dos mejores difieren en tres consultas y el test de McNemar da p igual a 1. Por eso se reporta como el mejor resultado observado, no como superioridad demostrada.

## Lámina 74 — OE5 · Evaluación técnica · Lámina 40 · El F1 sin la matriz engaña
Textos: EVALUACIÓN CON MÉTRICAS DE CLASIFICACIÓN · 02 / 03 | Clasificación de pares · el F1 sin la matriz engaña | 1 | 2 | 3 | TF-IDF / umbral 0,5238 | Embeddings / umbral 0,378 | Cross-encoder / umbral 0,998844 | 72,04% | 73,42% | 97,41% | F1 DE PARES | F1 DE PARES | F1 DE PARES | Precisión 61,70% · Recall 90,63% — | acepta casi todo | Precisión 74,44% · Recall 69,79% | Precisión 96,91% · Recall 97,92% | 35,38% | 83,08% | 4,62% | FALSOS POSITIVOS | FALSOS POSITIVOS | FALSOS POSITIVOS | Los modelos 1 y 2 parecen equivalentes por F1 (72,04% y 73,42%) y sus matrices son opuestas. Aquí la superioridad del cross-encoder sí es contundente y no ambigua.

Nota del orador: Clasificación de pares. Los modelos uno y dos parecen equivalentes por F1 — 72% contra 73% — y sus matrices son opuestas: uno rechaza de más, el otro acepta casi todo. El cross-encoder llega a 97,41% con 4,62% de falsos positivos. Aquí la superioridad sí es contundente.

## Lámina 75 — OE5 · Evaluación técnica · Lámina 41 · Los negativos difíciles
Textos: EVALUACIÓN CON MÉTRICAS DE CLASIFICACIÓN · 03 / 03 | Los negativos difíciles · la cifra que cuenta la historia | Sufijo distinto — NPX150/INT frente a NPX150/90 · 41 pares | Embeddings | 90,24% | TF-IDF | 36,59% | 4,88% | Cross-encoder | Reacondicionado — sufijo R1 · 24 pares | 70,83% | Embeddings | 33,33% | TF-IDF | 4,17% | Cross-encoder | Tasa de falsos positivos. Esta es exactamente la variabilidad de criterio que el planteamiento del problema identifica: confundir dos variantes casi idénticas del mismo producto.

Nota del orador: Y esta es la cifra que cuenta la historia. Sobre variantes casi idénticas del mismo producto, los embeddings fallan el 90% de las veces y TF-IDF el 36%. El cross-encoder, el 4,88%. Esto es exactamente la variabilidad de criterio que el planteamiento del problema identificaba.

## Lámina 76 — OE5 · Evaluación técnica · Lámina 42 · La matriz de confusión
Textos: EVALUACIÓN CON MÉTRICAS DE CLASIFICACIÓN · 04 / 05 | La matriz de confusión del cross-encoder sobre el test | PREDICHO: CORRESPONDENCIA | PREDICHO: NO CORRESPONDE | 222 | 9 | REAL: CORRESPONDE | 231 pares | VERDADEROS POSITIVOS | FALSOS NEGATIVOS | 4 | 109 | REAL: NO CORRESPONDE | 113 pares | FALSOS POSITIVOS | VERDADEROS NEGATIVOS | 0,998844 | 344 | 3,5 % | 3,9 % | UMBRAL FIJADO EN VALIDACIÓN | PARES DE TEST | TASA DE FALSO POSITIVO | TASA DE FALSO NEGATIVO | El umbral se fijó sobre validación y se aplicó sin retocar al test — es la única forma de que la cifra signifique algo. Los 4 falsos positivos son los cuatro títulos de la lámina anterior.

Nota del orador: La matriz completa sobre los 344 pares de test: 222 aciertos positivos, 109 negativos correctos, 4 falsos positivos y 9 falsos negativos. El umbral se fijó en validación y se aplicó al test sin retocarlo — es la única forma de que la cifra signifique algo.

## Lámina 77 — OE5 · Evaluación técnica · Lámina 43 · El techo del recuperador
Textos: EVALUACIÓN CON MÉTRICAS DE CLASIFICACIÓN · 05 / 05 | El techo que ningún reordenador puede superar | Consultas de test | 147 | publicaciones a resolver | Con el producto correcto dentro del pool | 135 | techo del recuperador · 91,8 % | Acertadas en primera posición | 121 | Recall@1 · 82,3 % | Acertadas dentro de las cinco primeras | 129 | Recall@5 · 87,8 % | Imposibles: la verdad nunca entró al pool | 12 | el reordenador no puede recuperarlas | De los 26 fallos de primera posición, 12 son irrecuperables: el candidato correcto nunca llegó a la lista. Mejorar el reordenador no los arregla — hay que ensanchar la recuperación. MRR 0,8515.

Nota del orador: Y una limitación que conviene decir antes de que la pregunten. De los 26 fallos de primera posición, 12 son irrecuperables: el candidato correcto nunca entró al pool. Mejorar el reordenador no los arregla; hay que ensanchar la recuperación.

## Lámina 78 — OE5 · Evidencia externa · Lámina 44 · Gold externo, los tres modelos
Textos: EVIDENCIA FUERA DEL DATASET · 01 / 04 | Gold externo: los tres modelos sobre datos que nunca vieron | M1 | M2 | M3 | TF-IDF | Embeddings | Unión + reordenador | Recupera por n-gramas de caracteres | Compara sentido, no caracteres | Lee los dos textos juntos | 0,615 | 0,183 | 0,615 | RECALL@1 | RECALL@1 | RECALL@1 | R@5 0,8638 · MRR 0,7315 | R@5 0,3380 · MRR 0,2566 | R@5 0,8357 · MRR 0,7025 | 213 consultas anotadas a mano, fuera del entrenamiento. Bootstrap pareado de 10.000 muestras: la diferencia entre M1 y M3 en Recall@1 es exactamente 0,0, IC 95 % [−0,047; +0,047], p = 1,0. El reordenador no mejora la recuperación aquí; su aporte es decidir cuándo automatizar.

Nota del orador: 213 consultas anotadas a mano, fuera del entrenamiento. Y aquí el resultado es honesto: modelo uno y modelo tres empatan en Recall@1. El bootstrap de diez mil muestras da una diferencia de exactamente cero. El aporte del reordenador no es recuperar mejor: es decidir cuándo automatizar.

## Lámina 79 — OE5 · Evidencia externa · Lámina 45 · Bélgica, dos publicaciones reales
Textos: EVIDENCIA FUERA DEL DATASET · 02 / 04 | Bélgica: dos publicaciones reales y lo que el sistema hizo | COOLBLUEBE · PUBLICADO TAL CUAL | Philips Ambilight 43" PUS8550 QLED (2025) | 43PUS8550/12 | 0,994589 | 0,010567 | Revisión | CANDIDATO ELEGIDO | SCORE | MARGEN | CANDIDATO CORRECTO | COOLBLUEBE · PUBLICACIÓN COMPUESTA | Philips 55" PUS7800 QLED 4K (2025) + Philips TAB5309 | TAB5309/10 | 0,996685 | 0,002209 | Revisión | CANDIDATO ELEGIDO | SCORE | MARGEN | GOLD: NIC | La segunda publicación vende un televisor y una barra de sonido: no corresponde a un solo producto del catálogo. El score es altísimo, pero el margen de 0,0022 delata la ambigüedad y el sistema se abstiene. Se abstiene por la razón correcta.

Nota del orador: Dos publicaciones belgas reales. La primera se resuelve bien. La segunda vende un televisor y una barra de sonido: no corresponde a un solo producto del catálogo. El score es altísimo, pero el margen de 0,0022 delata la ambigüedad y el sistema se abstiene. Se abstiene por la razón correcta.

## Lámina 80 — OE5 · Evidencia externa · Lámina 46 · Benchmark multipaís v7.5
Textos: EVIDENCIA FUERA DEL DATASET · 03 / 04 | Benchmark multipaís v7.5: 2.365 publicaciones, 19 países | 2.365 | 54,2 % | 94,5 % | 70 | PUBLICACIONES EVALUADAS | AUTOMATIZADAS · 1.282 | PRECISIÓN AUTOMATIZADA | DESACUERDOS EXTERNOS | Kuwait · Xcite | 100,0 % | 173 consultas · 67,6 % automatizadas | Sudáfrica · Makro | 98,1 % | 353 consultas · 45,3 % automatizadas | Vietnam · ShopeeVN + LazadaVN | 96,2 % | 293 consultas · 62,1 % automatizadas | Alemania · AmazonDE + MediamarktDE | 87,6 % | 360 consultas · 23 errores | Estados Unidos · AmazonUS | 80,9 % | 124 consultas · 18 errores | Ningún retailer de esta prueba estuvo en el entrenamiento. Los dos peores son los dos marketplaces más grandes: títulos escritos por vendedores terceros, sin código y con la marca repetida. La degradación tiene una causa identificable, no es ruido.

Nota del orador: La prueba de generalización: 2.365 publicaciones, 19 países, ningún retailer visto en el entrenamiento. 54,2% automatizado con 94,5% de precisión. Los dos peores resultados son los dos marketplaces más grandes, donde el título lo escribe un vendedor tercero. La degradación tiene una causa identificable.

## Lámina 81 — OE5 · Evidencia externa · Lámina 47 · Con código y sin código
Textos: EVIDENCIA FUERA DEL DATASET · 04 / 04 | Con código y sin código: el mismo sistema, dos desenlaces | AMAZONDE · ALEMANIA · RETAILER NO VISTO | Philips TV Philips 32PFS5603/12 80 cm (32 Zoll) Full-HD Fernseher (Triple Tuner), Weiß | el título lleva el código completo | 32PFS5603/12 | 0,999573 | 32PFS5603/12 | Match | ELEGIDO | SCORE | GOLD | AUTOMATIZADO Y CORRECTO | MAKRO · SUDÁFRICA · RETAILER NO VISTO | Philips Air Fryer (7.2 L) | ningún código · solo categoría y capacidad | NA341/00 | 0,999650 | HD9285/90 | Match | ELEGIDO | SCORE | GOLD | AUTOMATIZADO Y ERRADO | Mismo umbral, misma compuerta, scores casi idénticos — y uno acierta y el otro no. Sin código en el título, «Philips Air Fryer (7,2 L)» describe varias freidoras del catálogo: el modelo elige una plausible con total confianza. Es el límite del método, y es el que marca dónde sigue haciendo falta el operador.

Nota del orador: Y esta lámina explica por qué. Dos publicaciones, mismo umbral, scores casi idénticos. La primera lleva el código en el título y acierta. La segunda dice solo «Philips Air Fryer, 7,2 litros» — que describe varias freidoras del catálogo — y el modelo elige una plausible con total confianza. Es el límite del método.

## Lámina 82 — OE6 · Contraste operativo · Lámina 48 · Línea base manual observada
Textos: OE6 · CONTRASTE CON EL PROCESO MANUAL · 01 / 09 | Línea base manual observada | PERIODO | TIEMPO ACTIVO | PUBLICACIONES-SEMANA | PROMEDIO | 24–27 AGO | 27.120 s | 1.826 | 14,852 s | 31 AGO–3 SEP | 35.460 s | 1.942 | 18,260 s | Combinado | 62.580 s | 3.768 | 16,608 s | REGISTROS OPERATIVOS · 2 SEMANAS | UNIDAD: PUBLICACIÓN-SEMANA

Nota del orador: La línea base reúne dos semanas operativas. Se registraron 62.580 segundos para 3.768 publicaciones-semana. El promedio combinado es 16,608 segundos por publicación-semana.

## Lámina 83 — OE6 · Contraste operativo · Lámina 49 · Latencia del sistema v7.5
Textos: OE6 · CONTRASTE CON EL PROCESO MANUAL · 02 / 09 | Latencia del sistema v7.5 | −60,76% | COMPARACIÓN UNITARIA | 2.365 | 15.411,8 s | 4,28 h | −10,092 s | CONSULTAS | EJECUCIÓN | MÁQUINA | DIFERENCIA UNITARIA

Nota del orador: La corrida v7.5 procesó 2.365 consultas en 15.411,8 segundos. La latencia promedio fue 6,5166 segundos por consulta, equivalente a una reducción unitaria del 60,76% frente a la línea base manual.

## Lámina 84 — OE6 · Contraste operativo · Lámina 50 · Escenario operativo asistido
Textos: OE6 · CONTRASTE CON EL PROCESO MANUAL · 03 / 09 | Escenario operativo asistido · 2.365 publicaciones | ESCENARIO | CASOS HUMANOS | HORAS HUMANAS | HORAS DE MÁQUINA | TIEMPO SECUENCIAL | Manual | 2.365 | 10,91 h | — | 10,91 h | Asistido | 1.083 | 5,00 h | 4,28 h | 9,28 h | Diferencia | −1.282 | −5,91 h | +4,28 h | −1,63 h | −54,21% | −14,97% | 54,21% | HORAS HUMANAS | TIEMPO SECUENCIAL | COBERTURA AUTOMÁTICA

Nota del orador: En el mismo lote, el proceso manual proyecta 10,91 horas humanas. Con el modelo, el operador revisa 1.083 casos y utiliza 5,00 horas humanas. La reducción del trabajo humano es 54,21%; si máquina y persona se consideran secuenciales, la reducción total es 14,97%.

## Lámina 85 — OE6 · Contraste operativo · Lámina 51 · Consistencia durante la evaluación y el uso
Textos: OE6 · CONTRASTE CON EL PROCESO MANUAL · 04 / 09 | Consistencia durante la evaluación y el uso | Evaluación interna · Modelo 3 | Benchmark externo · v7.5 | Uso controlado | 0 | 96,89% | 94,54% | EXACTITUD · 161 PARES | COINCIDENCIA SELECTIVA | ERRORES REGISTRADOS | 97,41% | 70 / 1.282 | Aceptado | F1-SCORE | DESACUERDOS AUTOMATIZADOS | REGISTRO DE USO

Nota del orador: La evaluación interna del Modelo 3 alcanza 96,89% de exactitud y 97,41% de F1. En el benchmark externo, la coincidencia selectiva es 94,54%. Los 70 casos son desacuerdos externos; durante el uso controlado se registraron cero errores.

## Lámina 86 — Contrastación de la hipótesis · Lámina 52 · Resultados de la consistencia de la calidad
Textos: OE6 · CONTRASTACIÓN DE LA HIPÓTESIS · 05 / 09 | Resultados de la consistencia de la calidad | Accuracy | 94 + 62 | Error | 3 + 2 | × 100 = | 96,89% | × 100 = | 3,11% | 161 | TASA ALGORÍTMICA | 161 | EXACTITUD | Precisión | 94 | Recall | 94 | × 100 = | 96,91% | × 100 = | 97,92% | VERDADEROS POSITIVOS | 94 + 3 | SENSIBILIDAD | 94 + 2 | F1-score | 96,91 × 97,92 | 2 × | = | 97,41% | MEDIA ARMÓNICA | 96,91 + 97,92 | USO CONTROLADO | ERRORES REGISTRADOS = 0

Nota del orador: Con 94 verdaderos positivos, 62 verdaderos negativos, 3 falsos positivos y 2 falsos negativos, la exactitud es 96,89%, la precisión 96,91%, el recall 97,92%, el F1 97,41% y la tasa de error 3,11%. En el uso controlado, la tasa de error observada es cero.

## Lámina 87 — Contrastación de la hipótesis · Lámina 53 · Resultados del tiempo de validación
Textos: OE6 · CONTRASTACIÓN DE LA HIPÓTESIS · 06 / 09 | Resultados del tiempo de validación | Promedio manual | Latencia v7.5 | 27.120 + 35.460 | 16,608 s | 15.411,8 | 6,5166 s | = | = | 1.826 + 1.942 | 2.365 | PUBLICACIÓN-SEMANA | POR CONSULTA | Reducción unitaria | Reducción humana | 16,608 − 6,5166 | 60,76% | 10,9114 − 4,9967 | 54,21% | × 100 = | × 100 = | 16,608 | 10,9114 | MANUAL FRENTE A MODELO | ESCENARIO ASISTIDO | Reducción total | Tiempo de máquina | 10,9114 − 9,2778 | 14,97% | 15.411,8 s | 4,28 h | × 100 = | = | 10,9114 | 3.600 | TIEMPO SECUENCIAL | EJECUCIÓN COMPLETA

Nota del orador: La línea base manual resulta de dividir 62.580 segundos entre 3.768 publicaciones-semana: 16,608 segundos. La latencia del modelo es 15.411,8 entre 2.365: 6,5166 segundos. La reducción unitaria es 60,76%, la reducción de horas humanas 54,21% y la reducción secuencial total 14,97%.

## Lámina 88 — Contrastación de la hipótesis · Lámina 54 · Matriz de contrastación de la hipótesis
Textos: OE6 · CONTRASTACIÓN DE LA HIPÓTESIS · 07 / 09 | Matriz de contrastación de la hipótesis | VARIABLE | EVIDENCIA | RESULTADO | VI | Modelo de PLN | Modelo 3 · cascada v7.5 · HITL | APLICADO | VD₁ | 96,89% interna · 94,54% externa · 0 errores de uso | MEJORA | Consistencia | VD₂ | 6,5166 s/consulta · −54,21% humano · −14,97% total | Tiempo | REDUCE | Hipótesis aceptada | CONSISTENCIA DE LA CALIDAD + REDUCCIÓN DEL TIEMPO

Nota del orador: La variable independiente se materializa en el Modelo 3, la cascada v7.5 y el esquema Human in the Loop. Para la primera variable dependiente, la evidencia interna, externa y de uso muestra mejora de consistencia. Para la segunda, la latencia y las horas humanas demuestran reducción del tiempo.

## Lámina 89 — Contrastación de la hipótesis · Lámina 55 · Contrastación de la hipótesis
Textos: OE6 · RESULTADO FINAL · 08 / 09 | Contrastación de la hipótesis | VI | Modelo de PLN | VD₁ | Consistencia | VD₂ | Tiempo de validación | El modelo de Procesamiento de Lenguaje Natural mejora la consistencia de la calidad del matching y reduce el tiempo de validación, en comparación con el proceso manual, en el área de operaciones de Agilsoft SRL. | HIPÓTESIS ACEPTADA

Nota del orador: Por tanto, el modelo de Procesamiento de Lenguaje Natural mejora la consistencia de la calidad del matching y reduce el tiempo de validación, en comparación con el proceso manual, en el área de operaciones de Agilsoft SRL. Se acepta la hipótesis dentro del alcance del estudio.

## Lámina 90 — Cierre · Lámina 56 · Gracias
Textos: Gracias | MODELO DE PROCESAMIENTO DE LENGUAJE NATURAL EN LA VALIDACIÓN DE CORRESPONDENCIA DE PRODUCTOS DEL ECOSISTEMA PHILIPS | PABLO ENRIQUE CAÑEZ LARICO

Nota del orador: Muchas gracias por su atención. Quedo atento a sus preguntas.
