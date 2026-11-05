# Guía editorial y sistema común de figuras

B01 fija una plantilla para revisar antes de extenderla al libro. El punto de partida es el PDF rector de 64 páginas. La guía conserva su lectura académica y sus títulos azules; corrige incoherencias de composición propias del borrador.

## Redacción y desarrollo didáctico

La pregunta económica organiza cada sección. La teoría introduce relaciones y conceptos; los datos mexicanos muestran cómo se observan y qué interpretación permiten. La exposición define sus variables antes de utilizarlas y enlaza las figuras con una explicación de su contenido. Las actividades del estudiante deben referirse a conceptos y evidencia ya presentados.

La prosa será formal y continua, con párrafos cuya extensión responda al argumento. Se evitan guiones largos, exceso de dos puntos, aperturas breves forzadas, ternas mecánicas, observaciones vacías y comparaciones formularias del tipo «no es X sino Y» o «no solamente X, también Y». Se revisa su uso en contexto; los títulos o listas necesarios para una comparación no se sustituyen por rodeos.

La evidencia, la interpretación y los alcances del método se distinguen en el desarrollo. Una asociación estimada no acredita por sí misma causalidad. Un cociente de localización no mide productividad ni bienestar. La cautela metodológica se integra a la explicación y evita advertencias hipotéticas repetidas.

## Bibliografía y atribución

Se usa una bibliografía común con claves estables y citas autor-año. Cada entrada registra edición consultada, enlace o identificador, acceso y páginas verificadas. La matriz bibliográfica también señala la contribución concreta al argumento y el capítulo donde se necesita. El estado «localizada» no equivale a «leída»; una referencia inaccesible permanece pendiente o se sustituye con evidencia comprobable.

La obra de Clemente Ruiz Durán tendrá presencia transversal sustentada en textos concretos. Se conserva la distinción del manuscrito entre las ideas atribuidas al autor y la síntesis propia del capítulo. No se distribuyen citas de un mismo texto por todos los capítulos sin comprobar su pertinencia.

Los números de página se cotejan con la obra consultada, distinguiendo la foliación impresa de la posición física de un PDF. Las paráfrasis y las citas literales se revisan por separado. Se mantiene el año de edición, el periodo de los datos y la fecha de consulta como campos distintos.

## Composición basada en el manuscrito

La inspección encontró páginas carta de 612 × 792 puntos, márgenes de texto cercanos a 72 puntos y cuerpo principalmente de 12 puntos. Los títulos usan Calibri de 20 y 16 puntos en azul petróleo. El color extraído es RGB 0.0588, 0.278, 0.38, equivalente aproximado a `#0F4761`. El cuerpo alterna Arial y Calibri y las ecuaciones usan Cambria Math. Esa mezcla procede del borrador y no obliga a conservar fuentes distintas dentro de un mismo nivel.

La plantilla común utiliza una familia sans serif legible, título azul petróleo y cuerpo oscuro sobre fondo blanco. En PDF se conservan tamaño carta, márgenes de una pulgada y cuerpo cercano a 12 puntos. Las ecuaciones mantienen una fuente matemática compatible. En web el ancho de lectura será de aproximadamente 42–46 em, con interlineado de 1.5–1.65 y márgenes adaptables. El texto se alinea a la izquierda en pantallas; se evita la justificación que genere espacios excesivos.

Los títulos conservan jerarquía y espacio suficiente. Cada figura queda junto al pasaje que la explica y su pie incluye contenido, periodo, unidad, fuente y transformaciones relevantes. En PDF se evita separar el rótulo de su figura o dejar páginas casi vacías por saltos manuales heredados. Las tablas largas deben dividirse de forma legible y repetir encabezados cuando sea necesario.

La navegación web es discreta y permite ubicar capítulo y apartado. La página debe poder leerse con teclado y en una pantalla angosta. Los controles tienen nombres visibles; la información económica relevante no depende exclusivamente de pasar el puntero ni del color.

## Datos y notación

Toda base conserva fuente, fecha de consulta cuando esté demostrada, periodo, cobertura, unidad, frecuencia y transformación. Se distingue precio corriente de constante, año base, ausencia de datos y cero observado. Las claves territoriales se tratan como texto cuando sus ceros iniciales son significativos. El corte se fija por edición; no se descarga una serie nueva durante cada compilación.

