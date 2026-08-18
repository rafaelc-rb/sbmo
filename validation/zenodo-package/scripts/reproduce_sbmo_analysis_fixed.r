# Reproducible analysis of the SBMO validation survey
# Designed for RStudio; requires only base R.
#
# Methodological references:
# - RV coefficient: Escoufier (1973), Biometrics 29(4), 751–760.
# - Permutation tests: Good (2005), Permutation, Parametric, and Bootstrap
#   Tests of Hypotheses, 3rd ed.
# - False-discovery-rate adjustment: Benjamini & Hochberg (1995), JRSS B 57,
#   289–300.
# - Fisher's exact test: Fisher (1922), JRSS 85, 87–94.
# - Phi effect size: Cohen (1988), Statistical Power Analysis, 2nd ed.

options(stringsAsFactors = FALSE)
set.seed(20260815)

# Set the path below, define environment variable SBMO_CSV, or pass the CSV path
# as the first command-line argument when running with Rscript.
args <- commandArgs(trailingOnly = TRUE)
input_csv <- if (length(args) >= 1) args[1] else Sys.getenv("SBMO_CSV")
if (!nzchar(input_csv)) {
  input_csv <- "SBMO — Validação de Modelo de Negócio de Software (respostas) - Respostas ao formulário 1.csv"
}
if (!file.exists(input_csv)) stop("CSV not found. Set input_csv or SBMO_CSV to the survey file path.")

output_dir <- "sbmo_analysis_output"
dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)
dat <- read.csv(input_csv, check.names = FALSE, fileEncoding = "UTF-8-BOM")
names(dat) <- trimws(gsub("[[:space:]]+", " ", names(dat)))
stopifnot(nrow(dat) == 31)

# FIX (2026-08-18): the raw Google Forms export delimits multiple selections
# within a multi-select cell with ";", not ",". Option labels themselves
# contain "," inside parentheses (e.g. "Receita por assinatura (pagamentos
# periódicos recorrentes)"), so splitting on "," (even with the original
# depth-tracking guard) produced spurious extra "categories" and merged
# distinct selections into single strings joined by ";" — this silently
# inflated ObservedClasses (e.g. Product/service type: 8 expected vs 18
# observed) and invalidated every downstream statistic (coverage, RV,
# phi/Fisher). Verified against the actual header/cell content of
# validations/sbmo-form-answers.csv. Splitting on ";" requires no
# parenthesis-depth tracking, since ";" never occurs inside an option label.
split_multiselect <- function(x) {
  if (is.na(x) || !nzchar(trimws(x))) return(character(0))
  out <- trimws(strsplit(trimws(x), ";", fixed = TRUE)[[1]])
  out <- out[nzchar(out)]
  out
}

dimension_columns <- c(
  "Product/service type" = "Tipo de produto ou serviço",
  "Delivery mode" = "Modo de entrega",
  "Revenue source" = "Fontes de receita",
  "Pricing strategy" = "Estratégia de precificação",
  "Customer type" = "Tipo de cliente",
  "Ecosystem role" = "Papel no ecossistema",
  "Acquisition channel" = "Canal de aquisição",
  "IP regime" = "Regime de propriedade intelectual",
  "Pricing base unit" = "Unidade base de precificação",
  "Network effect" = "Tipo de efeito de rede",
  "Success factor" = "Fatores de sucesso",
  "Implementation challenge" = "Desafios de implementação",
  "Mitigation strategy" = "Estratégias de mitigação"
)

make_matrix <- function(column) {
  parsed <- lapply(dat[[column]], split_multiselect)
  categories <- sort(unique(unlist(parsed)))
  x <- sapply(categories, function(z) as.integer(vapply(parsed, function(v) z %in% v, logical(1))))
  if (is.null(dim(x))) x <- matrix(x, ncol = 1)
  colnames(x) <- categories
  x
}
matrices <- lapply(dimension_columns, make_matrix)

