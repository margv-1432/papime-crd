"""B02 F04: fuentes congeladas, agregación y salidas independientes.

Ejecutar desde la raíz del repositorio con Python 3 (openpyxl, reportlab,
pypdfium2 y Pillow). --extraer-fuentes requiere los dos anuarios originales
en tmp/fuentes/F04 y pdfplumber; normalmente se usan los extractos congelados.
La compilación nunca descarga ni actualiza series.
"""
from pathlib import Path
import argparse, base64, collections, csv, hashlib, html, io, json, math, re
from decimal import Decimal
import openpyxl
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
import pypdfium2 as pdfium
from PIL import Image, ImageChops

ROOT=Path(__file__).resolve().parents[2]
RAW=ROOT/'datos/originales/capitulo-01/F04'
PREP=ROOT/'datos/preparados/capitulo-01'
ASSET=ROOT/'assets/capitulo-01'
TMP=ROOT/'tmp/fuentes/F04'
NAMES=['Aguascalientes','Baja California','Baja California Sur','Campeche','Coahuila de Zaragoza','Colima','Chiapas','Chihuahua','Ciudad de México','Durango','Guanajuato','Guerrero','Hidalgo','Jalisco','México','Michoacán','Morelos','Nayarit','Nuevo León','Oaxaca','Puebla','Querétaro','Quintana Roo','San Luis Potosí','Sinaloa','Sonora','Tabasco','Tamaulipas','Tlaxcala','Veracruz','Yucatán','Zacatecas']
STATES={f'{i:02}':n for i,n in enumerate(NAMES,1)}
ALIASES={n.upper():k for k,n in STATES.items()}
ALIASES.update({'COAHUILA':'05','ESTADO DE MÉXICO':'15','MICHOACAN':'16'})

