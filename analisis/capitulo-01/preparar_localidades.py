"""Prepara la selección F01 desde ITER 2020 oficial, sin sumar agregados."""
from pathlib import Path
import csv, io, json, zipfile, hashlib

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "datos/preparados/capitulo-01"
OUT.mkdir(parents=True, exist_ok=True)
RAW = ROOT / "datos/originales/geografia/iter_00_cpv2020_csv.zip"
if not RAW.exists():
    RAW = ROOT / ".local/B02-originales/iter_00_cpv2020_csv.zip"
with zipfile.ZipFile(RAW) as z:
    name = next(n for n in z.namelist() if "/conjunto_de_datos/" in n and n.endswith(".csv"))
    rows = csv.DictReader(io.TextIOWrapper(z.open(name), encoding="utf-8-sig"))
    national = None
    selected = []
    def decimal(s):
        import re
        parts = re.findall(r"\d+(?:\.\d+)?", s)
        if len(parts) != 3:
            raise ValueError(f"Coordenada sin DMS: {s!r}")
        return float(parts[0]) + float(parts[1])/60 + float(parts[2])/3600
    for r in rows:
        if r["ENTIDAD"] == "00" and r["MUN"] == "000" and r["LOC"] == "0000":
            national = int(r["POBTOT"])
        if r["ENTIDAD"] == "00" or r["MUN"] == "000" or r["LOC"] in ("0000", "9998", "9999"):
            continue
        if not r["POBTOT"].isdigit() or int(r["POBTOT"]) < 100000:
            continue
        selected.append({"cveloc": r["ENTIDAD"]+r["MUN"]+r["LOC"], "cve_ent": r["ENTIDAD"],
                         "entidad": r["NOM_ENT"], "localidad": r["NOM_LOC"], "poblacion": int(r["POBTOT"]),
                         "longitud": -decimal(r["LONGITUD"]), "latitud": decimal(r["LATITUD"]),
                         "altitud_censal_m": r["ALTITUD"]})
assert national == 126014024
assert len(selected) == 145 and len({r["cveloc"] for r in selected}) == 145
assert all(-119 < r["longitud"] < -86 and 14 < r["latitud"] < 33 for r in selected)
selected.sort(key=lambda r: r["cveloc"])
with (OUT/"F01-localidades-2020.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=selected[0].keys()); w.writeheader(); w.writerows(selected)
meta = {"fuente": "INEGI, ITER Censo 2020", "url": "https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/iter/iter_00_cpv2020_csv.zip",
        "sha256_original": hashlib.sha256(RAW.read_bytes()).hexdigest(), "consulta": "2026-11-05", "localidades": len(selected),
        "poblacion_seleccion": sum(r["poblacion"] for r in selected), "poblacion_nacional": national,
        "porcentaje_poblacion": sum(r["poblacion"] for r in selected)/national*100,
        "seleccion": "ENTIDAD distinta 00; MUN distinto000; LOC distinta0000,9998,9999; POBTOT>=100000",
        "coordenadas": "DMS originales convertidas a grados decimales; longitud oeste negativa", "unidad": "localidad estadística; no ciudad funcional ni zona metropolitana"}
(OUT/"F01-localidades-metadatos.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(meta, ensure_ascii=False))
