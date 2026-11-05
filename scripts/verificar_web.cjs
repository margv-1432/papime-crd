// Verificación B01 con Chrome local y Playwright del runtime. No instala nada.
// node scripts/verificar_web.cjs http://127.0.0.1:8765/
// Sin argumento comprueba entregas/web mediante file://.
const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require('C:/Program Files/WindowsApps/OpenAI.CodexPrimaryRuntime.v26-1030-493-0_26.1030.493.0_x64__3k8sg7r9htsxt/dependencies/node/node_modules/playwright');
const root = process.cwd();
let base = process.argv[2] === '--serve' ? '' : process.argv[2] || pathToFileURL(path.join(root,'entregas/web/')).href;
const qa = path.join(root,'tmp/qa-web');fs.mkdirSync(qa,{recursive:true});
const report = {fecha:'2026-11-05',base,pruebas:[],errores_consola:[],solicitudes_externas:[],fallos_red:[],capturas:[]};
let browser,server;
function check(nombre,ok,detalle){report.pruebas.push({nombre,resultado:ok?'correcto':'FALLO',detalle});return ok;}
function parseCSV(s){const rows=[];let row=[],v='',quoted=false;s=s.replace(/^\uFEFF/,'');for(let i=0;i<s.length;i++){const c=s[i];if(c==='"'){if(quoted&&s[i+1]==='"'){v+='"';i++;}else quoted=!quoted;}else if(c===','&&!quoted){row.push(v);v='';}else if((c==='\r'||c==='\n')&&!quoted){if(c==='\r'&&s[i+1]==='\n')i++;row.push(v);if(row.some(x=>x!==''))rows.push(row);row=[];v='';}else v+=c;}if(v||row.length){row.push(v);rows.push(row);}return rows;}
async function shot(page,name){const p=path.join(qa,name);await page.screenshot({path:p,fullPage:false});report.capturas.push(path.relative(root,p));}
async function main(){
 if(process.argv[2]==='--serve'){
  const http=require('node:http'),web=path.join(root,'entregas/web');
  const mime={'.html':'text/html; charset=utf-8','.js':'application/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.json':'application/json; charset=utf-8','.png':'image/png','.svg':'image/svg+xml','.woff':'font/woff','.woff2':'font/woff2','.ttf':'font/ttf','.pdf':'application/pdf','.csv':'text/csv; charset=utf-8'};
  server=http.createServer((req,res)=>{try{let local=decodeURIComponent(new URL(req.url,'http://localhost').pathname);if(local.endsWith('/'))local+='index.html';const target=path.resolve(web,'.'+local);if(!target.startsWith(web+path.sep)){res.writeHead(403);res.end();return;}const bytes=fs.readFileSync(target);res.writeHead(200,{'Content-Type':mime[path.extname(target)]||'application/octet-stream'});res.end(bytes);}catch{res.writeHead(404);res.end('No encontrado');}});
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));base='http://127.0.0.1:'+server.address().port+'/';report.base=base;
 }
 browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',args:['--disable-gpu']});
 const context=await browser.newContext({viewport:{width:1440,height:1050},acceptDownloads:true});
 const page=await context.newPage();
 context.on('request',r=>{const u=r.url();if(/^https?:/.test(u)&&!/^https?:\/\/(127\.0\.0\.1|localhost)(:|\/)/.test(u))report.solicitudes_externas.push(u);});
 page.on('pageerror',e=>report.errores_consola.push(String(e)));
 page.on('requestfailed',r=>report.fallos_red.push({url:r.url(),error:r.failure()?.errorText}));
 await page.goto(new URL('index.html',base).href,{waitUntil:'networkidle'});
 check('Presentación navegable',await page.locator('h1').filter({hasText:'Presentación del piloto'}).count()>0,page.url());
 await shot(page,'01-portada-desktop.png');
 await page.locator('.summary a[href="especializacion.html"]').first().click();
 await page.waitForURL('**/especializacion.html');
 await page.waitForFunction(()=>document.querySelectorAll('mjx-container').length>=18,{},{timeout:15000}).catch(()=>{});
 const math=await page.evaluate(()=>({contenedores:document.querySelectorAll('mjx-container').length,displays:document.querySelectorAll('mjx-container[display="true"]').length,inline:document.querySelectorAll('mjx-container:not([display="true"])').length,errores:document.querySelectorAll('mjx-merror,merror,[data-mjx-error]').length,formulas:document.querySelectorAll('.math').length}));
 check('Navegación presentación a especialización',/especializacion\.html/.test(page.url()),page.url());
 check('Ecuaciones MathJax renderizadas',math.displays>=5&&math.inline>=10&&math.errores===0,math);
 const refsEspecial=await page.locator('.csl-entry').count();
 const enlacesCita=await page.locator('.citation a').evaluateAll(as=>as.map(a=>({href:a.getAttribute('href'),texto:a.textContent})));
 await shot(page,'02-especializacion-desktop.png');
 const frame=page.frameLocator('iframe.grafico-interactivo');
 await frame.locator('#ksi g.fila').last().waitFor();
 check('Gráfico integrado con 32 barras',await frame.locator('#ksi g.fila').count()===32,await frame.locator('#ksi g.fila').count());
 const data=await frame.locator('#f07-datos').textContent();const embedded=JSON.parse(data);
 const originals=parseCSV(fs.readFileSync(path.join(root,'datos/preparados/capitulo-02/KSI_entidades.csv'),'utf8'));
 const header=originals.shift();const key=header.indexOf('cve_ent'),ksiIndex=header.indexOf('KSI');
 check('Valores embebidos iguales al CSV preparado',embedded.filas.length===32&&embedded.filas.every(d=>originals.some(r=>r[key]===d.cve_ent&&r[ksiIndex]===d.KSI_texto)),{filas:embedded.filas.length});
 const inicial=await frame.locator('#ksi g.fila').evaluateAll(gs=>gs.map(g=>g.getAttribute('data-entidad')));
 check('Orden inicial descendente',inicial[0]==='04'&&inicial.length===32,inicial.slice(0,5));
 await frame.locator('#entidad').selectOption('05');
 const seleccionado=await frame.locator('#valor-exacto').textContent();
 check('Selección conserva 32 barras y destaca Coahuila',await frame.locator('#ksi g.fila').count()===32&&await frame.locator('#ksi g.fila.seleccionada[data-entidad="05"]').count()===1&&seleccionado.includes(embedded.filas.find(d=>d.cve_ent==='05').KSI_texto),seleccionado);
 await frame.locator('#orden').selectOption('alfabetico');
 const alfabetico=await frame.locator('#ksi g.fila').evaluateAll(gs=>gs.map(g=>g.getAttribute('data-entidad')));
 check('Orden alfabético sin perder selección',alfabetico[0]==='01'&&await frame.locator('#entidad').inputValue()==='05',alfabetico.slice(0,6));
 const campeche=frame.locator('#ksi g.fila[data-entidad="04"]');await campeche.focus();await campeche.press('Enter');
 check('Selección con teclado',await frame.locator('#entidad').inputValue()==='04',await frame.locator('#lectura-titulo').textContent());
 await frame.locator('#tabla-datos summary').click();
 check('Tabla completa accesible',await frame.locator('#tabla-cuerpo tr').count()===32&&await frame.locator('#tabla-datos').getAttribute('open')!==null,await frame.locator('#tabla-cuerpo tr').count());
 const downloadPromise=page.waitForEvent('download');await frame.locator('#descargar').click();const download=await downloadPromise;const downloaded=await download.path();const downloadedRows=parseCSV(fs.readFileSync(downloaded,'utf8'));const originalRows=parseCSV(fs.readFileSync(path.join(root,'datos/preparados/capitulo-02/KSI_entidades.csv'),'utf8'));
 check('Descarga CSV completa e idéntica en valores',JSON.stringify(downloadedRows)===JSON.stringify(originalRows),{nombre:download.suggestedFilename(),filas:downloadedRows.length-1});
 await page.locator('iframe.grafico-interactivo').scrollIntoViewIfNeeded();await shot(page,'03-grafico-integrado-desktop.png');
 await page.locator('.summary a[href="referencias.html"]').first().click();await page.waitForURL('**/referencias.html');
 const references=await page.locator('.csl-entry').count();
 const referenceIds=await page.locator('.csl-entry').evaluateAll(es=>es.map(e=>e.id));
 check('Navegación a referencias',references===3,{referencias:references,ids:referenceIds});
 check('Referencias sin duplicación en el capítulo',refsEspecial===0&&references===3,{enCapitulo:refsEspecial,enReferencias:references});
 check('Citas enlazadas al destino existente',enlacesCita.every(c=>c.href&&referenceIds.includes(c.href.split('#')[1])),enlacesCita);
 await shot(page,'04-referencias-desktop.png');
 // La búsqueda de GitBook carga search_index.json por HTTP.
 if(/^http/.test(base)){
  try{
   await page.locator('.fa-search').first().click();const input=page.locator('#search-box');await input.waitFor({state:'visible',timeout:3000});await input.fill('Campeche');await page.waitForTimeout(500);const results=await page.locator('.summary li.chapter:visible').count();const links=await page.locator('.summary li.chapter:visible a').evaluateAll(as=>as.map(a=>a.getAttribute('href')));await input.fill('zzzyyyxxx12345');await page.waitForTimeout(300);const noResults=await page.locator('.summary li.chapter:visible').count();check('Búsqueda del libro',results>0&&links.some(u=>u.includes('especializacion.html'))&&noResults===0,{coincidencias:results,enlaces:links,sinCoincidencias:noResults});await input.fill('');await input.press('Escape');
  }catch(e){check('Búsqueda del libro',false,String(e));}
 }else check('Búsqueda del libro',true,'No se prueba por file://; requiere servidor HTTP documentado.');
 await page.setViewportSize({width:360,height:900});
 for(const file of ['index.html','especializacion.html','referencias.html']){
  await page.goto(new URL(file,base).href,{waitUntil:'networkidle'});
  if(file==='especializacion.html')await page.waitForFunction(()=>document.querySelectorAll('mjx-container').length>=18,{},{timeout:10000}).catch(()=>{});
  const overflow=await page.evaluate(()=>{const b=document.querySelector('.book-body'), p=document.querySelector('.page-inner'), s=document.querySelector('section.normal');return{viewport:innerWidth,html:document.documentElement.scrollWidth,body:document.body.scrollWidth,bookBody:{client:b.clientWidth,scroll:b.scrollWidth},inner:{client:p.clientWidth,scroll:p.scrollWidth},content:{client:s.clientWidth,scroll:s.scrollWidth}};});
  check('Móvil 360 sin desbordamiento '+file,overflow.html<=360&&overflow.body<=360&&overflow.content.scroll<=overflow.content.client+1,overflow);
  await shot(page,'movil-'+file.replace('.html','.png'));
  if(file==='especializacion.html'){
   const ff=page.frameLocator('iframe.grafico-interactivo');await ff.locator('#ksi g.fila').last().waitFor();const mobile=await ff.locator('body').evaluate(b=>({viewport:innerWidth,ancho:b.scrollWidth,barras:document.querySelectorAll('#ksi g.fila').length}));check('Gráfico móvil 360 sin desbordamiento',mobile.ancho<=mobile.viewport&&mobile.barras===32,mobile);
  }
 }
 const standalone=await context.newPage();await standalone.setViewportSize({width:360,height:900});await standalone.goto(new URL('recursos/F07-ksi.html',base).href,{waitUntil:'networkidle'});await shot(standalone,'05-grafico-autonomo-movil.png');
 check('Gráfico autónomo navegable',await standalone.locator('#ksi g.fila').count()===32,standalone.url());
 check('Sin solicitudes externas',report.solicitudes_externas.length===0,report.solicitudes_externas);
 check('Sin errores JavaScript',report.errores_consola.length===0,report.errores_consola);
 await browser.close();browser=null;
}
main().catch(e=>{report.error=String(e);report.stack=e.stack;}).finally(async()=>{
 if(browser)await browser.close().catch(()=>{});
 if(server)await new Promise(resolve=>server.close(resolve));
 report.resultado=report.error||report.pruebas.some(p=>p.resultado==='FALLO')?'incidencias':'correcto';
 fs.mkdirSync(path.join(root,'seguimiento'),{recursive:true});fs.writeFileSync(path.join(root,'seguimiento/verificacion-web.json'),JSON.stringify(report,null,2)+'\n');
 console.log(JSON.stringify({resultado:report.resultado,pruebas:report.pruebas.length,fallos:report.pruebas.filter(p=>p.resultado==='FALLO'),error:report.error,solicitudes_externas:report.solicitudes_externas,errores:report.errores_consola},null,2));
 if(report.resultado!=='correcto')process.exitCode=1;
});
