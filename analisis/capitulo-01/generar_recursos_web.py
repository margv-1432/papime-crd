"""Genera F04 web autónoma a partir de los derivados congelados de B02.

No descarga fuentes, recalcula agregados ni produce figuras estáticas.
La geometría de entidades procede de generar_fisico_web.R --geometria.
"""
from pathlib import Path
import base64, csv, hashlib, json

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PREP = ROOT / 'datos/preparados/capitulo-01'
OUT = ROOT / 'assets/capitulo-01/interactivos/F04-recursos.html'
FILES = {
    'cobre': 'F04_A_cobre_2023.csv',
    'madera': 'F04_B_madera_2023.csv',
    'pesca': 'F04_C_pesca_acuacultura_2023.csv',
    'cubierta': 'F04_correspondencia_vegetacion.csv',
}

def main():
    tables = {}
    hashes = {}
    for panel, filename in FILES.items():
        path = PREP / filename
        with path.open(encoding='utf-8-sig', newline='') as stream:
            reader = csv.DictReader(stream)
            tables[panel] = {'fields': reader.fieldnames, 'rows': list(reader), 'archivo': filename}
        hashes[filename] = hashlib.sha256(path.read_bytes()).hexdigest()
    assert all(len(tables[p]['rows']) == 32 for p in ('cobre', 'madera', 'pesca'))
    assert len(tables['cubierta']['rows']) == 183
    states = json.loads((PREP / 'estados-web.json').read_text(encoding='utf8'))
    assert len(states['estados']) == 32
    assert {s['cve_ent'] for s in states['estados']} == {f'{n:02}' for n in range(1, 33)}
    payload = {'tables': tables, 'geometry': states, 'hashes': hashes}
    document = (HERE / 'recursos_web.html').read_text(encoding='utf8')
    replacements = {
        '__STYLE__': (HERE / 'recursos_web.css').read_text(encoding='utf8'),
        '__SCRIPT__': (HERE / 'recursos_web.js').read_text(encoding='utf8'),
        '__PAYLOAD__': json.dumps(payload, ensure_ascii=False, allow_nan=False).replace('<', '\\u003c'),
        '__COVER__': base64.b64encode((PREP / 'F04_cubierta_recortada.png').read_bytes()).decode('ascii'),
    }
    for token, value in replacements.items():
        document = document.replace(token, value)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(document, encoding='utf8')
    print(json.dumps({'figura': 'F04', 'html': str(OUT.relative_to(ROOT)), 'bytes': OUT.stat().st_size,
                      'entidades': 32, 'claves_cubierta': 183, 'fuentes_sha256': hashes}, ensure_ascii=False))

if __name__ == '__main__':
    main()
