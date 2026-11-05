# Capítulo II, inciso 2. Medición de la especialización
# México, 2024. Valor agregado a precios de 2018.
# KSI e ICE: distancia absoluta sin dividir entre dos. IEE: cociente de localización.

ruta_excel <- "C:/Users/marce/Downloads/PIBE/PIBE_2024_In.xlsx"
carpeta_salida <- file.path(dirname(ruta_excel), "Figuras_Capitulo_II_Especializacion_2024")
carpeta_geografia <- file.path(dirname(ruta_excel), "Cartografia_INEGI")
ruta_cartografia <- ""
crear_mapas <- TRUE
guardar_pdf <- TRUE
n_destacados <- 5L
fuente <- "Fuente: elaboración propia con base en datos de INEGI (2026). PIBE 2024, precios de 2018."
# Se conserva el año de consulta indicado en el script original.

paquetes <- c("readxl", "dplyr", "tidyr", "ggplot2", "scales", "stringr",
              "ggrepel", "ragg")
faltantes <- paquetes[!vapply(paquetes, requireNamespace, logical(1), quietly = TRUE)]
if (length(faltantes)) install.packages(faltantes, repos = "https://cloud.r-project.org")
if (!all(vapply(paquetes, requireNamespace, logical(1), quietly = TRUE))) {
  stop("Faltan paquetes. Revisa los mensajes de instalación.")
}
suppressPackageStartupMessages({library(dplyr); library(tidyr); library(ggplot2)})
options(scipen = 999, timeout = max(120, getOption("timeout")))
if (!file.exists(ruta_excel)) stop("No se encontró el Excel: ", ruta_excel)
dir.create(carpeta_salida, recursive = TRUE, showWarnings = FALSE)
normalizar <- function(x) tolower(iconv(stringr::str_squish(x), to = "ASCII//TRANSLIT"))
comprobar <- function(condicion, mensaje) {
  if (!isTRUE(condicion)) stop(mensaje, call. = FALSE)
}
comparar <- function(a, b, mensaje, tolerancia = 1e-8) {
  comprobar(length(a) == length(b) && all(is.finite(a)) && all(is.finite(b)),
            paste(mensaje, "contiene datos incompletos."))
  comprobar(max(abs(as.numeric(a) - as.numeric(b))) <= tolerancia,
            paste(mensaje, "no coincide."))
}

# 1. Matriz original. No se usan los índices precalculados como insumo.
hojas <- readxl::excel_sheets(ruta_excel)
hoja <- hojas[normalizar(gsub("_", " ", hojas)) == "indices krugman"]
comprobar(length(hoja) == 1, "No se encontró una única hoja Indices_Krugman.")
tabla <- readxl::read_excel(ruta_excel, sheet = hoja, range = "A1:W34",
  col_types = c("text", rep("numeric", 22)), .name_repair = "minimal")
comprobar(nrow(tabla) == 33 && ncol(tabla) == 23, "Se esperan 32 entidades y el total nacional.")
comprobar(normalizar(tabla[[1]][33]) == "estados unidos mexicanos", "Falta la fila nacional.")
comprobar(length(unique(tabla[[1]][1:32])) == 32, "Hay entidades repetidas.")
sectores <- tibble(
  codigo = c("11", "21-1", "21-2", "22", "23", "31-33", "43", "46", "48-49",
             "51", "52", "53", "54", "55", "56", "61", "62", "71", "72", "81", "93"),
  etiqueta = c(
    "11 Agricultura, ganadería, pesca y actividades forestales",
    "21-1 Minería petrolera", "21-2 Minería no petrolera",
    "22 Electricidad, agua y gas", "23 Construcción", "31-33 Manufacturas",
    "43 Comercio al por mayor", "46 Comercio al por menor",
    "48-49 Transportes, correos y almacenamiento", "51 Información en medios masivos",
    "52 Servicios financieros y seguros", "53 Servicios inmobiliarios y alquiler",
    "54 Servicios profesionales, científicos y técnicos", "55 Corporativos",
    "56 Apoyo a negocios, residuos y remediación", "61 Servicios educativos",
    "62 Salud y asistencia social", "71 Esparcimiento, cultura y deporte",
    "72 Alojamiento y preparación de alimentos", "81 Otros servicios",
    "93 Actividades gubernamentales y legislativas"
  ),
  grupo = c("Primarias", rep("Secundarias", 5), rep("Terciarias", 15)),
  nombre_excel = names(tabla)[2:22]
)
codigos_excel <- stringr::str_trim(sub(" - .*", "", sectores$nombre_excel))
comprobar(identical(codigos_excel, sectores$codigo),
          "Cambió la selección u orden de los 21 sectores de la tabla.")

