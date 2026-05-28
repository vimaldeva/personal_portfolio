## Label Encoding
Label Encoding is a technique used in machine learning to convert categorical data (text-based labels) into numerical format. Each unique category in a column is assigned an integer starting from 0, 1, 2, and so on.

For example, if you have a "City" column:

London → 0
New York→ 1
Paris → 2

---
### Advantages
- Simplicity: It is very easy to implement and understand.
- Memory Efficiency: It doesn't increase the number of columns in your dataset (unlike One-Hot Encoding). It keeps the data compact.
- Requirement for Algorithms: Most machine learning libraries (like Scikit-Learn) cannot handle strings directly; they require numbers.

---
### Disadvantages
- The "Order" Problem: This is the biggest drawback. Label encoding introduces a mathematical order that might not exist.
- Example: If London = 0 and Paris = 2, the model might think "Paris is greater than London" or that the average of London and Paris is New York (1).
- Model Bias: Linear models (Linear Regression, Logistic Regression) and distance-based models (KNN, SVM) can get confused by these numbers and assign weights based on the arbitrary integer value.

 ---
 ### When to use it?
- Ordinal Data: When the categories have a natural rank or order.
- Example: Education (High School < Bachelor's < Master's < PhD) or Size (Small < Medium < Large).
- Target Variable (y): It is commonly used to encode the output/label you are trying to predict in a classification problem.
- Tree-based Models: Algorithms like Random Forest, XGBoost, and Decision Trees are usually "smart" enough to handle label-encoded features because they split data based on values rather than calculating distances or weights.

---
### When NOT to use it?
- Nominal Data: When there is no natural order between categories.
- Example: Colors (Red, Green, Blue), Countries, or Gender.
- Linear/Distance Models: Avoid using it for Linear Regression, KNN, or K-Means clustering for features, as the artificial ranking will distort the results. Use One-Hot Encoding instead for these models.

---
### Sample Code in Python

```
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# 1. Create a sample dataset
data = {'User_ID': [1, 2, 3, 4, 5],
        'Education': ['High School', 'Masters', 'Bachelors', 'Masters', 'High School']}

df = pd.DataFrame(data)
print("Original Data:")
print(df)

# 2. Initialize the LabelEncoder
le = LabelEncoder()

# 3. Fit and Transform the column
# This converts 'High School', 'Masters', 'Bachelors' into 0, 1, 2
df['Education_Encoded'] = le.fit_transform(df['Education'])

print("\nAfter Label Encoding:")
print(df)

# 4. To see which number represents which category
mapping = dict(zip(le.classes_, le.transform(le.classes_)))
print("\nMapping:", mapping)

# 5. To reverse it back to original text
# df['Original'] = le.inverse_transform(df['Education_Encoded'])
```

| Feature | Label Encoding | One-Hot Encoding |
| :-- | :-- | :-- |
| Data Type | Best for Ordinal (Ranked) | Best for Nominal (Unranked) |
| Dimensions | Keeps same number of columns | Increases number of columns |
| Model Type | Good for Decision Trees | Good for Linear Models / KNN |
| Potential Issue | Introduces fake mathematical order | Can cause "Dimensionality Curse" |
