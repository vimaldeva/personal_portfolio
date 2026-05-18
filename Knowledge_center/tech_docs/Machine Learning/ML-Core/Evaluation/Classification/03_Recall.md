#### What is Recall?
Recall is a classification metric that answers the question: "Of all the items that were actually positive, how many did the model successfully identify?"

It measures the completeness of the positive predictions. A model with high recall is good at finding all the positive cases, meaning it generates very few False Negatives.

Recall is also known by other names, including Sensitivity and True Positive Rate (TPR).

--- 
#### How to Calculate It 

Recall is calculated using values from the Confusion Matrix:

```
Formula: Recall = True Positives / (True Positives + False Negatives)
```
In simple terms, it's the number of correct positive predictions divided by the total number of actual positive cases that exist in the dataset.

---
#### What Problem Does It Solve?
Recall directly addresses the cost of False Negatives. It is the most important metric to use when failing to identify a positive case is very damaging or costly. It answers whether a model is missing too many important things.

---
#### Advantages
- Focus on Coverage: It provides a clear measure of how well the model is "covering" the positive class and finding all instances of it.
- Crucial for "Don't Miss" Scenarios: It is the go-to metric when the primary goal is to minimize missed detections.
- Intuitive Concept: The idea of "we found X% of all the things we were looking for" is a very clear and understandable measure of performance.

---
#### Disadvantages
- Completely Ignores False Positives: This is its critical weakness. A model can achieve perfect (100%) recall by simply predicting "positive" for every single sample. It will find all the true positives (because it missed none), but it will also incorrectly label all negative samples as positive, leading to a massive number of False Positives.
- Can be Misleading in Isolation: Because it ignores False Positives, a high recall score alone doesn't mean a model is good. It must be considered alongside Precision.

---
#### When to Use It (Prioritize Recall)
- You should prioritize Recall when the cost of a False Negative is significantly higher than the cost of a False Positive.

- Medical Screening for Serious Disease (e.g., Cancer): A False Negative is catastrophic—a sick patient is told they are healthy and does not receive life-saving treatment. A False Positive (a healthy patient is told they might be sick) leads to more tests and anxiety but is a far more acceptable error. You must find all the sick patients.
- Fraudulent Transaction Detection: A False Negative means a fraudulent charge is approved, resulting in a direct financial loss. A False Positive (a legitimate transaction is blocked) is an inconvenience for the customer but is often less costly than losing money to fraud.
- Manufacturing Quality Control: A False Negative means a defective product is shipped to a customer, which could lead to safety issues, brand damage, and costly recalls. A False Positive (a good product is flagged as defective) results in wasted material but is often the lesser of two evils.

---

#### When Not to Use It (as the primary metric)
You should not prioritize Recall when the cost of a False Positive is high.

- Email Spam Detection: A False Positive (a legitimate email goes to spam) is a much bigger problem than a False Negative (a spam email lands in your inbox). In this case, Precision is more important.
- YouTube/Netflix Recommendations: A False Positive is a bad recommendation that frustrates the user. A False Negative is simply a missed opportunity to recommend something good, which is far less noticeable. You want the recommendations you do make to be high quality (high Precision).

---
#### Python code

```
# Import the necessary function
from sklearn.metrics import recall_score

# Assume these are your true labels and model predictions
# There are 4 actual "Spam" emails. The model only finds 3 of them.
y_true = ["Spam", "Spam", "Not Spam", "Spam", "Spam"]
y_pred = ["Spam", "Spam", "Spam",     "Not Spam", "Spam"]

# Manually calculate:
# True Positives (TP) = 3 (correctly predicted "Spam")
# False Negatives (FN) = 1 (incorrectly predicted "Not Spam" when it was "Spam")
# Recall = TP / (TP + FN) = 3 / (3 + 1) = 0.75

# Calculate using scikit-learn
# The `pos_label` argument tells the function which class to consider as "Positive".
recall = recall_score(y_true, y_pred, pos_label="Spam")

print(f"Recall: {recall:.2f}")
# Output:
# Recall: 0.75
```