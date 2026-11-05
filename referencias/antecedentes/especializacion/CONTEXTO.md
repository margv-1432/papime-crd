# PAPIME_Mx: contexto completo para continuar el trabajo sobre medición de la especialización

**Fecha del documento:** 4 de noviembre de 2026, hora de referencia de Ciudad de México.  
**Proyecto:** PAPIME_Mx.  
**Tema y ubicación:** capítulo II, “Estructura productiva y especialización regional”, inciso 2, “Medición de la especialización”.  
**Estado al cierre del chat:** sección redactada y revisada; código y resultados terminados; última modificación aceptada: revisión de la prosa y cinco entidades destacadas en cada mapa.

Este archivo reúne el encargo, las decisiones metodológicas, la evolución de las entregas y el estado verificable de los archivos. Está pensado para incorporarse a un proyecto nuevo que trabaje en una carpeta de la computadora del usuario. El futuro asistente debe tomar la última versión entregada como punto de partida y aplicar los cambios que el usuario solicite después de este documento.

El registro distingue las modificaciones ya realizadas de las adaptaciones añadidas para trasladar el proyecto. Los apéndices conservan el manuscrito completo con sus marcas de ecuaciones y figuras, el script R vigente, un generador de Word adaptado a rutas locales y la matriz original en CSV. El paquete `PAPIME_Mx_Continuidad_Local.zip` acompaña este MD con los archivos binarios y las figuras que el Markdown no incorpora como imágenes.

No se necesitan conversaciones sobre otros proyectos del usuario para continuar este trabajo. El contexto pertinente es el manual de economía mexicana y su apartado de especialización regional.

## 1. Lectura inicial para el nuevo proyecto

Antes de editar, conviene revisar las secciones 2 a 6, las especificaciones gráficas de la sección 7 y las instrucciones editoriales de la sección 9. La sección 12 explica la carpeta local; la sección 13 contiene las instrucciones de ejecución. Los apéndices permiten recuperar el contenido editable aunque sólo se conserve este MD.

Las decisiones que deben mantenerse son las siguientes:

- El texto pertenece a un manual universitario: la teoría organiza la exposición y los datos mexicanos sirven para explicar los conceptos.
- KSI e ICE se calculan como sumas de diferencias absolutas, **sin dividir entre dos**. La escala general utilizada es de cero a dos.
- El IEE es el cociente de localización aplicado al valor agregado. Se calcula para las 672 combinaciones de entidad y actividad.
- Los denominadores son las sumas sectoriales del VAB. Los cálculos utilizan la matriz de 2024 a precios de 2018 proporcionada por el usuario.
- Se conservan 32 entidades y 21 actividades, con minería petrolera y no petrolera separadas.
- El mapa de calor presenta toda la matriz, sin números dentro de las celdas.
- El mapa de calor y los mapas del IEE comparten un degradado continuo de azul a rojo oscuro y una barra horizontal inferior. El mapa del KSI utiliza esa familia de colores con su propia escala.
- Se producen cinco mapas independientes: uno del KSI y cuatro del IEE. Todos identifican las cinco entidades con mayor índice.
- La prosa debe ser formal, continua y explicativa, con variación natural de los párrafos y sin advertencias hipotéticas innecesarias.

La última petición del usuario antes de solicitar este MD ya fue atendida. No hay un encargo pendiente de ampliar el capítulo, cambiar los índices, actualizar el año de los datos o modificar nuevamente la paleta. El trabajo posterior dependerá de sus nuevas instrucciones.

## 2. Encargo original y alcance

El usuario pidió actuar como un economista con doctorado y experiencia en economía mexicana, economía regional, geografía económica y matemáticas. El objetivo fue escribir una sección comprensible para estudiantes de Economía que explicara los métodos de medición de la especialización productiva y los ilustrara con México.

La sección debía ocupar aproximadamente entre 2,000 y 3,000 palabras e incorporar las especificaciones, variables e interpretación del KSI, el ICE y el Índice de Especialización Económica. También debía incluir referencias a la literatura y figuras vinculadas con el desarrollo teórico. El avance del libro se utilizó como guía de redacción y como referencia de la ubicación del apartado.

El capítulo II del PDF original tiene como título “Estructura productiva y especialización regional”. El inciso anterior se titula “Segmentación de la producción” y el siguiente, “Cadenas de valor regionales”, introduce la matriz de insumo-producto. El apartado escrito termina con una transición hacia ese tema. No corresponde reescribir los demás incisos del libro por iniciativa propia.

### 2.1. Insumos proporcionados

| Nombre mencionado por el usuario | Archivo efectivamente disponible en este entorno | Función |
| --- | --- | --- |
| `PAPIME Libro.pdf` | `upload/PAPIME Libro.pdf` | Avance del manual; estructura y referencia de estilo |
| `Plots_Krugman_2024.R` | `upload/Plots_Krugman_2024(3).R` | Script de referencia anterior a las modificaciones de este chat |
| `PIBE_2024_In.xlsx` | `upload/PIBE_2024_In(2).xlsx` | Datos y cálculos originales de KSI e ICE |

Los sufijos `(2)` y `(3)` corresponden a los nombres de los archivos recibidos en el entorno de trabajo. En la carpeta nueva, el Excel se guarda como `datos/PIBE_2024_In.xlsx`; el script anterior se distingue como `referencias/Plots_Krugman_2024_original.R`. Cambiar esos nombres para ordenar la carpeta no altera sus bytes.

### 2.2. Entregables del trabajo principal

Se entregó un documento Word independiente con la sección, un script R que reproduce los cálculos y las figuras, y un ZIP con las figuras, tablas e instrucciones. El archivo original del libro no fue sustituido por un PDF con el inciso insertado; la sección está preparada para integrarse posteriormente al manual.

El Excel original se mantuvo como insumo. El IEE se añadió al flujo de cálculo de R y se exportó a CSV; no se añadió una hoja nueva con ese índice dentro del Excel original. El script R recibido se conserva como referencia y se distingue del script R final, aunque ambos llevan nombres relacionados con `Plots_Krugman_2024`.

## 3. Evolución de las versiones y solicitudes atendidas

La secuencia siguiente registra el orden de las modificaciones. No asigna fechas a cada iteración, porque el historial disponible no permite establecerlas con la misma precisión que el orden de las solicitudes.

| Etapa | Solicitud o decisión | Resultado y condición vigente |
| --- | --- | --- |
| Encargo inicial | Redactar el inciso, explicar KSI, ICE e IEE y ajustar el script con ejemplos mexicanos | Se auditó la matriz, se calcularon los índices y se produjo una primera sección de unas 2,300 palabras con cinco figuras integradas. La primera entrega generaba nueve figuras |
| Primera revisión editorial y gráfica | Dar más peso a la teoría; eliminar aperturas cortas obligatorias; representar toda la matriz; separar y estilizar los mapas | Se amplió el desarrollo teórico y se incorporó el mapa de calor de 32 × 21. Los cuatro mapas del IEE pasaron a archivos independientes. La sección llegó a unas 2,600 palabras y ocho figuras integradas |
| Revisión de colores | Usar un degradado de azul relativamente oscuro a rojo oscuro; sustituir cajas de colores por una barra horizontal inferior | Se estableció la escala continua actual. El mapa de calor y los mapas sectoriales comparten la misma escala del IEE; el KSI utiliza una escala de cero a dos |
| Última revisión de estilo y etiquetas | Quitar construcciones hipotéticas que sonaban artificiales y pasar del top 2 al top 5 | Se revisaron los 28 párrafos del cuerpo. El texto quedó en aproximadamente 2,500 palabras y los cinco mapas señalan cinco entidades cada uno |
| Entrega de contexto | Documentar todo para continuar en una carpeta local | Se preparó este MD, se volvieron a contrastar los datos y se reunió un paquete de traslado con los insumos y los archivos finales. Se añadieron un lanzador local de R y una copia portátil del generador de Word |

Las menciones a “nueve figuras” y “cinco figuras integradas” corresponden a la primera versión. **El estado final tiene once figuras producidas, ocho integradas en el Word y cinco mapas separados.**

Entre los nombres de figuras que quedaron sustituidos durante las revisiones están `05_IEE_ejemplos`, `06_Matriz_IEE_completa` y `09_Mapas_IEE`. No deben confundirse con la entrega vigente. El mapa de calor actual se llama `05_Matriz_IEE_completa` y los mapas sectoriales actuales son los archivos 09 a 12.

## 4. Datos: fuente, cobertura y organización exacta

### 4.1. Fuente y unidad

El libro Excel corresponde al Producto Interno Bruto por Entidad Federativa del INEGI para 2024. Las cifras utilizadas están expresadas en **millones de pesos de 2018**. La referencia “INEGI (2026)” que aparece en las figuras es el año de consulta conservado del script original; no debe interpretarse como el año de los datos ni como una nueva comprobación de la fecha de publicación de la serie.

El archivo contiene dos hojas:

| Hoja | Uso en el trabajo |
| --- | --- |
| `2024 - Millones de pesos 2018` | Hoja de información original del libro; se conserva con el archivo recibido |
| `Indices_Krugman` | Fuente directa de la matriz y lugar donde se encuentran los valores originales de KSI e ICE usados para comprobación |

El script reconoce la hoja de índices normalizando mayúsculas, espacios, acentos y guiones bajos. Con el archivo actual, su nombre exacto es `Indices_Krugman`.

### 4.2. Rango de lectura y dimensiones

| Parte del Excel | Contenido |
| --- | --- |
| `A1:W34` | Tabla completa leída por R, incluidos encabezados |
| `A1` | Encabezado de entidad federativa |
| `B1:V1` | Encabezados de las 21 actividades |
| `W1` | Total |
| `A2:A33` | Nombres de las 32 entidades |
| `B2:V33` | Matriz económica original de 32 × 21 |
| `W2:W33` | Totales estatales que se contrastan con las sumas de fila |
| `A34` | `Estados Unidos Mexicanos` |
| `B34:V34` | Totales nacionales por actividad |
| `W34` | Total nacional de la tabla |
| `W78:W109` | KSI precalculado, empleado únicamente para comprobación |
| `B147:V147` | ICE precalculado, empleado únicamente para comprobación |

Al usar la primera fila como encabezado, R obtiene 33 filas de datos y 23 columnas: las 32 entidades más el total nacional. La matriz de cálculo excluye la fila nacional y la columna de total.

El total nacional obtenido al sumar las 21 actividades es **23,982,097.474 millones de pesos de 2018**. Las 672 celdas estatales contienen valores numéricos no negativos; hay **36 ceros**. No se sustituyeron ceros por datos faltantes ni se eliminó alguna entidad o actividad para producir las figuras.

### 4.3. Valor agregado y denominadores

La suma de las actividades de la matriz corresponde al valor agregado bruto, identificado en el trabajo como VAB. Éste es el agregado utilizado para obtener las participaciones. El PIB incorpora además los impuestos netos de subsidios sobre los productos; dividir las actividades de esta matriz entre un agregado diferente rompería la condición de que las participaciones sectoriales sumen uno.

Esta decisión se refleja en el texto, el código y las tablas. Aunque el producto estadístico de origen se llame PIBE, la variable `VAB` del script es la suma de las actividades efectivamente utilizadas. No debe cambiarse su denominador sin reconstruir la base de comparación y revisar todo el desarrollo teórico.

### 4.4. Actividades y orden

La apertura de la minería sustituye el sector agregado por minería petrolera y no petrolera. Así se pasa de veinte sectores a veintiuna actividades sin duplicar la producción. `21-1` y `21-2` son las etiquetas de esa apertura en la tabla; no son nuevos sectores SCIAN independientes.

| Orden | Código | Actividad en la presentación |
| --- | --- | --- |
| 1 | 11 | 11 Agricultura, ganadería, pesca y actividades forestales |
| 2 | 21-1 | 21-1 Minería petrolera |
| 3 | 21-2 | 21-2 Minería no petrolera |
| 4 | 22 | 22 Electricidad, agua y gas |
| 5 | 23 | 23 Construcción |
| 6 | 31-33 | 31-33 Manufacturas |
| 7 | 43 | 43 Comercio al por mayor |
| 8 | 46 | 46 Comercio al por menor |
| 9 | 48-49 | 48-49 Transportes, correos y almacenamiento |
| 10 | 51 | 51 Información en medios masivos |
| 11 | 52 | 52 Servicios financieros y seguros |
| 12 | 53 | 53 Servicios inmobiliarios y alquiler |
| 13 | 54 | 54 Servicios profesionales, científicos y técnicos |
| 14 | 55 | 55 Corporativos |
| 15 | 56 | 56 Apoyo a negocios, residuos y remediación |
| 16 | 61 | 61 Servicios educativos |
| 17 | 62 | 62 Salud y asistencia social |
| 18 | 71 | 71 Esparcimiento, cultura y deporte |
| 19 | 72 | 72 Alojamiento y preparación de alimentos |
| 20 | 81 | 81 Otros servicios |
| 21 | 93 | 93 Actividades gubernamentales y legislativas |

El script exige que el orden y la selección de estas columnas coincidan con el catálogo esperado. Los rótulos completos del Excel se guardan en `Catalogo_sectores.csv`; las formas abreviadas anteriores se emplean para que las figuras sean legibles.

### 4.5. Identificación de entidades

Las uniones geográficas se hacen con `cve_ent`, en formato de dos caracteres, de `01` a `32`. El script normaliza los nombres del Excel y los relaciona con un registro estatal propio; no une directamente los mapas mediante nombres abreviados.

El registro distingue, entre otros casos, `Coahuila de Zaragoza` de `Coahuila`, `México` de `Estado de México`, `Michoacán de Ocampo` de `Michoacán` y `Veracruz de Ignacio de la Llave` de `Veracruz`. Conviene leer las claves como texto al importar los CSV para conservar los ceros iniciales. `México` en la fila estatal identifica al Estado de México; el país aparece como `Estados Unidos Mexicanos` en la fila nacional.

## 5. Definiciones y decisiones metodológicas

### 5.1. Notación común

Sea $x_{ij}$ el VAB de la actividad $j$ en la entidad $i$, con $i=1,\ldots,32$ y $j=1,\ldots,21$. Los totales se definen como:

$$
x_{i\cdot}=\sum_{j=1}^{21}x_{ij},\qquad
x_{\cdot j}=\sum_{i=1}^{32}x_{ij},\qquad
x_{\cdot\cdot}=\sum_i x_{i\cdot}=\sum_j x_{\cdot j}.
$$

Las participaciones utilizadas son:

| Símbolo | Fórmula | Significado | Nombre en el código |
| --- | --- | --- | --- |
| $s_{ij}$ | $x_{ij}/x_{i\cdot}$ | Participación de la actividad dentro de la entidad | `s`; exportada como `participacion_local` |
| $s_j$ | $x_{\cdot j}/x_{\cdot\cdot}$ | Participación nacional de la actividad | `s_nacional`; exportada como `participacion_nacional` |
| $q_{ij}$ | $x_{ij}/x_{\cdot j}$ | Participación de la entidad en el total nacional de la actividad | `q`; exportada como `participacion_sector` |
| $w_i$ | $x_{i\cdot}/x_{\cdot\cdot}$ | Peso económico de la entidad en el VAB nacional | `peso_estado`; exportado como `peso` |

Las participaciones del archivo se expresan como proporciones, no como porcentajes. El script multiplica por cien únicamente cuando construye la variable `diferencia_pp` o un rótulo porcentual.

### 5.2. KSI: una medida de la composición productiva de cada entidad

$$
KSI_i=\sum_{j=1}^{21}\left|s_{ij}-s_j\right|.
$$

El KSI compara dos estructuras sectoriales y produce un resultado por entidad. Un valor de cero corresponde a participaciones iguales a las del país; el índice aumenta con la distancia entre esas composiciones. El valor absoluto evita que una actividad con mayor participación local compense aritméticamente a otra con menor participación.

La suma sin valores absolutos sería cero porque ambas estructuras suman uno. La contribución de una actividad al índice es $|s_{ij}-s_j|$. La diferencia con signo, $s_{ij}-s_j$, permite saber si esa actividad pesa más o menos en la entidad que en el país; esa información se utiliza en la figura de brechas sectoriales.

La convención de este proyecto mantiene la suma completa, con intervalo general de cero a dos. Su mitad tiene la interpretación de la fracción de participaciones que se reasigna para igualar las estructuras, manteniendo fija la referencia. Por ejemplo, un KSI de 0.4 corresponde a una distancia de 0.2 bajo esa normalización. Explicar esa equivalencia no cambia la normalización utilizada por el código.

La entidad forma parte del agregado nacional con el que se compara. Si $s_{-i,j}$ representa la composición del resto del país, se cumple:

$$
s_j=w_i s_{ij}+(1-w_i)s_{-i,j},\qquad
KSI_i=(1-w_i)\sum_j|s_{ij}-s_{-i,j}|\leq 2(1-w_i).
$$

Se trata de una cota superior, no de un valor que necesariamente alcance una entidad. El Word explica la influencia del tamaño estatal sobre la referencia nacional, pero los resultados vigentes se calculan contra el país completo. No se sustituyó esa referencia por el resto del país.

El KSI mide especialización **relativa a la estructura nacional**. La diversidad interna de una economía requiere examinar sus participaciones sectoriales; no se infiere una diversificación absoluta de un KSI pequeño. En la redacción del manual esta precisión se integra al significado del indicador, sin una sucesión de advertencias hipotéticas.

### 5.3. ICE: una medida de la distribución territorial de cada actividad

$$
ICE_j=\sum_{i=1}^{32}\left|q_{ij}-w_i\right|.
$$

El ICE se obtiene recorriendo cada columna y produce un resultado por actividad. Compara la distribución territorial del VAB sectorial con la distribución territorial del VAB total. Así incorpora el diferente tamaño económico de los estados.

Con ICE igual a cero, una entidad que representa 10 % del VAB nacional también aporta 10 % al VAB de la actividad examinada. La referencia es esa proporcionalidad económica. El reparto idéntico entre las 32 entidades constituye una comparación distinta.

El proyecto utiliza la suma completa, sin factor $1/2$, también en escala general de cero a dos. Las normalizaciones que llevan la distancia al intervalo de cero a uno se mencionan para que el estudiante reconozca la diferencia entre fórmulas.

