# PAPIME B01 / F07-KSI. Ejecutar desde la raíz del repositorio:
# Rscript --vanilla analisis/capitulo-02/preparar_especializacion.R
# Sin descargas ni paquetes externos. Matriz 2024 a precios de 2018.
options(scipen = 999, digits = 16)
if (.Platform$OS.type == "windows") {
  suppressWarnings(Sys.setlocale("LC_CTYPE", "Spanish_Mexico.utf8"))
}
raiz <- normalizePath(".", winslash = "/", mustWork = TRUE)
insumo <- file.path(raiz, "datos", "originales", "especializacion", "Matriz_original_Indices_Krugman.csv")
stopifnot(file.exists(insumo))
salida <- file.path(raiz, "datos", "preparados", "capitulo-02")
tablas <- file.path(raiz, "assets", "capitulo-02", "tablas")
figuras <- file.path(raiz, "assets", "capitulo-02", "figuras-estaticas")
for (p in c(salida, tablas, figuras)) dir.create(p, recursive = TRUE, showWarnings = FALSE)
tabla <- read.csv(insumo, check.names = FALSE, fileEncoding = "UTF-8", stringsAsFactors = FALSE)
asegurar <- function(condicion, texto) if (!isTRUE(condicion)) stop(texto, call. = FALSE)
comparar <- function(a, b, texto, tol = 1e-8) {
  asegurar(length(a) == length(b) && all(is.finite(a)) && all(is.finite(b)), paste(texto, "contiene datos inválidos"))
  asegurar(max(abs(as.numeric(a) - as.numeric(b))) <= tol, paste(texto, "no coincide"))
}
asegurar(nrow(tabla) == 33L && ncol(tabla) == 23L, "La tabla debe contener 32 entidades, total nacional y 21 actividades")
asegurar(tabla[33, 1] == "Estados Unidos Mexicanos", "Falta la fila nacional")
codigos <- c("11", "21-1", "21-2", "22", "23", "31-33", "43", "46", "48-49", "51", "52", "53", "54", "55", "56", "61", "62", "71", "72", "81", "93")
asegurar(identical(sub(" - .*", "", names(tabla)[2:22]), codigos), "Cambió el orden o la selección de actividades")
estados <- data.frame(cve_ent = sprintf("%02d", 1:32), nombre = tabla[1:32, 1], stringsAsFactors = FALSE)
estados$nombre_corto <- c("Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Coahuila", "Colima", "Chiapas", "Chihuahua", "Ciudad de México", "Durango", "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", "Estado de México", "Michoacán", "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas")
estados$abreviatura <- c("Ags.", "B.C.", "B.C.S.", "Camp.", "Coah.", "Col.", "Chis.", "Chih.", "CDMX", "Dgo.", "Gto.", "Gro.", "Hgo.", "Jal.", "Méx.", "Mich.", "Mor.", "Nay.", "N.L.", "Oax.", "Pue.", "Qro.", "Q.Roo", "S.L.P.", "Sin.", "Son.", "Tab.", "Tamps.", "Tlax.", "Ver.", "Yuc.", "Zac.")
# El orden estatal se verifica contra el registro conservado, sin unir nombres abreviados.
esperados <- c("Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Coahuila de Zaragoza", "Colima", "Chiapas", "Chihuahua", "Ciudad de México", "Durango", "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", "México", "Michoacán de Ocampo", "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz de Ignacio de la Llave", "Yucatán", "Zacatecas")
asegurar(identical(estados$nombre, esperados), "Cambió el orden o la denominación de entidades")
etiquetas <- c("11 Agricultura, ganadería, pesca y actividades forestales", "21-1 Minería petrolera", "21-2 Minería no petrolera", "22 Electricidad, agua y gas", "23 Construcción", "31-33 Manufacturas", "43 Comercio al por mayor", "46 Comercio al por menor", "48-49 Transportes, correos y almacenamiento", "51 Información en medios masivos", "52 Servicios financieros y seguros", "53 Servicios inmobiliarios y alquiler", "54 Servicios profesionales, científicos y técnicos", "55 Corporativos", "56 Apoyo a negocios, residuos y remediación", "61 Servicios educativos", "62 Salud y asistencia social", "71 Esparcimiento, cultura y deporte", "72 Alojamiento y preparación de alimentos", "81 Otros servicios", "93 Actividades gubernamentales y legislativas")
sectores <- data.frame(codigo = codigos, etiqueta = etiquetas, grupo = c("Primarias", rep("Secundarias", 5), rep("Terciarias", 15)), nombre_excel = names(tabla)[2:22], stringsAsFactors = FALSE)
X <- as.matrix(tabla[1:32, 2:22])
storage.mode(X) <- "double"
nacional <- as.numeric(unlist(tabla[33, 2:22], use.names = FALSE))
asegurar(all(is.finite(X)) && all(X >= 0) && all(is.finite(nacional)) && all(nacional > 0), "Celdas faltantes, negativas o sectores nacionales nulos")
total_estado <- rowSums(X)
total_nacional <- sum(nacional)
asegurar(all(total_estado > 0), "Hay un total estatal no positivo")
comparar(total_estado, tabla[1:32, 23], "Totales estatales", 0.02)
comparar(total_nacional, tabla[33, 23], "Total nacional", 0.02)
comparar(colSums(X), nacional, "Agregación territorial", 0.02)
s <- sweep(X, 1, total_estado, "/")
sn <- nacional / total_nacional
q <- sweep(X, 2, nacional, "/")
w <- total_estado / total_nacional
iee <- sweep(s, 2, sn, "/")
brechas <- sweep(s, 2, sn, "-")
ak <- abs(brechas)
ac <- abs(sweep(q, 1, w, "-"))
ksi <- rowSums(ak)
ice <- colSums(ac)
comparar(rowSums(s), rep(1, 32), "Participaciones estatales")
comparar(colSums(q), rep(1, 21), "Participaciones territoriales")
comparar(iee, sweep(q, 1, w, "/"), "Expresiones equivalentes del IEE")
comparar(as.numeric(iee %*% sn), rep(1, 32), "Promedio sectorial del IEE")
comparar(as.numeric(crossprod(w, iee)), rep(1, 21), "Promedio territorial del IEE")
comparar(sum(w * ksi), sum(sn * ice), "Identidad ponderada KSI/ICE")
asegurar(all(ksi >= 0 & ksi <= 2 * (1 - w) + 1e-10) && all(ice >= 0 & ice <= 2), "Distancia fuera de límites")
asegurar(all(is.finite(iee)) && all(iee >= 0), "IEE inválido")
estados$VAB <- total_estado
estados$peso <- w
estados$KSI <- ksi
sectores$ICE <- ice
sectores$participacion_nacional <- sn
dimnames(iee) <- list(estados$cve_ent, sectores$codigo)
datos <- expand.grid(cve_ent = estados$cve_ent, codigo = codigos, KEEP.OUT.ATTRS = FALSE, stringsAsFactors = FALSE)
datos$VAB_sector <- as.vector(X)
datos$participacion_local <- as.vector(s)
datos$participacion_sector <- as.vector(q)
datos$IEE <- as.vector(iee)
datos$diferencia_pp <- as.vector(brechas) * 100
datos$aportacion_KSI <- as.vector(ak)
datos$aportacion_ICE <- as.vector(ac)
datos <- cbind(datos, estados[match(datos$cve_ent, estados$cve_ent), -1, drop = FALSE], sectores[match(datos$codigo, sectores$codigo), -1, drop = FALSE])
rownames(datos) <- NULL
X20 <- cbind(X[, 1], rowSums(X[, 2:3, drop = FALSE]), X[, 4:21])
n20 <- c(nacional[1], sum(nacional[2:3]), nacional[4:21])
ksi20 <- rowSums(abs(sweep(sweep(X20, 1, total_estado, "/"), 2, n20 / total_nacional, "-")))
asegurar(all(ksi20 <= ksi + 1e-10), "La agregación aumentó el KSI")
sensibilidad <- data.frame(cve_ent = estados$cve_ent, nombre_corto = estados$nombre_corto, KSI_21 = ksi, KSI_20 = ksi20, diferencia = ksi - ksi20)
productos <- list(KSI_entidades = estados[order(-ksi), ], ICE_sectores = sectores[order(-ice), ], Indices_entidad_sector = datos,
  Matriz_IEE = cbind(entidad = estados$nombre, as.data.frame(iee, check.names = FALSE)),
  Catalogo_sectores = sectores[, c("codigo", "etiqueta", "nombre_excel")], Sensibilidad_agregacion_minera = sensibilidad)
