# Distribuciones generales


# Empleo
library(tidyverse)

enoe <- read_csv("datos/empleo/enoe.csv", locale = locale(encoding = "latin1"))

empleo <- enoe %>% 
  mutate(Year = substr(Periodo, 1,4)) %>% 
  filter(Year >= 2019,
         Indicador == "2.1.1. Población ocupada") %>% 
  group_by(`Área geográfica`) %>% 
  summarise(empleo = mean(DATA))


hist(empleo$empleo)


nom_pibe <- "Millones de pesos a precios de 2018|PIBPM---Producto interno bruto, a precios de mercado"


pibe <- read.csv("datos/pibe_csv/conjunto_de_datos/conjunto_de_datos_pibe_actividad_pibe2024_r.csv")


pibe <- pibe %>% 
  filter(grepl(nom_pibe, pibe$Descriptores, fixed = TRUE)) %>% 
  slice(-1) %>% 
  mutate(Descriptores = substr(Descriptores,90,1099),
         Descriptores = str_replace_all(Descriptores, pattern = "<C1>" , replacement = "")) %>% 
  rename("NOM_ENT" = "Descriptores")

pibe <- pibe %>% 
  pivot_longer(cols = 2:last_col(), names_to = "date", values_to = "pibe_2018") %>% 
  mutate(date = str_remove_all(date, "\\D"),
         date = ymd(paste0(date,"-01-01"))) %>% 
  arrange(date) %>% 
  left_join(regiones_mexico, by = "NOM_ENT")


pibe_hist <- pibe %>% filter(year(date) >= 2019) %>% 
  group_by(NOM_ENT) %>% 
  summarise(PIBE = mean(pibe_2018))


hist(pibe_hist$PIBE)



pib_manufacturero <- read.csv(
  "datos/pibe_csv/conjunto_de_datos/conjunto_de_datos_pibe_actividad_31_332024_r.csv")


pibe_manufacturero_2024 <- pib_manufacturero %>% 
  select(1,last_col()) %>% slice(2:33) %>% 
  mutate("NOMGEO" = entidades)