No existe en este flujo un “ICE de cada estado”: sus 21 resultados corresponden a actividades. Por esa razón el ICE se presenta en barras por sector y en una comparación territorial complementaria; no se hizo un mapa estatal con un supuesto ICE por entidad.

### 5.4. IEE: el cociente de localización

$$
IEE_{ij}=\frac{x_{ij}/x_{i\cdot}}{x_{\cdot j}/x_{\cdot\cdot}}
=\frac{s_{ij}}{s_j}=\frac{q_{ij}}{w_i}.
$$

El IEE describe una combinación de entidad y actividad. Su interpretación se conserva así:

| Valor | Interpretación |
| --- | --- |
| $IEE=0$ | Actividad nula en esa celda, con denominadores positivos |
| $0<IEE<1$ | La actividad tiene menor participación en el VAB estatal que en el nacional |
| $IEE=1$ | Coinciden las participaciones local y nacional |
| $IEE>1$ | La actividad tiene mayor participación relativa dentro de la entidad |
| $IEE=2$ | La participación local duplica la participación nacional |

El IEE no tiene un máximo universal de dos. Su magnitud depende, entre otros elementos, de la participación nacional de la actividad. En la matriz actual el máximo es **22.745029490562416**, correspondiente a minería petrolera en Campeche. El índice no está expresado en puntos porcentuales: un valor de 2.16 representa una razón entre participaciones.

El índice se denomina IEE en este apartado y corresponde al cociente de localización. Se aplica al valor agregado; no se calcularon cocientes con empleo, exportaciones ni número de establecimientos. La productividad y la composición sectorial explican que otras variables puedan producir cocientes distintos.

### 5.5. Relación entre los índices

Las dos distancias se pueden escribir con el IEE:

$$
KSI_i=\sum_j s_j|IEE_{ij}-1|,\qquad
ICE_j=\sum_i w_i|IEE_{ij}-1|.
$$

En el KSI las ponderaciones son las participaciones nacionales de las actividades; en el ICE son los pesos de las entidades en la economía del país. Una misma distancia del IEE respecto de uno aporta más al KSI cuando corresponde a una actividad de mayor peso nacional.

También se cumplen las identidades:

$$
\sum_j s_j IEE_{ij}=1\quad\text{para cada entidad},\qquad
\sum_i w_i IEE_{ij}=1\quad\text{para cada actividad}.
$$

Y la identidad agregada:

$$
\sum_i w_iKSI_i=\sum_j s_jICE_j.
$$

Con los datos de este proyecto, ambos lados son aproximadamente **0.4218519204286904**. El script verifica estas relaciones para detectar errores en denominadores, orientación o correspondencia de los datos. Son comprobaciones del cálculo; no constituyen resultados econométricos.

### 5.6. Agregación y comparabilidad

Al reunir actividades, las diferencias de signo contrario se pueden compensar dentro del nuevo grupo. Por la desigualdad triangular, al mantener datos y referencia comparables, la suma de diferencias absolutas se reduce o se conserva. El script prueba esa propiedad al unir las dos columnas mineras y comparar el KSI de 21 actividades con el de 20 sectores.

En Zacatecas, por ejemplo, el KSI es aproximadamente 0.496361 con la apertura minera y 0.442580 con minería agregada. La diferencia no se debe a eliminar producción: los totales permanecen iguales y cambia el detalle de la clasificación. La figura complementaria de sensibilidad muestra las ocho entidades con mayor variación.

Los índices son invariantes al cambio común de unidad monetaria, como pasar de pesos a millones de pesos. La base de precios y la clasificación sectorial sí afectan las participaciones; al extender el trabajo a otros años se deben mantener coberturas y bases compatibles. La versión actual utiliza exclusivamente los datos proporcionados de 2024.

## 6. Estructura y funcionamiento del script R vigente

El archivo final es `scripts/Plots_Krugman_2024.R` en la carpeta de traslado. Su contenido es idéntico al archivo entregado anteriormente como `output/Plots_Krugman_2024.R`; el apéndice B conserva esa misma versión. No debe confundirse con el script de referencia anterior que se guarda en `referencias/`.

### 6.1. Configuración original conservada

```r
ruta_excel <- "C:/Users/marce/Downloads/PIBE/PIBE_2024_In.xlsx"
carpeta_salida <- file.path(dirname(ruta_excel), "Figuras_Capitulo_II_Especializacion_2024")
carpeta_geografia <- file.path(dirname(ruta_excel), "Cartografia_INEGI")
ruta_cartografia <- ""
crear_mapas <- TRUE
guardar_pdf <- TRUE
n_destacados <- 5L
```

La ruta Windows se mantuvo por instrucción expresa del usuario. La carpeta de resultados se crea junto al Excel con el nombre `Figuras_Capitulo_II_Especializacion_2024`, diferente de la carpeta del script original recibido. Los PNG y CSV de esta carpeta pueden sobrescribirse al volver a ejecutar; conviene conservar una copia de la entrega aceptada antes de una revisión.

No se utiliza `file.choose()`, no se solicita un archivo RDS y no hay un flujo de selección interactiva de modelos. El insumo económico es el Excel. Las rutas del entorno temporal usadas para verificar el script en este chat no deben copiarse como rutas válidas de la computadora del usuario.

### 6.2. Secuencia de cálculo

El script instala los paquetes faltantes, comprueba la existencia del Excel y crea la carpeta de salida. Después identifica la hoja, lee `A1:W34`, valida nombres y columnas, forma la matriz `X` y obtiene los totales. Calcula las participaciones, los tres índices y las aportaciones por celda antes de elaborar las tablas y figuras.

Las operaciones fundamentales se implementan con `rowSums`, `colSums` y `sweep`. Los datos largos se construyen con 672 filas mediante `expand.grid` y las matrices se vectorizan en el mismo orden por columnas de R. Se incorporan los nombres estatales y sectoriales con uniones por claves.

Los índices precalculados del Excel se leen después del cálculo desde la matriz. Sirven como contraste; no alimentan los resultados. La comparación está dentro de un `tryCatch`: si se ha movido el bloque de resultados guardados, se comunica el problema y se conserva el recálculo desde la matriz.

### 6.3. Validaciones incluidas

El código comprueba la existencia de una sola hoja de índices, las dimensiones de la tabla, la fila nacional, la identificación de las 32 entidades y la correspondencia de los 21 códigos. Exige valores finitos, celdas no negativas y denominadores positivos. Las sumas de fila y columna se contrastan con los totales del archivo con tolerancia de 0.02 en la unidad monetaria de origen; las identidades de participaciones e índices utilizan por defecto tolerancia de $10^{-8}$.

Se verifica que las participaciones sectoriales de cada entidad y las participaciones territoriales de cada actividad sumen uno, que las dos expresiones del IEE coincidan, que sus promedios ponderados sean uno y que la identidad agregada entre KSI e ICE se cumpla. Además, se comprueban los rangos generales del KSI y del ICE, los IEE no negativos y la propiedad de agregación minera.

Los faltantes económicos detienen el cálculo; no se convierten automáticamente en cero. Los fallos cartográficos se manejan por separado para conservar las tablas y gráficas ya producidas.

### 6.4. Paquetes y entorno registrado

El script requiere `readxl`, `dplyr`, `tidyr`, `ggplot2`, `scales`, `stringr`, `ggrepel` y `ragg`. Los mapas requieren además `sf`; `grid`, `grDevices`, `utils`, `stats` y otras funciones utilizadas forman parte de R o de sus paquetes base.

El archivo `Sesion_R.txt` registra una ejecución con R 4.3.3 en Ubuntu 24.04.3 LTS. Entre las versiones cargadas están `ggplot2 3.4.4`, `dplyr 1.1.4`, `tidyr 1.3.1`, `readxl 1.4.3`, `stringr 1.5.1`, `scales 1.3.0`, `ggrepel 0.9.5`, `ragg 1.2.7` y `sf 1.0-15`. Son las versiones de la sesión registrada, no requisitos mínimos declarados ni un entorno bloqueado mediante `renv`.

El script intenta instalar paquetes desde `https://cloud.r-project.org` cuando faltan. En una computadora nueva se necesita acceso a ese repositorio o paquetes ya instalados. Las dependencias de sistema de `sf` dependen del sistema operativo y de la disponibilidad de binarios. La carpeta de traslado no incluye una instalación completa de R ni las bibliotecas de paquetes del entorno de ejecución anterior.

## 7. Especificaciones gráficas aceptadas

### 7.1. Matriz completa del IEE

El mapa de calor muestra las 32 entidades por las 21 actividades, con 672 celdas. Las entidades siguen el orden del registro estatal y las actividades mantienen el orden económico del Excel. Se usan bordes blancos entre las celdas, rótulos sectoriales abreviados e inclinados y nombres estatales legibles.

La versión final no imprime los valores dentro de las celdas. El usuario prefirió una visión completa del país a una selección de ejemplos o una matriz saturada de números. Los valores exactos se consultan en los CSV.

### 7.2. Paleta continua común del IEE

El mapa de calor y los cuatro mapas sectoriales utilizan la misma función `escala_iee()`. La transformación del color es `log1p`, es decir, $\log(1+IEE)$; admite el cero y permite representar los valores grandes de la minería petrolera junto con los cocientes menores.

La transformación se aplica a la escala de color. Los IEE almacenados, los rankings, las etiquetas y las tablas conservan el valor original. Los números de la barra inferior también están expresados en el índice original.

| Valor de anclaje del IEE | Color hexadecimal | Función en la escala |
| --- | --- | --- |
| 0 | `#244A73` | Azul profundo: extremo inferior y actividad nula |
| 0.5 | `#7DA5BD` | Azul intermedio |
| 1 | `#F4F0EA` | Tono claro asociado con la referencia nacional |
| 2 | `#DDB1A8` | Transición al rojo |
| 4 | `#C4787C` | Rojo medio |
| 8 | `#A44759` | Rojo más intenso |
| Límite superior | `#681D32` | Rojo vino oscuro |

El límite se define como `max(24, ceiling(max(datos$IEE)))`; con esta matriz es 24. Los puntos de color se colocan según su posición transformada, de manera que la referencia de uno se mantiene en el tono claro. La barra presenta marcas en 0, 0.5, 1, 2, 4, 8, 16 y 24.

La barra es horizontal y se coloca debajo de cada figura. Se genera con `guide_colorbar`, ancho de 14 cm, alto de 0.45 cm y 512 divisiones de representación del degradado. No debe sustituirse por una leyenda de cajas o clases discretas. Tampoco debe recuperarse la paleta violeta-verde con ceros grises de una versión intermedia.

Como la escala común abarca los valores petroleros, algunas diferencias de los otros sectores se representan con tonos cercanos. Esa escala se mantuvo para conservar comparabilidad entre mapas. Si se desea cambiarla, hará falta una instrucción nueva del usuario y una explicación coherente en el texto y los pies de figura.

### 7.3. Mapa del KSI

El KSI se representa con un degradado continuo de azul a rojo oscuro, con límites fijos de cero a dos y barra inferior. Su paleta es `#244A73`, `#6C94B0`, `#B7CBD7`, `#F4F0EA`, `#DAB6AF`, `#B65E6B`, `#681D32`, con posiciones uniformes en esa escala.

El tono central de este mapa no tiene el significado económico de la unidad del IEE. La unidad del cociente de localización es una referencia de proporcionalidad; el KSI es una distancia. Las explicaciones de color deben conservar esa diferencia.

### 7.4. Mapas separados y cinco etiquetas

Se conservan cinco archivos cartográficos independientes: el KSI estatal y los IEE de minería petrolera, manufacturas, servicios financieros y alojamiento y alimentos. No se combinan los mapas sectoriales en un panel único.

El parámetro general es `n_destacados <- 5L`. Las etiquetas se seleccionan con `slice_max(..., n = n_destacados, with_ties = FALSE)`, por lo que se toman exactamente cinco registros. No hay un filtro previo de `IEE > 1`.

Esto explica que el quinto IEE petrolero, Chiapas, sea menor que uno y que tres de los cinco mayores cocientes financieros también sean inferiores a uno. Los rótulos describen “los cinco mayores índices”; no sería correcto afirmar que todos los estados etiquetados presentan especialización superior a la referencia nacional.

Las etiquetas incluyen la abreviatura de la entidad y el valor del índice, con tres decimales en el KSI y dos en el IEE. `ggrepel` utiliza semilla 2024 y `max.overlaps = Inf` para conservar los rótulos. Los puntos de referencia se obtienen con `st_point_on_surface`, lo que evita asignar un punto fuera del polígono. La ubicación final puede variar con tipografías y versiones de las bibliotecas; debe revisarse al cambiar el entorno.

### 7.5. Cartografía y límites

Los mapas contienen únicamente límites estatales y un contorno nacional. Se retiraron las capas físicas y otros elementos del script original: ríos, orografía y referencias ajenas al tema del apartado.

El script obtiene cartografía del servicio `https://gaia.inegi.org.mx/wscatgeo/v2/geo/mgee/` cuando no encuentra una copia local. Su caché por defecto es `Cartografia_INEGI/entidades_INEGI.geojson` junto al Excel. En el paquete de traslado ya se incluye la cartografía utilizada, así que el lanzador local puede trabajar con ella sin volver a descargarla.

El GeoJSON conservado tiene 32 entidades. Sus metadatos indican “INEGI. Marco Geoestadístico, diciembre de 2025”; también contiene atributos del Censo 2020 que no se utilizan como ponderaciones en los índices. Los pesos económicos proceden exclusivamente del Excel de 2024.

El código acepta campos `cve_ent` o `cvegeo`, normaliza las claves y comprueba que cubran las 32 entidades. El flujo valida y transforma las geometrías a una proyección cónica conforme de Lambert para México:

```text
+proj=lcc +lat_1=17.5 +lat_2=29.5 +lat_0=12 +lon_0=-102 +datum=WGS84 +units=m +no_defs
```

Se eliminan dimensiones Z/M y se agrupa por entidad. La simplificación visual usa una tolerancia de 300 metros, con conservación de topología; no cambia las cifras económicas ni las claves estatales. Los mapas no muestran ejes geográficos.

Si ocurre un error cartográfico, el bloque correspondiente emite un aviso y escribe `Aviso_cartografia.txt`. La presencia de CSV o de un mensaje final no prueba por sí misma que se hayan generado los cinco mapas: hay que revisar los archivos cartográficos y el aviso. Un aviso de una ejecución anterior puede permanecer en la carpeta, porque el script no lo elimina automáticamente después de una ejecución exitosa.

### 7.6. Formato de salida y correspondencia con el capítulo

Se guardan once figuras en PNG de 320 ppp y once PDF vectoriales, con fondo blanco. Para PNG se utiliza `ragg::agg_png`; para PDF, Cairo cuando está disponible y el dispositivo PDF de R en caso contrario. En Windows las figuras usan Arial y en otros sistemas se solicita `sans`.

| Nombre base del archivo | Figura en el capítulo | Contenido | Ancho × alto, pulgadas |
| --- | --- | --- | --- |
| 01_KSI_entidades | II.2.1 | Barras del KSI de las 32 entidades | 10 × 10.7 |
| 02_Diferencias_sectoriales_KSI | II.2.2 | Cuatro brechas de mayor magnitud en cada una de cuatro entidades | 11 × 7.8 |
| 03_ICE_sectores | II.2.3 | Barras del ICE de las 21 actividades | 10 × 9.5 |
| 04_Distribucion_territorial_ICE | Complementaria | Participación sectorial y peso estatal: minería petrolera y corporativos | 13 × 6 |
| 05_Matriz_IEE_completa | II.2.4 | Mapa de calor: las 672 combinaciones, sin cifras interiores | 8.8 × 11.2 |
| 07_Sensibilidad_agregacion | Complementaria | Ocho entidades con mayor cambio del KSI por agregación minera | 11 × 6.5 |
| 08_Mapa_KSI | Complementaria | Mapa estatal del KSI y sus cinco valores mayores | 12 × 8.6 |
| 09_IEE_mineria_petrolera | II.2.5 | Mapa del IEE petrolero: cinco valores mayores | 12 × 8.6 |
| 10_IEE_manufacturas | II.2.6 | Mapa del IEE manufacturero: cinco valores mayores | 12 × 8.6 |
| 11_IEE_servicios_financieros | II.2.7 | Mapa del IEE financiero: cinco valores mayores | 12 × 8.6 |
| 12_IEE_alojamiento_alimentos | II.2.8 | Mapa del IEE de alojamiento y alimentos: cinco valores mayores | 12 × 8.6 |

El salto del número 05 al 07 en los nombres de archivo es un residuo de la revisión de figuras. No falta una figura necesaria con el número 06. La numeración editorial del capítulo, II.2.1 a II.2.8, es independiente de esos nombres.

El gráfico 02 muestra los cuatro mayores aportes absolutos al KSI de Campeche, Coahuila, Ciudad de México y Jalisco, conservando el signo de la brecha. El KSI sigue sumando las 21 actividades. El gráfico 04 compara los cinco mayores aportantes territoriales y el resto de entidades en minería petrolera y corporativos; su ordenación por participación sectorial es distinta del ranking de IEE usado para las etiquetas de los mapas.

Las gráficas de barras y comparaciones complementarias conservan sus colores propios del script. La exigencia del degradado continuo azul-rojo se aplicó a los mapas y al mapa de calor, que fueron los objetos expresamente señalados por el usuario.

## 8. Resultados numéricos y archivos de consulta

Esta sección conserva resultados para comprobar una ejecución y localizar los ejemplos del texto. No convierte el apartado del manual en un informe dominado por rankings. Los CSV contienen más precisión que las cifras redondeadas de las figuras.

### 8.1. Cinco mayores KSI: etiquetas del mapa estatal

| Lugar | Entidad | KSI |
| --- | --- | --- |
| 1 | Campeche | 1.352436583 |
| 2 | Tabasco | 0.919431584 |
| 3 | Quintana Roo | 0.661785855 |
| 4 | Ciudad de México | 0.610662761 |
| 5 | Nayarit | 0.598206921 |

Las cinco entidades con menor KSI, de mayor a menor dentro de ese grupo, son Veracruz, Puebla, Hidalgo, Jalisco y Morelos. Sus valores aproximados son 0.261923, 0.248455, 0.248127, 0.227524 y 0.213899. Estos resultados describen semejanza a la composición nacional bajo la clasificación utilizada.

