# Sistema común de gráficos

Versión B01, 5 de noviembre de 2026.

Cada figura responde a una pregunta económica y conserva un identificador F estable en el registro. La etiqueta editorial (por ejemplo II.2.1) depende de su ubicación; el identificador F07-KSI conserva la unión entre dato, cálculo y salidas. Los archivos se nombran F07-ksi para compatibilidad entre sistemas.

El piloto consulta los 32 resultados KSI y presenta una escala fija de 0 a 2, con barras azul petróleo #0F4761, texto Arial y números legibles. El orden inicial es descendente y la selección destaca una entidad sin ocultar las demás. La tabla completa y la descarga CSV son parte del mismo recurso. El HTML individual no requiere una conexión ni bibliotecas externas. El libro conserva sus bibliotecas junto a las páginas.

Las figuras interactivas y estáticas se generan a partir del mismo CSV preparado. El script R vuelve a calcular ese CSV desde la matriz original y contrasta sus resultados con los antecedentes. La cifra mostrada puede redondearse; el cálculo conserva toda su precisión. La selección de una entidad modifica solamente su destaque visual.

Los mapas de KSI y de IEE y la matriz completa conservan sus convenciones registradas en METODO_ESPECIALIZACION.md y GUIA_EDITORIAL.md. La matriz de IEE mantiene 672 celdas sin cifras internas y el color usa log(1+IEE), con leyenda inferior en valores originales. Los mapas del IEE comparten escala y destacan cinco entidades. El piloto de barras no sustituye esos recursos.

Para un recurso nuevo se documentarán fuente original, fecha de consulta real, periodo, cobertura, precios, unidad, ceros, faltantes y transformaciones en datos/manifiesto.csv. Se comprobarán controles con teclado, pantalla pequeña, vínculos, tabla y lectura inicial. El equivalente estático debe sostener el argumento del PDF sin depender de los controles. Las figuras junto a sus explicaciones tendrán leyendas y notas legibles al tamaño final de página.
