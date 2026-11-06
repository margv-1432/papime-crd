"""Contraste independiente de ITER, dominios DBF y derivados de F01/F02."""
from pathlib import Path
import csv, io, json, zipfile, struct, collections, hashlib, math
ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/'datos/preparados/capitulo-01'
checks=[]
def check(name, condition, detail):
    checks.append(dict(prueba=name,correcta=bool(condition),detalle=detail))
def original(name):
    for d in (ROOT/'.local/B02-originales', ROOT/'datos/originales/geografia'):
        p=d/name
        if p.exists(): return p
    raise FileNotFoundError(name)
def dbf(path):
    with path.open('rb') as f:
        h=f.read(32);n,hlen,rlen=struct.unpack_from('<IHH',h,4)
        fields=[]
        while f.tell()<hlen-1:
            z=f.read(32)
            if z[0]==13:break
            fields.append((z[:11].split(b'\0')[0].decode('ascii'),z[16]))
        f.seek(hlen)
        for i in range(n):
            z=f.read(rlen)
            if z[:1]==b'*':continue
            pos=1;r={}
            for name,width in fields:
                r[name]=z[pos:pos+width].decode('latin1').strip();pos+=width
            yield r
with zipfile.ZipFile(original('iter_00_cpv2020_csv.zip')) as z:
    fn=next(n for n in z.namelist() if '/conjunto_de_datos/' in n and n.endswith('.csv'))
    rs=csv.DictReader(io.TextIOWrapper(z.open(fn),encoding='utf-8-sig'))
    selected={};national=None
    for r in rs:
        if r['ENTIDAD']=='00' and r['MUN']=='000' and r['LOC']=='0000':national=int(r['POBTOT'])
        if r['ENTIDAD']!='00' and r['MUN']!='000' and r['LOC'] not in {'0000','9998','9999'} and r['POBTOT'].isdigit() and int(r['POBTOT'])>=100000:
            selected[r['ENTIDAD']+r['MUN']+r['LOC']]=int(r['POBTOT'])
with (OUT/'F01-localidades-2020.csv').open(encoding='utf-8-sig') as f:
    cached=list(csv.DictReader(f))
check('ITER selección de localidades',len(selected)==145 and len(cached)==145,len(selected))
check('ITER valores conservados',selected=={r['cveloc']:int(r['poblacion']) for r in cached},'145 códigos y poblaciones contrastados con el CSV nacional')
check('ITER total censal',national==126014024,national)
pop=sum(selected.values());pct=pop/national*100
check('ITER población cubierta',pop==61026805,pop)
check('ITER porcentaje',math.isclose(pct,48.42858204416994,abs_tol=1e-10),pct)
meta=json.loads((OUT/'F01-localidades-metadatos.json').read_text(encoding='utf-8'))
check('Metadatos de selección',meta['poblacion_seleccion']==pop and math.isclose(meta['porcentaje_poblacion'],pct,abs_tol=1e-10),'Totales y porcentaje coinciden')
cl=list(dbf(ROOT/'tmp/F02-clima/unidadesClimaticas.dbf'))
check('Clima polígonos originales',len(cl)==1695,len(cl))
allowed={11,12,21,22,31,32,42,70,91,92}|set(range(51,65))
check('Clima dominio exhaustivo',all(int(r['TIPO_N']) in allowed for r in cl),sorted({int(r['TIPO_N']) for r in cl}))
with (OUT/'F02-correspondencia-climas.csv').open(encoding='utf-8-sig') as f:clcache=list(csv.DictReader(f))
check('Clima correspondencia exhaustiva',{(r['CLAVE'],int(r['TIPO_N'])) for r in cl}=={(r['CLAVE'],int(r['TIPO_N'])) for r in clcache},len(clcache))
check('Clima extranjeros excluidos',sum(int(r['TIPO_N'])==91 for r in cl)==2,2)
so=list(dbf(ROOT/'tmp/F02-suelo/794551131916/conjunto_de_datos/cdv_edaf_esc_250k_serie II_cont_nac.dbf'))
check('Suelo polígonos originales',len(so)==75491,len(so))
counts=dict(collections.Counter(r['FRUDICA'] for r in so))
check('Suelo códigos nominales sensibles a mayúsculas',counts=={'N/A':10673,'N':37234,'R':16433,'r':11151},counts)
bad=[r for r in so if r['FRUDICA']=='R' and r['F_SUPERF']=='GRAVOSA']
check('Suelo discordancia conservada',len(bad)==1,len(bad))
with (OUT/'F02-correspondencia-suelos.csv').open(encoding='utf-8-sig') as f:socache=list(csv.DictReader(f))
check('Suelo correspondencia exhaustiva',{(r['CLAVE_WRB'],r['FRUDICA'],r['F_SUPERF']) for r in so}=={(r['CLAVE_WRB'],r['FRUDICA'],r['F_SUPERF']) for r in socache},len(socache))
check('Suelo no confunde N con ausencia de limitaciones',all(r['grupo']=='Sin fase registrada (N)' for r in socache if r['FRUDICA']=='N'),'Etiqueta conservada')
report={'fecha':'2026-11-05','alcance':'Contraste independiente Python; ITER y DBF oficiales, sin estimación de superficies o accesibilidad','pruebas':checks,'correctas':sum(c['correcta'] for c in checks),'total':len(checks)}
(ROOT/'seguimiento/auditoria-F01-F02.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
if not all(c['correcta'] for c in checks):raise SystemExit(1)