### 8.2. Cinco mayores IEE por mapa sectorial

### Minería petrolera (21-1)

| Lugar | Entidad | IEE |
| --- | --- | --- |
| 1 | Campeche | 22.745029491 |
| 2 | Tabasco | 17.754462246 |
| 3 | Veracruz | 1.672240642 |
| 4 | Tamaulipas | 1.064965687 |
| 5 | Chiapas | 0.819382854 |

### Manufacturas (31-33)

| Lugar | Entidad | IEE |
| --- | --- | --- |
| 1 | Coahuila | 2.156485985 |
| 2 | San Luis Potosí | 1.837033295 |
| 3 | Baja California | 1.741342821 |
| 4 | Aguascalientes | 1.687160957 |
| 5 | Chihuahua | 1.594968672 |

### Servicios financieros y seguros (52)

| Lugar | Entidad | IEE |
| --- | --- | --- |
| 1 | Ciudad de México | 2.624351581 |
| 2 | Nuevo León | 1.208097699 |
| 3 | Sinaloa | 0.956762995 |
| 4 | Quintana Roo | 0.928065038 |
| 5 | Baja California Sur | 0.887529845 |

### Alojamiento y alimentos (72)

| Lugar | Entidad | IEE |
| --- | --- | --- |
| 1 | Baja California Sur | 6.304235590 |
| 2 | Quintana Roo | 6.100074116 |
| 3 | Nayarit | 4.688036659 |
| 4 | Yucatán | 2.056911801 |
| 5 | Guerrero | 1.743723208 |

### 8.3. ICE de las 21 actividades

| Código | Actividad | ICE |
| --- | --- | --- |
| 21-1 | 21-1 Minería petrolera | 1.726543579 |
| 55 | 55 Corporativos | 1.466717467 |
| 21-2 | 21-2 Minería no petrolera | 1.084421109 |
| 51 | 51 Información en medios masivos | 0.898292605 |
| 11 | 11 Agricultura, ganadería, pesca y actividades forestales | 0.721292108 |
| 71 | 71 Esparcimiento, cultura y deporte | 0.697864163 |
| 56 | 56 Apoyo a negocios, residuos y remediación | 0.605108990 |
| 54 | 54 Servicios profesionales, científicos y técnicos | 0.564405236 |
| 52 | 52 Servicios financieros y seguros | 0.529274317 |
| 31-33 | 31-33 Manufacturas | 0.514466944 |
| 72 | 72 Alojamiento y preparación de alimentos | 0.424747826 |
| 22 | 22 Electricidad, agua y gas | 0.412221147 |
| 23 | 23 Construcción | 0.331996731 |
| 93 | 93 Actividades gubernamentales y legislativas | 0.312250287 |
| 61 | 61 Servicios educativos | 0.264525013 |
| 46 | 46 Comercio al por menor | 0.263071571 |
| 48-49 | 48-49 Transportes, correos y almacenamiento | 0.262455625 |
| 53 | 53 Servicios inmobiliarios y alquiler | 0.223961958 |
| 81 | 81 Otros servicios | 0.196145114 |
| 62 | 62 Salud y asistencia social | 0.195010159 |
| 43 | 43 Comercio al por mayor | 0.174269472 |

### 8.4. Ejemplos usados en el manuscrito

En Campeche, minería petrolera equivale aproximadamente a 61.16 % del VAB estatal frente a 2.69 % en el país. La brecha aporta alrededor de 0.585 al KSI estatal de 1.352; el resto de actividades también integra el índice. El IEE petrolero es aproximadamente 22.745.

En Coahuila, las manufacturas representan aproximadamente 46.74 % del VAB estatal y 21.67 % del VAB del país. El cociente se obtiene con cifras completas: $0.4673996001/0.2167413113\approx2.156485985$. La diferencia entre participaciones aporta aproximadamente 0.251 al KSI. El manuscrito presenta la razón como unas 2.16 veces el peso nacional.

Campeche y Tabasco reúnen aproximadamente 87.57 % del VAB petrolero y 4.39 % del VAB total del país. El ICE petrolero es aproximadamente 1.726544. El comercio al por mayor tiene un ICE cercano a 0.174269, que sirve como contraste de distribución territorial más próxima al peso económico de las entidades.

El sector 72 incluye alojamiento temporal y preparación de alimentos y bebidas. El manuscrito lo relaciona con actividades turísticas y consumo local, conservando esa cobertura sectorial; no lo identifica con el conjunto completo del turismo.

### 8.5. Sensibilidad de la agregación minera

| Entidad | KSI: 21 actividades | KSI: 20 sectores | Diferencia |
| --- | --- | --- | --- |
| Durango | 0.340819485 | 0.287038405 | 0.053781080 |
| Zacatecas | 0.496361235 | 0.442580155 | 0.053781080 |
| Sonora | 0.420108601 | 0.366327521 | 0.053781080 |
| Baja California Sur | 0.515334363 | 0.476977320 | 0.038357043 |
| San Luis Potosí | 0.427706463 | 0.398077856 | 0.029628607 |
| Colima | 0.497319327 | 0.469813085 | 0.027506242 |
| Guerrero | 0.588610449 | 0.569297071 | 0.019313378 |
| Campeche | 1.352436583 | 1.334755378 | 0.017681205 |

### 8.6. CSV de la entrega

| Archivo | Filas de datos | Contenido |
| --- | --- | --- |
| `KSI_entidades.csv` | 32 | Claves y nombres estatales, VAB, peso nacional y KSI; ordenado de mayor a menor KSI |
| `ICE_sectores.csv` | 21 | Código, rótulos, grupo, ICE y participación nacional; ordenado de mayor a menor ICE |
| `Indices_entidad_sector.csv` | 672 | Base larga con VAB por celda, participaciones, IEE, brechas y aportaciones; incluye variables estatales y sectoriales |
| `Matriz_IEE.csv` | 32 | Nombre de la entidad y 21 columnas de IEE |
| `Catalogo_sectores.csv` | 21 | Código, etiqueta abreviada y encabezado completo del Excel |
| `Sensibilidad_agregacion_minera.csv` | 32 | KSI con 21 actividades, KSI con minería agregada y diferencia |

Las columnas de `Indices_entidad_sector.csv` tienen los siguientes significados:

| Columna | Definición |
| --- | --- |
| `cve_ent` | Clave de entidad de dos dígitos |
| `codigo` | Código de la actividad de esta matriz |
| `VAB_sector` | $x_{ij}$, VAB de la celda |
| `participacion_local` | $s_{ij}$, peso sectorial dentro de la entidad |
| `participacion_sector` | $q_{ij}$, peso estatal dentro del sector nacional |
| `IEE` | Cociente de localización |
| `diferencia_pp` | $100(s_{ij}-s_j)$, brecha en puntos porcentuales |
| `aportacion_KSI` | $|s_{ij}-s_j|$ |
| `aportacion_ICE` | $|q_{ij}-w_i|$ |
| `nombre` | Nombre estatal completo del registro |
| `nombre_corto` | Forma abreviada para presentación |
| `abreviatura` | Rótulo estatal utilizado en los mapas |
| `VAB` | $x_{i\cdot}$, total estatal |
| `peso` | $w_i$, peso estatal en el total nacional |
| `KSI` | KSI de la entidad, repetido en sus 21 actividades |
| `etiqueta` | Nombre abreviado de la actividad |
| `grupo` | Primarias, Secundarias o Terciarias |
| `nombre_excel` | Encabezado completo de la actividad en el Excel |
| `ICE` | ICE de la actividad, repetido en sus 32 entidades |
| `participacion_nacional` | $s_j$, peso nacional de la actividad |

Los CSV usan UTF-8, punto decimal y coma como separador. En instalaciones de Excel que esperan punto y coma conviene importarlos mediante la opción de datos de texto/CSV. `Matriz_IEE.csv` contiene índices y no debe usarse como si fuera la matriz de VAB original.

## 9. Criterios de redacción que deben conservarse

El usuario revisó varias veces el estilo y pidió que sonara como un capítulo de un manual escrito por una persona con dominio del tema. La prioridad editorial es explicar la teoría con continuidad y precisión. Los ejemplos de México acompañan la argumentación, sin desplazarla por una sucesión de cifras o clasificaciones.

### 9.1. Instrucciones expresas

- Evitar guiones largos y el uso excesivo de dos puntos.
- Evitar construcciones como “no es x, sino y” y “no solamente x, sino también y”.
- No planear los párrafos o las enumeraciones del capítulo con una plantilla repetida de tres elementos.
- Evitar que todos los párrafos comiencen con una oración breve de anuncio, seguida de una explicación larga.
- Dar variedad a la extensión y a la sintaxis de los párrafos, manteniendo la relación entre las ideas.
- Retirar frases vacías, transiciones que anuncian una precaución y advertencias sobre interpretaciones hipotéticas que interrumpen el argumento.
- Mantener la formalidad académica y explicar las ecuaciones, las variables y la lectura económica de los resultados.

Estas preferencias se refieren especialmente a la prosa del capítulo. La documentación técnica de este MD utiliza tablas y listados cuando facilitan consultar rutas, archivos o verificaciones.

### 9.2. Frases señaladas por el usuario

El usuario pidió quitar o modificar expresiones como:

> “La referencia nacional exige otra precaución.”

> “Su interpretación como diversificación absoluta requeriría información adicional sobre la distribución de la producción dentro de la propia entidad.”

El problema editorial señalado fue la aparición de una advertencia abstracta o de una interpretación hipotética que se podía expresar directamente. En la versión vigente, el significado relativo del KSI se explica al desarrollar lo que compara, las aportaciones sectoriales y el signo de las brechas. Se mantiene la precisión conceptual sin volver a insertar una cadena de reservas al final de cada párrafo.

La revisión de estilo no debe borrar distinciones sustantivas: el denominador VAB, la referencia nacional del KSI, la proporcionalidad económica del ICE y el significado de la unidad en el IEE forman parte de la explicación. La intervención editorial consiste en expresarlas con naturalidad y en el lugar adecuado del argumento.

La solicitud de eliminar rasgos que el usuario asocia con IA se tradujo en una revisión de sintaxis, cadencia, contenido y repetición. No se aplicó un detector que permita atribuir autoría ni se puede garantizar la clasificación que un sistema externo asigne al texto. La referencia para continuar es el estilo concreto aprobado por el usuario.

### 9.3. Orden del manuscrito vigente

El archivo fuente tiene el título “2. Medición de la especialización” y desarrolla los apartados: “La matriz de actividad económica”, “El índice de especialización de Krugman”, “La concentración espacial de las actividades”, “El Índice de Especialización Económica”, “Relación entre los índices”, “Alcances de la medición” y “Referencias”.

La exposición parte de las participaciones y sus denominadores, presenta las fórmulas y sus propiedades, introduce ejemplos mexicanos y termina vinculando la distribución de la producción con el análisis de cadenas de valor del inciso siguiente. Ésa es la continuidad con el manual original.

## 10. Documento Word y fuentes editables

El documento final es `output/Medicion_de_la_Especializacion.docx`. El cuerpo del texto tiene **2466 palabras** según el contador utilizado para producirlo: cuenta el texto anterior a referencias, incluidos encabezados, y excluye las marcas de ecuaciones y figuras. Por eso las entregas anteriores lo describieron como “aproximadamente 2,500 palabras”. No se trata del conteo completo del Word con referencias y pies.

El archivo tiene ocho figuras integradas y diez bloques de ecuaciones nativas de Word. El XML contiene veinte objetos matemáticos en total, contando los que aparecen dentro del texto. Las ecuaciones se escribieron en OMML, de modo que son editables en Word y no imágenes pegadas.

La maquetación efectivamente utilizada en esta entrega es la siguiente:

| Elemento | Configuración actual |
| --- | --- |
| Página | Carta, 8.5 × 11 pulgadas |
| Fuente del cuerpo | Calibri, 11.5 puntos |
| Interlineado del cuerpo | 1.15 |
| Espacio posterior del cuerpo | 7 puntos |
| Alineación del cuerpo | Justificada |
| Márgenes superior e inferior | 0.8 pulgadas |
| Márgenes izquierdo y derecho | 0.85 pulgadas |
| Ancho de las figuras | 6.8 pulgadas |
| Pies de figura | 10 puntos, sin cursivas |
| Referencias | 11 puntos, alineación izquierda y sangría francesa |
| Color del texto | Negro |
| Paginación | Campo de número de página en el pie |

Estas son las propiedades leídas del documento y del generador vigentes. No deben sustituirse por Arial 12 o interlineado 1.5 a partir de preferencias de otros proyectos del usuario. En este chat no se solicitó ese cambio; sólo se aplicaría si lo pide para una nueva versión.

La última representación PDF conservada para revisión tiene catorce páginas de tamaño carta. La paginación puede cambiar por disponibilidad de fuentes o por el motor de Word; la cifra es una referencia del render revisado, no una restricción editorial adicional.

La fuente del manuscrito es `texto/seccion_revisada.md`. Utiliza marcas `[[EQ:...]]` para las ecuaciones y `[[FIG:archivo|pie]]` para insertar las figuras. Los grupos de ecuaciones son `totales`, `ksi`, `ice`, `iee`, `ejemplo` y `relaciones`; el archivo contiene seis marcas de ecuación que se expanden a diez bloques. El generador inserta las ecuaciones y las imágenes y guarda el DOCX.

El apéndice A conserva la fuente del manuscrito. El apéndice C conserva el generador con dos adaptaciones de rutas para la carpeta local. El generador original se guarda además en `referencias/build_doc_original.py` como registro de la implementación anterior.

La generación de Word utiliza Python, `python-docx` y `lxml`. La revisión visual previa se realizó con una representación a PDF y páginas PNG, y se corrigieron la legibilidad, los tamaños de figura y la paginación. Esos renders son archivos de revisión; no se necesitan todos los temporales del entorno anterior para continuar el proyecto.

## 11. Referencias bibliográficas y función en el apartado

La bibliografía vigente reúne siete referencias. Sus datos completos y enlaces están preservados al final del manuscrito del apéndice A. Los enlaces se conservan de esa versión; este documento de contexto no añade una nueva revisión bibliográfica en internet.

| Referencia | Función en el texto |
| --- | --- |
| Krugman (1991), *Geography and Trade* | Referencia del análisis comparativo de estructuras productivas y la especialización |
| Krugman (2010), *The New Economic Geography, Now Middle-Aged* | Contexto de la nueva geografía económica en la exposición existente |
| Hoover (1936), *The measurement of industrial localization* | Antecedente de medición de localización industrial |
| Hildebrand y Mace (1950), *The employment multiplier in an expanding industrial market: Los Angeles County, 1940-47* | Antecedente del uso del cociente de localización en análisis regional |
| Lira y Quiroga (2009), *Técnicas de análisis regional*, Manuales 59, CEPAL e ILPES | Sistematización de técnicas e indicadores regionales |
| U.S. Bureau of Labor Statistics (2011), *Using Location Quotients to Analyze Occupational Data* | Apoyo para la interpretación del cociente de localización |
| INEGI, PIBE, año base 2018, datos de 2024, consulta 2026 | Fuente estadística de la aplicación mexicana |

El IEE no se presenta como un índice originalmente desarrollado por Krugman. El ICE utiliza aquí una distancia absoluta aplicada a las participaciones territoriales, con antecedentes de análisis regional; las referencias y las normalizaciones se deben mantener diferenciadas al redactar.

## 12. Carpeta local de traslado y archivos que deben conservarse

El archivo `PAPIME_Mx_Continuidad_Local.zip` se extrae en una carpeta llamada `PAPIME_Mx`. Los siguientes caminos son relativos a esa raíz. Su estructura no depende del directorio temporal de este chat.

| Ruta relativa | Contenido y condición |
| --- | --- |
| `CONTEXTO_PAPIME_Mx_Especializacion.md` | Este documento de contexto |
| `datos/PIBE_2024_In.xlsx` | Excel original recibido, renombrado sin cambiar sus bytes |
| `datos/Matriz_original_Indices_Krugman.csv` | Copia textual de `A1:W34`, con encabezados, 32 entidades y total nacional |
| `referencias/PAPIME_Libro.pdf` | PDF original del manual, sin modificaciones |
| `referencias/Plots_Krugman_2024_original.R` | Script anterior a las modificaciones del chat |
| `referencias/build_doc_original.py` | Generador de Word anterior al traslado; contiene rutas del entorno anterior |
| `scripts/Plots_Krugman_2024.R` | Script final vigente, conserva la ruta Windows solicitada |
| `scripts/ejecutar_proyecto_local.R` | Lanzador añadido para usar la carpeta nueva sin modificar el script final |
| `scripts/build_doc.py` | Generador de Word con rutas relativas a la raíz del proyecto |
| `texto/seccion_revisada.md` | Manuscrito editable vigente con marcas de ecuaciones y figuras |
| `Cartografia_INEGI/entidades_INEGI.geojson` | Límites estatales utilizados en las ejecuciones y mapas |
| `output/Medicion_de_la_Especializacion.docx` | Documento final aceptado antes del traslado |
| `output/LEEME.txt` | Instrucciones de la entrega previa; menciona la ruta Windows original |
| `output/Figuras_Capitulo_II_Especializacion_2024/` | Once PNG, once PDF, seis CSV, guía y registro de sesión |
| `MANIFIESTO_SHA256.csv` | Tamaño y SHA-256 de los demás archivos del paquete |

El ZIP de la entrega anterior, `Material_Medicion_Especializacion_2024.zip`, reunía el DOCX, el R, el LEEME, las figuras y las tablas. No contenía el Excel, el PDF original del manual, la cartografía ni el generador. El paquete de traslado agrega esos insumos. No es necesario anidar el ZIP anterior dentro del nuevo, porque sus contenidos útiles ya se incluyen descomprimidos.

Las copias históricas, los scripts de parches de cada iteración, los paquetes de instalación y las imágenes intermedias de revisión se mantienen fuera del paquete. Su función ya quedó registrada en este MD; no son dependencias del trabajo final. El código y el manuscrito vigentes son los archivos que se deben editar para continuar.

### 12.1. Adaptaciones nuevas, realizadas sólo para el traslado