# Anonymized processed matrix.
case_id <- sprintf("Case%02d", seq_len(nrow(dat)))
org_raw <- trimws(dat[["Nome da empresa"]])
declined <- tolower(org_raw) %in% c("não indentificada", "não quero informar", "prefiro não dizer")
org_id <- match(tolower(org_raw), unique(tolower(org_raw)))
org_cluster <- sprintf("ORG_%02d", org_id)
org_cluster[declined] <- sprintf("ORG_ANON_%02d", seq_len(sum(declined)))
product_cluster <- sprintf("PROD_%02d", match(tolower(trimws(dat[["Nome do produto ou serviço"]])), unique(tolower(trimws(dat[["Nome do produto ou serviço"]])))))

processed <- data.frame(
  CaseID = case_id,
  OrganizationClusterID = org_cluster,
  ProductClusterID = product_cluster,
  LaunchYear = suppressWarnings(as.numeric(dat[["Ano de lançamento"]])),
  KnowledgeScore = suppressWarnings(as.numeric(dat[["Qual o seu conhecimento sobre o modelo de negócio deste produto/serviço?"]])),
  OperationalStatus = dat[["O modelo de negócio deste produto/serviço já está operacional?"]],
  check.names = FALSE
)
for (nm in names(matrices)) {
  processed[[paste0("Count__", nm)]] <- rowSums(matrices[[nm]])
  z <- matrices[[nm]]
  colnames(z) <- paste0(nm, "__", colnames(z))
  processed <- cbind(processed, z)
}
processed$Missing__LaunchYear <- as.integer(is.na(processed$LaunchYear))
processed$Missing__KnowledgeScore <- as.integer(is.na(processed$KnowledgeScore))
write.csv(processed, file.path(output_dir, "processed_data.csv"), row.names = FALSE, fileEncoding = "UTF-8")

# Descriptive statistics and vocabulary coverage.
status_table <- data.frame(Status = c("Sim", "Parcialmente", "Não"))
status_table$n <- as.integer(table(factor(processed$OperationalStatus, levels = status_table$Status)))
status_table$percentage <- 100 * status_table$n / nrow(processed)
write.csv(status_table, file.path(output_dir, "operational_status.csv"), row.names = FALSE)

is_other <- function(label) grepl("^Outro", label, ignore.case = TRUE)
coverage <- do.call(rbind, lapply(names(matrices), function(nm) {
  x <- matrices[[nm]]
  other <- if (any(is_other(colnames(x)))) sum(rowSums(x[, is_other(colnames(x)), drop = FALSE]) > 0) else 0
  data.frame(Dimension = nm, Valid = sum(!is.na(dat[[dimension_columns[[nm]]]])), Other = other,
             Coverage = 1 - other / nrow(dat), ObservedClasses = ncol(x))
}))
write.csv(coverage, file.path(output_dir, "coverage.csv"), row.names = FALSE)

frequencies <- do.call(rbind, lapply(names(matrices), function(nm) {
  n <- colSums(matrices[[nm]])
  data.frame(Dimension = nm, Option = names(n), n = as.integer(n), Percentage = 100*n/nrow(dat))
}))
frequencies <- frequencies[order(frequencies$Dimension, -frequencies$n), ]
write.csv(frequencies, file.path(output_dir, "option_frequencies.csv"), row.names = FALSE)

# RV coefficient and row-permutation test.
rv_coefficient <- function(x, y) {
  x <- scale(x, center = TRUE, scale = FALSE); y <- scale(y, center = TRUE, scale = FALSE)
  numerator <- sum(crossprod(x, y)^2)
  denominator <- sqrt(sum(crossprod(x)^2) * sum(crossprod(y)^2))
  if (denominator == 0) return(NA_real_)
  numerator / denominator
}
rv_test <- function(x, y, permutations = 9999L) {
  observed <- rv_coefficient(x, y)
  permuted <- replicate(permutations, rv_coefficient(x, y[sample.int(nrow(y)), , drop = FALSE]))
  c(RV = observed, p = (1 + sum(permuted >= observed - .Machine$double.eps)) / (permutations + 1))
}

