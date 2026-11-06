# Reconstrucción explícita de F01/F02 desde originales grandes. No descarga.
# Rscript analisis/capitulo-01/preparar_fisico.R
.libPaths(c('.local/R', Sys.getenv('PAPIME_R_LIBRARY'), 'C:/Users/marce/AppData/Local/R/win-library/4.6', .libPaths()))
invisible(Sys.setlocale('LC_CTYPE','English_United States.utf8'))
for(p in c('sf','terra','jsonlite','digest')) if(!requireNamespace(p,quietly=TRUE))stop('Falta ',p)
out <- 'datos/preparados/capitulo-01'; dir.create(out,recursive=TRUE,showWarnings=FALSE)
raw <- function(name) {
  p<-c(file.path('.local/B02-originales',name),file.path('datos/originales/geografia',name))
  p<-p[file.exists(p)]
  if(!length(p))stop('Original ausente: ',name,'. Consulte seguimiento/B02-F01-F02.md')
  p[1]
}
extract <- function(name,subdir) {
  d<-file.path('tmp',subdir);dir.create(d,recursive=TRUE,showWarnings=FALSE)
  unzip(raw(name),exdir=d); d
}
crs_map <- '+proj=lcc +lat_1=17.5 +lat_2=29.5 +lat_0=12 +lon_0=-102 +x_0=2500000 +y_0=0 +ellps=GRS80 +units=m +no_defs'
states<-sf::st_read('../Mexicana_Tarea_3/00ent.shp',quiet=TRUE)
states<-sf::st_transform(states,crs_map)
stopifnot(nrow(states)==32L)
# Máscara con geometría original; contornos portátiles simplificados sólo para dibujo.
sf::st_write(sf::st_simplify(states,dTolerance=100,preserveTopology=TRUE),file.path(out,'F01-estados.gpkg'),quiet=TRUE,delete_dsn=TRUE)
b<-sf::st_bbox(states)
template<-terra::rast(xmin=b['xmin'],xmax=b['xmax'],ymin=b['ymin'],ymax=b['ymax'],resolution=1800,crs=crs_map)
mask<-terra::rasterize(terra::vect(states),template,field=1,background=NA)
if(!file.exists(file.path(out,'F01-provincias.gpkg'))) {
  p<-sf::st_read('../Mexicana_Tarea_3/_cache_mapas_2024/provincias_locales/provincias_fisiograficas.shp',quiet=TRUE)
  p<-p[p$ENTIDAD=='PROVINCIA',c('CLAVE','NOMBRE')]
  p<-sf::st_transform(p,crs_map)
  stopifnot(length(unique(p$CLAVE))==15L)
  sf::st_write(sf::st_simplify(p,dTolerance=500,preserveTopology=TRUE),file.path(out,'F01-provincias.gpkg'),quiet=TRUE,delete_dsn=TRUE)
}
cldir<-extract('702825267568_s.zip','F02-clima')
cl<-sf::st_read(list.files(cldir,pattern='[.]shp$',full.names=TRUE,recursive=TRUE)[1],quiet=TRUE)
soil_crs<-sf::st_crs(cl)
# TIPO_N identifica sin ambigüedad los grupos descritos en TIPO_C. La familia
# seca (51..64) se agrupa sin confundirla con categorías térmicas húmedas.
groups<-c('Cálido húmedo','Cálido subhúmedo','Semicálido húmedo','Semicálido subhúmedo','Templado húmedo','Templado subhúmedo','Semifrío subhúmedo','Secos y semisecos','Frío','Agua')
cl$grupo_id<-match(cl$TIPO_N,c(11,12,21,22,31,32,42,NA,70,92))
cl$grupo_id[cl$TIPO_N%in%51:64]<-8L
stopifnot(all(is.na(cl$grupo_id)==(cl$TIPO_N==91)))
cor<-unique(sf::st_drop_geometry(cl)[c('CLAVE','TIPO_N','TIPO_C','grupo_id')]);cor$grupo<-groups[cor$grupo_id]
write.csv(cor,file.path(out,'F02-correspondencia-climas.csv'),row.names=FALSE,fileEncoding='UTF-8')
cl<-cl[cl$TIPO_N!=91,];cl<-sf::st_transform(cl,crs_map)
clras<-terra::mask(terra::rasterize(terra::vect(cl),template,field='grupo_id'),mask)
terra::writeRaster(clras,file.path(out,'F02-climas-1800m.tif'),overwrite=TRUE,datatype='INT1U',gdal='COMPRESS=LZW')
sodir<-extract('794551131916_s.zip','F02-suelo')
so<-sf::st_read(list.files(sodir,pattern='[.]shp$',full.names=TRUE,recursive=TRUE)[1],quiet=TRUE)
# El productor no distribuye PRJ. Se asigna exclusivamente la proyección
# declarada en el metadato original: ITRF92, LCC17.5/29.5,-102/12,2500000/0.
stopifnot(is.na(sf::st_crs(so)))
sf::st_crs(so)<-soil_crs
so<-sf::st_transform(so,crs_map)
soil_groups<-c('Piedras (R)','Gravas y guijarros (r)','Sin fase registrada (N)','Agua','Localidad (sin clasificación)','Arrecife (no aplica)','Dato inconsistente')
so$grupo_id<-ifelse(so$FRUDICA=='R',1L,ifelse(so$FRUDICA=='r',2L,ifelse(so$FRUDICA=='N',3L,NA_integer_)))
so$grupo_id[so$CLAVE_WRB=='CUERPO DE AGUA']<-4L
so$grupo_id[so$CLAVE_WRB=='LOCALIDAD']<-5L
so$grupo_id[so$CLAVE_WRB=='ARRECIFE']<-6L
discord<-so$FRUDICA=='R'&so$F_SUPERF=='GRAVOSA'
so$grupo_id[discord]<-7L
stopifnot(sum(discord)==1L,all(is.na(so$grupo_id)==(so$CLAVE_WRB=='PAIS EXTRANJERO')))
cor<-unique(sf::st_drop_geometry(so)[c('CLAVE_WRB','FRUDICA','F_SUPERF','grupo_id')]);cor$grupo<-soil_groups[cor$grupo_id]
write.csv(cor,file.path(out,'F02-correspondencia-suelos.csv'),row.names=FALSE,fileEncoding='UTF-8')
write.csv(sf::st_drop_geometry(so[discord,]),file.path(out,'F02-suelo-inconsistente.csv'),row.names=FALSE,fileEncoding='UTF-8')
so<-so[so$CLAVE_WRB!='PAIS EXTRANJERO',]
soras<-terra::mask(terra::rasterize(terra::vect(so),template,field='grupo_id'),mask)
terra::writeRaster(soras,file.path(out,'F02-suelos-1800m.tif'),overwrite=TRUE,datatype='INT1U',gdal='COMPRESS=LZW')
jsonlite::write_json(list(clima=list(poligonos_originales=nrow(cl)+2L,grupos=groups,metodo='rasterización por centro de celda;1800m;sin cálculo de superficie'),suelo=list(poligonos_originales=nrow(so)+2L,grupos=soil_groups,inconsistencias=sum(discord),crs_asignado_desde_metadato=TRUE),cobertura='Marco Geoestadístico2020;islas pequeñas pueden no ocupar centro de celda',resolution_m=1800),file.path(out,'F02-metadatos.json'),pretty=TRUE,auto_unbox=TRUE)
cat('F02: clima y suelo preparados; todas las categorías originales clasificadas.\n')