El script final `Plots_Krugman_2024.R`, el Excel y el DOCX aceptado se copiaron sin modificaciones. Se añadieron estos archivos auxiliares:

| Archivo | Adaptación |
| --- | --- |
| `scripts/ejecutar_proyecto_local.R` | Lee el script final y reemplaza en memoria cuatro asignaciones de rutas: Excel, salida, carpeta geográfica y archivo cartográfico. No cambia índices, paletas, etiquetas ni resultados |
| `scripts/build_doc.py` | Deriva la raíz a partir de la ubicación del archivo y lee `texto/seccion_revisada.md` con UTF-8. Conserva la lógica de ecuaciones, figuras y formato del generador original |
| `datos/Matriz_original_Indices_Krugman.csv` | Exportación de valores de la tabla original; no contiene las fórmulas ni todas las hojas del Excel |

Estas adaptaciones no constituyen otra revisión sustantiva del capítulo. La validación de esta entrega de contexto contrastó los datos de manera independiente, comprobó las rutas esperadas, compiló la sintaxis Python del generador y verificó la integridad del paquete. No se volvió a ejecutar el script R completo ni a renderizar el Word durante la preparación de este MD; la ejecución y la revisión visual completas corresponden a la entrega anterior.

### 12.2. Huellas de los archivos de referencia

Las huellas siguientes identifican los insumos y salidas preservados. Cambiar de nombre a un archivo no cambia su SHA-256. Si se edita, su huella dejará de coincidir y el manifiesto deberá actualizarse.

| Archivo de referencia en la carpeta nueva | SHA-256 |
| --- | --- |
| referencias/PAPIME_Libro.pdf | `f05cce5e149265063d81bc3b1d6e0b4c04d2ffeb538c8d20e10f395aa0df7a12` |
| referencias/Plots_Krugman_2024_original.R | `5d0b5cfb139272f6a2e33511d80ce67315fbe1d6fd48f4ecdc7d3c88b8f1c44f` |
| datos/PIBE_2024_In.xlsx | `0ce674346f2861aa580ef33a4edd4da653ef8aadd817fc0928be56033843cf79` |
| Cartografia_INEGI/entidades_INEGI.geojson | `170c3ea5ff472f08ece97970dc90ad4ba8c6f503e33859655f315091c105cc91` |
| scripts/Plots_Krugman_2024.R | `edfcf0d90a376edd0129fe79ff0cf2f1419427cc1c773a175c5e6a938eb821cd` |
| output/Medicion_de_la_Especializacion.docx | `6f9bdccab40b4258fb494f5630fa042f38d7f8292a9bc0e843033f1800a9499e` |
| output/LEEME.txt | `eb0e9fa23fc109e6716db57b5593ad2ba4482ffa318455cf84309bdeca80bdc8` |
| texto/seccion_revisada.md | `e054c74337077d0847bcbe452033d8a6864872255aedf7a0dfdb473eb4d8e715` |
| referencias/build_doc_original.py | `a5f8b8b9c4d29c8bdec47ec9ba1a4010259fc7f9c93030256306eea42702bdf4` |

La huella del generador portátil será distinta de la del generador original por las dos adaptaciones de rutas. Este MD y el ZIP de traslado no se identifican mediante una huella incluida dentro de sí mismos; el manifiesto del paquete incluye el MD y excluye su propio archivo.

## 13. Cómo ejecutar el proyecto en la computadora

### 13.1. Opción recomendada: trabajar desde la carpeta nueva

Extraer el ZIP, abrir `PAPIME_Mx` como carpeta del proyecto y conservar los nombres relativos de sus subcarpetas. El archivo `datos/PIBE_2024_In.xlsx` y el GeoJSON ya están incluidos.

En RStudio se puede fijar el directorio de trabajo a la raíz `PAPIME_Mx` y ejecutar:

```r
source("scripts/ejecutar_proyecto_local.R", encoding = "UTF-8")
```

Desde una terminal ubicada en esa misma raíz:

```bash
Rscript scripts/ejecutar_proyecto_local.R
```

El lanzador ajusta las rutas dentro del código que evalúa y produce los resultados en `output/Figuras_Capitulo_II_Especializacion_2024`. La cartografía local evita la descarga; siguen siendo necesarios R y los paquetes del script. Los mensajes de generación y el número de archivos permiten revisar que el flujo llegó a los cinco mapas.

La carpeta raíz se toma del directorio de trabajo, no de la ubicación desde la que el editor abrió un archivo aislado. Si RStudio tiene abierto otro directorio, se debe cambiar a `PAPIME_Mx` antes de ejecutar el lanzador.

### 13.2. Opción alternativa: conservar la ubicación Windows original

Si el Excel está en `C:/Users/marce/Downloads/PIBE/PIBE_2024_In.xlsx`, se puede ejecutar directamente el script final desde R o RStudio. Los resultados se guardarán junto al Excel en la carpeta solicitada originalmente. La variable `ruta_cartografia` admite una ruta explícita a un archivo geográfico local.

Para cambiar de carpeta sin usar el lanzador basta con editar las asignaciones iniciales de rutas en una copia de trabajo del script. El resto del código no necesita modificarse por ese traslado. En Windows conviene usar `/` en las rutas de R o escapar correctamente las barras invertidas.

### 13.3. Regenerar el Word

El Word no se actualiza por el hecho de volver a ejecutar R. El flujo completo es: producir las figuras, editar el manuscrito cuando corresponda y ejecutar el generador de documento. El generador utiliza los archivos PNG ubicados en la carpeta de resultados y las marcas de figura de `texto/seccion_revisada.md`.

Con Python disponible y desde la raíz del proyecto:

```bash
python -m pip install python-docx lxml
python scripts/build_doc.py
```

En Windows se puede utilizar `py` en lugar de `python` si ése es el lanzador configurado. El proceso guarda `output/Medicion_de_la_Especializacion.docx`. No genera automáticamente un PDF ni reproduce por sí mismo las capturas de revisión del entorno anterior.

Si cambian cifras, sectores, pies o fórmulas, deben mantenerse coordinados el manuscrito, las ecuaciones definidas en `equation()`, los CSV y las figuras. El ejemplo numérico de Coahuila de `equation('ejemplo')` está escrito de forma explícita en el generador; actualizar el Excel no cambia esos números dentro del Word de manera automática.

Los límites de 21 actividades y 32 entidades también aparecen en las ecuaciones y en los controles del código. Cambiar la cobertura exige revisar conjuntamente esos elementos; no basta con sustituir un archivo con otra dimensión.

### 13.4. Si sólo se conserva este MD

Los apéndices están delimitados por comentarios `PAPIME:BEGIN` y `PAPIME:END`. Dentro de cada bloque se conserva el contenido del archivo indicado. Se pueden copiar manualmente a sus rutas o extraer con el ejemplo del apéndice F.

El MD conserva los valores de la matriz económica y el código. No incorpora los bytes del PDF original del manual, la cartografía, las figuras ni el DOCX final. Para conservar esos archivos y trabajar sin volver a descargarlos se debe usar el ZIP de traslado. El CSV de origen permite recuperar los cálculos aun si se pierde el Excel, pero una reconstrucción no recupera sus fórmulas, sus formatos ni la otra hoja.

### 13.5. Situaciones que conviene reconocer al continuar

| Situación | Acción concreta |
| --- | --- |
| `No se encontró el Excel` | Revisar `ruta_excel`, el nombre del archivo y el directorio de trabajo del lanzador |
| Error de hoja o códigos | Conservar `Indices_Krugman` y comprobar `A1:W34`, los encabezados y el orden de actividades |
| Se recalculó desde la matriz, pero no coinciden o faltan los índices guardados | Revisar la ubicación de `W78:W109` y `B147:V147`; el mensaje de ese bloque es informativo y no cambia la fuente de cálculo |
| Faltan mapas | Revisar `Aviso_cartografia.txt`, `sf`, la ruta del GeoJSON y la cobertura de 32 entidades |
| Error en nombres estatales | Comparar con el registro del script; conservar las claves de dos dígitos |
| CSV con caracteres extraños | Importar con UTF-8 y separador coma |
| Matriz de calor incompleta o sólo una selección | Usar `05_Matriz_IEE_completa`; no recuperar una figura de ejemplos de una versión anterior |
| Las leyendas muestran cajas o colores verde-violeta | Se está utilizando una versión intermedia del código o figuras antiguas |
| Sólo aparecen dos etiquetas | Comprobar `n_destacados <- 5L` y regenerar los PNG y PDF con el script vigente |
| El Word conserva imágenes anteriores | Regenerar el DOCX después de ejecutar R, verificando que el generador apunte a la carpeta correcta |
| Cambia el máximo del IEE con datos nuevos | Revisar el límite y las marcas de `escala_iee()`; las marcas finales actuales llegan a 24 aunque el límite pueda crecer automáticamente |
| Cambia la disposición de etiquetas o páginas | Revisar la tipografía disponible y la representación final de las figuras y del documento |

## 14. Verificaciones realizadas y alcance de la evidencia

En el trabajo previo se ejecutó el script R completo con el Excel recibido y una ruta local de cartografía. Se generaron las figuras y las tablas, se verificaron los cálculos y se revisaron las representaciones del Word después de las modificaciones. Los archivos `Sesion_R.txt` y `Guia_de_figuras_y_calculos.txt` conservan evidencia de esa ejecución.

Para preparar este contexto se volvieron a leer los archivos vigentes y se reprodujeron los cálculos con Python a partir de los valores del Excel. Esa comprobación independiente permite identificar con precisión el estado transferido, sin presentar como nuevas decisiones metodológicas las operaciones del traslado.

| Comprobación de esta entrega de contexto | Resultado |
| --- | --- |
| Dimensión de la matriz | 32 × 21 |
| Celdas con cero | 36 |
| Totales sectoriales: máxima diferencia entre suma estatal y fila nacional | Aproximadamente $9.31\times10^{-10}$ millones de pesos |
| IEE: máxima diferencia con `Matriz_IEE.csv` | Aproximadamente $4.97\times10^{-14}$ |
| KSI: máxima diferencia con valores guardados del Excel | Aproximadamente $4.44\times10^{-16}$ |
| ICE: máxima diferencia con valores guardados del Excel | Aproximadamente $4.44\times10^{-16}$ |
| Identidad de promedios ponderados | Ambos lados: 0.4218519204286904 |
| Figuras finales | Once PNG y once PDF |
| Figuras integradas en el Word | Ocho |
| Bloques de ecuaciones nativas | Diez |
| Integridad de las copias | Comparación de SHA-256 y manifiesto del paquete |

Las diferencias numéricas anteriores son de precisión de punto flotante. No corresponden a cambios de la base de datos. El traslado no descargó una versión nueva de los datos del PIBE, no estimó otro modelo y no cambió la cobertura económica ni geográfica utilizada.

## 15. Instrucciones de continuidad para el siguiente asistente

El siguiente trabajo debe comenzar leyendo este documento y los archivos actuales, especialmente `texto/seccion_revisada.md` y `scripts/Plots_Krugman_2024.R`. El usuario valoró favorablemente el resultado y pidió ajustes acotados en cada revisión; se debe conservar ese punto de partida.

Al recibir una petición nueva, identificar si afecta la teoría, los datos, la redacción, las figuras o el formato, y actualizar los archivos vinculados con ese cambio. Una modificación de colores implica regenerar las imágenes y el Word si las incorpora; una modificación del ejemplo numérico implica revisar el texto y la ecuación definida en el generador. Una revisión de prosa sin cambios cuantitativos no exige recalcular toda la matriz.

No se debe volver a una matriz seleccionada, a mapas agrupados, a dos etiquetas por mapa o a leyendas discretas. Tampoco corresponde añadir capas físicas al mapa, cambiar silenciosamente la escala de los índices, agregar nuevos años, atribuir al KSI una lectura de diversificación absoluta o presentar como “cinco estados especializados” un ranking que incluye IEE menores que uno.

La revisión final de una nueva entrega debe comprobar la coherencia entre el texto, las fórmulas, las fuentes, las figuras y los pies. Si se genera un DOCX, revisar su representación para detectar ecuaciones rotas, etiquetas superpuestas, figuras ilegibles y espacios o saltos de página inconvenientes. Los valores completos se conservan para el cálculo y se redondean sólo para la exposición.

La carpeta de trabajo puede gestionarse con Git si el usuario lo desea, pero el proyecto trasladado no presupone un repositorio existente. No hay credenciales, conexiones externas ni servicios de publicación necesarios para editar el capítulo y ejecutar el análisis local.

### Texto listo para presentar al nuevo proyecto

> Estamos continuando PAPIME_Mx, un manual universitario de economía mexicana. El trabajo actual es el inciso 2, “Medición de la especialización”, del capítulo II, “Estructura productiva y especialización regional”. Lee `CONTEXTO_PAPIME_Mx_Especializacion.md` y utiliza la última versión de `texto/seccion_revisada.md`, el Word de `output/` y `scripts/Plots_Krugman_2024.R` como base.
>
> La sección está terminada, con unas 2,500 palabras, teoría prioritaria, ecuaciones editables y ocho figuras integradas. KSI e ICE se calculan sin dividir entre dos; el IEE es el cociente de localización. Los datos son VAB estatal de 2024 a precios de 2018, con 32 entidades y 21 actividades; la minería petrolera está separada de la no petrolera. La matriz fuente está en `datos/PIBE_2024_In.xlsx`, hoja `Indices_Krugman`, rango `A1:W34`. El denominador es la suma sectorial del VAB.
>
> Mantén el mapa de calor completo de 672 celdas sin cifras interiores, los mapas en archivos separados, el degradado continuo de azul a rojo oscuro y la barra horizontal inferior. Los mapas del IEE comparten escala con transformación del color `log1p`, sin cambiar los índices. Los cinco mapas identifican las cinco entidades de mayor índice, aunque alguna tenga IEE menor que uno.
>
> En la redacción conserva un tono académico natural: explica directamente los conceptos, usa los ejemplos mexicanos como apoyo y evita aperturas breves obligatorias, advertencias hipotéticas, frases vacías, guiones largos, exceso de dos puntos y estructuras repetidas en grupos de tres. La última versión ya atendió esas observaciones; aplica los cambios nuevos que te pida sin reiniciar el trabajo.
>
> Para ejecutar desde esta carpeta usa `scripts/ejecutar_proyecto_local.R`. El R original entregado conserva mi ruta Windows, y el lanzador ajusta las rutas a la carpeta del proyecto. `scripts/build_doc.py` reconstruye el Word desde el manuscrito y las figuras. Revisa los archivos antes de editar y conserva la coherencia entre texto, código, resultados y figuras.

## 16. Apéndices de recuperación

Los siguientes bloques conservan los contenidos editables completos. Los delimitadores son parte de este MD y no deben copiarse dentro de los archivos recuperados. La fuente del manuscrito y el script R son las versiones vigentes; el generador Python y el lanzador de R incorporan las adaptaciones de traslado descritas en la sección 12.1.

### Apéndice A. Manuscrito vigente: `texto/seccion_revisada.md`

El texto se conserva con las marcas originales del generador. `[[EQ:...]]` inserta una ecuación y `[[FIG:...]]` identifica una imagen y su pie. Las referencias bibliográficas forman parte de este mismo archivo.

