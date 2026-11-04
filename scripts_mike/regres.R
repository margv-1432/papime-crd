# Regresiones

# Load required libraries (install if needed: install.packages(c("tidyverse", "broom")))
library(tidyverse)
library(broom)

# 1. Feature Engineering: Create intensive variables & specific 4+ lane indices
df_models <- RNC_PIBE %>%
  mutate(
    # Dependent variables (Y) normalized
    pibe_manuf_km2 = pibe_manuf / superficie_km2,          # Spatial manufacturing density
    pibe_manuf_pc  = pibe_manuf / pob_2025,                # Per capita manufacturing PIBE
    
    # Independent variables (X) focused on 4+ lanes (High-Capacity Corridors)
    densidad_4c    = pavimentada_4 / superficie_km2,       # Density of 4+ lane roads
    engel_4c       = (pavimentada_4 * 100) / sqrt(superficie_km2 * pob_2025), # Engel for 4+ lanes
    prop_4c        = pavimentada_4 / pavimentada           # Share of paved network that is 4+ lanes
  )

# 2. Define candidate model specifications
# Note: The main infrastructure predictor is always placed first on the RHS to extract its p-value easily
formulas <- list(
  # Group A: Controlled Levels (Isolating scale effect via controls)
  "M1: Levels + Area & Pop Controls"     = pibe_manuf ~ pavimentada_4 + superficie_km2 + pob_2025,
  "M2: Log-Log + Area & Pop Controls"    = log(pibe_manuf) ~ log(pavimentada_4 + 1) + log(superficie_km2) + log(pob_2025),
  
  # Group B: Spatial Density Matching (Intensive Y vs Intensive X)
  "M3: Spatial Density (Linear)"         = pibe_manuf_km2 ~ densidad_4c,
  "M4: Spatial Density (Log-Log)"        = log(pibe_manuf_km2) ~ log(densidad_4c + 0.0001),
  
  # Group C: Engel Index Specifications (4+ Lanes & Total Paved)
  "M5: PIBE per capita vs Engel (4+)"    = pibe_manuf_pc ~ engel_4c,
  "M6: Log PIBE per capita vs Log Engel" = log(pibe_manuf_pc) ~ log(indice_engel),
  "M7: Log PIBE (Total) vs Engel (4+)"   = log(pibe_manuf) ~ engel_4c + log(pob_2025),
  
  # Group D: Network Quality / Upgrading Ratio
  "M8: PIBE per capita vs Share of 4+c"  = pibe_manuf_pc ~ prop_4c
)

# 3. Function to fit model and extract both model-level and predictor-level diagnostics
run_diagnostics <- function(form, data) {
  fit <- lm(form, data = data)
  
  # Model-level metrics
  mod_stats <- glance(fit)
  
  # Predictor-level metrics (Row 2 corresponds to the primary infrastructure variable)
  coef_stats <- tidy(fit)[2, ]
  
  # Check residual normality (Shapiro-Wilk p-value)
  shapiro_p <- shapiro.test(residuals(fit))$p.value
  
  tibble(
    Predictor_Term = coef_stats$term,
    Beta_Estimate  = round(coef_stats$estimate, 4),
    Std_Error      = round(coef_stats$std.error, 4),
    t_stat         = round(coef_stats$statistic, 2),
    p_value_X      = round(coef_stats$p.value, 5),
    Signif_X       = ifelse(coef_stats$p.value < 0.05, "Yes (*)", "No"),
    R2             = round(mod_stats$r.squared, 3),
    Adj_R2         = round(mod_stats$adj.r.squared, 3),
    F_stat         = round(mod_stats$statistic, 2),
    AIC            = round(mod_stats$AIC, 1),
    Shapiro_p      = round(shapiro_p, 3),
    N              = mod_stats$nobs
  )
}

# 4. Run all models on Full Sample (N = 32)
diagnostics_table <- map_dfr(formulas, ~ run_diagnostics(.x, data = df_models), .id = "Model")

# Print sorted by Predictor p-value and Adjusted R2
print(diagnostics_table %>% arrange(p_value_X, desc(Adj_R2)), width = Inf)


mod_rnc <- lm(log(pibe_manuf_km2) ~ log(densidad_4c + 0.0001), data = df_models)
summary(mod_rnc)
