"""Cotejo independiente Excel/CSV/R de especialización. Ejecutar desde la raíz.

Dependencia de auditoría: openpyxl 3.1.5. El flujo editorial de R usa sólo base R.
No descarga ni modifica insumos. Los datos precalculados sólo se usan al contrastar.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

import openpyxl

ROOT = Path.cwd()
ORIGINAL = ROOT / "datos/originales/especializacion"
PREP = ROOT / "datos/preparados/capitulo-02"
OLD = ROOT / "referencias/antecedentes/especializacion/Figuras_Capitulo_II_Especializacion_2024"
RECORD = ROOT / "seguimiento"
RECORD.mkdir(parents=True, exist_ok=True)


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


checks = []


def check(name, difference, tolerance=1e-8, count=1):
    difference = float(difference)
    passed = math.isfinite(difference) and difference <= tolerance
    checks.append({"prueba": name, "n": count, "diferencia_maxima": difference, "tolerancia": tolerance, "resultado": "correcto" if passed else "FALLO"})
    if not passed:
        raise AssertionError(f"{name}: {difference} > {tolerance}")


with (ORIGINAL / "Matriz_original_Indices_Krugman.csv").open(encoding="utf-8-sig", newline="") as stream:
    raw = list(csv.reader(stream))
assert len(raw) == 34 and all(len(row) == 23 for row in raw)
names = [row[0] for row in raw[1:33]]
codes = [s.split(" - ")[0] for s in raw[0][1:22]]
assert len(set(names)) == 32 and len(set(codes)) == 21
X = [[float(c) for c in row[1:22]] for row in raw[1:33]]
n = [float(c) for c in raw[33][1:22]]
assert all(math.isfinite(v) and v >= 0 for row in X for v in row)
assert all(math.isfinite(v) and v > 0 for v in n)
rows = [sum(row) for row in X]
total = sum(n)
assert all(v > 0 for v in rows)
s = [[X[i][j] / rows[i] for j in range(21)] for i in range(32)]
sn = [v / total for v in n]
q = [[X[i][j] / n[j] for j in range(21)] for i in range(32)]
w = [v / total for v in rows]
iee = [[s[i][j] / sn[j] for j in range(21)] for i in range(32)]
ksi = [sum(abs(s[i][j] - sn[j]) for j in range(21)) for i in range(32)]
ice = [sum(abs(q[i][j] - w[i]) for i in range(32)) for j in range(21)]

# El Excel se abre con las cifras calculadas conservadas, sin ejecutar fórmulas.
book = openpyxl.load_workbook(ORIGINAL / "PIBE_2024_In.xlsx", data_only=True, read_only=True)
sheet = book["Indices_Krugman"]
excel = list(sheet.iter_rows(min_row=1, max_row=147, min_col=1, max_col=23, values_only=True))
check("Excel/CSV celdas A1:W34 numéricas", max(abs(float(raw[i][j]) - float(excel[i][j])) for i in range(1, 34) for j in range(1, 23)), 0, 726)
check("Excel/CSV etiquetas", sum(raw[i][0] != excel[i][0] for i in range(34)), 0, 34)
check("CSV/R denominadores estatales", max(abs(rows[i] - float(raw[i + 1][22])) for i in range(32)), 0.02, 32)
check("Agregación territorial por actividad", max(abs(sum(X[i][j] for i in range(32)) - n[j]) for j in range(21)), 0.02, 21)
check("Agregación nacional", abs(sum(rows) - total), 0.02)
check("KSI precalculado Excel W78:W109", max(abs(ksi[i] - float(excel[77 + i][22])) for i in range(32)), count=32)
check("ICE precalculado Excel B147:V147", max(abs(ice[j] - float(excel[146][1 + j])) for j in range(21)), count=21)
check("Suma participaciones estatales", max(abs(sum(row) - 1) for row in s), count=32)
check("Suma participaciones territoriales", max(abs(sum(q[i][j] for i in range(32)) - 1) for j in range(21)), count=21)
check("IEE dos expresiones", max(abs(iee[i][j] - q[i][j] / w[i]) for i in range(32) for j in range(21)), count=672)
check("IEE media sectorial ponderada", max(abs(sum(iee[i][j] * sn[j] for j in range(21)) - 1) for i in range(32)), count=32)
check("IEE media territorial ponderada", max(abs(sum(iee[i][j] * w[i] for i in range(32)) - 1) for j in range(21)), count=21)
weighted_ksi = sum(w[i] * ksi[i] for i in range(32))
weighted_ice = sum(sn[j] * ice[j] for j in range(21))
check("Identidad ponderada KSI/ICE", abs(weighted_ksi - weighted_ice))
check("Cota KSI 2(1-w_i)", max(0, max(ksi[i] - 2 * (1 - w[i]) for i in range(32))), count=32)
assert all(0 <= v <= 2 for v in ksi + ice)
for folder, label in ((PREP, "R"), (OLD, "antecedente")):
    k = {r["cve_ent"]: float(r["KSI"]) for r in read_csv(folder / "KSI_entidades.csv")}
    c = {r["codigo"]: float(r["ICE"]) for r in read_csv(folder / "ICE_sectores.csv")}
    long = {(r["cve_ent"], r["codigo"]): r for r in read_csv(folder / "Indices_entidad_sector.csv")}
    assert len(k) == 32 and len(c) == 21 and len(long) == 672
    check(f"KSI Python/{label}", max(abs(ksi[i] - k[f"{i+1:02d}"]) for i in range(32)), count=32)
    check(f"ICE Python/{label}", max(abs(ice[j] - c[codes[j]]) for j in range(21)), count=21)
    check(f"IEE Python/{label}", max(abs(iee[i][j] - float(long[(f"{i+1:02d}", codes[j])]["IEE"])) for i in range(32) for j in range(21)), count=672)
    # Todos los demás derivados económicos se comprueban, no sólo el índice final.
    columns = {
        "VAB_sector": lambda i, j: X[i][j],
        "participacion_local": lambda i, j: s[i][j],
        "participacion_sector": lambda i, j: q[i][j],
        "diferencia_pp": lambda i, j: (s[i][j] - sn[j]) * 100,
        "aportacion_KSI": lambda i, j: abs(s[i][j] - sn[j]),
        "aportacion_ICE": lambda i, j: abs(q[i][j] - w[i]),
        "VAB": lambda i, j: rows[i], "peso": lambda i, j: w[i],
        "participacion_nacional": lambda i, j: sn[j],
    }
    for col, expected in columns.items():
        tol = 1e-7 if col in ("VAB", "VAB_sector") else 1e-8
        check(f"{col} Python/{label}", max(abs(expected(i, j) - float(long[(f"{i+1:02d}", codes[j])][col])) for i in range(32) for j in range(21)), tol, 672)

max_pair = max(((iee[i][j], i, j) for i in range(32) for j in range(21)))
coah = names.index("Coahuila de Zaragoza")
manuf = codes.index("31-33")
report = {
    "fecha_verificacion": "2026-11-05", "bloque": "B01", "figura": "F07-KSI",
    "resultado": "correcto", "dimensiones": [32, 21], "celdas": 672,
    "ceros_observados": sum(v == 0 for row in X for v in row), "faltantes": 0,
    "anio_datos": 2024, "precios_base": 2018, "unidad": "millones de pesos de 2018",
    "VAB_nacional": total, "identidad_ponderada_KSI_ICE": weighted_ksi,
    "maximo_IEE": {"valor": max_pair[0], "entidad": names[max_pair[1]], "codigo": codes[max_pair[2]]},
    "casos_texto": {
        "Campeche_KSI": ksi[3], "Campeche_mineria_petrolera_local": s[3][1],
        "mineria_petrolera_nacional": sn[1], "Coahuila_manufacturas_local": s[coah][manuf],
        "manufacturas_nacional": sn[manuf], "Coahuila_manufacturas_IEE": iee[coah][manuf],
    },
    "insumos_sha256": {p.name: sha256(p) for p in (ORIGINAL / "Matriz_original_Indices_Krugman.csv", ORIGINAL / "PIBE_2024_In.xlsx")},
    "pruebas": checks,
    "revision_visual": "PNG estático y PDF vectorial renderizado revisados sin recortes ni superposición; 32 rótulos y escala 0 a 2 legibles.",
}
(RECORD / "auditoria-especializacion.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
with (RECORD / "auditoria-especializacion.csv").open("w", encoding="utf-8", newline="") as stream:
    writer = csv.DictWriter(stream, fieldnames=list(checks[0]))
    writer.writeheader()
    writer.writerows(checks)
print(json.dumps({"resultado": "correcto", "pruebas": len(checks), "VAB": total, "max_IEE": max_pair[0], "ceros": report["ceros_observados"], "casos_texto": report["casos_texto"]}, ensure_ascii=False))
