# Datos del piloto de especialización

El manifiesto registra procedencia, transformaciones y hashes. El original del Excel y su matriz CSV se conservan íntegros. La hoja `Indices_Krugman`, celdas A1:W34, contiene encabezados, 32 entidades y una fila nacional. Las columnas B a V contienen VAB sectorial y W un total de control. No sumar de nuevo la fila nacional a las estatales.

`cve_ent` es una clave de dos caracteres, incluidos ceros iniciales. `codigo` identifica la actividad y conserva los guiones de 21-1, 21-2, 31-33 y 48-49. `nombre_corto` se usa para leyendas y no reemplaza la clave territorial. El catálogo conserva el nombre original y el rótulo didáctico.

`VAB_sector` es el valor de la celda en millones de pesos de 2018. `VAB` es la suma estatal de las 21 actividades; `peso` es su participación en la suma nacional. `participacion_local` es la proporción del sector dentro de la entidad. `participacion_nacional` es la proporción del sector en el VAB del país. `participacion_sector` es la proporción estatal dentro del sector nacional. Las participaciones están en escala 0–1, salvo el campo `diferencia_pp`, expresado en puntos porcentuales.

`IEE` es participacion_local/participacion_nacional. `aportacion_KSI` y `aportacion_ICE` son diferencias absolutas de participaciones. `KSI` e `ICE` suman dichas contribuciones, sin factor 1/2. Los CSV conservan precisión de cálculo; los textos y etiquetas pueden redondear. La tabla de sensibilidad agrega las dos actividades mineras sin eliminar valor agregado.

Los 36 ceros de la matriz original se preservan. No hay faltantes. Un dato faltante, un valor negativo o un denominador nulo detienen el cálculo. El corte se identifica como matriz recibida de 2024; no se afirma que sea la revisión más reciente del productor. Las fechas de consulta bibliográfica en 2026 corresponden a verificación documental y no prueban la fecha original de descarga de los datos.
