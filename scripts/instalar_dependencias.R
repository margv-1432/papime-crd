# Biblioteca del proyecto; no modifica bibliotecas globales.
args <- commandArgs(trailingOnly = FALSE)
archivo <- sub("^--file=", "", args[grepl("^--file=", args)])
raiz <- normalizePath(file.path(dirname(archivo), ".."), winslash="/")
lib <- file.path(raiz, ".local/R")
dir.create(lib, recursive=TRUE, showWarnings=FALSE)
.libPaths(c(lib, .libPaths()))
paquetes <- c("bookdown","rmarkdown","knitr","htmltools","jsonlite","tinytex","xfun",
 "bslib","evaluate","fontawesome","jquerylib","yaml","cachem","memoise","mime",
 "sass","lifecycle","rlang","cli","glue","R6","rappdirs","fs","fastmap","base64enc","digest","highr")
faltan <- paquetes[!vapply(paquetes, requireNamespace, quietly=TRUE, FUN.VALUE=logical(1))]
if (length(faltan)) install.packages(faltan, lib=lib, repos="https://cloud.r-project.org")
if (!all(vapply(paquetes, requireNamespace, quietly=TRUE, FUN.VALUE=logical(1)))) stop("Hay dependencias sin resolver.")
cat("Dependencias de R disponibles. Pandoc y XeLaTeX se instalan por separado.\n")
