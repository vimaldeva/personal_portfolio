## What is Ordinal Encoding?
Ordinal Encoding is a data preprocessing technique used to convert categorical features with an intrinsic ranked order into a numerical format. It assigns a unique integer to each category based on its position in the hierarchy.

The key is that the numerical values are assigned in a way that preserves the original ranking of the categories.

Example: For a feature like T-Shirt Size with categories ['Small', 'Medium', 'Large'], Ordinal Encoding would convert them to [0, 1, 2].

---
#### How Does It Work?
The process is simple and requires you to define the order:

Define the Order: First, you must establish the correct sequence of the categories, from lowest to highest. For example, ['Low', 'Medium', 'High'].
Map to Integers: Assign an integer to each category according to its defined rank. The first category gets 0, the second gets 1, and so on.

---
#### What Problem Does It Solve?
It solves the problem of representing ordinal categorical data for machine learning models. It's the middle ground between Label Encoding and One-Hot Encoding.

Compared to One-Hot Encoding: OHE would create separate columns (is_Small, is_Medium, is_Large) and in doing so, would lose the valuable information that Large > Medium.
Compared to simple Label Encoding: While technically the same process, the intent is different. "Label Encoding" is often used as a general term that can be misused on nominal data (e.g., Red=0, Green=1, Blue=2), creating a false order. "Ordinal Encoding" is the correct application of this integer mapping specifically for data that has a real order.
Ordinal Encoding correctly tells the model that there is a monotonic relationship between the categories—one is greater than the other.

---
#### Advantages
- Preserves Order Information: This is its main purpose and biggest advantage. The model can learn relationships like "as education level increases, income tends to increase."
- Simple and Efficient: It's easy to implement and doesn't add new columns to the dataset (unlike One-Hot Encoding), which keeps the feature space small and computationally efficient.

---
#### Disadvantages
- Assumes Equal Spacing: This is a subtle but important drawback. The model will interpret the difference between 0 ('Small') and 1 ('Medium') as being exactly the same as the difference between 1 ('Medium') and 2 ('Large'). In reality, the "distance" between categories might not be uniform.
- Prone to Misuse: It's crucial that you only apply it to features that are truly ordinal. Applying it to nominal data (like Country) will mislead your model by creating a false and arbitrary ranking.

---
#### When to Use It
You should use Ordinal Encoding only when the categorical feature has a clear and meaningful intrinsic order.

Education Levels: ['High School', 'Bachelor\'s', 'Master\'s', 'PhD']
Survey Responses: ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
Quality Tiers: ['Low', 'Medium', 'High', 'Premium']
Clothing Sizes: ['XS', 'S', 'M', 'L', 'XL']

---
#### When Not to Use It
For Nominal Data (No Order): This is the most important rule. For features like Country, Color, Department, or City, there is no logical ranking. Using Ordinal Encoding here would be wrong. Use One-Hot Encoding instead.
When the Order is Arbitrary: If the order doesn't have a real-world, monotonic meaning, don't use it.

---
#### Python code
```
from sklearn.preprocessing import OrdinalEncoder

# Create a sample DataFrame
df = pd.DataFrame({
    'size': ['M', 'L', 'S', 'L', 'S'],
    'quality': ['Good', 'Excellent', 'Bad', 'Good', 'Excellent']
})

# 1. Define the order for the categories in a list of lists
# The order of the inner lists must match the order of the columns in the DataFrame
category_order = [
    ['S', 'M', 'L'],  # Order for the 'size' column
    ['Bad', 'Good', 'Excellent'] # Order for the 'quality' column
]

# 2. Instantiate the encoder with the defined order
encoder = OrdinalEncoder(categories=category_order)

# 3. Fit and transform the data
encoded_data = encoder.fit_transform(df[['size', 'quality']])

# Add the new encoded columns back to the DataFrame
df['size_encoded'] = encoded_data[:, 0]
df['quality_encoded'] = encoded_data[:, 1]


print("\nDataFrame after scikit-learn OrdinalEncoder:")
print(df)
```

