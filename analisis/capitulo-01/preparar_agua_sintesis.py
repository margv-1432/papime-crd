"""B02 F03, F05 y F06. Python 3, pypdf y reportlab; sin descargas al compilar.

Se ejecuta desde la raíz del repositorio. La cartografía original se conserva
comprimida sin cambios; la generalización a 1 km sólo sirve para dibujar.
"""
from pathlib import Path
import csv, gzip, hashlib, html, json, math, re, shutil, subprocess
from decimal import Decimal
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[2]
ORIG=ROOT/'datos/originales/capitulo-01/agua'
PREP=ROOT/'datos/preparados/capitulo-01'
STATIC=ROOT/'assets/capitulo-01/figuras-estaticas'
INTER=ROOT/'assets/capitulo-01/interactivos'
TABLE=ROOT/'assets/capitulo-01/tablas'
for p in [PREP,STATIC,INTER,TABLE]: p.mkdir(parents=True,exist_ok=True)
BLUE='#0F4761'; ORANGE='#A34F26'; INK='#24313A'; GRAY='#56616B'

def readcsv(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def writecsv(p,rows):
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,data):p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
data=readcsv(ORIG/'EAM2023_tabla-1-5-2_transcripcion.csv')
assert len(data)==13 and len({r['rha'] for r in data})==13
for r in data:
    r['orden']=int(r['orden']);r['agua_renovable_hm3_anio']=int(r['agua_renovable_hm3_anio'])
    r['poblacion_millones']=float(r['poblacion_millones'])
assert sum(r['agua_renovable_hm3_anio'] for r in data)==461640
assert sum(Decimal(str(r['poblacion_millones'])) for r in data)==Decimal('129.35')
# Contraste independiente con la extracción de los cuadros del original, sin
# aceptar que una suma nacional correcta por sí sola valide la transcripción.
extract=PdfReader(ORIG/'EAM2023_extracto-editorial-cuadros.pdf')
text=extract.pages[2].extract_text().split('Tabla 1.5.2')[-1]
# La extracción PDF posiciona el título después del cuadro; el segundo bloque
# de filas comienza con la segunda aparición de I 154 279.
alltext=extract.pages[2].extract_text()
matched=re.findall(r'^([IVX]+)\s+([\d ]+)\s+(\d+\.\d{2})\s+',alltext,re.M)
# Verificar sobre filas completas (superficie + agua se separan por la lista
# de valores publicados y por la población, que tiene decimal).
for r in data:
    pattern=rf"^{r['rha']}\s+[\d ]+\s+{r['poblacion_millones']:.2f}\s+"
    matches=[line for line in alltext.splitlines() if re.match(pattern,line)]
    assert len(matches)==1,(r['rha'],matches)
    before=matches[0].split(f"{r['poblacion_millones']:.2f}")[0]
    compact=''.join(re.findall(r'\d',before))
    assert compact.endswith(str(r['agua_renovable_hm3_anio'])),matches[0]
for r in data:
    r['porcentaje_agua']=100*r['agua_renovable_hm3_anio']/461640
    r['porcentaje_poblacion']=100*r['poblacion_millones']/129.35
    r['diferencia_puntos_porcentuales']=r['porcentaje_agua']-r['porcentaje_poblacion']
assert abs(sum(r['porcentaje_agua'] for r in data)-100)<1e-10
assert abs(sum(r['porcentaje_poblacion'] for r in data)-100)<1e-10
writecsv(PREP/'F03_F05_agua_poblacion_2022.csv',data)
shutil.copyfile(PREP/'F03_F05_agua_poblacion_2022.csv',TABLE/'F03_F05_agua_poblacion_2022.csv')

geomfile=ORIG/'RHA2023_consulta.json.gz'
if not geomfile.exists():
    with gzip.open(geomfile,'wb') as f:f.write((ORIG/'RHA2023_consulta.json').read_bytes())
source=json.loads(gzip.decompress(geomfile.read_bytes()))
assert len(source['features'])==13 and not source.get('exceededTransferLimit',False)
assert 'Lambert_Conformal_Conic' in source['spatialReference']['wkt']
lookup={r['rha']:r for r in data}

def dseg(p,a,b):
    dx=b[0]-a[0];dy=b[1]-a[1]
    t=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/(dx*dx+dy*dy))) if dx or dy else 0
    return math.hypot(p[0]-a[0]-t*dx,p[1]-a[1]-t*dy)