registro <- tibble(
  cve_ent = sprintf("%02d", 1:32),
  nombre = c("Aguascalientes", "Baja California", "Baja California Sur", "Campeche",
             "Coahuila de Zaragoza", "Colima", "Chiapas", "Chihuahua", "Ciudad de México",
             "Durango", "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", "México",
             "Michoacán de Ocampo", "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla",
             "Querétaro", "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco",
             "Tamaulipas", "Tlaxcala", "Veracruz de Ignacio de la Llave", "Yucatán", "Zacatecas"),
  nombre_corto = c("Aguascalientes", "Baja California", "Baja California Sur", "Campeche",
                   "Coahuila", "Colima", "Chiapas", "Chihuahua", "Ciudad de México",
                   "Durango", "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", "Estado de México",
                   "Michoacán", "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla",
                   "Querétaro", "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco",
                   "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"),
  abreviatura = c("Ags.", "B.C.", "B.C.S.", "Camp.", "Coah.", "Col.", "Chis.", "Chih.",
                 "CDMX", "Dgo.", "Gto.", "Gro.", "Hgo.", "Jal.", "Méx.", "Mich.", "Mor.",
                 "Nay.", "N.L.", "Oax.", "Pue.", "Qro.", "Q.Roo", "S.L.P.", "Sin.",
                 "Son.", "Tab.", "Tamps.", "Tlax.", "Ver.", "Yuc.", "Zac.")
)
posiciones <- match(normalizar(tabla[[1]][1:32]), normalizar(registro$nombre))
comprobar(!anyNA(posiciones), "Hay nombres de entidades que no se pudieron identificar.")
estados <- registro[posiciones, ]

X <- as.matrix(tabla[1:32, 2:22])
nacional <- as.numeric(unlist(tabla[33, 2:22], use.names = FALSE))
comprobar(all(is.finite(X)) && all(X >= 0) && all(is.finite(nacional)) && all(nacional > 0),
          "Hay celdas faltantes, negativas o sectores nacionales sin actividad.")
total_estado <- rowSums(X)
total_nacional <- sum(nacional)
comprobar(all(total_estado > 0), "Los totales estatales deben ser positivos.")
comparar(total_estado, tabla[[23]][1:32], "Totales estatales", 0.02)
comparar(total_nacional, tabla[[23]][33], "Total nacional", 0.02)
comparar(colSums(X), nacional, "Agregación territorial", 0.02)

s <- sweep(X, 1, total_estado, "/")       # s_ij = x_ij / x_i.
s_nacional <- nacional / total_nacional # s_j = x_.j / x_..
q <- sweep(X, 2, nacional, "/")          # q_ij = x_ij / x_.j
peso_estado <- total_estado / total_nacional # w_i = x_i. / x_..
IEE <- sweep(s, 2, s_nacional, "/")      # IEE_ij = s_ij / s_j = q_ij / w_i
diferencias <- sweep(s, 2, s_nacional, "-")
exceso_territorial <- sweep(q, 1, peso_estado, "-")
aportaciones_ksi <- abs(diferencias)
aportaciones_ice <- abs(exceso_territorial)
ksi <- rowSums(aportaciones_ksi)
ice <- colSums(aportaciones_ice)

comparar(rowSums(s), rep(1, 32), "Participaciones estatales")
comparar(colSums(q), rep(1, 21), "Participaciones territoriales")
comparar(IEE, sweep(q, 1, peso_estado, "/"), "Dos expresiones del IEE")
comparar(as.numeric(IEE %*% s_nacional), rep(1, 32), "Promedio sectorial ponderado del IEE")
comparar(as.numeric(crossprod(peso_estado, IEE)), rep(1, 21), "Promedio territorial ponderado del IEE")
comparar(sum(peso_estado * ksi), sum(s_nacional * ice), "Identidad ponderada KSI e ICE")
comprobar(all(ksi >= 0 & ksi <= 2) && all(ice >= 0 & ice <= 2), "KSI o ICE fuera de rango.")
comprobar(all(is.finite(IEE)) && all(IEE >= 0), "Hay IEE no válidos.")