<!-- PAPIME:BEGIN MANUSCRITO -->
```markdown
# 2. Medición de la especialización

La estructura productiva de las entidades mexicanas presenta diferencias que se aprecian tanto en el valor de la producción como en su distribución entre actividades. Las cifras absolutas expresan el tamaño de cada economía estatal, mientras que las participaciones sectoriales muestran la importancia de sus actividades dentro del total. Una entidad con una producción manufacturera elevada y otra con una producción mucho menor pueden dedicar la misma proporción de su actividad a las manufacturas. Para estudiar su especialización interesa comparar esas proporciones con las del país y reconocer en qué actividades se apartan del patrón nacional.

El índice de especialización de Krugman (KSI) compara la composición productiva de cada entidad con la nacional y resume las diferencias en un solo valor. Al estudiar la distribución territorial de una actividad se utiliza el Índice de Concentración Espacial (ICE), que toma en cuenta el tamaño económico de las entidades. El Índice de Especialización Económica (IEE), por su parte, identifica el peso relativo de cada actividad dentro de cada estado respecto de su participación en el país. Los cálculos se desarrollan a continuación con datos de México de 2024.

## La matriz de actividad económica

La información se organiza en una matriz cuyas filas corresponden a entidades y cuyas columnas representan actividades, de modo que cada elemento xᵢⱼ es el valor agregado de la actividad j en la entidad i. La suma de una fila proporciona el valor agregado estatal, xᵢ·, y la suma de una columna, el valor agregado nacional de esa actividad, x·ⱼ. Ambas agregaciones conducen al total nacional, x··. En la matriz de México, integrada por 32 entidades y 21 actividades, las sumas se expresan de la siguiente manera.

[[EQ:totales]]

Se utiliza la información del Producto Interno Bruto por Entidad Federativa del INEGI para 2024, expresada en millones de pesos de 2018. La matriz conserva los sectores económicos y separa la minería petrolera de la no petrolera, por lo que reúne 21 actividades. Los códigos 21-1 y 21-2 identifican esta apertura de la minería en la tabla. La suma de las actividades corresponde al valor agregado bruto (VAB), denominado actividad económica total en el archivo, y sirve como denominador de las participaciones sectoriales. El PIB incorpora, además, los impuestos netos de subsidios sobre los productos; dividir entre ese agregado produciría participaciones cuya suma difiere de uno.

Los cálculos utilizan valores no negativos y totales positivos, con la misma cobertura sectorial para todas las entidades. El cero registra la ausencia de actividad en una celda; los datos faltantes se conservan como tales hasta completar o revisar la información. La apertura de la minería sustituye la columna del sector agregado por sus dos componentes, manteniendo el total económico de la matriz. Así, cada actividad se contabiliza una sola vez y las participaciones de cada entidad suman uno.

## El índice de especialización de Krugman

Krugman (1991, 2010) empleó la suma de diferencias absolutas entre participaciones sectoriales para comparar estructuras productivas regionales. En la comparación entre una entidad y el país, sᵢⱼ representa la participación de la actividad j en el VAB estatal y sⱼ su participación en el VAB nacional. Para cada actividad se calcula la diferencia entre ambas proporciones, se obtiene su valor absoluto y se suman los resultados. El KSI recoge de esta forma las distancias sectoriales entre las dos estructuras.

[[EQ:ksi]]

Las diferencias entre las participaciones sectoriales suman cero cuando se conserva su signo, porque las participaciones de cada estructura suman uno. El valor absoluto evita que las diferencias positivas se cancelen con las negativas y recoge la magnitud de cada brecha. Una entidad con las mismas participaciones que el país registra un KSI de cero; las diferencias más grandes elevan el índice. Los resultados para las entidades mexicanas se presentan en la figura II.2.1.

El KSI varía entre cero y dos, y el extremo superior corresponde a estructuras sin actividades compartidas. En la comparación con el país, la producción de cada entidad forma parte del agregado nacional, por lo que ese extremo queda fuera del alcance del índice estatal. Su límite es 2(1 − wᵢ), donde wᵢ representa la participación de la entidad en el VAB del país. Cuanto mayor es ese peso, mayor es también su influencia sobre la estructura nacional. La comparación con el resto del país excluye a la propia entidad y registra una distancia mayor entre las composiciones productivas, salvo cuando estas coinciden.

La suma de las diferencias positivas equivale a la mitad del KSI y expresa la fracción de las participaciones que se reasigna entre actividades para igualar ambas estructuras, manteniendo fija la referencia nacional. Por ejemplo, un KSI de 0.4 equivale a una reasignación de 0.2, es decir, de 20 puntos porcentuales distribuidos entre las actividades. Bajo esta normalización, el índice varía entre cero y uno y conserva el mismo ordenamiento de las entidades. La suma completa y su mitad expresan la misma distancia en escalas distintas.

[[FIG:01_KSI_entidades.png|Figura II.2.1. Especialización relativa de las entidades federativas en 2024.]]

Con el KSI, una entidad se considera más especializada cuanto mayor es la distancia entre su composición productiva y la del país. Las actividades con participaciones semejantes en ambos territorios aportan poco al índice, incluso cuando tienen un peso elevado dentro de las dos economías. Para conocer el perfil de la especialización se examina la aportación de cada actividad y el signo de su diferencia respecto del país, como se hace en la figura II.2.2. Las brechas positivas señalan las actividades con mayor presencia local y las negativas, aquellas con menor participación relativa.

En Campeche, la minería petrolera representa 61.16 % del VAB estatal frente a 2.69 % en el país, por lo que la diferencia aporta aproximadamente 0.585 al KSI de 1.352. El resto del índice procede de las brechas en las demás actividades, incluidas aquellas con participaciones locales inferiores a las nacionales. En Coahuila, las manufacturas concentran 46.74 % del VAB estatal frente a 21.67 % en el país, una diferencia que aporta 0.251 al índice. En ambos casos, el KSI incorpora las aportaciones de las 21 actividades.

[[FIG:02_Diferencias_sectoriales_KSI.png|Figura II.2.2. Mayores diferencias sectoriales respecto de la estructura nacional. Se muestran cuatro por entidad; el KSI incorpora las 21 actividades.]]

## La concentración espacial de las actividades

La concentración espacial se estudia a partir de las columnas de la matriz, que reúnen la producción de una actividad en todas las entidades. Para cada actividad, qᵢⱼ expresa la participación de la entidad i en su VAB nacional, mientras que wᵢ representa el peso de esa entidad en el VAB total del país. El ICE suma las diferencias absolutas entre ambas participaciones a lo largo del territorio. La referencia es la distribución territorial del conjunto de la economía, de modo que el cálculo incorpora las diferencias de tamaño entre los estados.

[[EQ:ice]]

La medición de la localización industrial tiene antecedentes en Hoover (1936), y sus procedimientos forman parte de las técnicas de análisis regional sistematizadas por Lira y Quiroga (2009). El ICE aquí utilizado aplica a las participaciones territoriales la distancia absoluta empleada por Krugman, con una escala general de cero a dos. En las formulaciones que dividen la suma entre dos, el intervalo es de cero a uno. La normalización se identifica en la fórmula y determina la escala en que se expresan los resultados.

Un ICE de cero expresa una distribución sectorial proporcional al peso económico de las entidades. Con una participación estatal de 10 % en el VAB del país, la proporcionalidad corresponde a una aportación de 10 % al VAB de la actividad examinada. La diferencia entre ambas participaciones es cero y esa entidad no agrega distancia al índice. El ICE aumenta conforme las participaciones sectoriales se apartan de los pesos estatales, aun en actividades presentes en numerosos estados. Su valor depende de cuánto se aleja la distribución de la actividad de la distribución territorial del VAB nacional.

Campeche y Tabasco reúnen 87.57 % del VAB de la minería petrolera y 4.39 % del VAB total del país, con un ICE sectorial de 1.727. En los corporativos, la participación de la Ciudad de México también rebasa ampliamente su peso en la economía nacional, mientras que el comercio al por mayor presenta un ICE de 0.174 y una distribución más cercana a la referencia. La especialización manufacturera de Coahuila, en cambio, forma parte de una actividad extendida entre numerosos estados. El KSI describe la composición completa de esa entidad y el ICE manufacturero resume la distribución de la actividad entre todas las entidades.

[[FIG:03_ICE_sectores.png|Figura II.2.3. Concentración espacial relativa por actividad económica en 2024.]]

## El Índice de Especialización Económica

La especialización de cada combinación de entidad y actividad se obtiene al dividir la participación local de la actividad entre su participación nacional. Este cálculo corresponde al cociente de localización, utilizado tempranamente por Hildebrand y Mace (1950) en el análisis del empleo regional y sistematizado por Lira y Quiroga (2009). Aquí se denomina Índice de Especialización Económica y se aplica al valor agregado. Las diferencias de productividad entre actividades explican que sus resultados difieran de los obtenidos con empleo, puesto que cada variable asigna un peso distinto a los sectores. La fórmula admite dos expresiones equivalentes, una basada en las participaciones sectoriales y otra en las territoriales.

[[EQ:iee]]

El IEE es igual a uno cuando la participación estatal de una actividad coincide con la nacional. Los valores superiores a uno indican un peso relativo mayor dentro de la entidad, y los inferiores, una participación local menor. Un IEE de dos expresa que la participación local duplica la nacional, siguiendo la interpretación habitual del cociente de localización (U.S. Bureau of Labor Statistics, 2011). El cero corresponde a una actividad nula en la celda examinada, con denominadores positivos.

El IEE expresa una proporción entre participaciones y su escala depende del peso nacional de la actividad, por lo que carece del máximo universal de dos utilizado en los índices anteriores. Una actividad que aporta 1 % del VAB del país y 10 % del estatal registra un IEE de diez. Ese valor resulta de dividir las participaciones y describe la importancia relativa del sector dentro de la entidad. El umbral de uno separa las actividades con un peso local superior al nacional de aquellas con una participación inferior, y sirve para reconocer el perfil de especialización de cada estado.

En las manufacturas de Coahuila, la participación en el VAB estatal es aproximadamente 0.4674, frente a 0.2167 en el país. La división de ambas proporciones, utilizando los valores completos antes del redondeo, da el siguiente resultado.

[[EQ:ejemplo]]

El peso manufacturero dentro de Coahuila equivale a unas 2.16 veces el nacional. Al utilizar la expresión territorial de la fórmula, la participación de Coahuila en las manufacturas del país equivale a 2.16 veces su peso en el VAB nacional. Ambas operaciones producen el mismo cociente porque relacionan el valor de la actividad estatal con los mismos totales de la matriz. La primera expresión utiliza la composición productiva local y la segunda, la distribución territorial de las manufacturas.

## Relación entre los índices

Al sustituir las participaciones por su expresión en términos del IEE, el KSI y el ICE se escriben como sumas ponderadas de las distancias del cociente respecto de uno. Las ponderaciones del KSI corresponden a las participaciones nacionales de las actividades, y las del ICE, a los pesos económicos de las entidades. En estas expresiones se conserva el valor absoluto para sumar todas las desviaciones respecto de la referencia.

[[EQ:relaciones]]

La aportación de una actividad al KSI depende de su participación nacional y de la distancia de su IEE respecto de uno. Las actividades grandes reciben una ponderación mayor, mientras que las de escaso peso nacional aportan menos ante una misma desviación del cociente. A su vez, el promedio del KSI ponderado por el VAB estatal coincide con el promedio del ICE ponderado por el VAB de las actividades. Ambos promedios agregan las distancias de la misma matriz, conservando la importancia económica de cada entidad y cada actividad.

Al reunir actividades, las diferencias de signo contrario se compensan dentro del nuevo grupo. Por la desigualdad triangular, esta agregación reduce o conserva la suma de diferencias absolutas cuando se mantiene la misma información y referencia. La separación de la minería petrolera y la no petrolera recoge diferencias entre los perfiles extractivos de las entidades mexicanas que se compensan parcialmente en el sector agregado. En las manufacturas ocurre lo mismo entre ramas industriales, de manera que el detalle de la clasificación determina el nivel al que se estudia la especialización. Las comparaciones se realizan con una desagregación equivalente.

En la figura II.2.4, las filas muestran el perfil de especialización de cada entidad y las columnas, la presencia relativa de cada actividad entre estados. El degradado continuo va del azul al rojo oscuro, con un tono claro en la unidad; los azules corresponden a participaciones inferiores a la nacional y los rojos, a valores superiores. Para representar las diferencias entre las 672 combinaciones se aplica al color el logaritmo de uno más el IEE, que conserva los ceros. La barra inferior presenta los valores originales del índice y relaciona cada tonalidad con la intensidad de la especialización.

Los mapas del IEE utilizan una escala común para comparar la localización de las actividades. La minería petrolera presenta sus mayores cocientes en Campeche y Tabasco, mientras que las manufacturas tienen un patrón extendido hacia el norte y el centro del país, como se observa en las figuras II.2.5 y II.2.6. En cada mapa se identifican las cinco entidades con mayor IEE y se conserva el valor del cociente en sus etiquetas.

[[FIG:05_Matriz_IEE_completa.png|Figura II.2.4. Índice de Especialización Económica en las 32 entidades y las 21 actividades. Los colores representan un degradado continuo del IEE; la barra inferior muestra su escala.]]

[[FIG:09_IEE_mineria_petrolera.png|Figura II.2.5. Especialización relativa en minería petrolera. Se identifican las cinco entidades con mayor IEE.]]

[[FIG:10_IEE_manufacturas.png|Figura II.2.6. Especialización relativa en manufacturas. Se señalan las cinco entidades con mayor IEE.]]

En las actividades terciarias, los mapas de las figuras II.2.7 y II.2.8 muestran los perfiles correspondientes a los servicios financieros y al alojamiento y preparación de alimentos. La primera actividad comprende los servicios financieros y de seguros; la segunda reúne establecimientos que atienden tanto demanda turística como consumo local. El sector de alojamiento y alimentos representa una parte de las actividades vinculadas con el turismo. La cobertura de cada columna de la matriz determina la actividad económica a la que corresponde su IEE.

[[FIG:11_IEE_servicios_financieros.png|Figura II.2.7. Servicios financieros y seguros. Cinco entidades con mayor IEE.]]

[[FIG:12_IEE_alojamiento_alimentos.png|Figura II.2.8. Alojamiento temporal y preparación de alimentos y bebidas. Cinco entidades con mayor IEE.]]

## Alcances de la medición

Las unidades monetarias se cancelan al formar las participaciones, por lo que expresar el VAB en pesos o en millones de pesos produce los mismos índices. La elección de precios, en cambio, modifica la ponderación de las actividades dentro del valor agregado. Los precios de 2018 valoran la composición sectorial con la estructura de ese año, mientras que los precios corrientes incorporan las variaciones posteriores de los precios relativos. La comparación entre periodos conserva una base de precios y una cobertura compatibles, y toma en cuenta los cambios de la estructura nacional utilizada como referencia.

Los índices describen la distribución de la actividad económica y la división territorial de la producción en un año. El estudio de las cadenas de valor regionales sigue las compras y ventas entre actividades, tanto dentro de una entidad como entre regiones. La matriz de insumo-producto, desarrollada en el siguiente apartado, organiza esas relaciones y describe la interdependencia productiva que existe detrás de las participaciones sectoriales.

## Referencias

Hildebrand, G. H., y Mace, A., Jr. (1950). The employment multiplier in an expanding industrial market: Los Angeles County, 1940-47. The Review of Economics and Statistics, 32(3), 241-249. https://doi.org/10.2307/2937531

Hoover, E. M., Jr. (1936). The measurement of industrial localization. The Review of Economics and Statistics, 18(4), 162-171. https://doi.org/10.2307/1927875

Instituto Nacional de Estadística y Geografía (INEGI). (2026, consulta). Producto Interno Bruto por Entidad Federativa. Año base 2018. Sistema de Cuentas Nacionales de México. Datos de 2024. https://www.inegi.org.mx/programas/pibent/2018/

Krugman, P. (1991). Geography and Trade. MIT Press y Leuven University Press. https://mitpress.mit.edu/9780262111591/geography-and-trade/

Krugman, P. (2010). The New Economic Geography, Now Middle-Aged. Ponencia para la Association of American Geographers, 16 de abril. https://www.princeton.edu/~pkrugman/aag.pdf

Lira, L., y Quiroga, B. (2009). Técnicas de análisis regional. Serie Manuales, núm. 59. CEPAL e ILPES. https://digitallibrary.un.org/record/674928

U.S. Bureau of Labor Statistics. (2011). Using Location Quotients to Analyze Occupational Data. Occupational Employment Statistics Highlights, abril. https://www.bls.gov/oes/highlight_location_quotients.htm
```
<!-- PAPIME:END MANUSCRITO -->

### Apéndice B. Script final íntegro: `scripts/Plots_Krugman_2024.R`

Esta copia conserva la ruta Windows original y el parámetro de cinco entidades destacadas. Para ejecutarla en la carpeta nueva se recomienda el lanzador del apéndice E.

