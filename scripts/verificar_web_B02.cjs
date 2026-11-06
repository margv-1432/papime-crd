// Navegador real: integración del libro, selección táctil y portabilidad de los HTML.
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),{pathToFileURL}=require('node:url');
const runtime='C:/Program Files/WindowsApps/OpenAI.CodexPrimaryRuntime.v26-1105-1297-0_26.1105.1297.0_x64__3k8sg7r9htsxt/dependencies/node/node_modules';
const {chromium}=require(path.join(runtime,'playwright'));
const root=process.cwd(),web=path.join(root,'entregas/web'),qa=path.join(root,'tmp/qa-web-B02-funcional');
fs.mkdirSync(qa,{recursive:true});
const figures=['F01-relieve-localizacion','F02-clima-suelos','F03-agua-renovable','F04-recursos','F05-agua-poblacion','F06-mecanismos-territoriales'];
const report={fecha:'2026-11-06',edicion:'web D25–D28',pruebas:[],errores:[],externas:[],fallos_red:[],capturas:[]};
let browser,server;
const check=(prueba,ok,detalle='')=>report.pruebas.push({prueba,correcto:!!ok,detalle});
async function shot(page,name){const dest=path.join(qa,name+'.png');await page.screenshot({path:dest});report.capturas.push(path.relative(root,dest));}
async function main(){
 const mime={'.html':'text/html; charset=utf-8','.js':'application/javascript','.css':'text/css','.csv':'text/csv','.svg':'image/svg+xml','.png':'image/png','.json':'application/json'};
 server=http.createServer((req,res)=>{try{let p=decodeURIComponent(new URL(req.url,'http://localhost').pathname);if(p.endsWith('/'))p+='index.html';const f=path.resolve(web,'.'+p);if(!f.startsWith(web+path.sep))throw Error();const bytes=fs.readFileSync(f);res.writeHead(200,{'Content-Type':mime[path.extname(f)]||'application/octet-stream'});res.end(bytes);}catch{res.writeHead(404);res.end();}});
 await new Promise(r=>server.listen(0,'127.0.0.1',r));const base='http://127.0.0.1:'+server.address().port+'/';
 browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 const context=await browser.newContext({viewport:{width:1440,height:1000},acceptDownloads:true});
 const telemetry=c=>{c.on('request',r=>{if(/^https?:/.test(r.url())&&!r.url().startsWith(base))report.externas.push(r.url());});c.on('page',p=>{p.on('pageerror',e=>report.errores.push(String(e)));p.on('requestfailed',r=>report.fallos_red.push(r.url()));});};telemetry(context);
 const page=await context.newPage();let refs=[],cites=[];
 for(const file of ['index.html','territorio.html','especializacion.html','referencias.html']){
  await page.goto(base+file,{waitUntil:'networkidle'});
  check('Página disponible '+file,await page.locator('h1').count()>0);
  check('Sin enlaces locales PDF '+file,await page.locator('a[href$=".pdf"]:not([href^="http"])').count()===0);
  check('Sin actividades ni navegación residual '+file,await page.locator('[id="actividades-territorio"],a[href*="actividades-territorio"]').count()===0&&!(await page.locator('body').innerText()).includes('I.3 Actividades'));
  if(file==='referencias.html'){refs=await page.locator('.csl-entry').evaluateAll(es=>es.map(e=>e.id));check('Bibliografía única 33 entradas',refs.length===33&&new Set(refs).size===refs.length);}
  else cites.push(...await page.locator('.citation a').evaluateAll(as=>as.map(a=>a.getAttribute('href'))));
  if(file==='territorio.html'){
   check('Seis exploradores integrados',await page.locator('iframe.territorio').count()===6);
   await page.waitForFunction(()=>[...document.querySelectorAll('iframe.territorio')].every(f=>f.dataset.alturaAjustada==='true'),{},{timeout:15000}).catch(()=>{});
   const heights=await page.locator('iframe.territorio').evaluateAll(fs=>fs.map(f=>({src:f.getAttribute('src'),h:f.getBoundingClientRect().height,ajustada:f.dataset.alturaAjustada})));
   check('Altura coordinada sin recortes de iframe',heights.every(f=>f.ajustada==='true'&&f.h>=600),heights);
   const bodies=await Promise.all(page.frames().filter(f=>f!==page.mainFrame()).map(async f=>({src:path.basename(f.url()),...await f.evaluate(()=>({contenido:document.documentElement.scrollHeight,alto:innerHeight}))})));
   check('Contenido completo dentro de iframes escritorio',bodies.every(d=>d.contenido<=d.alto+4),bodies);
   for(const frame of page.frames().filter(f=>f!==page.mainFrame())){
    check('Controles y datos integrados '+path.basename(frame.url()),await frame.locator('input[type="search"],input[type="text"]').count()>0&&await frame.locator('table').count()>0);
   }
  }
  if(file==='especializacion.html'){await page.waitForFunction(()=>document.querySelectorAll('mjx-container').length>=18).catch(()=>{});check('Cinco ecuaciones conservadas',await page.locator('mjx-container[display=true]').count()>=5&&await page.locator('mjx-merror').count()===0);}
  await shot(page,file.replace('.html','')+'-desktop');
 }
 check('Citas resueltas en bibliografía',cites.every(c=>refs.includes(c.split('#')[1])),cites.length);
 await page.goto(base+'index.html',{waitUntil:'networkidle'});await page.locator('.summary a[href="territorio.html"]').first().click();
 check('Navegación al capítulo',page.url().endsWith('territorio.html'));
 await page.locator('.fa-search').first().click();await page.locator('#search-box').fill('Frontera Sur');await page.waitForTimeout(500);
 check('Búsqueda del libro',await page.locator('.summary li.chapter:visible a[href*="territorio.html"]').count()>0);
 await page.locator('#search-box').fill('zzzyyyxxx123456');await page.waitForTimeout(300);check('Búsqueda vacía clara',await page.locator('.summary li.chapter:visible').count()===0);
 const mobile=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,acceptDownloads:true});telemetry(mobile);
 const touch=await mobile.newPage();
 for(const file of ['index.html','territorio.html','especializacion.html','referencias.html']){
  await touch.goto(base+file,{waitUntil:'networkidle'});const dims=await touch.evaluate(()=>({html:document.documentElement.scrollWidth,w:innerWidth,section:document.querySelector('section.normal').scrollWidth,client:document.querySelector('section.normal').clientWidth}));
  check('Lectura móvil '+file,dims.html<=dims.w+1&&dims.section<=dims.client+1,dims);await shot(touch,file.replace('.html','')+'-movil');
  if(file==='territorio.html'){
   await touch.waitForFunction(()=>[...document.querySelectorAll('iframe.territorio')].every(f=>f.dataset.alturaAjustada==='true')).catch(()=>{});
   const bodies=await Promise.all(touch.frames().filter(f=>f!==touch.mainFrame()).map(async f=>({src:path.basename(f.url()),...await f.evaluate(()=>({contenido:document.documentElement.scrollHeight,alto:innerHeight}))})));
   check('Contenido completo dentro de iframes móvil',bodies.every(d=>d.contenido<=d.alto+4),bodies);
  }
 }
 for(const name of figures){
  await page.goto(base+'recursos/'+name+'.html',{waitUntil:'networkidle'});await shot(page,name+'-desktop');
  await touch.goto(base+'recursos/'+name+'.html',{waitUntil:'networkidle'});
  check('Explorador móvil sin desborde '+name,await touch.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  const specific={'F01-relieve-localizacion':'path[data-state="26"]','F02-clima-suelos':'path[data-state="26"]','F03-agua-renovable':'[data-rha="XI"]','F04-recursos':'#estado-26','F05-agua-poblacion':'[data-chart="XI"]','F06-mecanismos-territoriales':'[data-mobile-node="acceso"]'};
  const target=touch.locator(specific[name]||'svg [role="button"]:visible,svg [role="checkbox"]:visible').first();
  if(await target.count()){
   await target.scrollIntoViewIfNeeded();const before=await target.getAttribute('aria-pressed')||await target.getAttribute('aria-checked');
   await target.tap();await touch.waitForTimeout(100);
   const after=await target.getAttribute('aria-pressed')||await target.getAttribute('aria-checked');
   check('Selección táctil persistente '+name,before!==after&&after!==null,{before,after});
   await target.focus();await target.press('Enter');const key=await target.getAttribute('aria-pressed')||await target.getAttribute('aria-checked');
   check('Selección por teclado '+name,key!==after,{after,key});
  }else check('Selección táctil '+name,false,'Sin elemento accesible');
  await touch.evaluate(()=>scrollTo(0,0));await shot(touch,name+'-movil');
  await page.goto(pathToFileURL(path.join(root,'assets/capitulo-01/interactivos',name+'.html')).href,{waitUntil:'load'});
  check('HTML portátil local '+name,await page.locator('input[type="search"],input[type="text"]').count()>0&&await page.locator('tbody tr').count()>0);
 }
 check('Sin errores JavaScript',report.errores.length===0,report.errores);
 check('Sin recursos externos',report.externas.length===0,report.externas);
 check('Sin fallos de red',report.fallos_red.length===0,report.fallos_red);
}
main().catch(e=>{report.error=String(e);report.stack=e.stack;}).finally(async()=>{if(browser)await browser.close();if(server)await new Promise(r=>server.close(r));report.resultado=report.error||report.pruebas.some(p=>!p.correcto)?'incidencias':'correcto';fs.writeFileSync(path.join(root,'seguimiento/verificacion-web-B02-funcional.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({resultado:report.resultado,pruebas:report.pruebas.length,fallos:report.pruebas.filter(p=>!p.correcto),error:report.error}));if(report.resultado!=='correcto')process.exitCode=1;});