La notación matemática se mantiene entre prosa, ecuaciones y tablas. Se definen índices territoriales y sectoriales, denominadores y agregaciones. Los porcentajes se distinguen de las proporciones, los puntos porcentuales y los índices sin unidad. Los redondeos se aplican a la presentación, con la precisión completa conservada para calcular.

## Acuerdos metodológicos de especialización

| Elemento | Convención conservada |
|---|---|
| Base | Matriz recibida de 2024, millones de pesos de 2018 |
| Cobertura | 32 entidades, 21 actividades; minería petrolera y no petrolera separadas |
| Denominadores | Sumas sectoriales del VAB, sin añadir impuestos netos de subsidios del PIB |
| KSI | Suma de diferencias absolutas de participaciones sectoriales, sin dividir entre dos; escala general 0–2 |
| ICE | Suma de diferencias absolutas de participaciones territoriales, sin dividir entre dos; 21 resultados sectoriales |
| IEE | Cociente de localización del VAB, 672 combinaciones; referencia nacional igual a 1 |
| Referencia territorial | País completo, incluyendo la entidad comparada |
| Ceros y faltantes | Ceros observados conservados; faltantes detienen el cálculo |
| Comparabilidad | Misma cobertura sectorial y base de precios para las comparaciones |

El KSI mide distancia respecto de la estructura nacional; un valor bajo no demuestra diversificación absoluta. El ICE utiliza el peso económico estatal como referencia y no representa un reparto idéntico entre entidades. No se construye un mapa con un supuesto ICE estatal. El IEE no tiene máximo universal de dos.

## Sistema común de gráficos

Las salidas estáticas e interactivas consumen los mismos datos preparados. Cada figura cuenta con identificador estable, pregunta económica, unidad, fuente y script reproducible. La vista inicial permite leer el resultado sin operar controles. La interacción se concentra en la figura y responde a una pregunta concreta, con tabla o descarga cuando facilita examinar los valores.

La familia cromática de especialización se conserva. El mapa de calor muestra la matriz completa 32 × 21, sin números dentro de las celdas. El mapa de calor y los mapas de IEE comparten un degradado continuo de azul a rojo oscuro y una barra horizontal inferior. La transformación del color es `log(1 + IEE)`; las etiquetas de la barra muestran el índice original. La unidad nacional recibe un tono claro. Los ceros conservan el extremo azul.

La paleta antecedente del IEE usa `#244A73`, `#7DA5BD`, `#F4F0EA`, `#DDB1A8`, `#C4787C`, `#A44759` y `#681D32` según los puntos de la escala documentados por el script vigente. No debe reconstituirse el sistema con una escala automática distinta por figura. El mapa KSI utiliza la misma familia con su propia escala 0–2. Los gráficos de barras conservan el orden y la jerarquía necesarios para comparar las entidades.

Los cinco mapas antecedentes son independientes: un mapa KSI y cuatro de IEE. Señalan las cinco entidades con mayor índice. Sus figuras de IEE usan escala común y límites comparables. B01 puede probar un recurso de ese sistema; B03 integra la matriz y los mapas completos sin perder estos acuerdos.

Los ejes, unidades y leyendas deben ser legibles al tamaño de inserción. Las escalas se eligen según el significado del indicador y se explican si son transformadas. El color se complementa con rótulos, orden y acceso a valores. Las versiones HTML individuales deben incluir sus dependencias o una carpeta claramente vinculada y funcionar desde las rutas de entrega.

## Verificación y continuidad

Antes de entregar se comprueban cálculo, cifras del texto, rótulos, citas y referencias cruzadas. Se compilan web y PDF desde los archivos guardados. Se revisa visualmente el PDF y el navegador, incluyendo pantallas angostas y operación básica por teclado. Se prueba que las descargas correspondan a la tabla usada por la figura.

Las decisiones y cambios de método se registran en `seguimiento/DECISIONES.md`. Cada sesión deja resultado, comprobaciones y continuación en seguimiento. La aceptación de B01 corresponde a la revisión del piloto; B02 no comienza durante su preparación.