# La comparación con resultados guardados es informativa; el cálculo no depende de ellos.
revision_excel <- tryCatch({
  k <- readxl::read_excel(ruta_excel, sheet = hoja, range = "W78:W109", col_names = FALSE, .name_repair = "minimal")[[1]]
  c <- unlist(readxl::read_excel(ruta_excel, sheet = hoja, range = "B147:V147", col_names = FALSE, .name_repair = "minimal"))
  comparar(ksi, as.numeric(k), "KSI guardado en Excel")
  comparar(ice, as.numeric(c), "ICE guardado en Excel")
  "KSI e ICE coinciden con los valores guardados en Excel."
}, error = function(e) paste("Se recalculó desde la matriz original.", conditionMessage(e)))
message(revision_excel)

estados$VAB <- total_estado
estados$peso <- peso_estado
estados$KSI <- ksi
sectores$ICE <- ice
sectores$participacion_nacional <- s_nacional
dimnames(X) <- dimnames(s) <- dimnames(q) <- dimnames(IEE) <-
  dimnames(diferencias) <- dimnames(aportaciones_ksi) <- dimnames(aportaciones_ice) <-
  list(estados$cve_ent, sectores$codigo)
datos <- expand.grid(cve_ent = estados$cve_ent, codigo = sectores$codigo,
                     KEEP.OUT.ATTRS = FALSE, stringsAsFactors = FALSE)
datos$VAB_sector <- as.vector(X)
datos$participacion_local <- as.vector(s)
datos$participacion_sector <- as.vector(q)
datos$IEE <- as.vector(IEE)
datos$diferencia_pp <- as.vector(diferencias) * 100
datos$aportacion_KSI <- as.vector(aportaciones_ksi)
datos$aportacion_ICE <- as.vector(aportaciones_ice)
datos <- datos %>% left_join(estados, by = "cve_ent") %>% left_join(sectores, by = "codigo")

# 2. Cuadros completos para reproducir el texto y consultar cada celda.
escribir_csv <- function(x, nombre) {
  write.csv(x, file.path(carpeta_salida, paste0(nombre, ".csv")),
            row.names = FALSE, fileEncoding = "UTF-8", na = "")
}
escribir_csv(estados %>% arrange(desc(KSI)), "KSI_entidades")
escribir_csv(sectores %>% arrange(desc(ICE)), "ICE_sectores")
escribir_csv(datos, "Indices_entidad_sector")
escribir_csv(cbind(entidad = estados$nombre, as.data.frame(IEE, check.names = FALSE)), "Matriz_IEE")
escribir_csv(sectores %>% select(codigo, etiqueta, nombre_excel), "Catalogo_sectores")

# Comparación de 21 actividades con la agregación usual de 20 sectores.
X20 <- cbind(X[, 1], rowSums(X[, 2:3, drop = FALSE]), X[, 4:21])
n20 <- c(nacional[1], sum(nacional[2:3]), nacional[4:21])
ksi20 <- rowSums(abs(sweep(sweep(X20, 1, total_estado, "/"), 2, n20 / total_nacional, "-")))
comprobar(all(ksi20 <= ksi + 1e-10), "La agregación aumentó el KSI: revisa el cálculo.")
sensibilidad <- estados %>% mutate(KSI_21 = ksi, KSI_20 = ksi20,
  diferencia = KSI_21 - KSI_20) %>% select(cve_ent, nombre_corto, KSI_21, KSI_20, diferencia)
escribir_csv(sensibilidad, "Sensibilidad_agregacion_minera")

# 3. Formato. Figuras PNG de 320 ppp y PDF vectoriales.
familia <- if (Sys.info()[["sysname"]] == "Windows") "Arial" else "sans"
azul <- "#00688B"; naranja <- "#CD6600"; morado <- "#571854"
form_indice <- scales::label_number(accuracy = 0.001, decimal.mark = ".")
form_pct <- scales::label_percent(accuracy = 0.1, decimal.mark = ".")
tema <- function() theme_minimal(base_size = 15, base_family = familia) + theme(
  panel.grid.minor = element_blank(), panel.grid.major.y = element_blank(),
  panel.grid.major.x = element_line(color = "#E3E3E3", linewidth = 0.3),
  plot.title = element_text(face = "bold", size = 17, color = "black"),
  plot.caption = element_text(size = 9, hjust = 0, margin = margin(t = 10)),
  plot.caption.position = "plot", plot.title.position = "plot", axis.text = element_text(color = "#222222", size = 14),
  legend.position = "bottom", strip.text = element_text(face = "bold", size = 12),
  plot.margin = margin(12, 20, 12, 12))
