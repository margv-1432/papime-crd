# Ejecutar una vez en R, en la biblioteca personal del colaborador.
paquetes <- c("knitr", "rmarkdown", "sf", "terra", "jsonlite", "base64enc")
faltan <- paquetes[!vapply(paquetes, requireNamespace, logical(1), quietly = TRUE)]
if (length(faltan)) install.packages(faltan, repos = "https://cloud.r-project.org")
