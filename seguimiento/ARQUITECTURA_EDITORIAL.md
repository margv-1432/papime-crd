# Arquitectura editorial en Quarto

El manuscrito rector es `bibliografia/manuscrito-base.pdf`. Conserva su función de fuente y guía visual. `index.qmd` presenta el libro; `_quarto.yml` organiza la edición web. Cada capítulo tiene una fuente editable en `capitulos/` con su título y anclas estables. La navegación incorpora el capítulo I y el fragmento II.2, con referencias comunes. Los archivos de capítulos pendientes se incorporan al índice cuando tengan contenido revisado.

La revisión de B02 conserva el capítulo I y F01–F06. El capítulo II conserva la medición de especialización y F07-KSI, preparada originalmente como piloto. B03 completará II.1 Segmentación de la producción, II.2 Medición de la especialización, II.3 Cadenas de valor regionales y II.4 Regiones y el sector externo. Las fuentes de capítulos pendientes son lugares de edición.

Los rótulos siguen capítulo, apartado y secuencia, por ejemplo II.2.1. El registro de figuras vincula sus IDs con fuentes, datos y generadores. Un número editorial puede ajustarse durante la integración; el ID de recurso se conserva. Los pies se mantienen con la figura en la fuente del capítulo. Las citas remiten a `bibliografia/bibliografia.bib`.

Los `.qmd` enlazan los exploradores HTML de `plots/capitulo-XX/`. Quarto ejecuta los generadores antes del render. El CSS del libro y de cada capítulo está en `estilos/`; los widgets incorporan su estilo al generarse. Los datos compartidos tienen una única ruta en `datos/globales/` y los exclusivos permanecen en su capítulo. El navegador carga las figuras desde el sitio, sin reconstruir cálculos a partir de filtros visuales.

La edición activa es web, sin actividades finales. La guía editorial y las decisiones metodológicas continúan vigentes. La revisión comprueba prosa, referencias, cifras e interacciones en el conjunto del capítulo.
