# Planeación final del manual interactivo de Economía Mexicana

Versión reorganizada del 5 de noviembre de 2026. B01 ejecutado por encargo del autor: piloto y preparación verificados, sincronización con GitHub pendiente de acceso. El estado mantenido se encuentra en `seguimiento/ESTADO.md`. Esta versión sustituye la organización anterior por unidades pequeñas y conserva los acuerdos de planeación. B02 no iniciado.

El documento rector es `PAPIME Libro.pdf`, ubicado en la carpeta principal del proyecto. Los resúmenes de PAPIME_Mx y los materiales anteriores sirven como antecedentes. El repositorio de referencia es [postsocratico/papime-crd](https://github.com/postsocratico/papime-crd). La revisión de esta planeación corresponde a su rama main, commit `458257c3d7b69602560cbcaeb89fd0980297ad6b`.

El trabajo se organiza en diez bloques amplios: preparación, un bloque por cada capítulo e integración final. El usuario encarga el bloque y el asistente coordina sus tareas internas hasta obtener un resultado completo y revisable. El alcance de cada bloque se mantiene a través de las sesiones que necesite.

## Resultado previsto

- Un libro web integrado en bookdown, con lectura continua y una presentación basada en el PDF actual.
- Un PDF completo con figuras estáticas de calidad editorial.
- Los capítulos editables en R Markdown, acompañados por una bibliografía común y referencias cruzadas consistentes.
- Los componentes conservados por separado, incluidos scripts, datos preparados, tablas, gráficos interactivos HTML y figuras estáticas.

La integración será progresiva. Cada capítulo se incorporará al libro al quedar revisado; la etapa final resolverá la coherencia del conjunto y comprobará sus entregables.

## Criterios transversales

**Bibliografía.** Cada capítulo combinará literatura seminal y contribuciones posteriores pertinentes, con estudios sobre México y debates necesarios para interpretar sus resultados. La obra de Clemente Ruiz Durán tendrá presencia transversal sustentada en textos concretos. Cada referencia registrará la edición consultada y el argumento al que contribuye; se comprobarán páginas y datos bibliográficos. Los pasajes citados se contrastarán con la obra original siempre que sea accesible. Una fuente inaccesible se registrará como pendiente o se sustituirá por evidencia verificable, sin atribuirle una lectura que no se realizó.

**Redacción.** Se conservará el tono académico y didáctico ya trabajado. Se evitarán los guiones largos, el exceso de dos puntos, las comparaciones formularias del tipo «no es X sino Y» o «no solamente X, también Y», las enumeraciones y párrafos organizados mecánicamente en ternas, las frases introductorias cortas forzadas y las observaciones vacías. La variedad de extensión responderá al desarrollo del argumento. La revisión distinguirá evidencia, interpretación y alcances de los métodos empleados.

**Datos.** Se conservarán la fuente original y su fecha de consulta, junto con periodo, cobertura, unidades y transformaciones. Se distinguirán precios corrientes y constantes, año base, frecuencia, valores faltantes y ceros. Las comparaciones territoriales utilizarán clasificaciones y denominadores compatibles. Los datos tendrán un corte explícito por edición del libro; las actualizaciones serán deliberadas y verificables.

**Diseño editorial.** El PDF actual será la referencia para la composición y el tono visual. La web tendrá un ancho de lectura cómodo, jerarquías tipográficas consistentes, navegación discreta y figuras colocadas junto a la explicación pertinente. La adaptación a pantalla conservará la identidad del libro.

**Gráficos.** La interactividad se concentrará en las figuras. Cada recurso tendrá una vista inicial suficiente para acompañar la lectura y controles pertinentes a su pregunta económica. Se cuidarán las escalas, etiquetas y leyendas, así como los espacios y la continuidad cromática. Las versiones interactivas y estáticas utilizarán los mismos datos preparados. Se preservarán las decisiones ya trabajadas para KSI, ICE e IEE; cualquier cambio metodológico deberá justificarse y registrarse.

**Reproducibilidad y continuidad.** Los cálculos deberán poder ejecutarse desde los archivos conservados, con rutas relativas y dependencias documentadas. Las sesiones dejarán un registro breve del resultado, sus verificaciones y el siguiente trabajo. El guardado será progresivo y las versiones coherentes se registrarán en GitHub.

## Referencias iniciales de diseño y bibliografía

El [manual del BIE de INEGI](https://www.inegi.org.mx/app/indicadores/doc/AyudaBIEv2.pdf) orientará la relación entre gráfica y tabla, la selección geográfica y la exportación. El [SIE de Banco de México](https://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?accion=consultarCuadro&idCuadro=CR354&locale=es&sector=2) servirá de referencia para presentar periodos y unidades, con notas y metadatos accesibles. [Data México](https://www.economia.gob.mx/datamexico/) aportará referencias para explorar y comparar perfiles territoriales. La composición del manual y sus colores se resolverán desde su propia identidad editorial.

La siguiente selección es un punto de partida para la revisión bibliográfica. No representa una bibliografía exhaustiva ni supone que las obras ya hayan sido leídas e incorporadas.

| Capítulo | Núcleo inicial de revisión |
|---|---|
| I | [Bassols Batalla, México: formación de regiones económicas](https://ru.iiec.unam.mx/1563/); [García Martínez, Las regiones de México](https://libros.colmex.mx/tienda/las-regiones-de-mexico-breviario-geografico-e-historico/). |
| II | [Krugman, Increasing Returns and Economic Geography](https://www.princeton.edu/~pkrugman/geography.pdf); [Dávila Flores, coord., Modelos interregionales de insumo producto de la economía mexicana](https://www.cise.uadec.mx/produccionacademica/downloads/LibrosElectronicos/LibroModelosInterregionales.pdf). Se revisará también la edición de Miller y Blair utilizada por el manuscrito. |
| III | [North, Institutions, Institutional Change and Economic Performance](https://www.cambridge.org/core/books/institutions-institutional-change-andeconomic-performance/AAE1E27DF8996E24C5DD07EB79BBA7EE); [Ostrom, Governing the Commons](https://www.cambridge.org/core/books/governing-the-commons/7AB7AE11BADA84409C34815CC288CD79). |
| IV | [Aschauer, Is Public Expenditure Productive?](https://www.sciencedirect.com/science/article/pii/0304393289900470); [Redding y Turner, Transportation Costs and the Spatial Organization of Economic Activity](https://collaborate.princeton.edu/en/publications/transportation-costs-and-the-spatial-organization-of-economic-act/). La revisión incorporará literatura específica de energía. |
| V | [Alonso, Location and Land Use](https://www.degruyterbrill.com/document/doi/10.4159/harvard.9780674730854/html); [Becker, Human Capital](https://www.nber.org/books-and-chapters/human-capital-theoretical-and-empirical-analysis-special-reference-education-first-edition). Se ampliará con estudios mexicanos de vivienda y acceso urbano. |
| VI | [Sen, Inequality Reexamined](https://sen.scholars.harvard.edu/publications/inequality-reexamined); [Del Castillo, La magnitud de la desigualdad en el ingreso y la riqueza en México](https://www.cepal.org/es/publicaciones/39531-la-magnitud-la-desigualdad-ingreso-la-riqueza-mexico-propuesta-calculo). |
| VII | [Georgescu-Roegen, The Entropy Law and the Economic Process](https://www.degruyterbrill.com/document/doi/10.4159/harvard.9780674281653/html); [Rodrik, Industrial Policy for the Twenty-First Century](https://www.hks.harvard.edu/publications/industrial-policy-twenty-first-century). |
| VIII | [Prebisch, El desarrollo económico de la América Latina y algunos de sus principales problemas](https://repositorio.cepal.org/handle/11362/30088); [Hanson, Why Isn't Mexico Rich?](https://pubs.aeaweb.org/doi/abs/10.1257/jel.48.4.987). |

## Organización en diez bloques

Las actividades de cada bloque se ejecutan como un conjunto. Se enlazan la investigación y la elaboración de recursos, verificando los resultados durante el avance. Las operaciones internas se coordinan por el asistente y no requieren que el usuario solicite cada una.

### B01. Preparación editorial y técnica del libro

**Alcance.** Conciliar el inventario local y el repositorio, identificar la versión vigente y registrar insumos faltantes. Establecer la copia local de trabajo y las carpetas del proyecto, preservando los originales. Resolver la arquitectura editorial y la numeración de apartados, junto con la guía de redacción y la matriz bibliográfica inicial.

Construir el esqueleto de bookdown y su plantilla editorial basada en el PDF. Definir el sistema común de gráficos y probar ambas plantillas con el fragmento de especialización existente, incluyendo citas, ecuaciones y un gráfico interactivo con su equivalente estático. Documentar la compilación y las dependencias necesarias.

**Entregable.** Proyecto organizado y reproducible, con un piloto navegable y su PDF. El piloto permitirá revisar la identidad visual y la lectura antes de extenderlas al libro. La matriz bibliográfica orientará la investigación posterior, que se profundizará dentro de cada capítulo.

**Cierre.** El piloto compila en ambos formatos, sus cifras corresponden al cálculo y los archivos de seguimiento permiten retomar el proyecto. Las decisiones metodológicas existentes quedan registradas. Las comprobaciones del piloto se aprovecharán en el capítulo II.

### B02. Capítulo I. Fundamentos históricos y geográficos del territorio mexicano

**Alcance.** Investigar y redactar «Evolución territorial de México». Revisar «Geografía y recursos de una geografía desigual», sus contrastes regionales y la regionalización utilizada, resolviendo las notas pendientes del manuscrito.

Completar el conjunto de figuras F01–F06. Verificar relieve y localización, clasificaciones de clima y suelo, los recursos y sus paneles, así como las comparaciones de agua y población. Preparar conjuntamente los datos compartidos de F03 y F05 y resolver el esquema integrador F06. Elaborar las salidas interactivas pertinentes y sus versiones estáticas, junto con las actividades del capítulo.

**Entregable.** Capítulo I completo en R Markdown e integrado al libro web y al PDF, con bibliografía verificada y recursos individuales conservados.

**Cierre.** La historia territorial y la explicación geográfica forman un argumento continuo. Las figuras coinciden con los datos y la prosa; sus coberturas y clasificaciones son explícitas.

### B03. Capítulo II. Estructura productiva y especialización regional

**Alcance.** Completar la introducción y «Segmentación de la producción» con la literatura pertinente. Extender el piloto de especialización para integrar KSI, ICE e IEE, preservando los criterios metodológicos y visuales ya trabajados, incluida la matriz completa.

Reproducir el modelo nacional de insumo-producto y su explicación, distinguiendo los tratamientos de insumos domésticos y totales cuando corresponda. Recuperar y validar la base regional antes de desarrollar su aplicación y explorador. Revisar «Regiones y el sector externo», verificar unidades y conversiones monetarias y completar sus figuras. Integrar las actividades y revisar el capítulo en su conjunto.

**Entregable.** Capítulo II completo con modelos reproducibles y visualizaciones interactivas, acompañado por las salidas estáticas y sus bases documentadas.

**Cierre.** La aplicación regional tiene una base y método resueltos; las figuras del sector externo utilizan series comparables. Los resultados de especialización conservan las convenciones acordadas. Si falta un insumo decisivo, se avanza en los componentes independientes y se registra exactamente qué impide cerrar el capítulo.

### B04. Capítulo III. Gobernanza y políticas públicas

**Alcance.** Revisar la literatura y delimitar el alcance institucional del capítulo. Desarrollar los conceptos de gobernanza y coordinación territorial, considerando las capacidades de gobierno y sus tensiones. Seleccionar y elaborar un caso mexicano con evidencia documental verificable.

Preparar el recurso didáctico y las actividades que ayuden a analizar el caso. La interactividad se incorporará cuando exista una pregunta que pueda explorarse con datos.

**Entregable.** Capítulo III completo con marco conceptual y caso documentado, integrado en los formatos del libro.

**Cierre.** El análisis identifica actores y mecanismos y distingue los efectos respaldados por evidencia de las interpretaciones propuestas.

### B05. Capítulo IV. Infraestructura e importancia estratégica del transporte y la energía

**Alcance.** Recuperar y validar los insumos viales y energéticos. Reproducir las regresiones y completar la tabla pendiente del manuscrito, revisando sus supuestos y alcances. Preparar las series de tecnologías de generación y comprobar las fuentes geográficas de centrales e infraestructura.

Desarrollar sus mapas y gráficos, incluidas las dispersiones vinculadas con los modelos ya verificados. Completar ubicación, logística y puertos, coordinando los datos compartidos con el capítulo II. Revisar el texto y las actividades e integrar el conjunto.

**Entregable.** Capítulo IV completo con análisis reproducibles y recursos gráficos terminados, tanto interactivos como estáticos.

**Cierre.** Las bases y ubicaciones están comprobadas. La interpretación distingue las asociaciones observadas de las afirmaciones causales que requerirían otro sustento.

### B06. Capítulo V. Ciudad, vivienda y capital humano

**Alcance.** Revisar la bibliografía y establecer las unidades territoriales y los indicadores. Desarrollar el análisis urbano y de vivienda, vinculando el acceso a oportunidades con la organización espacial de las ciudades. Examinar educación y capacidades laborales con una discusión crítica de su medición.

Preparar la evidencia y los recursos comparativos, revisar las actividades y cerrar el capítulo.

**Entregable.** Capítulo V completo con indicadores documentados y visualizaciones pertinentes, integrado al libro web y al PDF.

**Cierre.** Las comparaciones utilizan unidades territoriales compatibles. Las relaciones entre condiciones urbanas y oportunidades de la población están sustentadas.

### B07. Capítulo VI. Desigualdad y diagnóstico territorial

**Alcance.** Revisar los enfoques de desigualdad y formular el método de diagnóstico. Construir la base comparable y resolver las diferencias de cobertura o periodo. Elaborar el análisis territorial y contrastarlo con la literatura.

Preparar los perfiles territoriales y su exploración interactiva, junto con sus versiones estáticas y las actividades del capítulo.

**Entregable.** Capítulo VI completo con diagnóstico reproducible y perfiles regionales trazables a sus datos.

**Cierre.** Las dimensiones e indicadores están justificados. Las limitaciones de comparabilidad y medición se reflejan en la interpretación.

### B08. Capítulo VII. Política Pública y Sustentabilidad

**Alcance.** Revisar la literatura y vincular el diagnóstico territorial con los objetivos de intervención y las restricciones ambientales. Desarrollar los instrumentos de política y sus condiciones de ejecución, considerando capacidades institucionales y coordinación.

Integrar criterios de sustentabilidad y evaluación. Preparar un ejercicio acotado de escenarios y sus actividades, utilizando interactividad si aporta al aprendizaje.

**Entregable.** Capítulo VII completo con propuestas argumentadas y un ejercicio de evaluación o escenarios documentado.

**Cierre.** Los instrumentos responden al diagnóstico. Los escenarios explicitan sus supuestos y se presentan como ejercicios, con las tensiones entre objetivos debidamente discutidas.

### B09. Capítulo VIII. El territorio ante la globalización

**Alcance.** Revisar la literatura y definir los procesos globales que organizarán el capítulo. Analizar la inserción económica de México y sus efectos territoriales, aprovechando la evidencia ya verificada. Examinar estrategias y casos regionales a partir de sus condiciones productivas e institucionales.

Elaborar el recurso de síntesis y las actividades, revisar el texto e integrarlo al argumento del libro.

**Entregable.** Capítulo VIII completo con evidencia y bibliografía verificadas, acompañado por sus recursos gráficos.

**Cierre.** Los casos y las estrategias tienen sustento documental y un alcance temporal explícito. El capítulo enlaza con las conclusiones generales.

### B10. Integración editorial, verificación y entrega

**Alcance.** Revisar el argumento del conjunto, completar la introducción general y las conclusiones y resolver repeticiones o transiciones deficientes. Auditar bibliografía y citas, además de cifras, ecuaciones y referencias cruzadas.

Revisar visualmente el libro web y el PDF. Comprobar controles, enlaces y descargas, así como el uso en pantallas pequeñas, teclado y dispositivos táctiles. Preparar los entregables locales y su versión en GitHub, documentar la reproducción y actualización y publicar en el destino acordado.

**Entregable.** Libro web integrado, PDF final y componentes individuales organizados, con una versión identificable del proyecto y las instrucciones necesarias para mantenerlo.

**Cierre.** Las incidencias de contenido y funcionamiento están resueltas o, cuando dependen de una condición externa, identificadas con precisión. La edición publicada se comprueba en su destino. Este bloque realiza una revisión transversal de capítulos que ya fueron comprobados durante su desarrollo.

Los títulos de los ocho capítulos proceden del PDF actual. Los apartados todavía no desarrollados se organizarán durante el trabajo del capítulo correspondiente.

## Orden de avance y autonomía

La secuencia ordinaria es B01, los capítulos I–VIII y B10. Cada capítulo se incorpora al libro conforme se completa. El piloto de B01 se reutiliza al elaborar B03, los datos del sector externo se coordinan con B05 y el diagnóstico de B07 alimenta B08.

La solicitud de comenzar un bloque autoriza a avanzar sobre todas las tareas comprendidas en él y a resolver las decisiones ordinarias conforme a los acuerdos editoriales vigentes. El asistente coordinará los pasos internos y continuará mientras pueda producir un avance sustancial verificable. Solo consultará cuando sea indispensable una decisión del autor que cambie el contenido, el método o el alcance, y continuará el trabajo independiente mientras espera.

Cada bloque puede abarcar varias sesiones. La sesión se organizará alrededor del mayor resultado coherente que pueda elaborarse y comprobarse con la capacidad disponible. Se guardará el trabajo de forma progresiva. Las tareas pendientes se conservarán dentro del mismo bloque, con una continuación concreta, sin convertirlas en una secuencia de encargos que deba administrar el usuario.

Al terminar un bloque se entregará su resultado para revisión y se indicará el siguiente. El cambio al siguiente bloque dependerá del alcance de la instrucción del usuario. Si una instrucción ya comprende varios bloques, se avanzará dentro de ese alcance sin pedir una nueva autorización para cada operación.

## Organización de los archivos

B01 incorporará este plan al repositorio como `seguimiento/PLAN.md`, que será la versión mantenida durante la ejecución. La copia local prevista estará en `C:\Users\marce\Downloads\PAPIME\papime-crd`, salvo que al inventariar se identifique una copia existente adecuada.

```text
papime-crd/
  referencias/
    manuscrito-base/
    antecedentes/
  libro/
    index.Rmd
    _bookdown.yml
    _output.yml
    capitulos/
    bibliografia.bib
    estilos/
  analisis/
    capitulo-01/ ... capitulo-08/
  datos/
    originales/
    preparados/
      capitulo-01/ ... capitulo-08/
    manifiesto.csv
  assets/
    capitulo-01/ ... capitulo-08/
      figuras-estaticas/
      interactivos/
      tablas/
  seguimiento/
    PLAN.md
    ESTADO.md
    DECISIONES.md
    registro-figuras.csv
    sesiones/
  entregas/
    capitulos/
    web/
    pdf/
```

Los originales se conservarán íntegros. Los datos compartidos tendrán una ubicación común con procedencia documentada; los derivados se identificarán por capítulo. Los archivos grandes tendrán un mecanismo de conservación y distribución adecuado a su tamaño. Se registrarán las dependencias y se separará la configuración local de los archivos publicados.

Cada figura conservará un identificador estable que vincule su fuente, cálculo y ubicación editorial con sus salidas HTML y estática. Los HTML individuales incluirán las dependencias necesarias o indicarán claramente la carpeta que los acompaña.

## Cierre de sesiones y capítulos

Una sesión termina con archivos guardados, fuentes y decisiones relevantes registradas y las comprobaciones realizadas descritas. El registro de estado identifica el bloque activo y el próximo trabajo concreto. El asistente mantendrá estos registros sin requerir que el usuario los redacte o reconstruya.

Un bloque se considerará terminado cuando su entregable esté completo, verificado e integrado donde corresponda. Un capítulo requerirá correspondencia entre las cifras de la prosa y las figuras, referencias completas y lectura comprobada en los formatos aplicables. Los problemas metodológicos que alteren la interpretación deberán resolverse antes del cierre.

Los avances coherentes se conservarán localmente y se registrarán en GitHub. Se informará de cualquier sincronización pendiente. Un insumo faltante limitará el trabajo dependiente de él, y se continuará con las actividades independientes.

Cada entrega resumirá el avance sustancial y enlazará sus archivos. También indicará las comprobaciones realizadas y las cuestiones pendientes que afecten al contenido o a la continuación. Los detalles operativos quedarán en el registro del proyecto.

## Organización recomendada de los chats

Se recomienda iniciar un chat nuevo dentro de este proyecto para la ejecución, conservando esta conversación como antecedente de planeación. Ese chat puede continuar durante varias sesiones y bloques. Al pasar a un capítulo amplio puede abrirse otro si ayuda a mantener el trabajo centrado.

La continuidad descansará en los archivos del proyecto. Al abrir un chat se leerán el plan y el estado, junto con las decisiones y el último cierre pertinente. El asistente comprobará primero qué trabajo está terminado para reutilizarlo. Esta recomendación sigue la práctica de conservar decisiones y evidencias por fases descrita en la [documentación oficial de OpenAI](https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex).

Instrucción de arranque sugerida para el nuevo chat:

> Trabajaremos en el libro PAPIME. Lee `C:\Users\marce\Downloads\PAPIME\PLAN_FINAL_PAPIME.md`, que contiene la planeación vigente en diez bloques. El documento base es `PAPIME Libro.pdf` en esa misma carpeta y el repositorio es `postsocratico/papime-crd`. Comienza el bloque B01 y avanza de forma autónoma sobre todo su alcance, incluyendo la organización del proyecto, las plantillas y el piloto. Conserva los acuerdos bibliográficos, editoriales y metodológicos. Coordina las tareas internas sin pedirme que dirija cada paso. Guarda los avances localmente y en GitHub, comprueba los resultados y actualiza el registro de estado. Si el bloque necesita otra sesión, deja una continuación precisa. Cierra con un resultado sustancial revisable y sus archivos; no comiences B02 hasta que revisemos B01.

Para continuar dentro de un bloque:

> Continúa con el bloque activo desde el estado guardado. Reutiliza lo verificado y avanza hacia su entregable completo, guardando y comprobando los resultados.

Para pasar al siguiente:

> El bloque está revisado. Continúa con el siguiente bloque del plan y coordina sus tareas internas hasta obtener el entregable acordado.

## Uso de las sesiones

Los bloques describen el alcance del trabajo, no una cantidad fija de horas, mensajes o cuota de Plus. Con Sol 6.1 Ultra se mantendrán encargos centrados en resultados amplios y verificables, con delegación de tareas independientes cuando aporte valor. Se reutilizarán cálculos y plantillas y se evitará repetir inventarios o lecturas ya documentadas.

La carga de una sesión se ajustará según los resultados y el consumo observado. El guardado progresivo y los registros permiten reanudar un bloque sin repetir su planificación. Esta organización no requiere que el usuario administre los pasos técnicos ni que abra una conversación por cada tarea.
