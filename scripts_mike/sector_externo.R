library(pacman)
p_load(httr2, tidyverse, sf, siebanxicor, pheatmap)

{
regiones_mexico <- data.frame(
  CVE_ENT = 1:32,
  NOM_ENT = c(
    "Aguascalientes", "Baja California", "Baja California Sur", "Campeche",
    "Coahuila de Zaragoza", "Colima", "Chiapas", "Chihuahua",
    "Ciudad de México", "Durango", "Guanajuato", "Guerrero",
    "Hidalgo", "Jalisco", "México", "Michoacán de Ocampo",
    "Morelos", "Nayarit", "Nuevo León", "Oaxaca",
    "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí",
    "Sinaloa", "Sonora", "Tabasco", "Tamaulipas",
    "Tlaxcala", "Veracruz de Ignacio de la Llave", "Yucatán", "Zacatecas"
  ),
  region = c(
    "2. Corredor Industrial Centro-Bajío",
    "1. Frontera Norte / Manufactura Avanzada",
    "7. Pacífico Norte y Mar de Cortés",
    "4. Energética y Golfo (Petrolera)",
    "1. Frontera Norte / Manufactura Avanzada",
    "7. Pacífico Norte y Mar de Cortés",
    "6. Corredor Interoceánico y Pacífico Sur",
    "1. Frontera Norte / Manufactura Avanzada",
    "3. Núcleo Metropolitano y Financiero (Centro)",
    "7. Pacífico Norte y Mar de Cortés",
    "2. Corredor Industrial Centro-Bajío",
    "6. Corredor Interoceánico y Pacífico Sur",
    "3. Núcleo Metropolitano y Financiero (Centro)",
    "2. Corredor Industrial Centro-Bajío",
    "3. Núcleo Metropolitano y Financiero (Centro)",
    "7. Pacífico Norte y Mar de Cortés",
    "3. Núcleo Metropolitano y Financiero (Centro)",
    "7. Pacífico Norte y Mar de Cortés",
    "1. Frontera Norte / Manufactura Avanzada",
    "6. Corredor Interoceánico y Pacífico Sur",
    "3. Núcleo Metropolitano y Financiero (Centro)",
    "2. Corredor Industrial Centro-Bajío",
    "5. Peninsular (Turismo y Servicios del Caribe)",
    "2. Corredor Industrial Centro-Bajío",
    "7. Pacífico Norte y Mar de Cortés",
    "1. Frontera Norte / Manufactura Avanzada",
    "4. Energética y Golfo (Petrolera)",
    "1. Frontera Norte / Manufactura Avanzada",
    "3. Núcleo Metropolitano y Financiero (Centro)",
    "4. Energética y Golfo (Petrolera)",
    "5. Peninsular (Turismo y Servicios del Caribe)",
    "7. Pacífico Norte y Mar de Cortés"
  ),
  stringsAsFactors = FALSE
)
}



# Exportaciones % PIBE --------------------------------------------------------------


# Verificar estructura y primeras filas
str(regiones_mexico)
head(regiones_mexico, 10)

token_inegi <- "269a9c6a-3daf-4400-df8c-dc616b577d74"

etef <- read.csv("datos/eef_trimestral_csv/conjunto_de_datos/eef_trimestral_tr_cifra_2007_2026.csv")

etef <- etef %>% 
  mutate(date = ymd(paste(ANIO, substr(MES,1,2), "01", sep = "-"))) %>% 
  left_join(regiones_mexico)

etef %>% 
  group_by(region, year = year(date)) %>% 
  summarise(export = sum(VAL_USD, na.rm = TRUE)) %>% 
  ggplot(aes(x = year, y = export, fill = region)) +
  geom_col(position = "dodge") 


# Exportaciones anuales por entidad
eaef <- etef %>% 
  select(date, CODIGO_SCIAN, date, NOM_ENT, region, VAL_USD) %>% 
  group_by(date = year(date), NOM_ENT, region) %>% 
  summarise(exportaciones = sum(VAL_USD, na.rm = TRUE)) %>% 
  mutate(date = ymd(paste0(date,"-01-01")))


nom_pib <- "Millones de pesos|PIBPM---Producto interno bruto, a precios de mercado"

pibe_nominal <- read.csv("datos/pibe_csv/conjunto_de_datos/conjunto_de_datos_pibe_actividad_pibe2024_r.csv")

pibe_nominal <- pibe_nominal %>% 
  filter(grepl(nom_pib, pibe_nominal$Descriptores, fixed = TRUE)) %>% 
  slice(-1) %>% 
  mutate(Descriptores = substr(Descriptores,72,1099),
         Descriptores = str_replace_all(Descriptores, pattern = "<C1>" , replacement = "")) %>% 
  rename("NOM_ENT" = "Descriptores")

