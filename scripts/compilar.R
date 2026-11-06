# Punto de entrada de la edición vigente. El piloto B01 se conserva en compilar_B01.R.
args<-commandArgs(trailingOnly=FALSE)
file<-sub("^--file=","",args[grepl("^--file=",args)])
source(file.path(dirname(normalizePath(file,winslash="/")),"compilar_B02.R"),encoding="UTF-8")
