"""Verificación de integración B02: fuentes, cifras, referencias, enlaces y PDF."""
from pathlib import Path
import csv,hashlib,json,re
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from pypdf import PdfReader
R=Path(__file__).resolve().parents[1];W=R/'entregas/web';checks=[]
def ck(n,c,d=''):checks.append(dict(prueba=n,correcto=bool(c),detalle=d))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
class HTML(HTMLParser):
 def __init__(self,s):super().__init__();self.ids=[];self.links=[];self.feed(s)
 def handle_starttag(self,t,a):
  a=dict(a)
  if 'id' in a:self.ids.append(a['id'])
  for k in ('href','src'):
   if k in a:self.links.append((t,k,a[k]))
pages={p.resolve():HTML(p.read_text(encoding='utf8')) for p in W.glob('*.html')}
bad=[];count=0
for p,h in pages.items():
 ck('IDs únicos '+p.name,len(h.ids)==len(set(h.ids)))
 for t,k,v in h.links:
  u=urlsplit(v)
  if u.scheme or u.netloc:continue
  target=(p.parent/unquote(u.path)).resolve() if u.path else p
  if target.is_dir():target/= 'index.html'
  count+=1
  if not target.exists():bad.append(str(target))
  elif u.fragment and target.suffix=='.html':
   x=pages.get(target) or HTML(target.read_text(encoding='utf8'))
   if unquote(u.fragment) not in x.ids:bad.append(str(target)+'#'+u.fragment)
ck('Enlaces y recursos locales',not bad,dict(comprobados=count,rotos=bad))
bib=(R/'libro/bibliografia.bib').read_text(encoding='utf8');keys=re.findall(r'@\w+\{([^,]+),',bib)
text=(R/'libro/capitulos/01-territorio.Rmd').read_text(encoding='utf8')
cites=set(re.findall(r'@([A-Za-z][A-Za-z0-9_-]+)',text))
ck('Claves bibliográficas únicas',len(keys)==len(set(keys)))
ck('30citas B02 resueltas',len(cites)==30 and cites<=set(keys))
ck('Sin notas editoriales pendientes',not re.search('Nota editorial|B02-GEOGRAFIA|TODO|TBD',text))
ck('Sin guiones largos',chr(0x2014) not in text)
water=list(csv.DictReader((R/'datos/preparados/capitulo-01/F03_F05_agua_poblacion_2022.csv').open(encoding='utf-8-sig')))
ck('Cifras agua de prosa',sum(int(r['agua_renovable_hm3_anio']) for r in water)==461640 and abs(sum(float(r['poblacion_millones']) for r in water)-129.35)<1e-10)
for r in water:
 if r['rha']=='XI':ck('PorcentajesXI de prosa',round(float(r['porcentaje_agua']),1)==34.2 and round(float(r['porcentaje_poblacion']),1)==6.4)
 if r['rha']=='III':ck('PorcentajesIII de prosa',round(float(r['porcentaje_agua']),1)==5.8 and round(float(r['porcentaje_poblacion']),1)==3.7)
pdfs={}
for name in ('PAPIME-B02-capitulo-I.pdf','PAPIME-libro-avance-B02.pdf'):
 p=R/'entregas/pdf'/name;reader=PdfReader(p);s='\n'.join(x.extract_text() or '' for x in reader.pages)
 ck('PDF sin páginas vacías '+name,all((x.extract_text() or '').strip() for x in reader.pages),len(reader.pages))
 ck('Seis rótulos en '+name,all('I.2.'+str(i) in s for i in range(1,7)))
 ck('Cifras integradas '+name,all(v in s for v in ('461,640','129.35','550,597.50','34.2','6.4')))
 ck('PDF web idéntico '+name,sha(p)==sha(W/('papime-libro.pdf' if 'avance' in name else name)))
 pdfs[name]=dict(paginas=len(reader.pages),sha256=sha(p),bytes=p.stat().st_size)
figures=['F01-relieve-localizacion','F02-clima-suelos','F03-agua-renovable','F04-recursos','F05-agua-poblacion','F06-mecanismos-territoriales']
for f in figures:
 for ext,folder in [('html','interactivos'),('pdf','figuras-estaticas'),('png','figuras-estaticas')]:
  p=R/'assets/capitulo-01'/folder/(f+'.'+ext)
  ck('Recurso integrado idéntico '+f+'.'+ext,p.exists() and sha(p)==sha(W/'recursos'/p.name))
ck('Manuscrito rector intacto',sha(R/'referencias/manuscrito-base/PAPIME Libro.pdf')=='7bd8d8a23ff225a42728c167723c323a2bedebda7c999a9aa186df7a8e486b35')
report=dict(fecha='2026-11-05',resultado='correcto' if all(x['correcto'] for x in checks) else 'incidencias',pruebas=len(checks),pdfs=pdfs,comprobaciones=checks)
(R/'seguimiento/verificacion-proyecto-B02.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(dict(resultado=report['resultado'],pruebas=len(checks),fallos=[x for x in checks if not x['correcto']],pdfs=pdfs),ensure_ascii=False))
if report['resultado']!='correcto':raise SystemExit(1)
