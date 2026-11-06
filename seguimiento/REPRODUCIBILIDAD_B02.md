# Reproducir B02 web

La edición vigente se rige por D25–D28. Desde la raíz se ejecuta `Rscript scripts/compilar.R web`; sin argumento también compila la web y `todo` se conserva como alias de esa misma entrega HTML.

El flujo genera F01–F06 desde los derivados congelados, compila el libro en `libro/_book-web` y copia a `entregas/web` únicamente el manual, los HTML individuales, las tablas y sus dependencias locales. La salida del libro se configura en `_bookdown-web.yml` y `_output.yml`. Los PDF históricos permanecen en `entregas/pdf` y las figuras estáticas anteriores en sus carpetas de assets. La limpieza de la entrega activa comprueba el hash de cada copia retirada y documenta su conservación en `limpieza-entrega-web-B02.json`; una copia histórica única se guarda primero en `entregas/antecedentes`.

## Entorno

Se utiliza R 4.6.1 con bookdown/rmarkdown, sf, terra, jsonlite y base64enc, junto con Pandoc y Python 3. Los generadores HTML nuevos usan los datos locales y las bibliotecas ordinarias de Python; la edición web no necesita XeLaTeX ni herramientas de composición PDF. `PAPIME_PYTHON` permite seleccionar el intérprete y `PAPIME_R_LIBRARY` otra biblioteca R. Para las comprobaciones se utilizan Node, Playwright y Chrome. La sesión R efectiva queda en `compilacion-B02-sessionInfo.txt`.

El script conserva como alternativa la ruta del runtime disponible en esta computadora. Las dependencias instaladas no se distribuyen. El manual incluye las copias locales de MathJax y Fuse con sus licencias.

## Generadores y fuentes

- `analisis/capitulo-01/generar_fisico_web.R`: F01/F02 y geometría estatal de contexto `estados-web.json`, a partir de GPKG y rásteres congelados. El argumento `--geometria` prepara sólo esa geometría.
- `analisis/capitulo-01/generar_recursos_web.py`: F04; incrusta sus plantillas HTML/CSS/JS, tablas estatales, catálogo de cubierta y raster conservado.
- `analisis/capitulo-01/generar_agua_mecanismos_web.py`: F03/F05/F06 a partir de la tabla común de agua, geometría RHA, nodos y relaciones documentados.

Los HTML canónicos están en `assets/capitulo-01/interactivos` y son autónomos. Se copian byte por byte a `entregas/web/recursos`. Los pies del manual se mantienen en `libro/figuras-capitulo-I.csv`. Los generadores históricos se conservan como antecedentes y quedan fuera de la compilación ordinaria.

La reconstrucción de las fuentes geoespaciales originales es distinta de la compilación. Los ZIP grandes siguen identificados por URL, tamaño y SHA256 en `datos/originales/geografia/fuentes-F01-F02.csv` y se conservan en `.local/B02-originales`. Los antecedentes SHP recibidos están en `../Mexicana_Tarea_3`; el clon incluye los GPKG y demás derivados necesarios para producir el manual sin esa carpeta. Las notas por figura explican las consultas, escalas, cortes y transformaciones anteriores.

## Comprobar

`python scripts/verificar_B02.py` valida la integración HTML, enlaces, citas, retiro de actividades, narrativa conservada, datos y documentos históricos. Guarda `verificacion-proyecto-B02-web.json`.

`node scripts/verificar_web_B02.cjs` prueba el libro integrado y los HTML individuales con navegador real, incluyendo navegación, búsqueda, adaptación de iframes, escritorio, toque, teclado y archivos locales. Guarda `verificacion-web-B02-funcional.json`. Las pruebas por familia de figuras contrastan selecciones y exportaciones con las bases preparadas; sus nombres y resultados efectivos se registran en el informe funcional.

Las capturas de comprobación quedan en `tmp`, fuera de Git. El informe y el estado enlazan los resultados mantenidos. Los verificadores y comprobantes de las entregas PDF anteriores permanecen como antecedentes; sus cantidades de páginas y pruebas describen aquellas ediciones.

## Entrega y continuidad

La carpeta completa `entregas/web` puede descargarse y abrirse por `index.html`; cada figura también puede abrirse por separado. La reproducción y lectura ordinarias funcionan con archivos locales y sin consultas de datos a servicios externos. La publicación se realiza exclusivamente en `margv-1432/papime-crd`, rama B02 y PR del propio fork. B03 no forma parte de esta revisión.
