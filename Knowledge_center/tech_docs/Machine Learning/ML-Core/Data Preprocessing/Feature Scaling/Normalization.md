## What is Normalization (Min-Max Scaling)?
Normalization is a data preprocessing technique used to rescale numerical features to a fixed, common range, typically 0 to 1.

It transforms the data by "squishing" or "stretching" the values in a column so that the minimum value becomes 0 and the maximum value becomes 1, with all other values falling somewhere in between.

---
#### How Does It Work?
The transformation is applied to each value in a feature column using the following formula:

X_normalized = (X - X_min) / (X_max - X_min)

Where:

X is the original value.
X_min is the minimum value in the entire column.
X_max is the maximum value in the entire column.
Example: Imagine a feature Age with values [20, 30, 50].

X_min = 20
X_max = 50
The transformation would be:

For age 20: (20 - 20) / (50 - 20) = 0 / 30 = 0.0
For age 50: (50 - 20) / (50 - 20) = 30 / 30 = 1.0
For age 30: (30 - 20) / (50 - 20) = 10 / 30 ≈ 0.33
The new scaled feature would be [0.0, 0.33, 1.0]

---
#### What Problem Does It Solve?
It solves the problem of features having vastly different scales, which can cause machine learning models to perform poorly. Many algorithms are sensitive to the scale of the input data.

Example: Consider a model predicting house prices using number_of_rooms (range: 1-10) and area_in_sq_ft (range: 500-5000). The large values of area_in_sq_ft will completely dominate the small values of number_of_rooms. The model might incorrectly learn that area is a much more important feature simply because its numbers are bigger.

Normalization puts all features on a level playing field, ensuring that they contribute equally to the model's learning process.

---
#### Advantages
- Guarantees a Bounded Range: The output is always between 0 and 1, which can be a strict requirement for some algorithms, especially in neural networks.
- Intuitive to Understand: The concept of scaling to a 0-1 range is very straightforward.

---
#### Disadvantages
- Highly Sensitive to Outliers: This is its biggest weakness. If you have an outlier with an extreme value, it will become the new min or max. This will cause all the other "normal" data points to be "squished" into a very tiny sub-range, effectively losing their variance and making them harder to distinguish.
- Doesn't Handle New Data Well: If new data comes in that is outside the original min/max range, the scaled values will fall outside the 0-1 range.

---
#### When to Use It
- Neural Networks: It is commonly used for image data (scaling pixel values from 0-255 to 0-1) and is often a good choice for inputs to neural networks, especially when using activation functions like Sigmoid or Tanh that are sensitive to the input range.
- When your data does not follow a Gaussian (normal) distribution.
- When you need your data to be in a bounded range for specific calculations or visualizations.

---
#### When Not to Use It
- When your data has significant outliers. In this case, Standardization is a much safer and more robust choice.
For Tree-Based Models: Algorithms like Decision Trees, Random Forests, and Gradient Boosting are not sensitive to the scale of features because they make decisions by splitting data based on thresholds, not by calculating distances. Scaling is not necessary for them.
- When your data generally follows a normal distribution. Standardization is a more natural fit in this scenario.

---
#### Python code
```
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

# Create a sample DataFrame
data = {
    'age': [25, 30, 45, 60, 80],
    'income': [50000, 60000, 90000, 75000, 120000]
}
df = pd.DataFrame(data)

# Split data into train and test sets
X_train, X_test = train_test_split(df, test_size=0.4, random_state=42)

print("--- Original Data ---")
print("Train:\n", X_train)
print("\nTest:\n", X_test)
print("-" * 30)

# 1. Instantiate the scaler
scaler = MinMaxScaler()

# 2. Fit the scaler on the TRAINING data only and transform it
# This learns the min and max from the training data.
X_train_scaled = scaler.fit_transform(X_train)

# 3. Transform the TEST data using the scaler that was fit on the training data
# This ensures the same scaling transformation is applied to both sets.
X_test_scaled = scaler.transform(X_test)

# Convert the scaled arrays back to DataFrames for clarity
X_train_scaled_df = pd.DataFrame(X_train_scaled, columns=X_train.columns, index=X_train.index)
X_test_scaled_df = pd.DataFrame(X_test_scaled, columns=X_test.columns, index=X_test.index)

print("\n--- Scaled Data ---")
print("Train Scaled:\n", X_train_scaled_df)
print("\nTest Scaled:\n", X_test_scaled_df)

# You can inspect the learned min and max values
print("\nMin values learned from training data:", scaler.min_)
print("Scale (1/(max-min)) learned from training data:", scaler.scale_)
```