guardar <- function(p, nombre, ancho = 11, alto = 7) {
  ggsave(file.path(carpeta_salida, paste0(nombre, ".png")), p,
         width = ancho, height = alto, dpi = 320, device = ragg::agg_png, bg = "white", limitsize = FALSE)
  if (guardar_pdf) {
    dispositivo <- if (capabilities("cairo")) grDevices::cairo_pdf else grDevices::pdf
    ggsave(file.path(carpeta_salida, paste0(nombre, ".pdf")), p,
           width = ancho, height = alto, device = dispositivo, bg = "white", limitsize = FALSE)
  }
  message("Guardado: ", nombre)
}
orden_ksi <- estados$nombre_corto[order(ksi, decreasing = TRUE)]

# Figura II.2.1. KSI de todas las entidades.
p <- ggplot(estados, aes(KSI, reorder(nombre_corto, KSI))) +
  geom_col(fill = azul, width = 0.7) +
  geom_text(aes(label = form_indice(KSI)), hjust = -0.15, size = 4.2, family = familia) +
  scale_x_continuous(limits = c(0, 2), breaks = seq(0, 2, 0.25), expand = c(0, 0)) +
  labs(title = "Especialización productiva estatal en 2024",
       x = "KSI (0 a 2)", y = NULL, caption = fuente) + tema()
guardar(p, "01_KSI_entidades", 10, 10.7)

# Figura II.2.2. Diferencias con signo. Se muestran las cuatro mayores por entidad.
seleccion <- c("Campeche", "Coahuila", "Ciudad de México", "Jalisco")
d <- datos %>% filter(nombre_corto %in% seleccion) %>% group_by(cve_ent) %>%
  slice_max(aportacion_KSI, n = 4, with_ties = FALSE) %>% ungroup() %>%
  mutate(panel = factor(nombre_corto, levels = seleccion),
         item = paste(nombre_corto, etiqueta, sep = "::"),
         signo = ifelse(diferencia_pp >= 0, "Mayor peso local", "Menor peso local"))
p <- ggplot(d, aes(diferencia_pp, reorder(item, diferencia_pp), fill = signo)) +
  geom_vline(xintercept = 0, linewidth = 0.3) + geom_col(width = 0.65) +
  geom_text(aes(label = sprintf("%+.1f", diferencia_pp),
                hjust = ifelse(diferencia_pp >= 0, -0.12, 1.12)), size = 4.4, family = familia) +
  facet_wrap(~panel, ncol = 2, scales = "free_y") +
  scale_y_discrete(labels = function(z) {
    cod <- sub(" .*", "", sub(".*::", "", z))
    breve <- c("11" = "Agricultura y afines", "21-1" = "Minería petrolera", "23" = "Construcción",
      "31-33" = "Manufacturas", "43" = "Comercio mayorista", "46" = "Comercio minorista",
      "51" = "Información", "52" = "Servicios financieros", "53" = "Inmobiliarios", "54" = "Servicios profesionales")
    unname(breve[cod])
  }) +
  scale_fill_manual(values = c("Mayor peso local" = naranja, "Menor peso local" = azul), name = NULL) +
  scale_x_continuous(limits = c(-45, 90), breaks = c(-25, 0, 25, 50, 75)) +
  labs(title = "Diferencias respecto de la estructura nacional",
       x = "Participación estatal menos participación nacional (puntos porcentuales)", y = NULL,
       caption = paste("Cuatro mayores diferencias absolutas por entidad. El KSI suma las 21 actividades.", fuente, sep = "\n")) + tema() +
  theme(axis.text.y = element_text(size = 13), panel.spacing.x = grid::unit(0.6, "cm"))
guardar(p, "02_Diferencias_sectoriales_KSI", 11, 7.8)

