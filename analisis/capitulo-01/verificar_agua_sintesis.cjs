// Reutiliza Chrome/Playwright del entorno B01. Sin instalación ni red externa.
const fs=require('node:fs'),path=require('node:path'),{pathToFileURL}=require('node:url');
const {chromium}=require('C:/Program Files/WindowsApps/OpenAI.CodexPrimaryRuntime.v26-1030-493-0_26.1030.493.0_x64__3k8sg7r9htsxt/dependencies/node/node_modules/playwright');
const root=process.cwd(),out=path.join(root,'tmp/qa-agua');fs.mkdirSync(out,{recursive:true});
const report={fecha:'2026-11-05',pruebas:[],errores:[],solicitudes_externas:[]};
const check=(nombre,ok,detalle)=>report.pruebas.push({nombre,resultado:ok?'correcto':'FALLO',detalle});
(async()=>{const server=require('node:http').createServer((req,res)=>{try{const target=path.resolve(root,'.'+new URL(req.url,'http://localhost').pathname);if(!target.startsWith(root+path.sep)){res.writeHead(403);res.end();return}const bytes=fs.readFileSync(target);res.writeHead(200,{'Content-Type':target.endsWith('.html')?'text/html; charset=utf-8':'application/octet-stream'});res.end(bytes)}catch{res.writeHead(404);res.end()}});await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));const base='http://127.0.0.1:'+server.address().port+'/';
const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',args:['--disable-gpu']});try{const context=await browser.newContext({viewport:{width:1500,height:1100},acceptDownloads:true});
const p=await context.newPage();p.on('pageerror',e=>report.errores.push(String(e)));p.on('request',r=>{if(/^https?:/.test(r.url())&&!r.url().startsWith(base))report.solicitudes_externas.push(r.url())});
for(const name of ['F03-agua-renovable','F05-agua-poblacion','F06-mecanismos-territoriales']){
await p.goto(new URL('assets/capitulo-01/interactivos/'+name+'.html',base).href,{waitUntil:'load'});
check(name+' SVG presente',await p.locator('svg').count()===1);
if(name.startsWith('F06')){check('F06 diez relaciones explorables',await p.locator('#mecanismo option').count()===10);await p.locator('#mecanismo').selectOption('9');check('F06 relación final consultable',(await p.locator('#lectura').textContent()).includes('condiciones futuras'));}
else{
const d=JSON.parse(await p.locator('#datos-agua').textContent());
check(name+' 13 regiones y denominadores',d.filas.length===13&&Math.abs(d.filas.reduce((s,r)=>s+r.porcentaje_agua,0)-100)<1e-9&&Math.abs(d.filas.reduce((s,r)=>s+r.porcentaje_poblacion,0)-100)<1e-9);
check(name+' símbolos seleccionables',await p.locator('[data-rha]').count()===13);
await p.locator('#region').selectOption('XI');check(name+' consulta Frontera Sur',(await p.locator('#lectura').textContent()).includes('158,021'));
const g=p.locator('[data-rha="XIII"]');await g.focus();await g.press('Enter');check(name+' teclado selecciona XIII',await p.locator('#region').inputValue()==='XIII');
await p.locator('#tabla-datos summary').click();check(name+' tabla completa',await p.locator('tbody tr').count()===13);
}
const download=p.waitForEvent('download');await p.locator('#descargar').click();const dl=await download;const got=fs.readFileSync(await dl.path(),'utf8').replace(/^\uFEFF/,'');
const expected=fs.readFileSync(path.join(root,'datos/preparados/capitulo-01',name.startsWith('F06')?'F06_relaciones.csv':'F03_F05_agua_poblacion_2022.csv'),'utf8');check(name+' CSV idéntico',got.replace(/\r\n/g,'\n')===expected.replace(/\r\n/g,'\n'));
await p.screenshot({path:path.join(out,name+'-desktop.png'),fullPage:true});
await p.setViewportSize({width:360,height:800});await p.screenshot({path:path.join(out,name+'-mobile.png'),fullPage:true});
check(name+' texto móvil sin desbordar',await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),await p.evaluate(()=>({scroll:document.documentElement.scrollWidth,width:innerWidth})));
await p.setViewportSize({width:1500,height:1100});
}
check('Sin errores JavaScript',report.errores.length===0,report.errores);check('Sin solicitudes externas',report.solicitudes_externas.length===0,report.solicitudes_externas);
}finally{await browser.close();await new Promise(resolve=>server.close(resolve))}
report.resultado=report.pruebas.every(p=>p.resultado==='correcto')?'correcto':'incidencias';fs.writeFileSync(path.join(root,'seguimiento/verificacion-agua-sintesis-web.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));if(report.resultado!=='correcto')process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
