# Estado del proyecto PAPIME

Fecha de corte 5 de noviembre de 2026. Bloque activo B01. Alcance editorial y técnico terminado y verificado; cierre administrativo pendiente de sincronización en GitHub por falta de acceso de escritura. Entrega local lista para revisión. B02 no iniciado.

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
| Control de versiones | Checkpoints locales y paquete de sincronización conservados. GitHub mantiene 458257c: los intentos de escritura mediante el conector devolvieron 403. |

La revisión visual independiente del PDF aprobó sus nueve páginas. La web pasó 22/22 comprobaciones con un navegador real y servidor local, incluida búsqueda, descarga exacta, teclado y pantalla de 360 px. No hubo errores JavaScript ni solicitudes externas. La comprobación integral del proyecto pasó 22/22 pruebas adicionales. Los informes están en `auditoria-especializacion.json`, `verificacion-web.json` y `verificacion-proyecto.json`; el alcance de las revisiones consta en `VERIFICACION_B01.md`.

## Sincronización pendiente

La conexión GitHub está instalada en la cuenta `margv-1432` y permite consultar el repositorio público, pero rechazó la creación de un blob y de `seguimiento/PLAN.md` con `403 Resource not accessible by integration`. Git local tampoco tiene credenciales de escritura. No se creó un commit remoto ni se modificó la rama remota. La consulta inicial `permissions.push` del repositorio no demuestra acceso de escritura del token de la integración.

Se reintentó la subida por solicitud expresa del autor. El conector volvió a rechazar la escritura con el mismo 403 y el intento normal de `git push origin main`, sin forzar, confirmó que no hay credenciales disponibles. La instalación sigue correspondiendo únicamente a `margv-1432`, y se comprobó que `main` remoto permanece en `458257c3d7b69602560cbcaeb89fd0980297ad6b`. No hay cambios remotos que conciliar. El contenido del piloto y sus comprobaciones no cambiaron.

Se necesita habilitar `postsocratico/papime-crd` en una conexión con escritura o autenticar Git con una cuenta autorizada. El encargo ya autoriza sincronizar B01, así que no se necesita volver a decidir su contenido. Una vez disponible el acceso, comprobar primero `origin/main`, conservar cambios ajenos si los hubiera y subir los commits locales. Si se continúa en esta copia basta con autenticar y ejecutar `git push origin main`, sin forzar. El paquete `entregas/PAPIME-B01-git.bundle` permite recuperar los commits sobre el commit base en otra copia. El paquete de revisión y el bundle quedan fuera del versionado para evitar copias recursivas; todos sus componentes editoriales están guardados en el repositorio local.

## Continuación precisa

Resolver la sincronización anterior y revisar el piloto en `entregas/web/index.html` y `entregas/pdf/PAPIME-B01-piloto.pdf`. El paquete `entregas/PAPIME-B01-revision.zip` reúne las salidas y fuentes nuevas. Los cambios solicitados sobre identidad visual, navegación o densidad se aplicarán a las plantillas de B01 y se volverán a compilar y verificar. El capítulo I no se comenzará antes de esa revisión.

Tras la revisión del autor, B02 partirá de `ARQUITECTURA_EDITORIAL.md`, `GUIA_EDITORIAL.md`, `MATRIZ_BIBLIOGRAFICA.csv`, `registro-figuras.csv` e `INVENTARIO.md`. Se recuperarán las páginas 1–15 del PDF rector y los insumos de Mexicana_Tarea_3; se desarrollará evolución territorial y se resolverán regionalización y F01–F06. No repetir la auditoría del piloto ni cambiar su corte de datos para ese trabajo.

## Pendientes conservados para los bloques correspondientes

La descarga original de la matriz no tiene fecha demostrada. La edición de Miller y Blair y otras referencias incompletas requieren cotejo en B03. La base regional de insumo-producto sigue sin validar. Las notas de F01–F06 y la tabla de regresiones del capítulo IV permanecen dentro de sus bloques. Estos asuntos no impiden revisar y cerrar la preparación editorial de B01.
