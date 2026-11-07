"""Localiza las herramientas sin fijar la cuenta ni las rutas de una computadora."""
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

RAIZ = Path(__file__).resolve().parents[1]


def localizar(variable, comando, candidatos=()):
    elegido = os.environ.get(variable) or shutil.which(comando)
    if elegido and Path(elegido).is_file():
        return Path(elegido).resolve()
    for candidato in candidatos:
        if candidato.is_file():
            return candidato
    raise SystemExit(f"Instala {comando} o indica su ejecutable en {variable}.")


def entorno():
    env = os.environ.copy()
    program = Path(env.get("ProgramFiles", "C:/Program Files"))
    versiones = sorted((program / "R").glob("R-*/bin/Rscript.exe"), reverse=True)
    rscript = localizar("PAPIME_RSCRIPT", "Rscript", versiones)
    env["PAPIME_RSCRIPT"] = str(rscript)
    if os.name == "nt":
        version = re.search(r"R-(\d+\.\d+)\.", str(rscript))
        if version:
            biblioteca = Path.home() / "AppData/Local/R/win-library" / version[1]
            if biblioteca.is_dir():
                env.setdefault("PAPIME_R_LIBRARY", str(biblioteca))
        env.setdefault("QUARTO_R", str(rscript.parent))
    if env.get("PAPIME_R_LIBRARY"):
        env["R_LIBS_USER"] = env["PAPIME_R_LIBRARY"]
    env["PATH"] = os.pathsep.join((str(Path(sys.executable).parent), str(rscript.parent), env.get("PATH", "")))
    return env


def ejecutar(*args, env=None):
    subprocess.run([str(a) for a in args], cwd=RAIZ, env=env, check=True)
