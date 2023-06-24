# Import libraries

library("readxl")   # Package to read excel files
library("rhoR")     # Package to calculate Shaffer’s rho
library("irr")      # Package to calculate Krippendorff’s Alpha
library("tibble")   


###############################################################################


# Declare functions

# Function to remove corresponding NAs from 2 columns
rm_corr_na <- function(x1, x2) {
    if (length(x1) > length(x2)) {
        x1 <- head(x1, length(x2) - length(x1))
    }
    if (length(x2) > length(x1)) {
        x2 <- head(x2, length(x1) - length(x2))
    }
    temp_df <- data.frame("a" = x1, "b" = x2)
    temp_df <- na.omit(temp_df)
    return(temp_df)
}

# Function to encode a vector
encode <- function(x) {
    x <- as.numeric(factor(x, levels = unique(x), exclude = NULL))
    return(x)
}

# Function to split a vector in 2
split_in_2 <- function(x) {
    chunk_len <- length(x) / 2
    chunks <- split(x, ceiling(seq_along(x) / chunk_len))
    return(chunks)
}

# Function to calculate Krippendorff’s Alpha
kripp_alpha <- function(col1, col2) {
    na_df <- rm_corr_na(col1, col2)
    col1 <- na_df$a
    col2 <- na_df$b
    concat_col <- encode(c(col1, col2))
    concat_col <- split_in_2(concat_col)
    col1 <- concat_col$"1"
    col2 <- concat_col$"2"
    content <- tibble(col1, col2)
    content <- t(content)
    content <- as.matrix(content)
    alpha <- kripp.alpha(content)$value
    return(alpha)
}

# Function to create contingency table
create_contingency_table <- function(x1, x2) {
    x1 <- sapply(x1, function(x) x - 1)
    x2 <- sapply(x2, function(x) x - 1)
    p1p2 <- 0 # Rater 1 Positive & Rater 2 Positive
    n1p2 <- 0 # Rater 1 Negative & Rater 2 Positive
    p1n2 <- 0 # Rater 1 Positive & Rater 2 Negative
    n1n2 <- 0 # Rater 1 Negative & Rater 2 Negative
    for (ele in seq_along(x1)) {
        if (x1[ele] == 1 && x2[ele] == 1) {
            p1p2 <- p1p2 + 1
        }
        if (x1[ele] == 0 && x2[ele] == 1) {
            n1p2 <- n1p2 + 1
        }
        if (x1[ele] == 1 && x2[ele] == 0) {
            p1n2 <- p1n2 + 1
        } else {
            n1n2 <- n1n2 + 1
        }
    }
    return(matrix(c(p1p2, n1p2, p1n2, n1n2), nrow = 2, ncol = 2))
}

# Function to calculate Shaffer's Rho
shaffer_rho <- function(col1, col2) {
    na_df <- rm_corr_na(col1, col2)
    col1 <- na_df$a
    col2 <- na_df$b
    if (length(unique(col1)) > 2) {
        return("NaN")
    }
    concat_col <- encode(c(col1, col2))
    concat_col <- split_in_2(concat_col)
    col1 <- concat_col$"1"
    col2 <- concat_col$"2"
    ct <- create_contingency_table(col1, col2)
    rho_val <- rho(ct)$rho
    return(rho_val)
}

# Function to calculate Cohen's Kappa
cohen_kappa <- function(col1, col2) {
    na_df <- rm_corr_na(col1, col2)
    col1 <- na_df$a
    col2 <- na_df$b
    if (length(unique(col1)) > 2) {
        return("NaN")
    }
    concat_col <- encode(c(col1, col2))
    concat_col <- split_in_2(concat_col)
    col1 <- concat_col$"1"
    col2 <- concat_col$"2"
    ct <- create_contingency_table(col1, col2)
    rho_val <- rho(ct)$kappa
    return(rho_val)
}


###############################################################################


# Main code

# Read rater codings
coder_1_data <- read_excel("./coder_1.xlsx")
coder_2_data <- read_excel("./coder_2.xlsx")

# Rename column names
new_colnames <- c(
    "S.No", "Tweet", "Date.Of.Tweet", "Topic", "Parent.Tweet", "Language",
    "Quality", "Agreement", "Disagreement", "Deep.Argumentation",
    "Shallow.Argumentation", "Tone", "Writer.Character", "Remark", "Relevancy"
)
colnames(coder_1_data) <- new_colnames
colnames(coder_2_data) <- new_colnames

# Iterate through columns
for (col in colnames(coder_1_data)) {
    # Skip the following columns
    if (col %in% c(
        "S.No", "Tweet", "Date.Of.Tweet",
        "Topic", "Parent.Tweet", "Language"
    )) {
        next
    }
    cat(col, "\n")
    # Print Krippendorff’s Alpha
    cat("Krippendorff’s Alpha:")
    # Print Shaffer's Rho
    cat(kripp_alpha(coder_1_data[[col]], coder_2_data[[col]]), "\n")
    # Print Shaffer's Rho
    cat("Shaffer's Rho:")
    cat(shaffer_rho(coder_1_data[[col]], coder_2_data[[col]]), "\n")
    # Print Cohen's Kappa
    cat("Cohen's Kappa:")
    cat(cohen_kappa(coder_1_data[[col]], coder_2_data[[col]]), "\n")
    cat("\n")
}