def simplify(points,tol=1000):
    if len(points)<3:return points
    far=max(range(1,len(points)-1),key=lambda i:dseg(points[i],points[0],points[-1]),default=0)
    if far and dseg(points[far],points[0],points[-1])>tol:
        return simplify(points[:far+1],tol)[:-1]+simplify(points[far:],tol)
    return [points[0],points[-1]]
def ringarea(r):return sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(r,r[1:]))/2
def inside(pt,ring):
    x,y=pt;flag=False
    for a,b in zip(ring,ring[1:]):
        if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:flag=not flag
    return flag
def anchor(ring):
    xmin=min(p[0] for p in ring);xmax=max(p[0] for p in ring)
    ymin=min(p[1] for p in ring);ymax=max(p[1] for p in ring)
    candidates=[(xmin+(x+.5)*(xmax-xmin)/24,ymin+(y+.5)*(ymax-ymin)/24) for x in range(24) for y in range(24)]
    candidates=[p for p in candidates if inside(p,ring)]
    return max(candidates,key=lambda p:min(dseg(p,a,b) for a,b in zip(ring,ring[1:])))
geo=[];before=after=0
for f in source['features']:
    code=f['attributes']['Identifica'];assert code in lookup
    assert f['attributes']['Ano']==2023
    rings=[]
    for ring in f['geometry']['rings']:
        before+=len(ring)
        # Closed ring split at the furthest vertex, preserving the closure.
        split=max(range(len(ring)),key=lambda i:(ring[i][0]-ring[0][0])**2+(ring[i][1]-ring[0][1])**2)
        simp=simplify(ring[:split+1])[:-1]+simplify(ring[split:])
        if len(simp)>=4:rings.append(simp);after+=len(simp)
    main=max(rings,key=lambda r:abs(ringarea(r)))
    center=anchor(main)
    assert inside(center,main)
    geo.append({'rha':code,'nombre_capa':f['attributes']['Nombre_de_'],'rings':rings,'anchor':center})
geo.sort(key=lambda g:lookup[g['rha']]['orden'])
dump(PREP/'F03_RHA2023_dibujo.json',{'crs':source['spatialReference'],'tolerancia_m':1000,'uso':'Sólo dibujo; no cálculo de áreas ni asignaciones territoriales','regiones':geo})
writecsv(PREP/'F03_anclas.csv',[{'rha':g['rha'],'x_lcc':g['anchor'][0],'y_lcc':g['anchor'][1],'ancla_interior':True} for g in geo])

FONTDIR=Path('C:/Windows/Fonts')
if (FONTDIR/'arial.ttf').exists():
    pdfmetrics.registerFont(TTFont('Body',str(FONTDIR/'arial.ttf')))
    pdfmetrics.registerFont(TTFont('Bold',str(FONTDIR/'arialbd.ttf')))
else:
    # Helvetica is a PDF standard family; accents remain Latin-1 compatible.
    pdfmetrics.registerFont(pdfmetrics.Font('Body','Helvetica','WinAnsiEncoding'))
    pdfmetrics.registerFont(pdfmetrics.Font('Bold','Helvetica-Bold','WinAnsiEncoding'))

