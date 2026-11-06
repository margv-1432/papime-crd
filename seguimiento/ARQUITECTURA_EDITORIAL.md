# Edición web vigente y revisión transversal

Instrucción del autor del 6 de noviembre de 2026, registrada en D25–D28: la salida de trabajo y entrega es el manual web y sus figuras HTML. Los PDF existentes son antecedentes; el PDF rector conserva su función de fuente y referencia editorial. No se exige generar ni revisar nuevos PDF ni equivalentes estáticos para ellos. Se retirarán las actividades finales del capítulo I y sus enlaces y no se crearán actividades, cuestionarios o tareas en los capítulos siguientes. El argumento y sus ejemplos se desarrollan en la exposición y las figuras.

La revisión funcional de B02 retira las actividades y refuerza F01–F06 con selección persistente por clic/toque, consulta coordinada y comparación de elementos compatibles, restablecimiento y descarga de datos. La cobertura real rige cada selección: estados cuando existen datos estatales, RHA en F03/F05 y nodos y relaciones documentados en F06. F02 utiliza las entidades como contexto de localización de sus categorías nacionales. La compilación vigente usa `_bookdown-web.yml` y conserva los rótulos del capítulo y sus fuentes. B03 parte de esa revisión web y conserva el resto del contenido aceptado. Las descripciones del piloto y de las entregas anteriores que siguen son antecedentes históricos y no reintroducen requisitos PDF.

# Integración B02

El autor aceptó B01 y autorizó el capítulo I. B02 incorpora su texto completo y F01–F06 al libro. El piloto de II.2 sigue identificado como fragmento previo; los demás capítulos permanecen fuera de compilación. Los rótulos del capítulo I se mantienen en figuras-capitulo-I.csv. Las decisiones de arquitectura de B01 que siguen son el antecedente conservado.

La revisión del 6 de noviembre de 2026 aplica la prioridad narrativa de D23–D24 al capítulo, sus recursos, la presentación y el piloto ya integrado. La guía editorial rige también las futuras incorporaciones: cada sección desarrolla su argumento con un ritmo propio, y la revisión continua en contexto acompaña las comprobaciones de datos y formatos. La jerarquía de títulos y los componentes técnicos de esta arquitectura organizan el libro sin imponer una fórmula de párrafo.

# Arquitectura editorial del libro

Decisiones de B01, 5 de noviembre de 2026. El PDF rector fija los ocho capítulos y su orden. La estructura se implementa progresivamente; reservar un archivo de capítulo no significa haber redactado o validado su contenido. B01 termina en el piloto de especialización y espera revisión antes de B02.

## Orden del conjunto

| Orden | Título del PDF | Archivo editorial previsto | Bloque |
|---|---|---|---|
| Preliminar | Presentación e introducción general | `libro/index.Rmd` | B01 y cierre B10 |
| I | Fundamentos históricos y geográficos del territorio mexicano | `libro/capitulos/01-territorio.Rmd` | B02 |
| II | Estructura productiva y especialización regional | `libro/capitulos/02-estructura-productiva.Rmd` | B03 |
| III | Gobernanza y políticas públicas | `libro/capitulos/03-gobernanza.Rmd` | B04 |
| IV | Infraestructura e importancia estratégica del transporte y la energía | `libro/capitulos/04-infraestructura.Rmd` | B05 |
| V | Ciudad, vivienda y capital humano | `libro/capitulos/05-ciudad.Rmd` | B06 |
| VI | Desigualdad y diagnóstico territorial | `libro/capitulos/06-desigualdad.Rmd` | B07 |
| VII | Política Pública y Sustentabilidad | `libro/capitulos/07-sustentabilidad.Rmd` | B08 |
| VIII | El territorio ante la globalización | `libro/capitulos/08-globalizacion.Rmd` | B09 |
| Cierre | Conclusiones | `libro/capitulos/09-conclusiones.Rmd` | B10 |
| Referencias | Bibliografía común | `libro/bibliografia.bib` y sección final | Progresiva |

Los nombres de archivo son estables y carecen de acentos. La presentación al lector conserva los títulos españoles. Los capítulos se muestran con números romanos I–VIII; conclusiones y bibliografía quedan sin número de capítulo. Las introducciones internas pueden quedar sin número. No se crean capítulos ficticios para forzar el número del piloto.

## Jerarquía y numeración

Un encabezado de primer nivel representa el capítulo. El segundo nivel representa el apartado, por ejemplo II.2 Medición de la especialización. El tercer nivel organiza el desarrollo del apartado, por ejemplo II.2.1 La matriz de actividad económica. La numeración depende de la estructura editorial. En el piloto aislado se usa `number_sections: false`: el número editorial se escribe una sola vez en cada título visible y los encabezados llevan anclas semánticas. Así se conserva II.2 sin introducir un capítulo I ficticio. El esqueleto de los demás capítulos queda fuera de la compilación del piloto.

