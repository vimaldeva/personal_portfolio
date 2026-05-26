## What is Accuracy?
Accuracy is the ratio of correct predictions to the total number of predictions.

Accuracy = Number of Correct Predictions /Total Number of Predictions

Example: If your model predicts 100 house prices and gets 90 of them "close enough" (or in classification, gets 90 labels right), your accuracy is 90%.

---
### How do Transformations affect Accuracy?
The transformations we discussed (Log and Encoding) directly impact how well a model can learn, which in turn determines the accuracy:

- Log Transformation: By removing skewness, you make it easier for models (like Linear Regression or Logistic Regression) to find the "best fit" line. This usually increases accuracy because the model isn't being pulled away by extreme outliers.
- Ordinal Encoding: If you use Ordinal Encoding for your "Priority" column (Low=0, Medium=1, High=2), the model understands the relationship. If you used One-Hot Encoding instead, the model might struggle to see the "trend," potentially leading to lower accuracy on small datasets.
- Label Encoding (The Danger): If you use Label Encoding on non-ranked data (e.g., Colors: Red=0, Blue=1, Green=2), a Linear model will think Green > Red. This creates "noise," which decreases accuracy.

---
### The "Accuracy Trap" (When Accuracy Lies)
Accuracy is a great metric only if your classes are balanced (e.g., 50% "Yes" and 50% "No").

- The Scenario: Imagine you are building a model to detect a very rare disease that only 1% of people have.

- If your model is "dumb" and simply predicts "No Disease" for everyone, it will be 99% accurate.
- Is the model good? No, it failed to find the 1% of people who are actually sick.
- In this case, Accuracy is high, but the model is useless.

---
### When to use other metrics?
If your data is imbalanced (like the disease example or credit card fraud), you should look at these instead of just Accuracy:

- Precision: "Of all the people I predicted have the disease, how many actually have it?"
- Recall: "Of all the people who actually have the disease, how many did I correctly find?"
- F1-Score: A balance between Precision and Recall. This is usually the best metric for imbalanced data.

---
### Python Code: Calculating Accuracy


```
from sklearn.metrics import accuracy_score

# Actual values (Ground Truth)
y_true = [0, 1, 1, 0, 1, 1] 

# Model predictions
y_pred = [0, 1, 0, 0, 1, 1]

# Calculate Accuracy
acc = accuracy_score(y_true, y_pred)

print(f"Accuracy: {acc * 100}%") 
# Output: Accuracy: 83.33% (5 out of 6 were correct)
```

---
### Summary
- Transformations (Log, Encoding) help the model "see" patterns better, which improves accuracy.
- Accuracy is best for balanced data.
- F1-Score/Precision/Recall are better for imbalanced data.
