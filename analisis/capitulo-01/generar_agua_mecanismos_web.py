"""Genera F03/F05/F06 para el manual web desde derivados congelados.

Sólo escribe los tres HTML autónomos; conserva datos y salidas históricas.
"""
from pathlib import Path
import csv
import html
import json

ROOT = Path(__file__).resolve().parents[2]
PREP = ROOT / 'datos/preparados/capitulo-01'
DEST = ROOT / 'assets/capitulo-01/interactivos'


def read_csv(name):
    with (PREP / name).open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


water = read_csv('F03_F05_agua_poblacion_2022.csv')
nodes = read_csv('F06_nodos.csv')
relations = read_csv('F06_relaciones.csv')
assert len(water) == 13 and len(nodes) == 9 and len(relations) == 10
assert sum(int(row['agua_renovable_hm3_anio']) for row in water) == 461640
assert abs(sum(float(row['poblacion_millones']) for row in water) - 129.35) < 1e-9
geometry = json.loads((PREP / 'F03_RHA2023_dibujo.json').read_text(encoding='utf8'))
points = [point for region in geometry['regiones'] for ring in region['rings'] for point in ring]
xmin, xmax = min(p[0] for p in points), max(p[0] for p in points)
ymin, ymax = min(p[1] for p in points), max(p[1] for p in points)
scale = min(940 / (xmax-xmin), 610 / (ymax-ymin))


def xy(point):
    return [round(30 + (point[0]-xmin)*scale, 2), round(20 + (ymax-point[1])*scale, 2)]


shapes = []
for region in geometry['regiones']:
    d = ''.join('M' + 'L'.join(','.join(map(str, xy(p))) for p in ring) + 'Z' for ring in region['rings'])
    shapes.append(dict(rha=region['rha'], d=d, anchor=xy(region['anchor'])))

