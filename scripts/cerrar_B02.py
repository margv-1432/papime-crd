"""Consolida los registros de una entrega B02 comprobada, sin publicar automáticamente."""
import csv,json,hashlib,re,subprocess,zipfile
from pathlib import Path
R=Path(__file__).resolve().parents[1]
qa=json.loads((R/'seguimiento/verificacion-proyecto-B02.json').read_text(encoding='utf8'))
web=json.loads((R/'seguimiento/verificacion-web-B02.json').read_text(encoding='utf8'))
assert qa['resultado']==web['resultado']=='correcto'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
# Rótulos y rutas estables, sin tocar figuras de B03.
p=R/'seguimiento/registro-figuras.csv'
with p.open(encoding='utf-8-sig',newline='') as f:rr=csv.DictReader(f);fields=rr.fieldnames;rows=list(rr)
names=['F01-relieve-localizacion','F02-clima-suelos','F03-agua-renovable','F04-recursos','F05-agua-poblacion','F06-mecanismos-territoriales']
scripts=['generar_fisico.R','generar_fisico.R','preparar_agua_sintesis.py','preparar_F04.py','preparar_agua_sintesis.py','preparar_agua_sintesis.py']
for row in rows:
 if row['id_estable'] not in ['F01','F02','F03','F04','F05','F06']:continue
 i=int(row['id_estable'][-1])-1
 row.update(rotulo_editorial='I.2.'+str(i+1),datos_originales='Ver notas B02 por figura y manifiesto de originales',datos_preparados='datos/preparados/capitulo-01/',script='analisis/capitulo-01/'+scripts[i],html='assets/capitulo-01/interactivos/'+names[i]+'.html',estatica='assets/capitulo-01/figuras-estaticas/'+names[i]+'.pdf',estado='Completada, auditada e integrada B02',comprobacion_o_pendiente='Datos y lectura comprobados; límites y transformaciones en notas B02; F04 incluye cuatro paneles y valores faltantes explícitos')
