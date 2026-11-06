# F01/F02 offline: sólo lee derivados congelados de esta edición.
.libPaths(c('.local/R', Sys.getenv('PAPIME_R_LIBRARY'), 'C:/Users/marce/AppData/Local/R/win-library/4.6', .libPaths()))
invisible(Sys.setlocale('LC_CTYPE','English_United States.utf8'))
for(p in c('sf','terra','jsonlite','base64enc'))if(!requireNamespace(p,quietly=TRUE))stop('Falta ',p)
src<-'datos/preparados/capitulo-01';dst<-'assets/capitulo-01'
for(d in c('figuras-estaticas','interactivos'))dir.create(file.path(dst,d),recursive=TRUE,showWarnings=FALSE)
states<-sf::st_read(file.path(src,'F01-estados.gpkg'),quiet=TRUE)
prov<-sf::st_read(file.path(src,'F01-provincias.gpkg'),quiet=TRUE)
bb<-as.numeric(sf::st_bbox(states)); names(bb)<-c('xmin','ymin','xmax','ymax')
labs_e<-c('Menos de 0','0 a <200','200 a <500','500 a <1 000','1 000 a <2 000','2 000 a <3 000','3 000 o más')
labs_c<-c('Cálido húmedo','Cálido subhúmedo','Semicálido húmedo','Semicálido subhúmedo','Templado húmedo','Templado subhúmedo','Semifrío subhúmedo','Secos y semisecos','Frío','Agua')
labs_s<-c('Piedras (R)','Gravas y guijarros (r)','Sin fase registrada (N)','Agua','Localidad (sin clasificación)','Arrecife (no aplica)','Dato inconsistente')
col_e<-c('#17324D','#285944','#52785C','#82936A','#B0AD8C','#DACAB5','#F1EFEA')
col_c<-c('#073C2A','#879D7F','#347F7A','#8EC4BC','#5B7E9B','#B4D5DB','#8B85AA','#EEE8BE','#35333F','#E6F3F8')
col_s<-c('#65542D','#A18C59','#E7E5E0','#C9E2EC','#A8A9AA','#7FBAB5','#A65C87')
readmap<-function(name,type){
 r<-terra::rast(file.path(src,name)); m<-terra::as.matrix(r,wide=TRUE)
 m[abs(m)>1e20]<-NA
 if(type=='e')m<-matrix(as.integer(cut(m,breaks=c(-Inf,0,200,500,1000,2000,3000,Inf),right=FALSE)),nrow=nrow(m))
 colors<-switch(type,e=col_e,c=col_c,s=col_s)
 pixels<-matrix('#FFFFFF00',nrow(m),ncol(m));pixels[!is.na(m)]<-colors[m[!is.na(m)]]
 list(r=r,m=m,pixels=pixels,extent=as.vector(terra::ext(r)))
}
climate<-readmap('F02-climas-1800m.tif','c');soil<-readmap('F02-suelos-1800m.tif','s')
map_panel<-function(layer,outline=TRUE){
 e<-layer$extent
 plot(NA,xlim=e[1:2],ylim=e[3:4],asp=1,axes=FALSE,xlab='',ylab='',xaxs='i',yaxs='i',bty='n')
 rasterImage(as.raster(layer$pixels),e[1],e[3],e[2],e[4],interpolate=FALSE)
 if(outline)plot(sf::st_geometry(states),add=TRUE,border='#7B8589',col=NA,lwd=.28)
}
heading<-function(title,subtitle){mtext(title,side=3,line=.7,adj=0,font=2,col='#0F4761',cex=1.08);mtext(subtitle,side=3,line=-.3,adj=0,col='#52626C',cex=.77)}
legend_panel<-function(labels,colors,ncol=3){plot.new();legend('center',legend=labels,fill=colors,border=NA,ncol=ncol,bty='n',cex=.86,x.intersp=.5,y.intersp=1.05)}
savefigure<-function(id,fun){
 for(ext in c('png','pdf')){
  file<-file.path(dst,'figuras-estaticas',paste0(id,'.',ext))
  if(ext=='png')png(file,width=9,height=10.3,units='in',res=220,type='cairo',bg='white')else cairo_pdf(file,width=9,height=10.3,family='Arial',bg='white')
  par(family='Arial',mar=c(0,1.1,2.5,1.1),oma=c(3.2,.5,.2,.5),cex=.96)
  fun();dev.off()
 }
}
savefigure('F02-clima-suelos',function(){
 layout(matrix(1:4,ncol=1),heights=c(4.15,.85,4.15,.85))
 map_panel(climate);heading('A  Grupos climáticos','Unidades climáticas: edición 2008; base histórica del productor')
 par(mar=rep(0,4));legend_panel(labs_c,col_c,3)
 par(mar=c(0,1.1,2.5,1.1));map_panel(soil);heading('B  Fase rúdica superficial','Edafología Serie II: observaciones 2002–2006; edición 2024')
 par(mar=rep(0,4));legend_panel(labs_s,col_s,3)
 mtext('INEGI. Clima 1:1 000 000; suelos 1:250 000. Dibujo generalizado a 1.8 km.',outer=TRUE,side=1,line=2,adj=0,cex=.73)
 mtext('N significa sin fase registrada. R y r se conservan distintos. Una discordancia se muestra separada.',outer=TRUE,side=1,line=1,adj=0,cex=.73)
 mtext('La aptitud se evalúa para un uso y manejo definidos a partir de estas condiciones y de información local.',outer=TRUE,side=1,line=0,adj=0,cex=.73)
})

