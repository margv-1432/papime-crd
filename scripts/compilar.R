# Punto de entrada de la edición vigente. El piloto B01 se conserva en compilar_B01.R.
invisible(suppressWarnings(Sys.setlocale("LC_CTYPE","English_United States.utf8")))
args<-commandArgs(trailingOnly=FALSE)
file<-sub("^--file=","",args[grepl("^--file=",args)])
withCallingHandlers(source(file.path(dirname(normalizePath(file,winslash="/")),"compilar_B02.R"),encoding="UTF-8"),
  warning=function(w) if(grepl("invalid input",conditionMessage(w),fixed=TRUE))stop(w))
