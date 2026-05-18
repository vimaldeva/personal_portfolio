#### What is Precision?

Precision is a classification metric that answers the question: "Of all the times the model predicted a positive outcome, how many times was it actually correct?"

It measures the quality of the positive predictions. A model with high precision is trustworthy when it says something is positive, because it generates very few False Positives.

---
#### How to Calculate It
Precision is calculated using values from the Confusion Matrix:

```
Formula: Precision = True Positives / (True Positives + False Positives) 
```
In simple terms, it's the number of correct positive predictions divided by the total number of positive predictions the model made.

---

#### What Problem Does It Solve?
Precision directly addresses the cost of False Positives. It helps you evaluate a model in situations where incorrectly labeling a negative case as positive is very damaging or costly. It answers whether a model is "crying wolf" too often.

---

#### Advantages
- Focus on Reliability: It provides a clear measure of how reliable the model's positive predictions are.
- Intuitive for Stakeholders: The concept of "when we predict X, we are right Y% of the time" is easy for non-technical audiences to understand.
- Crucial for Certain Business Problems: It is the most important metric when the consequences of a False Positive are high (e.g., wasted money, poor user experience, unnecessary panic).

---

#### Disadvantages
- Completely Ignores False Negatives: This is its biggest weakness. A model can achieve perfect (100%) precision by being extremely conservative and only making a positive prediction when it is absolutely certain. In doing so, it might miss a large number of actual positive cases (high False Negatives), but Precision alone won't tell you that.
- Can be Misleading in Isolation: Because it ignores False Negatives, it should never be the sole metric used to evaluate a model, especially when finding all positive cases is important.

---
### When to Use It
You should prioritize Precision when the cost of a False Positive is significantly higher than the cost of a False Negative.

- Email Spam Detection: A False Positive means a legitimate email (like a job offer or a message from family) is sent to the spam folder. This is a very bad outcome. A False Negative (a spam email in your inbox) is just a minor annoyance. Therefore, you want high precision.
- Search Engine Results: When you search for something, you want the top results (the "positive" predictions) to be highly relevant. A False Positive is an irrelevant link on the first page, which wastes your time. You'd rather have the search engine miss a few good links (False Negatives) than show you junk.
- Recommender Systems (e.g., YouTube, Netflix): When a platform recommends a video or movie, it is making a positive prediction ("you will like this"). A False Positive is a bad recommendation, which leads to user frustration and loss of trust.

---

#### When Not to Use It (as the primary metric)
You should not prioritize Precision when the cost of a False Negative is high.

- Medical Screening for a Serious Disease: A False Negative means a sick person is told they are healthy, and they don't receive treatment. This is a catastrophic outcome. A False Positive (a healthy person is told they might be sick) leads to more tests and anxiety but is far less dangerous. In this case, Recall is the more important metric.
- Fraudulent Transaction Detection: A False Negative means a fraudulent transaction is allowed to go through, and money is lost. This is a direct financial loss. A False Positive (a legitimate transaction is blocked) is a bad customer experience but can often be resolved. Here, you need a balance, but you cannot ignore the False Negatives.

---
#### Python code
```
# Import the necessary function
from sklearn.metrics import precision_score

# Assume these are your true labels and model predictions
# Model made 3 positive predictions ("Spam"), but only 2 were correct.
y_true = ["Not Spam", "Spam", "Spam", "Not Spam", "Spam"]
y_pred = ["Not Spam", "Spam", "Not Spam", "Spam", "Spam"]

# Manually calculate:
# True Positives (TP) = 2 (correctly predicted "Spam")
# False Positives (FP) = 1 (incorrectly predicted "Spam" when it was "Not Spam")
# Precision = TP / (TP + FP) = 2 / (2 + 1) = 0.667

# Calculate using scikit-learn
# The `pos_label` argument tells the function which class to consider as "Positive".
precision = precision_score(y_true, y_pred, pos_label="Spam")

print(f"Precision: {precision:.3f}")
# Output:
# Precision: 0.667
```