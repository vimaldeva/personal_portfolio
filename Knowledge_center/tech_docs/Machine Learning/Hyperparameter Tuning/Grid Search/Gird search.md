## Grid search

#### The Problem: What are Hyperparameters?
Before understanding Grid Search, you must understand hyperparameters.

Parameters are values that a model learns from the data during training (e.g., the coefficients in a logistic regression).
Hyperparameters are settings that you, the data scientist, must choose before training begins. They are the "knobs" and "dials" that control the model's behavior.
Examples:

- In a Random Forest: How many trees should be in the forest (n_estimators)? What is the maximum depth of each tree (max_depth)?
- In an SVM: What should the regularization parameter C be? Which kernel should be used ('linear', 'rbf')?
- In KNN: What is the value of K (n_neighbors)?

The performance of a model is highly dependent on finding the right combination of these hyperparameters. But how do you find the best ones?

---
#### What is Grid Search?
Grid Search is an algorithm for hyperparameter tuning. It systematically works through multiple combinations of hyperparameter values, cross-validates each one, and determines which combination gives the best performance.

The name "Grid Search" comes from the idea that you are creating a "grid" of all possible hyperparameter combinations to test.

---
#### How Grid Search Works
The process is methodical and exhaustive:

- Step 1: Define the Grid. You create a dictionary where the keys are the names of the hyperparameters you want to tune, and the values are lists of the settings you want to test for those hyperparameters.

Example for an SVM classifier:

python


param_grid = {
    'C': [0.1, 1, 10, 100],
    'gamma': [1, 0.1, 0.01, 0.001],
    'kernel': ['rbf']
}
This grid defines 4 x 4 x 1 = 16 different combinations to test.

- Step 2: The Search. The Grid Search algorithm iterates through every single combination defined in the grid.

- Step 3: Cross-Validation. For each combination, it performs K-Fold Cross-Validation.

It splits the training data into K "folds" (e.g., 5 folds).
It trains the model on K-1 folds and evaluates it on the held-out fold.
It repeats this K times, so each fold gets to be the test set once.
The K performance scores are then averaged to get a robust, reliable performance estimate for that specific hyperparameter combination.
- Step 4: Identify the Best Combination. After testing all combinations, Grid Search identifies the set of hyperparameters that resulted in the highest average cross-validation score.

- Step 5: Refit the Final Model. Once the best parameters are found, Grid Search typically retrains the model one last time on the entire training dataset using those optimal parameters. This final model is then ready for use.

---
#### Advantages
- Exhaustive and Thorough: It is guaranteed to find the best possible combination of hyperparameters from the grid you provide.
- Easy to Parallelize: Each combination is independent, so the search can be easily distributed across multiple CPU cores to speed up the process.

---
#### Disadvantages
- Computationally Expensive (The Curse of Dimensionality): This is its biggest drawback. The number of combinations to test grows exponentially with the number of hyperparameters and the number of values you want to test. If you have 6 hyperparameters and test 5 values for each, you have 5^6 = 15,625 combinations to test. This can take an enormous amount of time and computational power.
- Only Tests Discrete Points: It only tests the specific values you provide. The true optimal value might lie somewhere in between the points on your grid (e.g., the best C is 50, but you only tested 10 and 100).

---
#### When to Use It
- When you have a relatively small number of hyperparameters to tune.
- When computational time is not a major constraint.
- When you want to be certain you've found the best combination from a limited set of options.

---
#### When Not to Use It (and What to Use Instead)
- When you have a large number of hyperparameters or a model that is very slow to train.
- Alternative 1: Randomized Search (RandomizedSearchCV): Instead of trying every combination, it tests a fixed number of random combinations from the grid. It is often much faster and can yield surprisingly good results, as it explores the hyperparameter space more broadly.
- Alternative 2: Bayesian Optimization: A "smarter" approach that uses the results from previous combinations to decide which combination to try next, focusing on more promising areas of the hyperparameter space.

---
#### Python code

```
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

# Load and split data
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# 1. Define the parameter grid
param_grid = {
    'C': [0.1, 1, 10, 100],
    'gamma': [1, 0.1, 0.01],
    'kernel': ['rbf', 'linear']
}

# 2. Instantiate the GridSearchCV object
# estimator: the model to tune
# param_grid: the grid of hyperparameters
# cv: number of cross-validation folds
# scoring: the metric to optimize for (e.g., 'accuracy', 'f1')
# n_jobs=-1: use all available CPU cores to speed up the search

grid_search = GridSearchCV(
    estimator=SVC(),
    param_grid=param_grid,
    cv=5,
    scoring='accuracy',
    n_jobs=-1
)

# 3. Fit the grid search to the data
# This will perform the entire search process.

grid_search.fit(X_train, y_train)

# 4. Print the best parameters and the best score

print(f"Best Hyperparameters found: {grid_search.best_params_}")
print(f"Best cross-validation score: {grid_search.best_score_:.3f}")

# The `grid_search` object is now a fully trained model with the best parameters.
# You can use it directly for predictions.

accuracy_on_test = grid_search.score(X_test, y_test)
print(f"Accuracy on test set: {accuracy_on_test:.3f}")
```