# HTML independientes: SVG y rásteres embebidos, sin servicios externos.
W<-1000;H<-round(W*(bb['ymax']-bb['ymin'])/(bb['xmax']-bb['xmin']))
xy<-function(m)cbind((m[,1]-bb['xmin'])/(bb['xmax']-bb['xmin'])*W,(bb['ymax']-m[,2])/(bb['ymax']-bb['ymin'])*H)
mpath<-function(m,close=FALSE){p<-xy(as.matrix(m)[,1:2,drop=FALSE]);if(nrow(p)<2)return('');paste0('M',paste(apply(round(p,1),1,paste,collapse=','),collapse=' '),if(close)'Z'else'')}
gpath<-function(g){
 type<-class(g)[class(g)%in%c('POLYGON','MULTIPOLYGON','LINESTRING','MULTILINESTRING')][1]
 if(type=='POLYGON')return(paste(vapply(g,mpath,'',close=TRUE),collapse=''))
 if(type=='MULTIPOLYGON')return(paste(vapply(g,function(p)paste(vapply(p,mpath,'',close=TRUE),collapse=''),''),collapse=''))
 if(type=='LINESTRING')return(mpath(g))
 if(type=='MULTILINESTRING')return(paste(vapply(g,mpath,''),collapse=''))
 ''
}
paths<-function(sfobj,tol=1000)vapply(sf::st_geometry(sf::st_simplify(sfobj,dTolerance=tol,preserveTopology=TRUE)),gpath,'')
statepath<-paste(paths(states),collapse='')
provpath<-paste(paths(prov),collapse='')
escape<-function(s){s<-gsub('&','&amp;',s,fixed=TRUE);s<-gsub('<','&lt;',s,fixed=TRUE);gsub('"','&quot;',s,fixed=TRUE)}
inline_raster<-function(layer,id){
 f<-file.path('tmp',paste0('F02-',id,'.png'));m<-layer$pixels
 png(f,width=ncol(m),height=nrow(m),bg='transparent',type='cairo');grid::grid.newpage();grid::grid.raster(m,interpolate=FALSE);dev.off()
 base64enc::dataURI(file=f,mime='image/png')
}
legend_html<-function(labels,colors)paste0('<ul class="legend">',paste0('<li><i style="background:',colors,'"></i>',escape(labels),'</li>',collapse=''),'</ul>')
style<-'<style>body{font:16px/1.5 Arial,sans-serif;color:#243746;background:white;margin:0 auto;max-width:1050px;padding:16px}h1{font-size:1.35rem;color:#0f4761;margin:.2em 0}h2{font-size:1.1rem}p{margin:.45em 0}.muted{color:#52626c;font-size:.88rem}.controls{display:flex;flex-wrap:wrap;gap:12px;margin:12px 0}.controls label{padding:5px 9px;background:#edf3f5;border-radius:4px}.map{width:100%;height:auto;border:1px solid #d9e2e5}.legend{list-style:none;display:flex;flex-wrap:wrap;gap:4px 20px;padding:0;font-size:.85rem}.legend li{display:flex;align-items:center;gap:6px}.legend i{display:inline-block;width:16px;height:12px}.hidden{display:none}button,select,input{font:inherit}table{border-collapse:collapse;font-size:.85rem;width:100%}td,th{padding:4px 8px;border-bottom:1px solid #d6e0e3;text-align:left}th{background:#edf3f5}details{margin:12px 0}a{color:#0f4761}:focus-visible{outline:3px solid #b45627;outline-offset:3px}@media(max-width:450px){body{padding:8px}.legend{gap:5px 10px;font-size:.78rem}}</style>'
writehtml<-function(name,title,content,js=''){
 h<-paste0('<!doctype html><html lang="es-MX"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>',title,'</title>',style,'<body><h1>',title,'</h1>',content,'<script>',js,'</script></body></html>')
 writeLines(h,file.path(dst,'interactivos',name),useBytes=TRUE)
}
content<-paste0('<p class="muted">INEGI. Clima: edición 2008, base histórica. Suelos: Serie II, observaciones 2002–2006, edición 2024.</p><div class="controls" role="group" aria-label="Capa temática"><label><input type="radio" name="capa" value="clima" checked> Clima</label><label><input type="radio" name="capa" value="suelo"> Suelos</label></div><svg class="map" viewBox="0 0 ',W,' ',H,'" role="img" aria-labelledby="maptitle"><title id="maptitle">Distribución nacional de categorías climáticas y fase superficial del suelo</title><image id="clima" href="',inline_raster(climate,'clima'),'" width="',W,'" height="',H,'"/><image id="suelo" class="hidden" href="',inline_raster(soil,'suelo'),'" width="',W,'" height="',H,'"/><path d="',statepath,'" fill="none" stroke="#64737b" stroke-width=".5"/></svg><div id="leg-clima">',legend_html(labs_c,col_c),'</div><div id="leg-suelo" class="hidden">',legend_html(labs_s,col_s),'</div><p class="muted">El dibujo se generaliza a 1.8 km y se recorta al Marco Geoestadístico 2020 para comparar las condiciones a escala nacional. Evaluar la aptitud de un terreno requiere definir su uso y manejo y consultar información local. La discordancia entre código y descripción del suelo se representa por separado.</p><details><summary>Clasificación y descargas</summary><p>Clima: TIPO_N 11, 12, 21, 22, 31, 32, 42 y 70 conservan su grupo; 51–64 se reúnen en secos y semisecos; 92 identifica agua. En suelos, R corresponde a piedras y r a gravas y guijarros. El código N reúne registros sin valor de fase al captarse o con una condición muy homogénea, según el diccionario de INEGI; se conserva como «Sin fase registrada».</p><p><a download="F02-correspondencia-climas.csv" href="',base64enc::dataURI(file=file.path(src,'F02-correspondencia-climas.csv'),mime='text/csv;charset=utf-8'),'">Correspondencias climáticas CSV</a> · <a download="F02-correspondencia-suelos.csv" href="',base64enc::dataURI(file=file.path(src,'F02-correspondencia-suelos.csv'),mime='text/csv;charset=utf-8'),'">Correspondencias de suelos CSV</a></p></details><p class="muted">Fuentes: <a href="https://www.inegi.org.mx/app/biblioteca/ficha.html?upc=702825267568">Unidades climáticas</a> · <a href="https://www.inegi.org.mx/app/biblioteca/ficha.html?upc=794551131916">Edafología Serie II</a>. Consulta documental 5 de noviembre de 2026.</p>')
writehtml('F02-clima-suelos.html','Condiciones climáticas y características superficiales del suelo',content,"document.querySelectorAll('input[name=capa]').forEach(r=>r.addEventListener('change',()=>{['clima','suelo'].forEach(id=>{document.getElementById(id).classList.toggle('hidden',id!==r.value);document.getElementById('leg-'+id).classList.toggle('hidden',id!==r.value)})}));")
cat('F02: PNG, PDF y HTML autónomo generados.\n')

