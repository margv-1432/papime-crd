# Edición B02: regeneración sin red de F01--F06 y compilación de ambas lecturas.
args <- commandArgs(trailingOnly=FALSE)
archivo <- sub("^--file=","",args[grepl("^--file=",args)])
raiz <- normalizePath(file.path(dirname(archivo),".."),winslash="/",mustWork=TRUE)
setwd(raiz)
invisible(suppressWarnings(Sys.setlocale("LC_CTYPE","Spanish_Mexico.utf8")))
.libPaths(c(".local/R",Sys.getenv("PAPIME_R_LIBRARY"),"C:/Users/marce/AppData/Local/R/win-library/4.6",.libPaths()))
if(!requireNamespace("bookdown",quietly=TRUE))stop("Instale las dependencias indicadas en seguimiento/REPRODUCIBILIDAD.md")
if(!nzchar(Sys.getenv("RSTUDIO_PANDOC")))Sys.setenv(RSTUDIO_PANDOC="C:/Program Files/RStudio/resources/app/bin/quarto/bin/tools")
if(!nzchar(Sys.which("xelatex")))Sys.setenv(PATH=paste(file.path(Sys.getenv("APPDATA"),"TinyTeX/bin/windows"),Sys.getenv("PATH"),sep=.Platform$path.sep))
modo <- commandArgs(trailingOnly=TRUE)
modo <- if(length(modo))modo[1] else "todo"
stopifnot(modo %in% c("web","pdf","todo"))
python <- Sys.getenv("PAPIME_PYTHON")
runtime <- "C:/Program Files/WindowsApps/OpenAI.CodexPrimaryRuntime.v26-1030-493-0_26.1030.493.0_x64__3k8sg7r9htsxt/dependencies/python/python.exe"
if(!nzchar(python))python<-if(file.exists(runtime))runtime else Sys.which("python")
if(!nzchar(python))stop("Defina PAPIME_PYTHON con Python 3 y dependencias de B02")
run <- function(bin,script) {
  result<-system2(bin,shQuote(script))
  if(result!=0)stop("Falló ",script)
}
run(python,"analisis/capitulo-01/preparar_agua_sintesis.py")
run(python,"analisis/capitulo-01/preparar_F04.py")
run(file.path(R.home("bin"),"Rscript.exe"),"analisis/capitulo-01/generar_fisico.R")
setwd(file.path(raiz,"libro"))
if(modo %in% c("pdf","todo")) {
  bookdown::render_book("index-capitulo-I.Rmd","bookdown::pdf_book",config_file="_bookdown-capitulo-I.yml",quiet=TRUE)
  bookdown::render_book("index.Rmd","bookdown::pdf_book",quiet=TRUE)
}
if(modo %in% c("web","todo"))bookdown::render_book("index.Rmd","bookdown::gitbook",quiet=TRUE)
setwd(raiz)
dir.create("entregas/pdf",recursive=TRUE,showWarnings=FALSE)
dir.create("entregas/web/recursos",recursive=TRUE,showWarnings=FALSE)
file.copy("libro/_book-capitulo-I/papime-capitulo-I.pdf","entregas/pdf/PAPIME-B02-capitulo-I.pdf",overwrite=TRUE)
file.copy("libro/_book/papime-libro.pdf","entregas/pdf/PAPIME-libro-avance-B02.pdf",overwrite=TRUE)
if(modo %in% c("web","todo")) {
  elements<-list.files("libro/_book",full.names=TRUE,all.files=TRUE,no..=TRUE)
  elements<-elements[!grepl("\\.tex$|reference-keys\\.txt$",elements)]
  file.copy(elements,"entregas/web",recursive=TRUE,overwrite=TRUE)
  for(folder in c("interactivos","figuras-estaticas","tablas")) {
    files<-list.files(file.path("assets/capitulo-01",folder),full.names=TRUE,all.files=FALSE)
    files<-files[!grepl("\\.gitkeep$",files)]
    file.copy(files,"entregas/web/recursos",recursive=TRUE,overwrite=TRUE)
  }
  for(file in c("F07-ksi.html","F07-ksi.png")) {
    sub<-if(grepl("html$",file))"interactivos" else "figuras-estaticas"
    file.copy(file.path("assets/capitulo-02",sub,file),"entregas/web/recursos",overwrite=TRUE)
  }
  file.copy("datos/preparados/capitulo-02/KSI_entidades.csv","entregas/web/recursos",overwrite=TRUE)
  for(v in c("mathjax-3.2.2","fuse-6.4.6")) {
    js<-if(startsWith(v,"mathjax"))"tex-svg.js" else "fuse.min.js"
    file.copy(file.path("libro/estilos/vendor",v,js),"entregas/web/recursos",overwrite=TRUE)
    file.copy(file.path("libro/estilos/vendor",v,"LICENSE"),file.path("entregas/web/recursos",paste0("LICENSE-",if(startsWith(v,"mathjax"))"MathJax" else "Fuse",".txt")),overwrite=TRUE)
  }
  for(page in list.files("entregas/web",pattern="\\.html$",full.names=TRUE)) {
    h<-readLines(page,encoding="UTF-8",warn=FALSE)
    h<-gsub("https://cdn.jsdelivr.net/npm/fuse.js@6.4.6/dist/fuse.min.js","recursos/fuse.min.js",h,fixed=TRUE)
    h<-gsub("https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.9/latest.js?config=TeX-MML-AM_CHTML","recursos/tex-svg.js",h,fixed=TRUE)
    writeLines(sub("[[:blank:]]+$","",h),page,useBytes=TRUE)
  }
  file.copy("entregas/pdf/PAPIME-B02-capitulo-I.pdf","entregas/web/PAPIME-B02-capitulo-I.pdf",overwrite=TRUE)
  file.copy("entregas/pdf/PAPIME-libro-avance-B02.pdf","entregas/web/papime-libro.pdf",overwrite=TRUE)
}
writeLines(sub("[[:blank:]]+$","",capture.output(sessionInfo())),"seguimiento/compilacion-B02-sessionInfo.txt")
cat("B02 compilado:",modo,"\n")
