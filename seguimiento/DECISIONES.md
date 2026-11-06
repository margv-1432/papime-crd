# Registro de decisiones

## Revisión narrativa transversal. 6 de noviembre de 2026

| ID | Decisión y fundamento | Alcance |
|---|---|---|
| D23 | El autor establece como prioridad editorial absoluta una narrativa natural, continua y variada, propia de un manual interactivo. Se revisan pasajes completos para superar la cadencia de oraciones cortas, las frases genéricas sobre objetos y funciones, las aclaraciones negativas ajenas al argumento y las estructuras repetidas como listados. | Aplicación transversal al capítulo I, presentación, fragmento ya existente de II.2, actividades y textos de recursos, y a los capítulos futuros. La guía, el plan y la plantilla incorporan esta prioridad; la revisión se comprueba en web y PDF. No se desarrollan contenidos nuevos de B03. |
| D24 | Las precisiones necesarias de método y fuente se integran a la interpretación o se documentan en pies y notas, según su función. Se conserva la información que permite reconstruir unidades, fechas, clasificaciones, denominadores y faltantes. | La revisión modifica la exposición y su distribución, con cálculos, cortes, controles, citas y acuerdos bibliográficos conservados. Los originales y entregas históricas permanecen como antecedentes. La aceptación narrativa requiere lectura editorial del conjunto, sin imponer una longitud uniforme ni una fórmula de párrafo. |

## Instrucción permanente de publicación. 6 de noviembre de 2026

| ID | Decisión y fundamento | Alcance |
|---|---|---|
| D22 | El autor reafirma que toda publicación debe realizarse en el fork `margv-1432/papime-crd`. El original `postsocratico/papime-crd` se utiliza sólo como referencia de consulta. | Aplica a todos los bloques y futuras conversaciones, incluidos commits, ramas y base de los PR. Comprobar el propietario del repositorio antes de escribir. B02 y su PR #1 ya pertenecen al fork. La restricción previa sobre `main` corresponde al `main` del fork y no autoriza cambiar de destino. |

## B01 5 de noviembre de 2026

