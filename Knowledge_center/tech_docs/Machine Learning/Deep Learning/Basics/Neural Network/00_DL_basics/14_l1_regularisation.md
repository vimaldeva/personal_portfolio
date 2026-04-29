## What is L1 Regularization?
L1 Regularization works by adding a penalty to the loss function based on the absolute sum of the weights.

In simple terms, it "taxes" the model for having weights. The larger the weight, the higher the tax. However, L1 has a very specific mathematical property: it doesn't just make weights smaller; it often pushes them to exactly zero.

---
### The Analogy: The "Marie Kondo" of Machine Learning
Imagine you are moving into a tiny apartment (a simple model). You have 100 boxes of stuff (100 features/weights).

- No Regularization: You try to cram all 100 boxes into the apartment. It’s a mess, and you can’t find anything (Overfitting).
- L2 Regularization: You try to make every box smaller, but you keep all 100 of them.
- L1 Regularization: You look at each box and ask, "Does this spark joy (is this feature useful)?" If a box isn't very useful, L1 forces you to throw it away entirely (Weight = 0).
- The Result: You end up with only the 10 most important boxes. Your apartment is clean, and you only kept what truly matters.

---
### How It Works: The Math
The new Loss Function looks like this:

```
Total Loss = Original Loss + λ∑i=1 n∣wi∣
```

∣wi∣: The absolute value of each weight.

λ (Lambda): The regularization strength.

- If λ is high, the model is forced to be very sparse (many zeros).
- If λ is low, the model behaves more like a standard neural network.

Why does it go to zero? Mathematically, the "shape" of the L1 penalty is a diamond. When the optimizer tries to minimize the loss, it is very likely to hit the "corners" of this diamond, which sit exactly on the axes where one or more weights are zero.

---
### Advantages
- Automatic Feature Selection: This is the biggest advantage. L1 identifies which features are useless and effectively deletes them by setting their weights to zero.
- Model Interpretability: Because many weights become zero, the final model is much simpler. You can clearly see which 5 or 10 features are actually driving the predictions.
- Reduces Model Size: A "sparse" model (one with many zeros) requires less memory and can be faster to run in production.

---
### Disadvantages
- Loss of Information: L1 might zero out a feature that has a very small but real signal, potentially hurting accuracy slightly compared to L2.
- Unstable with Correlated Features: If you have two features that are highly correlated (e.g., "Height in inches" and "Height in centimeters"), L1 will often randomly pick one to keep and throw the other away. This can make the model's logic seem arbitrary.
- Non-Differentiable at Zero: The absolute value function has a "sharp point" at zero, which makes the math slightly more complex for some optimizers (though modern frameworks handle this automatically).

---
### When to Use It
- High-Dimensional Data: When you have hundreds or thousands of features, but you suspect only a few of them are actually important.
- When you need a simple, interpretable model.
- To reduce the "noise" in a dataset by ignoring irrelevant inputs.

---
### Python code
```
from tensorflow.keras import layers, regularizers

model = models.Sequential([
    # Apply L1 regularization to the weights of this layer
    layers.Dense(64, activation='relu', 
                 kernel_regularizer=regularizers.l1(0.01), 
                 input_shape=(100,)),
    
    layers.Dense(1, activation='sigmoid')
])
```