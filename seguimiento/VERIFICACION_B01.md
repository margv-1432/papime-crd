# Verificación de la entrega B01

Corte 5 de noviembre de 2026.

| Componente | Evidencia | Resultado |
|---|---|---|
| Originales | Inventario de 476 archivos y manifiesto anterior 43/43 | Sin alteración de archivos externos; originales decisivos copiados íntegros |
| Cálculo | `auditoria-especializacion.json` | 38/38 pruebas Excel, CSV, Python, R y antecedentes |
| Proyecto | `verificacion-proyecto.json` | 22/22 comprobaciones de integridad, citas, enlaces y salidas |
| Navegador | `verificacion-web.json`; script `scripts/verificar_web.cjs --serve` | 22/22 pruebas; Chrome con servidor temporal local |
| PDF | Revisión visual independiente de las nueve páginas renderizadas | Títulos, cinco ecuaciones, figura y pie, folios y referencias legibles; sin recortes ni páginas vacías |
| GitHub | Fork autorizado [margv-1432/papime-crd](https://github.com/margv-1432/papime-crd); publicación inicial `576d2680750ea24f72b2c24c8481357384a58f2d` | 185 rutas añadidas o modificadas con hashes Git coincidentes y árbol idéntico al checkpoint local `7ebcd33`; repositorio original intacto |

Se verificaron 32 KSI, 21 ICE y 672 IEE. El VAB nacional es 23,982,097.474 millones de pesos de 2018, con 36 ceros y sin valores faltantes en la matriz. Las cifras empíricas del piloto se calculan en línea desde las tablas preparadas; sus casos de control también se comprueban antes de renderizar.

La prueba de navegador comprobó navegación entre las tres páginas, bibliografía única al final, cinco ecuaciones de bloque y trece expresiones en línea, sin errores matemáticos. En el gráfico, los controles mantienen las 32 entidades, el teclado permite seleccionar barras y la tabla y descarga conservan los valores del CSV. La búsqueda devuelve resultados pertinentes y una consulta inexistente devuelve cero. La pantalla de 360 px no produce desbordamiento del texto; las fórmulas largas tienen desplazamiento propio. No se observaron errores de JavaScript, fallos de red ni recursos de terceros solicitados por las páginas.

La revisión visual corrigió el espacio superior de títulos, el encabezado residual del índice y la separación entre figura y fuente. El PDF entregado conserva SHA256 `fc855580b8bacc7e1cd91c3d7bb94d593f2075e0d56a68ec5718f32a4690e996`. El PDF dentro de la carpeta web coincide byte por byte.

Los controles aquí aplicados verifican el piloto y su preparación. Los otros recursos de especialización permanecen conservados como antecedentes y los recursos F01–F06 y capítulos pendientes no se declaran validados por estas comprobaciones. Sus tareas están delimitadas en el registro de figuras y el inventario.


La publicación inicial de B01 en el fork conserva el árbol Git `e44bea84bcf4310213e78dd8734b1d7c4fcc7988`, correspondiente al checkpoint local `7ebcd33310d55b128e755f8610a72559648baf7e`, sobre el commit base `458257c3d7b69602560cbcaeb89fd0980297ad6b`. La comprobación de las 185 rutas añadidas o modificadas respecto de esa base incluye sus modos y hashes de blob canónicos, además de la identidad del árbol completo. El commit remoto inicial es `576d2680750ea24f72b2c24c8481357384a58f2d`; los checkpoints locales permanecen conservados. El cierre documental posterior deja registrada la nueva ubicación sin modificar el piloto. No fue necesario repetir los cálculos ni las pruebas de lectura por este cambio de destino. Los intentos previos sobre el repositorio original devolvieron 403; el fork resolvió ese impedimento.
