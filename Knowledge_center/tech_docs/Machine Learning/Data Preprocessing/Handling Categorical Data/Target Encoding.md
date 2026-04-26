#### What is Target Encoding?
Target Encoding is a technique that replaces a categorical feature with the mean of the target variable for that specific category. It directly encodes information about the target into the feature itself, creating a very powerful and predictive new feature.

It's also known by other names, including Mean Encoding or Bayesian Encoding (when smoothing is applied).

Example: Imagine you are predicting if a customer will Churn (1 for Yes, 0 for No) based on their City.

| City | Churn |
| :-- | :-- |
| San Francisco | 1 |
| New York | 0 |
| San Francisco | 1 |
| Boston | 0 |
| New York | 1 |
| San Francisco | 0 |

To target encode the City column:

Group by City:
San Francisco: 3 customers, 2 churned.
New York: 2 customers, 1 churned.
Boston: 1 customer, 0 churned.
Calculate the Mean of Churn for each city:
San Francisco: (1 + 1 + 0) / 3 = 0.67
New York: (0 + 1) / 2 = 0.50
Boston: 0 / 1 = 0.0
Replace the city names with these means:

| City (Original) | City (Encoded) |
| :-- | :-- |
| San Francisco | 0.67 |
| New York | 0.50 |
| San Francisco | 0.67 |
| Boston | 0.00 |
| New York | 0.50 |
| San Francisco | 0.67 |

---

#### What Problem Does It Solve?
Target Encoding is the go-to solution for high-cardinality categorical features (features with many unique categories, like ZIP Code, City, or Product ID).

One-Hot Encoding would create thousands of new columns, making the dataset huge and sparse.
Ordinal Encoding is incorrect as there is no inherent order.
Target Encoding solves this by converting a feature with thousands of categories into a single, powerful numerical feature.

---
#### The Critical Problem: Target Leakage and Overfitting
This is the most important concept to understand about Target Encoding. The "naive" approach described above has a fatal flaw: it causes target leakage.

When you calculate the encoding for a row, you are using the target value of that very same row. The feature now contains information it would never have in a real-world prediction scenario. This leads to a model that looks amazing during training but fails miserably on new, unseen data.

How to Do It Correctly (The Solutions):

Smoothing (Bayesian Encoding): What about a city with only one customer who happened to churn? Its encoded value would be 1.0, which is an extremely confident but unreliable signal. Smoothing addresses this by blending the category's mean with the overall global mean of the target.

Encoded_Value = (w * category_mean) + ((1 - w) * global_mean)

The weight w is based on the size of the category. A common way to calculate it is w = n / (n + m), where n is the number of samples in the category and m is a smoothing factor.

If n is large, w is close to 1, and we trust the category's mean.
If n is small, w is close to 0, and we pull the value closer to the global average.
Using a Cross-Validation Scheme: This is the most robust way to prevent leakage. For a 5-fold cross-validation:

Split your training data into 5 folds.
For fold 1, calculate the encodings using only the data from folds 2, 3, 4, and 5. Then apply these encodings to the data in fold 1.
Repeat this for all 5 folds. This ensures that the encoding for any given row is calculated without using its own target value.

---
#### Advantages
- Handles High Cardinality: This is its primary purpose and strength.
- Creates a Highly Predictive Feature: It directly captures the relationship between the feature and the target.
- Simple and Efficient (in prediction): It results in just one new column, making the model fast.

---
#### Disadvantages
- Prone to Overfitting: This is its biggest danger. If not implemented carefully with smoothing and proper validation, it will lead to target leakage and a useless model.
- Complex to Implement Correctly: Unlike One-Hot Encoding, a correct implementation requires careful handling of validation schemes.
- Sensitive to Outliers: An outlier in the target variable can significantly affect the mean for a smaller category.

---
#### When to Use It
- For high-cardinality categorical features where other methods are impractical.
- When you are confident in your validation setup to prevent target leakage.
- In competitions or scenarios where squeezing out maximum predictive power is the primary goal.

---
#### When Not to Use It
- When simpler methods like One-Hot Encoding are feasible (i.e., for low-cardinality features).
- If you are not prepared to implement a robust validation strategy. The risk of getting it wrong is high.
- If the feature has little to no relationship with the target, target encoding will just add noise.

---
#### Python code

```
import pandas as pd
from category_encoders import TargetEncoder
from sklearn.model_selection import train_test_split

# Create a sample DataFrame
df = pd.DataFrame({
    'city': ['New York', 'San Francisco', 'New York', 'Boston', 'San Francisco', 'New York', 'Boston', 'Boston'],
    'churn': [1, 0, 0, 1, 1, 0, 0, 1]
})

# Split data into train and test sets
X = df[['city']]
y = df['churn']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

# 1. Instantiate the TargetEncoder
# The `smoothing` parameter is the 'm' from our formula. It controls how much we blend with the global mean.
encoder = TargetEncoder(smoothing=2.0)

# 2. Fit the encoder on the TRAINING data only
# This learns the mean of the target for each city from the training set.
encoder.fit(X_train, y_train)

# 3. Transform both the training and test data
# It applies the learned mappings to both sets.
# It will also handle cities in the test set that were not in the training set by using the global mean.
X_train_encoded = encoder.transform(X_train)
X_test_encoded = encoder.transform(X_test)


print("--- Training Data ---")
print("Original:\n", X_train)
print("\nEncoded:\n", X_train_encoded)

print("\n--- Test Data ---")
print("Original:\n", X_test)
print("\nEncoded:\n", X_test_encoded)

# Let's see the mapping it learned from the training data
# Training data: SF(1), NY(0), BOS(1), BOS(0) -> SF=1.0, NY=0.0, BOS=0.5
print("\nLearned Mapping:")
print(encoder.mapping)
```

