# Sólo dibujo. La imagen temática se recorta al contorno MG2020 compartido
# con F01. No se calculan áreas a partir del mapa de pantalla.
if (.Platform$OS.type == 'windows') invisible(suppressWarnings(Sys.setlocale('LC_CTYPE','Spanish_Mexico.utf8')))
.libPaths(c('.local/R',file.path(Sys.getenv('USERPROFILE'),'AppData/Local/R/win-library/4.6'),.libPaths()))
for (p in c('sf','terra','jsonlite')) if (!requireNamespace(p,quietly=TRUE)) stop('Falta ',p)
raw <- 'datos/originales/capitulo-01/F04'
meta <- jsonlite::fromJSON(file.path(raw,'vegetacion-export-respuesta.json'))
img <- terra::rast(file.path(raw,'vegetacion-agrupada-1600.png'))
stopifnot(terra::ncol(img)==meta$width,terra::nrow(img)==meta$height)
terra::ext(img) <- terra::ext(meta$extent$xmin,meta$extent$xmax,meta$extent$ymin,meta$extent$ymax)
terra::crs(img) <- meta$extent$spatialReference$wkt
states <- sf::st_read('datos/preparados/capitulo-01/F01-estados.gpkg',quiet=TRUE)
stopifnot(nrow(states)==32L)
states <- sf::st_transform(states,terra::crs(img))
mask <- terra::rasterize(terra::vect(states),img[[1]],field=1,background=0)
terra::writeRaster(mask,'datos/preparados/capitulo-01/F04_mascara_MG2020.tif',overwrite=TRUE,datatype='INT1U',NAflag=255)
message('Máscara MG2020 preparada con la extensión exacta del servicio. Sin cambio de celdas temáticas.')