for (nombre in names(productos)) {
  for (carpeta in c(salida, tablas)) write.csv(productos[[nombre]], file.path(carpeta, paste0(nombre, ".csv")), row.names = FALSE, fileEncoding = "UTF-8", na = "")
}
# Contrastar índices con las tablas heredadas. Las tablas no intervienen en el cálculo.
previos <- file.path(raiz, "referencias", "antecedentes", "especializacion", "Figuras_Capitulo_II_Especializacion_2024")
if (dir.exists(previos)) {
  k0 <- read.csv(file.path(previos, "KSI_entidades.csv"), colClasses = c(cve_ent = "character"), fileEncoding = "UTF-8", check.names = FALSE)
  c0 <- read.csv(file.path(previos, "ICE_sectores.csv"), colClasses = c(codigo = "character"), fileEncoding = "UTF-8", check.names = FALSE)
  l0 <- read.csv(file.path(previos, "Indices_entidad_sector.csv"), colClasses = c(cve_ent = "character", codigo = "character"), fileEncoding = "UTF-8", check.names = FALSE)
  comparar(ksi, k0$KSI[match(estados$cve_ent, k0$cve_ent)], "KSI heredado")
  comparar(ice, c0$ICE[match(codigos, c0$codigo)], "ICE heredado")
  clave <- paste(datos$cve_ent, datos$codigo)
  comparar(datos$IEE, l0$IEE[match(clave, paste(l0$cve_ent, l0$codigo))], "672 IEE heredados")
}
# F07-KSI. Escala general [0, 2] común a estático y explorador.
# Azul editorial del antecedente de barras. Mapas mantienen su degradado azul-rojo.
dibujar <- function() {
  op <- par(mar = c(4.1, 9.4, 3.2, 1.4), mgp = c(2.0, 0.5, 0), tcl = -0.2, family = "Arial", cex = 0.9, xaxs = "i")
  on.exit(par(op))
  d <- estados[order(-estados$KSI), ]
  y <- rev(seq_len(nrow(d)))
  plot(NA, xlim = c(0, 2), ylim = c(0.35, 32.7), axes = FALSE, xlab = "KSI · suma de diferencias absolutas", ylab = "")
  abline(v = seq(0, 2, 0.25), col = "#E7E6E3", lwd = 0.6)
  rect(0, y - 0.32, d$KSI, y + 0.32, col = "#0F4761", border = NA)
  axis(1, at = seq(0, 2, 0.25), labels = format(seq(0, 2, 0.25), nsmall = 2), col = NA, col.ticks = "#777777", cex.axis = 0.9)
  axis(2, at = y, labels = d$nombre_corto, las = 1, tick = FALSE, cex.axis = 0.85)
  text(d$KSI + 0.025, y, labels = sprintf("%.3f", d$KSI), adj = 0, cex = 0.78, col = "#333333")
  title(main = "Especialización relativa de las entidades", adj = 0, cex.main = 1.2, col.main = "#24313A", line = 1.8)
  mtext("México 2024 · VAB a precios de 2018 · Referencia nacional", side = 3, adj = 0, line = 0.55, cex = 0.78, col = "#5B6167")
  mtext("Fuente: matriz PIBE de INEGI conservada en el proyecto. Cálculos propios.", side = 1, adj = 0, line = 3.0, cex = 0.68, col = "#5B6167")
}
png(file.path(figuras, "F07-ksi.png"), width = 2400, height = 3000, res = 300, type = "cairo", bg = "white")
dibujar()
dev.off()
if (capabilities("cairo")) {
  cairo_pdf(file.path(figuras, "F07-ksi.pdf"), width = 8, height = 10, family = "Arial", bg = "white")
} else {
  pdf(file.path(figuras, "F07-ksi.pdf"), width = 8, height = 10, family = "Helvetica", bg = "white", useDingbats = FALSE)
}
dibujar()
dev.off()
capture.output(sessionInfo(), file = file.path(salida, "Sesion_R.txt"))
message(sprintf("Comprobado: 32 KSI, 21 ICE, 672 IEE; VAB nacional %.3f; %d ceros. F07-KSI generado.", total_nacional, sum(X == 0)))
