"""Compila el manual web. Ejecutar: python scripts/compilar.py"""
import os
from pathlib import Path

from entorno import ejecutar, entorno, localizar


def main():
    env = entorno()
    program = Path(env.get("ProgramFiles", "C:/Program Files"))
    candidatos = (program / "Quarto/bin/quarto.exe", program / "RStudio/resources/app/bin/quarto/bin/quarto.exe")
    quarto = localizar("PAPIME_QUARTO", "quarto", candidatos if os.name == "nt" else ())
    ejecutar(quarto, "render", "--to", "html", env=env)


if __name__ == "__main__":
    main()
