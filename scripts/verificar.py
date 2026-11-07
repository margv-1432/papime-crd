"""Comprueba el libro compilado y la ubicación única de sus bases."""
import csv
import hashlib
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from entorno import RAIZ


class Documento(HTMLParser):
    def __init__(self, archivo):
        super().__init__()
        self.ids = set()
        self.rutas = []
        self.marcos = []
        self.feed(archivo.read_text(encoding="utf-8"))

    def handle_starttag(self, etiqueta, atributos):
        attrs = dict(atributos)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        for atributo in ("src", "href"):
            if attrs.get(atributo):
                self.rutas.append(attrs[atributo])
        if etiqueta == "iframe":
            self.marcos.append(attrs.get("src", ""))


def comprobar():
    web = RAIZ / "web"
    paginas = [web / "index.html", *sorted((web / "capitulos").glob("*.html"))]
    assert len(paginas) >= 4, "Falta compilar el libro."
    documentos = {p.resolve(): Documento(p) for p in paginas}
    enlaces = 0
    for pagina, doc in documentos.items():
        for enlace in doc.rutas:
            partes = urlsplit(enlace)
            if partes.scheme or partes.netloc:
                continue
            nombre = unquote(partes.path)
            destino = (pagina.parent / nombre).resolve() if nombre else pagina
            assert destino.is_relative_to(web), (pagina, enlace)
            assert destino.exists(), (pagina.name, enlace, "no existe")
            if partes.fragment and destino in documentos:
                assert unquote(partes.fragment) in documentos[destino].ids, (pagina.name, enlace, "ancla ausente")
            enlaces += 1
        for marco in doc.marcos:
            destino = (pagina.parent / unquote(urlsplit(marco).path)).resolve()
            fuente = RAIZ / destino.relative_to(web)
            assert fuente.read_bytes() == destino.read_bytes(), (marco, "HTML distinto del widget versionado")
    total_figuras = sum(len(doc.marcos) for doc in documentos.values())
    assert total_figuras >= 7, "Faltan figuras de los capítulos ya migrados."
    assert not list(web.rglob("*.pdf")), "Se copiaron PDF a la web."
    assert not any("actividades-finales" in doc.ids or "actividades" in doc.ids for doc in documentos.values())
    datos = RAIZ / "datos"
    with (datos / "uso-global.csv").open(encoding="utf-8", newline="") as stream:
        comunes = list(csv.DictReader(stream))
    registrados = {fila["archivo"] for fila in comunes}
    assert registrados == {p.relative_to(datos).as_posix() for p in (datos / "globales").rglob("*") if p.is_file()}
    for fila in comunes:
        caps = set(fila["capitulos"].split(";"))
        assert len(caps) > 1, (fila, "La base global requiere varios consumidores")
        scripts = [RAIZ / ruta for ruta in fila["generadores"].split(";")]
        assert {p.parent.name.removeprefix("capitulo-") for p in scripts} == caps
        nombre = Path(fila["archivo"]).name
        for script in scripts:
            codigo = script.read_text(encoding="utf-8")
            assert nombre in codigo and "globales" in codigo, (script, fila["archivo"])
    huellas = {}
    with (datos / "manifiesto.csv").open(encoding="utf-8", newline="") as stream:
        for fila in csv.DictReader(stream):
            p = RAIZ / fila["ruta"]
            assert p.is_file(), p
            digest = hashlib.sha256(p.read_bytes()).hexdigest()
            assert digest == fila["sha256"], (p, "cambió; documentar y comprobar los consumidores")
            assert digest not in huellas, (p, huellas.get(digest), "base duplicada")
            huellas[digest] = p
    bases = {p for carpeta in datos.iterdir() if carpeta.is_dir() for p in carpeta.rglob("*") if p.is_file()}
    assert bases == set(huellas.values()), "Hay bases no documentadas en el manifiesto."
    print(f"Web comprobada: {len(documentos)} páginas, {total_figuras} figuras, {enlaces} enlaces locales y {len(bases)} bases únicas.")


if __name__ == "__main__":
    comprobar()
