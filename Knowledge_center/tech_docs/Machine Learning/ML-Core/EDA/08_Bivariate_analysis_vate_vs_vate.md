##### Categorical vs. Categorical:

Question: Is there an association between the categories of two different variables?
- Quantification:
Contingency Table (Crosstab): A table showing the frequency of each combination of categories. (pd.crosstab(df['cat1'], df['cat2']))
- Visualization:
    - Grouped or Stacked Bar Charts: To visually compare the proportions.
    - Heatmap of the Crosstab: To see which combinations are common or rare.
- Statistical Test: Use a Chi-Squared test to check for statistical independence.