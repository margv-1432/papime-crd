# Encadenamientos

# Calcular un multiplicador doméstico (incluido ya en INEGI)


# Conjunto de datos a nivel RAMA4 dígitos de desagregación
leontief_rama <- read.csv("datos/mip_csv/conjunto de datos/conjunto_de_datos_mip_cdi_ixi_32018.csv")


mult_dom_rama <- pivot_longer(leontief_rama, cols = 2:ncol(leontief_rama)) %>% 
  group_by(name) %>% 
  summarise(mu_d = sum(value, na.rm = TRUE)) %>% 
  mutate(rama = substr(name,2,5))




# Multiplicador uso domestico + importado -------------------------------------------


ruta_mip <- "datos/mip_csv/conjunto de datos"
file_mip_ixi <- "conjunto_de_datos_mip_t_pb_ixi_32018.csv"

mip_ixi_d_m <- read.csv(file.path(ruta_mip, file_mip_ixi))

row_idx <- mip_ixi_d_m %>% select(Descriptores) %>% 
  mutate(n = seq_along(Descriptores))


cols <- colnames(mip_ixi_d_m)[-1]

col_idx <- tibble(n = seq_along(cols),
                      original_name = cols) %>% 
  mutate(
    category = str_extract(original_name, "^[^.]+"),
    sector = str_match(original_name,"\\.(\\d{4})\\.\\.\\.")[,2],
    
  )


ramas <- col_idx %>% drop_na() %>% pull(sector)


z_idx_ixi <- col_idx %>% 
  filter(category == "DI" & sector %in% ramas) %>% 
  pull(n)


mip_ixi_d_m <- as.matrix(mip_ixi_d_m[,-1])


Z_ixi <- as.matrix.data.frame(mip_ixi_d_m[1:length(z_idx_ixi), z_idx_ixi])
dimnames(Z_ixi) <- list(ramas, ramas)

X_ixi <- mip_ixi_d_m[1:length(z_idx_ixi),1]

A_ixi <- sweep(Z_ixi, MARGIN = 2, STATS = X_ixi, FUN = "/")

L_ixi <- solve(diag(nrow(A_ixi)) - A_ixi)

mu_ixi <- tibble(mu_t = colSums(L_ixi),
                 rama = ramas)



mus <- left_join(mult_dom_rama, mu_ixi, by = "rama") %>% 
  mutate(diff = mu_t - mu_d,
    rama = str_trim(as.character(rama)), # Remove any hidden whitespace
    rama = fct_reorder(rama, mu_t)       # Sort strictly by mu_t from bottom to top
  )
