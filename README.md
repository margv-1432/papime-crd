# Manual interactivo de economía mexicana

Proyecto PAPIME organizado para desarrollar el libro web y su edición en PDF a partir del manuscrito conservado. B01 prepara la arquitectura editorial, las fuentes, las plantillas y un piloto de medición de la especialización. El resultado se revisará antes de comenzar el capítulo I. El estado de compilación y las comprobaciones vigentes se registran en [seguimiento/ESTADO.md](seguimiento/ESTADO.md).

## Revisar el piloto

La entrega web se abre desde [entregas/web/index.html](entregas/web/index.html). Es necesario conservar la carpeta `entregas/web` completa para que funcionen las ecuaciones, los estilos, la navegación y sus recursos. El gráfico permite explorar los mismos datos preparados utilizados por la figura estática.

La versión de lectura e impresión está en [entregas/pdf/PAPIME-B01-piloto.pdf](entregas/pdf/PAPIME-B01-piloto.pdf). El piloto local está compilado y verificado. Su estado de sincronización con GitHub y las comprobaciones se mantienen en el registro de estado.

Si el navegador restringe funciones al abrir archivos locales, se puede servir la entrega desde la raíz del repositorio con Python 3:

```powershell
python -m http.server 8765 --bind 127.0.0.1 --directory entregas/web
```

Después se abre [el piloto local](http://127.0.0.1:8765/). El servidor se detiene con `Ctrl+C`. Esta operación solo permite revisar los archivos en la propia computadora; publicar la web tendrá un destino acordado durante la integración del libro.

## Organización

| Carpeta | Contenido |
|---|---|
| `referencias/` | Manuscrito base y antecedentes conservados. |
| `libro/` | Capítulos editables en R Markdown, bibliografía común, configuración de bookdown y estilos. |
| `analisis/` | Preparación de datos, cálculos y comprobaciones por capítulo. |
| `datos/originales/` | Insumos preservados; su procedencia y unidades se documentan en el manifiesto. |
| `datos/preparados/` | Derivados reproducibles utilizados por texto y figuras. |
| `assets/` | Figuras estáticas, interactivos individuales y tablas por capítulo. |
| `scripts/` | Instalación de dependencias y compilación. |
| `seguimiento/` | Plan vigente, estado, decisiones, inventario, bibliografía y registros de verificación. |
| `entregas/` | Copias preparadas para revisar y distribuir. |

Los datos y scripts ya existentes en el repositorio se mantienen como antecedentes de sus respectivos análisis. La conciliación con los insumos locales queda documentada en [el inventario](seguimiento/INVENTARIO.md).

## Reproducir

El entorno detectado utiliza R 4.6.1, bookdown 0.48 y rmarkdown 2.32, Pandoc incluido en RStudio y XeLaTeX de TinyTeX. Desde la raíz del repositorio:

```powershell
& 'C:\Program Files\R\R-4.6.1\bin\Rscript.exe' scripts/instalar_dependencias.R
& 'C:\Program Files\R\R-4.6.1\bin\Rscript.exe' scripts/compilar.R todo
```

También se admiten los modos `web` y `pdf`. La compilación vuelve a preparar los índices y las figuras desde la matriz conservada. Las versiones observadas de los paquetes y la sesión de R se guardan al finalizar. El instalador resuelve paquetes disponibles en CRAN; para repetir una edición debe compararse el entorno resultante con el manifiesto de dependencias guardado, pues el instalador no fija versiones antiguas automáticamente.

La biblioteca `.local/R` pertenece a esta computadora y está excluida de Git. No es necesario distribuirla junto con el libro. Las instrucciones completas, la auditoría independiente y el protocolo para actualizar datos están en [REPRODUCIBILIDAD.md](seguimiento/REPRODUCIBILIDAD.md).

## Continuidad editorial

La ejecución se rige por [el plan de diez bloques](seguimiento/PLAN.md), [las decisiones registradas](seguimiento/DECISIONES.md) y [el estado del proyecto](seguimiento/ESTADO.md). Los originales no se sobrescriben. El piloto conserva VAB de 2024 a precios de 2018, 32 entidades y 21 actividades, con minería petrolera y no petrolera separadas. KSI e ICE se calculan como sumas completas de diferencias absolutas; el IEE corresponde al cociente de localización.

La [matriz bibliográfica](seguimiento/MATRIZ_BIBLIOGRAFICA.csv) distingue fuentes consultadas, pasajes comprobados y lecturas pendientes. El siguiente bloque comenzará después de revisar B01.