pibe_nominal <- pibe_nominal %>% 
  pivot_longer(cols = 2:last_col(), names_to = "date", values_to = "pibe") %>% 
  mutate(date = str_remove_all(date, "\\D"),
         date = ymd(paste0(date,"-01-01"))) %>% 
  arrange(date) %>% 
  left_join(regiones_mexico, by = "NOM_ENT") %>% 
  left_join()
  



# Calcular exportacioens como porcentaje del PIBE

id_fix <- "SF17908"


token_banxico <- "def18a230f6375ab2e5183ffb31f5618b53697b2989a8e51a51f8191f0e34d35"

setToken(token_banxico)

fix <- getSeriesData(id_fix) %>% 
  getSerieDataFrame(id_fix) 


fix <- fix %>% 
  group_by(date = year(date)) %>% 
  summarise(fix = mean(value), .groups = "drop") %>% 
  mutate(date = ymd(paste0(date,"-01-01")))


exp_pibe <- left_join(eaef, pibe_nominal) %>% 
  left_join(fix) %>% 
  drop_na() %>% 
  mutate(exportaciones = ((exportaciones * fix) / 1000 ),
         x_pibe = exportaciones/pibe)



# Exportaciones por sector y entidad

# Exportaciones x sector ------------------------------------------------------------

etsec <- etef %>% 
  # filter(ANIO >= 2018) %>% 
  group_by(CODIGO_SCIAN, NOM_ENT) %>% 
  summarise(export = sum(VAL_USD, na.rm = TRUE)) %>% 
  filter(CODIGO_SCIAN != 0)

# Matriz de exportaciones
mat_x <- xtabs(export ~ NOM_ENT + as.factor(CODIGO_SCIAN), data = etsec)
mat <- as.matrix(mat_x)


# heatmap(as.matrix(mat), Rowv = NULL, Colv = NA, scale = "none")
library(viridisLite)


pheatmap(
  mat,
  scale = "row",
  cluster_rows = TRUE,
  cluster_cols = FALSE,
  clustering_distance_rows = "correlation",
  clustering_distance_cols = "correlation",
  clustering_method_rows = "ward.D2",
  clustering_method_cols = "ward.D2",
  cutree_rows = 6,
)




# Convert each row to sector shares summing to 100%
mat_share <- sweep(mat, 1, rowSums(mat), "/")



pheatmap(
  mat,
  scale = "column",
  cluster_rows = TRUE,
  cluster_cols = FALSE,
  clustering_distance_rows = "euclidean",
  clustering_method = "ward.D",
  cutree_rows = 6,
  # color = colorRampPalette(c("white", "#fcffa4", "#bc3754", "#57106e"),
  #                               space = "rgb")(100),
  
  main = "Distribución de las exportaciones por entidad federativa"
)




pheatmap(
  mat_share,
  scale = "none",
  cluster_rows = TRUE,
  cluster_cols = FALSE,
  clustering_distance_rows = "correlation",
  # clustering_distance_cols = "correlation",
  # clustering_method_rows = "ward.D2",
  clustering_method = "ward.D",
  cutree_rows = 6,
  color = colorRampPalette(c("white", "#fcffa4", "#bc3754", "#57106e"),
                                space = "rgb")(100),
  
  main = "Participación de las exportaciones por sector"
)











# Modelo 1 --------------------------------------------------------------------------



data_m1 <- left_join(pibe_nominal, eaef) %>% 
  left_join(fix) %>% 
  drop_na() %>% 
  mutate(export = (exportaciones * fix) / 1000)


library(plm)


mod_gmm <- pgmm(
  log(pibe) ~ lag(log(pibe), 1) + log(export) | 
    lag(log(pibe), 2:4) + lag(log(export), 2:4),
  data = data_m1,
  effect = "twoways",
  model = "twosteps",
  transformation = "ld", # System GMM
  collapse = TRUE        # Fundamental para evitar la proliferación excesiva de instrumentos con T=18
)

summary(mod_gmm, robust = TRUE)

  
library(fixest)

# Errores estándar clusterizados a nivel entidad (clustered SEs)
mod_twfe <- feols(
  log(pibe) ~ log(export)  | CVE_ENT + date,
  data = data_m1,
  cluster = ~CVE_ENT
)

summary(mod_twfe)




# Declare panel structure in fixest with panel(id, time)
mod_growth <- feols(
  d(log(pibe)) ~ l(d(log(export)), 1) | CVE_ENT + date,
  data = data_m1,
  panel.id = ~CVE_ENT + date
)


summary(mod_growth)
    

