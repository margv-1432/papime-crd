# Plots



# Exportaciones como Porcentaje del PIBE --------------------------------------------


exp_pibe %>% 
  group_by(NOM_ENT) %>% 
  filter(date == min(date, na.rm = TRUE) | date == max(date, na.rm = TRUE)) %>% 
  mutate(year = as.character(year(date))) %>% 
  ungroup() %>% 
  ggplot(aes(x = x_pibe, y = reorder(NOM_ENT, x_pibe))) +
  # Connecting line between the two years
  geom_line(aes(group = NOM_ENT), color = "#d3d3d3", linewidth = 1) +
  # Points for each year
  geom_point(aes(color = year), size = 3) +
  scale_color_manual(values = c("2007" = "grey60", "2024" = "black")) +
  scale_x_continuous(labels = scales::label_percent()) +
  labs(
    title = "Exportaciones como porcentaje del PIBE",
    x = NULL,
    y = NULL,
    color = "Año"
  ) +
  theme_minimal() +
  theme(
    legend.position = "top",
    panel.grid.major.y = element_blank(), # Cleans up horizontal lines behind dumbbells
    plot.title = element_text(face = "bold")
  )




# Mapa funciones de exportaciones ---------------------------------------------------


cluster_1 <- c("")



# Generación por tecnología anual ---------------------------------------------------


gen %>% 
  group_by(year = year(date), X) %>% 
  filter(X %in% c("Vapor", "Ciclo combinado", "Turbogas", "Combustión interna", 
                  "Dual", "Carboeléctrica", "Geotermoeleçtrica", "Nucleoeléctrica",
                  "Eólica", "Hidroeléctrica", "Fotovoltaica")) %>% 
  summarise(MWh = sum(MWh, na.rm = TRUE), .groups = 'drop_last') %>% 
  mutate(share = MWh / sum(MWh, na.rm = TRUE)) %>% 
  filter(year != "2026") %>% 
  mutate(date = ymd(paste0(year, "-01-01"))) %>% 
  ggplot(aes(x = year(date), y = share, fill = X)) +
  geom_col() +
  labs(title = "México: Generación bruta de electricidad por tecnología (Participación)",
       fill = "Tecnología",
       x = NULL,
       y = "%") +
  theme(plot.title = element_text(face = "bold"))





gen %>% 
  group_by(year = year(date), X) %>% 
  filter(X %in% c("Vapor", "Ciclo combinado", "Turbogas", "Combustión interna", 
                  "Dual", "Carboeléctrica", "Geotermoeleçtrica", "Nucleoeléctrica",
                  "Eólica", "Hidroeléctrica", "Fotovoltaica")) %>% 
  summarise(MWh = sum(MWh, na.rm = TRUE), .groups = 'drop_last') %>% 
  ggplot(aes(x = date, y = MWh)) +
  geom_line() +
  labs(title = "México: Generación bruta de electricidad por tecnología (Participación)",
       fill = "Tecnología",
       x = NULL,
       y = "%") +
  theme(plot.title = element_text(face = "bold"))




gen %>% 
  group_by(year = year(date)) %>% 
  filter(X %in% c("Vapor", "Ciclo combinado", "Turbogas", "Combustión interna", 
                  "Dual", "Carboeléctrica", "Geotermoeleçtrica", "Nucleoeléctrica",
                  "Eólica", "Hidroeléctrica", "Fotovoltaica")) %>% 
  summarise(MWh = sum(MWh, na.rm = TRUE)) %>% 
  mutate(date = ymd(paste0(year, "-01-01"))) %>% 
  ggplot(aes(x = date, y = MWh)) +
  geom_line() +
  labs(title = "México: Generación bruta de electricidad por tecnología (Participación)",
       fill = "Tecnología",
       x = NULL,
       y = "%") +
  theme(plot.title = element_text(face = "bold"))



# Densidad carretera de alta capacidad y PIBE ---------------------------------------

ggplot(RNC_PIBE, aes(x = densidad_carretera, y = pibe_manufacturero)) +
  geom_point() 



# Regresión carreteras --------------------------------------------------------------


# Cargar librerías necesarias (instalar ggrepel si no está: install.packages("ggrepel"))
library(ggplot2)
library(ggrepel)

