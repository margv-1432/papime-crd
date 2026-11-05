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
