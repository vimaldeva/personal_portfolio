## Precision Recall curve 

The Precision-Recall (PR) Curve is a graph used to evaluate the performance of a binary classification model, especially when the classes are imbalanced (e.g., 99% of data is "Normal" and 1% is "Fraud").

While Accuracy can be misleading, the PR Curve shows the trade-off between Precision and Recall for different probability thresholds.

---
### The Two Components
- Recall (Sensitivity): "Out of all actual positive cases, how many did we find?" (We want this to be high to catch all "bad" cases).
- Precision: "Out of all the cases we predicted as positive, how many were actually positive?" (We want this to be high to avoid "false alarms").

---
### Why use the PR Curve?
In many real-world scenarios, you care more about the Positive Class (the rare event).

- ROC Curves (the other common curve) can look "too good" if you have a lot of negative samples.
- PR Curves are much tougher; they focus only on the performance of the minority class. If your model is bad at finding the rare class, the PR curve will drop immediately.

---
### How to Read the Curve
- The Goal: You want the curve to be in the top-right corner.
- The Trade-off: As you try to increase Recall (catch more people with a disease), your Precision usually drops (you start misdiagnosing healthy people).
- AUC-PR (Area Under the Curve): A single number from 0 to 1. A score of 1.0 is a perfect model.

---
### Python Example

```
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_curve, average_precision_score

# 1. Create an imbalanced dataset (90% class 0, 10% class 1)
X, y = make_classification(n_samples=1000, n_classes=2, weights=[0.9, 0.1], random_state=42)

# 2. Split and Train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
model = LogisticRegression()
model.fit(X_train, y_train)

# 3. Get predicted probabilities for the positive class
probs = model.predict_proba(X_test)[:, 1]

# 4. Calculate precision and recall for various thresholds
precision, recall, thresholds = precision_recall_curve(y_test, probs)

# 5. Calculate the Average Precision (Area under the curve)
ap_score = average_precision_score(y_test, probs)

# 6. Plot the Curve
plt.figure(figsize=(8, 6))
plt.plot(recall, precision, label=f'PR Curve (AP = {ap_score:.2f})', color='blue', linewidth=2)
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.legend()
plt.grid(True)
plt.show()

```

---
### PR Curve vs. ROC Curve: Which one to use?

| Scenario | Use ROC Curve | Use PR Curve |
| :-- | :-- | :-- |
| Class Balance | Balanced (50/50) | Imbalanced (e.g., 95/5) |
| Focus | Overall performance of both classes | Performance on the Minority class |
| Example | Predicting Gender (Male/Female) | Fraud Detection, Cancer Diagnosis |

---
### Summary
If you are working on a project where the "Positive" class is rare (like a 0.1% failure rate in a factory), ignore Accuracy and ignore ROC. Use the Precision-Recall Curve to see how well your model actually performs on that rare event.