# Crear la gráfica del Modelo 4
grafica_mod4 <- ggplot(
  data = df_models, 
  aes(
    x = log(densidad_4c + 0.0001), 
    y = log(pibe_manuf_km2), 
    label = NOMGEO
  )
) +
  # 1. Banda de confianza y línea de regresión MCO
  geom_smooth(
    method = "lm", 
    formula = y ~ x, 
    se = TRUE, 
    color = "#1f4e78", 
    fill = "#b4c6e7", 
    alpha = 0.35,
    linewidth = 1
  ) +
  # 2. Puntos de las entidades federativas
  geom_point(
    color = "#c00000", 
    size = 2.8, 
    alpha = 0.85
  ) +
  # 3. Etiquetas de los estados sin traslape
  geom_text_repel(
    size = 3.2,
    color = "gray20",
    box.padding = 0.4,
    point.padding = 0.3,
    max.overlaps = Inf,       # Garantiza que aparezcan las 32 entidades
    segment.color = "gray60", # Línea guía sutil cuando la etiqueta se aleja del punto
    segment.size = 0.3
  ) +
  # 4. Anotación con la ecuación estimada y el R2 dentro del lienzo
  annotate(
    "text",
    x = min(log(df_models$densidad_4c + 0.0001), na.rm = TRUE) + 0.2,
    y = max(log(df_models$pibe_manuf_km2), na.rm = TRUE) - 0.5,
    label = "hat(y) == 7.24 + 1.45*x ~~ (R^2 == 0.521)",
    parse = TRUE,
    hjust = 0,
    size = 4,
    color = "#1f4e78"
  ) +
  # 5. Títulos y formato académico/editorial
  labs(
    title = "Conectividad de Alta Capacidad y Densidad Manufacturera en México",
    subtitle = "Relación log-log entre densidad vial de 4+ carriles y PIBE manufacturero por km²",
    x = "Log(Densidad carretera de 4+ carriles [km / km²])",
    y = "Log(PIBE Manufacturero por km²)",
    caption = "Fuente: Elaboración propia con datos de SICT e INEGI. Ajuste lineal por MCO con intervalo de confianza al 95%."
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(face = "bold", color = "gray10"),
    plot.subtitle = element_text(size = 11, color = "gray40", margin = margin(b = 12)),
    axis.title = element_text(face = "bold"),
    panel.grid.minor = element_blank(),
    plot.caption = element_text(hjust = 0, color = "gray50", size = 9, margin = margin(t = 12))
  )


# Mostrar en pantalla
print(grafica_mod4)

# Opcional: Guardar en alta resolución para documento o publicación
# ggsave("dispersion_conectividad_manuf.png", plot = grafica_mod4, width = 9, height = 6, dpi = 300, bg = "white")






# Scatterplot: VACB y Gasto en Energía ----------------------------------------------


censo_energia %>% ggplot(aes(x = log(vacb_l), y = log(gasto_l))) +
  geom_point(alpha = 0.45) +
  geom_smooth(method = "lm", 
              se = TRUE, 
              linewidth = 1, 
              linetype = "dashed") +
  labs(
    title = "Intensidad Energética y Productividad Laboral en Manufacturas (SCIAN 31-33)",
    subtitle = "Unidades a nivel Entidad Federativa × Subsector",
    x = "Intensidad Energética: ln(Gasto en Energía Eléctrica / Personal Ocupado)",
    y = "Productividad Laboral: ln(VACB / Personal Ocupado)",
    caption = "Fuente: Elaboración propia con datos de los Censos Económicos (INEGI).",
    size = "Valor agregado censal bruto"
  ) +
  theme_minimal() +
  theme(
    legend.position = "bottom",
    panel.grid.minor = element_blank(),
    plot.title = element_text(face = "bold")
  )




# Diferencial de multiplicadores de demanda -----------------------------------------


mus %>% filter(substr(rama,1,1) == 3) %>% 
ggplot(aes(y = rama)) +
  # Draw the connecting leakage line
  geom_segment(aes(x = mu_d, xend = mu_t, yend = rama),
               color = "grey65", 
               linewidth = 0.6) +
  # Draw Domestic points (mapping color to a string label creates the legend automatically)
  geom_point(aes(x = mu_d, color = "Doméstico"), 
             size = 2) +
  # Draw Total points
  geom_point(aes(x = mu_t, color = "Total (Dom + Imp)"), 
             size = 2) +
  # Assign colors to the string labels
  scale_color_manual(
    name = "Tipo de multiplicador",
    values = c("Doméstico" = "#1b9e77", "Total (Dom + Imp)" = "#d95f02")
  ) +
  labs(
    x = "Multiplicador de Leontief",
    y = "Rama industrial",
    title = "México: Encadenamientos hacia atrás domésticos vs totales"
  ) +
  theme_minimal() +
  theme(plot.title = element_text(face = "bold"))




# Comercio por tipo de transporte ---------------------------------------------------


comercio_transporte %>% 
  group_by(modo, date, tipo) %>% 
  summarise(m_usd = sum(VAL_USD, na.rm = TRUE)) %>% 
  ggplot(aes(x = date, y = m_usd, color = modo)) +
  geom_line()



comercio_transporte %>%
  filter(!is.na(modo)) %>% # Excludes total header rows if present
  group_by(date = year(date), modo, TIPO) %>% 
  summarise(m_usd = sum(VAL_USD, na.rm = TRUE)) %>% 
  filter(date < 2026) %>% 
  ggplot(aes(x = date, y = m_usd, fill = modo)) +
  geom_area(position = "stack", alpha = 0.85, color = "white", linewidth = 0.2) +
  facet_wrap(~ TIPO, ncol = 1, scales = "free_y") +
  scale_fill_brewer(palette = "Set2") +
  labs(
    title = "Comercio Exterior por Modo de Transporte",
    y = "Millones de dólares",
    x = NULL,
    fill = "Modo de Transporte"
  ) +
  scale_x_continuous(n.breaks = 12) +
  theme_minimal() +
  theme(plot.title = element_text(face = "bold"),
        legend.position = "bottom")




# Comercio por aduana ---------------------------------------------------------------

comercio_transporte %>% 
  filter(!CONCEPTO %in% names(MTRA)) %>% 
  group_by(CONCEPTO, modo) %>% 
  summarise(tot_val_usd = sum(VAL_USD)) %>% 
  view()