# Figura II.2.3. El ICE es un valor por sector, no por entidad.
p <- ggplot(sectores, aes(ICE, reorder(etiqueta, ICE))) +
  geom_col(fill = morado, width = 0.7) +
  geom_text(aes(label = form_indice(ICE)), hjust = -0.15, size = 4.2, family = familia) +
  scale_y_discrete(labels = function(z) stringr::str_wrap(z, 44)) +
  scale_x_continuous(limits = c(0, 2), breaks = seq(0, 2, 0.25), expand = c(0, 0)) +
  labs(title = "Concentración espacial de las actividades en 2024",
       x = "ICE (0 a 2)", y = NULL, caption = fuente) + tema()
guardar(p, "03_ICE_sectores", 10, 9.5)

# Material complementario. Comparación territorial que da origen al ICE.
d <- lapply(c("21-1", "55"), function(cod) {
  a <- datos %>% filter(codigo == cod) %>% arrange(desc(participacion_sector))
  bind_rows(a %>% slice_head(n = 5) %>% select(nombre_corto, participacion_sector, peso),
    a %>% slice(6:n()) %>% summarise(nombre_corto = "Resto de entidades",
      participacion_sector = sum(participacion_sector), peso = sum(peso))) %>%
    mutate(panel = a$etiqueta[1], item = paste(cod, nombre_corto, sep = "::"))
}) %>% bind_rows()
p <- ggplot(d, aes(y = reorder(item, participacion_sector))) +
  geom_segment(aes(x = peso, xend = participacion_sector, yend = reorder(item, participacion_sector)), color = "grey70") +
  geom_point(aes(x = participacion_sector, color = "Participación en el sector"), size = 3) +
  geom_point(aes(x = peso, color = "Peso económico estatal"), size = 3) +
  facet_wrap(~panel, ncol = 2, scales = "free_y") +
  scale_y_discrete(labels = function(z) sub(".*::", "", z)) +
  scale_color_manual(values = c("Participación en el sector" = morado, "Peso económico estatal" = naranja), name = NULL) +
  scale_x_continuous(labels = form_pct, limits = c(0, 1)) +
  labs(title = "Distribución de la actividad y peso de las entidades",
       x = "Participación nacional", y = NULL, caption = fuente) + tema()
guardar(p, "04_Distribucion_territorial_ICE", 13, 6)

# Figura II.2.4. Matriz completa de IEE, sin rótulos dentro de las celdas.
# Degradado continuo azul a rojo oscuro y una barra horizontal común.
# log(1 + IEE) comprime el color, conserva los ceros y no altera los índices.
limite_iee <- max(24, ceiling(max(datos$IEE)))
puntos_iee <- c(0, 0.5, 1, 2, 4, 8, limite_iee)
paleta_iee <- c("#244A73", "#7DA5BD", "#F4F0EA", "#DDB1A8",
                "#C4787C", "#A44759", "#681D32")
escala_iee <- function() scale_fill_gradientn(
  colors = paleta_iee, values = log1p(puntos_iee) / log1p(limite_iee),
  trans = "log1p", limits = c(0, limite_iee),
  breaks = c(0, 0.5, 1, 2, 4, 8, 16, 24),
  labels = c("0", "0.5", "1", "2", "4", "8", "16", "24"),
  name = "IEE · Referencia nacional = 1",
  guide = guide_colorbar(direction = "horizontal", title.position = "top", title.hjust = 0.5,
    barwidth = grid::unit(14, "cm"), barheight = grid::unit(0.45, "cm"), nbin = 512,
    ticks.colour = "#F4F0EA", frame.colour = NA))
etiquetas_cortas <- c("11 Agropecuario", "21-1 Petróleo", "21-2 Otra minería",
  "22 Energía y agua", "23 Construcción", "31-33 Manufacturas", "43 Mayoreo",
  "46 Menudeo", "48-49 Transportes", "51 Información", "52 Finanzas",
  "53 Inmobiliarios", "54 Profesionales", "55 Corporativos", "56 Apoyo a negocios",
  "61 Educación", "62 Salud", "71 Esparcimiento", "72 Alojamiento y alimentos",
  "81 Otros servicios", "93 Gobierno")
d <- datos %>% mutate(
  entidad = factor(nombre_corto, levels = rev(registro$nombre_corto)),
  actividad = factor(codigo, levels = sectores$codigo))