<!-- PAPIME:BEGIN SCRIPT_R -->
```r
# Capítulo II, inciso 2. Medición de la especialización
# México, 2024. Valor agregado a precios de 2018.
# KSI e ICE: distancia absoluta sin dividir entre dos. IEE: cociente de localización.

ruta_excel <- "C:/Users/marce/Downloads/PIBE/PIBE_2024_In.xlsx"
carpeta_salida <- file.path(dirname(ruta_excel), "Figuras_Capitulo_II_Especializacion_2024")
carpeta_geografia <- file.path(dirname(ruta_excel), "Cartografia_INEGI")
ruta_cartografia <- ""
crear_mapas <- TRUE
guardar_pdf <- TRUE
n_destacados <- 5L
fuente <- "Fuente: elaboración propia con base en datos de INEGI (2026). PIBE 2024, precios de 2018."
# Se conserva el año de consulta indicado en el script original.

paquetes <- c("readxl", "dplyr", "tidyr", "ggplot2", "scales", "stringr",
              "ggrepel", "ragg")
faltantes <- paquetes[!vapply(paquetes, requireNamespace, logical(1), quietly = TRUE)]
if (length(faltantes)) install.packages(faltantes, repos = "https://cloud.r-project.org")
if (!all(vapply(paquetes, requireNamespace, logical(1), quietly = TRUE))) {
  stop("Faltan paquetes. Revisa los mensajes de instalación.")
}
suppressPackageStartupMessages({library(dplyr); library(tidyr); library(ggplot2)})
options(scipen = 999, timeout = max(120, getOption("timeout")))
if (!file.exists(ruta_excel)) stop("No se encontró el Excel: ", ruta_excel)
dir.create(carpeta_salida, recursive = TRUE, showWarnings = FALSE)
normalizar <- function(x) tolower(iconv(stringr::str_squish(x), to = "ASCII//TRANSLIT"))
comprobar <- function(condicion, mensaje) {
  if (!isTRUE(condicion)) stop(mensaje, call. = FALSE)
}
comparar <- function(a, b, mensaje, tolerancia = 1e-8) {
  comprobar(length(a) == length(b) && all(is.finite(a)) && all(is.finite(b)),
            paste(mensaje, "contiene datos incompletos."))
  comprobar(max(abs(as.numeric(a) - as.numeric(b))) <= tolerancia,
            paste(mensaje, "no coincide."))
}

# 1. Matriz original. No se usan los índices precalculados como insumo.
hojas <- readxl::excel_sheets(ruta_excel)
hoja <- hojas[normalizar(gsub("_", " ", hojas)) == "indices krugman"]
comprobar(length(hoja) == 1, "No se encontró una única hoja Indices_Krugman.")
tabla <- readxl::read_excel(ruta_excel, sheet = hoja, range = "A1:W34",
  col_types = c("text", rep("numeric", 22)), .name_repair = "minimal")
comprobar(nrow(tabla) == 33 && ncol(tabla) == 23, "Se esperan 32 entidades y el total nacional.")
comprobar(normalizar(tabla[[1]][33]) == "estados unidos mexicanos", "Falta la fila nacional.")
comprobar(length(unique(tabla[[1]][1:32])) == 32, "Hay entidades repetidas.")
sectores <- tibble(
  codigo = c("11", "21-1", "21-2", "22", "23", "31-33", "43", "46", "48-49",
             "51", "52", "53", "54", "55", "56", "61", "62", "71", "72", "81", "93"),
  etiqueta = c(
    "11 Agricultura, ganadería, pesca y actividades forestales",
    "21-1 Minería petrolera", "21-2 Minería no petrolera",
    "22 Electricidad, agua y gas", "23 Construcción", "31-33 Manufacturas",
    "43 Comercio al por mayor", "46 Comercio al por menor",
    "48-49 Transportes, correos y almacenamiento", "51 Información en medios masivos",
    "52 Servicios financieros y seguros", "53 Servicios inmobiliarios y alquiler",
    "54 Servicios profesionales, científicos y técnicos", "55 Corporativos",
    "56 Apoyo a negocios, residuos y remediación", "61 Servicios educativos",
    "62 Salud y asistencia social", "71 Esparcimiento, cultura y deporte",
    "72 Alojamiento y preparación de alimentos", "81 Otros servicios",
    "93 Actividades gubernamentales y legislativas"
  ),
  grupo = c("Primarias", rep("Secundarias", 5), rep("Terciarias", 15)),
  nombre_excel = names(tabla)[2:22]
)
codigos_excel <- stringr::str_trim(sub(" - .*", "", sectores$nombre_excel))
comprobar(identical(codigos_excel, sectores$codigo),
          "Cambió la selección u orden de los 21 sectores de la tabla.")

registro <- tibble(
  cve_ent = sprintf("%02d", 1:32),
  nombre = c("Aguascalientes", "Baja California", "Baja California Sur", "Campeche",
             "Coahuila de Zaragoza", "Colima", "Chiapas", "Chihuahua", "Ciudad de México",
             "Durango", "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", "México",
             "Michoacán de Ocampo", "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla",
             "Querétaro", "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco",
             "Tamaulipas", "Tlaxcala", "Veracruz de Ignacio de la Llave", "Yucatán", "Zacatecas"),
  nombre_corto = c("Aguascalientes", "Baja California", "Baja California Sur", "Campeche",
                   "Coahuila", "Colima", "Chiapas", "Chihuahua", "Ciudad de México",
                   "Durango", "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", "Estado de México",
                   "Michoacán", "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla",
                   "Querétaro", "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco",
                   "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"),
  abreviatura = c("Ags.", "B.C.", "B.C.S.", "Camp.", "Coah.", "Col.", "Chis.", "Chih.",
                 "CDMX", "Dgo.", "Gto.", "Gro.", "Hgo.", "Jal.", "Méx.", "Mich.", "Mor.",
                 "Nay.", "N.L.", "Oax.", "Pue.", "Qro.", "Q.Roo", "S.L.P.", "Sin.",
                 "Son.", "Tab.", "Tamps.", "Tlax.", "Ver.", "Yuc.", "Zac.")
)
posiciones <- match(normalizar(tabla[[1]][1:32]), normalizar(registro$nombre))
comprobar(!anyNA(posiciones), "Hay nombres de entidades que no se pudieron identificar.")
estados <- registro[posiciones, ]

X <- as.matrix(tabla[1:32, 2:22])
nacional <- as.numeric(unlist(tabla[33, 2:22], use.names = FALSE))
comprobar(all(is.finite(X)) && all(X >= 0) && all(is.finite(nacional)) && all(nacional > 0),
          "Hay celdas faltantes, negativas o sectores nacionales sin actividad.")
total_estado <- rowSums(X)
total_nacional <- sum(nacional)
comprobar(all(total_estado > 0), "Los totales estatales deben ser positivos.")
comparar(total_estado, tabla[[23]][1:32], "Totales estatales", 0.02)
comparar(total_nacional, tabla[[23]][33], "Total nacional", 0.02)
comparar(colSums(X), nacional, "Agregación territorial", 0.02)

s <- sweep(X, 1, total_estado, "/")       # s_ij = x_ij / x_i.
s_nacional <- nacional / total_nacional # s_j = x_.j / x_..
q <- sweep(X, 2, nacional, "/")          # q_ij = x_ij / x_.j
peso_estado <- total_estado / total_nacional # w_i = x_i. / x_..
IEE <- sweep(s, 2, s_nacional, "/")      # IEE_ij = s_ij / s_j = q_ij / w_i
diferencias <- sweep(s, 2, s_nacional, "-")
exceso_territorial <- sweep(q, 1, peso_estado, "-")
aportaciones_ksi <- abs(diferencias)
aportaciones_ice <- abs(exceso_territorial)
ksi <- rowSums(aportaciones_ksi)
ice <- colSums(aportaciones_ice)

comparar(rowSums(s), rep(1, 32), "Participaciones estatales")
comparar(colSums(q), rep(1, 21), "Participaciones territoriales")
comparar(IEE, sweep(q, 1, peso_estado, "/"), "Dos expresiones del IEE")
comparar(as.numeric(IEE %*% s_nacional), rep(1, 32), "Promedio sectorial ponderado del IEE")
comparar(as.numeric(crossprod(peso_estado, IEE)), rep(1, 21), "Promedio territorial ponderado del IEE")
comparar(sum(peso_estado * ksi), sum(s_nacional * ice), "Identidad ponderada KSI e ICE")
comprobar(all(ksi >= 0 & ksi <= 2) && all(ice >= 0 & ice <= 2), "KSI o ICE fuera de rango.")
comprobar(all(is.finite(IEE)) && all(IEE >= 0), "Hay IEE no válidos.")

# La comparación con resultados guardados es informativa; el cálculo no depende de ellos.
revision_excel <- tryCatch({
  k <- readxl::read_excel(ruta_excel, sheet = hoja, range = "W78:W109", col_names = FALSE, .name_repair = "minimal")[[1]]
  c <- unlist(readxl::read_excel(ruta_excel, sheet = hoja, range = "B147:V147", col_names = FALSE, .name_repair = "minimal"))
  comparar(ksi, as.numeric(k), "KSI guardado en Excel")
  comparar(ice, as.numeric(c), "ICE guardado en Excel")
  "KSI e ICE coinciden con los valores guardados en Excel."
}, error = function(e) paste("Se recalculó desde la matriz original.", conditionMessage(e)))
message(revision_excel)

estados$VAB <- total_estado
estados$peso <- peso_estado
estados$KSI <- ksi
sectores$ICE <- ice
sectores$participacion_nacional <- s_nacional
dimnames(X) <- dimnames(s) <- dimnames(q) <- dimnames(IEE) <-
  dimnames(diferencias) <- dimnames(aportaciones_ksi) <- dimnames(aportaciones_ice) <-
  list(estados$cve_ent, sectores$codigo)
datos <- expand.grid(cve_ent = estados$cve_ent, codigo = sectores$codigo,
                     KEEP.OUT.ATTRS = FALSE, stringsAsFactors = FALSE)
datos$VAB_sector <- as.vector(X)
datos$participacion_local <- as.vector(s)
datos$participacion_sector <- as.vector(q)
datos$IEE <- as.vector(IEE)
datos$diferencia_pp <- as.vector(diferencias) * 100
datos$aportacion_KSI <- as.vector(aportaciones_ksi)
datos$aportacion_ICE <- as.vector(aportaciones_ice)
datos <- datos %>% left_join(estados, by = "cve_ent") %>% left_join(sectores, by = "codigo")

# 2. Cuadros completos para reproducir el texto y consultar cada celda.
escribir_csv <- function(x, nombre) {
  write.csv(x, file.path(carpeta_salida, paste0(nombre, ".csv")),
            row.names = FALSE, fileEncoding = "UTF-8", na = "")
}
escribir_csv(estados %>% arrange(desc(KSI)), "KSI_entidades")
escribir_csv(sectores %>% arrange(desc(ICE)), "ICE_sectores")
escribir_csv(datos, "Indices_entidad_sector")
escribir_csv(cbind(entidad = estados$nombre, as.data.frame(IEE, check.names = FALSE)), "Matriz_IEE")
escribir_csv(sectores %>% select(codigo, etiqueta, nombre_excel), "Catalogo_sectores")

# Comparación de 21 actividades con la agregación usual de 20 sectores.
X20 <- cbind(X[, 1], rowSums(X[, 2:3, drop = FALSE]), X[, 4:21])
n20 <- c(nacional[1], sum(nacional[2:3]), nacional[4:21])
ksi20 <- rowSums(abs(sweep(sweep(X20, 1, total_estado, "/"), 2, n20 / total_nacional, "-")))
comprobar(all(ksi20 <= ksi + 1e-10), "La agregación aumentó el KSI: revisa el cálculo.")
sensibilidad <- estados %>% mutate(KSI_21 = ksi, KSI_20 = ksi20,
  diferencia = KSI_21 - KSI_20) %>% select(cve_ent, nombre_corto, KSI_21, KSI_20, diferencia)
escribir_csv(sensibilidad, "Sensibilidad_agregacion_minera")

# 3. Formato. Figuras PNG de 320 ppp y PDF vectoriales.
familia <- if (Sys.info()[["sysname"]] == "Windows") "Arial" else "sans"
azul <- "#00688B"; naranja <- "#CD6600"; morado <- "#571854"
form_indice <- scales::label_number(accuracy = 0.001, decimal.mark = ".")
form_pct <- scales::label_percent(accuracy = 0.1, decimal.mark = ".")
tema <- function() theme_minimal(base_size = 15, base_family = familia) + theme(
  panel.grid.minor = element_blank(), panel.grid.major.y = element_blank(),
  panel.grid.major.x = element_line(color = "#E3E3E3", linewidth = 0.3),
  plot.title = element_text(face = "bold", size = 17, color = "black"),
  plot.caption = element_text(size = 9, hjust = 0, margin = margin(t = 10)),
  plot.caption.position = "plot", plot.title.position = "plot", axis.text = element_text(color = "#222222", size = 14),
  legend.position = "bottom", strip.text = element_text(face = "bold", size = 12),
  plot.margin = margin(12, 20, 12, 12))
guardar <- function(p, nombre, ancho = 11, alto = 7) {
  ggsave(file.path(carpeta_salida, paste0(nombre, ".png")), p,
         width = ancho, height = alto, dpi = 320, device = ragg::agg_png, bg = "white", limitsize = FALSE)
  if (guardar_pdf) {
    dispositivo <- if (capabilities("cairo")) grDevices::cairo_pdf else grDevices::pdf
    ggsave(file.path(carpeta_salida, paste0(nombre, ".pdf")), p,
           width = ancho, height = alto, device = dispositivo, bg = "white", limitsize = FALSE)
  }
  message("Guardado: ", nombre)
}
orden_ksi <- estados$nombre_corto[order(ksi, decreasing = TRUE)]

# Figura II.2.1. KSI de todas las entidades.
p <- ggplot(estados, aes(KSI, reorder(nombre_corto, KSI))) +
  geom_col(fill = azul, width = 0.7) +
  geom_text(aes(label = form_indice(KSI)), hjust = -0.15, size = 4.2, family = familia) +
  scale_x_continuous(limits = c(0, 2), breaks = seq(0, 2, 0.25), expand = c(0, 0)) +
  labs(title = "Especialización productiva estatal en 2024",
       x = "KSI (0 a 2)", y = NULL, caption = fuente) + tema()
guardar(p, "01_KSI_entidades", 10, 10.7)

# Figura II.2.2. Diferencias con signo. Se muestran las cuatro mayores por entidad.
seleccion <- c("Campeche", "Coahuila", "Ciudad de México", "Jalisco")
d <- datos %>% filter(nombre_corto %in% seleccion) %>% group_by(cve_ent) %>%
  slice_max(aportacion_KSI, n = 4, with_ties = FALSE) %>% ungroup() %>%
  mutate(panel = factor(nombre_corto, levels = seleccion),
         item = paste(nombre_corto, etiqueta, sep = "::"),
         signo = ifelse(diferencia_pp >= 0, "Mayor peso local", "Menor peso local"))
p <- ggplot(d, aes(diferencia_pp, reorder(item, diferencia_pp), fill = signo)) +
  geom_vline(xintercept = 0, linewidth = 0.3) + geom_col(width = 0.65) +
  geom_text(aes(label = sprintf("%+.1f", diferencia_pp),
                hjust = ifelse(diferencia_pp >= 0, -0.12, 1.12)), size = 4.4, family = familia) +
  facet_wrap(~panel, ncol = 2, scales = "free_y") +
  scale_y_discrete(labels = function(z) {
    cod <- sub(" .*", "", sub(".*::", "", z))
    breve <- c("11" = "Agricultura y afines", "21-1" = "Minería petrolera", "23" = "Construcción",
      "31-33" = "Manufacturas", "43" = "Comercio mayorista", "46" = "Comercio minorista",
      "51" = "Información", "52" = "Servicios financieros", "53" = "Inmobiliarios", "54" = "Servicios profesionales")
    unname(breve[cod])
  }) +
  scale_fill_manual(values = c("Mayor peso local" = naranja, "Menor peso local" = azul), name = NULL) +
  scale_x_continuous(limits = c(-45, 90), breaks = c(-25, 0, 25, 50, 75)) +
  labs(title = "Diferencias respecto de la estructura nacional",
       x = "Participación estatal menos participación nacional (puntos porcentuales)", y = NULL,
       caption = paste("Cuatro mayores diferencias absolutas por entidad. El KSI suma las 21 actividades.", fuente, sep = "\n")) + tema() +
  theme(axis.text.y = element_text(size = 13), panel.spacing.x = grid::unit(0.6, "cm"))
guardar(p, "02_Diferencias_sectoriales_KSI", 11, 7.8)

# Figura II.2.3. El ICE es un valor por sector, no por entidad.
p <- ggplot(sectores, aes(ICE, reorder(etiqueta, ICE))) +
  geom_col(fill = morado, width = 0.7) +
  geom_text(aes(label = form_indice(ICE)), hjust = -0.15, size = 4.2, family = familia) +
  scale_y_discrete(labels = function(z) stringr::str_wrap(z, 44)) +
  scale_x_continuous(limits = c(0, 2), breaks = seq(0, 2, 0.25), expand = c(0, 0)) +
  labs(title = "Concentración espacial de las actividades en 2024",
       x = "ICE (0 a 2)", y = NULL, caption = fuente) + tema()
guardar(p, "03_ICE_sectores", 10, 9.5)

# Material complementario. Comparación territorial que da origen al ICE.
d <- lapply(c("21-1", "55"), function(cod) {
  a <- datos %>% filter(codigo == cod) %>% arrange(desc(participacion_sector))
  bind_rows(a %>% slice_head(n = 5) %>% select(nombre_corto, participacion_sector, peso),
    a %>% slice(6:n()) %>% summarise(nombre_corto = "Resto de entidades",
      participacion_sector = sum(participacion_sector), peso = sum(peso))) %>%
    mutate(panel = a$etiqueta[1], item = paste(cod, nombre_corto, sep = "::"))
}) %>% bind_rows()
p <- ggplot(d, aes(y = reorder(item, participacion_sector))) +
  geom_segment(aes(x = peso, xend = participacion_sector, yend = reorder(item, participacion_sector)), color = "grey70") +
  geom_point(aes(x = participacion_sector, color = "Participación en el sector"), size = 3) +
  geom_point(aes(x = peso, color = "Peso económico estatal"), size = 3) +
  facet_wrap(~panel, ncol = 2, scales = "free_y") +
  scale_y_discrete(labels = function(z) sub(".*::", "", z)) +
  scale_color_manual(values = c("Participación en el sector" = morado, "Peso económico estatal" = naranja), name = NULL) +
  scale_x_continuous(labels = form_pct, limits = c(0, 1)) +
  labs(title = "Distribución de la actividad y peso de las entidades",
       x = "Participación nacional", y = NULL, caption = fuente) + tema()
guardar(p, "04_Distribucion_territorial_ICE", 13, 6)

# Figura II.2.4. Matriz completa de IEE, sin rótulos dentro de las celdas.
# Degradado continuo azul a rojo oscuro y una barra horizontal común.
# log(1 + IEE) comprime el color, conserva los ceros y no altera los índices.
limite_iee <- max(24, ceiling(max(datos$IEE)))
puntos_iee <- c(0, 0.5, 1, 2, 4, 8, limite_iee)
paleta_iee <- c("#244A73", "#7DA5BD", "#F4F0EA", "#DDB1A8",
                "#C4787C", "#A44759", "#681D32")
escala_iee <- function() scale_fill_gradientn(
  colors = paleta_iee, values = log1p(puntos_iee) / log1p(limite_iee),
  trans = "log1p", limits = c(0, limite_iee),
  breaks = c(0, 0.5, 1, 2, 4, 8, 16, 24),
  labels = c("0", "0.5", "1", "2", "4", "8", "16", "24"),
  name = "IEE · Referencia nacional = 1",
  guide = guide_colorbar(direction = "horizontal", title.position = "top", title.hjust = 0.5,
    barwidth = grid::unit(14, "cm"), barheight = grid::unit(0.45, "cm"), nbin = 512,
    ticks.colour = "#F4F0EA", frame.colour = NA))
etiquetas_cortas <- c("11 Agropecuario", "21-1 Petróleo", "21-2 Otra minería",
  "22 Energía y agua", "23 Construcción", "31-33 Manufacturas", "43 Mayoreo",
  "46 Menudeo", "48-49 Transportes", "51 Información", "52 Finanzas",
  "53 Inmobiliarios", "54 Profesionales", "55 Corporativos", "56 Apoyo a negocios",
  "61 Educación", "62 Salud", "71 Esparcimiento", "72 Alojamiento y alimentos",
  "81 Otros servicios", "93 Gobierno")
d <- datos %>% mutate(
  entidad = factor(nombre_corto, levels = rev(registro$nombre_corto)),
  actividad = factor(codigo, levels = sectores$codigo))
comprobar(nrow(d) == 32 * 21 && all(is.finite(d$IEE)), "La matriz de IEE no está completa.")
p <- ggplot(d, aes(actividad, entidad, fill = IEE)) +
  geom_tile(color = "white", linewidth = 0.42, width = 0.98, height = 0.98) +
  escala_iee() + scale_x_discrete(labels = etiquetas_cortas, expand = c(0, 0)) +
  scale_y_discrete(expand = c(0, 0)) +
  labs(title = "Especialización productiva en las 32 entidades",
       x = NULL, y = NULL,
       caption = paste("Matriz completa: 32 entidades y 21 actividades. Color continuo en escala log(1 + IEE).",
                       fuente, sep = "\n")) +
  tema() + theme(panel.grid = element_blank(), plot.title = element_text(size = 15),
    axis.text.y = element_text(size = 12),
    axis.text.x = element_text(size = 10.7, angle = 60, hjust = 1, vjust = 1),
    axis.ticks = element_blank(), legend.title = element_text(size = 11.5),
    legend.text = element_text(size = 10.3), legend.key.width = grid::unit(0.45, "cm"),
    legend.key.height = grid::unit(0.38, "cm"), legend.spacing.x = grid::unit(0.16, "cm"),
    plot.caption = element_text(size = 8.5, lineheight = 1.15),
    plot.margin = margin(12, 12, 12, 10))
guardar(p, "05_Matriz_IEE_completa", 8.8, 11.2)

d <- sensibilidad %>% arrange(desc(diferencia)) %>% slice_head(n = 8) %>%
  pivot_longer(c(KSI_21, KSI_20), names_to = "agregacion", values_to = "KSI")
p <- ggplot(d, aes(KSI, reorder(nombre_corto, diferencia), color = agregacion)) +
  geom_point(size = 3.5) +
  scale_color_manual(values = c(KSI_21 = naranja, KSI_20 = azul),
                     labels = c(KSI_21 = "Minería separada (21 actividades)", KSI_20 = "Minería agregada (20 sectores)"), name = NULL) +
  labs(title = "El nivel de agregación modifica la medición",
       x = "KSI", y = NULL, caption = paste("Ocho entidades con mayor diferencia. Se conserva toda la actividad económica.", fuente, sep = "\n")) + tema()
guardar(p, "07_Sensibilidad_agregacion", 11, 6.5)

# 4. Mapas de índices, exclusivamente con límites estatales del INEGI.
# No hay capas físicas, ríos, relieve ni un mapa de ICE por estado.
if (crear_mapas) {
  if (!requireNamespace("sf", quietly = TRUE)) install.packages("sf", repos = "https://cloud.r-project.org")
  tryCatch({
    comprobar(requireNamespace("sf", quietly = TRUE), "No se pudo instalar sf.")
    dir.create(carpeta_geografia, recursive = TRUE, showWarnings = FALSE)
    archivo_geo <- if (nzchar(ruta_cartografia)) ruta_cartografia else
      file.path(carpeta_geografia, "entidades_INEGI.geojson")
    if (!file.exists(archivo_geo)) {
      temporal <- tempfile(fileext = ".geojson")
      utils::download.file("https://gaia.inegi.org.mx/wscatgeo/v2/geo/mgee/", temporal,
                           mode = "wb", quiet = TRUE, method = "libcurl")
      comprobar(file.copy(temporal, archivo_geo, overwrite = TRUE), "No se guardó la cartografía.")
      unlink(temporal)
    }
    geo <- sf::st_read(archivo_geo, quiet = TRUE, stringsAsFactors = FALSE)
    campos <- tolower(names(geo))
    pos <- match("cve_ent", campos)
    if (is.na(pos)) pos <- match("cvegeo", campos)
    comprobar(!is.na(pos), "La cartografía necesita cve_ent o cvegeo.")
    geo$cve_ent <- sprintf("%02d", as.integer(as.character(geo[[pos]])))
    comprobar(setequal(unique(geo$cve_ent), registro$cve_ent), "La cartografía debe cubrir las 32 entidades.")
    if (is.na(sf::st_crs(geo))) {
      comprobar(tolower(tools::file_ext(archivo_geo)) %in% c("geojson", "json"), "Falta el CRS de la cartografía.")
      sf::st_crs(geo) <- 4326
    }
    crs_mexico <- "+proj=lcc +lat_1=17.5 +lat_2=29.5 +lat_0=12 +lon_0=-102 +datum=WGS84 +units=m +no_defs"
    geo <- geo %>% select(cve_ent)
    geo <- sf::st_transform(sf::st_make_valid(sf::st_zm(geo)), crs_mexico)
    geo <- geo %>% group_by(cve_ent) %>% summarise(.groups = "drop")
    comprobar(nrow(geo) == 32 && !any(sf::st_is_empty(geo)), "Hay geometrías faltantes.")
    # Simplificación visual de 300 m: no modifica los datos ni las claves estatales.
    geo <- sf::st_simplify(geo, dTolerance = 300, preserveTopology = TRUE)
    # Un archivo por mapa. Los contornos se conservan y no hay ejes geográficos.
    borde_nacional <- sf::st_union(geo)
    tema_mapa <- function() theme_void(base_size = 15, base_family = familia) + theme(
      plot.title = element_text(face = "bold", size = 21, color = "#24313A", hjust = 0),
      plot.title.position = "plot", plot.caption.position = "plot",
      plot.caption = element_text(size = 10, color = "#4D5961", hjust = 0,
                                  margin = margin(t = 12), lineheight = 1.2),
      legend.position = "bottom", legend.title = element_text(size = 13),
      legend.text = element_text(size = 12), legend.key.width = grid::unit(0.55, "cm"),
      legend.key.height = grid::unit(0.4, "cm"),
      legend.spacing.x = grid::unit(0.2, "cm"),
      plot.background = element_rect(fill = "white", color = NA),
      plot.margin = margin(18, 24, 16, 24))
    centros <- sf::st_coordinates(sf::st_point_on_surface(sf::st_geometry(geo)))
    posiciones <- data.frame(cve_ent = geo$cve_ent, x = centros[, 1], y = centros[, 2])
    mapa <- geo %>% left_join(estados, by = "cve_ent")
    etiquetas_ksi <- estados %>% slice_max(KSI, n = n_destacados, with_ties = FALSE) %>%
      left_join(posiciones, by = "cve_ent")
    p <- ggplot(mapa) + geom_sf(aes(fill = KSI), color = "#45414B", linewidth = 0.22) +
      geom_sf(data = borde_nacional, fill = NA, color = "#39343F", linewidth = 0.32) +
      scale_fill_gradientn(
        colors = c("#244A73", "#6C94B0", "#B7CBD7", "#F4F0EA", "#DAB6AF", "#B65E6B", "#681D32"),
        values = seq(0, 1, length.out = 7), limits = c(0, 2),
        name = "KSI", breaks = c(0, 0.25, 0.5, 0.75, 1, 1.5, 2),
        guide = guide_colorbar(direction = "horizontal", title.position = "top", title.hjust = 0.5,
          barwidth = grid::unit(14, "cm"), barheight = grid::unit(0.45, "cm"), nbin = 512,
          ticks.colour = "#F4F0EA", frame.colour = NA)) +
      ggrepel::geom_label_repel(data = etiquetas_ksi,
        aes(x = x, y = y, label = paste0(abreviatura, " ", sprintf("%.3f", KSI))),
        inherit.aes = FALSE, size = 4.7, family = familia, seed = 2024,
        max.overlaps = Inf, box.padding = 0.55, point.padding = 0.3,
        min.segment.length = 0, fill = "white", color = "#263D35", label.size = 0.15,
        segment.color = "#526E64", segment.size = 0.35) +
      coord_sf(datum = NA, expand = TRUE) +
      labs(title = "Especialización productiva estatal en 2024",
           caption = paste("Cinco entidades con mayor KSI. Escala de 0 a 2; un valor mayor indica más distancia respecto del país.",
                           fuente, sep = "\n")) + tema_mapa()
    guardar(p, "08_Mapa_KSI", 12, 8.6)

    # Figuras II.2.5 a II.2.8. Escala común y archivos separados para cada actividad.
    cod_mapa <- c("21-1", "31-33", "52", "72")
    titulos <- c("Minería petrolera", "Manufacturas", "Servicios financieros", "Alojamiento y alimentos")
    archivos <- c("09_IEE_mineria_petrolera", "10_IEE_manufacturas",
                  "11_IEE_servicios_financieros", "12_IEE_alojamiento_alimentos")
    for (k in seq_along(cod_mapa)) {
      d <- datos %>% filter(codigo == cod_mapa[k])
      mapas <- geo %>% left_join(d, by = "cve_ent")
      etiquetas <- d %>% slice_max(IEE, n = n_destacados, with_ties = FALSE) %>%
        left_join(posiciones, by = "cve_ent")
      p <- ggplot(mapas) + geom_sf(aes(fill = IEE), color = "#42494C", linewidth = 0.22) +
        geom_sf(data = borde_nacional, fill = NA, color = "#30383A", linewidth = 0.32) +
        escala_iee() +
        ggrepel::geom_label_repel(data = etiquetas,
          aes(x = x, y = y, label = paste0(abreviatura, " ", sprintf("%.2f", IEE))),
          inherit.aes = FALSE, size = 4.7, family = familia, seed = 2024,
          max.overlaps = Inf, box.padding = 0.5, point.padding = 0.3,
          min.segment.length = 0, fill = "white", color = "#263D35", label.size = 0.15,
          segment.color = "#526E64", segment.size = 0.35) +
        coord_sf(datum = NA, expand = TRUE) +
        labs(title = paste0(titulos[k], " en 2024"),
             caption = paste("Se señalan los cinco IEE más elevados. Color continuo en escala log(1 + IEE).",
                             fuente, sep = "\n")) + tema_mapa()
      guardar(p, archivos[k], 12, 8.6)
    }
  }, error = function(e) {
    aviso <- paste("No se generaron todos los mapas:", conditionMessage(e),
      "Las tablas y gráficas anteriores ya están guardadas. Revisa ruta_cartografia y vuelve a ejecutar.")
    warning(aviso, call. = FALSE)
    writeLines(aviso, file.path(carpeta_salida, "Aviso_cartografia.txt"), useBytes = TRUE)
  })
}

writeLines(c(
  "Medición de la especialización. México, 2024.",
  "Fuente de todos los cálculos: Indices_Krugman, A1:W34; matriz de 32 por 21 actividades.",
  "Unidad de origen: millones de pesos de 2018. Denominadores: sumas sectoriales de valor agregado.",
  "KSI_i = sum_j abs(s_ij - s_j). ICE_j = sum_i abs(q_ij - w_i). Ambos sin factor 1/2.",
  "IEE_ij = (x_ij / x_i.) / (x_.j / x_..). El umbral de especialización relativa es 1.",
  "21-1 y 21-2 son códigos de apertura de esta tabla, no nuevos sectores SCIAN independientes.",
  "Las figuras 01, 02, 03 y 05 corresponden a II.2.1 a II.2.4 del texto.",
  "Los mapas 09 a 12 corresponden a II.2.5 a II.2.8; cada uno se guarda por separado.",
  "Cada mapa señala las cinco entidades con mayor índice: KSI en 08 e IEE en 09 a 12.",
  "Las figuras 04, 07 y 08 son material complementario.",
  "El mapa de calor incluye las 672 celdas, sin cifras impresas. Los valores exactos están en los CSV.",
  "El mapa de calor y todos los mapas del IEE comparten un degradado continuo azul a rojo oscuro.",
  "La barra horizontal inferior muestra los valores originales del índice; el color usa log(1 + IEE).",
  "El azul corresponde a valores inferiores a uno; el tono claro señala uno y el rojo indica valores superiores.",
  "El cero conserva el extremo azul. El KSI utiliza un degradado continuo con su escala de cero a dos.",
  "IEE = 0 conserva los ceros observados. Los datos faltantes detienen el cálculo.",
  "KSI bajo indica semejanza al país; no demuestra por sí solo diversificación absoluta.",
  "ICE bajo indica distribución proporcional al peso económico estatal; no implica reparto igual entre estados.",
  "Referencias: Krugman (1991), Geography and Trade; Hoover (1936), doi:10.2307/1927875;",
  "Lira y Quiroga (2009), Técnicas de análisis regional, CEPAL, Manuales 59;",
  "Hildebrand y Mace (1950), doi:10.2307/2937531, antecedente del cociente de localización.",
  revision_excel,
  paste("Identidad ponderada KSI e ICE:", format(sum(peso_estado * ksi), digits = 12))
), file.path(carpeta_salida, "Guia_de_figuras_y_calculos.txt"), useBytes = TRUE)
capture.output(sessionInfo(), file = file.path(carpeta_salida, "Sesion_R.txt"))
message("Terminado. Resultados guardados en: ", normalizePath(carpeta_salida, winslash = "/"))
```
<!-- PAPIME:END SCRIPT_R -->

