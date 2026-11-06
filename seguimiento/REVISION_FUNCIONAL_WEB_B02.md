# Revisión funcional del manual web B02

6 de noviembre de 2026. Aplicación de D25–D28 sobre la última revisión narrativa. Destino exclusivo: [fork margv-1432/papime-crd](https://github.com/margv-1432/papime-crd), rama `b02-capitulo-i`, [PR #1](https://github.com/margv-1432/papime-crd/pull/1).

## Capítulo y flujo de entrega

Se retiró I.3 con sus seis consignas. La comparación con el checkpoint anterior confirma que toda la narrativa del capítulo que precedía a ese apartado permanece igual; su último párrafo ya enlaza naturalmente con el capítulo II. Se actualizaron índice, navegación y búsqueda al recompilar. La presentación describe la exploración web y el fragmento previo de especialización conserva cifras y fórmulas, con su cierre expositivo y el enlace al HTML individual.

La compilación habitual produce HTML desde los generadores nuevos y bookdown. El directorio de salida es `libro/_book-web`; la copia a entrega filtra también subdirectorios para excluir PDF. Se retiraron 29 copias históricas de PDF/estáticas de la web activa, comprobando antes sus hashes y rutas conservadas. Los archivos canónicos históricos y el PDF rector permanecen intactos. La limpieza queda registrada en `limpieza-entrega-web-B02.json`.

Los exploradores se integran con altura adaptable y acceso a ventana completa junto al rótulo. El libro conserva tipografía, color y ancho de lectura, mientras cada figura ajusta controles y vistas a la pantalla.

## Mejoras por figura

| Recurso | Exploración y coordinación |
|---|---|
| F01 | Selección múltiple de estados y localidades por mapa, listas y tabla; buscadores, marcas y detalle persistentes, capas de relieve/poblamiento, acercamiento y CSV de las localidades mostradas. Las áreas de los círculos mantienen proporcionalidad con la población; el objetivo táctil transparente es independiente. |
| F02 | Estados como contexto geográfico; categorías climáticas y de suelo seleccionables y comparables, control de visibilidad, búsqueda de códigos/descripciones, consulta por píxel de dibujo, tabla paginada y CSV filtrado o de página. Conserva R/r/N y discordancia. |
| F03 | Selección múltiple de las 13 RHA, mapa, detalle y tabla coordinados; búsqueda, variable agua/población, símbolos proporcionales, límites y claves controlables, reset y exportación visible. |
| F04 | Cuatro paneles con selección estatal persistente, búsqueda y comparación, mapa, barras, tabla y detalle, encuadre y CSV exacto. El mapa distingue ceros y faltantes. La cubierta conserva el raster nacional ampliable y un catálogo filtrable por categorías y texto. |
| F05 | Comparación de RHA en barras con escala común fija, series controlables, orden de comparación, búsqueda, multiselección, detalle y tabla sincronizados; CSV con el mismo orden y precisión de las filas visibles. |
| F06 | Nodos y flechas seleccionables, búsqueda, incorporación de vecinos, tabla de relaciones y referencias, reset y exportación de relaciones mostradas. En móvil se ofrece una vista vertical legible; los controles se ajustaron también a 390 px. |

Los controles tienen nombres visibles, foco y alternativas de selección por teclado. La selección funciona con clic o toque simple. Las [referencias de interacción](REFERENCIAS_INTERACCION_B02.md) documentan la consulta del BIE, SIE y Data México y su adaptación a la identidad del manual.

## Datos y alcance conservados

F03/F05 mantienen RHA y los denominadores nacionales de 461 640 hm³/año y 129.35 millones de habitantes. Las selecciones reúnen filas compatibles y conservan sus participaciones. F01 suma las localidades censales representadas en la selección; F02 utiliza las entidades para situar categorías nacionales. La cubierta F04 y su catálogo tienen alcance nacional, mientras los registros productivos conservan su cobertura por entidad y sector.

Se mantienen cortes, unidades, clasificaciones y precisión de los preparados. Los ceros, guiones y filas ausentes siguen diferenciados; la acuacultura forma parte del total sectorial y se conserva la diferencia de redondeo de 1 t. F06 mantiene sus nueve nodos, diez relaciones, textos y referencias documentadas. La geometría estatal de dibujo se deriva del GPKG congelado y se comparte mediante `estados-web.json`, con generalización para visualización.

La bibliografía, las citas y los acuerdos sobre Clemente Ruiz Durán y literatura seminal permanecen conservados. Los ejemplos se integran en la exposición y las figuras; el manual no añade tareas finales.

## Comprobaciones y resultado

| Suite mantenida | Correctas |
|---|---:|
| Integración HTML, narrativa, fuentes y datos | 37/37 |
| Libro integrado, iframes, móvil, toque, teclado y archivos locales | 59/59 |
| F01/F02 contra bases preparadas | 38/38 |
| F04 contra bases preparadas | 37/37 |
| F03/F05/F06 contra bases preparadas | 51/51 |
| Total | 222/222 |

Se descargaron y analizaron CSV completos y filtrados, incluyendo comparaciones y ordenaciones; los informes registran los cotejos reales con los archivos preparados. Las pruebas de Chrome no registraron errores JavaScript, recursos externos o fallos de red. Se comprobó que los seis iframes muestran todo el documento en escritorio y móvil, y que los HTML funcionan al abrirlos como archivos locales. Se revisaron capturas de la composición y los controles. Siete comprobaciones dirigidas adicionales verifican la disposición final de F06 a 390 px.

Los informes JSON y las instrucciones están enlazados desde [VERIFICACION_B02.md](VERIFICACION_B02.md) y [REPRODUCIBILIDAD_B02.md](REPRODUCIBILIDAD_B02.md). No surgieron decisiones de contenido, método o alcance que requieran consulta adicional. Queda la nueva lectura del autor; B03 no se ha iniciado.
