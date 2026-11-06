"""Coteja la revisión editorial con el checkpoint previo y con ambas lecturas."""
from pathlib import Path
from html.parser import HTMLParser
from collections import Counter
import argparse, csv, json, re, subprocess, unicodedata
from pypdf import PdfReader

R = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--base', default='e6c1f99f2512cf24fde4077cec4d9efabeef1087')
args = parser.parse_args()
checks = []
def check(name, ok, detail=''):
    checks.append(dict(prueba=name, correcto=bool(ok), detalle=detail))
def previous(path):
    return subprocess.check_output(['git', 'show', args.base+':'+path], cwd=R)
def norm(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', text).casefold() if c.isalnum())

for name in ['01-territorio.Rmd', '02-piloto-especializacion.Rmd']:
    path = 'libro/capitulos/'+name
    old = previous(path).decode('utf8'); new = (R/path).read_text(encoding='utf8')
    for label, pattern in [
        ('citas y localizadores', r'\[[^\]\n]*@[\s\S]*?\]'),
        ('chunks R', r'```\{r[\s\S]*?```'),
        ('cálculos R en línea', r'`r [^`]+`'),
        ('ecuaciones', r'\\\[[\s\S]*?\\\]'),
        ('fórmulas en línea', r'(?<!\$)\$[^$\n]+\$(?!\$)')]:
        a, b = old, new
        if label=='fórmulas en línea':
            a=re.sub(r'`[^`]*`','',a); b=re.sub(r'`[^`]*`','',b)
        check(name+': '+label, Counter(re.findall(pattern, a)) == Counter(re.findall(pattern, b)))

# La única tabla preparada modificable por esta revisión es el texto de nodos F06.
changed = subprocess.check_output(['git','diff','--name-only',args.base,'--','datos','referencias','libro/bibliografia.bib'], cwd=R).decode().splitlines()
allowed = {'datos/preparados/capitulo-01/F06_nodos.csv', 'datos/preparados/capitulo-01/manifiesto-B02.csv'}
check('Datos cuantitativos, originales y bibliografía intactos', set(changed) <= allowed, changed)
node_path='datos/preparados/capitulo-01/F06_nodos.csv'
old_nodes=list(csv.DictReader(previous(node_path).decode('utf8').splitlines()))
new_nodes=list(csv.DictReader((R/node_path).open(encoding='utf8')))
check('F06 conserva nodos, etiquetas y tipos',
      [{k:v for k,v in n.items() if k!='detalle'} for n in old_nodes] ==
      [{k:v for k,v in n.items() if k!='detalle'} for n in new_nodes])

class Paragraphs(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.active=False; self.current=None; self.paragraphs=[]; self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag=='section' and attrs.get('class')=='normal': self.active=True
        if self.active and tag=='p':
            self.current=[] if attrs.get('class','') not in ('alternativa','enlaces-edicion') else None
    def handle_data(self, data):
        if self.current is not None: self.current.append(data)
    def handle_endtag(self, tag):
        if tag=='p' and self.current is not None:
            self.paragraphs.append(''.join(self.current)); self.current=None

figures=list(csv.DictReader((R/'libro/figuras-capitulo-I.csv').open(encoding='utf8')))
def pdf_text(path):
    pages=[]
    for page in PdfReader(path).pages:
        lines=(page.extract_text() or '').splitlines()
        if lines and re.fullmatch(r'\s*(?:\d+|[ivxlcdm]+)\s*', lines[-1], re.I): lines.pop()
        pages.append('\n'.join(lines))
    text=norm('\n'.join(pages))
    check('Pies únicos y completos: '+path.name, all(text.count(norm(f['titulo']))==1 and text.count(norm(f['fuente']))==1 for f in figures))
    # Los flotantes pueden intercalarse entre dos páginas de un párrafo.
    # Se verifica primero el pie completo y luego se retira el bloque de figura
    # para comparar la secuencia continua de la prosa, sin texto del gráfico.
    for figure in figures:
        start=text.find(norm(figure['titulo']))
        source=norm(figure['fuente']); end=text.find(source,start)
        if start>=0 and end>=start: text=text[:start]+text[end+len(source):]
    return text

book = pdf_text(R/'entregas/pdf/PAPIME-libro-avance-B02.pdf')
chapter = pdf_text(R/'entregas/pdf/PAPIME-B02-capitulo-I.pdf')
for page, targets in [('index.html',[book]), ('territorio.html',[chapter,book]), ('especializacion.html',[book])]:
    paragraphs=Paragraphs((R/'entregas/web'/page).read_text(encoding='utf8')).paragraphs
    # Las expresiones LaTeX del piloto se comprueban arriba y en el navegador;
    # aquí se compara la prosa que admite extracción textual en ambos formatos.
    prose=[p.strip() for p in paragraphs if len(norm(p)) >= 50 and '\\(' not in p and '\\[' not in p and not p.strip().startswith(('Fuente:', 'Figura I.2.'))]
    missing=[p for p in prose if not all(norm(p) in target for target in targets)]
    check('Prosa web/PDF: '+page, not missing, dict(parrafos=len(prose), ausentes=missing))

report=dict(fecha='2026-11-06',base=args.base,resultado='correcto' if all(c['correcto'] for c in checks) else 'incidencias',pruebas=len(checks),comprobaciones=checks)
(R/'seguimiento/verificacion-revision-narrativa-B02.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=False))
raise SystemExit(0 if report['resultado']=='correcto' else 1)