### Apéndice C. Generador portátil de Word: `scripts/build_doc.py`

El código conserva las ecuaciones nativas, las ocho figuras y la maquetación de la entrega. Las dos diferencias frente al generador anterior son la resolución de la raíz del proyecto y la lectura de `texto/seccion_revisada.md` en UTF-8.

<!-- PAPIME:BEGIN GENERADOR_DOCX -->
```python
from pathlib import Path
import re, copy
from lxml import etree
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT

ROOT=Path(__file__).resolve().parents[1]
FIG=ROOT/'output/Figuras_Capitulo_II_Especializacion_2024'
doc=Document()
sec=doc.sections[0]
sec.page_width=Inches(8.5);sec.page_height=Inches(11)
sec.top_margin=sec.bottom_margin=Inches(0.8)
sec.left_margin=sec.right_margin=Inches(0.85)
sec.header_distance=sec.footer_distance=Inches(0.35)

for name in ['Normal','Title','Heading 1','Heading 2','Caption']:
    st=doc.styles[name];st.font.name='Calibri';st.font.color.rgb=RGBColor(0,0,0)
    st._element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'),'Calibri')
normal=doc.styles['Normal'];normal.font.size=Pt(11.5)
pf=normal.paragraph_format;pf.line_spacing=1.15;pf.space_after=Pt(7)
pf.widow_control=True
for name,size in [('Title',16),('Heading 1',12.5),('Heading 2',12)]:
    st=doc.styles[name];st.font.size=Pt(size);st.font.bold=(name!='Title')
    st.paragraph_format.space_before=Pt(12);st.paragraph_format.space_after=Pt(8)
    st.paragraph_format.keep_with_next=True
doc.styles['Caption'].font.size=Pt(10)
doc.styles['Caption'].font.italic=False
doc.styles['Caption'].paragraph_format.line_spacing=1.0
doc.styles['Caption'].paragraph_format.space_after=Pt(5)
doc.styles['Caption'].paragraph_format.keep_with_next=True

# Ecuaciones nativas de Word. Se revisan también en la representación PDF.
def el(tag, **attrs):
    e=OxmlElement('m:'+tag)
    for k,v in attrs.items():e.set(qn('m:'+k),str(v))
    return e
def r(text,plain=False):
    e=el('r')
    if plain:
        pr=el('rPr');pr.append(el('sty',val='p'));e.append(pr)
    t=el('t');t.set('{http://www.w3.org/XML/1998/namespace}space','preserve');t.text=text;e.append(t);return e
def seq(x):
    if isinstance(x,list):return x
    if isinstance(x,str):return [r(x)]
    return [x]
def sub(base,s):
    e=el('sSub');b=el('e');b.extend(seq(base));u=el('sub');u.extend(seq(s));e.extend([b,u]);return e
def frac(a,b):
    e=el('f');n=el('num');n.extend(seq(a));d=el('den');d.extend(seq(b));e.extend([n,d]);return e
def summ(index,upper,body):
    e=el('nary');p=el('naryPr');p.append(el('chr',val='∑'));p.append(el('limLoc',val='undOvr'));e.append(p)
    lo=el('sub');lo.append(r(index));hi=el('sup');hi.append(r(upper));b=el('e');b.extend(seq(body));e.extend([lo,hi,b]);return e
def absval(body):
    e=el('d');p=el('dPr');p.append(el('begChr',val='|'));p.append(el('endChr',val='|'));e.append(p)
    b=el('e');b.extend(seq(body));e.append(b);return e
def v(base,idx):return sub(r(base),r(idx))
def idx(base,i):return sub(r(base,True),r(i))
def eq(items):
    p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before=Pt(4);p.paragraph_format.space_after=Pt(10)
    p.paragraph_format.line_spacing=1.0;p.paragraph_format.keep_together=True
    mp=el('oMathPara');pp=el('oMathParaPr');pp.append(el('jc',val='center'));mp.append(pp)
    m=el('oMath');m.extend(items);mp.append(m);p._p.append(mp)

def equation(key):
    if key=='totales':
        eq([v('x','i·'),r('='),summ('j=1','21',v('x','ij')),r('  ,  ',True),v('x','·j'),r('='),summ('i=1','32',v('x','ij'))])
        eq([v('x','··'),r('='),summ('i=1','32',v('x','i·')),r('='),summ('j=1','21',v('x','·j'))])
    elif key=='ksi':
        eq([v('s','ij'),r('='),frac(v('x','ij'),v('x','i·')),r('  ,  ',True),v('s','j'),r('='),frac(v('x','·j'),v('x','··'))])
        eq([idx('KSI','i'),r('='),summ('j=1','21',absval([v('s','ij'),r('−'),v('s','j')]))])
    elif key=='ice':
        eq([v('q','ij'),r('='),frac(v('x','ij'),v('x','·j')),r('  ,  ',True),v('w','i'),r('='),frac(v('x','i·'),v('x','··'))])
        eq([idx('ICE','j'),r('='),summ('i=1','32',absval([v('q','ij'),r('−'),v('w','i')]))])
    elif key=='iee':
        eq([idx('IEE','ij'),r('='),frac(frac(v('x','ij'),v('x','i·')),frac(v('x','·j'),v('x','··'))),
            r('='),frac(v('s','ij'),v('s','j')),r('='),frac(v('q','ij'),v('w','i'))])
    elif key=='ejemplo':
        eq([idx('IEE','Coahuila, manufacturas'),r('='),frac(r('0.4673996'),r('0.2167413')),r('≈2.156')])
    elif key=='relaciones':
        eq([idx('KSI','i'),r('='),summ('j=1','21',[v('s','j'),absval([idx('IEE','ij'),r('−1')])])])
        eq([idx('ICE','j'),r('='),summ('i=1','32',[v('w','i'),absval([idx('IEE','ij'),r('−1')])])])

inline={'xᵢⱼ':('x','ij'),'xᵢ·':('x','i·'),'x·ⱼ':('x','·j'),'x··':('x','··'),
        'sᵢⱼ':('s','ij'),'sⱼ':('s','j'),'qᵢⱼ':('q','ij'),'wᵢ':('w','i')}
rx=re.compile('('+'|'.join(re.escape(k) for k in inline)+')')
def text_runs(p,text):
    for part in rx.split(text):
        if part in inline:
            m=el('oMath');m.append(v(*inline[part]));p._p.append(m)
        else:p.add_run(part)

def hyperlink(p,text,url):
    link=OxmlElement('w:hyperlink');link.set(qn('r:id'),p.part.relate_to(url,RT.HYPERLINK,is_external=True))
    run=OxmlElement('w:r');pr=OxmlElement('w:rPr');col=OxmlElement('w:color');col.set(qn('w:val'),'000000');pr.append(col)
    run.append(pr);t=OxmlElement('w:t');t.text=text;run.append(t);link.append(run);p._p.append(link)

text=(ROOT/'texto/seccion_revisada.md').read_text(encoding='utf-8')
in_refs=False
for block in text.strip().split('\n\n'):
    if block.startswith('# '):
        doc.add_paragraph(block[2:],'Title')
    elif block.startswith('## '):
        title=block[3:];in_refs=title=='Referencias'
        doc.add_paragraph(title,'Heading 1')
    elif block.startswith('[[EQ:'):
        n0=len(doc.paragraphs)
        equation(block[5:-2])
        for p in doc.paragraphs[n0:-1]:p.paragraph_format.keep_with_next=True
    elif block.startswith('[[FIG:'):
        fn,caption=block[6:-2].split('|',1)
        p=doc.add_paragraph(caption,'Caption')
        p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after=Pt(9);p.paragraph_format.line_spacing=1.0
        run=p.add_run();run.add_picture(str(FIG/fn),width=Inches(6.8))
        inline_shape=doc.inline_shapes[-1];inline_shape._inline.docPr.set('descr',caption)
    else:
        p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY
        if in_refs:
            p.alignment=WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.line_spacing=1.0;p.paragraph_format.space_after=Pt(6)
            p.paragraph_format.keep_together=True
            p.paragraph_format.left_indent=Inches(0.22);p.paragraph_format.first_line_indent=Inches(-0.22)
            parts=re.split(r'(https://\S+)',block)
            for part in parts:
                if part.startswith('https://'):hyperlink(p,part,part)
                else:p.add_run(part)
            for run in p.runs:run.font.size=Pt(11)
        else:text_runs(p,block)

footer=sec.footer.paragraphs[0];footer.alignment=WD_ALIGN_PARAGRAPH.CENTER
f=OxmlElement('w:fldSimple');f.set(qn('w:instr'),'PAGE');footer._p.append(f)
footer.style=doc.styles['Normal'];footer.paragraph_format.space_after=Pt(0)
doc.core_properties.title='Medición de la especialización'
doc.core_properties.subject='Capítulo II Estructura productiva y especialización regional'
doc.core_properties.author=''
doc.core_properties.keywords='México, PIBE, especialización, KSI, ICE, IEE'
for root in [doc.element, doc.styles.element]:
    for border in list(root.xpath('.//w:pBdr')):
        border.getparent().remove(border)
doc.save(ROOT/'output/Medicion_de_la_Especializacion.docx')
body=re.sub(r'\[\[.*?\]\]','',text.split('## Referencias')[0])
print('Palabras del cuerpo:',len(body.split()))
print('Ecuaciones:',len(doc.element.xpath('//m:oMathPara')),'Figuras:',len(doc.inline_shapes))
```
<!-- PAPIME:END GENERADOR_DOCX -->