STYLE = r'''
:root{--azul:#0F4761;--calido:#A34F26;--texto:#24313A;--gris:#596974;--borde:#CCD9E0;--fondo:#F1F6F8}
*{box-sizing:border-box}body{margin:0;background:#fff;color:var(--texto);font:16px/1.5 Arial,Calibri,sans-serif}
main{max-width:1280px;margin:auto;padding:20px}h1{font-size:1.55rem;color:var(--azul);line-height:1.25;margin:0 0 10px}
h2{font-size:1.15rem;color:var(--azul);margin:0 0 12px}h3{font-size:1rem;margin:0 0 5px;color:var(--azul)}p{margin:0 0 12px}
.meta,.nota{font-size:.88rem;color:var(--gris)}.badge{display:inline-block;padding:4px 9px;background:var(--fondo);border-radius:3px;font-size:.86rem}
button,input,select{font:inherit}button,select,input[type=search]{min-height:44px;border:1px solid #839AA7;background:white;color:var(--azul);border-radius:4px;padding:9px 12px}
button{cursor:pointer}button:hover{background:#E8F1F5}button.primario{background:var(--azul);color:white}button:disabled{opacity:.5;cursor:default}
input[type=checkbox]{width:20px;height:20px;accent-color:var(--azul);flex:none;margin:0 9px 0 0}:focus-visible{outline:3px solid #007CAF;outline-offset:3px}
a{color:var(--azul)}label{font-weight:600}fieldset{border:1px solid var(--borde);border-radius:5px;padding:12px;margin:0;min-width:0}legend{color:var(--azul);font-weight:bold;padding:0 5px}
.barra{display:flex;gap:10px;align-items:end;flex-wrap:wrap;margin:16px 0}.campo{display:flex;flex-direction:column;gap:5px}.campo input,.campo select{width:100%}
.explorador{display:grid;grid-template-columns:minmax(240px,300px) minmax(0,1fr);gap:18px;align-items:start}.selector{background:#FAFCFD;border:1px solid var(--borde);border-radius:6px;padding:14px}
.selector input[type=search]{width:100%;margin-bottom:8px}.opciones{max-height:310px;overflow:auto;scrollbar-gutter:stable}.opcion{display:flex;align-items:center;min-height:46px;padding:7px 5px;border-bottom:1px solid #E2E9ED;font-weight:400;cursor:pointer}
.opcion:hover{background:var(--fondo)}.opcion.activa{background:#E0EDF3;font-weight:bold}.selector .nota{margin:8px 0 0}.vistas{min-width:0}.lienzo{border:1px solid var(--borde);border-radius:6px;padding:12px;background:#fff}
.leyenda{display:flex;gap:18px;flex-wrap:wrap;align-items:center;font-size:.88rem;margin:10px 0}.punto{width:12px;height:12px;border-radius:50%;display:inline-block;margin-right:6px}.agua{background:var(--azul)}.poblacion{background:var(--calido)}
svg{display:block;width:100%;height:auto}svg text{font-family:Arial,Calibri,sans-serif}.region{cursor:pointer;outline:none}.region path{fill:#E3EDF2;stroke:#7392A4;stroke-width:1.2;vector-effect:non-scaling-stroke}
.region circle{fill:var(--azul);stroke:#fff;stroke-width:2;vector-effect:non-scaling-stroke}.region.activa path{fill:#C7DDE8;stroke:var(--calido);stroke-width:2.3}.region.activa circle{stroke:var(--calido);stroke-width:3}
.region.atenuada{opacity:.35}.region:hover path,.region:focus path{stroke:#007CAF;stroke-width:3}.region:hover,.region:focus{opacity:1}.region .numero{fill:#fff;pointer-events:none;font-size:16px;font-weight:bold;text-anchor:middle}
.region .externo{fill:var(--azul);paint-order:stroke;stroke:white;stroke-width:4px}.detalle{margin:16px 0;padding:14px;background:var(--fondo);border-left:4px solid var(--azul);border-radius:3px}
.tarjetas{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(240px,100%),1fr));gap:12px}.tarjeta{padding:12px;background:#fff;border:1px solid var(--borde);border-radius:5px}.tarjeta p:last-child{margin-bottom:0}
dl{display:grid;grid-template-columns:1fr auto;gap:4px 12px;margin:7px 0}dt{font-size:.9rem}dd{margin:0;font-variant-numeric:tabular-nums;font-weight:bold;text-align:right}.estado{font-weight:bold;color:var(--azul);min-height:24px}
.tabla{overflow-x:auto;max-width:100%;border:1px solid var(--borde);border-radius:5px}table{border-collapse:collapse;width:100%;font-size:.9rem}th,td{padding:9px 11px;text-align:left;border-bottom:1px solid #DAE4E9;vertical-align:top}th{background:var(--fondo);color:var(--azul)}td.num,th.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}tbody tr.activa{background:#E8F2F6}.tabla button{padding:3px 7px;min-height:44px;border:0;background:transparent;text-align:left}.tabla button[aria-pressed=true]{font-weight:bold}
details{margin:14px 0}summary{color:var(--azul);font-weight:bold;cursor:pointer;padding:8px 0;min-height:44px}.serie-control{display:flex;align-items:center;gap:12px;flex-wrap:wrap}.serie-control label{display:flex;align-items:center;min-height:44px;font-weight:400}
.filas-grafico{display:grid;gap:6px}.fila-grafico{display:block;width:100%;text-align:left;padding:10px;border:1px solid #E0E8EC;border-radius:4px;color:var(--texto);background:#fff;min-height:70px}.fila-grafico.activa{border:2px solid var(--calido);background:#F8FBFC;padding:9px}.nombre-fila{display:block;color:var(--azul);font-weight:bold;margin-bottom:6px;font-size:.9rem}
.pista{display:flex;align-items:center;gap:8px;min-height:22px}.carril{display:block;flex:1;background:#F1F4F5;height:10px;position:relative}.relleno{display:block;height:10px;border-radius:2px;min-width:1px}.valor{width:62px;text-align:right;font-size:.85rem;font-variant-numeric:tabular-nums}.eje{display:flex;justify-content:space-between;font-size:.8rem;color:var(--gris);margin:5px 70px 12px 0;padding-left:3px}.vacio{padding:15px;color:var(--gris)}
.grafo .nodo{cursor:pointer}.grafo .nodo rect{fill:#EFF5F8;stroke:#7296AA;stroke-width:1.6}.grafo .nodo text{fill:var(--azul);text-anchor:middle;font-size:17px;font-weight:bold;pointer-events:none}.grafo .nodo.activa rect{fill:#D7EAF3;stroke:var(--calido);stroke-width:3}.grafo .nodo:focus rect,.grafo .nodo:hover rect{stroke:#007CAF;stroke-width:3}.grafo .arista{cursor:pointer}.grafo .trazo{fill:none;stroke:#7593A3;stroke-width:2.4;marker-end:url(#flecha)}.grafo .arista.retorno .trazo{stroke:var(--calido);stroke-dasharray:6 4;marker-end:url(#flecha-retorno)}.grafo .arista.activa .trazo{stroke:var(--azul);stroke-width:4}.grafo .arista.retorno.activa .trazo{stroke:var(--calido)}.grafo .arista:focus .trazo,.grafo .arista:hover .trazo{stroke:#007CAF;stroke-width:5}.grafo .arista .zona{fill:none;stroke:transparent;stroke-width:22}.grafo .numero-arista{fill:white;stroke:#9DB2BF}.grafo .arista.activa .numero-arista{fill:#D7EAF3;stroke:var(--calido);stroke-width:2}.grafo .arista text{fill:var(--azul);font-size:13px;text-anchor:middle;pointer-events:none}.grafo .atenuada{opacity:.28}
.nodos-movil{display:none}.nodo-movil{width:100%;display:block;text-align:left;margin:7px 0;border-left:4px solid var(--azul)}.nodo-movil.activa{border-color:var(--calido);background:#E7F1F6;font-weight:bold}.nodo-movil small{display:block;color:var(--gris);font-weight:normal}
@media(max-width:760px){main{padding:12px}.explorador{grid-template-columns:1fr}.opciones{max-height:190px}.barra>.campo{flex-basis:100%;min-width:100%}.barra button{flex:1}.selector{padding:11px}.lienzo{padding:8px}.tarjetas{grid-template-columns:1fr}.estado{font-size:.92rem}.grafo{display:none}.nodos-movil{display:block}th,td{padding:8px}.eje{margin-right:67px}}
@media(max-width:600px){.barra:has(#vecinos){display:grid;grid-template-columns:1fr 1fr;align-items:stretch}.barra:has(#vecinos)>.campo,.barra:has(#vecinos)>#descargar{grid-column:1/-1}.barra:has(#vecinos)>button{min-width:0}}
@media(prefers-reduced-motion:no-preference){.region,.nodo,.arista{transition:opacity .15s}}
'''