class Drawing:
    def __init__(self,name,w,h):
        self.name=name;self.w=w;self.h=h;self.svg=[]
        self.c=canvas.Canvas(str(STATIC/(name+'.pdf')),pagesize=(w,h),pageCompression=1)
        self.c.setTitle(name+' · Capítulo I · PAPIME');self.c.setAuthor('Proyecto PAPIME')
    def text(self,x,y,text,size=20,color=INK,bold=False,anchor='start'):
        self.svg.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{700 if bold else 400}" text-anchor="{anchor}">{html.escape(text)}</text>')
        self.c.setFont('Bold' if bold else 'Body',size);self.c.setFillColor(HexColor(color))
        f={'start':self.c.drawString,'middle':self.c.drawCentredString,'end':self.c.drawRightString}[anchor];f(x,self.h-y,text)
    def line(self,x1,y1,x2,y2,color='#C9D4DA',width=1,dashed=False):
        self.svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"'+(' stroke-dasharray="8 5"' if dashed else '')+'/>')
        self.c.setStrokeColor(HexColor(color));self.c.setLineWidth(width);self.c.setDash([8,5] if dashed else []);self.c.line(x1,self.h-y1,x2,self.h-y2);self.c.setDash([])
    def rect(self,x,y,w,h,fill='#F2F6F8',stroke='#C9D4DA',radius=0):
        self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>')
        self.c.setFillColor(HexColor(fill));self.c.setStrokeColor(HexColor(stroke));self.c.roundRect(x,self.h-y-h,w,h,radius,fill=1,stroke=1)
    def circle(self,x,y,r,fill=BLUE,stroke='#FFFFFF'):
        self.svg.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>')
        self.c.setFillColor(HexColor(fill));self.c.setStrokeColor(HexColor(stroke));self.c.setLineWidth(1.4);self.c.circle(x,self.h-y,r,fill=1,stroke=1)
    def poly(self,points,fill,stroke='#FFFFFF',width=.8):
        d='M'+'L'.join(f'{x:.1f},{y:.1f}' for x,y in points)+'Z'
        self.svg.append(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')
        p=self.c.beginPath();p.moveTo(points[0][0],self.h-points[0][1])
        for x,y in points[1:]:p.lineTo(x,self.h-y)
        p.close();self.c.setFillColor(HexColor(fill));self.c.setStrokeColor(HexColor(stroke));self.c.setLineWidth(width);self.c.drawPath(p,fill=1,stroke=1)
    def arrow(self,x1,y1,x2,y2,color=BLUE,dashed=False):
        self.line(x1,y1,x2,y2,color,2.3,dashed)
        a=math.atan2(y2-y1,x2-x1)
        pts=[(x2,y2),(x2-12*math.cos(a)+5*math.sin(a),y2-12*math.sin(a)-5*math.cos(a)),(x2-12*math.cos(a)-5*math.sin(a),y2-12*math.sin(a)+5*math.cos(a))]
        self.poly(pts,color,color)
    def save(self):
        self.c.showPage();self.c.save()
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{self.name}"><rect width="100%" height="100%" fill="white"/><g font-family="Arial,Calibri,sans-serif">'+''.join(self.svg)+'</g></svg>'
        (STATIC/(self.name+'.svg')).write_text(svg,encoding='utf8');return svg

def fmt(v,n=0):return f'{v:,.{n}f}'.replace(',',' ')
# F03: symbols scaled by area, on the preserved projected geometry.
d=Drawing('F03-agua-renovable',1500,980)
d.text(35,45,'Distribución regional del agua renovable',32,BLUE,True)
d.text(35,80,'13 regiones hidrológico-administrativas · corte estadístico 2022',22,GRAY)
d.text(35,108,'Fuente: CONAGUA, EAM2023 (marzo de 2024), cuadro 1.5.2, p. 16; cartografía SEMARNAT, RHA2023.',17,GRAY)
coords=[p for g in geo for ring in g['rings'] for p in ring]
xmin=min(p[0] for p in coords);xmax=max(p[0] for p in coords);ymin=min(p[1] for p in coords);ymax=max(p[1] for p in coords)
scale=min(950/(xmax-xmin),690/(ymax-ymin))
def xy(p):return (35+(p[0]-xmin)*scale,115+(ymax-p[1])*scale)
for g in geo:
    for ring in g['rings']:d.poly([xy(p) for p in ring],'#E4EBEF',BLUE,.7)
for g in geo:
    r=lookup[g['rha']];x,y=xy(g['anchor']);rad=42*math.sqrt(r['agua_renovable_hm3_anio']/158021)
    start=len(d.svg)
    d.circle(x,y,rad,BLUE)
    # Small bubbles retain their proportional area; labels move outside rather
    # than enlarging the symbol and changing its quantitative meaning.
    if rad<17:d.text(x,y-rad-9,g['rha'],22,BLUE,True,'middle')
    else:d.text(x,y+6,g['rha'],20,'#FFFFFF',True,'middle')
    d.svg[start:]=[f'<g data-rha="{g["rha"]}" role="button" tabindex="0" aria-label="{html.escape(r["nombre"])}">'+''.join(d.svg[start:])+'</g>']
d.text(1010,130,'RHA',20,BLUE,True);d.text(1455,130,'hm³/año',20,BLUE,True,'end')
short={'I':'Península de Baja California','VII':'Cuencas Centrales del Norte','VIII':'Lerma-Santiago-Pacífico','XII':'Península de Yucatán','XIII':'Aguas del Valle de México'}
for i,r in enumerate(data):
    yy=170+i*41;d.text(1010,yy,r['rha'],18,BLUE,True);d.text(1080,yy,short.get(r['rha'],r['nombre']),17);d.text(1455,yy,fmt(r['agua_renovable_hm3_anio']),18,INK,False,'end')
    d.line(1005,yy+10,1465,yy+10,'#E0E6E9')
d.text(1010,740,'Total nacional',20,BLUE,True);d.text(1455,740,'461 640',20,BLUE,True,'end')
for i,v in enumerate([5000,50000,150000]):
    x=160+i*240;rad=42*math.sqrt(v/158021);d.circle(x,835,rad,BLUE);d.text(x,900,fmt(v),18,GRAY,False,'middle')
d.text(35,945,'El área del símbolo es proporcional al volumen. Límites RHA 2023 de referencia; generalización gráfica a 1 km.',20,GRAY)
svg3=d.save()
# F05 paired dots, common national denominators even after interaction.
d=Drawing('F05-agua-poblacion',1500,1200)
d.text(35,45,'Agua renovable y población por región',32,BLUE,True)
d.text(35,80,'Participación nacional (%) · agua renovable y población de referencia de 2022',22,GRAY)
d.circle(440,120,8,BLUE);d.text(458,127,'Agua renovable',21)
d.circle(760,120,8,ORANGE);d.text(778,127,'Población',21)
d.text(35,102,'Fuente: CONAGUA, EAM2023 (marzo de 2024), cuadro 1.5.2, p. 16. Cálculos propios sobre los valores publicados.',17,GRAY)
x0=470;span=910
for v in [0,5,10,15,20,25,30,35]:
    x=x0+span*v/36;d.line(x,155,x,1060,'#D6E0E5');d.text(x,1097,str(v),22,GRAY,False,'middle')
for i,r in enumerate(data):
    yy=185+i*70
    start=len(d.svg)
    d.text(440,yy+7,r['rha']+'. '+r['nombre'],23,INK,False,'end')
    a=x0+span*r['porcentaje_agua']/36;b=x0+span*r['porcentaje_poblacion']/36
    d.line(a,yy,b,yy,'#B5C6D0',3);d.circle(a,yy-6,7,BLUE);d.circle(b,yy+6,7,ORANGE)
    d.text(a,yy-18,fmt(r['porcentaje_agua'],1),21,BLUE,False,'middle');d.text(b,yy+29,fmt(r['porcentaje_poblacion'],1),21,ORANGE,False,'middle')
    d.svg[start:]=[f'<g data-rha="{r["rha"]}" role="button" tabindex="0" aria-label="{html.escape(r["nombre"])}">'+''.join(d.svg[start:])+'</g>']
d.text(920,1135,'Porcentaje del total nacional',23,GRAY,False,'middle')
d.text(35,1180,'Denominadores: 461 640 hm³/año y 129.35 millones de habitantes. La distancia entre puntos se lee en puntos porcentuales.',20,GRAY)
svg5=d.save()

nodes=[
 dict(id='base',etiqueta='Condiciones geográficas',detalle='Atravesar una sierra exige obras distintas de las de una llanura; al elegir un emplazamiento se consideran esas diferencias del terreno y los recursos disponibles.',tipo='proceso'),
 dict(id='acceso',etiqueta='Acceso efectivo',detalle='Una carretera cercana sirve para llegar a un servicio cuando hay transporte y el viaje puede pagarse. En el agua, también importan la captación y la calidad necesaria para cada uso.',tipo='proceso'),
 dict(id='uso',etiqueta='Aprovechamiento',detalle='Tras extraer un material puede transformarse cerca o enviarse a otra región. Seguir ese recorrido ayuda a reconocer las actividades que se articulan con su aprovechamiento.',tipo='proceso'),
 dict(id='resultados',etiqueta='Resultados territoriales',detalle='Para conocer qué queda en la región conviene seguir las compras y los ingresos de trabajadores y propietarios, junto con los costos que recaen sobre otros grupos.',tipo='proceso'),
 dict(id='infra',etiqueta='Infraestructura',detalle='Conducir agua a una parcela supone construir y mantener obras a lo largo del recorrido; en el transporte, el estado de las vías interviene en la continuidad de los viajes.',tipo='mediacion'),
 dict(id='tec',etiqueta='Tecnología y manejo',detalle='Un terreno puede responder de manera distinta al cambiar el cultivo o el manejo. Su aptitud se evalúa para esa práctica concreta y con información del lugar.',tipo='mediacion'),
 dict(id='org',etiqueta='Organización productiva',detalle='En las empresas forestales comunitarias, los acuerdos de gestión y reinversión pueden ampliar la transformación local de la madera y sostener capacidades compartidas.',tipo='mediacion'),
 dict(id='inst',etiqueta='Derechos y decisiones',detalle='Quién puede usar el recurso y participar en las decisiones forma parte del estudio de sus resultados. Los acuerdos de propiedad y gestión sitúan esas facultades en grupos y lugares concretos.',tipo='mediacion'),
 dict(id='conservacion',etiqueta='Conservación o degradación',detalle='El riego puede acompañarse de salinización, mientras que conservar manglares contribuye a sostener hábitats pesqueros. Esos cambios enlazan el uso presente con sus posibilidades futuras.',tipo='retorno')]
sources={
 'fao':'https://www.fao.org/4/T0715E/t0715e06.htm',
 'geurs':'https://doi.org/10.1016/j.jtrangeo.2003.10.005',
 'gasca':'https://doi.org/10.22198/rys.2014.60.a11',
 'bray':'https://www.ccmss.org.mx/wp-content/uploads/Mexicos-community-managed-forest-as-a-global-model-for-sustainable-landscapes.pdf',
 'aburto':'https://doi.org/10.1073/pnas.0804601105'}
links=[
 ('base','acceso','posibilidades y restricciones','fao'),('acceso','uso','medios utilizables','geurs'),
 ('uso','resultados','articulación y distribución','gasca'),('infra','acceso','captación y conexiones','geurs'),
 ('tec','acceso','usos definidos','fao'),('org','uso','gestión y transformación','gasca'),
 ('inst','resultados','participación y reparto','bray'),('uso','conservacion','manejo de recursos','fao'),
 ('resultados','conservacion','cargas y reinversión','aburto'),('conservacion','base','condiciones futuras','fao')]
rels=[dict(origen=a,destino=b,etiqueta=l,url=sources[s],tipo='retorno' if b in ['base','conservacion'] else 'interpretativa') for a,b,l,s in links]
writecsv(PREP/'F06_nodos.csv',nodes);writecsv(PREP/'F06_relaciones.csv',rels)
for n in ['F06_nodos.csv','F06_relaciones.csv']:shutil.copyfile(PREP/n,TABLE/n)
d=Drawing('F06-mecanismos-territoriales',1500,830)
d.text(35,45,'Mecanismos territoriales',32,BLUE,True)
d.text(35,80,'Síntesis interpretativa de las relaciones desarrolladas en el capítulo',22,GRAY)
d.text(35,115,'Elaboración propia con apoyo en FAO (1993), Geurs y van Wee (2004), Gasca (2014), Bray et al. (2003) y Aburto-Oropeza et al. (2008).',17,GRAY)
xs=[35,405,775,1145];w=310;cy=380
for i in range(3):d.arrow(xs[i]+w,cy+65,xs[i+1]-10,cy+65)
mainlines=[['Condiciones','geográficas'],['Acceso','efectivo'],['Aprovechamiento'],['Resultados','territoriales']]
subs=[['Relieve y localización','Clima, agua, suelos y recursos'],['Medios de conexión','Calidad y costos de utilización'],['Actividades y transformación','Vínculos entre territorios'],['Empleo e ingresos','Beneficios y cargas']]
for i,lines in enumerate(mainlines):
    d.rect(xs[i],cy,w,155,'#EAF2F6',BLUE,8)
    for j,t in enumerate(lines):d.text(xs[i]+w/2,cy+38+j*28,t,25,BLUE,True,'middle')
    for j,t in enumerate(subs[i]):d.text(xs[i]+w/2,cy+113+j*25,t,18,INK,False,'middle')
topnodes=[('Infraestructura',35,190,'Captación, conducción y transporte'),('Tecnología y manejo',405,190,'Requerimientos de un uso definido'),('Organización productiva',775,190,'Gestión, transformación y reinversión'),('Derechos y decisiones',1145,190,'Reglas, participación y distribución')]
for label,x,y,sub in topnodes:
    d.rect(x,y,w,74,'#F6F8F9','#A5BAC6',6);d.text(x+w/2,y+29,label,22,BLUE,True,'middle');d.text(x+w/2,y+56,sub,16,INK,False,'middle')
d.line(190,264,190,320,BLUE,2.3);d.line(190,320,480,320,BLUE,2.3);d.arrow(480,320,480,380)
d.arrow(560,264,560,380);d.arrow(930,264,930,380);d.arrow(1300,264,1300,380)
# Retorno visible con trayectorias separadas del flujo principal.
d.line(930,535,930,625,ORANGE,2.3,True);d.arrow(1300,535,1300,625,ORANGE,True)
d.line(930,625,1115,625,ORANGE,2.3,True);d.line(1300,625,1115,625,ORANGE,2.3,True)
d.rect(775,650,680,80,'#FBF3ED',ORANGE,8)
d.text(1115,685,'Conservación o degradación de la base natural',24,ORANGE,True,'middle')
d.text(1115,715,'El manejo y las cargas afectan condiciones de aprovechamiento futuro',17,INK,False,'middle')
d.arrow(1115,625,1115,650,ORANGE,True)
d.line(775,690,190,690,ORANGE,2.3,True);d.arrow(190,690,190,535,ORANGE,True)
d.text(420,730,'Retorno hacia condiciones futuras',19,ORANGE,False,'middle')
d.text(35,805,'Cada flecha propone una relación cuyo alcance y magnitud deben estudiarse en el territorio.',21,GRAY)
svg6=d.save()

STYLE='''*{box-sizing:border-box}body{margin:0;color:#24313A;font:16px/1.5 Arial,Calibri,sans-serif;background:white}main{max-width:1500px;margin:auto;padding:20px}h1{color:#0F4761;font-size:1.55rem;margin:0 0 8px}p{margin:0 0 15px}.fuente{font-size:.88rem;color:#56616B}.controles{display:flex;gap:16px;flex-wrap:wrap;align-items:end;margin:18px 0}label{display:block;font-weight:bold}select,button{font:inherit;min-height:44px;padding:8px;border:1px solid #879CA8;background:white;border-radius:4px;color:#0F4761}button{cursor:pointer}:focus-visible{outline:3px solid #007CAF;outline-offset:3px}.lectura{background:#F2F6F8;padding:12px;border-left:4px solid #0F4761;min-height:80px}.grafico{overflow:auto}svg{display:block;width:100%;height:auto;min-width:760px}svg text{font-family:Arial,Calibri,sans-serif}details{margin-top:20px}summary{color:#0F4761;cursor:pointer;padding:8px;min-height:44px;font-weight:bold}.tabla{overflow:auto}table{border-collapse:collapse;font-size:.9rem;width:100%}th,td{padding:7px 10px;border-bottom:1px solid #D6E0E5;text-align:left}th{background:#F2F6F8}td.num{text-align:right;font-variant-numeric:tabular-nums}a{color:#0F4761}svg g[data-rha]{cursor:pointer}svg g[data-rha]:focus{outline:3px solid #007CAF}svg g.seleccionada circle{stroke:#A34F26;stroke-width:4}@media(max-width:500px){main{padding:12px}select{max-width:100%}.controles>div{width:100%}svg{min-width:760px}}'''
def page(title,body,script=''):
    return f'<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title><style>{STYLE}</style></head><body><main><h1>{title}</h1>{body}</main>{script}</body></html>'
sourcehtml='<p class="fuente">Fuente: CONAGUA, <em>Estadísticas del Agua en México 2023</em>, publicada en marzo de 2024, tabla 1.5.2, p. 16 y tabla 2.2.2, p. 27. Las cifras de agua renovable describen recursos medios con corte 2022; la población es la proyección de mitad de ese año utilizada en la edición.</p>'
options='<option value="">Todas las regiones</option>'+''.join(f'<option value="{r["rha"]}">{r["rha"]}. {r["nombre"]}</option>' for r in data)
csvtext=(PREP/'F03_F05_agua_poblacion_2022.csv').read_text(encoding='utf8')
table='<details id="tabla-datos"><summary>Consultar las 13 regiones y sus valores</summary><div class="tabla"><table><thead><tr>'+''.join('<th scope="col">'+t+'</th>' for t in ['RHA','Región','Agua (hm³/año)','Población (millones)','Agua (%)','Población (%)'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td'+(' class="num"' if i>1 else '')+'>'+html.escape(str(v))+'</td>' for i,v in enumerate([r['rha'],r['nombre'],fmt(r['agua_renovable_hm3_anio']),fmt(r['poblacion_millones'],2),fmt(r['porcentaje_agua'],4),fmt(r['porcentaje_poblacion'],4)]))+'</tr>' for r in data)+'</tbody></table></div></details>'
payload=json.dumps({'filas':data,'csv':csvtext},ensure_ascii=False).replace('<','\\u003c')
for id_,title,svg in [('F03','Distribución regional del agua renovable',svg3),('F05','Agua renovable y población por región',svg5)]:
    # SVG includes all data in its initial view; selection adds exact textual data,
    # retaining all regions, a fixed denominator and an inspectable complete table.
    body='<p>Corte estadístico 2022 · 13 regiones hidrológico-administrativas</p><div class="controles"><div><label for="region">Región para examinar</label><select id="region">'+options+'</select></div><button id="descargar">Descargar datos CSV</button></div><section class="lectura" aria-live="polite" id="lectura">Seleccione una región para consultar sus valores exactos. Las 13 regiones permanecen visibles.</section><p class="fuente">En pantallas pequeñas, desplace la figura horizontalmente para conservar la legibilidad.</p><div class="grafico">'+svg+'</div>'+sourcehtml
    if id_=='F03':body+='<p class="fuente">La capa de RHA 2023 de SEMARNAT sirve como referencia espacial, en proyección Lambert Cónica Conforme y con generalización de dibujo a 1 km. La correspondencia con el cuadro de 2022 se establece por identificador regional. El área de cada símbolo es proporcional al volumen. La región XIII se llama «Valle de México» en la capa y «Aguas del Valle de México» en el cuadro.</p>'
    else:body+='<p class="fuente">Las participaciones se calculan sobre 461 640 hm³/año y 129.35 millones de habitantes. La selección de una región conserva esos denominadores nacionales, de modo que todas pueden compararse con la misma referencia. Las diferencias entre las dos participaciones se expresan en puntos porcentuales.</p>'
    body+=table+'<p class="fuente">Las participaciones se presentan con cuatro decimales en la tabla; el CSV conserva la precisión del cálculo.</p>'
    script='<script id="datos-agua" type="application/json">'+payload+'</script>'+'''<script>(()=>{const p=JSON.parse(document.getElementById('datos-agua').textContent),f=new Intl.NumberFormat('es-MX',{maximumFractionDigits:4});document.getElementById('region').addEventListener('change',e=>{const d=p.filas.find(r=>r.rha===e.target.value);document.getElementById('lectura').textContent=d?d.rha+'. '+d.nombre+': '+f.format(d.agua_renovable_hm3_anio)+' hm³/año; '+f.format(d.poblacion_millones)+' millones de habitantes. Participaciones nacionales: agua '+f.format(d.porcentaje_agua)+'%; población '+f.format(d.porcentaje_poblacion)+'%.':'Las 13 regiones permanecen visibles. Seleccione una región para consultar sus valores.';document.querySelectorAll('[data-rha]').forEach(g=>{g.classList.toggle('seleccionada',Boolean(d&&g.dataset.rha===d.rha));g.setAttribute('aria-pressed',String(Boolean(d&&g.dataset.rha===d.rha)))});document.querySelectorAll('tbody tr').forEach(tr=>{tr.style.background=d&&tr.firstElementChild.textContent===d.rha?'#E8F0F4':''})});document.querySelectorAll('[data-rha]').forEach(g=>{const choose=()=>{document.getElementById('region').value=g.dataset.rha;document.getElementById('region').dispatchEvent(new Event('change'))};g.addEventListener('click',choose);g.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();choose()}})});document.getElementById('descargar').addEventListener('click',()=>{const u=URL.createObjectURL(new Blob(['\\uFEFF',p.csv],{type:'text/csv;charset=utf-8'})),a=document.createElement('a');a.href=u;a.download='F03_F05_agua_poblacion_2022.csv';document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),30000)})})();</script>'''
    (INTER/(id_+('-agua-renovable' if id_=='F03' else '-agua-poblacion')+'.html')).write_text(page(title,body,script),encoding='utf8')

payload6=json.dumps({'nodos':nodes,'relaciones':rels},ensure_ascii=False).replace('<','\\u003c')
body='<p>El esquema sigue el paso de las condiciones geográficas al aprovechamiento y a sus resultados. Las mediaciones ayudan a explicar por qué ese recorrido cambia entre territorios; el retorno ambiental vincula el uso presente con sus posibilidades futuras.</p><div class="controles"><div><label for="mecanismo">Relación para examinar</label><select id="mecanismo">'+''.join(f'<option value="{i}">{next(n["etiqueta"] for n in nodes if n["id"]==r["origen"])} → {next(n["etiqueta"] for n in nodes if n["id"]==r["destino"])}</option>' for i,r in enumerate(rels))+'</select></div><button id="descargar">Descargar relaciones CSV</button></div><section id="lectura" class="lectura" aria-live="polite"></section><p class="fuente">En pantallas pequeñas, desplace el esquema horizontalmente. El selector permite leer cada relación en texto.</p><div class="grafico">'+svg6+'</div><p class="fuente">Fuente: síntesis propia de la discusión del capítulo, apoyada en Geurs y van Wee (2004), FAO (1993), Gasca Zamora (2014), Bray et al. (2003) y Aburto-Oropeza et al. (2008). Cada relación enlaza a su referencia de apoyo.</p><details><summary>Consultar nodos y relaciones</summary>'+''.join('<p><strong>'+html.escape(n['etiqueta'])+'.</strong> '+html.escape(n['detalle'])+'</p>' for n in nodes)+'</details>'
csv6=(PREP/'F06_relaciones.csv').read_text(encoding='utf8')
script='<script id="datos-mecanismos" type="application/json">'+payload6+'</script><script>(()=>{const p=JSON.parse(document.getElementById("datos-mecanismos").textContent),csv='+json.dumps(csv6,ensure_ascii=False)+''';function draw(){const r=p.relaciones[Number(document.getElementById('mecanismo').value)],a=p.nodos.find(n=>n.id===r.origen),b=p.nodos.find(n=>n.id===r.destino),s=document.getElementById('lectura');s.replaceChildren();const t=document.createElement('strong');t.textContent=a.etiqueta+' → '+b.etiqueta+'. '+r.etiqueta+'. ';s.appendChild(t);s.appendChild(document.createTextNode(b.detalle+' '));const link=document.createElement('a');link.href=r.url;link.textContent='Consultar referencia de apoyo';link.target='_blank';link.rel='noopener';s.appendChild(link)}document.getElementById('mecanismo').addEventListener('change',draw);document.getElementById('descargar').addEventListener('click',()=>{const u=URL.createObjectURL(new Blob(['\\uFEFF',csv],{type:'text/csv;charset=utf-8'})),a=document.createElement('a');a.href=u;a.download='F06_relaciones.csv';document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),30000)});draw()})();</script>'''
(INTER/'F06-mecanismos-territoriales.html').write_text(page('Mecanismos territoriales',body,script),encoding='utf8')

# PNGs derive from the exact vector PDF, avoiding two drawing implementations.
poppler=shutil.which('pdftoppm')
if not poppler:raise RuntimeError('Falta pdftoppm (Poppler) para generar los PNG desde los PDF vectoriales.')
for name in ['F03-agua-renovable','F05-agua-poblacion','F06-mecanismos-territoriales']:
    subprocess.run([poppler,'-singlefile','-scale-to','2400','-png',str(STATIC/(name+'.pdf')),str(STATIC/name)],check=True)

report={'fecha_consulta':'2026-11-05','fuente':'CONAGUA EAM2023 (marzo 2024), pp.16/27 impresas; posiciones PDF24/35','rha':13,'total_agua_hm3_anio':461640,'total_poblacion_millones':129.35,'porcentaje_agua_suma':sum(r['porcentaje_agua'] for r in data),'porcentaje_poblacion_suma':sum(r['porcentaje_poblacion'] for r in data),'transcripcion_contrastada_13_filas':True,'geometria_regiones':len(geo),'vertices_originales':before,'vertices_dibujo':after,'tolerancia_dibujo_m':1000,'anclas_interiores':all(inside(g['anchor'],max(g['rings'],key=lambda ring:abs(ringarea(ring)))) for g in geo),'F06_nodos':len(nodes),'F06_relaciones':len(rels),'rha_json_descomprimido_sha256':hashlib.sha256(gzip.decompress(geomfile.read_bytes())).hexdigest(),'insumos':[{'archivo':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in [ORIG/'EAM2023_extracto-editorial-cuadros.pdf',ORIG/'EAM2023_tabla-1-5-2_transcripcion.csv',geomfile]],'comprobaciones':{'unidades_y_nombres':True,'denominadores_nacionales_constantes':True,'sin_PIB_asignado_a_RHA':True,'sin_reparto_espacial':True,'sin_causalidad_cuantificada':True}}
dump(ROOT/'seguimiento/auditoria-agua-sintesis.json',report)
print(json.dumps(report,ensure_ascii=False,indent=2))
