# R/analysis_wrappers.R
# Reusable analysis functions for STAT 6179 — Part II

# --- small validator (assumes you've already cleaned names) ---
.require_cols <- function(df, cols) {
  miss <- setdiff(cols, names(df))
  if (length(miss)) stop("Missing cols: ", paste(miss, collapse = ", "))
  invisible(TRUE)
}

# --- S3 class helper ---
.as_project_result <- function(x, type) {
  x$type <- type
  class(x) <- c("project_result", class(x))
  x
}

#' Linear relation: Weight ~ Height (with plot)
#' @return project_result list: slope, ci, r2, p, model, plot
analyze_height_weight <- function(df) {
  .require_cols(df, c("Height","Weight"))
  mod <- stats::lm(Weight ~ Height, data = df)
  s   <- summary(mod)
  p   <- stats::pf(s$fstatistic[1], s$fstatistic[2], s$fstatistic[3], lower.tail = FALSE)
  r2  <- unname(s$r.squared)
  
  # 95% CI for slope
  slope_ci <- stats::confint(mod)["Height", ]
  
  # ggplot
  if (!requireNamespace("ggplot2", quietly = TRUE)) install.packages("ggplot2")
  library(ggplot2)
  plt <- ggplot(df, aes(Height, Weight)) +
    geom_point(alpha = 0.6) +
    geom_smooth(method = "lm", se = TRUE) +
    labs(
      title = "Weight vs Height with fitted line",
      subtitle = sprintf("R² = %.3f, p = %.1e", r2, p),
      x = "Height (cm)", y = "Weight (kg)"
    ) +
    theme_minimal(base_size = 11) +
    theme(panel.grid.minor = element_blank(), plot.title.position = "plot")
  
  .as_project_result(list(
    slope = unname(coef(mod)[["Height"]]),
    slope_ci = unname(slope_ci),
    r2 = r2,
    p = p,
    model = mod,
    plot = plt
  ), "lm_height_weight")
}

#' Two-sample t-test: mean Height by Gender (equal variances)
#' @return project_result list: diff (Male-Female), ci, p, df, var_test_p, plot
compare_mean_height <- function(df) {
  .require_cols(df, c("Height","Gender"))
  df$Gender <- factor(df$Gender, levels = c("Female","Male"))
  
  tt  <- stats::t.test(Height ~ Gender, data = df, var.equal = TRUE)
  vt  <- stats::var.test(Height ~ Gender, data = df)
  
  if (!requireNamespace("ggplot2", quietly = TRUE)) install.packages("ggplot2")
  library(ggplot2)
  plt <- ggplot(df, aes(Gender, Height)) +
    geom_point(position = position_jitter(width = 0.15, height = 0), alpha = 0.35) +
    stat_summary(fun = mean, geom = "crossbar", width = 0.5, fatten = 2) +
    labs(title = "Heights by gender (bold line = mean)", x = NULL, y = "Height (cm)") +
    theme_minimal(base_size = 11) +
    theme(panel.grid.minor = element_blank(), legend.position = "none")
  
  diff_M_minus_F <- unname(diff(rev(tt$estimate))) # Male - Female
  
  .as_project_result(list(
    diff = diff_M_minus_F,
    ci = unname(tt$conf.int),
    p = unname(tt$p.value),
    df = unname(tt$parameter),
    var_test_p = unname(vt$p.value),
    plot = plt
  ), "ttest_height_by_gender")
}

#' Chi-square: Gender × Physical.Activity
#' @return project_result list: table, expected, stat, df, p, plot
assoc_gender_activity <- function(df) {
  .require_cols(df, c("Gender","Physical.Activity"))
  df$Gender <- factor(df$Gender, levels = c("Female","Male"))
  df$Physical.Activity <- factor(df$Physical.Activity, levels = c("None","Moderate","Intense"))
  
  tab <- table(df$Gender, df$Physical.Activity)
  chi <- stats::chisq.test(tab, correct = FALSE)
  
  if (!requireNamespace("ggplot2", quietly = TRUE)) install.packages("ggplot2")
  if (!requireNamespace("scales", quietly = TRUE)) install.packages("scales")
  library(ggplot2); library(scales)
  plt <- as.data.frame(tab) |>
    setNames(c("Gender","Activity","Freq")) |>
    ggplot(aes(Activity, Freq, fill = Gender)) +
    geom_col(position = "fill") +
    scale_y_continuous(labels = percent_format()) +
    labs(title = "Activity distribution within each gender",
         x = "Physical Activity", y = "Proportion within gender", fill = "Gender") +
    theme_minimal(base_size = 11) +
    theme(panel.grid.minor = element_blank(), legend.position = "top")
  
  .as_project_result(list(
    table = tab,
    expected = chi$expected,
    statistic = unname(chi$statistic),
    df = unname(chi$parameter),
    p = unname(chi$p.value),
    plot = plt
  ), "chisq_gender_activity")
}

# --- S3 print method for concise console output ---
#' @export
# helper: NULL-coalescing
`%||%` <- function(a, b) if (is.null(a)) b else a

# --- S3 print method for concise console output ---
print.project_result <- function(x, ...) {
  t <- as.character(x$type %||% "")
  if (t == "lm_height_weight") {
    cat(sprintf(
      "Linear model (Weight ~ Height): slope = %.3f kg/cm, 95%% CI [%.3f, %.3f], R^2 = %.3f, p = %.3g\n",
      x$slope, x$slope_ci[1], x$slope_ci[2], x$r2, x$p
    ))
  } else if (t == "ttest_height_by_gender") {
    cat(sprintf(
      "Two-sample t-test (Male - Female): diff = %.2f cm, 95%% CI [%.2f, %.2f], t(%g), p = %.3g; var-test p = %.3g\n",
      x$diff, x$ci[1], x$ci[2], x$df, x$p, x$var_test_p
    ))
  } else if (t == "chisq_gender_activity") {
    cat(sprintf(
      "Chi-square: X^2(%g) = %.2f, p = %.3g\n",
      x$df, x$statistic, x$p
    ))
  } else {
    NextMethod()
  }
  invisible(x)
}