def write_csv(path, rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def read_csv(path):
    with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def extract():
    import pdfplumber
    with pdfplumber.open(TMP/'SGM-Anuario_2023_Edicion_2024.pdf') as d:
        page=d.pages[114]
        labels=[s for s in page.crop((20,145,177,430)).extract_text().splitlines() if s.startswith('Total') or s.upper() in ALIASES]
        values=page.crop((510,145,590,430)).extract_text().splitlines()
        assert len(labels)==len(values)==20
        rows=[]
        for name,s in zip(labels,values):
            if name.startswith('Total'):key='00'
            else:key=ALIASES[name.upper()]
            rows.append(dict(cve_ent=key,entidad='Total nacional publicado' if key=='00' else STATES[key],valor_original_2023=s,valor_t='' if s=='-' else Decimal(s.replace(' ','')),pagina_impresa=115,cuadro='7.4'))
        write_csv(RAW/'SGM-cuadro7.4-cobre2023-extracto.csv',rows)
    from pypdf import PdfReader
    d=PdfReader(TMP/'CONAPESCA-Anuario-2023.pdf')
    if d:
        datasets=[]
        for page_id,field in [(108,'total_sector_peso_vivo_t'),(132,'acuacultura_peso_vivo_t')]:
            text=d.pages[page_id].extract_text().replace('CUADRO 2.1.5','')
            rows=[]
            for line in text.splitlines():
                m=re.match(r'^([A-ZÁÉÍÓÚÜÑ ]+?)\s+([0-9,]+)(?:\s+([0-9,]+))?',line)
                if not m:continue
                label=m[1].strip()
                if label=='TOTAL':key='00'
                elif label in ALIASES:key=ALIASES[label]
                else:continue
                # El cuadro2.1.5 tiene desembarcado en primera columna y vivo en segunda.
                value=int(m[3 if page_id==108 else 2].replace(',',''))
                rows.append(dict(cve_ent=key,entidad='Total nacional publicado' if key=='00' else STATES[key],**{field:value},pagina_impresa=page_id+1))
            assert len(rows)==32 and len(set(r['cve_ent'] for r in rows))==32
            datasets.append({r['cve_ent']:r for r in rows})
        fish=[]
        for k in datasets[0]:
            fish.append(dict(cve_ent=k,entidad=datasets[0][k]['entidad'],total_sector_peso_vivo_t=datasets[0][k]['total_sector_peso_vivo_t'],acuacultura_peso_vivo_t=datasets[1][k]['acuacultura_peso_vivo_t'],paginas_impresas='109;133',cuadros='2.1.5;2.3.3'))
        write_csv(RAW/'CONAPESCA-cuadros2.1.5-2.3.3-2023-extracto.csv',fish)

def vegetation():
    # Se conserva la correspondencia completa recibida, incluso la categoría nula.
    a=json.loads((RAW/'vegetacion-semarnat-correspondencia.json').read_text(encoding='utf8'))
    assert not a.get('exceededTransferLimit')
    original=[r['attributes'] for r in a['features']]
    groups={
      'Bosques templados':'#315F3C','Bosque mesófilo':'#3C8779','Selvas':'#76A566',
      'Matorral xerófilo':'#B3A06A','Pastizal':'#D5C282','Otra vegetación':'#8EBFB0',
      'Vegetación inducida':'#B8BD9B','Agricultura y acuícola':'#E7E1CF',
      'Bosque cultivado':'#7F9952','Sin vegetación o asentamiento':'#D1D1CD','Agua':'#9CBED2'}
    out=[]
    for r in original:
        f=r['FORM_VEG_INEGI'];k=r['CLAVE']
        if f in ('BOSQUE DE CONÍFERAS','BOSQUE DE ENCINO'):g='Bosques templados'
        elif f=='BOSQUE MESÓFILO DE MONTAÑA':g='Bosque mesófilo'
        elif f and f.startswith('SELVA '):g='Selvas'
        elif f=='MATORRAL XERÓFILO':g='Matorral xerófilo'
        elif f=='PASTIZAL':g='Pastizal'
        elif f in ('OTROS TIPOS','VEGETACIÓN HIDRÓFILA'):g='Otra vegetación'
        elif f in ('VEGETACIÓN INDUCIDA','Pastizal inducido y cultivado'):g='Vegetación inducida'
        elif f and (f.startswith('Agricultura') or f=='Acuícola'):g='Agricultura y acuícola'
        elif f=='Bosque cultivado':g='Bosque cultivado'
        elif k in ('AH','ADV','DV'):g='Sin vegetación o asentamiento'
        elif k=='H2O':g='Agua'
        else:raise ValueError(r)
        out.append(dict(clave=k,descripcion=r['DESCRIPCIO'],formacion_original=f or '',grupo=g,color=groups[g]))
    assert len(out)==183 and len(set(r['clave'] for r in out))==183
    write_csv(PREP/'F04_correspondencia_vegetacion.csv',out)
    infos=[]
    for r in out:
        h=r['color'];rgb=[int(h[i:i+2],16) for i in (1,3,5)]
        infos.append(dict(value=r['clave'],label=r['grupo'],symbol=dict(type='esriSFS',style='esriSFSSolid',color=rgb+[255],outline=None)))
    dynamic=[dict(id=2,source=dict(type='mapLayer',mapLayerId=2),drawingInfo=dict(renderer=dict(type='uniqueValue',field1='CLAVE',uniqueValueInfos=infos,defaultSymbol=dict(type='esriSFS',style='esriSFSSolid',color=[230,0,230,255],outline=None))))]
    sr=json.loads((RAW/'vegetacion-semarnat-layers.json').read_text(encoding='utf8'))['layers']
    sr=next(x for x in sr if x['id']==2)['sourceSpatialReference']['wkt']
    request=dict(f='image',bbox='700000,200000,4230000,2420000',bboxSR=json.dumps(dict(wkt=sr)),imageSR=json.dumps(dict(wkt=sr)),size='1600,1006',format='png32',transparent='true',dpi='150',dynamicLayers=json.dumps(dynamic,ensure_ascii=False,separators=(',',':')))
    (PREP/'F04_solicitud_cobertura.json').write_text(json.dumps(request,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return out,groups

def prepare():
    rawc=read_csv(RAW/'SGM-cuadro7.4-cobre2023-extracto.csv');c={r['cve_ent']:r for r in rawc}
    copper=[]
    for k,n in STATES.items():
        r=c.get(k);s=r['valor_original_2023'] if r else ''
        status='sin_fila_en_cuadro' if not r else 'guion_publicado' if s=='-' else 'cero_explicito' if Decimal(r['valor_t'])==0 else 'numerico_publicado'
        copper.append(dict(cve_ent=k,entidad=n,valor_t=r['valor_t'] if r else '',estado_dato=status,valor_original_2023=s,periodo=2023,unidad='toneladas de metal',fuente='SGM 2024 cuadro7.4 p115; preliminar'))
    assert collections.Counter(r['estado_dato'] for r in copper)==dict(numerico_publicado=12,cero_explicito=1,guion_publicado=6,sin_fila_en_cuadro=13)
    assert sum(Decimal(r['valor_t']) for r in copper if r['valor_t'])==Decimal(c['00']['valor_t'])==Decimal('778838.95')
    assert c['26']['valor_t']=='550597.50'
    write_csv(PREP/'F04_A_cobre_2023.csv',copper)
    w=openpyxl.load_workbook(RAW/'SEMARNAT-Produccion-forestal-2019-2024.xlsx',read_only=True,data_only=True)
    source=[r for r in list(w['Datos'].values)[1:] if r[0]==2023]
    assert len(source)==292 and set(r[5] for r in source)=={'m3r'}
    assert len(set((r[0],r[1],r[3],r[4]) for r in source))==292
    wood=collections.defaultdict(Decimal)
    for r in source:wood[ALIASES[r[1].upper()]]+=Decimal(str(r[6]))
    timber=[dict(cve_ent=k,entidad=n,volumen_m3r=wood[k],filas_elementales=sum(ALIASES[r[1].upper()]==k for r in source),periodo=2023,unidad='m3 de madera en rollo',fuente='SEMARNAT base2019-2024; actualizacion21-09-2026') for k,n in STATES.items()]
    assert len(wood)==32 and abs(float(sum(wood.values()))-6621041.399495694)<1e-6
    write_csv(PREP/'F04_B_madera_2023.csv',timber)
    f={r['cve_ent']:r for r in read_csv(RAW/'CONAPESCA-cuadros2.1.5-2.3.3-2023-extracto.csv')}
    fishing=[]
    for k,n in STATES.items():
        r=f.get(k)
        fishing.append(dict(cve_ent=k,entidad=n,total_sector_peso_vivo_t=r['total_sector_peso_vivo_t'] if r else '',acuacultura_peso_vivo_t=r['acuacultura_peso_vivo_t'] if r else '',estado_dato='numerico_publicado' if r else 'sin_fila_en_cuadro',periodo=2023,unidad='toneladas en peso vivo',fuente='CONAPESCA Anuario2023 cuadros2.1.5 y2.3.3 pp109;133'))
    assert len(f)==32 and '09' not in f and int(f['00']['total_sector_peso_vivo_t'])==2150294
    assert sum(int(r['total_sector_peso_vivo_t']) for r in fishing if r['total_sector_peso_vivo_t'])==2150294
    assert sum(int(r['acuacultura_peso_vivo_t']) for r in fishing if r['acuacultura_peso_vivo_t'])==304732 and int(f['00']['acuacultura_peso_vivo_t'])==304731
    assert all(int(r['acuacultura_peso_vivo_t'])<=int(r['total_sector_peso_vivo_t']) for r in fishing if r['total_sector_peso_vivo_t'])
    write_csv(PREP/'F04_C_pesca_acuacultura_2023.csv',fishing)
    return copper,timber,fishing

def short(s):
    return {'Coahuila de Zaragoza':'Coahuila','Baja California Sur':'B. California Sur','Baja California':'Baja California','Ciudad de México':'Ciudad de México','San Luis Potosí':'San Luis Potosí'}.get(s,s)

def mask_coverage():
    original=Image.open(RAW/'vegetacion-agrupada-1600.png').convert('RGBA')
    mask=Image.open(PREP/'F04_mascara_MG2020.tif').convert('L')
    assert original.size==mask.size==(1600,1006)
    mask=mask.point(lambda v:255 if v==1 else 0)
    original.putalpha(ImageChops.multiply(original.getchannel('A'),mask))
    assert not any(r==230 and g==0 and b==230 and a>0 for r,g,b,a in original.getdata())
    original.save(PREP/'F04_cubierta_recortada.png')

def static(copper,timber,fishing,groups):
    out=ASSET/'figuras-estaticas';out.mkdir(parents=True,exist_ok=True)
    font=Path('C:/Windows/Fonts/arial.ttf');bold=Path('C:/Windows/Fonts/arialbd.ttf')
    if font.exists():pdfmetrics.registerFont(TTFont('F04Arial',str(font)));pdfmetrics.registerFont(TTFont('F04ArialBold',str(bold)))
    else:raise RuntimeError('Instale Arial o sustituya explícitamente las dos fuentes del gráfico.')
    W,H=540,590;c=canvas.Canvas(str(out/'F04-recursos.pdf'),pagesize=(W,H),pageCompression=1)
    c.setTitle('F04 Aprovechamientos regionales registrados')
    def text(x,y,s,size=9,bold=False,color='#26343B'):
        c.setFillColor(HexColor(color));c.setFont('F04ArialBold' if bold else 'F04Arial',size);c.drawString(x,y,s)
    def line(x,y,x2,y2,color='#DDE4E7'):
        c.setStrokeColor(HexColor(color));c.setLineWidth(.4);c.line(x,y,x2,y2)
    def bars(rows,field,x,top,w,h,color,title,unit,n=10,second=None):
        text(x,top,title,11,True,'#0F4761');text(x,top-15,unit,8.8)
        rr=sorted([r for r in rows if r[field]!=''],key=lambda r:float(r[field]),reverse=True)[:n]
        yy=top-34;rh=(h-50)/max(n,1);left=112;barw=w-left-29
        maximum=max(float(r[field]) for r in rr)/1000
        ticks= [0,200,400,600] if maximum>500 else [0,500,1000,1500] if maximum>1000 else [0,100,200,300,400]
        # Adaptar las marcas a la escala de cada panel, sin mezclar unidades.
        if field=='volumen_m3r':ticks=[0,500,1000,1500]
        if field=='total_sector_peso_vivo_t':ticks=[0,300,600,900]
        xmax=max(ticks[-1],maximum)*1.04
        for tick in ticks:
            xx=x+left+tick/xmax*barw;line(xx,yy+5,xx,yy-(n-1)*rh-7);text(xx-5,yy-(n-1)*rh-20,str(tick),7.7)
        for i,r in enumerate(rr):
            y=yy-i*rh;value=float(r[field])/1000
            text(x,y-2,short(r['entidad']),8.7)
            c.setFillColor(HexColor(color));c.rect(x+left,y-3,value/xmax*barw,6.5,stroke=0,fill=1)
            if second:
                v=float(r[second])/1000;c.setFillColor(HexColor('#A99C4D'));c.rect(x+left,y-6,v/xmax*barw,3,stroke=0,fill=1)
            if i<3:text(x+left+value/xmax*barw+3,y-2,f'{value:,.1f}'.replace(',',' '),7.6)
        return yy-(n-1)*rh-32
    text(16,568,'Aprovechamientos regionales registrados',15,True,'#0F4761')
    text(16,550,'Producción de 2023; cubierta vegetal de base 2018, Serie VII',9.5)
    end=bars(copper,'valor_t',16,526,508,195,'#9A633B','A. Cobre preliminar','Miles de toneladas de metal; las 13 entidades con valor numérico',13)
    text(16,320,'Guion y ausencia de fila se conservan como faltantes. Jalisco publica 0.',8.2)
    line(16,308,524,308)
    text(16,290,'B. Cubierta vegetal',11,True,'#0F4761')
    text(16,276,'Serie VII; agrupación de 183 claves',8.6)
    c.drawImage(ImageReader(str(PREP/'F04_cubierta_recortada.png')),16,130,width=250,height=138,mask='auto',preserveAspectRatio=True)
    names=list(groups);legend_y=122
    for i,g in enumerate(names):
        col=i%2;row=i//2;x=16+col*125;y=legend_y-row*11
        c.setFillColor(HexColor(groups[g]));c.rect(x,y-1,7,7,fill=1,stroke=0);text(x+10,y,g,6.6)
    text(16,49,'Vegetación primaria y secundaria reunidas.',7.5)
    bars(timber,'volumen_m3r',278,290,246,190,'#347560','C. Producción maderable','Miles de m³ rollo; diez mayores registros',10)
    text(278,90,'Total de 32 entidades; incluye plantaciones.',7.5)
    text(16,20,'Fuentes: SGM 2024; INEGI Serie VII/SEMARNAT; base forestal SEMARNAT 2019–2024.',7.7)
    c.showPage()
    # El segundo folio conserva el detalle de pesca con letras grandes y evita
    # reducir cuatro paneles hasta volver ilegibles sus rótulos en el libro.
    text(16,568,'Aprovechamientos regionales registrados',15,True,'#0F4761')
    text(16,550,'Continuación de F04',9.5)
    bars(fishing,'total_sector_peso_vivo_t',16,520,508,430,'#2A6381','D. Pesca y acuacultura registradas','Miles de toneladas en peso vivo; 31 entidades con fila publicada',31,'acuacultura_peso_vivo_t')
    text(16,65,'Azul: total del sector. Ocre: acuacultura incluida en el total.',9)
    text(16,49,'La entidad de registro puede diferir del sitio de captura. Ciudad de México sin fila.',8.5)
    text(16,33,'Fuentes: SGM 2024 p.115; SEMARNAT base 2019–2024; CONAPESCA 2023 pp.109,133.',7.7)
    text(16,20,'Cubierta: INEGI Serie VII, servicio SEMARNAT; renderizado AEA, sin medición de áreas.',7.7)
    c.save()
    d=pdfium.PdfDocument(str(out/'F04-recursos.pdf'))
    for i in range(len(d)):
        image=d[i].render(scale=2.5).to_pil();image.save(out/f'F04-recursos-{i+1}.png')
    # Vista principal mantiene primera página; la segunda tiene salida explícita.
    (out/'F04-recursos.png').write_bytes((out/'F04-recursos-1.png').read_bytes())
    # Paneles individuales legibles para situarlos junto a la prosa. Todos
    # reutilizan las tablas completas; C aquí conserva las32entidades.
    for suffix,title in [('A-cobre','A. Cobre preliminar'),('B-cubierta','B. Cubierta vegetal'),('C-madera','C. Producción maderable'),('D-pesca','D. Pesca y acuacultura')]:
        height=420 if suffix.startswith(('A','B')) else 610
        target=out/f'F04-{suffix}.pdf'
        c=canvas.Canvas(str(target),pagesize=(540,height),pageCompression=1)
        c.setTitle('F04 '+title)
        if suffix.startswith('A'):
            bars(copper,'valor_t',16,390,508,285,'#9A633B',title,'2023; miles de toneladas de metal; valores numéricos publicados',13)
            text(16,70,'Seis guiones y trece entidades sin fila se conservan como faltantes.',9)
            text(16,51,'Jalisco publica cero. Sonora registra 550 597.50 t; cifras preliminares.',9)
            text(16,30,'Fuente: SGM, Anuario 2023, edición 2024, cuadro 7.4, p.115.',9)
        elif suffix.startswith('B'):
            text(16,390,title,13,True,'#0F4761');text(16,371,'Serie VII, base de imágenes 2018; agrupación exhaustiva de 183 claves',9.4)
            c.drawImage(ImageReader(str(PREP/'F04_cubierta_recortada.png')),16,131,width=508,height=235,mask='auto',preserveAspectRatio=True)
            for i,g in enumerate(groups):
                col=i%3;row=i//3;x=16+col*172;y=118-row*16
                c.setFillColor(HexColor(groups[g]));c.rect(x,y-1,8,8,fill=1,stroke=0);text(x+11,y,g,8.1)
            text(16,45,'Vegetación primaria y secundaria reunidas por formación para la lectura nacional.',8.5)
            text(16,27,'Fuente: INEGI, Serie VII, servicio SEMARNAT; recorte al contorno MG2020.',8.5)
        elif suffix.startswith('C'):
            bars(timber,'volumen_m3r',16,580,508,478,'#347560',title,'2023; miles de m³ de madera en rollo; 32 entidades',32)
            text(16,58,'Suma de 292 filas elementales; incluye plantaciones y otras autorizaciones.',8.8)
            text(16,39,'Fuente: SEMARNAT, base 2019–2024; última actualización 21-09-2026.',8.8)
        else:
            bars(fishing,'total_sector_peso_vivo_t',16,580,508,478,'#2A6381',title,'2023; miles de toneladas en peso vivo; 31 entidades con fila',31,'acuacultura_peso_vivo_t')
            text(16,58,'Azul: total sectorial. Ocre: acuacultura incluida. Ciudad de México sin fila.',8.8)
            text(16,39,'Fuente: CONAPESCA, Anuario 2023, cuadros 2.1.5 y 2.3.3, pp.109,133.',8.8)
        c.save()
        panel=pdfium.PdfDocument(str(target));panel[0].render(scale=2.5).to_pil().save(target.with_suffix('.png'))

def interactive(copper,timber,fishing,groups):
    rows=[]
    for a,b,d in zip(copper,timber,fishing):
        rows.append(dict(id=a['cve_ent'],entidad=a['entidad'],cobre=None if a['valor_t']=='' else float(a['valor_t']),estado_cobre=a['estado_dato'],madera=float(b['volumen_m3r']),pesca=None if d['total_sector_peso_vivo_t']=='' else int(d['total_sector_peso_vivo_t']),acuacultura=None if d['acuacultura_peso_vivo_t']=='' else int(d['acuacultura_peso_vivo_t'])))
    payload=json.dumps(rows,ensure_ascii=False,allow_nan=False).replace('<','\\u003c')
    cover=base64.b64encode((PREP/'F04_cubierta_recortada.png').read_bytes()).decode()
    legend=''.join('<span><i style="background:'+v+'"></i>'+html.escape(k)+'</span>' for k,v in groups.items())
    downloads=[]
    for name in ['F04_A_cobre_2023.csv','F04_B_madera_2023.csv','F04_C_pesca_acuacultura_2023.csv','F04_correspondencia_vegetacion.csv']:
        data=base64.b64encode((PREP/name).read_bytes()).decode()
        downloads.append(f'<a download="{name}" href="data:text/csv;charset=utf-8;base64,{data}">{html.escape(name)}</a>')
    doc='''<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>F04 Aprovechamientos regionales registrados</title><style>
*{box-sizing:border-box}body{font:16px/1.55 Arial,sans-serif;color:#26343b;margin:0;background:#fff}main{max-width:1000px;margin:auto;padding:20px}h1{font-size:1.5rem;color:#0f4761;margin:0 0 10px}h2{font-size:1.15rem;color:#0f4761}label,select,button{font:inherit}select,button{padding:8px;border:1px solid #667b84;border-radius:4px;background:#fff}select:focus,button:focus,a:focus{outline:3px solid #a56532;outline-offset:3px}.controls{display:flex;gap:16px;flex-wrap:wrap;align-items:center}.note{font-size:.91rem;color:#43545c}.legend{display:flex;flex-wrap:wrap;gap:5px 16px;font-size:.85rem}.legend i{display:inline-block;width:13px;height:13px;margin-right:5px}.map{width:100%;max-height:500px;object-fit:contain}svg{width:100%;min-width:740px;display:block}#chart{overflow:auto}table{border-collapse:collapse;width:100%;font-size:.86rem}th,td{padding:6px 8px;border-bottom:1px solid #dce4e7;text-align:right}th:first-child,td:first-child{text-align:left}th{background:#eef3f5}.tablewrap{overflow:auto}a{color:#0f4761}.downloads{display:flex;gap:14px;flex-wrap:wrap;font-size:.85rem}[hidden]{display:none!important}.status{color:#53636b}summary{cursor:pointer;padding:8px 0}</style><main>
<h1>Aprovechamientos regionales registrados</h1><p class="note">Producción de 2023; cubierta vegetal Serie VII, base 2018. Cada panel conserva su unidad. La acuacultura forma parte del total pesquero.</p>
<div class="controls"><label for="panel">Panel <select id="panel"><option value="cobre">A. Cobre preliminar</option><option value="cubierta">B. Cubierta vegetal</option><option value="madera">C. Producción maderable</option><option value="pesca">D. Pesca y acuacultura</option></select></label><label for="order" id="order-label">Orden <select id="order"><option value="valor">Mayor a menor</option><option value="entidad">Clave estatal</option></select></label><button id="reset" type="button">Restablecer</button></div>
<p id="description"></p><div id="chart"></div><div id="coverage" hidden><img class="map" alt="Distribución nacional agrupada de la vegetación Serie VII, con bosques templados en las sierras y selvas en vertientes tropicales; mapa descriptivo sin cálculo de superficies" src="data:image/png;base64,COVER"><div class="legend">LEGEND</div><p class="note">La imagen de referencia reúne las 183 claves del servicio de SEMARNAT. La vegetación primaria y secundaria se agrupa por formación, mientras que los usos agrícolas y acuícolas, el bosque cultivado y las áreas sin vegetación mantienen categorías propias. El renderizado nacional permite comparar patrones amplios; el detalle por predio requiere cartografía de otra escala.</p></div>
<details open id="table-section"><summary>Tabla completa de 32 entidades</summary><div class="tablewrap"><table><thead id="thead"></thead><tbody id="tbody"></tbody></table></div></details>
<p class="note" id="limits"></p><details><summary>Fuentes, cobertura y descargas</summary><p class="note">Cobre: SGM, <a href="https://www.sgm.gob.mx/productos/pdf/Anuario_2023_Edicion_2024.pdf">Anuario 2023, edición 2024</a>, cuadro 7.4 p.115, cifras preliminares. Madera: SEMARNAT, <a href="https://anuarios.semarnat.gob.mx/wp-content/uploads/2026/10/Produccion-forestal-maderable-de-Mexico-2019-2024.xlsx">base 2019–2024</a>, observación 2023, actualización 21-09-2026; se agregan 292 filas elementales. Pesca: CONAPESCA, <a href="https://nube.conapesca.gob.mx/sites/cona/dgppe/2023/ANUARIO_ESTADISTICO_DE_ACUACULTURA_Y_PESCA_2023.pdf">Anuario 2023</a>, cuadros 2.1.5 p.109 y 2.3.3 p.133. Cubierta: INEGI Serie VII, base de imágenes 2018, publicada 2021; <a href="https://geomaticasig1.semarnat.gob.mx/arcgis/rest/services/aps/SDF_nacional_DGFDUA/MapServer/2">servicio SEMARNAT</a>, agrupación propia registrada por clave. Consulta de fuentes 05-11-2026.</p><div class="downloads">DOWNLOADS</div></details>
<script>const DATA=PAYLOAD;
const $=id=>document.getElementById(id),fmt=(v,d=2)=>v===null?'Sin fila':v.toLocaleString('es-MX',{maximumFractionDigits:d}),NS='http://www.w3.org/2000/svg';
const meta={cobre:{unit:'Toneladas de metal',field:'cobre',desc:'Producción preliminar de cobre por entidad, 2023. Las barras usan miles de toneladas.',limit:'Los seis guiones publicados y las trece entidades sin fila permanecen como faltantes, distintos del cero explícito de Jalisco. El panel compara producción registrada por entidad. Los puntos del directorio minero se descartaron porque su localización física no pudo certificarse.'},madera:{unit:'m³ de madera en rollo',field:'madera',desc:'Producción maderable por entidad, 2023. Las barras usan miles de m³ rollo.',limit:'La producción registrada incluye plantaciones forestales comerciales y otros tipos de autorización. La agregación utiliza las 292 filas elementales de 2023 y conserva el volumen de madera en rollo.'},pesca:{unit:'Toneladas en peso vivo',field:'pesca',desc:'Total pesquero y acuacultura por entidad de registro, 2023. Las barras usan miles de toneladas.',limit:'La acuacultura forma parte del total sectorial. La fuente publica 304 731 t para el país, mientras que la suma de las 31 filas estatales da 304 732 t; se conserva esa diferencia de redondeo. Ciudad de México carece de fila. Las cifras corresponden a la entidad de registro, que puede diferir del sitio de captura.'}};
function el(tag,attrs,text){const e=document.createElementNS(NS,tag);Object.entries(attrs||{}).forEach(([k,v])=>e.setAttribute(k,v));if(text!==undefined)e.textContent=text;return e}
function draw(){const p=$('panel').value,cover=p==='cubierta';$('coverage').hidden=!cover;$('chart').hidden=cover;$('order-label').hidden=cover;$('table-section').hidden=cover;
if(cover){$('description').textContent='Cubierta vegetal de base 2018, Serie VII; agrupación de formaciones para comparación nacional.';$('limits').textContent='Las categorías describen la cubierta de base 2018. Medir superficies o estudiar cambios posteriores requiere un análisis específico de las capas.';return}
const m=meta[p],rows=[...DATA].sort((a,b)=>$('order').value==='entidad'?a.id.localeCompare(b.id):(b[m.field]??-1)-(a[m.field]??-1));$('description').textContent=m.desc;$('limits').textContent=m.limit;
const vals=rows.filter(r=>r[m.field]!==null),w=900,l=180,r=75,barw=w-l-r,rh=25,h=55+vals.length*rh,maximum=Math.max(...vals.map(x=>x[m.field]))/1000,scale=barw/(maximum*1.06||1);const svg=el('svg',{viewBox:`0 0 ${w} ${h}`,role:'img','aria-label':m.desc});
for(let i=0;i<5;i++){const tick=maximum*i/4,x=l+tick*scale;svg.append(el('line',{x1:x,x2:x,y1:22,y2:h-25,stroke:'#dce4e7'}));svg.append(el('text',{x:x,y:15,'text-anchor':'middle','font-size':12,fill:'#43545c'},fmt(tick,1)))}
vals.forEach((v,i)=>{const y=40+i*rh;svg.append(el('text',{x:l-9,y:y+4,'text-anchor':'end','font-size':13,fill:'#26343b'},v.entidad));const bar=el('rect',{x:l,y:y-7,width:v[m.field]/1000*scale,height:13,fill:p==='cobre'?'#9A633B':p==='madera'?'#347560':'#2A6381'});bar.append(el('title',{},v.entidad+': '+fmt(v[m.field])+' '+m.unit));svg.append(bar);if(p==='pesca'){const aqua=el('rect',{x:l,y:y+4,width:v.acuacultura/1000*scale,height:4,fill:'#A99C4D'});aqua.append(el('title',{},'Acuacultura: '+fmt(v.acuacultura)+' t, incluida en total'));svg.append(aqua)}svg.append(el('text',{x:l+v[m.field]/1000*scale+5,y:y+4,'font-size':12,fill:'#26343b'},fmt(v[m.field]/1000,1)))});$('chart').replaceChildren(svg);
$('thead').innerHTML='<tr><th>Clave · Entidad</th><th>'+m.unit+'</th>'+(p==='pesca'?'<th>Acuacultura incluida (t)</th>':'')+(p==='cobre'?'<th>Estado del dato</th>':'')+'</tr>';
const tbody=$('tbody');tbody.replaceChildren();rows.forEach(v=>{const tr=document.createElement('tr');const a=[v.id+' · '+v.entidad,p==='cobre'&&v.cobre===null?(v.estado_cobre==='guion_publicado'?'Guion':'Sin fila'):fmt(v[m.field],p==='pesca'?0:6)];if(p==='pesca')a.push(fmt(v.acuacultura,0));if(p==='cobre')a.push(v.estado_cobre.replaceAll('_',' '));a.forEach(t=>{const td=document.createElement('td');td.textContent=t;tr.append(td)});tbody.append(tr)})}
$('panel').addEventListener('change',draw);$('order').addEventListener('change',draw);$('reset').addEventListener('click',()=>{$('panel').value='cobre';$('order').value='valor';draw()});draw();
</script></main></html>'''
    doc=doc.replace('COVER',cover).replace('LEGEND',legend).replace('DOWNLOADS',''.join(downloads)).replace('PAYLOAD',payload)
    target=ASSET/'interactivos/F04-recursos.html';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(doc,encoding='utf8')

def main():
    args=argparse.ArgumentParser();args.add_argument('--extraer-fuentes',action='store_true');args.add_argument('--preparar-solicitud',action='store_true');args=args.parse_args()
    PREP.mkdir(parents=True,exist_ok=True)
    if args.extraer_fuentes:extract()
    _,groups=vegetation()
    if args.preparar_solicitud:return
    copper,timber,fishing=prepare();mask_coverage();static(copper,timber,fishing,groups);interactive(copper,timber,fishing,groups)
    table=ASSET/'tablas';table.mkdir(parents=True,exist_ok=True)
    for f in PREP.glob('F04_*.csv'):(table/f.name).write_bytes(f.read_bytes())
    checks=dict(figura='F04',fuentes_consultadas='2026-11-05',cobre=dict(filas=32,numericos=13,guiones=6,sin_fila=13,total_t=778838.95,sonora_t=550597.50),madera=dict(filas_elementales_2023=292,entidades=32,total_m3r=float(sum(Decimal(r['volumen_m3r']) for r in timber))),pesca=dict(filas_estatales=31,total_nacional_t=2150294,acuacultura_nacional_publicada_t=304731,acuacultura_suma_estatal_t=304732,discrepancia_redondeo_t=1),vegetacion=dict(claves=183,grupos=len(groups),servicio='SEMARNAT; fuente INEGI SerieVII',medicion_superficies=False),fuentes=[dict(archivo=str(p.relative_to(ROOT)).replace('\\','/'),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in RAW.iterdir() if p.is_file()])
    (ROOT/'seguimiento/auditoria-F04.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps(checks,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
