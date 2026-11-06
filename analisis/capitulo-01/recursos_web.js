(() => {
'use strict';
const data=JSON.parse(document.getElementById('f04-data').textContent);
const $=id=>document.getElementById(id), NS='http://www.w3.org/2000/svg';
const stateRows=data.tables.cobre.rows, names=new Map(stateRows.map(r=>[r.cve_ent,r.entidad]));
const groups=[...new Set(data.tables.cubierta.rows.map(r=>r.grupo))];
const colors=new Map(data.tables.cubierta.rows.map(r=>[r.grupo,r.color]));
const selected=new Set(), selectedGroups=new Set();
let panel='cobre', active=null, shown=[];
const config={
 cobre:{title:'Cobre preliminar',field:'valor_t',unit:'toneladas de metal',color:'#9a633b',period:'2023 · Preliminar',source:'SGM, Anuario Estadístico de la Minería Mexicana 2023, edición 2024, cuadro 7.4, p. 115. El total publicado es 778 838.95 t. La selección conserva esta referencia nacional.'},
 madera:{title:'Producción maderable',field:'volumen_m3r',unit:'m³ de madera en rollo',color:'#347560',period:'2023 · 32 entidades',source:'SEMARNAT, Producción forestal maderable de México 2019–2024, observación 2023, actualización declarada 21-09-2026. Suma de 292 filas elementales de especie y producto, con plantaciones y otras autorizaciones incluidas.'},
 pesca:{title:'Pesca y acuacultura registradas',field:'total_sector_peso_vivo_t',unit:'toneladas en peso vivo',color:'#2a6381',period:'2023 · 31 entidades con fila publicada',source:'CONAPESCA, Anuario 2023, cuadros 2.1.5 y 2.3.3, pp. 109 y 133. La acuacultura forma parte del total sectorial. Ciudad de México no tiene fila; la entidad de registro puede diferir del sitio de captura.'},
 cubierta:{title:'Cubierta vegetal y catálogo de clases',unit:'categorías de la Serie VII',period:'Imágenes de referencia 2018 · Serie VII',source:'INEGI, uso del suelo y vegetación Serie VII, publicada en 2021, imágenes de referencia 2018; servicio SEMARNAT. Se conservan las 183 claves y su agrupación en once categorías para la representación nacional.'}
};
const labels={cve_ent:'Clave',entidad:'Entidad',valor_t:'Cobre (t)',estado_dato:'Estado del dato',valor_original_2023:'Valor publicado',periodo:'Año',unidad:'Unidad',fuente:'Fuente',volumen_m3r:'Madera (m³ rollo)',filas_elementales:'Filas elementales',total_sector_peso_vivo_t:'Total sectorial (t)',acuacultura_peso_vivo_t:'Acuacultura incluida (t)',clave:'Clave de cubierta',descripcion:'Descripción',formacion_original:'Formación original',grupo:'Grupo de dibujo',color:'Color'};
const statusLabels={numerico_publicado:'Valor numérico publicado',cero_explicito:'Cero explícito',guion_publicado:'Guion publicado',sin_fila_en_cuadro:'Sin fila en el cuadro'};
const fmt=(value,digits=6)=>value===''||value==null?'—':Number(value).toLocaleString('es-MX',{maximumFractionDigits:digits});
const normalize=text=>text.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
function element(tag,attrs={},text){const node=document.createElementNS(NS,tag);for(const [k,v] of Object.entries(attrs))node.setAttribute(k,String(v));if(text!=null)node.textContent=text;return node;}
function textNode(tag,text,cls){const node=document.createElement(tag);node.textContent=text;if(cls)node.className=cls;return node;}
function val(row){const raw=row[config[panel].field];return raw===''?null:Number(raw);}
function stateStatus(row){if(panel==='madera')return Number(row.volumen_m3r)===0?'Cero registrado':'Valor numérico publicado';return statusLabels[row.estado_dato]||row.estado_dato;}
function toggleState(id){if(selected.has(id))selected.delete(id);else selected.add(id);active=id;render();}
function activate(node,callback){node.addEventListener('click',callback);node.addEventListener('keydown',event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();callback();}});}
function rowView(){
 if(panel==='cubierta'){
  const term=normalize($('cover-search').value.trim());
  return data.tables.cubierta.rows.filter(row=>(!selectedGroups.size||selectedGroups.has(row.grupo))&&(!term||normalize(Object.values(row).join(' ')).includes(term)));
 }
 const rows=data.tables[panel].rows.filter(row=>!selected.size||selected.has(row.cve_ent));
 const order=$('order').value;
 return rows.sort((a,b)=>order==='nombre'?a.entidad.localeCompare(b.entidad,'es'):order==='clave'?a.cve_ent.localeCompare(b.cve_ent):(val(b)??-Infinity)-(val(a)??-Infinity)||a.cve_ent.localeCompare(b.cve_ent));
}
function renderOptions(){
 const term=normalize($('buscar').value.trim());
 const list=$('state-options');list.replaceChildren();
 const matches=stateRows.filter(row=>normalize(row.cve_ent+' '+row.entidad).includes(term));
 for(const row of matches){
  const label=document.createElement('label');label.className='state-option';
  const input=document.createElement('input');input.type='checkbox';input.value=row.cve_ent;input.checked=selected.has(row.cve_ent);input.dataset.state=row.cve_ent;input.setAttribute('aria-label',row.entidad);
  input.addEventListener('change',()=>{toggleState(row.cve_ent);const focus=$('state-options').querySelector('input[value="'+row.cve_ent+'"]');if(focus)focus.focus({preventScroll:true});});
  label.append(input,document.createTextNode(row.cve_ent+' · '+row.entidad));list.append(label);
 }
 if(!matches.length)list.append(textNode('p','Sin coincidencias. Pruebe otro nombre o clave.','small'));
}
function renderChips(){
 $('selection-count').textContent=selected.size?'('+selected.size+' seleccionadas)':'(todas)';
 const chips=$('chips');chips.replaceChildren();
 for(const id of selected){const button=document.createElement('button');button.type='button';button.className='chip';button.dataset.remove=id;button.setAttribute('aria-label','Quitar '+names.get(id)+' de la selección');button.textContent=names.get(id);button.append(textNode('span','×'));button.addEventListener('click',event=>{toggleState(id);if(!event.detail)($('chips').querySelector('button')||$('selector').querySelector('summary')).focus({preventScroll:true});});chips.append(button);}
 if(selected.size){const all=document.createElement('button');all.type='button';all.className='chip';all.textContent='Mostrar todas';all.addEventListener('click',()=>{selected.clear();active=null;render();});chips.append(all);}
}
const shapes=new Map();
for(const state of data.geometry.estados){
 const shape=element('path',{d:state.d,'data-state':state.cve_ent,id:'estado-'+state.cve_ent,class:'state-shape',role:'button',tabindex:'0','aria-pressed':'false','fill-rule':'evenodd'});
 shape.append(element('title',{},state.nombre));
 activate(shape,()=>toggleState(state.cve_ent));$('state-shapes').append(shape);shapes.set(state.cve_ent,shape);
}
$('mapa').setAttribute('viewBox',data.geometry.viewBox);
function color(value,max){if(value===null)return 'url(#missing-pattern)';if(value===0)return '#fff';const base=config[panel].color;const rgb=[1,3,5].map(i=>parseInt(base.slice(i,i+2),16));const t=.15+.85*(max?value/max:0);return 'rgb('+rgb.map(v=>Math.round(249+(v-249)*t)).join(',')+')';}
function renderMap(){
 const cover=panel==='cubierta';const all=cover?[]:data.tables[panel].rows;
 const max=cover?0:Math.max(...all.map(row=>val(row)??0));
 for(const [id,path] of shapes){
  const row=all.find(r=>r.cve_ent===id), amount=row?val(row):null;
  path.setAttribute('fill',cover?'#edf2ed':panel==='cobre'&&row.estado_dato==='guion_publicado'?'url(#dash-pattern)':color(amount,max));
  path.setAttribute('opacity',selected.size&&!selected.has(id)?'.45':'1');
  path.setAttribute('aria-pressed',String(selected.has(id)));
  const label=names.get(id)+(cover?' · Referencia de localización':': '+(amount===null?stateStatus(row):fmt(amount)+' '+config[panel].unit));
  path.setAttribute('aria-label',label);path.querySelector('title').textContent=label;
 }
 $('zoom-selection').disabled=!selected.size;
 $('map-title').textContent=cover?'Selección estatal de referencia':'Distribución estatal';
 $('map-note').textContent=cover?'Las entidades ubican la selección; el catálogo de cubierta corresponde al país.':'El color y la escala de barras conservan el máximo nacional de cada panel al seleccionar entidades.';
 const legend=$('map-legend');legend.replaceChildren();
 if(cover){legend.append(textNode('span','Contorno MG2020 · vista de localización'));return;}
 const range=document.createElement('span');const swatch=document.createElement('i');swatch.className='legend-swatch';swatch.style.background='linear-gradient(to right,#fff,'+config[panel].color+')';range.append(swatch,document.createTextNode('0 a '+fmt(max)+' '+config[panel].unit));legend.append(range);
 if(panel!=='madera'){
  const missing=document.createElement('span');const symbol=document.createElement('i');symbol.className='legend-swatch missing';missing.append(symbol,document.createTextNode('Sin fila'));legend.append(missing);
 }
 if(panel==='cobre'){
  for(const [cls,label] of [['dash','Guion publicado'],['','Cero explícito']]){const item=document.createElement('span'),symbol=document.createElement('i');symbol.className='legend-swatch '+cls;symbol.style.backgroundColor='#fff';item.append(symbol,document.createTextNode(label));legend.append(item);}
 }
}
function renderChart(){
 if(panel==='cubierta')return;
 const cfg=config[panel],nationalMax=Math.max(...data.tables[panel].rows.map(row=>val(row)??0));
 const width=640,left=175,right=110,top=28,rowHeight=36,height=top+shown.length*rowHeight+30;
 const svg=element('svg',{viewBox:`0 0 ${width} ${height}`,role:'group','aria-label':cfg.title+' por entidad'});
 const usable=width-left-right,scale=usable/(nationalMax||1);
 const ticks=[0,.25,.5,.75,1];
 for(const fraction of ticks){const x=left+usable*fraction;svg.append(element('line',{x1:x,x2:x,y1:top-8,y2:height-20,stroke:'#dce5e9'}));svg.append(element('text',{x,y:14,'font-size':12,'text-anchor':'middle',fill:'#52646c'},fmt(nationalMax*fraction,0)));}
 for(const [index,row] of shown.entries()){
  const y=top+index*rowHeight,amount=val(row),picked=selected.has(row.cve_ent);
  const group=element('g',{class:'bar','data-state':row.cve_ent,role:'button',tabindex:'0','aria-pressed':String(picked),'aria-label':row.entidad+': '+(amount===null?stateStatus(row):fmt(amount)+' '+cfg.unit)});
  group.append(element('rect',{x:0,y:y-6,width,height:rowHeight,class:'hit',rx:3}));
  group.append(element('text',{x:left-8,y:y+15,'text-anchor':'end',class:'bar-label'},row.entidad));
  if(amount!==null){
   group.append(element('rect',{x:left,y:y+3,width:Math.max(amount*scale,amount===0?1:0),height:13,fill:cfg.color}));
   if(panel==='pesca')group.append(element('rect',{x:left,y:y+16,width:Number(row.acuacultura_peso_vivo_t)*scale,height:4,fill:'#aa903c'}));
   group.append(element('text',{x:left+amount*scale+6,y:y+14,class:'bar-value'},fmt(amount,panel==='pesca'?0:3)));
  }else group.append(element('text',{x:left+6,y:y+15,class:'bar-value'},stateStatus(row)));
  activate(group,()=>{const id=row.cve_ent;toggleState(id);const again=$('chart').querySelector('[data-state="'+id+'"]')||shapes.get(id);if(again)again.focus({preventScroll:true});});svg.append(group);
 }
 $('chart').replaceChildren(svg);$('chart-title').textContent=cfg.title;
 $('chart-scale').textContent=cfg.unit+' · Escala lineal nacional'+(panel==='pesca'?' · Azul: total; ocre: acuacultura incluida.':'.');
}
function renderCategories(){
 const container=$('categories');container.replaceChildren();
 for(const group of groups){const button=document.createElement('button');button.type='button';button.className='category';button.dataset.group=group;button.setAttribute('aria-pressed',String(selectedGroups.has(group)));const swatch=document.createElement('i');swatch.className='color';swatch.style.background=colors.get(group);button.append(swatch,document.createTextNode(group));button.addEventListener('click',()=>{if(selectedGroups.has(group))selectedGroups.delete(group);else selectedGroups.add(group);render();const again=Array.from($('categories').children).find(n=>n.dataset.group===group);if(again)again.focus({preventScroll:true});});container.append(button);}
}
function renderTable(){
 const fields=data.tables[panel].fields;
 const tr=document.createElement('tr');for(const field of fields){const th=document.createElement('th');th.scope='col';th.textContent=labels[field]||field;tr.append(th);}$('thead').replaceChildren(tr);
 const body=$('tbody');body.replaceChildren();
 for(const row of shown){
  const tr=document.createElement('tr');if(panel!=='cubierta'){tr.dataset.state=row.cve_ent;tr.classList.toggle('selected',selected.has(row.cve_ent));}
  for(const field of fields){
   const td=document.createElement('td');td.dataset.field=field;td.dataset.value=row[field];
   if(field==='entidad'){
    const button=document.createElement('button');button.type='button';button.className='row-select';button.dataset.state=row.cve_ent;button.textContent=row.entidad;button.setAttribute('aria-pressed',String(selected.has(row.cve_ent)));button.setAttribute('aria-label','Comparar '+row.entidad);button.addEventListener('click',event=>{event.stopPropagation();toggleState(row.cve_ent);if(!event.detail)shapes.get(row.cve_ent).focus({preventScroll:true});});td.append(button);
   }else if(field==='estado_dato')td.textContent=statusLabels[row[field]]||row[field];
   else td.textContent=row[field]===''?'—':row[field];
   tr.append(td);
  }
  if(panel!=='cubierta')tr.addEventListener('click',()=>toggleState(row.cve_ent));body.append(tr);
 }
 if(!shown.length){const tr=document.createElement('tr'),td=document.createElement('td');td.colSpan=fields.length;td.className='empty';td.textContent='Sin coincidencias para esta selección.';tr.append(td);body.append(tr);}
 $('table-count').textContent=shown.length+(panel==='cubierta'?' claves':' entidades');
 $('table-caption').textContent=config[panel].title+' · '+config[panel].period+' · '+config[panel].unit;
 $('export').textContent='Descargar '+shown.length+' filas CSV';
}
function detailCard(title,paragraphs){const card=document.createElement('article');card.className='detail-item';card.append(textNode('h4',title));for(const [index,p] of paragraphs.entries())card.append(textNode('p',p,index===0?'detail-value':''));return card;}
function renderDetail(){
 const root=$('detail-content');root.replaceChildren();const grid=document.createElement('div');grid.className='detail-grid';
 if(panel==='cubierta'){
  const displayedGroups=groups.filter(g=>shown.some(r=>r.grupo===g));
  root.append(textNode('p',selected.size?'Referencia estatal: '+Array.from(selected).map(id=>names.get(id)).join(', ')+'.':'La vista nacional permite consultar el catálogo de cubierta por categoría.'));
  for(const group of displayedGroups){const rows=shown.filter(r=>r.grupo===group);const forms=[...new Set(rows.map(r=>r.formacion_original).filter(Boolean))];grid.append(detailCard(group,[rows.length+' claves en la vista',forms.join('; ')||'Claves específicas del catálogo de fuente.']));}
  if(!displayedGroups.length)grid.append(textNode('p','No hay claves que coincidan con la búsqueda.','small'));
 }else if(selected.size){
  for(const row of shown){
   const amount=val(row),paragraphs=[amount===null?stateStatus(row):fmt(amount,panel==='pesca'?0:9)+' '+config[panel].unit,stateStatus(row)+' · '+row.periodo];
   if(panel==='pesca'&&row.acuacultura_peso_vivo_t!=='')paragraphs.push('Acuacultura incluida: '+fmt(row.acuacultura_peso_vivo_t,0)+' t.');
   if(panel==='madera')paragraphs.push(row.filas_elementales+' filas elementales de especie y producto.');
   if(panel==='cobre'&&row.valor_original_2023)paragraphs.push('Registro original: '+row.valor_original_2023+'.');
   grid.append(detailCard(row.entidad,paragraphs));
  }
 }else{
  const focus=shown.find(row=>row.cve_ent===active)||shown.find(row=>val(row)!==null);
  root.append(textNode('p','La vista reúne las 32 entidades y conserva los estados de dato de la fuente. Una selección en el mapa, las barras o la tabla abre la comparación y mantiene el detalle a la vista.'));
  if(focus)grid.append(detailCard(focus.entidad,[fmt(val(focus),panel==='pesca'?0:9)+' '+config[panel].unit,stateStatus(focus)+' · '+focus.periodo]));
 }
 root.append(grid);
}
function render(){
 const cover=panel==='cubierta',cfg=config[panel];shown=rowView();
 for(const button of document.querySelectorAll('[data-panel]'))button.setAttribute('aria-pressed',String(button.dataset.panel===panel));
 $('cover-card').hidden=!cover;$('chart-card').hidden=cover;
 $('panel-title').textContent=cfg.title;$('meta').textContent=cfg.period+' · '+cfg.unit;$('source').textContent=cfg.source;
 $('status').textContent=cover?shown.length+' de 183 claves nacionales en la vista. '+(selected.size?selected.size+' entidades elegidas como referencia.':'La cubierta conserva once grupos de dibujo.'):(selected.size?selected.size+' entidades seleccionadas para comparar.':'32 entidades disponibles. Seleccione una o varias para comparar.')+' '+cfg.period+'.';
 renderOptions();renderChips();renderMap();renderChart();renderCategories();renderTable();renderDetail();resize();
}
function csvCell(value){const text=String(value);return /[",\r\n]/.test(text)?'"'+text.replaceAll('"','""')+'"':text;}
function download(){
 const fields=data.tables[panel].fields;
 const csv=[fields.join(','),...shown.map(row=>fields.map(key=>csvCell(row[key])).join(','))].join('\r\n')+'\r\n';
 const url=URL.createObjectURL(new Blob(['\uFEFF',csv],{type:'text/csv;charset=utf-8'})),a=document.createElement('a');
 a.href=url;a.download='F04-'+panel+'-vista.csv';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),30000);
}
for(const button of document.querySelectorAll('[data-panel]'))button.addEventListener('click',()=>{panel=button.dataset.panel;render();});
$('buscar').addEventListener('input',()=>{if($('buscar').value)$('selector').open=true;renderOptions();resize();});
$('cover-search').addEventListener('input',()=>render());$('order').addEventListener('change',render);$('export').addEventListener('click',download);
$('categories-all').addEventListener('click',()=>{selectedGroups.clear();$('cover-search').value='';render();});
$('zoom-all').addEventListener('click',()=>$('mapa').setAttribute('viewBox',data.geometry.viewBox));
$('zoom-selection').addEventListener('click',()=>{
 if(!selected.size)return;const boxes=Array.from(selected).map(id=>shapes.get(id).getBBox());
 const left=Math.min(...boxes.map(b=>b.x)),top=Math.min(...boxes.map(b=>b.y)),right=Math.max(...boxes.map(b=>b.x+b.width)),bottom=Math.max(...boxes.map(b=>b.y+b.height));
 const pad=Math.max((right-left)*.12,(bottom-top)*.12,10);$('mapa').setAttribute('viewBox',[left-pad,top-pad,right-left+pad*2,bottom-top+pad*2].join(' '));
});
$('cover-zoom').addEventListener('input',()=>{const z=$('cover-zoom').value;$('cover-image').style.width=z+'%';$('cover-zoom-value').textContent=z+' %';resize();});
$('reset').addEventListener('click',()=>{selected.clear();selectedGroups.clear();active=null;panel='cobre';$('buscar').value='';$('cover-search').value='';$('order').value='valor';$('selector').open=false;$('mapa').setAttribute('viewBox',data.geometry.viewBox);$('cover-zoom').value='100';$('cover-image').style.width='100%';$('cover-zoom-value').textContent='100 %';render();});
document.querySelector('.visual-grid').append($('cover-card'));
let resizeFrame;
function resize(){cancelAnimationFrame(resizeFrame);resizeFrame=requestAnimationFrame(()=>{const style=getComputedStyle(document.body);const height=Math.ceil(document.body.getBoundingClientRect().height+parseFloat(style.marginTop)+parseFloat(style.marginBottom));if(window.parent!==window)window.parent.postMessage({type:'papime:resize',height},'*');});}
new ResizeObserver(resize).observe(document.body);window.addEventListener('load',resize);
render();
})();