comprobar(nrow(d) == 32 * 21 && all(is.finite(d$IEE)), "La matriz de IEE no está completa.")
p <- ggplot(d, aes(actividad, entidad, fill = IEE)) +
  geom_tile(color = "white", linewidth = 0.42, width = 0.98, height = 0.98) +
  escala_iee() + scale_x_discrete(labels = etiquetas_cortas, expand = c(0, 0)) +
  scale_y_discrete(expand = c(0, 0)) +
  labs(title = "Especialización productiva en las 32 entidades",
       x = NULL, y = NULL,
       caption = paste("Matriz completa: 32 entidades y 21 actividades. Color continuo en escala log(1 + IEE).",
                       fuente, sep = "\n")) +
  tema() + theme(panel.grid = element_blank(), plot.title = element_text(size = 15),
    axis.text.y = element_text(size = 12),
    axis.text.x = element_text(size = 10.7, angle = 60, hjust = 1, vjust = 1),
    axis.ticks = element_blank(), legend.title = element_text(size = 11.5),
    legend.text = element_text(size = 10.3), legend.key.width = grid::unit(0.45, "cm"),
    legend.key.height = grid::unit(0.38, "cm"), legend.spacing.x = grid::unit(0.16, "cm"),
    plot.caption = element_text(size = 8.5, lineheight = 1.15),
    plot.margin = margin(12, 12, 12, 10))
guardar(p, "05_Matriz_IEE_completa", 8.8, 11.2)

d <- sensibilidad %>% arrange(desc(diferencia)) %>% slice_head(n = 8) %>%
  pivot_longer(c(KSI_21, KSI_20), names_to = "agregacion", values_to = "KSI")
p <- ggplot(d, aes(KSI, reorder(nombre_corto, diferencia), color = agregacion)) +
  geom_point(size = 3.5) +
  scale_color_manual(values = c(KSI_21 = naranja, KSI_20 = azul),
                     labels = c(KSI_21 = "Minería separada (21 actividades)", KSI_20 = "Minería agregada (20 sectores)"), name = NULL) +
  labs(title = "El nivel de agregación modifica la medición",
       x = "KSI", y = NULL, caption = paste("Ocho entidades con mayor diferencia. Se conserva toda la actividad económica.", fuente, sep = "\n")) + tema()
guardar(p, "07_Sensibilidad_agregacion", 11, 6.5)

