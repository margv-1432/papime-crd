"""Paquete revisable con los archivos añadidos o modificados durante B01."""
import hashlib
import json
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "458257c3d7b69602560cbcaeb89fd0980297ad6b"
git = lambda *args: subprocess.check_output(["git", "-c", "core.quotepath=false", *args], cwd=ROOT).decode("utf-8").strip()
version = git("rev-parse", "HEAD")
files = git("diff", "--name-only", BASE, "HEAD").splitlines()
dest = ROOT / "entregas/PAPIME-B01-revision.zip"
opening = f"""PAPIME B01 entrega para revisión
Versión local {version}

Abra entregas/pdf/PAPIME-B01-piloto.pdf para leer e imprimir.
Abra entregas/web/index.html para navegar por el piloto.
Conserve completa la carpeta web, con libs, estilos y recursos.
La búsqueda requiere un servidor local; instrucciones en README.md.
El gráfico individual funciona también al abrir
assets/capitulo-02/interactivos/F07-ksi.html sin conexión.

Este paquete reúne salidas, fuentes editables, plantillas, datos del piloto,
antecedentes de especialización y registros de B01. No incluye las carpetas
históricas del repositorio base que no intervienen en el piloto ni la
biblioteca local de programas.

El estado y la continuación están en seguimiento/ESTADO.md.
La sincronización con GitHub está pendiente de acceso de escritura.
El capítulo I no se ha comenzado.
"""
with zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as out:
    out.writestr("ABRIR.txt", opening.encode("utf-8"))
    for relative in files:
        source = ROOT / relative
        if source.is_file():
            out.write(source, relative)
with zipfile.ZipFile(dest) as check:
    assert check.testzip() is None
    names = set(check.namelist())
    assert {"entregas/web/index.html", "entregas/pdf/PAPIME-B01-piloto.pdf", "libro/index.Rmd", "seguimiento/ESTADO.md"} <= names
print(json.dumps(dict(archivo=str(dest), version=version, archivos=len(names), bytes=dest.stat().st_size,
                      sha256=hashlib.sha256(dest.read_bytes()).hexdigest()), ensure_ascii=False))
