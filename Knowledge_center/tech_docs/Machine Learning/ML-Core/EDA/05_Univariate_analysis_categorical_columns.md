##### For Categorical Variables:

- Frequency Counts: How many times does each category appear? (df['category_col'].value_counts())
Proportions/Percentages: What is the percentage of each category? (df['category_col'].value_counts(normalize=True))
- Cardinality: How many unique categories are there? (df['category_col'].nunique())
- Visualization:
    - Bar Charts / Count Plots: The standard for visualizing category frequencies.
    - Pie Charts: Good for showing proportions of a whole, but often less effective than bar charts for comparison.
