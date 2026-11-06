# Reconstrucción explícita del dibujo de carreteras F01. No descarga.
.libPaths(c('.local/R',Sys.getenv('PAPIME_R_LIBRARY'),'C:/Users/marce/AppData/Local/R/win-library/4.6',.libPaths()))
invisible(Sys.setlocale('LC_CTYPE','English_United States.utf8'))
for(p in c('sf','jsonlite','digest'))if(!requireNamespace(p,quietly=TRUE))stop('Falta ',p)
raw<-c('.local/B02-originales/794551163030_gpk.zip','datos/originales/geografia/794551163030_gpk.zip')
raw<-raw[file.exists(raw)][1];stopifnot(!is.na(raw))
dir.create('tmp/F01-rnc',recursive=TRUE,showWarnings=FALSE)
gpkg<-'tmp/F01-rnc/conjunto_de_datos/rnc2025.gpkg'
if(!file.exists(gpkg))unzip(raw,files='conjunto_de_datos/rnc2025.gpkg',exdir='tmp/F01-rnc')
sql<-"SELECT ID_RED, UNION_INI, UNION_FIN, geom FROM red_vial WHERE TIPO_VIAL = 'Carretera' AND ADMINISTRA = 'Federal' AND ESTATUS = 'Habilitado' AND CONDICION = 'En operación'"
r<-sf::st_read(gpkg,query=sql,quiet=TRUE)
stopifnot(nrow(r)==120863L,!anyDuplicated(r$ID_RED),!any(sf::st_is_empty(r)))
states<-sf::st_read('datos/preparados/capitulo-01/F01-estados.gpkg',quiet=TRUE)
r<-sf::st_transform(r,sf::st_crs(states))
# Encadenar sólo en nodos originales de grado2, sin inventar enlaces espaciales.
coords<-lapply(sf::st_geometry(r),function(g)as.matrix(g)[,1:2,drop=FALSE])
ini<-as.character(r$UNION_INI);fin<-as.character(r$UNION_FIN);n<-nrow(r)
adj<-list2env(split(rep(seq_len(n),2),c(ini,fin)),parent=emptyenv(),hash=TRUE)
visited<-rep(FALSE,n)
walk<-function(node,at){
 pieces<-list()
 repeat{
  edges<-get0(node,envir=adj,ifnotfound=integer())
  if(length(edges)!=2L)break
  next_edge<-edges[!visited[edges]]
  if(length(next_edge)!=1L)break
  e<-next_edge[1];g<-coords[[e]]
  if(ini[e]==node)other<-fin[e]else{g<-g[nrow(g):1,,drop=FALSE];other<-ini[e]}
  if(any(abs(g[1,]-at)>.01))break
  visited[e]<<-TRUE;pieces[[length(pieces)+1L]]<-g[-1,,drop=FALSE]
  node<-other;at<-g[nrow(g),]
 }
 pieces
}
chains<-list()
for(i in seq_len(n))if(!visited[i]){
 visited[i]<-TRUE;g<-coords[[i]]
 forward<-walk(fin[i],g[nrow(g),]);backward<-walk(ini[i],g[1,])
 back<-if(length(backward))do.call(rbind,backward)else matrix(numeric(),ncol=2)
 if(nrow(back))back<-back[nrow(back):1,,drop=FALSE]
 joined<-do.call(rbind,c(list(back,g),forward))
 if(nrow(joined)>=2L)chains[[length(chains)+1L]]<-sf::st_linestring(joined)
}
stopifnot(all(visited))
original<-sf::st_sfc(chains,crs=sf::st_crs(r))
simple<-sf::st_simplify(original,dTolerance=500,preserveTopology=FALSE)
display<-sf::st_sf(cadena=seq_along(simple),geometry=simple)
sf::st_write(display,'datos/preparados/capitulo-01/F01-carreteras-federales.gpkg',delete_dsn=TRUE,quiet=TRUE)
jsonlite::write_json(list(fuente='INEGI RNC2025, GPKG oficial',sha256_original=digest::digest(raw,file=TRUE,algo='sha256'),consulta='2026-11-05',seleccion_sql=sql,segmentos_fuente=n,cadenas_dibujo=length(chains),tolerancia_simplificacion_m=500,comprobaciones=list(id_red_unicos=TRUE,segmentos_visitados=sum(visited),sin_geometrias_vacias=TRUE),metodo='Encadenamiento exclusivamente en nodos originales de grado2 con extremo coincidente a0.01m;sin unión espacial ni modelación de rutas',alcance='Conectividad visual; no calcula accesibilidad, tiempos, velocidades o distancias'), 'datos/preparados/capitulo-01/F01-caminos-metadatos.json',auto_unbox=TRUE,pretty=TRUE)
cat('F01:',n,'segmentos;',length(chains),'cadenas portátiles; sin omisiones en la selección.\n')
