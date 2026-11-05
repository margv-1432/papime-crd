"""Comprobaciones de integridad, referencias y salidas del piloto B01."""
import csv
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "entregas/web"
checks = []

def check(name, condition, detail=""):
    checks.append(dict(prueba=name, correcto=bool(condition), detalle=detail))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

for source, copy in [
    (ROOT.parent / "PAPIME Libro.pdf", ROOT / "referencias/manuscrito-base/PAPIME Libro.pdf"),
    (ROOT.parent / "Medicion_de_la_Especializacion (1).docx", ROOT / "referencias/manuscrito-base/Medicion_de_la_Especializacion-variante-rectora.docx"),
    (ROOT.parent / "PAPIME_Mx/datos/PIBE_2024_In.xlsx", ROOT / "datos/originales/especializacion/PIBE_2024_In.xlsx"),
    (ROOT.parent / "PAPIME_Mx/datos/Matriz_original_Indices_Krugman.csv", ROOT / "datos/originales/especializacion/Matriz_original_Indices_Krugman.csv"),
]:
    # Los originales externos pueden no acompañar una clonación del repositorio.
    if source.exists():
        check("Original intacto " + copy.name, sha(source) == sha(copy))

manifest = list(csv.DictReader((ROOT / "datos/manifiesto.csv").open(encoding="utf-8")))
for row in manifest:
    check("Hash de " + row["id"], sha(ROOT / row["ruta"]) == row["sha256"])

class HTML(HTMLParser):
    def __init__(self, data):
        super().__init__()
        self.ids, self.links = set(), []
        self.feed(data)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        for key in ("href", "src"):
            if key in attrs:
                self.links.append((tag, key, attrs[key]))

pages = {p: HTML(p.read_text(encoding="utf-8")) for p in WEB.glob("*.html")}
broken, count, remote_assets = [], 0, []
for path, page in pages.items():
    for tag, key, value in page.links:
        url = urlsplit(value)
        if url.scheme or url.netloc:
            if key == "src" and url.scheme in ("https", "http"):
                remote_assets.append(value)
            continue
        target = (path.parent / unquote(url.path)).resolve() if url.path else path
        if target.is_dir():
            target /= "index.html"
        count += 1
        if not target.exists():
            broken.append(str(target))
        elif url.fragment and target.suffix == ".html":
            parsed = pages.get(target) or HTML(target.read_text(encoding="utf-8"))
            if unquote(url.fragment) not in parsed.ids:
                broken.append(str(target) + "#" + url.fragment)
check("Enlaces y recursos locales", not broken, {"comprobados":count,"rotos":broken})
check("Sin scripts externos", not remote_assets, remote_assets)

bib = (ROOT / "libro/bibliografia.bib").read_text(encoding="utf-8")
keys = re.findall(r"@\w+\{([^,]+),", bib)
check("Claves bibliográficas únicas", len(keys) == len(set(keys)) == 32)
cites = set()
for name in ("index.Rmd", "capitulos/02-piloto-especializacion.Rmd"):
    cites.update(re.findall(r"@([A-Za-z][A-Za-z0-9_-]+)", (ROOT / "libro" / name).read_text(encoding="utf-8")))
check("Citas resueltas", cites <= set(keys), sorted(cites))
specialization = (WEB / "especializacion.html").read_text(encoding="utf-8")
references = (WEB / "referencias.html").read_text(encoding="utf-8")
check("Bibliografía única en página final", 'class="csl-entry"' not in specialization and references.count('class="csl-entry"') == 3)

pdf = ROOT / "entregas/pdf/PAPIME-B01-piloto.pdf"
reader = PdfReader(pdf)
text = "\n".join(page.extract_text() or "" for page in reader.pages)
check("PDF de nueve páginas sin blancos", len(reader.pages) == 9 and all((p.extract_text() or "").strip() for p in reader.pages))
check("Cinco rótulos de ecuación", all(f"II.2.{i}" in text for i in range(1,6)))
check("Cifras del piloto en PDF", all(v in text for v in ("23,982,097.474", "1.352", "0.919", "2.156")))
check("Mismo PDF en web y entrega", sha(pdf) == sha(WEB / "papime-piloto.pdf"))
check("Mismo HTML autónomo en libro", sha(ROOT / "assets/capitulo-02/interactivos/F07-ksi.html") == sha(WEB / "recursos/F07-ksi.html"))

report = dict(fecha="2026-11-05", resultado="correcto" if all(c["correcto"] for c in checks) else "revisar",
              pruebas=len(checks), pdf_sha256=sha(pdf), comprobaciones=checks)
(ROOT / "seguimiento/verificacion-proyecto.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"resultado":report["resultado"],"pruebas":len(checks),"fallos":[c for c in checks if not c["correcto"]]}, ensure_ascii=False))
if report["resultado"] != "correcto":
    raise SystemExit(1)
