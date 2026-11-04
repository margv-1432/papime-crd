# Energía


gen <- read.csv("datos/energia/generacion_tecnologia.csv", skip = 7) %>% 
  slice(-1) %>% 
  head(-6) %>% 
  mutate(across(2:last_col(), as.numeric))

dates <- as.character(seq.Date(from = ymd("2002-01-01"), to = ymd("2026-08-01"), by = "1 month"))

colnames(gen)[2:ncol(gen)] <- dates

gen <- gen %>% 
  pivot_longer(cols = 2:last_col(), names_to = "date" , values_to = "MWh") %>% 
  mutate(date = ymd(date))


gen_ent <- read.csv("datos/energia/generacion_bruta_entidad.csv", skip = 7) %>% 
  slice(-1) %>% 
  head(-6) %>% 
  mutate(across(2:last_col(), as.numeric))

colnames(gen_ent)[2:ncol(gen_ent)] <- as.character(dates)

gen_ent <- gen_ent %>% 
  pivot_longer(cols = 2:last_col(), names_to = "date" , values_to = "MWh") %>% 
  mutate(date = ymd(date))

library(rmapshaper)
map <- st_read("shapefiles/dest25gw/dest25gw.shp") %>% 
  ms_simplify(keep = 0.01)


gen_ent %>% 
  group_by(X) %>% 
  summarise(generacion = mean(MWh, na.rm = TRUE)) %>% 
  arrange(desc(generacion))





# Intensidad Energética -------------------------------------------------------------


intens <- read.csv("datos/energia/intensidad_censo.csv", skip = 4) %>% 
  rename("NOMGEO" = "Entidad")
colnames(intens)[3:7] <- c("Sector" , "VA", "fuel", "gasto_energ", "prod_bruta")


intens <- intens %>% 
  mutate(intens =  (fuel + gasto_energ) / prod_bruta)

# 2. Filter for all target years and clean state names
years_target <- c(2008, 2013, 2018, 2023)

intens_filtered <- intens %>% 
  filter(Año.Censal %in% years_target) %>% 
  mutate(NOMGEO = substr(NOMGEO, 4, 100))

# 3. Join spatial data with census data across all selected years
#    Using map %>% inner_join(...) or left_join replicates the geometries per year
map_intens <- map %>% 
  inner_join(intens_filtered, by = "NOMGEO")

# 4. Plot with facet_wrap
ggplot(map_intens) +
  geom_sf(aes(fill = intens), color = "white", size = 0.1) +
  scale_fill_viridis_c(
    option = "inferno",
    direction = -1,
    na.value = "grey85",
    name = "Intensidad\n(Gasto / PB)"
  ) +
  facet_wrap(~ Año.Censal, ncol = 2) +
  labs(
    title = "Intensidad energética industrial",
    subtitle = "Censos Económicos 2008–2023",
    caption = "Fuente: Elaboración propia con datos censales."
  ) +
  theme_void() +
  theme(
    plot.title = element_text(face = "bold", size = 16, hjust = 0.5),
    plot.subtitle = element_text(size = 12, hjust = 0.5, margin = margin(b = 10)),
    strip.text = element_text(face = "bold", size = 12),
    legend.position = "bottom"
  )



ggplot(map_intens, aes(x = VA, y = gasto_energ)) +
  geom_point()


# Correlación -----------------------------------------------------------------------


censo_energia <- readr::read_csv("datos/energia/censo_energia.csv", skip = 4) 
colnames(censo_energia) <- c("year", "NOMGEO", "actividad", "personal",
                             "vacb", "prod_bruta", "activos", "gasto_energia")
censo_energia <- censo_energia %>% 
  filter(!actividad %in% c("Total estatal", "Sector 31-33 Industrias manufactureras")) %>% 
  mutate(vacb_l = vacb / personal,
         gasto_l = gasto_energia / personal)




# Modelo Función de Producción ------------------------------------------------------

library(fixest)

# 1. Preparación de datos: Forma intensiva (por trabajador) y logaritmos
df_panel <- censo_energia %>%
  # Filtrar ceros o valores negativos (pueden ocurrir en VACB censal) antes de aplicar log()
  filter(vacb > 0, gasto_energia > 0, activos > 0, personal > 0) %>%
  mutate(
    ln_y_l = log(vacb / personal),           # Productividad laboral
    ln_e_l = log(gasto_energia / personal),  # Intensidad energética por ocupado
    ln_k_l = log(activos / personal)   # Intensidad de capital por ocupado
  )

# 2. Especificación del modelo econométrico con Efectos Fijos (TWFE)
# Caso A: Si tu panel es Estado x Año
# modelo_estatal <- feols(
#   fml = ln_y_l ~ ln_e_l + ln_k_l | NOMGEO + year,
#   data = df_panel,
#   vcov = ~NOMGEO # Errores estándar agrupados (clustered) por entidad
# )

# Caso B: Si tu panel incluye Subsector SCIAN (Estado x Subsector x Año)
# (Absorbe diferencias tecnológicas por industria y tarifas regionales por estado-año)
modelo_sectorial <- feols(
  fml = ln_y_l ~ ln_e_l + ln_k_l | NOMGEO^year + actividad^year,
  data = df_panel,
  vcov = ~NOMGEO + actividad
)


# 3. Tabla de resultados y diagnóstico
etable(modelo_sectorial, digits = 3)



# CONAHCYT consumo por entidad ------------------------------------------------------


consumo_gwh_ent <- read.csv("datos/energia/consumo_gwh_entidad_federativa.csv")




# Global Power Plant ----------------------------------------------------------------


global_power_plant <- read.csv("datos/energia/globalpowerplantdatabasev130/global_power_plant_database.csv") %>% 
  filter(country == "MEX") 

global_power_plant %>% group_by(primary_fuel) %>% 
  count()


power_plants <- st_as_sf(globa_power_plant, 
                         coords = c("longitude", "latitude"), 
                         crs = 4326, remove = FALSE) %>% 
  st_transform(crs = st_crs(map))



ggplot() +
  geom_sf(data = map, color = "black") +
  geom_sf(data = power_plants, aes(color = primary_fuel)) +
  theme_minimal() +
  labs(color = "Combustible",
       title = "Ubicación de plantas eléctricas en México") +
  theme(plot.title = element_text(face = "bold"))




# Conteo de plantas por entidad federativa ------------------------------------------

plantas_estado <- st_join(power_plants, map[, "NOMGEO"], join = st_intersects)

plantas_estado %>% group_by(primary_fuel) %>% 
  count() %>% view()




# Plantas ---------------------------------------------------------------------------


denue_plantas <- read_csv("datos/energia/denue_00_22_csv/conjunto_de_datos/denue_inegi_22_.csv",
                          locale = locale(encoding = "ISO-8859-1")) %>% 
  filter(substr(codigo_act,1,5) == 22111)




# Global Energy Monitor -------------------------------------------------------------