### Apéndice D. Valores originales: `datos/Matriz_original_Indices_Krugman.csv`

Este CSV reproduce los valores de `Indices_Krugman!A1:W34`: primera fila de encabezados, 32 filas estatales y fila nacional. Las columnas B a V contienen el VAB; W conserva el total. Los códigos y rótulos completos son los del Excel. No son valores de IEE ni resultados calculados.

<!-- PAPIME:BEGIN MATRIZ_ORIGINAL -->
```csv
Entidad federativa,"11 - Agricultura, cría y explotación de animales, aprovechamiento forestal, pesca y caza",21-1 - Minería petrolera,21-2 - Minería no petrolera,"22 - Generación, transmisión, distribución y comercialización de energía eléctrica, suministro de agua y de gas natural por ductos al consumidor final",23 - Construcción,31-33 - Industrias manufactureras,43 - Comercio al por mayor,46 - Comercio al por menor,"48-49 - Transportes, correos y almacenamiento",51 - Información en medios masivos,52 - Servicios financieros y de seguros,53 - Servicios inmobiliarios y de alquiler de bienes muebles e intangibles,"54 - Servicios profesionales, científicos y técnicos",55 - Corporativos,"56 - Servicios de apoyo a los negocios y manejo de residuos, y servicios de remediación",61 - Servicios educativos,62 - Servicios de salud y de asistencia social,"71 - Servicios de esparcimiento culturales y deportivos, y otros servicios recreativos",72 - Servicios de alojamiento temporal y de preparación de alimentos y bebidas,81 - Otros servicios excepto actividades gubernamentales,"93 - Actividades legislativas, gubernamentales, de impartición de justicia y de organismos internacionales y extraterritoriales",Total
Aguascalientes,13328.677,0,3522.108,2243.47,16111.79,112236.005,32496.415,24678.605,16995.219,2303.508,7858.262,23336.056,6578.001,0,2718.163,10041.87,8075.854,1817.694,5371.978,5321.187,11891.355,306926.21699999995
Baja California,20113.925,0,1683.7,18088.933,54285.4,334788.712,78947.557,80891.782,48150.817,7439.286,23468.332,74541.372,15792.09,0,6271.128,26520.603,20552.193,10639.411,23965.564,14891.921,26010.595,887043.321
Baja California Sur,7451.246,0,5202.051,6563.798,13038.784,4003.545,16728.27,20754.804,16628.17,1329.509,6615.789,17675.965,3535.839,0,3506.765,6661.423,5770.033,1840.509,26593.889,3725.012,9257.639,176883.03999999998
Campeche,6777.622,284172.073,646.017,1589.354,71948.917,4630.188,9756.379,15660.613,14150.623,1671.02,4532.196,13645.71,5787.511,0,2331.562,6748.912,3909.91,170.19,4894.638,4404.471,7189.386,464617.292
Coahuila de Zaragoza,19245.429,60.209,11736.991,7454.598,48245.364,402373.975,59178.042,64973.924,71650.429,4772.063,18645.71,54520.623,11352.242,236.836,3222.182,21752.484,14670.775,1746.922,19711.252,9134.547,16193.279,860877.876
Colima,8381.079,0,3651.625,7602.327,13160.118,9291.758,23315.587,14825.101,25142.522,1238.336,4170.915,13845.776,2496.093,0,993.141,5821.8,3829.279,287.244,5614.304,2711.197,5873.377,152251.579
Chiapas,25226.273,8224.698,581.703,6716.333,30744.207,24795.851,40476.824,63917.553,18197.826,2940.853,10520.149,48662.454,3330.537,15.894,1788.669,34103.089,16368.464,401.288,6900.706,10278.49,19087.146,373279.0069999999
Chihuahua,56166.695,0,12225.54,14943.403,63674.696,304515.176,93660.703,77865.372,49790.609,9147.587,22657.807,63680.737,11914.565,597.919,4644.626,24115.919,20110.445,1543.911,12346.964,13351.647,23922.308,880876.6289999998
Ciudad de México,1374.693,0,232.107,12630.322,133879.209,195761.301,409532.377,291641.583,417082.156,276551.783,404769.67,404540.201,246299.459,141698.69,88143.124,110394.511,124777.27,38606.408,89152.985,64385.469,208482.423,3659935.740999999
Durango,26815.305,0,20123.906,4704.049,36240.595,61914.869,28727.487,31492.578,18823.17,2140.644,6454.699,27923.914,3504.865,207.371,2377.283,13554.107,7388.455,332.258,2910.103,4545.91,12039.07,312220.6379999999
Guanajuato,42515.39,0,2208.907,14440.918,62590.931,370086.659,133073.132,110517.746,82421.627,7998.225,32476.937,99318.899,13888.746,48.924,4286.321,32210.559,25035.883,3322.817,15950.588,20205.457,29443.363,1102042.029
Guerrero,16780.225,0,5997.544,7697.591,22665.109,10446.364,23242.186,56597.452,26340.796,2621.204,7979.379,43749.987,1908.754,0,1224.584,23039.891,9804.206,886.342,12540.915,6985.348,21062.343,301570.22
Hidalgo,12384.831,0,6043.758,6431.136,49136.058,110106.389,39818.883,52317.934,36181.621,1701.762,10128.135,43087.955,3526.098,0,852.072,20260.36,9083.466,2012.639,7306.425,6859.734,14327.186,431566.442
Jalisco,109217.409,0,6934.879,17957.988,86200.277,411620.59,273141.119,170940.047,125724.459,18924.091,61713.924,186426.826,42080.648,545.161,17104.958,50332.113,36882.643,12044.858,36332.524,40886.007,41121.737,1746132.2580000001
México,26337.91,0,4426.037,25388.353,86481.794,493106.579,221625.405,352165.823,190903.046,13633.972,67634.933,329867.76,34542.233,805.578,12714.595,97620.543,55059.178,7155.765,32885.52,48136.096,83191.111,2183682.231
Michoacán de Ocampo,95564.374,0,6299.217,6558.255,19026.688,75693.286,72887.837,118921.428,40018.488,4269.874,19077.54,66925.89,7111.965,0,3358.177,32140.688,16321.645,1980.854,26458.433,12512.515,26272.578,651399.732
Morelos,9562.627,0,424.908,3499.076,15554.233,55081.463,26045.682,32817.982,15739.603,3247.228,8273.232,32086.872,3649.826,0,981.206,13553.943,8745.687,970.075,3864.357,9241.553,11921.065,255260.61800000002
Nayarit,11268.869,0,1582.675,3001.849,12592.071,7513.905,12298.895,21647.014,5772.752,844.7,4922.217,18958.226,1883.349,0,1971.904,8812.951,5121.271,464.756,16719.501,4371.417,9795.711,149544.03299999997
Nuevo León,9530.773,2380.577,10424.255,22241.241,117561.987,659981.479,195995.108,162438.992,195508.981,42387.79,98235.199,137335.047,52174.624,15329.698,15370.741,58883.037,32610.969,16893.748,24336.371,24868.202,35045.85,1929534.6690000002
Oaxaca,18437.422,0,1334.412,7247.356,85589.55,74178.044,37891.06,64176.408,19697.492,2328.615,9459.407,43245.6,5445.515,0,1175.507,25739.636,8399.835,553.579,14153.015,8735.137,20298.335,448085.925
Puebla,32224.23,1433.886,3482.296,9513.938,61270.322,226247.425,78286.721,114042.561,42892.075,10380.331,23221.486,98705.742,14923.205,510.501,4755.563,39650.455,17950.105,2230.885,18010.915,15439.744,23208.629,838381.0149999999
Querétaro,15321.345,0,4191.933,6516.6,43948.367,198876.111,66514.019,47759.652,36947.876,9765.227,19680.545,45290.376,18491.6,900.991,6011.6,17565.671,11501.635,1010.802,10221.076,9300.669,12679.477,582495.5719999999
Quintana Roo,2832.018,0,66.034,4153.758,59663.61,6209.615,25812.338,40860.77,29171.639,3391.025,14101.289,49674.936,7502.953,71.464,12273.581,9713.483,8347.853,11999.277,52452.507,9376.542,12877.313,360552.00500000006
San Luis Potosí,25602.005,48.973,13718.024,10160.077,24048.214,218083.822,46237.045,42563.737,36442.583,3519.383,12274.373,40518.302,8454.284,9.563,1848.402,19155.663,10145.103,1045.85,7774.128,9357.816,16720.379,547727.726
Sinaloa,45238.23,0,2745.902,8963.151,31108.365,43469.773,82026.452,65809.554,39033.239,3912.622,19906.481,53468.371,11788.573,903.196,5606.527,24427.933,13294.016,2401.736,9275.077,13225.597,17111.701,493716.4959999999
Sonora,48734.235,0,68770.604,18793.688,46174.231,239226.466,74471.558,63795.266,34472.434,7086.101,16732.074,51298.817,11868.89,255.277,6835.158,20945.012,15787.044,1766.665,16504.424,11318.139,19922.887,774758.9700000001
Tabasco,10648.408,280585.441,3489.989,3580.564,42639.547,24201.514,22426.163,48886.24,33850.557,2635.536,8338.966,42120.034,6174.41,7.472,2311.414,16500.974,12094.587,393.372,5222.336,6212.507,15383.213,587703.2440000001
Tamaulipas,16291.821,20743.885,564.558,14140.373,32053.687,234830.32,59701.006,69541.096,84181.171,5586.207,18050.704,58285.288,7617.538,4.116,2584.562,25274.669,17733.581,1084.447,23284.433,11816.691,20990.679,724360.8320000002
Tlaxcala,4352.008,0,518.907,1324.476,5184.574,42023.756,7633.605,21315.3,7544.986,611.423,3076.858,23016.738,1542.5,0,394.72,8213.141,3785.391,135.615,1649.255,2762.989,6906.181,141992.42300000004
Veracruz de Ignacio de la Llave,65792.152,47241.807,5784.156,23154.896,76297.762,166417.48,106368.331,130552.871,94962.765,6272.442,27835.952,127415.504,11606.717,309.425,3122.995,51136.913,26393.255,1886.337,17846.985,23002.768,37176.252,1050577.7650000001
Yucatán,13763.898,0,5437.518,8174.939,38128.543,44867.954,55409.201,58060.55,19857.455,5451.778,13107.036,41490.346,8934.094,25.337,2201.089,14649.403,10564.818,1164.315,18822.174,10680.839,12907.91,383699.197
Zacatecas,18780.727,0,31309.318,1747.403,20586.766,31330.88,22267.786,24765.828,7384.163,1401.993,4727.173,19597.644,1744.602,0,823.526,12194.555,5772.8,289.378,2866.548,3793.688,11017.954,222402.73200000002
Estados Unidos Mexicanos,836061.851,644891.549,245361.579,307224.213,1519831.766,5197911.254,2475993.173,2557196.166,1901661.349,467506.118,1010647.369,2394257.968,587452.326,162483.413,223805.845,881736.311,585887.649,129079.947,571939.89,441839.306,839328.432,23982097.474
```
<!-- PAPIME:END MATRIZ_ORIGINAL -->

### Apéndice E. Lanzador local de R: `scripts/ejecutar_proyecto_local.R`

Debe ejecutarse desde la raíz `PAPIME_Mx`. Cambia cuatro rutas en memoria y evalúa el script vigente; no escribe encima de su código.

<!-- PAPIME:BEGIN LANZADOR_R -->
```r
# Ejecutar desde la raíz de PAPIME_Mx:
# Rscript scripts/ejecutar_proyecto_local.R
# Conserva intacto el script original entregado y cambia sólo sus rutas en memoria.

raiz_proyecto <- normalizePath(getwd(), winslash = "/", mustWork = TRUE)
ruta_codigo <- file.path(raiz_proyecto, "scripts", "Plots_Krugman_2024.R")
if (!file.exists(ruta_codigo)) {
  stop("Ejecuta este archivo desde la carpeta raíz PAPIME_Mx, que contiene scripts, datos y output.")
}
codigo <- readLines(ruta_codigo, encoding = "UTF-8", warn = FALSE)

cambiar_ruta <- function(lineas, variable, valor) {
  patron <- paste0("^", variable, " <- ")
  posicion <- grep(patron, lineas)
  if (length(posicion) != 1L) {
    stop("Se esperaba una sola asignación inicial para ", variable)
  }
  lineas[posicion] <- paste0(variable, " <- ", encodeString(valor, quote = '"'))
  lineas
}

codigo <- cambiar_ruta(codigo, "ruta_excel",
  file.path(raiz_proyecto, "datos", "PIBE_2024_In.xlsx"))
codigo <- cambiar_ruta(codigo, "carpeta_salida",
  file.path(raiz_proyecto, "output", "Figuras_Capitulo_II_Especializacion_2024"))
codigo <- cambiar_ruta(codigo, "carpeta_geografia",
  file.path(raiz_proyecto, "Cartografia_INEGI"))
codigo <- cambiar_ruta(codigo, "ruta_cartografia",
  file.path(raiz_proyecto, "Cartografia_INEGI", "entidades_INEGI.geojson"))

eval(parse(text = codigo, keep.source = FALSE), envir = new.env(parent = globalenv()))
```
<!-- PAPIME:END LANZADOR_R -->

### Apéndice F. Extracción de archivos si únicamente se conserva este MD

El siguiente ejemplo se ejecuta con Python desde la carpeta donde se guardó este MD. Extrae los bloques delimitados y crea la estructura editable. No recupera archivos binarios que no están contenidos en el Markdown.

```python
from pathlib import Path
import re

raiz = Path.cwd()
contexto = raiz / "CONTEXTO_PAPIME_Mx_Especializacion.md"
contenido = contexto.read_text(encoding="utf-8")

destinos = {
    "MANUSCRITO": "texto/seccion_revisada.md",
    "SCRIPT_R": "scripts/Plots_Krugman_2024.R",
    "GENERADOR_DOCX": "scripts/build_doc.py",
    "MATRIZ_ORIGINAL": "datos/Matriz_original_Indices_Krugman.csv",
    "LANZADOR_R": "scripts/ejecutar_proyecto_local.R",
}

for clave, ruta in destinos.items():
    patron = (
        r"(?ms)^<!-- PAPIME:BEGIN " + re.escape(clave)
        + r" -->\n```[^\n]*\n(.*?)\n```\n<!-- PAPIME:END "
        + re.escape(clave) + r" -->$"
    )
    coincidencia = re.search(patron, contenido)
    if coincidencia is None:
        raise RuntimeError("No se encontró el bloque " + clave)
    destino = raiz / ruta
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(coincidencia.group(1) + "\n", encoding="utf-8")
    print(destino)
```

Si el Excel original se perdió, se puede reconstruir una hoja mínima con los valores del CSV mediante `openpyxl`:

```python
from pathlib import Path
import csv
from openpyxl import Workbook

raiz = Path.cwd()
origen = raiz / "datos/Matriz_original_Indices_Krugman.csv"
wb = Workbook()
ws = wb.active
ws.title = "Indices_Krugman"

with origen.open(encoding="utf-8", newline="") as archivo:
    for numero_fila, fila in enumerate(csv.reader(archivo), start=1):
        if numero_fila == 1:
            ws.append(fila)
        else:
            ws.append([fila[0]] + [float(valor) for valor in fila[1:]])

destino = raiz / "datos/PIBE_2024_recuperado_de_MD.xlsx"
wb.save(destino)
print(destino)
```

Esa reconstrucción no es el archivo original: carece de sus fórmulas, de su primera hoja y de los bloques de índices precalculados. Para usarla se debe apuntar `ruta_excel` a `PIBE_2024_recuperado_de_MD.xlsx` en una copia del script o ajustar la ruta del lanzador. El recálculo desde `A1:W34` sigue siendo posible; el bloque informativo de comparación con índices guardados comunicará que no los encontró. No debe presentarse la hoja reconstruida como una nueva descarga oficial del INEGI ni como una copia binaria del Excel del usuario.
