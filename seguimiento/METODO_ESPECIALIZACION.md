# Método conservado de medición de la especialización

Registro B01 del 5 de noviembre de 2026. Este documento fija las convenciones del fragmento vigente y el contrato de sus datos. Las comprobaciones quedan disponibles para el capítulo II, sin actualizar el año de la matriz ni modificar los índices aceptados.

## Insumos y corte de la edición

La fuente directa es `datos/originales/especializacion/PIBE_2024_In.xlsx`, hoja `Indices_Krugman`, rango `A1:W34`. Su copia tabular, `Matriz_original_Indices_Krugman.csv`, coincide exactamente con las 726 celdas numéricas del rango y conserva las etiquetas estatales. Ambos archivos mantienen sus bytes y su huella SHA-256 en `auditoria-especializacion.json`.

La matriz corresponde a 2024 y se expresa en millones de pesos de 2018. Reúne 32 entidades y 21 actividades, con minería petrolera y no petrolera separadas. Las etiquetas `21-1` y `21-2` identifican esa apertura dentro de la tabla; no se presentan como sectores SCIAN independientes. La apertura reemplaza la minería agregada y evita duplicarla.

El total de las actividades es VAB. El VAB nacional asciende a **23,982,097.474 millones de pesos de 2018**. Se conservan las 672 observaciones, incluidos 36 ceros. No hay datos faltantes. La rutina se detiene ante valores no finitos o negativos, totales estatales no positivos o actividades nacionales nulas.

La consulta original se conserva como INEGI (2026), de acuerdo con el antecedente. El día de descarga original no está documentado y no se sustituye por la fecha de esta auditoría. La verificación local se realizó el 5 de noviembre de 2026. El corte de B01 mantiene esta matriz; una revisión de la serie en INEGI se evaluará expresamente al trabajar el capítulo II.

## Definiciones y denominadores

Sea \(x_{ij}\) el VAB de la actividad \(j\) en la entidad \(i\). Los totales son \(x_{i\cdot}=\sum_j x_{ij}\), \(x_{\cdot j}=\sum_i x_{ij}\) y \(x_{\cdot\cdot}=\sum_i\sum_j x_{ij}\). Se utilizan las siguientes participaciones.

| Símbolo | Cálculo | Campo conservado |
|---|---|---|
| \(s_{ij}\) | \(x_{ij}/x_{i\cdot}\) | `participacion_local` |
| \(s_j\) | \(x_{\cdot j}/x_{\cdot\cdot}\) | `participacion_nacional` |
| \(q_{ij}\) | \(x_{ij}/x_{\cdot j}\) | `participacion_sector` |
| \(w_i\) | \(x_{i\cdot}/x_{\cdot\cdot}\) | `peso` |

Las participaciones se conservan como proporciones. Sólo `diferencia_pp` y los rótulos porcentuales multiplican por cien. Los denominadores proceden de las sumas de VAB de la misma matriz. El producto estadístico de origen es PIBE; ello no autoriza a sustituir el denominador por un PIB con impuestos netos de subsidios sobre los productos.

\[
KSI_i=\sum_{j=1}^{21}|s_{ij}-s_j|,
\qquad ICE_j=\sum_{i=1}^{32}|q_{ij}-w_i|.
\]

KSI e ICE mantienen la **suma completa, sin factor 1/2**, con escala general de cero a dos. Se obtienen 32 KSI y 21 ICE. El KSI compara la composición de una entidad con la del país completo, que incluye a esa entidad. La cota estatal es \(2(1-w_i)\). Un KSI bajo expresa semejanza con la estructura nacional; la diversidad interna requiere examinar las participaciones sectoriales. El ICE compara el reparto territorial de una actividad con el peso económico de las entidades y no constituye un índice estatal.

\[
IEE_{ij}=\frac{s_{ij}}{s_j}=\frac{q_{ij}}{w_i}.
\]

El IEE es el cociente de localización aplicado a VAB. Se calculan las 672 combinaciones. El umbral de referencia es uno; valores superiores indican una participación local mayor que la nacional. El IEE no comparte la cota superior de dos de las distancias. La matriz observada alcanza 22.7450294905624 en minería petrolera de Campeche. Los ceros se mantienen como IEE igual a cero cuando los denominadores son positivos.

## Relaciones comprobadas

Se verifican la suma unitaria de las participaciones, las dos expresiones del IEE, sus promedios ponderados y la identidad entre las distancias.

\[
KSI_i=\sum_j s_j|IEE_{ij}-1|,\qquad
ICE_j=\sum_i w_i|IEE_{ij}-1|,
\]
\[
\sum_i w_iKSI_i=\sum_j s_jICE_j.
\]

Las dos agregaciones utilizan los mismos valores y coberturas. La sensibilidad a la agregación minera se conserva como cálculo complementario de 20 sectores y se comprueba que no aumenta el KSI. El piloto utiliza los 21 componentes aceptados.

## Cifras para el texto del piloto

