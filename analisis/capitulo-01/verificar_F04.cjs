// Cotejo del HTML autónomo con las tablas usadas por PDF y prosa.
const fs=require('node:fs'),path=require('node:path'),{pathToFileURL}=require('node:url');
const {chromium}=require('C:/Program Files/WindowsApps/OpenAI.CodexPrimaryRuntime.v26-1030-493-0_26.1030.493.0_x64__3k8sg7r9htsxt/dependencies/node/node_modules/playwright');
const root=process.cwd(),tests=[],errors=[],requests=[];
function check(name,ok,detail){tests.push({prueba:name,correcta:!!ok,detalle:detail});if(!ok)throw Error(name)}
(async()=>{
const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',args:['--disable-gpu']});
try{
const page=await browser.newPage({viewport:{width:1100,height:850},acceptDownloads:true});
page.on('pageerror',e=>errors.push(String(e)));page.on('request',r=>{if(/^https?:/.test(r.url()))requests.push(r.url())});
await page.goto(pathToFileURL(path.join(root,'assets/capitulo-01/interactivos/F04-recursos.html')).href,{waitUntil:'networkidle'});
check('Cobre:13barras y32registros',await page.locator('#chart svg rect').count()===13&&await page.locator('#tbody tr').count()===32);
check('Cobre:Sonora550597.5t',await page.locator('#tbody tr').first().textContent().then(s=>s.includes('Sonora')&&s.includes('550,597.5')));
check('Cobre:guion,ausencia,cero',await page.locator('#tbody tr').allTextContents().then(rows=>rows.some(s=>s.includes('Jalisco')&&s.includes('cero explicito'))&&rows.filter(s=>s.includes('guion publicado')).length===6&&rows.filter(s=>s.includes('sin fila en cuadro')).length===13));
await page.selectOption('#panel','madera');check('Madera:32valores',await page.locator('#chart svg rect').count()===32&&await page.locator('#tbody tr').count()===32);
await page.selectOption('#panel','pesca');check('Pesca:31totales y31acuacultura',await page.locator('#chart svg rect').count()===62&&await page.locator('#tbody tr').count()===32);
check('Pesca:CDMXsin fila',await page.locator('#tbody tr').filter({hasText:'Ciudad de México'}).textContent().then(s=>(s.match(/Sin fila/g)||[]).length===2));
check('Pesca:redondeo nacional explícito',await page.locator('#limits').textContent().then(s=>s.includes('304 731')&&s.includes('304 732')));
await page.selectOption('#order','entidad');check('Orden estatal conserva clave01',await page.locator('#tbody tr').first().textContent().then(s=>s.startsWith('01')));
await page.selectOption('#panel','cubierta');check('Cubierta:11grupos yPNG1600x1006',await page.locator('#coverage .legend span').count()===11&&await page.locator('#coverage img').evaluate(e=>e.naturalWidth===1600&&e.naturalHeight===1006));
check('Cubierta:tabla numérica oculta',!await page.locator('#table-section').isVisible());
await page.locator('details').last().locator('summary').click();
for(const a of await page.locator('a[download]').all()){
 const name=await a.getAttribute('download'),href=await a.getAttribute('href');
 const bytes=Buffer.from(href.split(',')[1],'base64');
 check('Descarga exacta '+name,bytes.equals(fs.readFileSync(path.join(root,'datos/preparados/capitulo-01',name))),bytes.length);
}
await page.locator('#reset').click();check('Restablecer vista inicial',await page.locator('#panel').inputValue()==='cobre'&&await page.locator('#order').inputValue()==='valor');
await page.locator('#panel').focus();await page.keyboard.press('ArrowDown');await page.keyboard.press('Enter');check('Selección por teclado',await page.locator('#panel').inputValue()==='cubierta');
await page.setViewportSize({width:360,height:900});
for(const panel of ['cobre','cubierta','madera','pesca']){
 await page.selectOption('#panel',panel);
 const bounds=await page.evaluate(()=>({viewport:innerWidth,html:document.documentElement.scrollWidth,body:document.body.scrollWidth}));
 check('Móvil360 sin desbordamiento '+panel,bounds.html<=360&&bounds.body<=360,bounds);
}
check('Sin JavaScript errores',errors.length===0,errors);check('Sin solicitudes externas',requests.length===0,requests);
const dir=path.join(root,'tmp/qa-F04');fs.mkdirSync(dir,{recursive:true});await page.screenshot({path:path.join(dir,'movil-pesca.png'),fullPage:false});
}finally{await browser.close()}
})().catch(e=>{errors.push(String(e));process.exitCode=1}).finally(()=>{
const report={fecha:'2026-11-05',resultado:errors.length?'incidencias':'correcto',pruebas:tests,errores:errors,solicitudes_externas:requests};
fs.writeFileSync(path.join(root,'seguimiento/verificacion-F04-web.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({resultado:report.resultado,pruebas:tests.length,errores:errors}));
});