with p.open('w',encoding='utf8',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
# Manifiesto común: sólo originales que acompañan al clon.
p=R/'datos/manifiesto.csv'
with p.open(encoding='utf-8-sig',newline='') as f:rr=csv.DictReader(f);fields=rr.fieldnames;old=[r for r in rr if not r['id'].startswith('B02-')]
inputs=sorted([p for folder in ['datos/originales/capitulo-01','datos/originales/geografia'] for p in (R/folder).rglob('*') if p.is_file() and p.stat().st_size<50_000_000])
for i,p in enumerate(inputs,1):
 row=dict.fromkeys(fields,'');row.update(id=f'B02-{i:03}',ruta=p.relative_to(R).as_posix(),procedencia='Fuente o extracto documentado B02; ver notas por figura',fuente_original='INEGI;CONAGUA;SEMARNAT;SGM;CONAPESCA según recurso',fecha_descarga_original='2026-11-05 recuperación B02',fecha_verificacion='2026-11-05',periodo='Conservado por producto; ver metadatos y registro de figuras',cobertura='México; unidades de cada figura',unidad='Ver fuente y diccionario específico',transformacion='Íntegro salvo extractos o transcripciones identificados expresamente',ceros='No se imputan',faltantes='Estados originales conservados',sha256=sha(p),bytes=p.stat().st_size,estado='Congelado B02');old.append(row)
with p.open('w',encoding='utf8',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(old)
prepared=[dict(ruta=p.relative_to(R).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted((R/'datos/preparados/capitulo-01').glob('*')) if p.is_file()]
with (R/'datos/preparados/capitulo-01/manifiesto-B02.csv').open('w',encoding='utf8',newline='') as f:w=csv.DictWriter(f,fieldnames=['ruta','bytes','sha256']);w.writeheader();w.writerows([x for x in prepared if not x['ruta'].endswith('manifiesto-B02.csv')])
chapter=qa['pdfs']['PAPIME-B02-capitulo-I.pdf'];book=qa['pdfs']['PAPIME-libro-avance-B02.pdf']
state=f'''# Estado del proyecto PAPIME

Corte del 5 de noviembre de 2026. **B02 completo y entregado para revisión del autor.** B01 fue revisado y su aceptación autorizó este bloque. El trabajo se mantuvo dentro del capítulo I. B03 no se ha iniciado.

El capítulo «Fundamentos históricos y geográficos del territorio mexicano» contiene evolución territorial, criterios explícitos de regionalización, desarrollo geográfico y seis actividades. Se integran F01–F06 con HTML autónomos, estáticas y tablas. La bibliografía del capítulo utiliza 30 claves; la matriz conserva 63 registros, con acceso y páginas realmente consultadas. Ruiz Durán1997/1999 y el ejemplar de Bassols1992 están cotejados; Hanson conserva el alcance de sus resúmenes originales y García2008 queda como candidata sin lectura atribuida.

## Entrega y comprobación

- Capítulo I: `entregas/pdf/PAPIME-B02-capitulo-I.pdf`, {chapter['paginas']} páginas, SHA256 `{chapter['sha256']}`.
- Libro integrado: `entregas/pdf/PAPIME-libro-avance-B02.pdf`, {book['paginas']} páginas. Conserva el piloto B01 del capítulo II identificado como fragmento, sin desarrollar B03.
- Web: `entregas/web/index.html`, cuatro páginas navegables, seis figuras del capítulo y el piloto anterior.
- Fuente editable: `libro/capitulos/01-territorio.Rmd`; pies y rótulos en `libro/figuras-capitulo-I.csv`.
- Integración: {qa['pruebas']}/{qa['pruebas']} comprobaciones correctas. Navegador: {len(web['pruebas'])}/{len(web['pruebas'])} correctas, escritorio y360px, sin erroresJavaScript ni recursos externos. Auditorías específicas conservadas: F01/F02 15 aritméticas y10 geométricas; agua/esquema23 pruebas de navegador; F04 22.

El PDF se revisó por páginas renderizadas; se corrigió la separación de rótulos y pies. La tabla de unidades se adapta a móvil. Las versiones del PDF en web y entrega son idénticas. La reproducción ordinaria funciona sin red con derivados congelados. Los originales grandes se conservan en `.local/B02-originales`, con URL/hash para recuperación; no se incorporan archivos superiores al límite de GitHub.

## Versionado y continuación

Publicación en el fork autorizado `margv-1432/papime-crd`. El resultado de la sincronización se consigna en `verificacion-publicacion-B02.json` y en la sesión B02; hasta que exista ese informe con ref comprobada, no debe presumirse sincronización remota. El cierre previo de B01 y sus checkpoints permanecen en la historia de Git.

No quedan tareas necesarias de contenido o funcionamiento dentro de B02. Corresponde revisar el capítulo entregado. Si el autor solicita ajustes, reanudar en `libro/capitulos/01-territorio.Rmd`, modificar el recurso afectado, compilar con `scripts/compilar.R todo` y repetir sus comprobaciones pertinentes. No comenzar B03 sin autorización que lo comprenda.

Las limitaciones declaradas permanecen explícitas: climatología histórica, generalización de dibujo, diferencia temporal RHA2022/2023, una discordancia de suelo separada y diferencia de redondeo acuícola de1t. No impiden las comparaciones realizadas y no se ocultan mediante imputaciones. La reconstrucción geoespacial completa requiere recuperar los originales grandes y dos capas antecedentes descritas en `REPRODUCIBILIDAD_B02.md`; el clon sí contiene todo lo necesario para compilar y generar las figuras.
'''
(R/'seguimiento/ESTADO.md').write_text(state,encoding='utf8')
v=f'''# Verificación B02

Corte del 5 de noviembre de 2026. Capítulo I completo y revisable. Los informes automáticos son `verificacion-proyecto-B02.json`, `verificacion-web-B02.json`, `auditoria-F01-F02.json`, `auditoria-geometria-F01-F02.json`, `auditoria-agua-sintesis.json` y `auditoria-F04.json`.

Integración {qa['pruebas']}/{qa['pruebas']} y navegador {len(web['pruebas'])}/{len(web['pruebas'])} correctos. El navegador comprobó navegación, búsqueda, 33 referencias únicas al final, seis figuras integradas, controles y teclado, descarga hídrica exacta, figuras autónomas, lectura de360px y ausencia de errores o solicitudes externas. Las pruebas individuales de agua y F04 amplían esos controles. Se conservaron los datos y el PDF del piloto B01.

Se renderizaron y revisaron las {chapter['paginas']} páginas del capítulo. Se comprobaron jerarquía, tabla de unidades, figuras, pies, folios y bibliografía. Los rótulos y fuentes acompañan sus figuras; F04 utiliza paneles estáticos separados con continuación explícita para conservar la lectura de32entidades en madera y31en pesca. No se encontraron recortes o caracteres ausentes. El libro integrado tiene {book['paginas']} páginas; las ecuaciones del piloto se comprobaron en navegador y su contenido previo se conserva.

El capítulo tiene SHA256 `{chapter['sha256']}`; el libro integrado `{book['sha256']}`. Las copias en la web coinciden con los PDF de entrega. Los límites metodológicos y las condiciones de acceso bibliográfico se registran en las notas de figuras, matriz y estado. La aprobación aquí consignada cubre las comparaciones efectivamente realizadas, sin extenderse a accesibilidad, aptitud, causalidad o futuros bloques.
'''
(R/'seguimiento/VERIFICACION_B02.md').write_text(v,encoding='utf8')
(R/'seguimiento/sesiones/2026-11-05-B02.md').open('a',encoding='utf8').write('\n## Cierre comprobado\n\nCapítulo, seis figuras, datos y fuentes guardados. Compilación web/PDF correcta. Informes globales aprobados; ver VERIFICACION_B02.md. La red RNC2025 completa tiene953717715bytes, SHA256f6cb5dcb5d52b29461146830edc6050ac7e0022ba7d81558995629547c96ed6e, y CRC correcto de los12miembros. Se retienen120863segmentos en7467cadenas de dibujo, sin omitir segmentos seleccionados. B02 no requiere continuación de contenido; queda revisión del autor y comprobación del guardado remoto en su informe específico.\n')
print(json.dumps(dict(capitulo_paginas=chapter['paginas'],libro_paginas=book['paginas'],pruebas_web=len(web['pruebas']),originales_versionados=len(inputs))))
