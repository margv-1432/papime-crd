# Ejecutar desde cualquier directorio: Rscript scripts/compilar.R [web|pdf|todo]
args <- commandArgs(trailingOnly = FALSE)
archivo <- sub("^--file=", "", args[grepl("^--file=", args)])
raiz <- normalizePath(file.path(dirname(archivo), ".."), winslash = "/", mustWork = TRUE)
setwd(raiz)
if (.Platform$OS.type == "windows") invisible(suppressWarnings(Sys.setlocale("LC_CTYPE", "Spanish_Mexico.utf8")))
.libPaths(c(file.path(raiz, ".local/R"), .libPaths()))
if (!requireNamespace("bookdown", quietly = TRUE)) stop("Ejecute scripts/instalar_dependencias.R antes de compilar.")
if (!nzchar(Sys.getenv("RSTUDIO_PANDOC"))) {
  candidato <- "C:/Program Files/RStudio/resources/app/bin/quarto/bin/tools"
  if (file.exists(file.path(candidato, "pandoc.exe"))) Sys.setenv(RSTUDIO_PANDOC = candidato)
}
if (!nzchar(Sys.which("xelatex")) && .Platform$OS.type == "windows") {
  candidato <- file.path(Sys.getenv("APPDATA"), "TinyTeX/bin/windows")
  if (dir.exists(candidato)) Sys.setenv(PATH = paste(candidato, Sys.getenv("PATH"), sep = .Platform$path.sep))
}
modo <- commandArgs(trailingOnly = TRUE)
modo <- if (length(modo)) modo[1] else "todo"
stopifnot(modo %in% c("web", "pdf", "todo"))
source("analisis/capitulo-02/preparar_especializacion.R", chdir = FALSE, encoding = "UTF-8")
source("analisis/capitulo-02/generar_interactivo.R", chdir = FALSE, encoding = "UTF-8")
setwd(file.path(raiz, "libro"))
if (modo %in% c("pdf", "todo")) bookdown::render_book("index-B01.Rmd", "bookdown::pdf_book", config_file="_bookdown-B01.yml", quiet = TRUE)
if (modo %in% c("web", "todo")) bookdown::render_book("index-B01.Rmd", "bookdown::gitbook", config_file="_bookdown-B01.yml", quiet = TRUE)
setwd(raiz)
dir.create("entregas/pdf", recursive = TRUE, showWarnings = FALSE)
dir.create("entregas/B01-web", recursive = TRUE, showWarnings = FALSE)
pdf <- "libro/_book-B01/papime-piloto.pdf"
if (file.exists(pdf)) file.copy(pdf, "entregas/pdf/PAPIME-B01-piloto.pdf", overwrite = TRUE)
if (modo %in% c("web", "todo")) {
  elementos <- list.files("libro/_book-B01", full.names = TRUE, all.files = TRUE, no.. = TRUE)
  elementos <- elementos[!grepl("\\.tex$|reference-keys\\.txt$", elementos)]
  file.copy(elementos, "entregas/B01-web", recursive = TRUE, overwrite = TRUE)
  dir.create("entregas/B01-web/recursos", recursive = TRUE, showWarnings = FALSE)
  file.copy("assets/capitulo-02/interactivos/F07-ksi.html", "entregas/B01-web/recursos/F07-ksi.html", overwrite = TRUE)
  file.copy("assets/capitulo-02/figuras-estaticas/F07-ksi.png", "entregas/B01-web/recursos/F07-ksi.png", overwrite = TRUE)
  file.copy("datos/preparados/capitulo-02/KSI_entidades.csv", "entregas/B01-web/recursos/KSI_entidades.csv", overwrite = TRUE)
  file.copy("libro/estilos/vendor/mathjax-3.2.2/tex-svg.js", "entregas/B01-web/recursos/tex-svg.js", overwrite = TRUE)
  file.copy("libro/estilos/vendor/mathjax-3.2.2/LICENSE", "entregas/B01-web/recursos/LICENSE-MathJax.txt", overwrite = TRUE)
  file.copy("libro/estilos/vendor/fuse-6.4.6/fuse.min.js", "entregas/B01-web/recursos/fuse.min.js", overwrite = TRUE)
  file.copy("libro/estilos/vendor/fuse-6.4.6/LICENSE", "entregas/B01-web/recursos/LICENSE-Fuse.txt", overwrite = TRUE)
  for (pagina in list.files("entregas/B01-web", pattern="\\.html$", full.names=TRUE)) {
    h <- readLines(pagina, encoding="UTF-8", warn=FALSE)
    h <- gsub("https://cdn.jsdelivr.net/npm/fuse.js@6.4.6/dist/fuse.min.js", "recursos/fuse.min.js", h, fixed=TRUE)
    h <- gsub("https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.9/latest.js?config=TeX-MML-AM_CHTML", "recursos/tex-svg.js", h, fixed=TRUE)
    h <- sub("[[:blank:]]+$", "", h)
    writeLines(h, pagina, useBytes=TRUE)
  }
  if (file.exists(pdf)) file.copy(pdf, "entregas/B01-web/papime-piloto.pdf", overwrite = TRUE)
}
writeLines(sub("[[:blank:]]+$", "", capture.output(sessionInfo())), "seguimiento/compilacion-sessionInfo.txt")
paquetes <- list.dirs(".local/R", recursive = FALSE, full.names = TRUE)
manifiesto <- do.call(rbind, lapply(paquetes, function(p) {
  d <- file.path(p, "DESCRIPTION")
  if (!file.exists(d)) return(NULL)
  x <- read.dcf(d)
  data.frame(paquete=x[1,"Package"], version=x[1,"Version"], stringsAsFactors=FALSE)
}))
write.csv(manifiesto, "seguimiento/dependencias-R.csv", row.names = FALSE, fileEncoding = "UTF-8")
cat("Piloto compilado:", modo, "\n")
