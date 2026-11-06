# F04 · Revisión funcional web de B02

6 de noviembre de 2026. Aplicación de D25–D28 sobre las tablas y la cubierta congeladas. El generador vigente de HTML es `analisis/capitulo-01/generar_recursos_web.py`, acompañado por las plantillas `recursos_web.html`, `recursos_web.css` y `recursos_web.js`; las tres se incrustan en el HTML autónomo. El generador histórico y sus salidas estáticas se conservan como antecedentes.

## Exploración implementada

Los paneles de cobre, madera y pesca ofrecen un mapa de las 32 entidades y un gráfico de barras, con selección persistente por clic, toque, Enter o espacio. La búsqueda acota el selector de entidades y permite construir comparaciones múltiples. El cambio de panel conserva la selección territorial, y el mapa, las barras, la tabla y el detalle reflejan las mismas entidades. Los colores y las barras mantienen la referencia nacional de su panel. También se puede acercar el mapa a la selección y recuperar su encuadre completo.

La tabla conserva todos los campos y la precisión de las bases preparadas. La descarga CSV reúne exactamente sus filas y su orden actuales. Los guiones publicados, las ausencias de fila y los ceros explícitos tienen representación y detalle diferentes. En pesca permanecen el total sectorial, la acuacultura incluida y la diferencia de redondeo de 1 t entre total nacional publicado y suma estatal.

En cubierta se puede ampliar y desplazar el raster conservado, seleccionar varias categorías y buscar por clave, formación o descripción. La selección de categorías coordina el catálogo de 183 claves y el detalle; el mapa nacional mantiene su representación completa. La vista estatal separada aporta localización contextual. Esta separación respeta sus distintas proyecciones y evita producir áreas o clasificaciones estatales a partir de colores mezclados del raster. Las tablas exportadas siguen siendo las correspondencias nacionales originales.

El restablecimiento recupera el panel inicial, las 32 entidades, el encuadre, el orden y las categorías completas. Los controles principales tienen áreas de al menos 44 px; el documento se adapta a 360 px y el desplazamiento de gráficos y tablas queda dentro de sus contenedores. Los cambios de altura se notifican al libro mediante `papime:resize`.

## Comprobaciones

`scripts/verificar_recursos_web_B02.cjs` pasó **37/37** pruebas en Chrome real con Playwright. El informe es `seguimiento/verificacion-recursos-web-B02.json`. Se cotejaron las cuatro tablas contra las bases de disco, el caso Sonora de 550 597.50 t, el cero de Jalisco, el faltante de Ciudad de México, los decimales maderables y los totales pesqueros. Las exportaciones se descargaron y analizaron, incluidas comparaciones múltiples y subconjuntos de categorías. Se probaron reset, encuadre, búsqueda sin resultados, teclado, toque y descarga móvil. A 800 px, mapa y gráfico se apilan para la inserción en el manual; a 1440 px se presentan juntos. No se registraron errores JavaScript ni peticiones externas.

Se revisaron capturas de escritorio y de selección, mapa y categorías a 360 px, conservadas temporalmente en `tmp/qa-recursos-web-B02`. Las bases cuantitativas, el catálogo preparado, el raster y las figuras estáticas no se modificaron. La geometría estatal de dibujo se comparte con F01/F02 a través de `estados-web.json`. La integración final del manual y su publicación corresponden al cierre de B02.
