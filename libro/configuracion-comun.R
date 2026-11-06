# Configuración compartida por el libro integrado y el capítulo I independiente.
knitr::opts_chunk$set(echo=FALSE, warning=FALSE, message=FALSE, fig.align="center", out.width="100%")
raiz <- ".."
ksi <- read.csv(file.path(raiz,"datos/preparados/capitulo-02/KSI_entidades.csv"), check.names=FALSE, colClasses=c(cve_ent="character"))
indices <- read.csv(file.path(raiz,"datos/preparados/capitulo-02/Indices_entidad_sector.csv"), check.names=FALSE, colClasses=c(cve_ent="character",codigo="character"))
fmt <- function(x,n=3) formatC(x,format="f",digits=n,decimal.mark=".")
camp <- subset(indices,cve_ent=="04" & codigo=="21-1")
coah <- subset(indices,cve_ent=="05" & codigo=="31-33")
stopifnot(nrow(ksi)==32L,nrow(indices)==672L,sum(indices$VAB_sector==0)==36L,
          abs(camp$participacion_local*100-61.1626123)<1e-6,
          abs(camp$participacion_nacional*100-2.6890540)<1e-6,
          abs(coah$IEE-2.156485985)<1e-8)
agua <- read.csv(file.path(raiz,"datos/preparados/capitulo-01/F03_F05_agua_poblacion_2022.csv"),check.names=FALSE)
stopifnot(nrow(agua)==13L, abs(sum(agua$agua_renovable_hm3_anio)-461640)<1e-7,
          abs(sum(agua$poblacion_millones)-129.35)<1e-8,
          abs(agua$porcentaje_agua[agua$rha=="XI"]-34.2303526558)<1e-8,
          round(agua$porcentaje_poblacion[agua$rha=="XI"],1)==6.4,
          round(agua$porcentaje_agua[agua$rha=="III"],1)==5.8,
          round(agua$porcentaje_poblacion[agua$rha=="III"],1)==3.7)
figuras_territorio <- c(F01="F01-relieve-localizacion",F02="F02-clima-suelos",
                       F03="F03-agua-renovable",F04="F04-recursos",
                       F05="F05-agua-poblacion",F06="F06-mecanismos-territoriales")
rotulos_territorio <- read.csv("figuras-capitulo-I.csv",check.names=FALSE)
figura_territorio <- function(id,titulo,alto=1000) {
  nombre <- unname(figuras_territorio[id])
  stopifnot(length(nombre)==1L,!is.na(nombre))
  rotulo <- rotulos_territorio[rotulos_territorio$id==id,]
  stopifnot(nrow(rotulo)==1L)
  if(knitr::is_html_output()) {
    cat(sprintf('<div id="%s"><p><strong>%s</strong></p>\n',rotulo$ancla,rotulo$titulo))
    cat(sprintf('<iframe class="grafico-interactivo territorio" src="recursos/%s.html" title="%s" style="height:%spx" loading="eager"></iframe>\n',nombre,titulo,alto))
    cat(sprintf('<p class="alternativa"><a href="recursos/%s.html">Abrir figura y tablas en ventana completa</a> · <a href="recursos/%s.pdf">Descargar figura estática en PDF</a></p>\n',nombre,nombre))
    cat(sprintf('<p class="fuente-figura">%s</p></div>\n',rotulo$fuente))
  } else {
    esc <- function(s) gsub("%","\\%",s,fixed=TRUE)
    cat("\n\\begin{figure}[!htbp]\\centering\n")
    cat(sprintf("\\hypertarget{%s}{}\\textbf{%s}\\par\n",rotulo$ancla,esc(rotulo$titulo)))
    if(id=="F04") {
      paneles <- c("F04-A-cobre","F04-B-cubierta","F04-C-madera","F04-D-pesca")
      for(i in seq_along(paneles)) {
        if(i>2) cat("\n\\end{figure}\n\\begin{figure}[!htbp]\\centering\n\\textbf{Figura I.2.4 (continuación)}\n")
        alto <- if(i<=2) ".36" else ".78"
        cat(sprintf("\n\\begin{center}\\includegraphics[width=\\linewidth,height=%s\\textheight,keepaspectratio]{../assets/capitulo-01/figuras-estaticas/%s.pdf}\\end{center}\n",alto,paneles[i]))
      }
    } else cat(sprintf("\n\\begin{center}\\includegraphics[width=\\linewidth,height=.78\\textheight,keepaspectratio]{../assets/capitulo-01/figuras-estaticas/%s.pdf}\\end{center}\n",nombre))
    cat(sprintf("\n{\\small %s}\\par\n",esc(rotulo$fuente)))
    cat("\\end{figure}\n")
  }
}
