## What is L2 Regularization?
L2 Regularization works by adding a penalty to the loss function based on the sum of the squares of the weights.

While L1 tries to throw away unimportant features (sparsity), L2 tries to ensure that no single weight becomes too large. It forces the model to spread its "influence" across all the features rather than relying heavily on just one or two.

---
### The Analogy: The "Balanced Team"
Imagine you are a manager of a 10-person team working on a project.

- No Regularization: One "superstar" employee does 99% of the work, and the other 9) do nothing. If that superstar gets sick (if that one feature is noisy or missing in the real world), the whole project fails.
- L2 Regularization: You implement a rule: "No one is allowed to do all the work." You force every team member to contribute a little bit.

The Result: You have a balanced, robust team. If any one person is unavailable, the others can easily fill the gap because they were all involved. The project is much more likely to succeed in the long run.

---
### How It Works: The Math
The new Loss Function looks like this:

```
Total Loss = Original Loss + λ∑i=1 n wi2
```

wi2 : The square of each weight. Squaring the weights means that large weights are penalized much more heavily than small weights. (e.g., a weight of 10 adds 100 to the loss, while a weight of 1 adds only 1).

λ  (Lambda): The regularization strength.

Why is it called "Weight Decay"? When we calculate the gradient for L2, the update rule effectively says: "In every step, before you do anything else, shrink the current weight by a small percentage." Because the weights are constantly being pulled toward zero, they "decay" over time unless the data provides very strong evidence that they should be large.

---
### Advantages
- Stability: L2 is mathematically "smoother" than L1. It leads to more stable training and more consistent results.
- Handles Correlated Features: If you have two highly correlated features, L2 will distribute the weight between them roughly equally. L1 would randomly pick one and kill the other.
- Prevents "Exploding" Weights: It is the best defense against weights growing out of control, which can happen in very deep networks.
- Better Generalization: In the vast majority of deep learning tasks, L2 results in better final accuracy on the test set than L1.

---

### Disadvantages
- No Feature Selection: Unlike L1, L2 will never set a weight to exactly zero. You will always end up with a model that uses every single input feature, even if some are barely useful.
- Less Interpretable: Because every feature is kept, it’s harder to say which specific features are the "drivers" of the model.

---

### When to Use It
- The Default Choice: You should start with L2 regularization for almost every neural network you build. It is the industry standard.
- When you have many features that you believe all contribute a small amount to the final result.
- To prevent overfitting in almost any deep learning architecture (CNNs, RNNs, MLPs).

---
### Python code

```
from tensorflow.keras import layers, regularizers

model = models.Sequential([
    # Apply L2 regularization to the weights (kernel) of this layer
    layers.Dense(64, activation='relu', 
                 kernel_regularizer=regularizers.l2(0.01), 
                 input_shape=(100,)),
    
    layers.Dense(1, activation='sigmoid')
])
```

---
### Summary
| Feature | L1 (Lasso) | L2 (Ridge) |
| :-- | :-- | :-- |
| Penalty | $$ | w |
| Weights | Can become Zero. | Become Small (but not zero). |
| Outcome | Sparse model (Feature selection). | Stable model (Balanced weights). |
| Use Case | High-dimensional data / Interpretability. | Default choice / General performance. |