| ID | Decisión y fundamento | Alcance |
|---|---|---|
| D01 | El PDF raíz de 64 páginas es el manuscrito rector. Se preservan su copia y la variante DOCX de la raíz; el PDF anterior de 35 páginas y la sección editable se conservan como antecedentes. Los hashes están en el inventario. | Ningún original se sobrescribe. |
| D02 | Se conserva el commit recibido 458257c y sus carpetas de datos. La arquitectura nueva añade libro, análisis, datos preparados, recursos, entregas y seguimiento. | Los scripts heredados mantienen sus rutas de entrada hasta su revisión por capítulo. |
| D03 | El piloto adapta un fragmento de II.2, con el primer párrafo del PDF vigente y una selección didáctica sobre KSI, ICE e IEE. Se corrige la notación errónea de la actividad j en la extracción del manuscrito. | Prueba editorial; no sustituye toda la sección ni declara terminado B03. |
| D04 | Se conservan 32 entidades, 21 actividades, minería separada, VAB de 2024 a precios de 2018 y denominadores por suma de actividades. KSI e ICE no se dividen entre dos. | Comprobación independiente de 672 IEE, 32 KSI y 21 ICE. |
| D05 | El gráfico del piloto es F07-KSI, con rótulo II.2.1. Rótulos editoriales explícitos y anclas semánticas evitan introducir capítulos ficticios. Cada rótulo visible tiene una sola fuente. | La integración posterior conservará la correspondencia entre ID y ubicación. |
| D06 | Azul petróleo #0F4761 y Arial/Calibri proceden del PDF. La lectura web utiliza ancho limitado y la interactividad se concentra en figuras. | Las escalas y paletas de los mapas y matriz IEE existentes quedan conservadas para B03. |
| D07 | La matriz original permanece congelada. Su fecha original de descarga no está documentada; la verificación de B01 y la consulta de fichas oficiales se registran por separado. | No se atribuye una descarga nueva ni se mezclan revisiones del PIBE. |
| D08 | Las citas de Krugman 2010 p.12 y BLS 2011 p.2 se contrastaron con originales. Se distingue su variable empleo de la aplicación al VAB. | Las demás obras están en la matriz con estados de acceso y lectura. No se presume lectura de originales inaccesibles. |
| D09 | El piloto se compila con bookdown a HTML y PDF desde los mismos Rmd. Los datos y figura se vuelven a generar; las cifras empíricas del texto se enlazan al cálculo y se comprueban. | El HTML individual no requiere servicios externos. MathJax y Fuse se distribuyen con sus licencias en la web. |
| D10 | La revisión de B01 precede el trabajo del capítulo I. Los archivos reservados de capítulos quedan fuera de la compilación del piloto. | B02 no iniciado. |
| D11 | Git conserva bytes exactos de originales y antecedentes mediante atributos específicos. Los CSV mantienen sus finales de línea, también al clonar; los hashes del manifiesto se refieren al archivo efectivo. | Evita que la normalización de texto altere los originales recibidos. |
| D12 | La conexión existente rechazó escritura con 403 y Git no tiene credenciales. Se preservan commits y bundle locales sin afirmar sincronización. | Retomar el guardado remoto al habilitar acceso, sin forzar ramas ni iniciar B02. |
| D13 | El autor autorizó crear un fork para organizar y publicar las entregas. B01 se publica en [margv-1432/papime-crd](https://github.com/margv-1432/papime-crd), commit inicial `576d2680750ea24f72b2c24c8481357384a58f2d`, como instantánea del árbol `e44bea84bcf4310213e78dd8734b1d7c4fcc7988` del checkpoint local `7ebcd33`, sobre `458257c`. | Resuelve el impedimento de D12; conserva originales, historia base y checkpoints locales. No cambia método, datos ni figuras. B01 entregado a revisión; B02 no iniciado. |

## B02. 5 de noviembre de 2026

| ID | Decisión y fundamento | Alcance |
|---|---|---|
| D14 | El autor dio B01 por terminado y autorizó expresamente B02. Se desarrolla y comprueba el capítulo I completo; no se inicia B03. | Sustituye la espera de D10 para este bloque. |
| D15 | La regionalización se define por pregunta y unidad de fuente: provincias, localidades, categorías ambientales, RHA y entidades. Centro/frontera es un contraste histórico de manufacturas; no una agregación estadística nueva. | Resuelve la nota del curso sin inventar una regionalización universal ni repartir PIB entre RHA. |
| D16 | Se recuperan los mismos cortes de las capas físicas del manuscrito. Los exportadores anteriores sirven como contraste; los originales y sus cálculos se verifican de nuevo. Los grandes ZIP quedan locales con URL y SHA256, y los derivados portátiles permiten compilar sin red. | F01/F02: CEM3.0 archivo20170619, ITER2020, RNC2025, clima2008 y suelo2024 observado2002–2006. |
| D17 | R y r se distinguen en suelo. Una discordancia entre código R y descripción GRAVOSA se conserva como dato inconsistente; N se rotula «sin fase registrada». | No se imputan categorías ni se construye aptitud o rentabilidad. |
| D18 | F03/F05 comparten las trece filas oficiales de CONAGUA, corte2022, publicadas marzo2024. Porcentajes sobre461640hm³/año y129.35millones, a partir de valores publicados redondeados. Cartografía RHA2023 sólo de referencia. | Sin identidad geométrica supuesta, intersecciones o PIB asignado. Brechas descriptivas, sin índice de déficit o bienestar. |
| D19 | F04 conserva cobertura SerieVII y producción2023 por sector. Distingue cero, guion y ausencia; acuacultura es parte del total. Se mantiene diferencia de redondeo de1t. | Producción no sustituye ocurrencias ni reservas; se excluyen puntos de directorios sin localización física certificada. Cuatro paneles, con estáticas individuales y compuesto. |
| D20 | El PDF bajo la ficha Bassols1979 corresponde a segunda edición revisada1983/reimpresión1992; se cita bassols1992 y se omite su ISBN impreso con checksum inconsistente. Ruiz1997pp433–434 y1999pp13–15 se cotejan con originales. | La matriz distingue pasajes leídos y resúmenes originales Hanson; García2008 permanece candidata inaccesible, sustituida aquí por García2004 consultado. |
| D21 | F06 es síntesis propia con nueve nodos y diez relaciones documentadas; flechas interpretativas, sin coeficientes causales. Los rótulos del capítulo tienen fuente única en figuras-capitulo-I.csv. | Integración web/PDF y actividades; se conserva el piloto B01 sin modificar su método. |

Los cambios de método, corte, regionalización o alcance requieren una justificación explícita en este registro. Las decisiones ordinarias de composición y organización se ejecutan dentro de la autonomía autorizada por el plan.
