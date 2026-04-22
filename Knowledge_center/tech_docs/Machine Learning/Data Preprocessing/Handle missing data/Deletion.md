## What is Deletion?
Deletion is the process of removing data from your dataset to handle missing values. Instead of trying to guess or calculate what the missing values might be, you simply discard the data points that have them. It is the most direct and simplest strategy for dealing with NaNs (Not a Number) or null values.

---
#### How to Do It (The Two Main Types)
There are two primary ways to perform deletion:

Listwise Deletion (Row Deletion):

How it works: If a row in your dataset contains at least one missing value in any of its columns, the entire row is removed.
Analogy: You are conducting a survey. If a person skips even a single question, you throw out their entire survey form.
Column Deletion (Feature Deletion):

How it works: If a column (feature) contains a high percentage of missing values, the entire column is removed from the dataset.
Analogy: You ask a survey question that almost nobody answers. You conclude the question is useless and remove it from your analysis entirely.

---
#### What Problem Does It Solve?
The primary problem it solves is model compatibility. Most machine learning algorithms in libraries like scikit-learn cannot handle missing data. If you try to train a model on a dataset containing NaN values, the program will crash with an error.

Deletion provides a quick and easy way to create a "complete" dataset that can be fed directly into a machine learning model without causing errors.

---
#### Advantages (When to Use It)
- Simplicity: It is extremely easy to understand and implement, often requiring just a single line of code.
No Data Distortion: Unlike imputation (filling in values), it doesn't create any "synthetic" data. The remaining data is all original and unaltered.
- When Missing Data is Small: If you have a very large dataset and only a tiny fraction of rows have missing values (e.g., < 5%), deleting them is a safe and reasonable approach as the information loss is minimal.
- When a Column is Mostly Empty: If a feature is missing for a very high percentage of observations (e.g., > 60-70%), the feature is likely not useful and may add more noise than signal. Deleting the column is a good choice.
- When Data is Missing Completely at Random (MCAR): If the fact that a value is missing is completely random and has no relationship to any other data, deleting the row will not introduce bias into your model.

---
#### Disadvantages (When Not to Use It)
- Significant Information Loss: This is the biggest drawback. You are throwing away data. Even if one value is missing in a row, the other values in that same row could have contained valuable information.
- Can Introduce Severe Bias: This is the most dangerous drawback. If the data is not missing completely at random, deletion can create a biased dataset.
- Example: Imagine you are predicting income, and people with very high incomes are less likely to report it. If you delete all rows with missing income, your model will be trained almost exclusively on low and middle-income individuals. It will perform very poorly when predicting high incomes because it has never seen them.
- Reduces Dataset Size: This reduces the statistical power of your analysis and can lead to less reliable and less generalizable models, especially if your initial dataset is small.
- Don't use it when the dataset is small. Every data point is precious.
- Don't use it when a very important predictive feature has missing values. You are better off trying to impute the values than deleting the feature or the rows.

---
#### Python code

```
import pandas as pd
import numpy as np

# Create a sample DataFrame with missing values
data = {
    'age': [25, 30, np.nan, 35, 40],
    'income': [50000, 60000, 55000, np.nan, 70000],
    'gender': ['Male', 'Female', 'Female', 'Male', 'Male'],
    'survey_notes': ['Good', np.nan, np.nan, np.nan, 'Okay'] # This column is mostly empty
}
df = pd.DataFrame(data)

print("Original DataFrame:")
print(df)
print("-" * 30)


# --- Part 1: Listwise (Row) Deletion ---
# Remove any row that has at least one NaN value.
df_rows_deleted = df.dropna()

print("DataFrame after deleting rows with any missing values:")
print(df_rows_deleted)
# Notice that only the first and last rows remain, as they were the only complete ones.
print("-" * 30)


# --- Part 2: Column Deletion ---
# A more robust way to delete columns is based on a threshold.

# First, calculate the percentage of missing values in each column
missing_percentage = df.isnull().sum() / len(df) * 100
print("Percentage of missing values per column:")
print(missing_percentage)
print("-" * 20)

# Define a threshold for dropping columns
threshold = 60.0 # Drop columns with 60% or more missing values

# Identify columns to drop
cols_to_drop = missing_percentage[missing_percentage > threshold].index
print(f"Columns to drop (>{threshold}% missing): {list(cols_to_drop)}")

# Drop the identified columns
df_cols_deleted = df.drop(columns=cols_to_drop)

print("\nDataFrame after deleting columns with >60% missing values:")
print(df_cols_deleted)
# Notice that the 'survey_notes' column is gone.
```