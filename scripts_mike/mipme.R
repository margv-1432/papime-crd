# REGIONALES

library(tidyverse); library(readxl)
ageeml <- read.csv("datos/ageeml.csv")


mipme_index <- read.csv("datos/mipme/mipme_index.csv")


mipme_z <- as.matrix(read.csv("datos/mipme/mipme_z.csv", header = FALSE))

mipme_va <- read.csv("datos/mipme/mipme_va.csv", header = FALSE)

mipme_x <- mipme_va %>% slice(nrow(mipme_va)) %>% 
  unlist()

mipme_x <- mipme_x[!is.na(mipme_x)]

length(mipme_x)


mipme_a <- as.matrix(sweep(mipme_z, 2, mipme_x, "/"))

mipme_a[is.na(mipme_a)] <- 0

mipme_L <- solve(diag(1, nrow = nrow(mipme_a)) - mipme_a)




# Multiplicadores regionales --------------------------------------------------------


mipme_mu <- tibble(mu_e = colSums(mipme_L),
                   n = seq_along(mu_e)) %>% 
  left_join(mipme_index, by = "n") %>% 
  filter(mu_e > 1)

     












library(tidyverse)
library(readxl)

# Load metadata and indices
ageeml <- read.csv("datos/ageeml.csv")
mipme_index <- read.csv("datos/mipme/mipme_index.csv")

# Load Z matrix and Gross Output (X)
mipme_z <- as.matrix(read.csv("datos/mipme/mipme_z.csv", header = FALSE))

mipme_va <- read.csv("datos/mipme/mipme_va.csv", header = FALSE)

# Extract total gross production vector (last row of VA matrix)
mipme_x <- mipme_va %>%
  slice_tail(n = 1) %>%
  unlist(use.names = FALSE)

mipme_x <- mipme_x[!is.na(mipme_x)]

# Sanity check: dimensions must match
stopifnot(ncol(mipme_z) == length(mipme_x))
stopifnot(nrow(mipme_z) == ncol(mipme_z))

# Technical coefficient matrix A: a_ij = z_ij / x_j
mipme_a <- sweep(mipme_z, 2, mipme_x, "/")

# Handle divide-by-zero (Inf/NaN) and missing values
mipme_a[!is.finite(mipme_a)] <- 0

# Leontief inverse: L = (I - A)^(-1)
I <- diag(1, nrow = nrow(mipme_a))
mipme_L <- solve(I - mipme_a)

# Regional Multipliers
# colSums = backward output multipliers (shocks to final demand)
# rowSums = forward output multipliers
mipme_mu <- tibble(
  n = seq_len(ncol(mipme_L)),
  mu_e = colSums(mipme_L)
) %>%
  left_join(mipme_index, by = "n")



mipme_mu %>% group_by(NOM_ENT) %>% 
  summarise(mu_avg = mean(mu_e)) %>% 
  arrange(-mu_avg) %>% 
  view()







# Dimension and total sum of the Leontief inverse
n_sec <- ncol(mipme_L)
total_L <- sum(mipme_L)

# Mean of the multiplier matrix (1 / n^2 * sum(L))
mean_L <- total_L / (n_sec^2)

# Compute normalized linkages and classify sectors
mipme_rh <- tibble(
  n = seq_len(n_sec),
  # Backward linkage: normalized column sum
  BL = (colSums(mipme_L) / n_sec) / mean_L,
  # Forward linkage: normalized row sum
  FL = (rowSums(mipme_L) / n_sec) / mean_L
) %>%
  mutate(
    sector_type = case_when(
      BL > 1  & FL > 1  ~ "Clave (Key)",
      BL <= 1 & FL > 1  ~ "Base / Impulsor (Forward)",
      BL > 1  & FL <= 1 ~ "Arrastre (Backward)",
      BL <= 1 & FL <= 1 ~ "Independiente (Independent)"
    )
  ) %>%
  left_join(mipme_index, by = "n")





# Con importaciones -----------------------------------------------------------------



files_mipme_mrm <- list.files(path = "datos/mipme/mip_pxp_me_mrm",
                              full.names = TRUE)

read_excel(files_mipme_mrm[[1]], skip = 6, col_names = FALSE) %>% 
  head(-4) %>% select(3:(ncol(.)-7)) %>% 
  view()

mipme_mrm_all <- list()

# Lista con las matrices estatales con importaciones del resto del mundo
mipme_mrm_all <- lapply(files_mipme_mrm, function(x){
  
  as.matrix(read_excel(x, skip = 6, col_names = FALSE) %>% 
    head(-4) %>% select(3:(ncol(.)-7)))
  
})

mipme_z_t <- mipme_z


S <- nrow(mipme_mrm_all[[1]])

for (i in seq_along(mipme_mrm_all)) {
  idx <- ((i - 1) * S + 1):(i * S)
  
  mipme_z_t[idx, idx] <- mipme_z_t[idx, idx] + mipme_mrm_all[[i]]
}




# Multiplicadores de oferta con uso importado ---------------------------------------



# Coeficientes técnicos totales
mipme_a_t <- sweep(mipme_z_t, 2, mipme_x, "/")
mipme_a_t[!is.finite(mipme_a_t)] <- 0

# Inversa total
I <- diag(1, nrow = nrow(mipme_a_t))
mipme_L_t <- solve(I - mipme_a_t)

# Regional Multipliers
# colSums = backward output multipliers (shocks to final demand)
# rowSums = forward output multipliers
mipme_mu_t <- tibble(
  n = seq_len(ncol(mipme_L_t)),
  mu_e = colSums(mipme_L_t)
) %>%
  left_join(mipme_index, by = "n")



mipme_mu_t %>% group_by(NOM_ENT) %>% 
  summarise(mu_avg = mean(mu_e)) %>% 
  arrange(-mu_avg) %>% 
  view()


