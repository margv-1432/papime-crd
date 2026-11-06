# Reproducir la edición B02

La compilación utiliza datos preparados congelados y funciona sin red. Desde la raíz del repositorio, ejecutar `Rscript scripts/compilar.R todo` o `Rscript scripts/compilar_B02.R todo`. Los modos `pdf` y `web` limitan los formatos. Se generan el capítulo I independiente, el avance integrado con el piloto anterior y los recursos individuales. No se cambia la matriz de especialización de B01.

El entorno local utiliza R 4.6.1 con bookdown/rmarkdown, sf, terra, jsonlite y base64enc; Python 3 con pypdf, pdfplumber, reportlab, openpyxl, Pillow y pypdfium2; Pandoc y XeLaTeX; Poppler para las salidas de agua. Se reutilizan las bibliotecas instaladas. `PAPIME_PYTHON` permite seleccionar Python y `PAPIME_R_LIBRARY` otra biblioteca de R. El script conserva las rutas detectadas en esta computadora como alternativas, sin distribuir esas dependencias. La sesión final de R queda en `compilacion-B02-sessionInfo.txt` y las versiones geoespaciales en la auditoría geométrica.

## Preparación y fuentes

`preparar_agua_sintesis.py`, `preparar_F04.py` y `generar_fisico.R` regeneran las seis figuras desde las entradas pequeñas conservadas. El cálculo comparte una sola tabla entre F03 y F05. Los pies del libro se mantienen en `libro/figuras-capitulo-I.csv`; ese archivo es la fuente única de sus rótulos editoriales.

La reconstrucción completa de las capas físicas es una operación distinta de compilar. Requiere recuperar los originales identificados por URL, tamaño y SHA256 en `datos/originales/geografia/fuentes-F01-F02.csv`. Los grandes ZIP están en `.local/B02-originales`, fuera de Git. Con ellos presentes se ejecutan `preparar_localidades.py`, `preparar_fisico.R` y `preparar_caminos.R`, seguidos por `auditar_fisico.py` y `auditar_geometria_fisica.R`. Los SHP antecedentes de estados y provincias recibidos permanecen fuera del repositorio, en `../Mexicana_Tarea_3`; los GPKG preparados necesarios para compilar sí se distribuyen. Para reconstruir desde un clon sin esa carpeta, recuperar MG2020 y las provincias del productor y ajustar únicamente las rutas de esas dos entradas documentadas.

F04 conserva la consulta de cubierta vegetal, sus 183 correspondencias y su máscara MG2020. La máscara se regenera con `recortar_cobertura_F04.R`; la figura ordinaria utiliza la versión congelada. Los anuarios completos SGM y CONAPESCA se consultaron en `tmp/fuentes/F04`; se distribuyen extractos numéricos propios y sus hashes, no sus gráficos originales. El extracto de cuatro páginas de CONAGUA conserva las condiciones de reproducción no lucrativa y atribución de la publicación. Los detalles de consulta y transformación están en las notas por figura.

## Comprobar

`python scripts/verificar_B02.py` comprueba cifras, citas, enlaces, integridad y correspondencia entre salidas. `node scripts/verificar_web_B02.cjs` abre Chrome mediante Playwright y un servidor temporal local. Las pruebas individuales de agua y F04 están en `analisis/capitulo-01/verificar_agua_sintesis.cjs` y `verificar_F04.cjs`. Las capturas temporales se conservan en `tmp/qa-web-B02`; la revisión del PDF queda en `VERIFICACION_B02.md`.

El piloto anterior conserva fuentes y configuración en `index-B01.Rmd`, `_bookdown-B01.yml` y `scripts/compilar_B01.R`, que compila a carpetas separadas. Los registros de su auditoría original y su PDF de entrega permanecen conservados. La edición B02 no incorpora contenidos nuevos de B03.
