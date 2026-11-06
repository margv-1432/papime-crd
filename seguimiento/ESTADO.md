# Estado del proyecto PAPIME

## Destino permanente de publicación

Instrucción del autor reafirmada el 6 de noviembre de 2026: **todos los avances, archivos versionados, ramas y pull requests se publican exclusivamente en el fork [margv-1432/papime-crd](https://github.com/margv-1432/papime-crd)**. El original `postsocratico/papime-crd` es únicamente de consulta y no recibe cambios ni pull requests. Esta regla continúa vigente en las siguientes conversaciones y bloques.

`origin` apunta al fork y `upstream` al original. En el conector GitHub se indica siempre `repository_full_name: margv-1432/papime-crd`. B02 se entrega en [b02-capitulo-i](https://github.com/margv-1432/papime-crd/tree/b02-capitulo-i), [PR #1 del propio fork](https://github.com/margv-1432/papime-crd/pull/1). Main remoto conserva B01; la restricción de actualización documentada corresponde a main del fork. La revisión actual continúa en la rama B02.

## Avance vigente

Corte del 6 de noviembre de 2026. **B02 completo, con revisión narrativa aplicada y listo para nueva lectura del autor.** B01 fue aceptado y autorizó este bloque; B03 no se ha iniciado. La corrección transversal alcanza el capítulo I, F01–F06, actividades, presentación y estilo del fragmento II.2 ya integrado, sin añadir contenido de B03.

**Prioridad editorial absoluta para continuar:** narrativa natural, continua y variada, propia de un manual interactivo. Se revisan argumentos completos y sus transiciones, evitando la sucesión de frases breves, las fórmulas genéricas de objeto y función, las precisiones negativas ajenas al asunto y las plantillas repetidas de párrafo. Aplicar `GUIA_EDITORIAL.md`, el plan y D23–D24 también a los siguientes capítulos y a las explicaciones de los recursos. La revisión técnica complementa la lectura editorial del conjunto.

El capítulo conserva evolución territorial, unidades de regionalización, desarrollo geográfico, seis actividades y seis figuras con HTML autónomos, estáticas y tablas. Se mantienen 30 claves citadas y 63 registros de matriz bibliográfica. Ruiz Durán (1997 y 1999) y Bassols (1992) permanecen cotejados; Hanson conserva el alcance de los resúmenes originales y García Martínez (2008) sigue como candidata sin lectura atribuida. Se preservan el manuscrito rector, literatura seminal y acuerdos previos.

## Entrega y comprobación

- Capítulo I: `entregas/pdf/PAPIME-B02-capitulo-I.pdf`, 23 páginas, SHA256 `660ed0e6650d854d1e3cf7960b988a0a0626e7f69d007bee0d4bdaf6c2e3247d`.
- Libro integrado: `entregas/pdf/PAPIME-libro-avance-B02.pdf`, 30 páginas, SHA256 `d9a3519aab4c8fde6c5e23b149654a53bed3b276608ddd8c587a5e8089ce876f`.
- Web: `entregas/web/index.html`, cuatro páginas navegables, F01–F06 y el piloto de especialización.
- Fuentes: `libro/capitulos/01-territorio.Rmd`, presentación, fragmento II.2, CSV de pies y generadores de las figuras.
- Integración 40/40; navegador 39/39; preservación y consistencia narrativa 17/17. Se cotejaron 75 párrafos de extracción comparable, los pies completos y las fórmulas/código conservados.
- Revisión visual de las 23 páginas del capítulo y 30 del libro, más vistas de escritorio y móvil. Sin recortes, glifos ausentes o fórmulas desbordadas. Las copias PDF en web coinciden con las de entrega.

Los datos cuantitativos, originales, bibliografía y matriz de especialización permanecen intactos. Sólo se actualizaron los detalles textuales de nodos F06 entre los datos preparados, con el manifiesto de hashes correspondiente. Las auditorías específicas anteriores se conservan como antecedentes.

## Continuidad

El [informe de revisión](REVISION_NARRATIVA_B02.md) detalla el alcance y la verificación. El contenido corregido está publicado en el commit `f43d22daf7905a2e578ad3de7d15dfcca8453e6e`, con árbol idéntico al checkpoint local `745ab2e7be8ae6f8827bdf29cc032a527c1b893e`. Se comprobaron 61 blobs únicos y 92 rutas actualizadas; véase [el comprobante de esta revisión](verificacion-publicacion-revision-B02.json). El PR #1 está actualizado. Los comprobantes anteriores se conservan como antecedentes. No quedan archivos de esta solicitud pendientes de publicación.

No quedan correcciones independientes o decisiones metodológicas pendientes de esta solicitud. Corresponde la nueva lectura del autor. Para ajustes posteriores, reanudar en `libro/capitulos/01-territorio.Rmd` o el generador del recurso afectado, consultar primero plan/estado/decisiones/guía, compilar con `Rscript scripts/compilar.R todo` y repetir las comprobaciones pertinentes. Conservar la prioridad narrativa y el destino fork. No iniciar B03 sin autorización que lo comprenda.

Se mantienen documentados la climatología histórica, la generalización cartográfica, la diferencia temporal RHA 2022/2023, la discordancia de suelo y el redondeo acuícola de 1 t. La compilación ordinaria funciona sin red con derivados congelados; los originales grandes permanecen en `.local/B02-originales` y su recuperación se describe en `REPRODUCIBILIDAD_B02.md`. `cerrar_B02.py` conserva el cierre histórico y está protegido para que no sobrescriba estas instrucciones actuales.