| Ejemplo | Resultado sin redondear | Presentación orientativa |
|---|---:|---:|
| KSI de Campeche | 1.352436583141807 | 1.352 |
| Minería petrolera en el VAB de Campeche | 0.6116261230328897 | 61.16 % |
| Minería petrolera en el VAB nacional | 0.02689053989957109 | 2.69 % |
| Manufacturas en el VAB de Coahuila | 0.46739960012632503 | 46.74 % |
| Manufacturas en el VAB nacional | 0.21674131129002683 | 21.67 % |
| IEE manufacturero de Coahuila | 2.156485984810188 | 2.156 |

El cálculo conserva toda la precisión de los valores de origen. Los redondeos pertenecen a la presentación y no se realimentan a los índices.

## Contrato gráfico

`F07-KSI` identifica el piloto de barras estatales y se vincula con `F07-ksi.png`, `F07-ksi.pdf` y su explorador HTML. Los datos son `datos/preparados/capitulo-02/KSI_entidades.csv`, con orden inicial descendente y 32 entidades visibles. El eje utiliza la escala general de 0 a 2. El azul `#0F4761` adapta las barras a la identidad editorial del PDF base y conserva una única serie; esta decisión de presentación no altera los resultados. La salida PNG tiene 300 ppp y el PDF es vectorial con tipografía incrustada mediante Cairo.

Los identificadores estables de figuras no dependen de su número impreso. `F01` a `F06` quedan reservados al capítulo I. La ubicación prevista de F07-KSI en el capítulo II es el apartado de medición de la especialización, primera figura del inciso. La edición del piloto puede emplear numeración propia de prueba.

Se conservan las decisiones de las demás figuras del fragmento. La matriz de calor reúne las 32 × 21 celdas sin números dentro de ellas. Los mapas del IEE y la matriz comparten degradado continuo de azul a rojo oscuro, con color transformado por `log(1 + IEE)` y barra horizontal inferior rotulada en valores originales. El mapa del KSI utiliza la misma familia cromática con escala propia de 0 a 2. Los cinco mapas independientes son uno de KSI y cuatro de IEE; cada uno identifica las cinco entidades con mayor índice. La escala común del IEE, los ceros y la matriz completa no se cambian por un filtro del explorador del piloto. B01 conserva esos mapas como antecedentes y no los presenta como mapas recién elaborados.

## Reproducción y comprobaciones

Desde la raíz del repositorio se ejecuta:

```text
Rscript --vanilla analisis/capitulo-02/preparar_especializacion.R
Rscript --vanilla analisis/capitulo-02/generar_interactivo.R
python analisis/capitulo-02/auditar_especializacion.py
```

La primera rutina usa exclusivamente R base y los dispositivos gráficos incluidos con R. Se verificó con R 4.6.1 y Cairo disponible. No instala paquetes ni descarga series. Escribe los datos preparados, las tablas y las dos salidas estáticas. `Sesion_R.txt` registra el entorno. El contraste heredado usa los CSV de `referencias/antecedentes/especializacion/Figuras_Capitulo_II_Especializacion_2024` únicamente como control, después del cálculo.

La auditoría independiente utiliza Python con `openpyxl` 3.1.5 para abrir el Excel y vuelve a calcular los indicadores con operaciones numéricas propias de Python. Sus 38 comprobaciones contrastan las cifras del Excel, el CSV original, las salidas R y las tablas aceptadas del antecedente. También contrastan aportaciones, participaciones y denominadores. El informe completo es `auditoria-especializacion.json`; la tabla de pruebas es `auditoria-especializacion.csv`. Todas las pruebas resultaron correctas con tolerancia de 1e-8 para índices y proporciones. Las sumas monetarias usan 0.02 millones como tolerancia de agregación del antecedente, y el cotejo de sus exportaciones usa 1e-7.

La segunda rutina produce `assets/capitulo-02/interactivos/F07-ksi.html` con los 32 resultados y el CSV completos embebidos. El HTML funciona sin conexión ni bibliotecas externas. La vista inicial conserva el orden descendente; el orden alfabético cambia la ubicación de las barras y la selección destaca una entidad sin retirar las restantes. La tabla sigue el orden visible y muestra los valores conservados. El eje permanece en 0 a 2 al cambiar los controles. La descarga CSV incluye las 32 entidades y los mismos datos preparados. Se comprobó la estructura del JSON, la sintaxis del programa, las dimensiones y la ausencia de dependencias externas; la revisión del recurso integrado se registra en las comprobaciones editoriales de B01.

Se inspeccionaron la imagen final y una rasterización del PDF de F07-KSI. Las 32 etiquetas estatales, cifras, eje, fuente y título son legibles y no presentan recortes ni superposición. Los originales no se modificaron durante los cálculos.

## Reutilización en B03

El capítulo II podrá incorporar estas rutinas, fuentes y datos sin recalcular desde índices ya guardados. Al extender la interactividad se reutilizarán los mismos datos preparados para ICE y toda la matriz IEE. La verificación de la fuente oficial, la trazabilidad de la regionalización para insumo-producto y la bibliografía completa pertenecen al alcance de B03. El cierre técnico de este piloto no sustituye esas tareas.