COMMON = r'''
const $=id=>document.getElementById(id), escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const number=(v,n=4)=>new Intl.NumberFormat('es-MX',{maximumFractionDigits:n}).format(Number(v));
const clean=s=>String(s).normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
function csvText(rows,fields){const cell=v=>'"'+String(v??'').replace(/"/g,'""')+'"';return fields.map(cell).join(',')+'\r\n'+rows.map(r=>fields.map(k=>cell(r[k])).join(',')).join('\r\n')+'\r\n';}
function download(name,rows,fields){const a=document.createElement('a'),url=URL.createObjectURL(new Blob(['\uFEFF',csvText(rows,fields)],{type:'text/csv;charset=utf-8'}));a.href=url;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),15000);}
function activate(element,callback){element.addEventListener('click',callback);element.addEventListener('keydown',event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();callback(event);}});}
function rememberFocus(){const el=document.activeElement;if(!el)return null;for(const attr of ['data-option','data-rha','data-table','data-chart','data-node','data-edge','data-mobile-node','data-table-edge'])if(el.hasAttribute(attr))return '['+attr+'="'+CSS.escape(el.getAttribute(attr))+'"]';return el.id?'#'+CSS.escape(el.id):null;}
function restoreFocus(selector){if(selector)document.querySelector(selector)?.focus({preventScroll:true});}
function sendHeight(){if(window.parent!==window)window.parent.postMessage({type:'papime:resize',height:Math.ceil(document.body.getBoundingClientRect().height)+2},'*');}
new ResizeObserver(()=>requestAnimationFrame(sendHeight)).observe(document.body);window.addEventListener('load',sendHeight);
'''


def page(title, body, payload, script):
    encoded = json.dumps(payload, ensure_ascii=False).replace('<', '\\u003c')
    return ('<!doctype html><html lang="es-MX"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{html.escape(title)}</title><style>{STYLE}</style></head>'
            f'<body><main><h1>{html.escape(title)}</h1>{body}</main>'
            f'<script id="datos-figura" type="application/json">{encoded}</script>'
            f'<script>(()=>{{"use strict";{COMMON}\n{script}\n}})();</script></body></html>')


WATER_BODY = '''
<p class="meta">CONAGUA · corte estadístico 2022 · 13 regiones hidrológico-administrativas</p>
<p>Seleccione regiones en el mapa, el gráfico o la lista para reunir una comparación. Cada selección permanece marcada y comparte sus valores con la tabla y el detalle.</p>
<div class="barra"><button id="restablecer">Restablecer vista</button><button id="descargar" class="primario">Descargar tabla visible CSV</button></div>
<p id="estado" class="estado" aria-live="polite"></p>
<div class="explorador"><aside class="selector" aria-label="Selección de regiones">
<label for="buscar">Buscar regiones</label><input id="buscar" type="search" placeholder="Nombre o número de RHA" autocomplete="off">
<div id="opciones" class="opciones" role="group" aria-label="Regiones para comparar"></div>
<p class="nota">Marque una o varias regiones. Sin selección se muestra el conjunto nacional.</p></aside>
<div class="vistas"><div class="lienzo">__VISTA__</div></div></div>
<section class="detalle" aria-labelledby="titulo-detalle"><h2 id="titulo-detalle">Lectura de la selección</h2><div id="detalle"></div></section>
<h2>Datos de la vista</h2><p class="nota">Las participaciones conservan sus denominadores nacionales: 461 640 hm³/año y 129.35 millones de habitantes. La descarga conserva la precisión de la base preparada.</p>
<div class="tabla"><table><thead><tr><th scope="col">Región</th><th scope="col" class="num">Agua<br>hm³/año</th><th scope="col" class="num">Población<br>millones</th><th scope="col" class="num">Agua<br>% nacional</th><th scope="col" class="num">Población<br>% nacional</th><th scope="col" class="num">Diferencia<br>puntos porcentuales</th></tr></thead><tbody id="tabla"></tbody></table></div>
<details><summary>Fuentes, unidades y cobertura</summary>
<p class="nota">CONAGUA, <em>Estadísticas del agua en México 2023</em>, publicada en marzo de 2024, tabla 1.5.2, p. 16 y tabla 2.2.2, p. 27. Agua renovable de recursos medios y población proyectada de mitad de 2022 de esa edición.</p>
<p class="nota">La cartografía de RHA de SEMARNAT, referencia 2023, se vincula por identificador a los valores del cuadro de 2022. El dibujo utiliza la proyección Lambert Cónica Conforme y una generalización de 1 km; la región XIII aparece como «Valle de México» en la capa y «Aguas del Valle de México» en el cuadro.</p>
<p class="nota">Las diferencias entre participaciones son descriptivas. Para estudiar demanda, servicio o estrés hídrico deben incorporarse los usos y las condiciones de abastecimiento que se explican en el capítulo.</p>
</details>
'''

