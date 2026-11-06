# Estado del proyecto PAPIME

## Edición vigente: B02 web

6 de noviembre de 2026. **Revisión D25–D28 implementada y comprobada.** El capítulo I conserva la narrativa y las citas de la revisión anterior, con su cierre natural y sin el apartado I.3, sus seis consignas ni enlaces residuales. B01 aceptado; B03 no iniciado.

La entrega activa es el manual HTML y sus seis exploradores. El flujo habitual `Rscript scripts/compilar.R web` genera únicamente recursos web y compila en `libro/_book-web`. La web activa no contiene PDF. Se retiraron 29 copias de PDF y estáticas después de comprobar su conservación; los documentos históricos, el PDF rector, las fuentes y las estáticas canónicas permanecen intactos.

## Destino permanente

**Todo se publica exclusivamente en el fork [margv-1432/papime-crd](https://github.com/margv-1432/papime-crd)**, rama [b02-capitulo-i](https://github.com/margv-1432/papime-crd/tree/b02-capitulo-i), [PR #1 del propio fork](https://github.com/margv-1432/papime-crd/pull/1). El original `postsocratico/papime-crd` es sólo de consulta y no recibe cambios ni PR. `origin` apunta al fork; `upstream` al original. Esta instrucción D22 continúa vigente entre conversaciones y bloques. En el conector, usar `repository_full_name: margv-1432/papime-crd`.

La revisión se conserva también en `C:\Users\marce\Downloads\PAPIME\papime-crd`. Los comprobantes de publicación identifican los commits y árboles locales/remotos de cada entrega; las historias pueden tener SHA distintos y árboles de contenido iguales.

## Resultado funcional

F01 permite comparar entidades y localidades censales, conservar la selección en el mapa y la tabla, controlar capas, acercarse y exportar las filas mostradas. Sus sumas corresponden al conjunto de localidades representadas, con el umbral censal conservado.

F02 incorpora selección estatal de contexto, comparación y búsqueda de categorías, consulta por píxel de la rejilla de dibujo, capas y tabla de correspondencias paginada/exportable. Las categorías conservan su alcance nacional y R/r/N y la discordancia permanecen diferenciados.

F03/F05 permiten seleccionar y comparar varias RHA con buscador, mapa o gráfico, detalle y tabla coordinados. Mantienen 461 640 hm³/año y 129.35 millones como denominadores nacionales. F04 coordina selección de las 32 entidades, mapa, barras, tabla, detalle y descargas en sus paneles cuantitativos, distinguiendo cero, guion y ausencia de fila; la cubierta se explora con su raster y catálogo nacional.

F06 ofrece selección de nueve nodos y diez relaciones, conexiones vecinas, detalle y referencias, tabla y descarga. Su vista móvil vertical mantiene la exploración del esquema. Los seis HTML son autónomos y notifican su altura al libro para conservar la lectura continua.

## Verificaciones

- Integración y preservación: 37/37.
- Libro y HTML individuales en Chrome real: 59/59, con escritorio, móvil táctil, teclado, archivos locales e iframes completos.
- F01/F02: 38/38; F04: 37/37; F03/F05/F06: 51/51, con valores y CSV contrastados contra las bases preparadas.
- Total de las cinco suites mantenidas: 222 comprobaciones correctas. Se conservaron además siete controles dirigidos de disposición y toque de F06 a 390 px.
- Sin errores JavaScript, solicitudes externas o fallos de red en las pruebas. Citas, ecuaciones y expresiones R del piloto conservadas.
- Datos cuantitativos, bibliografía, originales y PDF históricos intactos. Se añadió únicamente geometría estatal de dibujo a los preparados y se actualizó su manifiesto.

El [informe funcional](REVISION_FUNCIONAL_WEB_B02.md), la [verificación](VERIFICACION_B02.md) y los JSON correspondientes documentan el alcance real. Las comprobaciones anteriores de PDF son antecedentes y no requisitos de esta edición.

## Continuidad

No quedan decisiones adicionales ni tareas independientes pendientes de esta solicitud. Corresponde la lectura del autor sobre `entregas/web/index.html` y los seis HTML de `assets/capitulo-01/interactivos`. Las limitaciones de cobertura conservadas se explican en cada recurso y en el informe.

Para ajustes posteriores: leer plan, estado, decisiones, guía y arquitectura; partir del generador web de la figura o de `libro/capitulos/01-territorio.Rmd`; compilar HTML y repetir las pruebas pertinentes. Mantener la prioridad absoluta de narrativa natural y variada, sin actividades finales ni nuevas entregas PDF. Las fuentes, cortes y acuerdos bibliográficos sobre Ruiz Durán y literatura seminal permanecen vigentes. B03 requiere una instrucción posterior cuyo alcance lo comprenda.
