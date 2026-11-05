# Inventario y conciliación de insumos de B01

Corte de inventario 5 de noviembre de 2026. La copia de trabajo es `C:/Users/marce/Downloads/PAPIME/papime-crd`. El inventario corresponde a los insumos preexistentes y al commit base, no a una lista variable de archivos generados durante la compilación.

## Versión rectora y procedencia

La planeación vigente es `PLAN_FINAL_PAPIME.md`; su copia mantenida pasa a `seguimiento/PLAN.md`. El manuscrito rector es el PDF de la carpeta raíz, por instrucción del autor. El repositorio se recibió en `main`, commit `458257c3d7b69602560cbcaeb89fd0980297ad6b`, el mismo que documenta el plan. En ese corte hay 294 archivos versionados, principalmente datos y scripts, sin proyecto bookdown. Se conservan sus nombres y ubicaciones para no romper las rutas de los análisis heredados.

| Insumo | Resultado de conciliación | Tratamiento |
|---|---|---|
| `PAPIME Libro.pdf` de la raíz | 64 páginas carta, creado el 4 de noviembre de 2026 según metadatos; contiene la sección de especialización integrada | Manuscrito rector conservado íntegro |
| `PAPIME_Mx/referencias/PAPIME_Libro.pdf` | 35 páginas, antecedente del 26 de octubre según metadatos; su SHA256 difiere del rector | Antecedente, sin sustituir al PDF de 64 páginas |
| Dos copias de `CONTEXTO_PAPIME_Mx_Especializacion.md` | Coinciden byte por byte | Se conserva su procedencia y se usa el contexto como registro de acuerdos |
| `Medicion_de_la_Especializacion (1).docx` de la raíz | 2,754 palabras de texto extraído; coincide en la apertura con el PDF rector | Variante del manuscrito, conservada para cotejo |
| `PAPIME_Mx/output/Medicion_de_la_Especializacion.docx` | 2,724 palabras de texto extraído; difiere de la variante de la raíz | Entrega antecedente vinculada a `texto/seccion_revisada.md` |
| `PAPIME_Mx/texto/seccion_revisada.md` | Texto editable con marcadores de ecuaciones y figuras, documentado en el contexto de continuidad | Fuente recuperable del piloto; las adaptaciones de selección y composición se registran |
| `PAPIME_Mx/datos/PIBE_2024_In.xlsx` | Matriz recibida con 32 entidades y 21 actividades, 2024 a precios de 2018 | Insumo congelado, sin actualización automática |
| `PAPIME_Mx/output/Figuras_Capitulo_II_Especializacion_2024` | Once figuras en PNG y PDF, tablas de índices y guía del cálculo | Resultados antecedentes para contraste, no sustituyen la reproducción |
| `PAPIME_Mx/Cartografia_INEGI/entidades_INEGI.geojson` | Cartografía de 28,836,523 bytes | Conservar el original; documentar cualquier simplificación antes de publicación |
| `Mexicana_Tarea_3` | 129 archivos de cartografía, bases y resultados de geografía | Antecedentes para B02; no se incorporan como evidencia nueva en B01 |
| `tools` | Herramientas locales anteriores | Inventariadas como antecedentes técnicos |

Los recuentos de palabras se obtuvieron del texto de `word/document.xml`, sin usar propiedades de Word; sirven para distinguir variantes y no certifican equivalencia semántica. Los metadatos de creación tampoco prueban fecha de consulta de las fuentes. La revisión del capítulo deberá cotejar variantes con el PDF rector antes de reemplazar su prosa. B01 adapta un fragmento para probar la plantilla; no sustituye el manuscrito completo.

## Integridad comprobada

`inventario-insumos.csv` reúne 476 registros: 182 archivos locales preexistentes y 294 archivos del commit base. Cada registro conserva bytes y SHA256. Los archivos remotos incluyen además el identificador de blob de Git y el commit de procedencia. Las copias nuevas del proyecto no se mezclan con el inventario de entrada. Para los archivos del commit base, los bytes y SHA256 se calculan sobre el contenido canónico del blob de Git, no sobre su representación de trabajo en Windows, que puede convertir finales de línea LF en CRLF.

