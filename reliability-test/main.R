# Import libraries

library("readxl")   # Package to read excel files
# library("rhoR")     # Package to calculate Shaffer’s rho
# library("irr")      # Package to calculate Krippendorff’s Alpha


###############################################################################


# Declare functions

kripp_alpha <- function(col1, col2) {
    cat(length(col1), '\n')
    cat(length(col2), '\n')
}


###############################################################################


# Read rater codings
coder_1_data <- read_excel("./coder_1.xlsx")
coder_2_data <- read_excel("./coder_2.xlsx")

# Remove rows with NA
coder_1_data <- na.omit(coder_1_data)
coder_2_data <- na.omit(coder_2_data)

# for (col in colnames(coder_1_data)) {
#     cat(col, '\n')
# }

# Rename column names
new_colnames <- c(
    'S.No', 'Tweet', 'Date.Of.Tweet', 'Topic', 'Parent.Tweet', 'Language', 
    'Quality', 'Agreement', 'Disagreement', 'Deep.Argumentation',
    'Shallow.Argumentation', 'Tone', 'Writer.Character', 'Remark', 'Relevancy'
)
colnames(coder_1_data) <- new_colnames
colnames(coder_2_data) <- new_colnames

kripp_alpha(coder_1_data$Quality, coder_2_data$Quality)
