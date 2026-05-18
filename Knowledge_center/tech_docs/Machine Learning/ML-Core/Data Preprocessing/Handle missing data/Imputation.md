## What is Imputation?
Imputation is the process of replacing missing data with substituted values. Instead of throwing away data points that have missing values (deletion), you make an "educated guess" about what the missing value might be and fill it in.

The goal is to preserve your data, allowing you to use the other valuable information in a row or column, while still making your dataset complete and usable for machine learning models.

---
#### How to Do It (The Main Types)
Imputation methods range from simple and fast to complex and computationally intensive.

1. Simple (Univariate) Imputation
These methods only use the information from the column containing the missing value.

- Mean Imputation: Replace the missing values with the mean of the column.
Best for: Numerical data that is normally distributed and has no significant outliers.
- Median Imputation: Replace the missing values with the median of the column.
Best for: Numerical data that is skewed or contains outliers, as the median is less sensitive to extreme values.
- Mode Imputation (Most Frequent): Replace the missing values with the most frequent value (the mode) in the column.
Best for: Categorical (non-numeric) features.
Constant Value Imputation: Replace the missing values with a fixed, arbitrary value (e.g., 0, -1, or "Unknown").
Best for: When you want the model to explicitly learn that the value was missing. This is often used in conjunction with creating a "was_missing" indicator column.
2. Advanced (Multivariate) Imputation
These methods use information from other columns in the dataset to make a more intelligent guess.

- K-Nearest Neighbors (KNN) Imputation: For a missing value, it finds the 'k' most similar rows (its "neighbors") based on the other features. It then imputes the missing value by taking the average (for numerical) or mode (for categorical) of the values from those neighbors.
- Multivariate Imputation by Chained Equations (MICE): This is a very powerful technique. It treats the column with missing values as a target variable and builds a regression or classification model to predict the missing values based on the other features in the dataset. It often does this iteratively to refine its predictions.

---
#### What Problem Does It Solve?
Like deletion, imputation solves the problem of model compatibility by getting rid of NaN values. However, its primary goal is to do this while avoiding the information loss that comes with deletion. It allows you to keep your valuable rows and columns, preserving the size and statistical power of your dataset.

---
#### Advantages
- Preserves Data: This is the biggest advantage. It allows you to keep all your rows, which is especially important for smaller datasets.
- Maintains Statistical Power: By keeping the dataset size intact, it leads to more reliable and stable models.
- Can Improve Model Performance: Advanced imputation methods that capture relationships between variables can result in more accurate models than if the data were simply deleted.

---
#### Disadvantages
- Distorts Data Distribution: This is the most significant drawback. Imputation adds "synthetic" data. Simple methods like mean/median imputation can artificially reduce the natural variance of a feature, as they pull all the imputed values to a single point.
- Can Introduce Bias: If the wrong imputation method is chosen, it can introduce bias and distort the relationships between variables.
- Ignores Relationships (for simple methods): Mean, median, and mode imputation don't account for the relationships between features. For example, imputing the average income for a missing value ignores whether the person is a CEO or an intern.
- Complexity and Computational Cost: Advanced methods like MICE are much more complex to implement and can be computationally expensive on large datasets.

---
#### When to Use It
- When the amount of missing data is low to moderate (e.g., 5-40%).
- When deleting data would mean losing a significant portion of your dataset.
- When the missing values are thought to be Missing at Random (MAR), meaning the missingness can be explained by other variables in the dataset (this is the ideal scenario for multivariate imputation).
- When you want to preserve the dataset size to maintain statistical power.

---
#### When Not to Use It
- When a column is almost entirely empty (e.g., > 70-80% missing). In this case, the column likely contains no useful information, and deleting the column is a better choice.
- When the missingness itself is a powerful predictive signal. In this case, you might be better off using Constant Value Imputation (e.g., creating a category called "Unknown") so the model can learn from the absence of a value.

---
#### Python code 

```
import pandas as pd
import numpy as np
# Import imputers from scikit-learn
from sklearn.impute import SimpleImputer, KNNImputer

# Create a sample DataFrame with missing values
data = {
    'age': [25, 30, np.nan, 35, 40],
    'income': [50000, 60000, 55000, np.nan, 70000],
    'department': ['Sales', 'IT', 'IT', np.nan, 'Sales']
}
df = pd.DataFrame(data)
print("Original DataFrame:")
print(df)
print("-" * 30)

# --- Part 1: Simple Imputation with Pandas ---
# This is quick for exploration.
df_pandas_imputed = df.copy()
# Impute 'age' with the mean
df_pandas_imputed['age'].fillna(df['age'].mean(), inplace=True)
# Impute 'department' with the mode
df_pandas_imputed['department'].fillna(df['department'].mode()[0], inplace=True)
print("DataFrame after simple Pandas imputation:")
print(df_pandas_imputed)
print("-" * 30)


# --- Part 2: Imputation with Scikit-learn (Recommended for ML Pipelines) ---
# Create copies for demonstration
df_simple_imputed = df.copy()
df_knn_imputed = df.copy()

# A. SimpleImputer for numerical and categorical data
# For numerical features (using median for robustness)
num_imputer = SimpleImputer(strategy='median')
df_simple_imputed[['age', 'income']] = num_imputer.fit_transform(df_simple_imputed[['age', 'income']])

# For categorical features
cat_imputer = SimpleImputer(strategy='most_frequent')
df_simple_imputed[['department']] = cat_imputer.fit_transform(df_simple_imputed[['department']])

print("DataFrame after scikit-learn SimpleImputer:")
print(df_simple_imputed)
print("-" * 30)


# B. KNNImputer for a more advanced approach
# NOTE: KNNImputer only works on numerical data and is sensitive to scale.
# You would typically scale your data first in a real pipeline.
# We will only impute the numerical columns here.
knn_imputer = KNNImputer(n_neighbors=2)
df_knn_imputed[['age', 'income']] = knn_imputer.fit_transform(df_knn_imputed[['age', 'income']])

print("DataFrame after scikit-learn KNNImputer (on numerical columns):")
print(df_knn_imputed)
# Notice the imputed values for age (32.5) and income (65000) are derived from their "neighbors".
```