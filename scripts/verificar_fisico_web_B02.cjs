// Chrome real: F01/F02, selección persistente, tablas y exportaciones contra CSV.
const fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const {chromium}=require('C:/Program Files/WindowsApps/OpenAI.CodexPrimaryRuntime.v26-1105-1297-0_26.1105.1297.0_x64__3k8sg7r9htsxt/dependencies/node/node_modules/playwright');
const root=process.cwd(),out=path.join(root,'tmp/qa-fisico-web');fs.mkdirSync(out,{recursive:true});
const report={fecha:'2026-11-06',pruebas:[],errores:[],externas:[],capturas:[]};
function ck(name,ok,detail=''){report.pruebas.push({prueba:name,correcto:!!ok,detalle:detail});if(!ok)throw Error(name+': '+JSON.stringify(detail))}
function parseCSV(text){text=text.replace(/^\uFEFF/,'');let rows=[],row=[],field='',quoted=false;for(let i=0;i<text.length;i++){const c=text[i];if(c==='"'){if(quoted&&text[i+1]==='"'){field+='"';i++}else quoted=!quoted}else if(c===','&&!quoted){row.push(field);field=''}else if((c==='\r'||c==='\n')&&!quoted){if(c==='\r'&&text[i+1]==='\n')i++;row.push(field);if(row.some(Boolean))rows.push(row);row=[];field=''}else field+=c}if(field||row.length){row.push(field);rows.push(row)}const fields=rows.shift();return{fields,rows:rows.map(r=>Object.fromEntries(fields.map((k,i)=>[k,r[i]??''])))}}
const local=parseCSV(fs.readFileSync('datos/preparados/capitulo-01/F01-localidades-2020.csv','utf8')).rows;
const climate=parseCSV(fs.readFileSync('datos/preparados/capitulo-01/F02-correspondencia-climas.csv','utf8')).rows;
const soil=parseCSV(fs.readFileSync('datos/preparados/capitulo-01/F02-correspondencia-suelos.csv','utf8')).rows;
const normalize=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
async function state(page){return page.evaluate(()=>window.figureState())}
async function download(page,button,name){const p=page.waitForEvent('download');await page.locator(button).click();const d=await p;await d.saveAs(path.join(out,name));return parseCSV(fs.readFileSync(path.join(out,name),'utf8'))}
async function shot(page,name){await page.screenshot({path:path.join(out,name+'.png'),fullPage:true});report.capturas.push('tmp/qa-fisico-web/'+name+'.png')}
async function selectState(page,id){await page.locator('#state-search').fill('');await page.locator('#state-options input[value="'+id+'"]').check()}
let browser,server,base;
(async()=>{
 const html=path.join(root,'assets/capitulo-01/interactivos');
 server=http.createServer((req,res)=>{try{const f=path.resolve(html,'.'+new URL(req.url,'http://localhost').pathname);if(!f.startsWith(html+path.sep))throw Error();const bytes=fs.readFileSync(f);res.writeHead(200,{'Content-Type':'text/html; charset=utf-8'});res.end(bytes)}catch{res.writeHead(404);res.end()}});
 await new Promise(r=>server.listen(0,'127.0.0.1',r));base='http://127.0.0.1:'+server.address().port+'/';
 browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 const context=await browser.newContext({viewport:{width:1280,height:960},acceptDownloads:true});
 context.on('request',r=>{if(/^https?:/.test(r.url())&&!r.url().startsWith(base))report.externas.push(r.url())});
 const page=await context.newPage();page.on('pageerror',e=>report.errores.push(String(e)));
 await page.goto(base+'F01-relieve-localizacion.html');
 await page.waitForFunction(()=>typeof window.figureState==='function');
 ck('F01 32 entidades seleccionables',await page.locator('[data-state]').count()===32);
 ck('F01 universo original',JSON.stringify((await state(page)).filas.map(r=>r.cveloc))===JSON.stringify(local.map(r=>r.cveloc)));
 await page.locator('#map').scrollIntoViewIfNeeded();const point=await page.evaluate(()=>{const d=JSON.parse(document.querySelector('#figure-data').textContent),r=d.localidades.find(r=>r.localidad==='Hermosillo'),svg=document.querySelector('#map'),p=svg.createSVGPoint();p.x=r.cx;p.y=r.cy;const q=p.matrixTransform(svg.getScreenCTM());return{x:q.x,y:q.y}});
 await page.mouse.click(point.x,point.y);ck('F01 clic en mapa selecciona Sonora',(await state(page)).estados.includes('26'));
 ck('F01 tabla estatal preserva selección de localidades',JSON.stringify((await state(page)).filas.map(r=>r.cveloc))===JSON.stringify(local.filter(r=>r.cve_ent==='26').map(r=>r.cveloc)));
 const nationalBox=await page.locator('#map').getAttribute('viewBox');await page.locator('#zoom-selection').click();ck('F01 acercar selección conserva filas',(await page.locator('#map').getAttribute('viewBox'))!==nationalBox&&(await state(page)).filas.length===local.filter(r=>r.cve_ent==='26').length);await page.locator('#zoom-national').click();ck('F01 vuelve al encuadre nacional',await page.locator('#map').getAttribute('viewBox')===nationalBox);
 await selectState(page,'08');ck('F01 comparación estatal múltiple',(await state(page)).estados.length===2);
 await page.locator('#city-search').fill('hermosillo');ck('F01 búsqueda coordinada',(await state(page)).filas.length===1);
 const hermo=local.find(r=>r.localidad==='Hermosillo'),chih=local.find(r=>r.localidad==='Chihuahua');
 await page.locator('#city-options input[value="'+hermo.cveloc+'"]').check();await page.locator('#city-search').fill('');
 await page.locator('#city-options input[value="'+chih.cveloc+'"]').check();
 ck('F01 comparación de localidades',JSON.stringify((await state(page)).filas.map(r=>r.cveloc).sort())===JSON.stringify([hermo.cveloc,chih.cveloc].sort()));
 const exported=await download(page,'#download','F01-seleccion.csv');
 ck('F01 CSV fiel a las filas y valores preparados',JSON.stringify(exported.rows)===JSON.stringify(local.filter(r=>[hermo.cveloc,chih.cveloc].includes(r.cveloc))));
 ck('F01 detalle incluye suma de selección',(await page.locator('#detail').innerText()).includes(new Intl.NumberFormat('es-MX').format(Number(hermo.poblacion)+Number(chih.poblacion))));
 await page.locator('[data-city="'+hermo.cveloc+'"]').press('Enter');ck('F01 teclado actualiza selección persistente',!(await state(page)).localidades.includes(hermo.cveloc)&&(await state(page)).localidades.includes(chih.cveloc));
 await page.locator('#roads-toggle').uncheck();ck('F01 control de capa vial',await page.locator('#roads').evaluate(e=>e.classList.contains('hidden')));
 await page.locator('#reset').click();ck('F01 reset nacional',(await state(page)).filas.length===145&&(await state(page)).vista==='elevacion');
 await selectState(page,'29');ck('F01 entidad sin localidades en el umbral',(await state(page)).filas.length===local.filter(r=>r.cve_ent==='29').length);
 await page.locator('#reset').click();await shot(page,'F01-escritorio');
 await page.goto(base+'F02-clima-suelos.html');
 await page.waitForFunction(()=>typeof window.figureState==='function');
 ck('F02 32 entidades contextuales',await page.locator('[data-state]').count()===32);
 ck('F02 clasificación climática original',JSON.stringify((await state(page)).filas)===JSON.stringify(climate.filter(r=>Number(r.grupo_id)>=1&&Number(r.grupo_id)<=10)));
 await selectState(page,'26');await selectState(page,'08');
 ck('F02 comparación estatal sólo contextual',(await state(page)).estados.length===2&&(await state(page)).filas.length===climate.filter(r=>Number(r.grupo_id)>=1&&Number(r.grupo_id)<=10).length);
 await page.locator('#zoom-selection').click();ck('F02 acercamiento mantiene clasificación nacional',(await page.locator('#map').getAttribute('viewBox'))!==nationalBox&&(await state(page)).filas.length===climate.filter(r=>Number(r.grupo_id)>=1&&Number(r.grupo_id)<=10).length);await page.locator('#zoom-national').click();
 await page.locator('input[name=layer][value=suelo]').check();
 ck('F02 clasificación de suelos original',JSON.stringify((await state(page)).filas)===JSON.stringify(soil.filter(r=>Number(r.grupo_id)>=1&&Number(r.grupo_id)<=7)));
 await page.locator('#classification-search').fill('GRAVOSA');
 const expected=soil.filter(r=>Number(r.grupo_id)>=1&&Number(r.grupo_id)<=7&&Object.values(r).some(v=>normalize(v).includes('gravosa')));
 ck('F02 búsqueda de clasificación',JSON.stringify((await state(page)).filas)===JSON.stringify(expected));
 const soilExport=await download(page,'#download','F02-gravosa.csv');
 ck('F02 CSV filtrado idéntico a base preparada',JSON.stringify(soilExport.rows)===JSON.stringify(expected));
 const pageExpected=(await state(page)).filasPagina;const pageExport=await download(page,'#download-page','F02-pagina.csv');
 ck('F02 CSV de página idéntico a las filas visibles',JSON.stringify(pageExport.rows)===JSON.stringify(pageExpected));
 ck('F02 discordancia R/GRAVOSA conservada',expected.some(r=>r.grupo_id==='7'&&r.F_SUPERF==='GRAVOSA'));
 await page.locator('#classification-search').fill('');const cats=await page.locator('#category-options input').count();
 for(let i=0;i<cats;i++){const el=page.locator('#category-options input').nth(i);if(await el.inputValue()!=='1')await el.uncheck()}
 ck('F02 categoría filtra mapa y tabla',(await state(page)).categorias.length===1&&(await state(page)).filas.every(r=>r.grupo_id==='1'));
 ck('F02 categorías ocultas no se dibujan',await page.locator('[data-category="suelo-2"]').evaluate(e=>e.style.display==='none'));
 await page.locator('#category-options input[value="2"]').focus();await page.keyboard.press('Space');
 ck('F02 comparación por teclado',(await state(page)).categorias.includes(1)&&(await state(page)).categorias.includes(2));
 ck('F02 conserva foco al actualizar controles',await page.locator('#category-options input[value="2"]').evaluate(e=>e===document.activeElement));
 await page.locator('#reset').click();await page.locator('input[name=interaction][value=categoria]').check();
 await page.locator('#map').scrollIntoViewIfNeeded();const hit=await page.evaluate(()=>{const d=JSON.parse(document.querySelector('#figure-data').textContent),v=d.capas.clima,a=new Uint8Array(v.columnas*v.renglones);let at=0,index=-1,score=Infinity;v.runs.lengths.forEach((n,i)=>{a.fill(v.runs.values[i],at,at+n);at+=n});for(let i=v.columnas*10;i<a.length-v.columnas*10;i++){if(a[i]!==8||a[i-1]!==8||a[i+1]!==8||a[i-v.columnas]!==8||a[i+v.columnas]!==8)continue;const s=Math.abs(i%v.columnas/v.columnas-.45)+Math.abs(Math.floor(i/v.columnas)/v.renglones-.5);if(s<score){score=s;index=i}}const svg=document.querySelector('#map'),p=svg.createSVGPoint();p.x=(index%v.columnas+.5)/v.columnas*d.width;p.y=(Math.floor(index/v.columnas)+.5)/v.renglones*d.height;const q=p.matrixTransform(svg.getScreenCTM());return{x:q.x,y:q.y}});
 await page.mouse.click(hit.x,hit.y);ck('F02 clic sobre categoría persistente',(await state(page)).categorias.length===1&&(await state(page)).categorias[0]===8);
 await page.locator('#reset').click();ck('F02 reset restaura categorías y entidades',(await state(page)).categorias.length===10&&(await state(page)).estados.length===0);
 await shot(page,'F02-escritorio');
 const mobile=await browser.newContext({viewport:{width:360,height:800},isMobile:true,hasTouch:true,acceptDownloads:true}),touch=await mobile.newPage();touch.on('pageerror',e=>report.errores.push(String(e)));
 for(const id of ['F01-relieve-localizacion','F02-clima-suelos']){
  await touch.goto(base+id+'.html');
  await touch.locator('#state-search').fill('sonora');await touch.locator('#state-options .option').tap();
  ck(id+' selección por toque',(await state(touch)).estados.includes('26'));
  ck(id+' sin desborde horizontal de página',await touch.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  ck(id+' botones táctiles de al menos 44px',await touch.locator('#reset').evaluate(e=>e.getBoundingClientRect().height>=44));
  await shot(touch,id+'-movil');
 }
 ck('Sin errores JavaScript',report.errores.length===0,report.errores);ck('HTML autónomos sin peticiones externas',report.externas.length===0,report.externas);
 report.resultado='correcto';
})().catch(e=>{report.resultado='incidencias';report.error=String(e);console.error(e);process.exitCode=1}).finally(async()=>{if(browser)await browser.close();if(server)server.close();fs.writeFileSync(path.join(out,'verificacion-fisico-web.json'),JSON.stringify(report,null,2));fs.writeFileSync(path.join(root,'seguimiento/verificacion-fisico-web-B02.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({resultado:report.resultado,pruebas:report.pruebas.length,fallos:report.pruebas.filter(p=>!p.correcto),error:report.error}));});
