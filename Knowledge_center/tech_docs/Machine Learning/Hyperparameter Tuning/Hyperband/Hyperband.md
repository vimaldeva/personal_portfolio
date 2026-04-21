## Hyperband

You're now moving into the cutting edge of hyperparameter optimization. Hyperband is a clever and highly efficient algorithm designed to address a key weakness of both Randomized Search and Bayesian Optimization: they waste a lot of time on bad hyperparameter configurations.

---
#### The Problem: The Cost of Bad Guesses
Imagine you are tuning a deep learning model. Each hyperparameter configuration needs to be trained for, say, 100 epochs, which might take hours.

- Randomized Search will pick a random configuration, train it for the full 100 epochs, record the score, and then repeat. If it picks a terrible configuration (e.g., a learning rate that's way too high), it will still waste hours training it to completion, even though it was clear after 5 epochs that it was performing poorly.
- Bayesian Optimization is smarter about what to try next, but it still treats each evaluation as a black box: it picks a configuration, waits for the full 100 epochs to finish, gets the final score, and then uses that to update its model. It also wastes time on bad configurations.
- Hyperband asks a simple but powerful question: "Why should we waste resources fully training a configuration that is clearly performing badly?"

---
#### The Core Idea: A Tournament of Models (Successive Halving)
The core mechanism behind Hyperband is a strategy called Successive Halving. Think of it as a multi-round tournament for your hyperparameter configurations.

- Round 1: The Broad Start. Start by training a large number (n) of randomly chosen hyperparameter configurations, but give each one only a very small resource budget (r). For a neural network, a "resource" is typically the number of epochs. So, you might train 64 different models for just 1 epoch each.

- Round 2: Promote the Best. Evaluate the performance of all 64 models after their 1 epoch. Keep the top half (the best 32 models) and discard the rest.

- Round 3: Give More Resources. Take the 32 surviving models and train them for more epochs (e.g., double the resources). Now they have all been trained for a total of 2 epochs.

- Round 4: Repeat. Evaluate the 32 models. Keep the top half (the best 16) and discard the rest.

Continue... This process of evaluating, keeping the top fraction, and allocating more resources to the survivors continues until only one configuration—the champion—remains.

This is incredibly efficient because it quickly gets rid of bad configurations without wasting time training them to completion.

---
#### From Successive Halving to Hyperband
Successive Halving has its own problem: the trade-off between n (the number of configurations you start with) and r (the initial resource budget).

- If you start with a huge n and a tiny r, you might eliminate a "slow starter"—a good configuration that just needs a few epochs to get going.
- If you start with a small n and a larger r, you might not be exploring enough different configurations.

Hyperband solves this by being a "wrapper" around Successive Halving. It essentially runs the Successive Halving tournament multiple times with different starting values of n and r, ensuring that it tries both very aggressive, broad searches and more conservative, deep searches. It then reports the best configuration found across all of these tournaments.

---
#### Advantages
- Extremely Efficient: It is often much faster than Randomized Search and Bayesian Optimization because it allocates resources intelligently and stops training unpromising configurations early.
- Highly Parallelizable: Within each round of the tournament, all configurations can be trained independently and in parallel.
- Simple and Robust: It's based on a simple principle (early stopping of bad runs) and doesn't rely on complex probabilistic models like Bayesian Optimization.

---
#### Disadvantages
- Requires Iterative Training: This is the key constraint. The algorithm only works for models that can be trained and evaluated incrementally. It's perfect for deep learning (epochs), gradient boosting (number of trees), but it's not suitable for models like a standard scikit-learn SVM, where training is a one-shot process.
- Assumes "Early Potential" is a Good Indicator: It assumes that a configuration that performs poorly with a small budget will also perform poorly with a large budget. While this is usually true, it's possible to have a "slow starter" configuration that gets unfairly eliminated.

---
#### When to Use It
- Deep Learning: This is the killer use case. Hyperband and its derivatives (like ASHA) are the standard for tuning neural networks where training for many epochs is the main bottleneck.
- Gradient Boosting Models: You can use the number of boosting rounds (n_estimators) as the resource.
- Any model where training can be broken down into iterative steps and evaluated at each step.

---
#### Python code
```
# Import necessary libraries
# Note: HalvingRandomSearchCV is still an experimental feature, so we need to enable it.
from sklearn.experimental import enable_halving_search_cv
from sklearn.model_selection import HalvingRandomSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from scipy.stats import randint

# Generate a large dataset
X, y = make_classification(n_samples=10000, n_features=20, random_state=42)

# 1. Define the parameter search space
param_dist = {
    'max_depth': randint(3, 20),
    'min_samples_leaf': randint(1, 10)
}

# 2. Instantiate the HalvingRandomSearchCV object
# resource: The resource that is increased at each iteration. For many models, this is 'n_samples'.
# factor: The proportion of candidates to keep at each iteration (e.g., factor=3 means keep the top 1/3).
# min_resources: The initial amount of resource to allocate at the first iteration.
halving_search = HalvingRandomSearchCV(
    estimator=RandomForestClassifier(random_state=42),
    param_distributions=param_dist,
    n_candidates='exhaust', # Start with as many candidates as possible
    factor=3,
    resource='n_samples', # The resource we are increasing is the number of training samples
    min_resources=1000, # Start by training on a small subset of the data
    random_state=42,
    n_jobs=-1
)

# 3. Fit the search to the data
# This will perform the entire Successive Halving tournament.
halving_search.fit(X, y)

# 4. Print the best parameters and the best score
print(f"Best Hyperparameters found: {halving_search.best_params_}")
print(f"Best cross-validation score: {halving_search.best_score_:.3f}")

# The `halving_search` object is now a fully trained model with the best parameters.
print(f"\nNumber of iterations: {halving_search.n_iterations_}")
print(f"Number of candidates at last iteration: {halving_search.n_candidates_at_last_iteration_}")
```