pairs <- list(
  CQ1 = c("Revenue source", "Delivery mode"),
  CQ2 = c("Pricing strategy", "Revenue source"),
  CQ3 = c("Customer type", "Acquisition channel"),
  CQ4 = c("Ecosystem role", "Network effect"),
  CQ5 = c("Success factor", "Implementation challenge"),
  CQ6 = c("Mitigation strategy", "Implementation challenge")
)
association_results <- do.call(rbind, lapply(names(pairs), function(cq) {
  pair <- pairs[[cq]]; z <- rv_test(matrices[[pair[1]]], matrices[[pair[2]]])
  data.frame(CQ = cq, DimensionA = pair[1], DimensionB = pair[2], RV = z["RV"], PermutationP = z["p"])
}))
association_results$BH_q <- p.adjust(association_results$PermutationP, method = "BH")
write.csv(association_results, file.path(output_dir, "rv_associations.csv"), row.names = FALSE)

# Sensitivity analysis: retain first response for each organization label.
first_by_org <- !duplicated(tolower(org_raw))
sensitivity <- do.call(rbind, lapply(names(pairs), function(cq) {
  pair <- pairs[[cq]]
  z <- rv_test(matrices[[pair[1]]][first_by_org, , drop = FALSE], matrices[[pair[2]]][first_by_org, , drop = FALSE])
  data.frame(CQ = cq, RV = z["RV"], PermutationP = z["p"])
}))
write.csv(sensitivity, file.path(output_dir, "sensitivity_analysis.csv"), row.names = FALSE)

# Descriptive strongest binary association for each competency-question pair.
phi_coefficient <- function(x, y) {
  if (sd(x) == 0 || sd(y) == 0) return(NA_real_)
  cor(x, y)
}
strongest <- do.call(rbind, lapply(names(pairs), function(cq) {
  pair <- pairs[[cq]]; x <- matrices[[pair[1]]]; y <- matrices[[pair[2]]]
  candidates <- expand.grid(i = seq_len(ncol(x)), j = seq_len(ncol(y)))
  candidates <- candidates[colSums(x)[candidates$i] >= 3 & colSums(x)[candidates$i] <= 28 &
                             colSums(y)[candidates$j] >= 3 & colSums(y)[candidates$j] <= 28 &
                             !is_other(colnames(x)[candidates$i]) & !is_other(colnames(y)[candidates$j]), ]
  candidates$phi <- mapply(function(i,j) phi_coefficient(x[,i],y[,j]), candidates$i,candidates$j)
  best <- candidates[which.max(abs(candidates$phi)),]
  tab <- table(factor(x[,best$i],0:1),factor(y[,best$j],0:1))
  ft <- fisher.test(tab)
  data.frame(CQ=cq, OptionA=colnames(x)[best$i], OptionB=colnames(y)[best$j], Phi=best$phi,
             FisherP=ft$p.value, OddsRatio=unname(ft$estimate))
}))
write.csv(strongest, file.path(output_dir, "strongest_binary_pairs.csv"), row.names = FALSE)

# Base-R figures.
png(file.path(output_dir, "operational_status.png"), width = 1600, height = 1000, res = 180)
barplot(status_table$n, names.arg = c("Operational", "Partially", "Planning"), col = "#2F75B5",
        ylab = "Number of cases", main = "Operational status", ylim = c(0,25))
text(seq_along(status_table$n), status_table$n, labels = status_table$n, pos = 3)
dev.off()

png(file.path(output_dir, "vocabulary_coverage.png"), width = 1800, height = 1400, res = 180)
par(mar = c(5, 12, 3, 2)); bp <- barplot(100*coverage$Coverage, names.arg = coverage$Dimension,
  horiz = TRUE, las = 1, xlim = c(75,105), col = "#2F75B5", xlab = "Coverage (%)", main = "Controlled-vocabulary coverage")
text(100*coverage$Coverage, bp, labels = sprintf("%.1f",100*coverage$Coverage), pos = 4)
dev.off()

png(file.path(output_dir, "rv_coefficients.png"), width = 1500, height = 1000, res = 180)
bp <- barplot(association_results$RV, names.arg = association_results$CQ, horiz = TRUE, las = 1,
  xlim = c(0,.65), col = "#2F75B5", xlab = "RV coefficient", main = "Multivariate associations")
text(association_results$RV, bp, labels = sprintf("%.2f",association_results$RV), pos = 4)
dev.off()

writeLines(capture.output(sessionInfo()), file.path(output_dir, "sessionInfo.txt"))
message("Analysis complete. Outputs written to: ", normalizePath(output_dir))