# CEM3 nacional congelado, resolución de distribución120m, archivo20170619.
cemdir<-extract('CEM_V3_20170619_R120_Nacional.zip','F01-cem')
cemfile<-list.files(cemdir,pattern='[.](bil|tif)$',recursive=TRUE,full.names=TRUE,ignore.case=TRUE)
stopifnot(length(cemfile)==1L)
cem<-terra::rast(cemfile)
cem_coarse<-terra::aggregate(cem,fact=10,fun='mean',na.rm=TRUE)
elev<-terra::mask(terra::project(cem_coarse,template,method='bilinear'),mask)
terra::writeRaster(elev,file.path(out,'F01-elevacion-1800m.tif'),overwrite=TRUE,datatype='FLT4S',gdal='COMPRESS=LZW')
jsonlite::write_json(list(fuente='INEGI CEM3.0, distribución nacional120m, archivo20170619',sha256_original=digest::digest(raw('CEM_V3_20170619_R120_Nacional.zip'),file=TRUE,algo='sha256'),consulta='2026-11-05',resolucion_original=terra::res(cem),crs_original=terra::crs(cem),dimensiones_originales=c(nrow(cem),ncol(cem)),unidad='metros de elevación',transformacion='Media de bloques10x10 en rejilla nativa, proyección bilineal aLCC1800m, máscaraMG2020 original',resolucion_dibujo_m=1800,uso='Exclusivamente dibujo;no se computaron proporciones por altitud',limites_dibujo=as.list(as.vector(terra::ext(elev)))),file.path(out,'F01-elevacion-metadatos.json'),pretty=TRUE,auto_unbox=TRUE)
cat('F01: elevación preparada.\n')
