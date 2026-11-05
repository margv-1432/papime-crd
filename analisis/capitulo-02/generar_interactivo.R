# F07-KSI. HTML autónomo desde el mismo CSV de la figura estática.
# Ejecutar desde la raíz: Rscript --vanilla analisis/capitulo-02/generar_interactivo.R
# R base; no descarga bibliotecas ni necesita conexión para explorar el HTML.
if (.Platform$OS.type == "windows") invisible(suppressWarnings(Sys.setlocale("LC_CTYPE", "Spanish_Mexico.utf8")))
insumo <- file.path("datos", "preparados", "capitulo-02", "KSI_entidades.csv")
destino <- file.path("assets", "capitulo-02", "interactivos", "F07-ksi.html")
stopifnot(file.exists(insumo))
datos <- read.csv(insumo, colClasses = "character", check.names = FALSE,
                  fileEncoding = "UTF-8", stringsAsFactors = FALSE)
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
<style>
:root{color-scheme:light;--azul:#0F4761;--tinta:#24313A;--gris:#56616B;--linea:#D6E0E5;--suave:#F2F6F8}
*{box-sizing:border-box}body{margin:0;background:#fff;color:var(--tinta);font:16px/1.55 Arial,Calibri,sans-serif}
main{max-width:1000px;margin:auto;padding:24px 24px 30px}h1{font-size:clamp(1.25rem,3.6vw,1.8rem);line-height:1.25;margin:0 0 6px;font-weight:700}
p{margin:0 0 14px}.subtitulo{color:var(--gris);font-size:.95rem}.controles{display:flex;gap:16px;flex-wrap:wrap;margin:22px 0 14px}
.campo{flex:1 1 245px}.campo label{display:block;font-weight:700;font-size:.9rem;margin-bottom:5px}
select,button{font:inherit;color:var(--tinta);border:1px solid #879CA8;border-radius:4px;background:#fff;padding:9px 11px;min-height:44px}
select{width:100%}button{cursor:pointer;color:var(--azul);font-weight:700}button:hover{background:var(--suave)}
:focus-visible{outline:3px solid #007CAF;outline-offset:3px}a{color:var(--azul)}
.lectura{background:var(--suave);border-left:4px solid var(--azul);padding:12px 15px;min-height:94px;margin-bottom:14px}
.lectura strong{display:block;font-size:1.04rem}.lectura p{margin:2px 0 0;font-size:.92rem}.valor-exacto{font-variant-numeric:tabular-nums;font-size:.86rem;color:var(--gris)}
.ayuda{color:var(--gris);font-size:.86rem;margin-bottom:8px}.grafico{width:100%;min-width:0}svg{display:block;width:100%;height:auto;overflow:visible}
.fila{cursor:pointer}.fila:focus{outline:none}.fila:focus .foco{stroke:#007CAF;stroke-width:2;fill:#F2F8FB}.fila:hover .foco{fill:#F2F8FB}
.nombre{fill:var(--tinta)}.cifra{fill:var(--tinta);font-variant-numeric:tabular-nums}.fila.seleccionada .nombre,.fila.seleccionada .cifra{font-weight:700}
.fuente{font-size:.86rem;color:var(--gris);margin:14px 0 18px}.fuente p{margin:0 0 6px}
.acciones{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin:12px 0 20px}.aviso-descarga{font-size:.86rem;color:var(--gris)}
details{border-top:1px solid var(--linea);padding-top:14px}summary{cursor:pointer;color:var(--azul);font-weight:700;min-height:44px;padding:7px 0}
.tabla-contenedor{overflow:auto}table{width:100%;border-collapse:collapse;font-size:.92rem}caption{text-align:left;padding:10px 0;color:var(--gris);font-size:.85rem}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--linea)}th{background:var(--suave)}td.numero{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}th.numero{text-align:right}tr.destacada td{background:#E8F0F4;font-weight:700}
.sr-only{position:absolute;clip:rect(0,0,0,0);width:1px;height:1px;overflow:hidden;white-space:nowrap}
@media(max-width:480px){main{padding:16px 10px 22px}.controles{gap:10px;margin-top:16px}.campo{flex-basis:100%}body{font-size:15px}.lectura{padding:10px 12px}}
@media print{main{max-width:none;padding:0}.controles,.acciones,.ayuda,details{display:none}svg{max-height:230mm}.lectura{break-inside:avoid}h1{font-size:18pt}.fuente{font-size:9pt}}
</style>
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
<noscript><p>Active JavaScript para explorar las barras. La versión estática y las tablas completas se conservan en la entrega del libro.</p></noscript>
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
 dibujar();
})();
</script>
</body>
</html>
)---"
partes <- strsplit(plantilla, "__DATOS_F07__", fixed = TRUE)[[1]]
stopifnot(length(partes) == 2L)
html <- paste0(partes[1], json, partes[2])
dir.create(dirname(destino), recursive = TRUE, showWarnings = FALSE)
writeLines(enc2utf8(html), destino, useBytes = TRUE)
message("F07-KSI autónomo generado con 32 entidades y CSV integrado: ", destino)
