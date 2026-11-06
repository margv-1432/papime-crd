# Estado del proyecto PAPIME

## Destino permanente de publicación

Instrucción del autor reafirmada el 6 de noviembre de 2026: **todos los avances, archivos versionados, ramas y pull requests deben publicarse exclusivamente en el fork [margv-1432/papime-crd](https://github.com/margv-1432/papime-crd)**. El repositorio original `postsocratico/papime-crd` se conserva únicamente como referencia de consulta; no se debe escribir en él ni dirigirle pull requests. Esta regla continúa vigente al abrir otra conversación y al avanzar a los siguientes bloques.

En Git local, `origin` apunta al fork y `upstream` al original de consulta. En el conector GitHub, indicar siempre `repository_full_name: margv-1432/papime-crd` y comprobar que la base y la rama de cada PR pertenezcan a ese fork. B02 ya está allí, en `b02-capitulo-i`, [PR #1 del propio fork](https://github.com/margv-1432/papime-crd/pull/1).

La restricción documentada para actualizar `main` se refiere a **la rama `main` del fork**, no al repositorio original. No cambia el destino de publicación.

## Avance del libro

Corte del 5 de noviembre de 2026. **B02 completo y entregado para revisión del autor.** B01 fue revisado y su aceptación autorizó este bloque. El trabajo se mantuvo dentro del capítulo I. B03 no se ha iniciado.

El capítulo «Fundamentos históricos y geográficos del territorio mexicano» contiene evolución territorial, criterios explícitos de regionalización, desarrollo geográfico y seis actividades. Se integran F01–F06 con HTML autónomos, estáticas y tablas. La bibliografía del capítulo utiliza 30 claves; la matriz conserva 63 registros, con acceso y páginas realmente consultadas. Ruiz Durán (1997 y 1999) y el ejemplar de Bassols (1992) están cotejados; Hanson conserva el alcance de sus resúmenes originales y García Martínez (2008) queda como candidata sin lectura atribuida.

## Entrega y comprobación

- Capítulo I: `entregas/pdf/PAPIME-B02-capitulo-I.pdf`, 24 páginas, SHA256 `2f746a4d136e427fb7c4cdb286aa9ff4a32d8d542889b2f632d7f8d66f207e55`.
- Libro integrado: `entregas/pdf/PAPIME-libro-avance-B02.pdf`, 31 páginas. Conserva el piloto B01 del capítulo II identificado como fragmento, sin desarrollar B03.
- Web: `entregas/web/index.html`, cuatro páginas navegables, seis figuras del capítulo y el piloto anterior.
- Fuente editable: `libro/capitulos/01-territorio.Rmd`; pies y rótulos en `libro/figuras-capitulo-I.csv`.
- Integración: 40/40 comprobaciones correctas. Navegador: 39/39 correctas, escritorio y 360 px, sin errores JavaScript ni recursos externos. Auditorías específicas conservadas: F01/F02 15 aritméticas y10 geométricas; agua/esquema23 pruebas de navegador; F04 22.

El PDF se revisó por páginas renderizadas; se corrigió la separación de rótulos y pies. La tabla de unidades se adapta a móvil. Las versiones del PDF en web y entrega son idénticas. La reproducción ordinaria funciona sin red con derivados congelados. Los originales grandes se conservan en `.local/B02-originales`, con URL/hash para recuperación; no se incorporan archivos superiores al límite de GitHub.

## Versionado y continuación

Publicación completa en la rama [b02-capitulo-i](https://github.com/margv-1432/papime-crd/tree/b02-capitulo-i), [PR #1 en borrador](https://github.com/margv-1432/papime-crd/pull/1). El commit de contenido es dc9779a594eaaa44f1a0ff9473f63e6bad62c724. Se verificaron 152 blobs y la identidad del árbol Git completo con el checkpoint local dd858f5. El comprobante es verificacion-publicacion-B02.json. No hay archivos pendientes de publicar.

La revisión automática rechazó actualizar la rama predeterminada main por requerir autorización específica. La alternativa de rama y PR conserva la entrega revisable en el repositorio; main remoto sigue en B01. La integración del PR requiere la revisión y autorización del autor. Los checkpoints locales no se borran ni reescriben; su historia puede diferir de los commits creados mediante el conector, con árboles de contenido idénticos.

No quedan tareas necesarias de contenido o funcionamiento dentro de B02. Corresponde revisar el capítulo entregado. Si el autor solicita ajustes, reanudar en `libro/capitulos/01-territorio.Rmd`, modificar el recurso afectado, compilar con `scripts/compilar.R todo` y repetir sus comprobaciones pertinentes. No comenzar B03 sin autorización que lo comprenda.

Las limitaciones declaradas permanecen explícitas: climatología histórica, generalización de dibujo, diferencia temporal RHA2022/2023, una discordancia de suelo separada y diferencia de redondeo acuícola de 1 t. No impiden las comparaciones realizadas y no se ocultan mediante imputaciones. La reconstrucción geoespacial completa requiere recuperar los originales grandes y dos capas antecedentes descritas en `REPRODUCIBILIDAD_B02.md`; el clon sí contiene todo lo necesario para compilar y generar las figuras.
