# Estado del proyecto PAPIME

Fecha de corte 5 de noviembre de 2026. B01 completado, verificado y publicado en GitHub. Entrega disponible para revisión del autor antes de avanzar al capítulo I. B02 no iniciado.

El proyecto de trabajo está en `C:/Users/marce/Downloads/PAPIME/papime-crd`. La planeación mantenida es `seguimiento/PLAN.md`; el PDF rector está preservado en `referencias/manuscrito-base`. No se modificaron los originales de la carpeta principal.

## Avance de B01

| Componente | Resultado |
|---|---|
| Conciliación | Inventario de 476 insumos y contraste 43/43 del manifiesto anterior. PDF vigente y antecedentes distinguidos. |
| Arquitectura | Ocho capítulos reservados; reglas de numeración, anclas y registro de 17 figuras. |
| Guía editorial | Composición del PDF adaptada a web y PDF; reglas de redacción y datos conservadas. |
| Bibliografía | 32 claves en biblioteca común y 34 registros de matriz inicial; cinco obras con participación de Ruiz Durán. Acceso, lectura y páginas pendientes explícitos. |
| Cálculo | R base reproduce la matriz; auditoría independiente Python/Excel con 38 pruebas correctas. |
| Piloto | Tres páginas web navegables y PDF de nueve páginas; cinco ecuaciones, citas verificadas y F07-KSI en HTML y figura estática. |
| Reproducción | Scripts de preparación, compilación, instalación y auditoría; versiones de paquetes y sesión registradas. |
| Control de versiones | Publicación inicial de B01 en el fork [margv-1432/papime-crd](https://github.com/margv-1432/papime-crd), commit `576d2680750ea24f72b2c24c8481357384a58f2d`. Checkpoints locales conservados. |

La revisión visual independiente del PDF aprobó sus nueve páginas. La web pasó 22/22 comprobaciones con un navegador real y servidor local, incluida búsqueda, descarga exacta, teclado y pantalla de 360 px. No hubo errores JavaScript ni solicitudes externas. La comprobación integral del proyecto pasó 22/22 pruebas adicionales. Los informes están en `auditoria-especializacion.json`, `verificacion-web.json` y `verificacion-proyecto.json`; el alcance de las revisiones consta en `VERIFICACION_B01.md`.

## Publicación y conservación

El repositorio de trabajo publicado es [margv-1432/papime-crd](https://github.com/margv-1432/papime-crd), fork autorizado por el autor de [postsocratico/papime-crd](https://github.com/postsocratico/papime-crd). La publicación inicial de B01 corresponde al [commit `576d2680750ea24f72b2c24c8481357384a58f2d`](https://github.com/margv-1432/papime-crd/commit/576d2680750ea24f72b2c24c8481357384a58f2d). El repositorio original no se modificó.

La instantánea publicada mediante la API conserva el árbol Git `e44bea84bcf4310213e78dd8734b1d7c4fcc7988`, idéntico al del checkpoint local `7ebcd33310d55b128e755f8610a72559648baf7e`, sobre el commit base `458257c3d7b69602560cbcaeb89fd0980297ad6b`. Se comprobó la correspondencia de las 185 rutas añadidas o modificadas mediante sus identificadores de blob de Git y la identidad del árbol completo. Las actualizaciones de seguimiento que documentan esta publicación constituyen el cierre posterior; no cambian datos, cálculos ni figuras del piloto.

Los checkpoints locales no se borraron ni se reescribieron. La creación del fork resolvió el acceso para publicar, después de los rechazos 403 al escribir en el repositorio original y de la ausencia de credenciales para Git local. Esos fallos quedan como antecedentes, sin tareas de sincronización pendientes para B01.

En la copia local, `origin` identifica el fork y `upstream` conserva el repositorio de referencia. La rama `main` queda alineada con la publicación tras comprobar la igualdad de sus árboles. La rama `respaldo/b01-local-20261105` conserva los checkpoints anteriores y el cierre documental local; no se descartaron archivos ni se reescribió la historia del repositorio original. Las siguientes publicaciones mediante el conector partirán del último commit de `main` del fork y comprobarán el árbol resultante.

La entrega se consulta en el [PDF del piloto](https://github.com/margv-1432/papime-crd/blob/main/entregas/pdf/PAPIME-B01-piloto.pdf), la [carpeta del libro web](https://github.com/margv-1432/papime-crd/tree/main/entregas/web) y las fuentes organizadas del fork. La carpeta web conserva todos sus recursos para descargarla y abrirla localmente; su presencia en GitHub no implica un sitio de GitHub Pages publicado. El paquete de revisión y el bundle locales siguen disponibles fuera del versionado para evitar copias recursivas.

## Continuación precisa

Revisar el piloto en `entregas/web/index.html` y `entregas/pdf/PAPIME-B01-piloto.pdf`. El paquete `entregas/PAPIME-B01-revision.zip` reúne las salidas y fuentes nuevas. Los cambios solicitados sobre identidad visual, navegación o densidad se aplicarán a las plantillas de B01 y se volverán a compilar y verificar. El capítulo I no se comenzará antes de esa revisión.

Tras la revisión del autor, B02 partirá de `ARQUITECTURA_EDITORIAL.md`, `GUIA_EDITORIAL.md`, `MATRIZ_BIBLIOGRAFICA.csv`, `registro-figuras.csv` e `INVENTARIO.md`. Se recuperarán las páginas 1–15 del PDF rector y los insumos de Mexicana_Tarea_3; se desarrollará evolución territorial y se resolverán regionalización y F01–F06. No repetir la auditoría del piloto ni cambiar su corte de datos para ese trabajo.

## Pendientes conservados para los bloques correspondientes

La descarga original de la matriz no tiene fecha demostrada. La edición de Miller y Blair y otras referencias incompletas requieren cotejo en B03. La base regional de insumo-producto sigue sin validar. Las notas de F01–F06 y la tabla de regresiones del capítulo IV permanecen dentro de sus bloques. Estos asuntos no impiden revisar y cerrar la preparación editorial de B01.
