
##### Numerical vs. Categorical:

Question: Does the distribution of the numerical variable change across different categories?
- Visualization:
    - Grouped Box Plots: The best way to compare the distributions of a numerical variable for each category.
    - Grouped Violin Plots: Similar to box plots but provides more detail on the distribution's shape.
    - Bar Charts (of means/medians): Summarize the central tendency of the numerical variable for each category.
- Quantification:
    - Use groupby() to calculate summary statistics (mean, median, std) of the numerical variable for each category. (df.groupby('category_col')['numerical_col'].mean())