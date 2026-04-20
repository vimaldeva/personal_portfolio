#### What is the F1-Score?
The F1-Score is a single metric that combines both Precision and Recall into one number. It is the harmonic mean of Precision and Recall.

The harmonic mean is used because it penalizes extreme values more than a simple average would. In other words, you can only achieve a high F1-Score if both your Precision and Recall are high. You can't "cheat" by having one be perfect and the other be terrible.

Simple Average Example: Precision = 1.0 (perfect), Recall = 0.1 (terrible). The simple average is (1.0 + 0.1) / 2 = 0.55. This looks deceptively okay.
Harmonic Mean (F1-Score) Example: For the same values, the F1-Score would be approximately 0.18. This low score correctly reflects that the model is poor overall because it's failing badly on one of the key metrics.

---
#### How to Calculate It
The F1-Score is calculated from Precision and Recall:

```
Formula: F1-Score = 2 * (Precision * Recall) / (Precision + Recall)
```
---
#### What Problem Does It Solve?
It solves the Precision-Recall Trade-off. In many models, you can adjust a setting (a prediction threshold) to make the model more precise, but this often comes at the cost of lower recall. Conversely, you can increase recall, but this often lowers precision.

The F1-Score gives you a single number to optimize. Instead of trying to balance two separate metrics, you can aim to maximize the F1-Score, which implicitly balances them for you.

---
#### Advantages
- Provides a Single Score: This is extremely useful for comparing different models or for tuning hyperparameters. It's much easier to compare models based on one number rather than two.
- Works Well on Imbalanced Datasets: Since it's based on Precision and Recall, it is not easily fooled by a large majority class, unlike accuracy.
- Balances Competing Goals: It provides a robust measure of a model's performance when you care about minimizing both False Positives and False Negatives.

---
#### Disadvantages
- Less Interpretable: While Precision ("how many of our positive predictions were right?") and Recall ("how many of the actual positives did we find?") are very intuitive, the F1-Score ("the harmonic mean of...") is more abstract and harder to explain to non-technical stakeholders.
- Loses Nuance: By combining two numbers into one, you lose the specific information about the type of errors your model is making. A decent F1-Score could be hiding a critical weakness in either precision or recall.
- Assumes Equal Importance: The standard F1-Score gives equal weight to Precision and Recall. In some business contexts, one might be significantly more important than the other. (Note: A more general version, the F-beta score, allows you to give more weight to one over the other).

---
#### When to Use It
- On Imbalanced Datasets: This is the primary use case. It's a much more reliable metric than accuracy when one class dominates the others.
- When the Cost of FP and FN are Similar: When you don't have a strong reason to prioritize either Precision or Recall, the F1-Score is an excellent default choice as it balances them equally.
- For Model Optimization: It is often used as the target metric to maximize during hyperparameter tuning (e.g., in a Grid Search) because it simplifies the optimization process to a single value.

---
#### When Not to Use It (as the sole metric)
- When the Cost of FP and FN are Vastly Different:
For a cancer diagnosis model, a False Negative (missing a sick patient) is catastrophic. You should prioritize Recall directly.
- For a spam filter, a False Positive (blocking a legitimate email) is a major problem. You should prioritize Precision directly. In these cases, you should still look at the F1-Score, but it shouldn't be your primary decision-making metric.

---
#### Python code
```
# Import the necessary functions
from sklearn.metrics import f1_score, precision_score, recall_score

# Assume these are your true labels and model predictions
y_true = ["Spam", "Spam", "Not Spam", "Spam", "Spam"]
y_pred = ["Spam", "Spam", "Spam",     "Not Spam", "Spam"]

# Manually calculate:
# TP = 3, FP = 1, FN = 1
# Precision = 3 / (3 + 1) = 0.75
# Recall = 3 / (3 + 1) = 0.75
# F1 = 2 * (0.75 * 0.75) / (0.75 + 0.75) = 0.75

# Calculate using scikit-learn
# The `pos_label` argument tells the function which class to consider as "Positive".
f1 = f1_score(y_true, y_pred, pos_label="Spam")

print(f"F1-Score: {f1:.2f}")
# Output:
# F1-Score: 0.75

# You can see how it relates to precision and recall
precision = precision_score(y_true, y_pred, pos_label="Spam")
recall = recall_score(y_true, y_pred, pos_label="Spam")
print(f"Precision: {precision:.2f}") # Output: 0.75
print(f"Recall: {recall:.2f}")    # Output: 0.75
```