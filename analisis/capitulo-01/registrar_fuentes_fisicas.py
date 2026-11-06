from pathlib import Path
import csv,hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[2]
sources=[
('F01-elevacion','CEM_V3_20170619_R120_Nacional.zip','https://www.inegi.org.mx/app/geo2/elevacionesmex/DownloadFile.do?file=CEM_V3_20170619_R120_Nacional.zip&res=120&entidad=Nacional','CEM3.0;distribución120m;archivo20170619','metros de elevación;territorio continental'),
('F01-localidades','iter_00_cpv2020_csv.zip','https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/iter/iter_00_cpv2020_csv.zip','Censo2020;ITER nacional','personas;localidad estadística'),
('F01-caminos','794551163030_gpk.zip','https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/geografia/caminos/2025/794551163030_gpk.zip','RNC2025;GeoPackage nacional','geometría y atributos de red vial'),
('F02-clima','702825267568_s.zip','https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/geografia/tematicas/CLIMAS/702825267568_s.zip','Unidades climáticas;edición2008;base histórica','clases nominales;escala1:1000000'),
('F02-suelo','794551131916_s.zip','https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/geografia/tematicas/Edafologia_hist/1_250_000/serie%20II/794551131916_s.zip','SerieII;observación2002-2006;edición2024','clases nominales;escala1:250000'),
]
rows=[]
for id,name,url,period,unit in sources:
    paths=[ROOT/'.local/B02-originales'/name,ROOT/'datos/originales/geografia'/name]
    p=next((p for p in paths if p.exists()),None)
    if p is None:raise FileNotFoundError(name)
    with zipfile.ZipFile(p) as z:
        bad=z.testzip()
        if bad is not None:raise ValueError(f'CRC inválido: {bad}')
    sha=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):sha.update(b)
    rows.append(dict(id=id,archivo=name,fuente='INEGI',url=url,periodo_edicion=period,unidad_cobertura=unit,consulta='2026-11-05',bytes=p.stat().st_size,sha256=sha.hexdigest(),conservacion_local=p.relative_to(ROOT).as_posix(),integridad_zip='CRC correcto de todos los miembros'))
out=ROOT/'datos/originales/geografia/fuentes-F01-F02.csv'
with out.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
print(json.dumps(rows,ensure_ascii=False))