if(!file.exists(file.path(src,'F01-elevacion-1800m.tif')))stop('F01 requiere elevación preparada.')
elev<-readmap('F01-elevacion-1800m.tif','e')
local<-read.csv(file.path(src,'F01-localidades-2020.csv'),colClasses=c(cveloc='character',cve_ent='character'),check.names=FALSE,encoding='UTF-8')
loc<-sf::st_transform(sf::st_as_sf(local,coords=c('longitud','latitud'),crs=6365,remove=FALSE),sf::st_crs(states))
roads<-sf::st_read(file.path(src,'F01-carreteras-federales.gpkg'),quiet=TRUE)
savefigure('F01-relieve-localizacion',function(){
 layout(matrix(1:4,ncol=1),heights=c(4.15,.65,4.15,.95))
 map_panel(elev);plot(sf::st_geometry(prov),add=TRUE,border='#626B64',col=NA,lwd=.35);heading('A  Elevación (m) y provincias fisiográficas','CEM 3.0: distribución 120 m, archivo 20170619; provincias: edición 2001')
 par(mar=rep(0,4));legend_panel(labs_e,col_e,4)
 par(mar=c(0,1.1,2.5,1.1));plot(sf::st_geometry(states),col='#F2F3F0',border='#A0ABB0',lwd=.35,axes=FALSE,reset=FALSE)
 plot(sf::st_geometry(roads),add=TRUE,col='#92A5AA',lwd=.32)
 points(sf::st_coordinates(loc),pch=21,bg='#DDA45B90',col='#B77938',cex=sqrt(local$poblacion/100000)*.58,lwd=.45)
 heading('B  Localidades y carreteras federales','Censo 2020: localidades ≥100 000 habitantes; RNC 2025: habilitadas y en operación')
 par(mar=rep(0,4));plot.new();legend('center',legend=c('100 000','500 000','1 500 000'),pch=21,pt.bg='#DDA45B90',col='#B77938',pt.cex=sqrt(c(1,5,15))*.58,title='Población (personas); área del símbolo proporcional',horiz=TRUE,bty='n',cex=.86)
 mtext('Fuente: INEGI. Capas de distintas fechas; límites del Marco Geoestadístico 2020.',outer=TRUE,side=1,line=2,adj=0,cex=.73)
 mtext('145 localidades; 61 026 805 personas, 48.43% del total censal. Se excluyen agregados municipales y estatales.',outer=TRUE,side=1,line=1,adj=0,cex=.73)
 mtext('La red sitúa conexiones para la lectura nacional; evaluar accesibilidad requiere datos de viaje y destinos.',outer=TRUE,side=1,line=0,adj=0,cex=.73)
})
loc_xy<-xy(sf::st_coordinates(loc)); loc_svg<-paste0('<circle cx="',round(loc_xy[,1],1),'" cy="',round(loc_xy[,2],1),'" r="',round(sqrt(local$poblacion/100000)*1.8,2),'" fill="#dda45b" fill-opacity=".65" stroke="#a56a2d" stroke-width=".5"><title>',escape(local$localidad),' (',escape(local$entidad),'): ',format(local$poblacion,big.mark=' ',scientific=FALSE,trim=TRUE),' habitantes</title></circle>',collapse='')
roadpath<-paste(paths(roads,tol=1000),collapse='')
rows<-paste0('<tr><td>',escape(local$localidad),'</td><td>',escape(local$entidad),'</td><td>',format(local$poblacion,big.mark=' ',scientific=FALSE,trim=TRUE),'</td></tr>',collapse='')
content<-paste0('<p class="muted">CEM 3.0, archivo 20170619; provincias 2001; población 2020; carreteras 2025; límites 2020.</p><div class="controls" role="group" aria-label="Panel"><label><input type="radio" name="panel" value="elevacion" checked> Elevación</label><label><input type="radio" name="panel" value="poblamiento"> Poblamiento y conexiones</label><label><input id="provincias-toggle" type="checkbox" checked> Provincias fisiográficas</label></div><svg class="map" viewBox="0 0 ',W,' ',H,'" role="img" aria-labelledby="maptitle"><title id="maptitle">Relieve, localidades seleccionadas y carreteras federales de México</title><g id="elevacion"><image href="',inline_raster(elev,'elevacion'),'" width="',W,'" height="',H,'"/><path id="provincias" d="',provpath,'" fill="none" stroke="#59635b" stroke-width=".65"/></g><g id="poblamiento" class="hidden"><path d="',statepath,'" fill="#f2f3f0" fill-rule="evenodd" stroke="#a0abb0" stroke-width=".5"/><path d="',roadpath,'" fill="none" stroke="#91a5ad" stroke-width=".6"/>',loc_svg,'</g><path d="',statepath,'" fill="none" stroke="#64737b" stroke-width=".45"/></svg><div id="leg-elevacion">',legend_html(labs_e,col_e),'</div><p id="leg-poblamiento" class="hidden muted">El área de los círculos es proporcional a la población. Consulte las cifras en la tabla.</p><p class="muted">Las 145 localidades de al menos 100 000 habitantes reúnen 61 026 805 personas, 48.43% de la población nacional censal de 2020. La selección se hace por localidad censal; una ciudad funcional puede reunir varias localidades. Las carreteras permiten reconocer conexiones a escala nacional. Para estudiar accesibilidad se necesitan datos de viaje y destinos.</p><details><summary>Localidades y descarga de datos</summary><p><a download="F01-localidades-2020.csv" href="',base64enc::dataURI(file=file.path(src,'F01-localidades-2020.csv'),mime='text/csv;charset=utf-8'),'">Descargar localidades CSV</a></p><table><thead><tr><th scope="col">Localidad</th><th scope="col">Entidad</th><th scope="col">Población</th></tr></thead><tbody>',rows,'</tbody></table></details><details><summary>Provincias fisiográficas</summary><p>',paste(sort(unique(prov$NOMBRE)),collapse='; '),'.</p></details><p class="muted">Elaboración propia con INEGI. La elevación se agrega y proyecta a una rejilla de 1.8 km. La generalización facilita la lectura nacional y puede omitir islas pequeñas. La selección vial conserva TIPO_VIAL=Carretera, ADMINISTRA=Federal, ESTATUS=Habilitado y CONDICION=En operación. Consulta documental 5 de noviembre de 2026.</p>')
writehtml('F01-relieve-localizacion.html','Relieve, poblamiento y conexiones de México',content,"document.querySelectorAll('input[name=panel]').forEach(r=>r.addEventListener('change',()=>{['elevacion','poblamiento'].forEach(id=>{document.getElementById(id).classList.toggle('hidden',id!==r.value);document.getElementById('leg-'+id).classList.toggle('hidden',id!==r.value)})}));document.getElementById('provincias-toggle').addEventListener('change',e=>document.getElementById('provincias').classList.toggle('hidden',!e.target.checked));")
cat('F01: PNG, PDF y HTML autónomo generados.\n')
