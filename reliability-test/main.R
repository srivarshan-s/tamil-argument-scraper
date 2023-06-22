# Import libraries

library("readxl") # Package to read excel files
# library("rhoR")     # Package to calculate Shaffer’s rho
library("irr") # Package to calculate Krippendorff’s Alpha
library("tibble")


###############################################################################


# Declare functions

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

encode <- function(x) {
    x <- as.numeric(factor(x, levels = unique(x), exclude = NULL))
    return(x)
}

split_in_2 <- function(x) {
    chunk_len <- length(x) / 2
    chunks <- split(x, ceiling(seq_along(x) / chunk_len))
    return(chunks)
}

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
    alpha <- kripp.alpha(content, method = "interval")$value
    return(alpha)
}


###############################################################################


# Read rater codings
coder_1_data <- read_excel("./coder_1.xlsx")
coder_2_data <- read_excel("./coder_2.xlsx")

# Remove rows with NA
# coder_1_data <- na.omit(coder_1_data)
# coder_2_data <- na.omit(coder_2_data)

# for (col in colnames(coder_1_data)) {
#     cat(col, '\n')
# }

# Rename column names
new_colnames <- c(
    "S.No", "Tweet", "Date.Of.Tweet", "Topic", "Parent.Tweet", "Language",
    "Quality", "Agreement", "Disagreement", "Deep.Argumentation",
    "Shallow.Argumentation", "Tone", "Writer.Character", "Remark", "Relevancy"
)
colnames(coder_1_data) <- new_colnames
colnames(coder_2_data) <- new_colnames

for (col in colnames(coder_1_data)) {
    if (col %in% c(
        "S.No", "Tweet", "Date.Of.Tweet",
        "Topic", "Parent.Tweet", "Language"
    )) {
        next
    }
    cat(col, "\n")
    cat("Krippendorff’s Alpha:")
    cat(kripp_alpha(coder_1_data[[col]], coder_2_data[[col]]), "\n")
    cat("\n")
}
