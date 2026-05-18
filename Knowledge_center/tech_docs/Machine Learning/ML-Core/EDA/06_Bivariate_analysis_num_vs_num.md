#### Phase 3: Bivariate & Multivariate Analysis (Analyzing Relationships)
This is where you discover the most interesting insights by comparing variables to each other.

#####  Numerical vs. Numerical:

- Question: Is there a relationship between these two numerical variables? Is it linear, non-linear? Is it strong or weak?
- Visualization:
    - Scatter Plots: The most important tool here. Look for patterns, trends, and clusters.
Quantification:
    - Correlation: Calculate the correlation coefficient (e.g., Pearson's r) to measure the strength and direction of a linear relationship.
Tools:
    - Correlation Matrix: A table showing the correlation between all pairs of numerical variables. (df.corr())
    - Heatmap: A powerful visualization of the correlation matrix. (sns.heatmap(df.corr()))
    - Pair Plot: A grid of scatter plots for every pair of numerical variables. A great way to get a quick overview. (sns.pairplot(df))
