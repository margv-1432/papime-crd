# F07-KSI. HTML autónomo desde la tabla conservada; mantiene el índice y sus denominadores.
# Ejecutar desde la raíz: Rscript --vanilla plots/capitulo-02/generar_interactivo.R
# El catálogo territorial compartido aporta las denominaciones del explorador.
if (.Platform$OS.type == "windows") invisible(suppressWarnings(Sys.setlocale("LC_CTYPE", "Spanish_Mexico.utf8")))
file_arg <- grep("^--file=", commandArgs(trailingOnly = FALSE), value = TRUE)
if (length(file_arg) != 1L) stop("Ejecute este generador con Rscript.")
script_file <- normalizePath(sub("^--file=", "", file_arg), winslash = "/", mustWork = TRUE)
here <- dirname(script_file)
root <- normalizePath(file.path(here, "..", ".."), winslash = "/", mustWork = TRUE)
extra <- Sys.getenv("PAPIME_R_LIBRARY")
if (nzchar(extra)) .libPaths(c(strsplit(extra, .Platform$path.sep, fixed = TRUE)[[1]], .libPaths()))
insumo <- file.path(root, "datos", "capitulo-02", "KSI_entidades.csv")
destino <- file.path(here, "F07-ksi.html")
stopifnot(file.exists(insumo))
datos <- read.csv(insumo, colClasses = "character", check.names = FALSE,
                  fileEncoding = "UTF-8", stringsAsFactors = FALSE)
catalogo <- jsonlite::fromJSON(file.path(root, "datos/globales/estados-web.json"))$estados
stopifnot(nrow(catalogo) == 32L, !anyDuplicated(catalogo$cve_ent), setequal(datos$cve_ent, catalogo$cve_ent))
datos$nombre <- catalogo$nombre[match(datos$cve_ent, catalogo$cve_ent)]
stopifnot(nrow(datos) == 32L, !anyDuplicated(datos$cve_ent),
          all(is.finite(as.numeric(datos$KSI))), all(as.numeric(datos$KSI) >= 0),
          all(as.numeric(datos$KSI) <= 2))
