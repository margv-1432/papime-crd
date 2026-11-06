# Revisión de estilo de los recursos B02

6 de noviembre de 2026. Se revisaron el capítulo I, la guía editorial vigente y las notas de preparación de F01–F06. La intervención se concentra en los textos que explican la lectura de los recursos y en los pies del libro.

## Cambios

- En `generar_fisico.R`, las notas de F01 relacionan la red vial con la lectura de conexiones y con la información de viajes que exigiría estudiar accesibilidad. F02 explica la evaluación de aptitud para un uso y manejo definidos, y desarrolla el significado de N a partir del diccionario documentado. Se conservan las categorías R/r/N, la discordancia separada, los filtros viales y las fechas de cada capa.
- En `preparar_agua_sintesis.py`, las notas de F03 precisan el carácter medio del recurso y la correspondencia por identificador entre el cuadro de 2022 y la cartografía de referencia 2023. F05 explica qué conserva el selector y cómo se leen las diferencias entre participaciones. Se mantienen los denominadores de 461 640 hm³/año y 129.35 millones de habitantes.
- En F06 se reescribieron los detalles de los nodos como explicaciones de los mecanismos, con menos enumeraciones y metacomentarios. La advertencia repetida tras cada selección se retiró; el pie del esquema concentra el alcance interpretativo de las flechas. Se conserva la atribución como síntesis propia, con las mismas referencias de apoyo, nueve nodos y diez relaciones.
- En `preparar_F04.py`, las notas acompañan la lectura de cada panel. Permanecen explícitos los faltantes de cobre y el cero de Jalisco, la inclusión de plantaciones en la producción maderable y la diferencia entre 304 731 t de acuacultura publicadas para el país y 304 732 t al sumar los estados. La explicación del directorio minero excluido se conserva en el panel correspondiente.
- En `figuras-capitulo-I.csv` se revisaron los seis pies. Las unidades sectoriales de F04 y los denominadores de F05 quedan recuperables en el pie; se retiraron negaciones sobre usos ajenos a la comparación presentada.

Los controles, las leyendas, las categorías y los títulos mantienen su formulación funcional. Los cambios se hicieron en los generadores y se propagaron mediante la compilación a estáticas, interactivos y CSV de nodos F06. En la lectura final, los detalles de F06 se afinaron con ejemplos de transporte, agua, extracción y manejo comunitario ya desarrollados en el capítulo. No se editaron manualmente HTML finales ni tablas de cálculo.

## Comprobaciones y continuación

La sintaxis de ambos scripts Python y del script R es correcta. Al sustituir las cadenas por un marcador común, los árboles de sintaxis de los tres archivos coinciden con el checkpoint anterior a la revisión: las expresiones de cálculo y control permanecen iguales. Las etiquetas y los atributos HTML de los generadores también coinciden. El CSV de pies conserva seis filas válidas y los mismos identificadores, anclas y títulos.

Se midieron con Arial las notas fijas modificadas de los generadores Python y caben en el ancho disponible. Los textos explicativos nuevos del HTML conservan el flujo adaptable de sus contenedores. Tras regenerar los recursos se revisaron las páginas PDF y vistas web, incluidos los pies de F04/F05 y la lectura móvil.

La entrega integrada pasó 40 comprobaciones de proyecto, 39 de navegador y 17 de preservación y consistencia. Se actualizaron los detalles preparados de F06 y las copias de descarga; sus identificadores, etiquetas y tipos permanecen iguales. El manifiesto registra el nuevo hash textual. No se detectaron impedimentos técnicos ni decisiones adicionales pendientes.