WATER_SCRIPT = r'''
const payload=JSON.parse($('datos-figura').textContent), rows=payload.filas, selected=new Set();
const fields=Object.keys(rows[0]), lookup=new Map(rows.map(r=>[r.rha,r]));
function visible(){return rows.filter(r=>!selected.size||selected.has(r.rha));}
function toggle(id){selected.has(id)?selected.delete(id):selected.add(id);render();}
function options(){const query=clean($('buscar').value);$('opciones').innerHTML=rows.filter(r=>clean(r.rha+' '+r.nombre).includes(query)).map(r=>`<label class="opcion ${selected.has(r.rha)?'activa':''}"><input type="checkbox" data-option="${r.rha}" ${selected.has(r.rha)?'checked':''}><span>${escape(r.rha+'. '+r.nombre)}</span></label>`).join('')||'<p class="vacio">Sin coincidencias.</p>';$('opciones').querySelectorAll('input').forEach(el=>el.addEventListener('change',()=>toggle(el.dataset.option)));}
function render(){
 const previousFocus=rememberFocus();options();const view=visible();$('estado').textContent=selected.size?`${selected.size} de 13 regiones seleccionadas · ${view.map(r=>r.rha).join(', ')} · denominadores nacionales constantes`:'Vista nacional · 13 regiones · sin selección activa';
 $('tabla').innerHTML=view.map(r=>`<tr data-row="${r.rha}" class="${selected.has(r.rha)?'activa':''}"><td><button data-table="${r.rha}" aria-pressed="${selected.has(r.rha)}">${escape(r.rha+'. '+r.nombre)}</button></td><td class="num">${number(r.agua_renovable_hm3_anio,0)}</td><td class="num">${number(r.poblacion_millones,2)}</td><td class="num">${number(r.porcentaje_agua)}</td><td class="num">${number(r.porcentaje_poblacion)}</td><td class="num">${number(r.diferencia_puntos_porcentuales)}</td></tr>`).join('');
 $('tabla').querySelectorAll('button').forEach(el=>el.addEventListener('click',()=>toggle(el.dataset.table)));
 $('detalle').innerHTML=selected.size?'<div class="tarjetas">'+view.map(r=>`<article class="tarjeta" data-detail="${r.rha}"><h3>${escape(r.rha+'. '+r.nombre)}</h3><dl><dt>Agua renovable</dt><dd>${number(r.agua_renovable_hm3_anio,0)} hm³/año</dd><dt>Población de referencia</dt><dd>${number(r.poblacion_millones,2)} millones</dd><dt>Participación del agua</dt><dd>${number(r.porcentaje_agua)} %</dd><dt>Participación de población</dt><dd>${number(r.porcentaje_poblacion)} %</dd><dt>Diferencia de participaciones</dt><dd>${number(r.diferencia_puntos_porcentuales)} pp</dd></dl></article>`).join('')+'</div>':'<p>El conjunto reúne 461 640 hm³/año y 129.35 millones de habitantes. Seleccione una región para leer sus valores o reúna varias para compararlas. Los porcentajes siempre se refieren al mismo conjunto nacional.</p>';
 draw(view);restoreFocus(previousFocus);requestAnimationFrame(sendHeight);
}
$('buscar').addEventListener('input',options);
$('descargar').addEventListener('click',()=>download(payload.id+'_tabla_visible_2022.csv',visible(),fields));
$('restablecer').addEventListener('click',()=>{selected.clear();$('buscar').value='';resetView();render();});
'''

