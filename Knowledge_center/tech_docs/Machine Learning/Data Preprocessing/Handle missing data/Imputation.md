Simple Imputation:
Mean: Replace missing values with the mean of the column. Good for normally distributed data.
Median: Replace with the median. Better for skewed data or data with outliers.
Mode: Replace with the most frequent value. Used for categorical features.
Constant Value: Replace with a fixed value like 0, -1, or "Unknown".
Advanced Imputation:
K-Nearest Neighbors (KNN) Imputation: Finds the 'k' most similar rows (based on other features) and uses their values to impute the missing one.
Multivariate Imputation (e.g., MICE): Builds a model to predict the missing values based on other features. More complex but often more accurate.