El PDF presenta en I.2 una introducción seguida por apartados numerados 2, 3, 4 y 5, con una numeración que se confunde con la del nivel superior. La reserva editorial para B02 es la siguiente; se confirmará al trabajar el capítulo sin alterar ahora su contenido.

| Identificador | Apartado |
|---|---|
| I.1 | Evolución territorial de México |
| I.2 | Geografía y recursos de una geografía desigual |
| I.2.1 | Introducción |
| I.2.2 | Relieve y localización |
| I.2.3 | Climas, agua y suelos |
| I.2.4 | Recursos naturales y aprovechamiento regional |
| I.2.5 | Cierre integrador |

Se conservan II.1 Segmentación de la producción, II.2 Medición de la especialización, II.3 Cadenas de valor regionales y II.4 Regiones y el sector externo. `3. 1 Una introducción al modelo de insumo-producto` pasa a II.3.1 cuando se integre B03. No se asignan subapartados definitivos a capítulos aún no desarrollados.

Las figuras conservan la convención capítulo.apartado.secuencia ya utilizada en especialización, por ejemplo figura II.2.1. Tablas y ecuaciones utilizan identificadores propios con la misma ubicación editorial cuando requieren referencia. El número visible puede cambiar al integrar contenido; el identificador técnico estable no cambia. El piloto enlaza figuras y ecuaciones mediante anclas y conserva rótulos explícitos, incluida la figura II.2.1 y las ecuaciones II.2.1 en adelante. Cada rótulo tiene una fuente única en el archivo editorial, sin añadir después un segundo número automático. Los enlaces y números se verifican en la edición web vigente. Al integrar el libro, cualquier automatización debe respetar la misma tabla de correspondencias.

## Identificadores y componentes

F01–F06 se reservan para las figuras del capítulo I que identifica el plan. El piloto KSI conserva el identificador estable `F07-KSI` y su rótulo editorial de figura II.2.1. El registro de figuras vincula cada identificador con fuente, periodo, script, datos preparados y salida HTML; las estáticas existentes se identifican como antecedentes. No se recicla un identificador para una pregunta distinta. F08–F17 identifican las diez figuras restantes de especialización según la correspondencia verificable de la guía antecedente. F18 queda sin asignar; los once archivos de especialización incluyen al propio F07-KSI.

`datos/originales` conserva las entradas sin edición. `datos/preparados/capitulo-XX` guarda las tablas usadas efectivamente por los gráficos y el texto. `analisis/capitulo-XX` contiene las transformaciones y comprobaciones. `assets/capitulo-XX` separa las figuras estáticas, interactivos y tablas. Los HTML individuales se entregan con sus dependencias o de forma autocontenida y deben funcionar sin rutas de la computadora del autor.

Las carpetas heredadas del commit base permanecen disponibles como fuentes. Su conservación evita romper scripts históricos. La nueva arquitectura documenta su relación con los derivados mediante manifiestos; no implica mover o sobrescribir datos originales por razones de orden visual.

## Piloto de B01, antecedente completado

El piloto selecciona y recorta un fragmento de II.2 para probar el argumento, citas, notación, ecuaciones, referencias y gráficos en web y PDF. Incluye la matriz conceptual, KSI y una síntesis de ICE e IEE. Omite del recorrido la matriz de calor y los mapas sectoriales, que se conservan como antecedentes. La apertura se cotejó con el PDF rector; se ajustó la notación errónea de actividad `x_j` en p.19 a `j`. Las referencias originales de Krugman y BLS explicitan que su variable es empleo, frente a la adaptación al VAB del piloto. Mantiene su ubicación conceptual en el capítulo II. La selección se identifica al lector como piloto editorial y no pretende presentar como terminado el capítulo.

La introducción del piloto explica su pregunta económica y permite llegar a la figura sin contenido de capítulos inconclusos. La vista inicial del gráfico ofrece una comparación suficiente. Sus controles amplían la exploración de los mismos datos preparados; el PDF presenta el equivalente estático y una nota que informa la unidad y la referencia nacional. Se conserva la convención KSI sin factor un medio.

La aceptación de la identidad editorial precede la extensión al capítulo I. Las reservas de capítulos y las tareas pendientes permanecen en seguimiento, sin notas operativas insertadas como si fueran prosa del libro.

## Criterio de integración posterior

Cada capítulo se integra cuando su texto, cifras, referencias y recursos han sido comprobados. La compilación debe permitir distinguir el piloto, los capítulos revisados y las reservas. B10 unifica introducción, conclusiones, transiciones y bibliografía sin repetir mecánicamente el trabajo de verificación ya realizado.
