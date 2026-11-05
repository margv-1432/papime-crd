# Reproducción y actualización del proyecto

Este documento describe cómo reconstruir el piloto B01 desde los insumos conservados. La compilación y la revisión de sus resultados son operaciones distintas. El cierre y las comprobaciones finales se consignan en `ESTADO.md` y en el registro de la sesión correspondiente; este documento no certifica por sí solo una compilación terminada.

## Entorno y dependencias

| Componente | Entorno detectado o función |
|---|---|
| R | 4.6.1. En esta computadora, `C:/Program Files/R/R-4.6.1/bin/Rscript.exe`. |
| bookdown | 0.48. Integra los archivos R Markdown y genera GitBook y PDF. |
| rmarkdown | 2.32. Coordina el procesamiento mediante knitr y Pandoc. |
| Pandoc | Incluido en RStudio. El script busca `C:/Program Files/RStudio/resources/app/bin/quarto/bin/tools/pandoc.exe` cuando no existe una configuración explícita. |
| XeLaTeX | Instalación TinyTeX del usuario. En Windows el script puede añadir `APPDATA/TinyTeX/bin/windows` al entorno del proceso. |
| Python 3 y openpyxl | Auditoría independiente de la matriz y sus valores en el Excel original. La generación del libro se ejecuta con R. |
| MathJax | 3.2.2, componente TeX a SVG conservado en el proyecto. Permite componer las ecuaciones sin un CDN. |
| Fuse.js | 6.4.6, biblioteca de búsqueda de GitBook conservada con la entrega. |

`scripts/instalar_dependencias.R` crea o utiliza la biblioteca `.local/R` y resuelve los paquetes faltantes. La biblioteca está excluida de Git y no debe copiarse a las entregas. Los paquetes ya disponibles en otras bibliotecas de R pueden utilizarse; por ello es necesario conservar también el registro de sesión y examinar qué versiones se cargaron realmente.

El instalador utiliza el repositorio de CRAN configurado en el script y puede requerir conexión a Internet. No instala R, RStudio, Pandoc ni la distribución TeX. Tampoco garantiza que CRAN entregue en el futuro las mismas versiones. Después de compilar, `seguimiento/dependencias-R.csv` registra los paquetes presentes en `.local/R`, mientras que `seguimiento/compilacion-sessionInfo.txt` identifica R, plataforma, bibliotecas y paquetes cargados. Si se requiere reconstruir exactamente una edición, se deben obtener las versiones registradas y cotejar los resultados, en vez de asumir que una instalación nueva coincide.

En una computadora distinta se puede utilizar `Rscript` disponible en su entorno. Si Pandoc está en otra ubicación, se configura `RSTUDIO_PANDOC` antes de compilar; XeLaTeX debe estar disponible en la ruta de búsqueda de programas. Las rutas particulares detectadas son ayudas de esta instalación. Los insumos, scripts y vínculos entre componentes del proyecto utilizan rutas relativas al repositorio.

## Instalación y compilación

Desde la raíz del repositorio en PowerShell:

```powershell
& 'C:\Program Files\R\R-4.6.1\bin\Rscript.exe' scripts/instalar_dependencias.R
& 'C:\Program Files\R\R-4.6.1\bin\Rscript.exe' scripts/compilar.R todo
```

Se puede sustituir `todo` por `web` o `pdf`. `compilar.R` localiza la raíz a partir de su propio archivo, configura la biblioteca del proyecto, prepara los datos, genera el interactivo y llama a bookdown. En el modo completo, genera primero el PDF y después la web. No descarga ni actualiza la matriz durante esta operación.

El libro se define en `libro/_bookdown.yml`, con el orden de lectura explícito. Las opciones de HTML y PDF se encuentran en `libro/_output.yml`. Los estilos de pantalla y el preámbulo de XeLaTeX están en `libro/estilos/`. Los capítulos y la bibliografía común se conservan en UTF-8. La opción `split_bib: false` mantiene la bibliografía reunida al final de la web y evita repetirla en cada archivo de capítulo. Después de compilar, debe comprobarse que ese comportamiento coincida con las páginas generadas.