MAP_VIEW = '''<div class="campo"><label for="variable">Variable del mapa</label><select id="variable"><option value="agua_renovable_hm3_anio">Agua renovable · hm³/año</option><option value="poblacion_millones">Población · millones</option></select></div>
<div class="leyenda"><span id="leyenda-mapa"></span><label class="opcion"><input id="simbolos" type="checkbox" checked>Símbolos proporcionales</label><label class="opcion"><input id="limites" type="checkbox" checked>Límites y claves RHA</label></div>
<svg id="mapa" viewBox="0 0 1000 650" aria-labelledby="mapa-title mapa-desc"><title id="mapa-title">Regiones hidrológico-administrativas de México</title><desc id="mapa-desc">Cada región puede seleccionarse con clic, toque, Enter o barra espaciadora. El área del símbolo representa la variable elegida.</desc></svg>
<svg id="escala-simbolos" viewBox="0 0 1000 120" aria-label="Ejemplos de área proporcional"></svg><p id="valores-escala" class="nota"></p>
<p class="nota">El área de los símbolos es proporcional al valor. Las regiones fuera de la selección permanecen como contexto y pueden añadirse con un clic. La lista facilita elegir regiones pequeñas.</p>'''

MAP_SCRIPT = r'''
const ns='http://www.w3.org/2000/svg';
function draw(){
 const metric=$('variable').value, maximum=Math.max(...rows.map(r=>Number(r[metric]))), svg=$('mapa');
 svg.querySelectorAll('.region').forEach(n=>n.remove());
 $('leyenda-mapa').textContent=metric==='agua_renovable_hm3_anio'?'Área proporcional · agua renovable (hm³/año)':'Área proporcional · población (millones)';
 const references=metric==='agua_renovable_hm3_anio'?[5000,50000,150000]:[1,10,20];$('escala-simbolos').style.display=$('simbolos').checked?'block':'none';$('valores-escala').textContent=$('simbolos').checked?'Escala de los símbolos, de izquierda a derecha: '+references.map(v=>number(v,0)).join(' · ')+(metric==='agua_renovable_hm3_anio'?' hm³/año.':' millones de habitantes.'):'';$('escala-simbolos').innerHTML=references.map((v,i)=>`<circle cx="${180+i*320}" cy="55" r="${42*Math.sqrt(v/maximum)}" fill="#0F4761"/>`).join('');
 payload.geometria.forEach(shape=>{const r=lookup.get(shape.rha),g=document.createElementNS(ns,'g');g.setAttribute('class','region'+(selected.has(r.rha)?' activa':selected.size?' atenuada':''));g.setAttribute('data-rha',r.rha);g.setAttribute('tabindex','0');g.setAttribute('role','button');g.setAttribute('aria-pressed',String(selected.has(r.rha)));g.setAttribute('aria-label',r.rha+'. '+r.nombre+', '+number(r[metric])+(metric==='agua_renovable_hm3_anio'?' hm³/año':' millones de habitantes'));
 const path=document.createElementNS(ns,'path');path.setAttribute('d',shape.d);if(!$('limites').checked)path.style.strokeWidth=0;g.append(path);
 const radius=42*Math.sqrt(Number(r[metric])/maximum);
 if($('simbolos').checked){const circle=document.createElementNS(ns,'circle');circle.setAttribute('cx',shape.anchor[0]);circle.setAttribute('cy',shape.anchor[1]);circle.setAttribute('r',radius);g.append(circle);}
 if($('limites').checked){const text=document.createElementNS(ns,'text');text.setAttribute('class','numero'+(radius<16||!$('simbolos').checked?' externo':''));text.setAttribute('x',shape.anchor[0]);text.setAttribute('y',shape.anchor[1]+(radius<16&&$('simbolos').checked?-radius-5:5));text.textContent=r.rha;g.append(text);}
 activate(g,()=>toggle(r.rha));svg.append(g);
 });
}
function resetView(){$('variable').value='agua_renovable_hm3_anio';$('simbolos').checked=true;$('limites').checked=true;}
['variable','simbolos','limites'].forEach(id=>$(id).addEventListener('change',()=>draw()));render();
'''

CHART_VIEW = '''<div class="barra"><div class="campo"><label for="orden">Orden de comparación</label><select id="orden"><option value="orden">Orden de RHA</option><option value="porcentaje_agua">Mayor participación de agua</option><option value="porcentaje_poblacion">Mayor participación de población</option><option value="diferencia_puntos_porcentuales">Mayor diferencia agua − población</option></select></div></div>
<fieldset><legend>Series visibles</legend><div class="serie-control"><label><input id="serie-agua" type="checkbox" checked><span class="punto agua"></span>Agua renovable</label><label><input id="serie-poblacion" type="checkbox" checked><span class="punto poblacion"></span>Población</label></div></fieldset>
<p class="nota">Porcentaje del total nacional, con una escala común de 0 a 36 %.</p><div class="eje" aria-hidden="true"><span>0 %</span><span>18 %</span><span>36 %</span></div><div id="grafico" class="filas-grafico" role="group" aria-label="Comparación de participaciones de agua y población"></div>'''

