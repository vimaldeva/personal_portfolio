## Column/Feature Review

#### What Does It Do?
Column/Feature Review is the process of moving from a high-level overview of the dataset to a more detailed examination of each individual column. While the Initial Data Inspection checks the overall structure, this step focuses on understanding the content, characteristics, and quality of each feature.

It involves three main activities:

- Listing and Cleaning: Identifying and standardizing the column names.
- Summarizing Numerical Features: Calculating key statistics (like mean, median, min, max) to understand their scale, central tendency, and spread.
- Summarizing Categorical Features: Counting unique categories and their frequencies to understand the composition of text-based features.

---
#### Python code
```
import pandas as pd
import numpy as np

# Create a sample DataFrame with common issues
data = {
    'Employee ID': [101, 102, 103, 104, 105, 106],
    'Department': ['Sales', 'IT', 'IT', 'Sales', 'Marketing', 'IT'],
    'Age': [25, 42, 31, 55, 29, 99], # 99 might be an outlier or error
    'Salary': [50000, 120000, 85000, 75000, 60000, 950000] # 950k is a huge outlier
}
df = pd.DataFrame(data)


# --- The Review Steps ---

# 1. List and Clean Column Names
print("--- 1. Original Column Names ---")
print(df.columns)
# Insight: The names have spaces and mixed cases, which can be annoying to work with.

# Clean the names: remove spaces, convert to lowercase
df.columns = df.columns.str.lower().str.replace(' ', '_')
print("\n--- Cleaned Column Names ---")
print(df.columns)


# 2. Get a Statistical Summary of Numerical Columns
print("\n--- 2. Numerical Summary (.describe()) ---")
print(df.describe())
# INSIGHTS from this table:
# - age: The 'count' is 6. The 'mean' (46.8) is much lower than the 'max' (99), suggesting a right skew.
# - salary: The 'mean' (223k) is VASTLY different from the '50%' (median) of 80k. This is a huge red flag for an outlier.
# - salary: The 'std' (standard deviation) is massive (360k), confirming a very wide spread, likely due to the outlier.
# - salary: The 'max' value of 950k is clearly an extreme outlier compared to the 75% percentile of 111k.


# 3. Get a Summary of Categorical Columns
print("\n--- 3. Categorical Summary (.describe(include='object')) ---")
print(df.describe(include=['object']))
# INSIGHTS from this table:
# - department: There are 6 entries ('count').
# - department: There are 3 unique departments.
# - department: The most frequent ('top') department is 'IT'.
# - department: 'IT' appears 3 times ('freq').


# 4. Deeper Dive into a Single Categorical Column
print("\n--- 4. Value Counts for a Single Categorical Column ---")
print(df['department'].value_counts())
# Insight: This gives a clear frequency breakdown for the 'department' feature.
```

---
#### Why Do We Need It? / What Problem Does It Solve?
- This step is critical because it solves the problem of "unknown feature characteristics." An initial inspection might tell you a column is a number (int64), but this review tells you if that number represents an age from 0-100 or a salary from 50,000-5,000,000. This context is essential.

It helps you answer key questions for each feature:

- What is its scale and range? (e.g., 0 to 1, or -1000 to 1000?)
What is a "typical" value? (Mean vs. Median)
- How spread out are the values? (Standard Deviation)
- Are there any potential data quality issues or errors? (e.g., a minimum age of -5, a maximum percentage of 200).
- What categories exist and how common are they?
- This step directly informs your entire data cleaning and feature engineering strategy.

---
#### Advantages of It
- Powerful Data Quality Check: It's the most effective way to spot impossible or suspicious values (e.g., negative prices, future dates) within individual columns.
- Informs Preprocessing Choices: The summaries directly guide your next steps.
- A large difference between the mean and median (50% percentile) suggests skewness, indicating a need for transformations like log transform.
- A very large standard deviation or a huge max value suggests the presence of outliers, indicating a need for outlier treatment.
- Features on vastly different scales indicate a need for scaling (Standardization or Normalization).
- Foundation for Deeper Analysis: It provides the necessary context for all subsequent univariate and bivariate analysis. You can't effectively visualize a feature if you don't know its basic properties.

---
#### Disadvantages of It
- Summaries Can Hide Details: This is the main limitation. A statistical summary (like describe()) doesn't show the shape of the data's distribution. A feature with two distinct peaks (bimodal) could have the same mean as a feature with a normal bell-curve distribution.
- Does Not Reveal Relationships: This step is purely univariate (one variable at a time). It tells you about the age column and the income column separately, but it tells you nothing about the relationship between them.
- Can Be Overwhelming: In a dataset with hundreds of columns, the output can be a very large table that is difficult to read through manually.

---
#### What Will Happen If We Don't Do It?
- Skipping this step means you are making preprocessing and modeling decisions without understanding the nature of your own features. This leads to:

- Failure to Spot Critical Errors: You would miss that a product_weight column has negative values, which could corrupt your entire analysis.
- Ineffective Preprocessing: You might apply a scaling technique (like Min-Max scaling) that is inappropriate for a feature with outliers, because you never checked for them.
- Misinterpretation of Model Results: You might build a model without realizing that one feature's scale is 1000x larger than another's, causing the model to be biased and its feature importances to be misleading.
- Wasted Time: You will inevitably discover these issues later during visualization or modeling, forcing you to go back and debug, wasting significant time.