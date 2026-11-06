# Verificación B02 web

6 de noviembre de 2026. Edición vigente conforme a D25–D28, en el fork [margv-1432/papime-crd](https://github.com/margv-1432/papime-crd), rama `b02-capitulo-i`, [PR #1](https://github.com/margv-1432/papime-crd/pull/1).

La compilación HTML completa terminó correctamente con `Rscript scripts/compilar.R web`. El directorio activo contiene las cuatro páginas de lectura y una página 404, recursos y dependencias locales. No contiene PDF. Los documentos históricos y el manuscrito rector siguen conservados con sus hashes; el comprobante de las 29 copias retiradas es [limpieza-entrega-web-B02.json](limpieza-entrega-web-B02.json).

| Comprobación | Resultado | Registro |
|---|---:|---|
| Integración y preservación | 37/37 | [verificacion-proyecto-B02-web.json](verificacion-proyecto-B02-web.json) |
| Libro y exploradores integrados | 59/59 | [verificacion-web-B02-funcional.json](verificacion-web-B02-funcional.json) |
| F01/F02 | 38/38 | [verificacion-fisico-web-B02.json](verificacion-fisico-web-B02.json) |
| F04 | 37/37 | [verificacion-recursos-web-B02.json](verificacion-recursos-web-B02.json) |
| F03/F05/F06 | 51/51 | [verificacion-agua-mecanismos-web-B02.json](verificacion-agua-mecanismos-web-B02.json) |

Las cinco suites mantenidas suman 222 comprobaciones correctas. Los siete controles dirigidos de F06 a 390 px se conservan en [verificacion-F06-controles-390-B02.json](verificacion-F06-controles-390-B02.json).

El navegador verificó selecciones persistentes, comparación múltiple, búsqueda, capas/categorías, tabla y detalle, reset, teclado, toque y exportaciones contrastadas con las bases. Se revisaron escritorio, pantallas de 360/390 px y el ancho de inserción del libro. Los seis iframes contienen toda su página sin recortes, y los HTML individuales funcionan mediante archivo local. No hubo errores JavaScript, solicitudes externas o fallos de red.

La narrativa del capítulo I previa a las actividades coincide exactamente con el checkpoint de partida. Las 30 claves citadas y sus localizadores permanecen resueltos, la bibliografía se conserva y el piloto mantiene ecuaciones y expresiones de cálculo. Las bases cuantitativas y las fuentes/entregas históricas están intactas; sólo se añadió la geometría estatal de dibujo y se actualizó el manifiesto.

Las capturas de QA están en `tmp/qa-web-B02-funcional`, `tmp/qa-fisico-web`, `tmp/qa-recursos-web-B02` y `tmp/qa-agua-web-B02`. El [informe funcional](REVISION_FUNCIONAL_WEB_B02.md) describe las mejoras y sus coberturas. Los comprobantes anteriores de PDF permanecen como historia de aquellas entregas y no forman parte de la verificación vigente.