CHART_SCRIPT = r'''
const originalVisible=visible;
visible=function(){const view=originalVisible();const key=$('orden').value;return key==='orden'?view:view.slice().sort((a,b)=>Number(b[key])-Number(a[key])||Number(a.orden)-Number(b.orden));};
function draw(view){
 const series=[['serie-agua','porcentaje_agua','agua','Agua renovable'],['serie-poblacion','porcentaje_poblacion','poblacion','Población']].filter(s=>$(s[0]).checked);
 $('grafico').innerHTML=series.length?view.map(r=>`<button class="fila-grafico ${selected.has(r.rha)?'activa':''}" data-chart="${r.rha}" aria-pressed="${selected.has(r.rha)}"><span class="nombre-fila">${escape(r.rha+'. '+r.nombre)}</span>${series.map(s=>`<span class="pista"><span class="punto ${s[2]}" aria-hidden="true"></span><span class="carril"><span class="relleno ${s[2]}" style="width:${Number(r[s[1]])/36*100}%"></span></span><span class="valor" aria-label="${s[3]}">${number(r[s[1]],1)} %</span></span>`).join('')}</button>`).join(''):'<p class="vacio">Active una serie para verla en el gráfico. La tabla conserva los datos de la vista.</p>';
 $('grafico').querySelectorAll('button').forEach(el=>el.addEventListener('click',()=>toggle(el.dataset.chart)));
}
function resetView(){$('orden').value='orden';$('serie-agua').checked=true;$('serie-poblacion').checked=true;}
['orden','serie-agua','serie-poblacion'].forEach(id=>$(id).addEventListener('change',render));render();
'''

F06_BODY = '''
<p class="meta">Síntesis interpretativa propia · 9 nodos · 10 relaciones documentadas</p>
<p>El esquema sigue el paso de las condiciones geográficas al aprovechamiento y a sus resultados. Al seleccionar un nodo aparecen sus conexiones; al elegir una relación se muestran sus extremos y la referencia que la respalda.</p>
<div class="barra"><div class="campo"><label for="modo">Explorar por</label><select id="modo"><option value="nodos">Nodos y sus conexiones</option><option value="relaciones">Relaciones documentadas</option></select></div><button id="vecinos">Añadir nodos conectados</button><button id="restablecer">Restablecer vista</button><button id="descargar" class="primario">Descargar relaciones visibles CSV</button></div>
<p id="estado" class="estado" aria-live="polite"></p>
<div class="explorador"><aside class="selector"><label for="buscar">Buscar en el esquema</label><input id="buscar" type="search" placeholder="Nombre o explicación" autocomplete="off"><div id="opciones" class="opciones" role="group" aria-label="Elementos para comparar"></div><p class="nota">La selección admite varios elementos. Las líneas discontinuas representan retornos hacia la base natural.</p></aside>
<div class="vistas"><div class="lienzo"><svg id="grafo" class="grafo" viewBox="0 0 1000 570" aria-labelledby="grafo-title grafo-desc"><title id="grafo-title">Mecanismos territoriales</title><desc id="grafo-desc">Nodos y relaciones seleccionables. Los números de las flechas corresponden a las filas de la tabla.</desc><defs><marker id="flecha" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0L8,4L0,8Z" fill="#7593A3"/></marker><marker id="flecha-retorno" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0L8,4L0,8Z" fill="#A34F26"/></marker></defs></svg><div id="nodos-movil" class="nodos-movil" aria-label="Nodos del esquema en vista vertical"></div><p class="nota">Cada flecha propone una relación para el análisis territorial. El esquema conserva su carácter conceptual y las referencias de apoyo del capítulo.</p></div></div></div>
<section class="detalle" aria-labelledby="titulo-detalle"><h2 id="titulo-detalle">Detalle de la selección</h2><div id="detalle"></div></section>
<h2>Relaciones de la vista</h2><div class="tabla"><table><thead><tr><th scope="col">N.º</th><th scope="col">Origen → destino</th><th scope="col">Relación</th><th scope="col">Tipo</th><th scope="col">Fuente</th></tr></thead><tbody id="tabla"></tbody></table></div>
<details><summary>Lectura y referencias</summary><p class="nota">Síntesis propia de la discusión del capítulo, apoyada en Geurs y van Wee (2004), FAO (1993), Gasca Zamora (2014), Bray et al. (2003) y Aburto-Oropeza et al. (2008). Las referencias de cada fila proceden del registro conservado de relaciones.</p><p class="nota">La descarga incluye únicamente las relaciones de la tabla visible, con sus identificadores de origen y destino, explicación, tipo y URL de referencia. Seleccionar elementos organiza la consulta del esquema.</p></details>
'''

