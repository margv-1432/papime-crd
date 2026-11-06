// Pruebas funcionales de F04 web contra las cuatro bases congeladas.
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),crypto=require('node:crypto');
let playwright;for(const prefix of ['C:/Program Files/WindowsApps/OpenAI.CodexPrimaryRuntime.v26-1105-1297-0_26.1105.1297.0_x64__3k8sg7r9htsxt/dependencies/node/node_modules','C:/Program Files/WindowsApps/OpenAI.CodexPrimaryRuntime.v26-1030-493-0_26.1030.493.0_x64__3k8sg7r9htsxt/dependencies/node/node_modules']){try{playwright=require(prefix+'/playwright');break;}catch{}}
if(!playwright)throw Error('Playwright no disponible');
const root=path.resolve(__dirname,'..'),asset=path.join(root,'assets/capitulo-01/interactivos/F04-recursos.html'),prep=path.join(root,'datos/preparados/capitulo-01');
const qa=path.join(root,'tmp/qa-recursos-web-B02');fs.mkdirSync(qa,{recursive:true});
const report={fecha:'2026-11-06',figura:'F04',comprobaciones:[],errores:[],externas:[],capturas:[]};
const check=(name,ok,detail='')=>{report.comprobaciones.push({prueba:name,correcto:!!ok,detalle:detail});};
function parseCSV(raw){const text=raw.replace(/^\uFEFF/,''),rows=[];let row=[],field='',quoted=false;for(let i=0;i<text.length;i++){const c=text[i];if(quoted){if(c==='"'&&text[i+1]==='"'){field+='"';i++;}else if(c==='"')quoted=false;else field+=c;}else if(c==='"')quoted=true;else if(c===','){row.push(field);field='';}else if(c==='\n'){row.push(field.replace(/\r$/,''));rows.push(row);row=[];field='';}else field+=c;}if(field||row.length){row.push(field);rows.push(row);}const fields=rows.shift();return {fields,rows:rows.filter(r=>r.length>1).map(values=>Object.fromEntries(fields.map((field,i)=>[field,values[i]??''])))};}
const sourceFiles={cobre:'F04_A_cobre_2023.csv',madera:'F04_B_madera_2023.csv',pesca:'F04_C_pesca_acuacultura_2023.csv',cubierta:'F04_correspondencia_vegetacion.csv'};
const source=Object.fromEntries(Object.entries(sourceFiles).map(([k,file])=>[k,parseCSV(fs.readFileSync(path.join(prep,file),'utf8'))]));
const equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
let browser,server;
async function rows(page){return page.locator('#tbody tr').evaluateAll(trs=>trs.filter(tr=>tr.querySelector('[data-field]')).map(tr=>Object.fromEntries([...tr.querySelectorAll('td[data-field]')].map(td=>[td.dataset.field,td.dataset.value]))));}
async function selected(page){return page.locator('#mapa [aria-pressed=true]').evaluateAll(es=>es.map(e=>e.dataset.state).sort());}
async function exported(page){const pending=page.waitForEvent('download');await page.locator('#export').click();const download=await pending;return {filename:download.suggestedFilename(),...parseCSV(fs.readFileSync(await download.path(),'utf8'))};}
async function shot(page,name){const file=path.join(qa,name+'.png');await page.screenshot({path:file,fullPage:false});report.capturas.push(path.relative(root,file));}
async function main(){
 server=http.createServer((req,res)=>{if(req.url==='/F04.html'){res.writeHead(200,{'Content-Type':'text/html; charset=utf-8'});res.end(fs.readFileSync(asset));}else{res.writeHead(404);res.end();}});
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));const base='http://127.0.0.1:'+server.address().port;
 browser=await playwright.chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 const context=await browser.newContext({viewport:{width:1440,height:1100},acceptDownloads:true});
 context.on('request',request=>{if(/^https?:/.test(request.url())&&!request.url().startsWith(base))report.externas.push(request.url());});
 const page=await context.newPage();page.on('pageerror',error=>report.errores.push(String(error)));
 await page.goto(base+'/F04.html',{waitUntil:'networkidle'});
 check('32 entidades seleccionables en mapa',await page.locator('#mapa .state-shape[role=button][tabindex="0"]').count()===32);
 check('Cobre: tabla inicial idéntica a base',equal((await rows(page)).slice().sort((a,b)=>a.cve_ent.localeCompare(b.cve_ent)),source.cobre.rows));
 check('Cobre: 32 barras y estados faltantes visibles',await page.locator('#chart .bar').count()===32&&(await page.locator('#chart').innerText()).includes('Guion publicado')&&(await page.locator('#chart').innerText()).includes('Sin fila'));
 const expectedHashes=Object.fromEntries(Object.values(sourceFiles).map(file=>[file,crypto.createHash('sha256').update(fs.readFileSync(path.join(prep,file))).digest('hex')]));
 check('Datos incrustados: hashes de las cuatro fuentes',await page.locator('#f04-data').evaluate((node,expected)=>{const d=JSON.parse(node.textContent);return Object.entries(expected).every(([file,hash])=>d.hashes[file]===hash);},expectedHashes));
 const allExport=await exported(page);check('Cobre: descarga inicial igual a tabla y base',equal(allExport.rows,await rows(page))&&allExport.rows.length===32);
 await page.locator('#estado-26').click();
 check('Clic en Sonora conserva selección',equal(await selected(page),['26']));
 check('Sonora: 550597.50 t y detalle persistente',equal(await rows(page),[source.cobre.rows.find(r=>r.cve_ent==='26')])&&(await page.locator('#detail-content').innerText()).includes('550,597.5'));
 await page.locator('#buscar').fill('jalisco');
 check('Búsqueda localiza Jalisco sin alterar la selección',await page.locator('#state-options input').count()===1&&equal(await selected(page),['26']));
 await page.locator('#state-options input[value="14"]').check();
 check('Multiselección coordina mapa, barras y tabla',equal(await selected(page),['14','26'])&&await page.locator('#chart .bar').count()===2&&(await rows(page)).length===2);
 check('Cero explícito de Jalisco conservado',await page.locator('#tbody tr[data-state="14"] td[data-field="valor_t"]').getAttribute('data-value')==='0.00'&&(await page.locator('#detail-content').innerText()).includes('Cero explícito'));
 const pairExport=await exported(page);check('Descarga de comparación contiene exactamente las filas visibles',equal(pairExport.rows,await rows(page))&&pairExport.rows.length===2&&pairExport.fields.join(',')===source.cobre.fields.join(','));
 const originalView=await page.locator('#mapa').getAttribute('viewBox');await page.locator('#zoom-selection').click();check('Acercamiento a selección cambia encuadre',await page.locator('#mapa').getAttribute('viewBox')!==originalView);await page.locator('#zoom-all').click();check('Mapa completo recupera encuadre sin perder selección',await page.locator('#mapa').getAttribute('viewBox')===originalView&&equal(await selected(page),['14','26']));
 await page.locator('#tbody button[data-state="14"]').focus();await page.keyboard.press('Enter');
 check('Tabla operable por teclado y foco conservado',equal(await selected(page),['26'])&&await page.locator('#estado-14').evaluate(node=>document.activeElement===node));
 await page.locator('button[data-panel="madera"]').click();
 check('Cambio de panel conserva selección estatal',equal(await selected(page),['26'])&&equal(await rows(page),[source.madera.rows.find(r=>r.cve_ent==='26')]));
 await page.locator('#reset').click();await page.locator('button[data-panel="madera"]').click();
 check('Madera: 32 filas exactas de la base',equal((await rows(page)).slice().sort((a,b)=>a.cve_ent.localeCompare(b.cve_ent)),source.madera.rows));
 await page.locator('#estado-10').focus();await page.keyboard.press(' ');await page.locator('#estado-08').focus();await page.keyboard.press('Enter');
 check('Madera: comparación por espacio/Enter',equal(await selected(page),['08','10'])&&equal((await rows(page)).slice().sort((a,b)=>a.cve_ent.localeCompare(b.cve_ent)),source.madera.rows.filter(r=>['08','10'].includes(r.cve_ent))));
 const woodExport=await exported(page);check('Madera: descarga conserva decimales originales',equal(woodExport.rows,await rows(page))&&woodExport.rows.find(r=>r.cve_ent==='08').volumen_m3r==='1303829.2024');
 await page.locator('#reset').click();await page.locator('button[data-panel="pesca"]').click();
 check('Pesca: 32 filas con CDMX vacía',equal((await rows(page)).slice().sort((a,b)=>a.cve_ent.localeCompare(b.cve_ent)),source.pesca.rows));
 await page.locator('#estado-09').focus();await page.keyboard.press('Enter');check('CDMX mantiene sin fila y valores vacíos',equal(await rows(page),[source.pesca.rows.find(r=>r.cve_ent==='09')])&&(await page.locator('#detail-content').innerText()).includes('Sin fila en el cuadro'));
 const emptyExport=await exported(page);check('Faltante de CDMX exportado como vacío',emptyExport.rows.length===1&&emptyExport.rows[0].total_sector_peso_vivo_t===''&&emptyExport.rows[0].acuacultura_peso_vivo_t==='');
 await page.locator('#reset').click();await page.locator('button[data-panel="pesca"]').click();const fishRows=await rows(page);
 check('Pesca: totales y diferencia de redondeo conservados',fishRows.reduce((s,r)=>s+Number(r.total_sector_peso_vivo_t),0)===2150294&&fishRows.reduce((s,r)=>s+Number(r.acuacultura_peso_vivo_t),0)===304732&&(await page.locator('.source-notes').textContent()).includes('304\u00a0731'));
 await page.locator('button[data-panel="cubierta"]').click();
 await page.locator('#cover-image').evaluate(image=>image.decode());
 check('Cubierta: raster conservado y once categorías',await page.locator('#cover-image').evaluate(image=>image.naturalWidth===1600&&image.naturalHeight===1006)&&await page.locator('#categories button').count()===11);
 check('Cubierta: 183 claves idénticas a fuente',equal(await rows(page),source.cubierta.rows));
 await page.locator('#categories button[data-group="Bosques templados"]').click();await page.locator('#categories button[data-group="Selvas"]').click();
 const expectedCover=source.cubierta.rows.filter(row=>['Bosques templados','Selvas'].includes(row.grupo));
 check('Cubierta: comparación múltiple coordina catálogo y detalle',equal(await rows(page),expectedCover)&&(await page.locator('#detail-content').innerText()).includes('Bosques templados')&&(await page.locator('#detail-content').innerText()).includes('Selvas'));
 const coverExport=await exported(page);check('Cubierta: exportación exacta del subconjunto visible',equal(coverExport.rows,expectedCover));
 await page.locator('#cover-search').fill('inexistente-xyz');check('Cubierta: estado sin coincidencias',await page.locator('#tbody [data-field]').count()===0&&(await page.locator('#tbody').innerText()).includes('Sin coincidencias'));
 await page.locator('#categories-all').click();check('Cubierta: restablecer categorías recupera 183 claves',equal(await rows(page),source.cubierta.rows));
 await page.locator('#cover-zoom').focus();await page.keyboard.press('ArrowRight');check('Cubierta: ampliación accesible por teclado',await page.locator('#cover-zoom').inputValue()==='125');
 await page.locator('#reset').click();check('Restablecimiento completo de panel, selección y tabla',await page.locator('button[data-panel="cobre"]').getAttribute('aria-pressed')==='true'&&(await selected(page)).length===0&&(await rows(page)).length===32&&await page.locator('#buscar').inputValue()===''&&await page.locator('#cover-zoom').inputValue()==='100');
 await shot(page,'F04-escritorio');
 await page.setViewportSize({width:800,height:1100});
 check('Ancho del libro: mapa y gráfico apilados sin desbordamiento',await page.evaluate(()=>{const map=document.querySelector('.map-card').getBoundingClientRect(),chart=document.querySelector('.chart-card').getBoundingClientRect();return chart.top>=map.bottom&&document.documentElement.scrollWidth<=innerWidth;}));
 await shot(page,'F04-ancho-libro');
 const touchContext=await browser.newContext({viewport:{width:360,height:900},isMobile:true,hasTouch:true,acceptDownloads:true});
 const mobile=await touchContext.newPage();mobile.on('pageerror',error=>report.errores.push(String(error)));await mobile.goto(base+'/F04.html',{waitUntil:'networkidle'});
 await mobile.locator('#estado-26').tap();check('Toque en mapa mantiene selección y detalle',equal(await selected(mobile),['26'])&&equal(await rows(mobile),[source.cobre.rows.find(r=>r.cve_ent==='26')]));
 await mobile.locator('#buscar').fill('Jalisco');await mobile.locator('#state-options label').tap();check('Multiselección por toque',equal(await selected(mobile),['14','26']));
 check('Móvil 360px sin desbordamiento del documento',await mobile.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 check('Controles principales con área táctil de 44px',await mobile.locator('.toolbar button, .panels button, #buscar').evaluateAll(nodes=>nodes.every(node=>node.getBoundingClientRect().height>=44)));
 await shot(mobile,'F04-movil-seleccion');await mobile.locator('#mapa').scrollIntoViewIfNeeded();await shot(mobile,'F04-movil-mapa');await mobile.locator('button[data-panel="cubierta"]').tap();await shot(mobile,'F04-movil-cubierta');
 await mobile.locator('#categories button[data-group="Selvas"]').tap();await shot(mobile,'F04-movil-categorias');const mobileExport=await exported(mobile);check('Cubierta móvil: descarga coincide con base filtrada',equal(mobileExport.rows,source.cubierta.rows.filter(row=>row.grupo==='Selvas')));
 check('Sin errores JavaScript ni peticiones externas',report.errores.length===0&&report.externas.length===0,{errores:report.errores,externas:report.externas});
}
main().catch(error=>{report.errores.push(String(error.stack||error));}).finally(async()=>{
 if(browser)await browser.close();if(server)await new Promise(resolve=>server.close(resolve));
 report.resultado=report.errores.length||report.comprobaciones.some(row=>!row.correcto)?'incidencias':'correcto';report.pruebas=report.comprobaciones.length;
 fs.writeFileSync(path.join(root,'seguimiento/verificacion-recursos-web-B02.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({resultado:report.resultado,pruebas:report.pruebas,fallos:report.comprobaciones.filter(row=>!row.correcto),errores:report.errores}));process.exitCode=report.resultado==='correcto'?0:1;
});
