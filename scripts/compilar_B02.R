# Edición web B02; generadores y PDF históricos permanecen como antecedentes.
args <- commandArgs(trailingOnly=FALSE)
archivo <- sub("^--file=","",args[grepl("^--file=",args)])
raiz <- normalizePath(file.path(dirname(archivo),".."),winslash="/",mustWork=TRUE)
setwd(raiz)
invisible(suppressWarnings(Sys.setlocale("LC_CTYPE","Spanish_Mexico.utf8")))
.libPaths(c(".local/R",Sys.getenv("PAPIME_R_LIBRARY"),"C:/Users/marce/AppData/Local/R/win-library/4.6",.libPaths()))
if(!requireNamespace("bookdown",quietly=TRUE))stop("Consulte seguimiento/REPRODUCIBILIDAD_B02.md")
if(!nzchar(Sys.getenv("RSTUDIO_PANDOC")))Sys.setenv(RSTUDIO_PANDOC="C:/Program Files/RStudio/resources/app/bin/quarto/bin/tools")
modo <- commandArgs(trailingOnly=TRUE)
modo <- if(length(modo))modo[1] else "web"
if(!modo %in% c("web","todo"))stop("La edición vigente compila HTML: use web. Un nuevo PDF requiere encargo expreso (D25).")
python <- Sys.getenv("PAPIME_PYTHON")
runtime <- "C:/Program Files/WindowsApps/OpenAI.CodexPrimaryRuntime.v26-1105-1297-0_26.1105.1297.0_x64__3k8sg7r9htsxt/dependencies/python/python.exe"
if(!nzchar(python))python<-if(file.exists(runtime))runtime else Sys.which("python")
if(!nzchar(python))stop("Defina PAPIME_PYTHON con Python 3")
run <- function(bin,script) {
  result<-system2(bin,shQuote(script))
  if(result!=0)stop("Falló ",script)
}
run(file.path(R.home("bin"),"Rscript.exe"),"analisis/capitulo-01/generar_fisico_web.R")
run(python,"analisis/capitulo-01/generar_recursos_web.py")
run(python,"analisis/capitulo-01/generar_agua_mecanismos_web.py")
setwd(file.path(raiz,"libro"))
bookdown::render_book("index.Rmd","bookdown::gitbook",config_file="_bookdown-web.yml",quiet=TRUE)
setwd(raiz)
dir.create("entregas/web/recursos",recursive=TRUE,showWarnings=FALSE)
elements<-list.files("libro/_book-web",recursive=TRUE,all.files=TRUE,no..=TRUE)
elements<-elements[!grepl("\\.(pdf|tex)$|reference-keys\\.txt$",elements,ignore.case=TRUE)]
for(relative in elements) {
  target<-file.path("entregas/web",relative)
  dir.create(dirname(target),recursive=TRUE,showWarnings=FALSE)
  if(!file.copy(file.path("libro/_book-web",relative),target,overwrite=TRUE))stop("Falló la copia de ",relative)
}
for(folder in c("interactivos","tablas")) {
  files<-list.files(file.path("assets/capitulo-01",folder),full.names=TRUE)
  files<-files[grepl("\\.(html|csv|json)$",files,ignore.case=TRUE)]
  if(!all(file.copy(files,"entregas/web/recursos",overwrite=TRUE)))stop("Falló la copia de recursos")
}
file.copy("assets/capitulo-02/interactivos/F07-ksi.html","entregas/web/recursos",overwrite=TRUE)
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
run(python,"scripts/limpiar_entrega_web.py")
writeLines(sub("[[:blank:]]+$","",capture.output(sessionInfo())),"seguimiento/compilacion-B02-sessionInfo.txt")
cat("B02 web compilado sin generación ni copia de PDF.\n")