# 4. Mapas de índices, exclusivamente con límites estatales del INEGI.
# No hay capas físicas, ríos, relieve ni un mapa de ICE por estado.
if (crear_mapas) {
  if (!requireNamespace("sf", quietly = TRUE)) install.packages("sf", repos = "https://cloud.r-project.org")
  tryCatch({
    comprobar(requireNamespace("sf", quietly = TRUE), "No se pudo instalar sf.")
    dir.create(carpeta_geografia, recursive = TRUE, showWarnings = FALSE)
    archivo_geo <- if (nzchar(ruta_cartografia)) ruta_cartografia else
      file.path(carpeta_geografia, "entidades_INEGI.geojson")
    if (!file.exists(archivo_geo)) {
      temporal <- tempfile(fileext = ".geojson")
      utils::download.file("https://gaia.inegi.org.mx/wscatgeo/v2/geo/mgee/", temporal,
                           mode = "wb", quiet = TRUE, method = "libcurl")
      comprobar(file.copy(temporal, archivo_geo, overwrite = TRUE), "No se guardó la cartografía.")
      unlink(temporal)
    }
    geo <- sf::st_read(archivo_geo, quiet = TRUE, stringsAsFactors = FALSE)
    campos <- tolower(names(geo))
    pos <- match("cve_ent", campos)
    if (is.na(pos)) pos <- match("cvegeo", campos)
    comprobar(!is.na(pos), "La cartografía necesita cve_ent o cvegeo.")
    geo$cve_ent <- sprintf("%02d", as.integer(as.character(geo[[pos]])))
    comprobar(setequal(unique(geo$cve_ent), registro$cve_ent), "La cartografía debe cubrir las 32 entidades.")
    if (is.na(sf::st_crs(geo))) {
      comprobar(tolower(tools::file_ext(archivo_geo)) %in% c("geojson", "json"), "Falta el CRS de la cartografía.")
      sf::st_crs(geo) <- 4326
    }
    crs_mexico <- "+proj=lcc +lat_1=17.5 +lat_2=29.5 +lat_0=12 +lon_0=-102 +datum=WGS84 +units=m +no_defs"
    geo <- geo %>% select(cve_ent)
    geo <- sf::st_transform(sf::st_make_valid(sf::st_zm(geo)), crs_mexico)
    geo <- geo %>% group_by(cve_ent) %>% summarise(.groups = "drop")
    comprobar(nrow(geo) == 32 && !any(sf::st_is_empty(geo)), "Hay geometrías faltantes.")
    # Simplificación visual de 300 m: no modifica los datos ni las claves estatales.
    geo <- sf::st_simplify(geo, dTolerance = 300, preserveTopology = TRUE)
    # Un archivo por mapa. Los contornos se conservan y no hay ejes geográficos.
    borde_nacional <- sf::st_union(geo)
    tema_mapa <- function() theme_void(base_size = 15, base_family = familia) + theme(
      plot.title = element_text(face = "bold", size = 21, color = "#24313A", hjust = 0),
      plot.title.position = "plot", plot.caption.position = "plot",
      plot.caption = element_text(size = 10, color = "#4D5961", hjust = 0,
                                  margin = margin(t = 12), lineheight = 1.2),
      legend.position = "bottom", legend.title = element_text(size = 13),
      legend.text = element_text(size = 12), legend.key.width = grid::unit(0.55, "cm"),
      legend.key.height = grid::unit(0.4, "cm"),
      legend.spacing.x = grid::unit(0.2, "cm"),
      plot.background = element_rect(fill = "white", color = NA),
      plot.margin = margin(18, 24, 16, 24))
    centros <- sf::st_coordinates(sf::st_point_on_surface(sf::st_geometry(geo)))
    posiciones <- data.frame(cve_ent = geo$cve_ent, x = centros[, 1], y = centros[, 2])
    mapa <- geo %>% left_join(estados, by = "cve_ent")
    etiquetas_ksi <- estados %>% slice_max(KSI, n = n_destacados, with_ties = FALSE) %>%
      left_join(posiciones, by = "cve_ent")
    p <- ggplot(mapa) + geom_sf(aes(fill = KSI), color = "#45414B", linewidth = 0.22) +
      geom_sf(data = borde_nacional, fill = NA, color = "#39343F", linewidth = 0.32) +
      scale_fill_gradientn(
        colors = c("#244A73", "#6C94B0", "#B7CBD7", "#F4F0EA", "#DAB6AF", "#B65E6B", "#681D32"),
        values = seq(0, 1, length.out = 7), limits = c(0, 2),
        name = "KSI", breaks = c(0, 0.25, 0.5, 0.75, 1, 1.5, 2),
        guide = guide_colorbar(direction = "horizontal", title.position = "top", title.hjust = 0.5,
          barwidth = grid::unit(14, "cm"), barheight = grid::unit(0.45, "cm"), nbin = 512,
          ticks.colour = "#F4F0EA", frame.colour = NA)) +
      ggrepel::geom_label_repel(data = etiquetas_ksi,
        aes(x = x, y = y, label = paste0(abreviatura, " ", sprintf("%.3f", KSI))),
        inherit.aes = FALSE, size = 4.7, family = familia, seed = 2024,
        max.overlaps = Inf, box.padding = 0.55, point.padding = 0.3,
        min.segment.length = 0, fill = "white", color = "#263D35", label.size = 0.15,
        segment.color = "#526E64", segment.size = 0.35) +
      coord_sf(datum = NA, expand = TRUE) +
      labs(title = "Especialización productiva estatal en 2024",
           caption = paste("Cinco entidades con mayor KSI. Escala de 0 a 2; un valor mayor indica más distancia respecto del país.",
                           fuente, sep = "\n")) + tema_mapa()
    guardar(p, "08_Mapa_KSI", 12, 8.6)

    # Figuras II.2.5 a II.2.8. Escala común y archivos separados para cada actividad.
    cod_mapa <- c("21-1", "31-33", "52", "72")
    titulos <- c("Minería petrolera", "Manufacturas", "Servicios financieros", "Alojamiento y alimentos")
    archivos <- c("09_IEE_mineria_petrolera", "10_IEE_manufacturas",
                  "11_IEE_servicios_financieros", "12_IEE_alojamiento_alimentos")
    for (k in seq_along(cod_mapa)) {
      d <- datos %>% filter(codigo == cod_mapa[k])
      mapas <- geo %>% left_join(d, by = "cve_ent")
      etiquetas <- d %>% slice_max(IEE, n = n_destacados, with_ties = FALSE) %>%
        left_join(posiciones, by = "cve_ent")
      p <- ggplot(mapas) + geom_sf(aes(fill = IEE), color = "#42494C", linewidth = 0.22) +
        geom_sf(data = borde_nacional, fill = NA, color = "#30383A", linewidth = 0.32) +
        escala_iee() +
        ggrepel::geom_label_repel(data = etiquetas,
          aes(x = x, y = y, label = paste0(abreviatura, " ", sprintf("%.2f", IEE))),
          inherit.aes = FALSE, size = 4.7, family = familia, seed = 2024,
          max.overlaps = Inf, box.padding = 0.5, point.padding = 0.3,
          min.segment.length = 0, fill = "white", color = "#263D35", label.size = 0.15,
          segment.color = "#526E64", segment.size = 0.35) +
        coord_sf(datum = NA, expand = TRUE) +
        labs(title = paste0(titulos[k], " en 2024"),
             caption = paste("Se señalan los cinco IEE más elevados. Color continuo en escala log(1 + IEE).",
                             fuente, sep = "\n")) + tema_mapa()
      guardar(p, archivos[k], 12, 8.6)
    }
  }, error = function(e) {
    aviso <- paste("No se generaron todos los mapas:", conditionMessage(e),
      "Las tablas y gráficas anteriores ya están guardadas. Revisa ruta_cartografia y vuelve a ejecutar.")
    warning(aviso, call. = FALSE)
    writeLines(aviso, file.path(carpeta_salida, "Aviso_cartografia.txt"), useBytes = TRUE)
  })
}

