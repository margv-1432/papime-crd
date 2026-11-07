# Manual interactivo de economía mexicana

Proyecto PAPIME. El [fork de trabajo](https://github.com/margv-1432/papime-crd) reúne los capítulos editables, los generadores de las figuras y sus datos. El repositorio `postsocratico/papime-crd` se consulta como antecedente.

| Carpeta | Contenido |
|---|---|
| [`capitulos/`](capitulos/) | Un archivo `.qmd` por capítulo. `index.qmd` es la presentación del libro. |
| [`plots/`](plots/) | Generadores, plantillas y HTML interactivos, organizados por capítulo. |
| [`datos/`](datos/) | Bases exclusivas en `capitulo-XX/`, compartidas en `globales/` y fuentes directas en `fuentes/`. |
| [`estilos/`](estilos/) | CSS del manual, de los capítulos y de sus widgets. |
| [`bibliografia/`](bibliografia/) | Referencias, matriz de consulta y manuscrito rector. |
| [`seguimiento/`](seguimiento/) | Planeación vigente, decisiones, registro de figuras y estado. |

## Edición conjunta

Edita el `.qmd` del capítulo desde una rama del fork y abre un pull request allí. Las citas usan claves de `bibliografia/bibliografia.bib`. Los cambios de una figura se hacen en su generador, plantilla o estilo y se versionan junto con el HTML resultante. Las modificaciones de una base compartida se comprueban en todos sus capítulos consumidores.

Quarto incluye en el libro la presentación, el capítulo I, el fragmento desarrollado de II.2 y las referencias. Los otros `.qmd` reservan el título y el lugar de los capítulos pendientes. Se incorporarán a `_quarto.yml` cuando tengan contenido revisado.

## Compilación web

Instala Quarto, Python 3 y R. En R, ejecuta `source("scripts/instalar.R")` una vez desde la raíz para preparar los paquetes. Si las herramientas no están disponibles por su nombre, puedes indicar sus rutas con `PAPIME_QUARTO`, `PAPIME_RSCRIPT` y, si es necesario, `PAPIME_R_LIBRARY`.

```sh
python scripts/compilar.py
python scripts/verificar.py
```

La compilación ejecuta los generadores de widgets antes de renderizar y deja el libro en `web/index.html`. Se reutilizan figuras cuando sus entradas y salidas coinciden con la verificación anterior. `web/` se genera localmente; los HTML individuales sí se versionan en `plots/` y contienen sus datos y estilos para poder abrirlos por separado. Las bases canónicas se consultan en `datos/`. El flujo utiliza datos congelados y entrega únicamente HTML.

Consulta el [plan](seguimiento/PLAN.md) y el [estado](seguimiento/ESTADO.md) antes de comenzar otro bloque. El historial de Git conserva las versiones y fuentes que salieron del árbol activo durante la reorganización.
