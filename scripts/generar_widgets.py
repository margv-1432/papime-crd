"""Regenera las figuras del libro desde datos locales. Quarto lo ejecuta antes de renderizar."""
import hashlib
import json
from pathlib import Path
import sys

from entorno import RAIZ, ejecutar, entorno

GENERADORES = (
    ("capitulo-01", "generar_fisico_web.R", ("F01-relieve-localizacion.html", "F02-clima-suelos.html")),
    ("capitulo-01", "generar_agua_mecanismos_web.py", ("F03-agua-renovable.html", "F05-agua-poblacion.html", "F06-mecanismos-territoriales.html")),
    ("capitulo-01", "generar_recursos_web.py", ("F04-recursos.html",)),
    ("capitulo-02", "generar_interactivo.R", ("F07-ksi.html",)),
)
CACHE = RAIZ / ".quarto" / "papime-widgets.json"


def firma(archivos):
    clave = hashlib.sha256()
    for archivo in sorted(set(archivos)):
        clave.update(archivo.relative_to(RAIZ).as_posix().encode())
        clave.update(hashlib.sha256(archivo.read_bytes()).digest())
    return clave.hexdigest()


def main():
    env = entorno()
    previo = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.is_file() else {}
    estado = {}
    for capitulo, nombre, salidas in GENERADORES:
        carpeta = RAIZ / "plots" / capitulo
        script = carpeta / nombre
        productos = [carpeta / salida for salida in salidas]
        entradas = [script, Path(__file__).resolve()]
        for directorio in (RAIZ / "datos" / capitulo, RAIZ / "datos/globales", RAIZ / "estilos/widgets", carpeta / "plantillas"):
            entradas.extend(p for p in directorio.rglob("*") if p.is_file())
        actual = firma(entradas)
        huella = lambda: firma(productos) if all(p.is_file() for p in productos) else None
        if "--forzar" in sys.argv or previo.get(nombre) != [actual, huella()] or not huella():
            if script.suffix == ".R":
                ejecutar(env["PAPIME_RSCRIPT"], "--vanilla", script, env=env)
            else:
                ejecutar(sys.executable, script, env=env)
        salida = huella()
        if not salida:
            raise SystemExit(f"{nombre} no produjo todos sus HTML.")
        estado[nombre] = [actual, salida]
    CACHE.parent.mkdir(exist_ok=True)
    CACHE.write_text(json.dumps(estado, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
