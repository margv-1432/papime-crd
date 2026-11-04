# Transportes

library(tidyverse); library(readxl)


superficie <- read_excel("datos/geografia/superficie_km2.xlsx")


carreteras_entidad <- read_excel(
  "datos/anuario_estadistico/14. Transportes_2025.xlsx",
  sheet = "14.2", range = "A53:N84", col_names = FALSE) %>% 
  select(1,2,3,5,10,14)


colnames(carreteras_entidad) <- c("NOMGEO", "total", "carreteras_federales", 
                                  "alimentadoras_estatales", "caminos_rurales", "brechas")


carreteras_superficie <- read_excel("datos/infraestructura/RNC_superficie.xlsx")


poblacion_2025 <- read_excel("datos/poblacion/poblacion_2025_anuario.xlsx")


# Carreteas de alta capacidad y PIB manufacturero

RNC_PIBE <- left_join(carreteras_superficie, superficie, by = "NOMGEO") %>% 
  left_join(pibe_manufacturero_2024, by = "NOMGEO")  %>% 
  left_join(poblacion_2025, by = "NOMGEO") %>% drop_na() %>% 
  select(NOMGEO, total, pavimentada, pavimentada_4, superficie_km2, pob_2025, `X2024.R.`) %>% 
  rename("pibe_manuf" = "X2024.R.") %>% 
  mutate(densidad_carretera = pavimentada / superficie_km2,
         indice_engel = (pavimentada * 100) / sqrt(superficie_km2 * pob_2025))