Se contrastaron las 43 entradas del manifiesto de traslado `PAPIME_Mx/MANIFIESTO_SHA256.csv` con los archivos actuales: 43 coincidencias y ninguna diferencia. El manifiesto no incluye su propio hash.

| Archivo decisivo | SHA256 |
|---|---|
| PDF rector de 64 páginas | `7bd8d8a23ff225a42728c167723c323a2bedebda7c999a9aa186df7a8e486b35` |
| PDF antecedente de 35 páginas | `f05cce5e149265063d81bc3b1d6e0b4c04d2ffeb538c8d20e10f395aa0df7a12` |
| Contexto de especialización, ambas copias | `32f2b3a25adfbf12760e0907a68e0dd84412c0e62ccb9d4cfdaa0fdd30f1fed3` |
| Excel recibido | `0ce674346f2861aa580ef33a4edd4da653ef8aadd817fc0928be56033843cf79` |

## Lectura del manuscrito y trabajo pendiente por bloque

Se extrajo texto de las 64 páginas y se revisaron visualmente las páginas 1, 3, 18, 26, 45 y 64. Las páginas indicadas son las posiciones físicas del PDF; el manuscrito no presenta folios impresos visibles en la muestra.

| Ubicación física | Contenido encontrado | Continuación prevista |
|---|---|---|
| 1–15 | Capítulo I; evolución territorial sin desarrollar, geografía redactada con seis figuras y notas editoriales | B02 resolverá regionalización, fuentes, cálculos y figuras F01–F06 |
| 16 | Página casi vacía | La plantilla evita reproducir este blanco accidental |
| 17–43 | Capítulo II; introducción, segmentación, especialización, insumo-producto y sector externo | B03 revisará el conjunto y reutilizará los controles del piloto |
| 44 | Capítulo III, título y marca residual `Nig` | B04 desarrollará el capítulo; la marca no se traslada al libro |
| 45–58 | Capítulo IV, modelos, energía, ubicación y puertos | B05 reproducirá regresiones y figuras; en p.51 falta la tabla de estimación |
| 59 | Capítulo V, sólo título | B06 |
| 60 | Capítulo VI, sólo título | B07 |
| 61 | Capítulo VII, inicio breve | B08 |
| 62 | Capítulo VIII, sólo título | B09 |
| 63 | Conclusiones, sólo título | B10 |
| 64 | Bibliografía breve, algunas entradas incompletas | Matriz inicial B01 y verificación por capítulo |

La bibliografía menciona Miller y Blair (2021), mientras que el cuerpo utiliza Miller y Blair (2009). No se unifican años por conjetura: B03 deberá identificar la edición efectivamente consultada. Asuad (2020) y Bhattacharyya (2019) requieren completar datos editoriales. La bibliografía final actual no reúne todas las citas del capítulo I, incluidas las atribuciones concretas a Ruiz Durán.

## Insumos por recuperar o confirmar

No se encontró el archivo editable del libro completo. El PDF rector permite recuperar estructura y redacción; un original de Word, si existe, facilitará cotejar ecuaciones y tablas del resto del libro. Esta ausencia no impide completar el piloto.

El repositorio contiene `mipme_f.csv`, `mipme_index.csv` y `mipme_va.csv`. Su presencia no demuestra que la base regional esté validada: B03 debe comprobar correspondencias, unidad, periodo y orientación de matrices antes de usarla. Las bases nacionales y los scripts heredados también requieren revisión dentro de sus capítulos.

En geografía permanecen pendientes la regionalización del curso y los cálculos marcados F01–F06. F01 no mide accesibilidad efectiva; F02 no construye un índice de aptitud; F04 requiere validar agregaciones y localizaciones. F05 compara agua y población y excluye asignar PIB estatal a regiones hidrológico-administrativas sin método reproducible. Estos acuerdos se conservan.

La fecha exacta de descarga original del PIBE y algunas capas no está demostrada por sus archivos. Se mantiene el corte recibido y se distingue la comprobación de B01 de una nueva consulta al productor. Los archivos de bibliografía registrarán por separado obra accesible, texto revisado y páginas pendientes.

El inventario registra materiales grandes sin eliminarlos ni volver a descargarlos. La distribución de la cartografía y otras bases pesadas deberá conservar su procedencia, integridad y un mecanismo reproducible; las versiones simplificadas son derivados identificables.