Las dependencias de lectura de la web también se versionan. MathJax 3.2.2 se conserva en `libro/estilos/vendor/mathjax-3.2.2/`, con `tex-svg.js` y su archivo `LICENSE` de Apache 2.0. La entrega utiliza `recursos/tex-svg.js` y `recursos/LICENSE-MathJax.txt`. La selección de salida SVG evita depender de la descarga de fuentes matemáticas. Fuse.js 6.4.6, utilizado por la búsqueda de GitBook, se conserva en `libro/estilos/vendor/fuse-6.4.6/`, con `fuse.min.js` y su licencia Apache 2.0; la entrega utiliza `recursos/fuse.min.js` y `recursos/LICENSE-Fuse.txt`. La licencia de esta versión se comprobó en el encabezado del archivo y en el [original de la etiqueta v6.4.6](https://raw.githubusercontent.com/krisk/Fuse/v6.4.6/LICENSE). Los archivos y sus licencias forman parte del versionado del proyecto y deben acompañar las copias distribuidas.

La configuración del piloto utiliza estos recursos locales, sin un CDN para MathJax ni para Fuse.js. La revisión web debe comprobar que las ecuaciones y la búsqueda funcionan con los archivos conservados y sin solicitudes a esos servicios externos. Cambiar una versión requiere registrar la procedencia del nuevo archivo, conservar su licencia y repetir ambas pruebas.

El comportamiento de composición y la selección de formatos siguen la documentación oficial de bookdown sobre [uso](https://pkg.yihui.org/bookdown/usage) y [formatos de salida](https://pkg.yihui.org/bookdown/output-formats). Se utilizan `bookdown::gitbook` y `bookdown::pdf_book`. La numeración visible del piloto responde a la arquitectura editorial registrada; no se cambia el número de capítulo por compilar solo un fragmento.

## Recorrido de los datos y las figuras

La matriz fuente de especialización se conserva en `datos/originales/especializacion/`. El Excel es el original recibido, y `Matriz_original_Indices_Krugman.csv` representa la tabla de valores utilizada por el cálculo. La auditoría debe comprobar su correspondencia con `Indices_Krugman!A1:W34`; una exportación CSV no reemplaza las fórmulas ni las demás hojas del libro Excel.

`analisis/capitulo-02/preparar_especializacion.R` calcula los índices desde el CSV original. Emite los datos preparados y las tablas, con la figura `F07-ksi` en PNG y PDF. Las tablas heredadas se utilizan para contraste y no como entrada de los cálculos. El script verifica dimensiones, códigos, orden de entidades, totales, participaciones, límites e identidades algebraicas. La sensibilidad a reunir la minería petrolera y no petrolera se conserva como comprobación; la edición utiliza las 21 actividades acordadas.

`analisis/capitulo-02/generar_interactivo.R` prepara la figura HTML individual a partir de los datos preparados. La versión web y la figura estática deben compartir cifras, unidades y referencias. Las dependencias del HTML y las descargas incluidas deben verificarse con la carpeta de entrega completa.

La auditoría con Python y openpyxl ofrece un contraste independiente con el Excel. Se ejecuta desde la raíz del repositorio, después de generar los datos preparados:

```powershell
python -m pip install openpyxl==3.1.5
python analisis/capitulo-02/auditar_especializacion.py
```

La instalación solo es necesaria si ese paquete no está disponible en el entorno de auditoría. Los resultados y tolerancias se guardan en `seguimiento/auditoria-especializacion.json` y su tabla CSV. Un resultado aprobado en R no reemplaza ese contraste, ni el contraste numérico reemplaza la inspección visual del PDF y de los controles del interactivo. El alcance de la revisión visual se confirma en el registro de la sesión, además del resultado numérico.

Los originales estadísticos del repositorio anteriores a B01 permanecen conservados. Su existencia no los convierte automáticamente en la base vigente de una figura: cada recurso debe enlazar el insumo elegido con su cálculo y sus salidas mediante el manifiesto y el registro de figuras.

## Archivos que se entregan para revisión

| Ruta | Uso |
|---|---|
| `entregas/web/index.html` | Entrada del piloto navegable. Se distribuye junto con toda `entregas/web`. |
| `entregas/pdf/PAPIME-B01-piloto.pdf` | Lectura y revisión de la composición estática. |
| `libro/` | Fuente editable común de las dos versiones. |
| `assets/capitulo-02/` | Figuras, interactivo y tablas individuales. |
| `datos/preparados/capitulo-02/` | Cifras utilizadas por los recursos del piloto. |
| `seguimiento/` | Estado, decisiones, comprobaciones y continuación. |

La carpeta `libro/_book` es una salida intermedia. `compilar.R` copia los resultados a `entregas/` y añade los recursos de consulta y descarga. Al reconstruir una edición, debe comprobarse que esas copias corresponden a la compilación vigente y que no quedan archivos obsoletos ajenos al orden actual del libro.

Para revisar mediante un servidor local, desde la raíz:

```powershell
python -m http.server 8765 --bind 127.0.0.1 --directory entregas/web
```

Se abre `http://127.0.0.1:8765/` y se detiene el servidor con `Ctrl+C`. Es suficiente para la revisión en la propia computadora. La publicación en un servicio de alojamiento se realiza en el destino acordado por el autor; guardar archivos en GitHub no equivale a publicar una web operativa.

## Comprobación antes del cierre

La sesión debe registrar el resultado de compilar ambos formatos, las verificaciones numéricas, la inspección de las páginas del PDF y la prueba de navegación, ecuaciones, citas, controles y descargas de la web. Las cifras citadas en la prosa se contrastan con los datos preparados antes del redondeo de presentación. Las citas deben resolver sus claves y conservar el alcance y las páginas realmente consultadas.

Las decisiones KSI, ICE e IEE permanecen en el registro metodológico. No se introducen factores de normalización, nuevas actividades, periodos ni cambios de precios como solución a un problema de compilación. Una modificación metodológica requiere justificación y registro explícitos.

El registro de estado identificará también la versión guardada en GitHub y cualquier sincronización pendiente. B01 se entrega para revisión de la identidad editorial y la lectura. El capítulo I comienza después de esa revisión, conforme al alcance autorizado.

## Actualización deliberada de una edición

La actualización de datos es una operación editorial separada. Se elige y registra el nuevo corte, se conserva el original anterior y se incorpora una copia identificable del nuevo insumo con fuente, consulta, cobertura, periodo, frecuencia, unidades, precios y hash. Se documentan las revisiones de clasificación y las diferencias entre ceros y faltantes antes de recalcular.

Los derivados se regeneran desde la nueva fuente. Se comparan cifras, ordenamientos e identidades con la edición anterior y se explican las diferencias relevantes. También se revisan la prosa, las notas de figura y las actividades que dependan de ellas. Una fecha nueva de consulta bibliográfica no altera por sí sola el año de los datos.

La matriz bibliográfica se actualiza después de consultar la edición y el pasaje utilizados. Una ficha editorial comprobada no debe marcarse como obra leída; los pendientes de acceso siguen visibles. Al cambiar de edición se coteja la paginación y se conserva la trazabilidad de la sustitución.

El cierre de la actualización requiere las mismas comprobaciones de lectura y funcionamiento, archivos de estado actualizados y una versión identificable en GitHub. Este protocolo conserva los cálculos y la evidencia de cada edición sin modificar silenciosamente los originales.
