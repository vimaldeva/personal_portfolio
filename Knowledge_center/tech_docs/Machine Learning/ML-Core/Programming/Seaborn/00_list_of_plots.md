## Popular Seaborn Plots by Category

#### Relational Plots

- scatterplot
- lineplot

#### Distribution Plots
- histplot
- kdeplot
- ecdfplot
- rugplot

#### Categorical Plots
- stripplot
- swarmplot
- boxplot
- violinplot
- boxenplot
- barplot
- countplot
- pointplot

#### Matrix Plots
- heatmap
- clustermap

#### Regression Plots
- regplot
- lmplot

#### Multi-plot Grids
- pairplot
- jointplot
- catplot
- FacetGrid

---
## Plots Used for EDA of Various Columns
Here is a list of plots organized by the type of analysis you are performing during Exploratory Data Analysis (EDA).

#### Univariate Analysis (Analyzing a Single Variable)
For a single Numerical variable:

- histplot (to see frequency distribution)
- kdeplot (to see probability density)
- boxplot (to see quartiles and outliers)
- violinplot (to see distribution shape and quartiles)

For a single Categorical variable:

- countplot (to see the frequency of each category)

#### Bivariate Analysis (Analyzing Relationships Between Two Variables)

Numerical vs. Numerical:

- scatterplot (the standard choice)
- jointplot (combines a scatter plot with histograms)
- regplot (adds a linear regression line)
- heatmap (used on a correlation matrix)

Numerical vs. Categorical:

- boxplot (best for comparing distributions across categories)
- violinplot (similar to boxplot, but shows density)
- barplot (to compare an aggregate metric like mean or sum)
- stripplot (a scatter plot for categorical data)
- swarmplot (like a stripplot, but points don't overlap)

Categorical vs. Categorical:

- countplot (using the hue parameter)
- heatmap (used on a pd.crosstab() contingency table)

#### Multivariate Analysis (Analyzing 3+ Variables)
- pairplot (to see all pairwise relationships in one grid)
- heatmap (on a correlation matrix for all numerical variables)
- Using the hue, size, and style parameters in other plots:
- scatterplot (with hue for a third categorical variable)
- lineplot (with hue or style for different categories)
- catplot (a flexible tool for creating faceted categorical plots)