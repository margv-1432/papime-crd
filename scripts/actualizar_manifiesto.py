"""Registra los insumos y derivados efectivamente empleados por el piloto, sin descargarlos."""
import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
files = [
    ("D01", "datos/originales/especializacion/PIBE_2024_In.xlsx", "Original recibido; INEGI PIBE, hoja Indices_Krugman A1:W34", "ninguna; original íntegro"),
    ("D02", "datos/originales/especializacion/Matriz_original_Indices_Krugman.csv", "Transcripción conservada del Excel recibido", "extracción antecedente; contrastada celda por celda en B01"),
    ("D03", "datos/preparados/capitulo-02/KSI_entidades.csv", "D02; preparar_especializacion.R", "suma absoluta de brechas de participaciones; sin factor 1/2"),
    ("D04", "datos/preparados/capitulo-02/ICE_sectores.csv", "D02; preparar_especializacion.R", "distancia territorial respecto del peso económico; sin factor 1/2"),
    ("D05", "datos/preparados/capitulo-02/Indices_entidad_sector.csv", "D02; preparar_especializacion.R", "participaciones, cociente de localización y contribuciones; 672 filas"),
    ("D06", "datos/preparados/capitulo-02/Matriz_IEE.csv", "D05", "matriz completa de cocientes 32 por 21"),
    ("D07", "datos/preparados/capitulo-02/Sensibilidad_agregacion_minera.csv", "D02; preparar_especializacion.R", "agregar minería sin excluir actividad; comparar 21 actividades con 20 sectores"),
    ("D08", "datos/preparados/capitulo-02/Catalogo_sectores.csv", "Encabezados D02 y clasificación del antecedente", "rótulos didácticos con correspondencia a códigos originales"),
]
rows = []
for identifier, relative, origin, transformation in files:
    data = (ROOT / relative).read_bytes()
    rows.append(dict(id=identifier, ruta=relative, procedencia=origin,
        fuente_original="INEGI Sistema de Cuentas Nacionales de México PIBE base 2018",
        url="https://www.inegi.org.mx/programas/pibent/2018/",
        fecha_descarga_original="No documentada", fecha_verificacion="2026-11-05",
        periodo="2024", cobertura="32 entidades; 21 actividades; minería petrolera y no petrolera separadas",
        unidad="D01-D02 VAB en millones de pesos de 2018; índices y participaciones adimensionales; ver diccionario",
        precios="Constantes de 2018", transformacion=transformation,
        ceros="36 ceros observados en matriz original, conservados", faltantes="0; el cálculo se detiene si aparecen",
        sha256=hashlib.sha256(data).hexdigest(), bytes=len(data), estado="Congelado B01; sin descarga de series nuevas"))
with (ROOT / "datos/manifiesto.csv").open("w", encoding="utf-8", newline="") as out:
    writer = csv.DictWriter(out, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
print(f"Manifiesto actualizado: {len(rows)} archivos")
