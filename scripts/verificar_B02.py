"""Comprueba B02 HTML: integridad, prosa, fuentes y recursos de la entrega activa."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from collections import Counter
import csv,hashlib,json,re,subprocess
R=Path(__file__).resolve().parents[1]; W=R/'entregas/web'
BASE='8e55f7961f22b0bed0229418160178723710cab7'
checks=[]
def ck(name,ok,detail=''):checks.append(dict(prueba=name,correcto=bool(ok),detalle=detail))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def prior(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=R).decode('utf8')
class HTML(HTMLParser):
 def __init__(self,s):super().__init__();self.ids=[];self.links=[];self.parts=[];self.feed(s)
 def handle_starttag(self,t,a):
  a=dict(a)
  if 'id' in a:self.ids.append(a['id'])
  for k in ('href','src'):
   if k in a:self.links.append((t,k,a[k]))
 def handle_data(self,d):self.parts.append(d)
pages={p.resolve():HTML(p.read_text(encoding='utf8')) for p in W.glob('*.html')}
ck('Cuatro páginas del manual',all((W/name).resolve() in pages for name in ('index.html','territorio.html','especializacion.html','referencias.html')))
ck('Página de enlace inexistente', (W/'404.html').exists())
bad=[];count=0
for p,h in pages.items():
 ck('IDs únicos '+p.name,len(h.ids)==len(set(h.ids)))
 for t,k,v in h.links:
  u=urlsplit(v)
  if u.scheme or u.netloc:continue
  target=(p.parent/unquote(u.path)).resolve() if u.path else p
  if target.is_dir():target/='index.html'
  count+=1
  if not target.exists():bad.append(str(target))
  elif u.fragment and target.suffix=='.html':
   x=pages.get(target) or HTML(target.read_text(encoding='utf8'))
   if unquote(u.fragment) not in x.ids:bad.append(str(target)+'#'+u.fragment)
ck('Enlaces y recursos locales',not bad,dict(comprobados=count,rotos=bad))
ck('Sin PDF en entrega web activa',not list(W.rglob('*.pdf')))
source=(R/'libro/capitulos/01-territorio.Rmd').read_text(encoding='utf8')
old=prior('libro/capitulos/01-territorio.Rmd')
core=old.split('## I.3 Actividades de análisis territorial')[0].strip()
ck('Narrativa del capítulo conservada',source.strip()==core)
ck('Actividades retiradas de fuente y navegación',not any('actividades-territorio' in p.read_text(encoding='utf8') or 'I.3 Actividades' in p.read_text(encoding='utf8') for p in [R/'libro/capitulos/01-territorio.Rmd',*W.glob('*.html'),W/'search_index.json']))
bib=(R/'libro/bibliografia.bib').read_text(encoding='utf8');keys=re.findall(r'@\w+\{([^,]+),',bib)
cites=set(re.findall(r'@([A-Za-z][A-Za-z0-9_-]+)',source))
ck('30 claves citadas resueltas',len(cites)==30 and cites<=set(keys) and len(keys)==len(set(keys)))
ck('Citas y localizadores conservados',Counter(re.findall(r'\[[^\]\n]*@[\s\S]*?\]',source))==Counter(re.findall(r'\[[^\]\n]*@[\s\S]*?\]',core)))
ck('Bibliografía conservada',bib==prior('libro/bibliografia.bib'))
pilot=(R/'libro/capitulos/02-piloto-especializacion.Rmd').read_text(encoding='utf8')
old_pilot=prior('libro/capitulos/02-piloto-especializacion.Rmd')
for label,pattern in [('ecuaciones',r'\\\[[\s\S]*?\\\]'),('expresiones R',r'`r [^`]+`'),('citas',r'\[[^\]\n]*@[\s\S]*?\]')]:
 ck('Piloto conserva '+label,Counter(re.findall(pattern,pilot))==Counter(re.findall(pattern,old_pilot)))
ck('Sin notas editoriales pendientes',not re.search('B02-GEOGRAFIA|TODO|TBD',source))
water=list(csv.DictReader((R/'datos/preparados/capitulo-01/F03_F05_agua_poblacion_2022.csv').open(encoding='utf-8-sig')))
ck('Denominadores de agua y población',sum(int(r['agua_renovable_hm3_anio']) for r in water)==461640 and abs(sum(float(r['poblacion_millones']) for r in water)-129.35)<1e-10)
for r in water:
 if r['rha']=='XI':ck('Participaciones XI',round(float(r['porcentaje_agua']),1)==34.2 and round(float(r['porcentaje_poblacion']),1)==6.4)
 if r['rha']=='III':ck('Participaciones III',round(float(r['porcentaje_agua']),1)==5.8 and round(float(r['porcentaje_poblacion']),1)==3.7)
figures=['F01-relieve-localizacion','F02-clima-suelos','F03-agua-renovable','F04-recursos','F05-agua-poblacion','F06-mecanismos-territoriales']
for name in figures:
 p=R/'assets/capitulo-01/interactivos'/(name+'.html')
 ck('HTML integrado idéntico '+name,p.exists() and sha(p)==sha(W/'recursos'/p.name))
 ck('HTML individual autónomo '+name,all(urlsplit(v).scheme or v.startswith(('#','data:','blob:')) for t,k,v in HTML(p.read_text(encoding='utf8')).links if k=='src'))
historical=['entregas/pdf','assets/capitulo-01/figuras-estaticas','assets/capitulo-02/figuras-estaticas','referencias','datos/originales']
changed=subprocess.check_output(['git','diff','--name-only',BASE,'--',*historical],cwd=R).decode().splitlines()
ck('Fuentes y entregas históricas intactas',not changed,changed)
changed_data=subprocess.check_output(['git','diff','--name-only',BASE,'--','datos/preparados'],cwd=R).decode().splitlines()
allowed={'datos/preparados/capitulo-01/manifiesto-B02.csv','datos/preparados/capitulo-01/estados-web.json'}
ck('Bases preparadas cuantitativas intactas',set(changed_data)<=allowed,changed_data)
ck('Manuscrito rector intacto',sha(R/'referencias/manuscrito-base/PAPIME Libro.pdf')=='7bd8d8a23ff225a42728c167723c323a2bedebda7c999a9aa186df7a8e486b35')
clean=json.loads((R/'seguimiento/limpieza-entrega-web-B02.json').read_text(encoding='utf8'))
ck('Copias retiradas conservadas con hash',all((R/a['conservado_en']).exists() and sha(R/a['conservado_en'])==a['sha256'] for a in clean['acciones']),len(clean['acciones']))
report=dict(fecha='2026-11-06',edicion='web D25–D28',base_preservada=BASE,resultado='correcto' if all(c['correcto'] for c in checks) else 'incidencias',pruebas=len(checks),comprobaciones=checks)
(R/'seguimiento/verificacion-proyecto-B02-web.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(dict(resultado=report['resultado'],pruebas=len(checks),fallos=[c for c in checks if not c['correcto']]),ensure_ascii=False))
raise SystemExit(0 if report['resultado']=='correcto' else 1)
