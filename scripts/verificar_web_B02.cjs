// QA de integración B02. Reutiliza Chrome y Playwright del entorno de B01.
const fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const {chromium}=require('C:/Program Files/WindowsApps/OpenAI.CodexPrimaryRuntime.v26-1030-493-0_26.1030.493.0_x64__3k8sg7r9htsxt/dependencies/node/node_modules/playwright');
const root=process.cwd(),web=path.join(root,'entregas/web'),qa=path.join(root,'tmp/qa-web-B02');fs.mkdirSync(qa,{recursive:true});
const report={fecha:'2026-11-06',pruebas:[],errores:[],externas:[],fallos_red:[],capturas:[]};
let browser,server;
const check=(prueba,ok,detalle='')=>report.pruebas.push({prueba,correcto:!!ok,detalle});
const norm=s=>s.replace(/^\uFEFF/,'').replace(/\r\n/g,'\n').trim();
async function shot(page,name){let p=path.join(qa,name+'.png');await page.screenshot({path:p,fullPage:false});report.capturas.push(path.relative(root,p));}
async function main(){
 const mime={'.html':'text/html; charset=utf-8','.js':'application/javascript','.css':'text/css','.csv':'text/csv','.svg':'image/svg+xml','.pdf':'application/pdf','.png':'image/png','.json':'application/json'};
 server=http.createServer((req,res)=>{try{let p=decodeURIComponent(new URL(req.url,'http://localhost').pathname);if(p.endsWith('/'))p+='index.html';let f=path.resolve(web,'.'+p);if(!f.startsWith(web+path.sep))throw Error();const bytes=fs.readFileSync(f);res.writeHead(200,{'Content-Type':mime[path.extname(f)]||'application/octet-stream'});res.end(bytes);}catch{res.writeHead(404);res.end();}});
 await new Promise(r=>server.listen(0,'127.0.0.1',r));const base='http://127.0.0.1:'+server.address().port+'/';report.base=base;
 browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 const context=await browser.newContext({viewport:{width:1440,height:1050},acceptDownloads:true});
 context.on('request',r=>{if(/^https?:/.test(r.url())&&!r.url().startsWith(base))report.externas.push(r.url());});
 const page=await context.newPage();page.on('pageerror',e=>report.errores.push(String(e)));page.on('requestfailed',r=>report.fallos_red.push(r.url()));
 let refs=[],cites=[];
 for(const file of ['index.html','territorio.html','especializacion.html','referencias.html']){
  await page.goto(base+file,{waitUntil:'networkidle'});check('Página disponible '+file,await page.locator('h1').count()>0);
  if(file==='referencias.html'){refs=await page.locator('.csl-entry').evaluateAll(es=>es.map(e=>e.id));check('Bibliografía única y completa',refs.length===33&&new Set(refs).size===refs.length,refs.length);}
  else {check('Sin bibliografía duplicada '+file,await page.locator('.csl-entry').count()===0);cites.push(...await page.locator('.citation a').evaluateAll(as=>as.map(a=>a.getAttribute('href'))));}
  if(file==='territorio.html'){
   check('Seis figuras integradas',await page.locator('iframe.territorio').count()===6);
   const frames=page.frames().filter(f=>f!==page.mainFrame());check('Seis documentos de figuras cargados',frames.length===6,frames.map(f=>f.url()));
   for(let i=0;i<frames.length;i++){
    const frame=frames[i];check('Figura accesible F0'+(i+1),(await frame.locator('body').innerText()).length>200);
    const selects=frame.locator('select');for(let j=0;j<await selects.count();j++){const s=selects.nth(j),opts=await s.locator('option').evaluateAll(os=>os.map(o=>o.value));if(opts.length>1)await s.selectOption(opts[opts.length-1]);}
    const radios=frame.locator('input[type=radio]');if(await radios.count()>1)await radios.last().check();
    const d=frame.locator('details summary');if(await d.count())await d.first().click();
   }
   const f1=page.frameLocator('iframe[src="recursos/F01-relieve-localizacion.html"]');check('F01 tabla145localidades',await f1.locator('tbody tr').count()===145);
   const f2=page.frameLocator('iframe[src="recursos/F02-clima-suelos.html"]');await f2.locator('input[value=suelo]').focus();await f2.locator('input[value=suelo]').press('Space');check('F02 control por teclado',await f2.locator('input[value=suelo]').isChecked());
   const f3=page.frameLocator('iframe[src="recursos/F03-agua-renovable.html"]');await f3.locator('#region').selectOption('XI');check('F03 selecciónXI', (await f3.locator('#lectura').innerText()).includes('158'));
   const f5=page.frameLocator('iframe[src="recursos/F05-agua-poblacion.html"]');await f5.locator('#region').selectOption('III');check('F05 selecciónIII',(await f5.locator('#lectura').innerText()).includes('Pacífico'));
   const dp=page.waitForEvent('download');await f5.locator('#descargar').click();const dload=await dp;const p=await dload.path();check('Descarga hídrica exacta',norm(fs.readFileSync(p,'utf8'))===norm(fs.readFileSync(path.join(root,'datos/preparados/capitulo-01/F03_F05_agua_poblacion_2022.csv'),'utf8')));
   await page.locator('#fig-f03').scrollIntoViewIfNeeded();await shot(page,'figuras-desktop');
  }
  if(file==='especializacion.html'){await page.waitForFunction(()=>document.querySelectorAll('mjx-container').length>=18).catch(()=>{});check('Piloto conservado y ecuaciones válidas',await page.locator('mjx-container[display=true]').count()>=5&&await page.locator('mjx-merror').count()===0);}
  await shot(page,file.replace('.html','')+'-desktop');
 }
 check('Citas enlazadas a referencias',cites.every(c=>refs.includes(c.split('#')[1])),cites.length);
 await page.goto(base+'index.html',{waitUntil:'networkidle'});await page.locator('.summary a[href="territorio.html"]').first().click();check('Navegación índice al capítulo',page.url().endsWith('territorio.html'));
 await page.locator('.fa-search').first().click();await page.locator('#search-box').fill('Frontera Sur');await page.waitForTimeout(600);check('Búsqueda encuentra capítulo',await page.locator('.summary li.chapter:visible a[href*="territorio.html"]').count()>0);await page.locator('#search-box').fill('zzzyyyxxx123456');await page.waitForTimeout(300);check('Búsqueda sin coincidencias',await page.locator('.summary li.chapter:visible').count()===0);
 await page.locator("#search-box").fill("");await page.locator("#search-box").press("Escape");await page.setViewportSize({width:360,height:900});
 for(const file of ['index.html','territorio.html','especializacion.html','referencias.html']){
  await page.goto(base+file,{waitUntil:'networkidle'});
  const dims=await page.evaluate(()=>({html:document.documentElement.scrollWidth,body:document.body.scrollWidth,content:document.querySelector('section.normal').scrollWidth,client:document.querySelector('section.normal').clientWidth,overflow:[...document.querySelectorAll('section.normal *')].filter(e=>e.scrollWidth>e.clientWidth+2&&e.clientWidth>0).slice(0,8).map(e=>({tag:e.tagName,cls:e.className,width:e.clientWidth,scroll:e.scrollWidth}))}));check('Texto360px '+file,dims.html<=360&&dims.body<=360&&dims.content<=dims.client+1,dims);await shot(page,file.replace('.html','')+'-movil');
 }
 for(const f of ['F01-relieve-localizacion','F02-clima-suelos','F03-agua-renovable','F04-recursos','F05-agua-poblacion','F06-mecanismos-territoriales']){
  await page.goto(base+'recursos/'+f+'.html',{waitUntil:'networkidle'});check('Figura autónoma móvil '+f,await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await shot(page,f+'-movil');
 }
 check('Sin errores JavaScript',report.errores.length===0,report.errores);check('Sin recursos externos',report.externas.length===0,report.externas);check('Sin fallos de red',report.fallos_red.length===0,report.fallos_red);
}
main().catch(e=>{report.error=String(e);report.stack=e.stack;}).finally(async()=>{if(browser)await browser.close();if(server)await new Promise(r=>server.close(r));report.resultado=report.error||report.pruebas.some(p=>!p.correcto)?'incidencias':'correcto';fs.writeFileSync(path.join(root,'seguimiento/verificacion-web-B02.json'),JSON.stringify(report,null,2));console.log(JSON.stringify({resultado:report.resultado,pruebas:report.pruebas.length,fallos:report.pruebas.filter(p=>!p.correcto),error:report.error}));if(report.resultado!=='correcto')process.exitCode=1;});
