## Phase 1: Basic Data Understanding & Housekeeping
This is the first-pass, "get to know your data" phase.

#### Initial Data Inspection:

- View Shape: How many rows and columns are there? (df.shape)
- Inspect Data Types: What are the data types of each column (e.g., int64, float64, object, datetime)? Are they appropriate? (df.info(), df.dtypes)
- Preview Data: Look at the first few and last few rows to get a feel for the values. (df.head(), df.tail())
- Random Sample: Look at a random sample of rows to avoid any bias from sorting. (df.sample(5))
- Check for Duplicates: Are there any completely duplicated rows? (df.duplicated().sum())
#### Column/Feature Review:

- List Column Names: What are the names of all the columns? (df.columns)
- Clean Column Names: Are the names clean and easy to work with? (e.g., remove spaces, special characters, convert to lowercase).
- Initial Statistical Summary: Get a quick statistical overview of the numerical columns (count, mean, std, min, max, quartiles). (df.describe())
- Categorical Summary: Get a summary for categorical/object columns (count, unique, top, frequency). (df.describe(include=['object', 'category']))
#### Initial Missing Value Assessment:

- Count Missing Values: How many missing values (NaN) are in each column? (df.isnull().sum())
- Percentage of Missing Values: What percentage of each column is missing? This is more informative than the raw count. (df.isnull().sum() / len(df) * 100)

---

#### Phase 2: Univariate Analysis (Analyzing One Variable at a Time)
The goal here is to understand each feature individually.

##### For Numerical Variables:

- Central Tendency: What is the "typical" value? (Mean, Median).
- Dispersion/Spread: How spread out is the data? (Standard Deviation, Variance, Min, Max, Range, Interquartile Range (IQR)).
- Distribution Shape:
- Visualization:
    - Histograms: To see the frequency distribution.
    - KDE (Kernel Density Estimate) Plots: A smoothed version of a histogram.
    - Box Plots: Excellent for spotting outliers and understanding quartiles.
    - Violin Plots: Combines a box plot with a KDE plot to show the distribution shape.
- Metrics:
    - Skewness: Is the data skewed to the left or right?
    - Kurtosis: How "peaked" or "flat" is the distribution? Does it have heavy tails?
    - Outlier Detection: Identify potential outliers using box plots or statistical methods (Z-score, IQR method).
##### For Categorical Variables:

- Frequency Counts: How many times does each category appear? (df['category_col'].value_counts())
Proportions/Percentages: What is the percentage of each category? (df['category_col'].value_counts(normalize=True))
- Cardinality: How many unique categories are there? (df['category_col'].nunique())
- Visualization:
    - Bar Charts / Count Plots: The standard for visualizing category frequencies.
    - Pie Charts: Good for showing proportions of a whole, but often less effective than bar charts for comparison.

---

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

##### Numerical vs. Categorical:

Question: Does the distribution of the numerical variable change across different categories?
- Visualization:
    - Grouped Box Plots: The best way to compare the distributions of a numerical variable for each category.
    - Grouped Violin Plots: Similar to box plots but provides more detail on the distribution's shape.
    - Bar Charts (of means/medians): Summarize the central tendency of the numerical variable for each category.
- Quantification:
    - Use groupby() to calculate summary statistics (mean, median, std) of the numerical variable for each category. (df.groupby('category_col')['numerical_col'].mean())

##### Categorical vs. Categorical:

Question: Is there an association between the categories of two different variables?
- Quantification:
Contingency Table (Crosstab): A table showing the frequency of each combination of categories. (pd.crosstab(df['cat1'], df['cat2']))
- Visualization:
    - Grouped or Stacked Bar Charts: To visually compare the proportions.
    - Heatmap of the Crosstab: To see which combinations are common or rare.
- Statistical Test: Use a Chi-Squared test to check for statistical independence.

##### Multivariate (3+ variables):

Use the hue, size, and style parameters in plots to add a third or fourth dimension.
sns.scatterplot(x='num1', y='num2', hue='cat1', data=df)
sns.pairplot(df, hue='cat1')
Use 3D plots (with caution, as they can be hard to interpret).

---

#### Phase 4: Summarization & Hypothesis Generation
This is the "so what?" phase where you consolidate your findings.

- Document Key Findings: Write down every interesting pattern, relationship, or data quality issue you discovered.
- Formulate Hypotheses: Based on your findings, create testable hypotheses. (e.g., "I hypothesize that customers from the 'West' region have a higher average purchase value.").
- Identify Data Quality Issues: Create a list of all data problems found (e.g., "Column X is 70% missing," "Column Y is heavily skewed," "Outliers detected in Z").
- Brainstorm Feature Engineering Ideas:
"I can create a price_per_unit feature by dividing total_price by quantity."
"The age feature is non-linear; I should try binning it."
"The city column has too many categories; I should try target or frequency encoding."
- Plan Preprocessing Steps: Based on your EDA, outline the necessary preprocessing steps for your model (e.g., "I will need to scale numerical features, one-hot encode categorical features, and impute missing values using the median.").