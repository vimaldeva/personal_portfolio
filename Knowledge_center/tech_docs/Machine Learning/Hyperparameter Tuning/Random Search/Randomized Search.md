## Randomized Search
Randomized Search, a more efficient and often more effective alternative to Grid Search for hyperparameter tuning.

---
#### What is Randomized Search?
Randomized Search is a hyperparameter tuning technique that, instead of testing every single combination like Grid Search, samples a fixed number of random combinations from a specified hyperparameter space.

The core idea is that not all hyperparameters are equally important. A brute-force Grid Search might spend an enormous amount of time meticulously testing different values for an unimportant hyperparameter, while a Randomized Search is more likely to quickly find a good combination for the hyperparameters that actually matter.

---
#### How Randomized Search Works
The process is similar to Grid Search but with a key difference in how it explores the search space:

Step 1: Define the Search Space (Distributions). Instead of a discrete grid of values, you define a search space using statistical distributions for each hyperparameter.

For categorical parameters, you provide a list of values (e.g., kernel: ['linear', 'rbf']).
For continuous parameters, you can provide a distribution like uniform or log-uniform (e.g., C: uniform(0.1, 100)). This is a major advantage over Grid Search.
Step 2: Set Your "Budget". You decide how many different combinations you want to test. This is controlled by the n_iter parameter (number of iterations). For example, you might decide you only have time to test 50 different combinations.

Step 3: The Search. The algorithm then randomly samples n_iter combinations from the search space you defined. If you used distributions, it will sample random values from those distributions.

Step 4: Cross-Validation. For each randomly sampled combination, it performs K-Fold Cross-Validation to get a robust performance estimate, just like Grid Search.

Step 5: Identify the Best Combination. After testing all n_iter combinations, it identifies the set of hyperparameters that resulted in the best average cross-validation score.

Step 6: Refit the Final Model. The model is retrained on the entire training dataset using the best-found parameters.

---
#### The Key Insight: Why Random is Often Better
- Research has shown that for most machine learning models, only a few hyperparameters have a significant impact on performance.

- Grid Search wastes a lot of time on unimportant hyperparameters. Imagine two knobs, one important and one unimportant. Grid Search will meticulously test every setting of the unimportant knob for each setting of the important one.
- Randomized Search is much more efficient. In every iteration, it tries a new, random value for every single hyperparameter. This means it explores the ranges of the important hyperparameters much more thoroughly and is more likely to stumble upon a great combination quickly.
(Image credit: Bergstra & Bengio, "Random Search for Hyper-Parameter Optimization")

---
#### Advantages
- Much More Efficient: It is significantly faster than Grid Search, especially when dealing with a large number of hyperparameters. You control the computational cost directly with the n_iter parameter.
- Often Finds Better Models: By exploring the hyperparameter space more broadly (instead of being stuck on a rigid grid), it can often find better-performing models than Grid Search in the same amount of time.
- Works with Continuous Distributions: It allows for a much finer-grained search over continuous parameters, rather than being limited to a few discrete points.

---
#### Disadvantages
- Not Exhaustive: Since it's a random sampling process, it does not guarantee that it will find the absolute best combination from the search space.
- Can Get Unlucky: If your n_iter budget is very small, you might get unlucky and only sample from poorly performing regions of the hyperparameter space.

---
#### When to Use It
- When you have many hyperparameters to tune. This is where it shines.
- When computational time is a constraint. It allows you to set a fixed budget for your tuning process.
- When you suspect that only a few hyperparameters are actually important.
- It is generally considered a better starting point than Grid Search for most real-world problems.

---
#### When Not to Use It
- When you have a very small number of hyperparameters (e.g., 2 or 3) and can easily afford the time for an exhaustive Grid Search.
- When you need to be absolutely certain you've tested a specific set of combinations.

---
#### Python code
```

from sklearn.model_selection import RandomizedSearchCV
from sklearn.svm import SVC
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from scipy.stats import uniform, randint


X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# 1. Define the parameter search space using distributions

param_dist = {
    'C': uniform(0.1, 100),  # Sample from a continuous uniform distribution
    'gamma': uniform(0.001, 1),
    'kernel': ['linear', 'rbf'], # Sample from a discrete list
    'class_weight': [None, 'balanced']
}

# 2. Instantiate the RandomizedSearchCV object
# n_iter: the number of random combinations to try

random_search = RandomizedSearchCV(
    estimator=SVC(),
    param_distributions=param_dist,
    n_iter=50,  # Set your budget here
    cv=5,
    scoring='accuracy',
    random_state=42, # for reproducibility
    n_jobs=-1
)

# 3. Fit the random search to the data
random_search.fit(X_train, y_train)

# 4. Print the best parameters and the best score
print(f"Best Hyperparameters found: {random_search.best_params_}")
print(f"Best cross-validation score: {random_search.best_score_:.3f}")

# The `random_search` object is now a fully trained model with the best parameters.

accuracy_on_test = random_search.score(X_test, y_test)
print(f"Accuracy on test set: {accuracy_on_test:.3f}")
```