json_string <- function(x) {
  piezas <- vapply(utf8ToInt(enc2utf8(x)), function(k) {
    if (k == 34) return('\\"')
    if (k == 92) return('\\\\')
    if (k < 32 || k %in% c(60, 62, 38, 8232, 8233)) return(sprintf('\\u%04x', k))
    intToUtf8(k)
  }, character(1))
  paste0('"', paste0(piezas, collapse = ''), '"')
}
filas <- vapply(seq_len(nrow(datos)), function(i) {
  paste0('{"cve_ent":', json_string(datos$cve_ent[i]),
         ',"nombre":', json_string(datos$nombre[i]),
         ',"nombre_corto":', json_string(datos$nombre_corto[i]),
         ',"KSI":', datos$KSI[i], ',"KSI_texto":', json_string(datos$KSI[i]), '}')
}, character(1))
csv <- paste(readLines(insumo, encoding = "UTF-8", warn = FALSE), collapse = "\r\n")
json <- paste0('{"filas":[', paste(filas, collapse = ','), '],"csv":', json_string(csv), '}')
plantilla <- r"---(<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Especialización relativa de las 32 entidades mexicanas. KSI calculado con el VAB de 2024 a precios de 2018.">
<title>Especialización relativa de las entidades · F07-KSI</title>
<style>__ESTILO_F07__</style>
</head>
<body>
<main>
<h1>Especialización relativa de las entidades</h1>
<p class="subtitulo">México 2024 · Valor agregado bruto a precios de 2018</p>
<div class="controles">
<div class="campo"><label for="orden">Orden de las entidades</label><select id="orden"><option value="descendente">KSI de mayor a menor</option><option value="alfabetico">Alfabético</option></select></div>
<div class="campo"><label for="entidad">Entidad para examinar</label><select id="entidad"><option value="">Todas las entidades</option></select></div>
</div>
<section class="lectura" aria-label="Lectura del índice" aria-live="polite" aria-atomic="true"><strong id="lectura-titulo">Comparación con la estructura nacional</strong><p id="lectura-texto">Un KSI mayor expresa más distancia entre la composición productiva de la entidad y la del país.</p><p class="valor-exacto" id="valor-exacto">La escala de 0 a 2 conserva la suma completa de diferencias absolutas.</p></section>
<p class="ayuda" id="instrucciones">Elija una entidad o pulse su barra para destacar su resultado. Las 32 entidades permanecen visibles. También puede recorrer las barras con Tab y seleccionarlas con Entrar.</p>
<div class="grafico" id="grafico"><svg id="ksi" role="group" aria-label="Gráfico de barras del KSI de las 32 entidades" aria-describedby="instrucciones"></svg></div>
<noscript><p>Active JavaScript para explorar las barras. El gráfico y la tabla utilizan los datos completos conservados en el proyecto.</p></noscript>
<div class="fuente"><p><strong>Fuente</strong> Matriz del PIBE de INEGI conservada en el proyecto. Cálculos propios con 32 entidades y 21 actividades, incluida la separación de la minería petrolera y no petrolera.</p><p>La matriz se expresa en millones de pesos de 2018; el KSI es adimensional. Los denominadores son las sumas sectoriales del VAB y la referencia es el país completo. Se utiliza la suma de diferencias absolutas, sin dividir entre dos.</p></div>
<div class="acciones"><button type="button" id="descargar">Descargar datos CSV</button><span class="aviso-descarga" id="descarga-aviso" role="status">Incluye las 32 entidades y los valores conservados.</span></div>
<details id="tabla-datos"><summary>Consultar la tabla completa de resultados</summary><div class="tabla-contenedor"><table><caption>La tabla sigue el orden de la gráfica. Los valores conservan la precisión del archivo de datos.</caption><thead><tr><th scope="col">Clave</th><th scope="col">Entidad</th><th scope="col" class="numero">KSI</th></tr></thead><tbody id="tabla-cuerpo"></tbody></table></div></details>
</main>
<script id="f07-datos" type="application/json">__DATOS_F07__</script>
<script>
'use strict';
(() => {
 const carga=JSON.parse(document.getElementById('f07-datos').textContent);
 const datos=carga.filas;
 if(datos.length!==32||new Set(datos.map(d=>d.cve_ent)).size!==32||datos.some(d=>!Number.isFinite(d.KSI)||d.KSI<0||d.KSI>2)) throw new Error('La matriz del KSI no es válida');
 const svg=document.getElementById('ksi'), contenedor=document.getElementById('grafico'), orden=document.getElementById('orden'), entidad=document.getElementById('entidad');
 const titulo=document.getElementById('lectura-titulo'), texto=document.getElementById('lectura-texto'), exacto=document.getElementById('valor-exacto'), tabla=document.getElementById('tabla-cuerpo');
 const ns='http://www.w3.org/2000/svg', colador=new Intl.Collator('es',{sensitivity:'base'});
 const tres=new Intl.NumberFormat('es-MX',{minimumFractionDigits:3,maximumFractionDigits:3});
 const dos=new Intl.NumberFormat('es-MX',{minimumFractionDigits:2,maximumFractionDigits:2});
 let seleccion='';
 function nodo(tipo,atributos,contenido){const n=document.createElementNS(ns,tipo);for(const [k,v] of Object.entries(atributos||{})) n.setAttribute(k,String(v));if(contenido!==undefined)n.textContent=contenido;return n;}
 for(const d of [...datos].sort((a,b)=>colador.compare(a.nombre_corto,b.nombre_corto))){const opt=document.createElement('option');opt.value=d.cve_ent;opt.textContent=d.nombre_corto;entidad.appendChild(opt);}
 function elegir(clave){seleccion=clave;entidad.value=clave;const d=datos.find(d=>d.cve_ent===clave);if(d){titulo.textContent=d.nombre_corto+' · KSI '+tres.format(d.KSI);texto.textContent='El índice resume las diferencias de participación de sus 21 actividades respecto de la estructura nacional.';exacto.textContent='Valor conservado: '+d.KSI_texto;}else{titulo.textContent='Comparación con la estructura nacional';texto.textContent='Un KSI mayor expresa más distancia entre la composición productiva de la entidad y la del país.';exacto.textContent='La escala de 0 a 2 conserva la suma completa de diferencias absolutas.';}dibujar();}
 function dibujar(){
  const foco=document.activeElement?.getAttribute?.('data-entidad');
  const lista=[...datos].sort(orden.value==='alfabetico'?(a,b)=>colador.compare(a.nombre_corto,b.nombre_corto):(a,b)=>b.KSI-a.KSI||colador.compare(a.nombre_corto,b.nombre_corto));
  const ancho=Math.max(320,Math.floor(contenedor.clientWidth)), estrecho=ancho<500;
  const izq=estrecho?128:190, der=estrecho?38:56, arriba=14, paso=estrecho?27:28, abajo=50, alto=arriba+paso*lista.length+abajo, espacio=ancho-izq-der;
  const x=v=>izq+(v/2)*espacio;
  svg.replaceChildren();svg.setAttribute('viewBox',`0 0 ${ancho} ${alto}`);svg.setAttribute('width',ancho);svg.setAttribute('height',alto);
  const tituloSvg=nodo('title',{id:'titulo-svg'},'KSI de las 32 entidades mexicanas en 2024');svg.appendChild(tituloSvg);
  const desc=nodo('desc',{},'Barras horizontales en escala de cero a dos. Los datos completos están disponibles en la tabla y la descarga CSV.');svg.appendChild(desc);
  const fin=arriba+paso*lista.length;
  const marcas=estrecho?[0,0.5,1,1.5,2]:[0,0.25,0.5,0.75,1,1.25,1.5,1.75,2];
  for(const v of marcas){svg.appendChild(nodo('line',{x1:x(v),x2:x(v),y1:arriba-4,y2:fin,stroke:'#E0E5E8','stroke-width':1}));svg.appendChild(nodo('text',{x:x(v),y:fin+18,'text-anchor':'middle','font-size':estrecho?10:12,fill:'#56616B'},dos.format(v)));}
  svg.appendChild(nodo('text',{x:izq+espacio/2,y:alto-7,'text-anchor':'middle','font-size':estrecho?10:13,fill:'#24313A'},'KSI · diferencias absolutas'));
  for(let i=0;i<lista.length;i++){
   const d=lista[i], y=arriba+i*paso, activo=d.cve_ent===seleccion;
   const g=nodo('g',{class:'fila'+(activo?' seleccionada':''),tabindex:0,role:'button','data-entidad':d.cve_ent,'aria-pressed':activo,'aria-label':d.nombre_corto+', KSI '+tres.format(d.KSI)+'. Seleccionar entidad.'});
   g.appendChild(nodo('rect',{class:'foco',x:1,y:y-2,width:ancho-2,height:paso-1,rx:3,fill:activo?'#E8F0F4':'transparent',stroke:'none'}));
   g.appendChild(nodo('title',{},d.nombre+': '+d.KSI_texto));
   g.appendChild(nodo('text',{class:'nombre',x:izq-9,y:y+paso*.58,'text-anchor':'end','font-size':estrecho?10.7:13.5},d.nombre_corto));
   g.appendChild(nodo('rect',{x:izq,y:y+4,width:Math.max(0,x(d.KSI)-izq),height:paso-10,fill:seleccion&&!activo?'#91ACBB':'#0F4761',stroke:activo?'#0F4761':'none','stroke-width':activo?1:0}));
   g.appendChild(nodo('text',{class:'cifra',x:x(d.KSI)+5,y:y+paso*.58,'font-size':estrecho?10.5:12.5},tres.format(d.KSI)));
   g.addEventListener('click',()=>elegir(d.cve_ent));g.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();elegir(d.cve_ent);}});svg.appendChild(g);
  }
  tabla.replaceChildren();for(const d of lista){const tr=document.createElement('tr');if(d.cve_ent===seleccion)tr.className='destacada';for(const [valor,clase] of [[d.cve_ent,''],[d.nombre_corto,''],[d.KSI_texto,'numero']]){const td=document.createElement('td');td.textContent=valor;if(clase)td.className=clase;tr.appendChild(td);}tabla.appendChild(tr);}
  if(foco){const previo=svg.querySelector(`[data-entidad="${foco}"]`);previo?.focus({preventScroll:true});}
 }
 orden.addEventListener('change',dibujar);entidad.addEventListener('change',()=>elegir(entidad.value));
 document.getElementById('descargar').addEventListener('click',()=>{const blob=new Blob(['\uFEFF',carga.csv,'\r\n'],{type:'text/csv;charset=utf-8'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download='F07-KSI_entidades_2024.csv';document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),30000);document.getElementById('descarga-aviso').textContent='Descarga preparada con las 32 entidades.';});
 if('ResizeObserver' in window){new ResizeObserver(dibujar).observe(contenedor);}else{window.addEventListener('resize',dibujar);}
 function publishHeight(){if(window.parent!==window)window.parent.postMessage({type:'papime:resize',height:Math.ceil(document.body.getBoundingClientRect().height)+2},'*');}
 if('ResizeObserver' in window)new ResizeObserver(publishHeight).observe(document.body);
 window.addEventListener('load',publishHeight);
 dibujar();
 publishHeight();
})();
</script>
</body>
</html>
)---"
estilo <- paste(readLines(file.path(root, "estilos", "widgets", "especializacion.css"), encoding = "UTF-8", warn = FALSE), collapse = "\n")
plantilla <- sub("__ESTILO_F07__", estilo, plantilla, fixed = TRUE)
partes <- strsplit(plantilla, "__DATOS_F07__", fixed = TRUE)[[1]]
stopifnot(length(partes) == 2L)
html <- paste0(partes[1], json, partes[2])
dir.create(dirname(destino), recursive = TRUE, showWarnings = FALSE)
writeLines(enc2utf8(html), destino, useBytes = TRUE)
message("F07-KSI autónomo generado con 32 entidades y CSV integrado: ", destino)