writeLines(c(
  "Medición de la especialización. México, 2024.",
  "Fuente de todos los cálculos: Indices_Krugman, A1:W34; matriz de 32 por 21 actividades.",
  "Unidad de origen: millones de pesos de 2018. Denominadores: sumas sectoriales de valor agregado.",
  "KSI_i = sum_j abs(s_ij - s_j). ICE_j = sum_i abs(q_ij - w_i). Ambos sin factor 1/2.",
  "IEE_ij = (x_ij / x_i.) / (x_.j / x_..). El umbral de especialización relativa es 1.",
  "21-1 y 21-2 son códigos de apertura de esta tabla, no nuevos sectores SCIAN independientes.",
  "Las figuras 01, 02, 03 y 05 corresponden a II.2.1 a II.2.4 del texto.",
  "Los mapas 09 a 12 corresponden a II.2.5 a II.2.8; cada uno se guarda por separado.",
  "Cada mapa señala las cinco entidades con mayor índice: KSI en 08 e IEE en 09 a 12.",
  "Las figuras 04, 07 y 08 son material complementario.",
  "El mapa de calor incluye las 672 celdas, sin cifras impresas. Los valores exactos están en los CSV.",
  "El mapa de calor y todos los mapas del IEE comparten un degradado continuo azul a rojo oscuro.",
  "La barra horizontal inferior muestra los valores originales del índice; el color usa log(1 + IEE).",
  "El azul corresponde a valores inferiores a uno; el tono claro señala uno y el rojo indica valores superiores.",
  "El cero conserva el extremo azul. El KSI utiliza un degradado continuo con su escala de cero a dos.",
  "IEE = 0 conserva los ceros observados. Los datos faltantes detienen el cálculo.",
  "KSI bajo indica semejanza al país; no demuestra por sí solo diversificación absoluta.",
  "ICE bajo indica distribución proporcional al peso económico estatal; no implica reparto igual entre estados.",
  "Referencias: Krugman (1991), Geography and Trade; Hoover (1936), doi:10.2307/1927875;",
  "Lira y Quiroga (2009), Técnicas de análisis regional, CEPAL, Manuales 59;",
  "Hildebrand y Mace (1950), doi:10.2307/2937531, antecedente del cociente de localización.",
  revision_excel,
  paste("Identidad ponderada KSI e ICE:", format(sum(peso_estado * ksi), digits = 12))
), file.path(carpeta_salida, "Guia_de_figuras_y_calculos.txt"), useBytes = TRUE)
capture.output(sessionInfo(), file = file.path(carpeta_salida, "Sesion_R.txt"))
message("Terminado. Resultados guardados en: ", normalizePath(carpeta_salida, winslash = "/"))