F06_SCRIPT = r'''
const payload=JSON.parse($('datos-figura').textContent),nodes=payload.nodos,edges=payload.relaciones;
const byId=new Map(nodes.map(n=>[n.id,n])),chosenNodes=new Set(),chosenEdges=new Set(),ns='http://www.w3.org/2000/svg';
const names={proceso:'Proceso',mediacion:'Mediación',retorno:'Retorno ambiental'};
const positions={infra:[130,65],tec:[375,65],org:[620,65],inst:[865,65],base:[130,270],acceso:[375,270],uso:[620,270],resultados:[865,270],conservacion:[620,485]};
const paths=[['M230 270 L275 270',252,270],['M475 270 L520 270',498,270],['M720 270 L765 270',742,270],['M130 110 L130 165 L340 165 L340 225',245,165],['M375 110 L375 225',375,180],['M620 110 L620 225',620,180],['M865 110 L865 225',865,180],['M620 315 L620 440',620,380],['M865 315 L865 390 L690 440',820,405],['M520 485 L130 485 L130 315',310,485]];
function active(){return $('modo').value==='nodos'?chosenNodes:chosenEdges;}
function visible(){if($('modo').value==='nodos')return edges.map((r,i)=>({...r,index:i})).filter(r=>!chosenNodes.size||chosenNodes.has(r.origen)||chosenNodes.has(r.destino));return edges.map((r,i)=>({...r,index:i})).filter(r=>!chosenEdges.size||chosenEdges.has(String(r.index)));}
function chooseNode(id){$('modo').value='nodos';chosenNodes.has(id)?chosenNodes.delete(id):chosenNodes.add(id);render();}
function chooseEdge(index){$('modo').value='relaciones';index=String(index);chosenEdges.has(index)?chosenEdges.delete(index):chosenEdges.add(index);render();}
function labelEdge(r,i){return (i+1)+'. '+byId.get(r.origen).etiqueta+' → '+byId.get(r.destino).etiqueta+' · '+r.etiqueta;}
function options(){const q=clean($('buscar').value),nodeMode=$('modo').value==='nodos';const list=nodeMode?nodes.map(n=>({id:n.id,label:n.etiqueta,search:n.etiqueta+' '+n.detalle})):edges.map((r,i)=>({id:String(i),label:labelEdge(r,i),search:labelEdge(r,i)}));$('opciones').innerHTML=list.filter(o=>clean(o.search).includes(q)).map(o=>`<label class="opcion ${active().has(o.id)?'activa':''}"><input type="checkbox" data-option="${o.id}" ${active().has(o.id)?'checked':''}><span>${escape(o.label)}</span></label>`).join('')||'<p class="vacio">Sin coincidencias.</p>';$('opciones').querySelectorAll('input').forEach(el=>el.addEventListener('change',()=>nodeMode?chooseNode(el.dataset.option):chooseEdge(el.dataset.option)));}
function render(){const previousFocus=rememberFocus();options();const view=visible(),shown=new Set(view.map(r=>r.index)),nodeMode=$('modo').value==='nodos';
 $('vecinos').disabled=!nodeMode||!chosenNodes.size;
 $('estado').textContent=active().size?`Selección: ${active().size} ${nodeMode?(active().size===1?'nodo':'nodos'):(active().size===1?'relación':'relaciones')} · ${view.length} relaciones en la vista`:'Esquema completo · 9 nodos · 10 relaciones';
 const svg=$('grafo');svg.querySelectorAll('.nodo,.arista').forEach(el=>el.remove());
 edges.forEach((r,i)=>{const [d,x,y]=paths[i],g=document.createElementNS(ns,'g');g.setAttribute('class','arista '+r.tipo+(shown.has(i)?' activa':' atenuada'));g.dataset.edge=String(i);g.setAttribute('role','button');g.setAttribute('tabindex','0');g.setAttribute('aria-pressed',String(!nodeMode&&chosenEdges.has(String(i))));g.setAttribute('aria-label',labelEdge(r,i));g.innerHTML=`<path class="trazo" d="${d}"/><path class="zona" d="${d}"/><circle class="numero-arista" cx="${x}" cy="${y}" r="13"/><text x="${x}" y="${y+4}">${i+1}</text>`;activate(g,()=>chooseEdge(i));svg.append(g);});
 nodes.forEach(n=>{const [x,y]=positions[n.id],g=document.createElementNS(ns,'g'),isChosen=nodeMode&&chosenNodes.has(n.id),connected=view.some(r=>r.origen===n.id||r.destino===n.id);g.dataset.node=n.id;g.setAttribute('role','button');g.setAttribute('tabindex','0');g.setAttribute('aria-pressed',String(isChosen));g.setAttribute('aria-label',n.etiqueta);g.setAttribute('class','nodo'+(isChosen?' activa':'')+(!connected?' atenuada':''));const words=n.etiqueta.split(' '),lines=n.etiqueta.length>22?[words.slice(0,Math.ceil(words.length/2)).join(' '),words.slice(Math.ceil(words.length/2)).join(' ')]:[n.etiqueta];g.innerHTML=`<rect x="${x-100}" y="${y-45}" width="200" height="90" rx="6"/>`+lines.map((line,i)=>`<text x="${x}" y="${y+(lines.length===1?5:-7)+i*25}">${escape(line)}</text>`).join('');activate(g,()=>chooseNode(n.id));svg.append(g);});
 $('nodos-movil').innerHTML=nodes.map(n=>`<button class="nodo-movil ${nodeMode&&chosenNodes.has(n.id)?'activa':''}" data-mobile-node="${n.id}" aria-pressed="${nodeMode&&chosenNodes.has(n.id)}">${escape(n.etiqueta)}<small>${names[n.tipo]}</small></button>`).join('');$('nodos-movil').querySelectorAll('button').forEach(el=>el.addEventListener('click',()=>chooseNode(el.dataset.mobileNode)));
 $('tabla').innerHTML=view.map(r=>`<tr data-relation="${r.index}" class="${!nodeMode&&chosenEdges.has(String(r.index))?'activa':''}"><td>${r.index+1}</td><td><button data-table-edge="${r.index}" aria-pressed="${!nodeMode&&chosenEdges.has(String(r.index))}">${escape(byId.get(r.origen).etiqueta+' → '+byId.get(r.destino).etiqueta)}</button></td><td>${escape(r.etiqueta)}</td><td>${r.tipo==='retorno'?'Retorno ambiental':'Interpretativa'}</td><td><a href="${escape(r.url)}" target="_blank" rel="noopener">Referencia de apoyo</a></td></tr>`).join('');$('tabla').querySelectorAll('button').forEach(el=>el.addEventListener('click',()=>chooseEdge(el.dataset.tableEdge)));
 let cards='';if(nodeMode&&chosenNodes.size)cards=nodes.filter(n=>chosenNodes.has(n.id)).map(n=>`<article class="tarjeta" data-detail-node="${n.id}"><h3>${escape(n.etiqueta)}</h3><p>${escape(n.detalle)}</p><p class="nota">${view.filter(r=>r.origen===n.id||r.destino===n.id).length} relaciones documentadas conectadas; sus referencias aparecen en la tabla.</p></article>`).join('');
 if(!nodeMode&&chosenEdges.size)cards=view.map(r=>`<article class="tarjeta" data-detail-edge="${r.index}"><h3>${escape(byId.get(r.origen).etiqueta+' → '+byId.get(r.destino).etiqueta)}</h3><p><strong>${escape(r.etiqueta)}.</strong> ${escape(byId.get(r.destino).detalle)}</p><a href="${escape(r.url)}" target="_blank" rel="noopener">Consultar referencia de apoyo</a></article>`).join('');
 $('detalle').innerHTML=cards?'<div class="tarjetas">'+cards+'</div>':'<p>Seleccione un nodo o el número de una flecha. La consulta puede reunir varios elementos y sus conexiones permanecen identificadas en la tabla. En pantalla pequeña, la vista vertical de nodos acompaña el mismo detalle.</p>';restoreFocus(previousFocus);requestAnimationFrame(sendHeight);
}
$('buscar').addEventListener('input',options);$('modo').addEventListener('change',()=>{$('buscar').value='';render();});
$('restablecer').addEventListener('click',()=>{chosenNodes.clear();chosenEdges.clear();$('modo').value='nodos';$('buscar').value='';render();});
$('vecinos').addEventListener('click',()=>{const expanded=new Set(chosenNodes);edges.forEach(r=>{if(chosenNodes.has(r.origen)||chosenNodes.has(r.destino)){expanded.add(r.origen);expanded.add(r.destino);}});expanded.forEach(id=>chosenNodes.add(id));render();});
$('descargar').addEventListener('click',()=>download('F06_relaciones_visibles.csv',visible(),Object.keys(edges[0])));render();
'''

DEST.mkdir(parents=True, exist_ok=True)
for identity, title, view, script, filename in [
    ('F03', 'Distribución regional del agua renovable', MAP_VIEW, MAP_SCRIPT, 'F03-agua-renovable.html'),
    ('F05', 'Agua renovable y población por región', CHART_VIEW, CHART_SCRIPT, 'F05-agua-poblacion.html'),
]:
    payload = dict(id=identity, filas=water)
    if identity == 'F03':
        payload['geometria'] = shapes
    (DEST/filename).write_text(page(title, WATER_BODY.replace('__VISTA__', view), payload, WATER_SCRIPT+script), encoding='utf8')
(DEST/'F06-mecanismos-territoriales.html').write_text(page('Mecanismos territoriales', F06_BODY, dict(nodos=nodes, relaciones=relations), F06_SCRIPT), encoding='utf8')
print('F03/F05/F06: tres HTML autónomos generados desde datos preparados, sin salidas PDF ni cambios de datos.')
