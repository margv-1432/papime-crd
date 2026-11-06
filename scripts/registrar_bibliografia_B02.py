"""Concilia los pasajes consultados de B02 con la matriz común, sin presumir lectura íntegra."""
import csv,re,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
bib=(R/'libro/bibliografia.bib').read_text(encoding='utf8')
entries={}
for match in re.finditer(r'@\w+\{([^,]+),\n(.*?)\n\}',bib,re.S):
    fields={k:v for k,v in re.findall(r'^  (\w+) = \{(.*?)\},?$',match[2],re.M)}
    entries[match[1]]=fields
cites=set(re.findall(r'@([A-Za-z][A-Za-z0-9_-]+)',(R/'libro/capitulos/01-territorio.Rmd').read_text(encoding='utf8')))
assert cites<=entries.keys()
pages={
 'bassols1992':'13–14;18–19;490 impresas (PDF14–15;19–20;491); portada y legal PDF4–5',
 'ruiz1997':'433–434 impresas (PDF216–217); índice y legal',
 'ruiz1999':'13–15 impresas (PDF7–8); índice y legal',
 'ruiz2019':'84;90–92 impresas',
 'geurs2004':'127–128 impresas (PDF1–2)',
 'gasca2014':'101;106–111 impresas (copia Redalyc con portada: PDF14;19–24)',
 'bray2003':'672–676 impresas (PDF1–5)',
 'aburto2008':'10456–10458; métodos y resultados en original PMC',
 'conagua2024':'16;23–28;69;143; tablas1.5.2 y2.2.2 p27; extracto directo p16/27',
 'sgm2024':'115 cuadro7.4;297 desglose Sonora cotejado directamente; Cananea382401.86t/Nacozari102596.09t',
 'conapesca2023':'109 cuadro2.1.5;133 cuadro2.3.3',
 'constitucion1824':'artículo5;facsimil PDF1',
 'constitucion1917original':'artículo27;facsímil DOF PDF2',
 'reformaCDMX2016':'artículos43 y44;DOF29-01-2016 vespertina',
 'tratado1848':'artículoV;transcripción y ficha del ejemplar de canje',
 'mesilla1853':'ficha y facsímil;firma30-12-1853;aprobación08-06-1854',
 'fao1993':'paso5 Evaluate land suitability;HTML sin folios',
 'escalante2004':'capítulo1;Los guerreros de Quetzalcóatl;HTML sin folios',
 'garcia2004':'capítulo2;El periodo de madurez y autonomía;HTML sin folios',
 'vazquez2004':'capítulo4;separaciones1823/1836 e integración nacional;HTML sin folios',
 'speckman2004':'capítulo5;apartado económico y ferrocarriles;HTML sin folios',
 'congresoBCS2017':'boletín institucional;conversión de BCS yQR1974',
 'inegi2001fisiografia':'fichaUPC702825267575;metadato ySHP de15provincias',
 'inegi2020iter':'CSV nacional;selección de145localidades ydocumentaciónITER',
 'inegi2008clima':'fichaUPC702825267568;DBF1695polígonos ymetadatos',
 'inegi2024suelos':'fichaUPC794551131916;DBF75491polígonos;diccionariofol18 yguía2011p5',
 'inegi2021usv':'fichaCONAFOR;servicioSEMARNATcapa2;183claves/11grupos',
 'semarnat2026madera':'XLSXhojasDatos/Metadatos/Diccionario/Comentarios;292filas2023'
}
uses={
 'bassols1992':'Formación histórica de regiones; diferencia entre región económica y agregación administrativa. Ejemplar: segunda edición revisada1983, primera reimpresión1992; no citarlo como primera1979. ISBN impreso inconsistente conchecksum, omitido delBibTeX.',
 'ruiz1997':'Organización territorial, heterogeneidad y capacidades; colaboración deFranciscoEscamilla explícita.',
 'ruiz1999':'Reorganización regional deañosnoventa, acuerdos yagentes; sin atribuirle toda síntesisambiental.',
 'ruiz2019':'Plataforma exportadora yencadenamientos; periodosdelartículo, sin diagnósticoactual.',
 'hanson1997':'Resultados generales de manufacturas, salarios ycostosdeacceso; ficha yresumen originales suficientes para paráfrasis acotada; sin atribuir páginas de texto inaccesible.',
 'hanson2003':'Diferencias salariales regionales yacceso comercio/inversión; resumen originalNBER; sin consultaíntegra.',
 'conagua2024':'Agua/población treceRHA; 461640hm³/año y129.35millones; F03/F05; corte2022, publicaciónmarzo2024.',
 'sgm2024':'Producción preliminar estatalde cobre2023; no confundir con reservas uocurrencias.',
 'conapesca2023':'Total sectorial yacuacultura enpeso vivo2023;31entidades; diferencia1t porredondeo.',
 'semarnat2026madera':'Volumen maderable2023; agregación de292filas elementales,32entidades; actualización21-09-2026.'
}
path=R/'seguimiento/MATRIZ_BIBLIOGRAFICA.csv'
with path.open(encoding='utf-8-sig',newline='') as f:
 reader=csv.DictReader(f);fields=reader.fieldnames;old=list(reader)
by={row['clave']:row for row in old}
rows=[]
for key in sorted(cites):
 e=entries[key];limited=key in ('hanson1997','hanson2003')
 row=dict.fromkeys(fields,'')
 row.update(clave=key,capitulos='I',funcion='Seminal y marco histórico' if key in ('bassols1992','ruiz1997','ruiz1999') else 'Fuente B02 verificada',autor=e.get('author','').replace('{','').replace('}',''),ano=e.get('year',''),titulo=e.get('title',''),edicion_objetivo=e.get('note',e.get('publisher',e.get('journal',''))),fuente_primaria=e.get('url',''),soporte_consultado='Ficha y resumen del productor/editor' if limited else 'Original o pasajes/archivos del productor indicados; consulta parcial explícita',estado_lectura='Resumen original verificado; texto íntegro pendiente' if limited else 'Pasajes y metadatos pertinentes cotejados; no se presume lectura íntegra',paginas_verificadas=pages.get(key,'Sin foliación; metadatos o resumen original'),argumento_o_uso_previsto=uses.get(key,'Argumento acotado del capítulo y relacionesF06; categorías/periodos conservados.'),siguiente_verificacion='Profundizar texto original si se incorporan resultados específicos' if limited else 'Ampliar lectura sólo para nuevas afirmaciones; conservar edición y corte',fecha_consulta='2026-11-05')
 rows.append(row);by[key]=row
# Conservar candidatas y pendientes iniciales, sin convertirlas en citas usadas.
by['bassols1979']['siguiente_verificacion']='La ficha1979 sirve PDFde segundaed1983/reimpresión1992; capítulo cita bassols1992. Ver página legal; ISBN no se corrige porconjetura.'
by['garcia2008']['siguiente_verificacion']='Repositorio conCAPTCHA ytienda403 enB02; no se cita como lectura sustantiva. Se utilizó capítulo originalGarcía2004 delCOLMEX parahistoria colonial.'
for dest,output in [(path,list(by.values())),(R/'seguimiento/MATRIZ_BIBLIOGRAFICA_B02.csv',rows)]:
 with dest.open('w',encoding='utf8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(output)
hashes=[]
for p in (R/'tmp/bibliografia').glob('*.pdf'):
 hashes.append(dict(archivo=p.name,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),distribuido=False))
(R/'seguimiento/B02-bibliografia-consultada.json').write_text(json.dumps(hashes,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(dict(citas_capitulo=len(cites),matriz_total=len(by),originales_locales=len(hashes))))
