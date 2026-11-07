# Datos del manual

Cada archivo tiene una ubicación canónica. Las bases exclusivas se guardan en `capitulo-XX/`. Si un segundo capítulo necesita una de ellas, se mueve a `globales/` y se actualizan todos los consumidores en el mismo cambio. El archivo `uso-global.csv` identifica los capítulos que utilizan cada base compartida.

`globales/estados-web.json` es el catálogo territorial y la geometría de dibujo común. Lo leen F01, F02 y F04 en el capítulo I; el generador F07 del capítulo II toma de ahí las denominaciones estatales mediante la clave de entidad. Sus cifras de especialización proceden exclusivamente de `capitulo-02/`.

Las fuentes directas que intervienen en un cálculo reproducible se guardan en `fuentes/`. El manifiesto conserva la procedencia y las huellas de los insumos preparados. [`procedencia-geografica.csv`](procedencia-geografica.csv) permite localizar los archivos oficiales de los que se obtuvieron las capas físicas. Los HTML contienen las porciones que necesitan para funcionar de forma autónoma; se regeneran desde estas bases y no se editan como fuentes de datos.
