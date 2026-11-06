# Estado del proyecto PAPIME

Corte del 5 de noviembre de 2026. **B02 completo y entregado para revisión del autor.** B01 fue revisado y su aceptación autorizó este bloque. El trabajo se mantuvo dentro del capítulo I. B03 no se ha iniciado.

El capítulo «Fundamentos históricos y geográficos del territorio mexicano» contiene evolución territorial, criterios explícitos de regionalización, desarrollo geográfico y seis actividades. Se integran F01–F06 con HTML autónomos, estáticas y tablas. La bibliografía del capítulo utiliza 30 claves; la matriz conserva 63 registros, con acceso y páginas realmente consultadas. Ruiz Durán1997/1999 y el ejemplar de Bassols1992 están cotejados; Hanson conserva el alcance de sus resúmenes originales y García2008 queda como candidata sin lectura atribuida.

## Entrega y comprobación

- Capítulo I: `entregas/pdf/PAPIME-B02-capitulo-I.pdf`, 24 páginas, SHA256 `2f746a4d136e427fb7c4cdb286aa9ff4a32d8d542889b2f632d7f8d66f207e55`.
- Libro integrado: `entregas/pdf/PAPIME-libro-avance-B02.pdf`, 31 páginas. Conserva el piloto B01 del capítulo II identificado como fragmento, sin desarrollar B03.
- Web: `entregas/web/index.html`, cuatro páginas navegables, seis figuras del capítulo y el piloto anterior.
- Fuente editable: `libro/capitulos/01-territorio.Rmd`; pies y rótulos en `libro/figuras-capitulo-I.csv`.
- Integración: 40/40 comprobaciones correctas. Navegador: 39/39 correctas, escritorio y360px, sin erroresJavaScript ni recursos externos. Auditorías específicas conservadas: F01/F02 15 aritméticas y10 geométricas; agua/esquema23 pruebas de navegador; F04 22.

El PDF se revisó por páginas renderizadas; se corrigió la separación de rótulos y pies. La tabla de unidades se adapta a móvil. Las versiones del PDF en web y entrega son idénticas. La reproducción ordinaria funciona sin red con derivados congelados. Los originales grandes se conservan en `.local/B02-originales`, con URL/hash para recuperación; no se incorporan archivos superiores al límite de GitHub.

## Versionado y continuación

Publicación en el fork autorizado `margv-1432/papime-crd`. El resultado de la sincronización se consigna en `verificacion-publicacion-B02.json` y en la sesión B02; hasta que exista ese informe con ref comprobada, no debe presumirse sincronización remota. El cierre previo de B01 y sus checkpoints permanecen en la historia de Git.

No quedan tareas necesarias de contenido o funcionamiento dentro de B02. Corresponde revisar el capítulo entregado. Si el autor solicita ajustes, reanudar en `libro/capitulos/01-territorio.Rmd`, modificar el recurso afectado, compilar con `scripts/compilar.R todo` y repetir sus comprobaciones pertinentes. No comenzar B03 sin autorización que lo comprenda.

Las limitaciones declaradas permanecen explícitas: climatología histórica, generalización de dibujo, diferencia temporal RHA2022/2023, una discordancia de suelo separada y diferencia de redondeo acuícola de1t. No impiden las comparaciones realizadas y no se ocultan mediante imputaciones. La reconstrucción geoespacial completa requiere recuperar los originales grandes y dos capas antecedentes descritas en `REPRODUCIBILIDAD_B02.md`; el clon sí contiene todo lo necesario para compilar y generar las figuras.
