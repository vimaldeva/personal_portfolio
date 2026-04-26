#### What is Frequency Encoding?
Frequency Encoding is a technique that replaces each category in a categorical feature with its frequency—that is, the total number of times that category appears in the dataset.

You can use either the raw count or the normalized percentage (fraction) of the total.

Example: Imagine you have a feature called Brand:

| ID | Brand |
| :-- | :-- |
| 1 | Apple |
| 2 | Samsung |
| 3 | Apple |
| 4 | Google |
| 5 | Apple |

Count the frequencies:
Apple: 3 times
Samsung: 1 time
Google: 1 time
Replace the brand names with their counts:

| ID | Brand (Original) | Brand (Encoded) |
| :-- | :-- | :-- |
| 1 | Apple | 3 |
| 2 | Samsung | 1 |
| 3 | Apple | 3 |
| 4 | Google | 1 |
| 5 | Apple | 3 |

---
#### What Problem Does It Solve?
Like Target Encoding, Frequency Encoding is primarily used to handle high-cardinality categorical features (features with many unique categories).

One-Hot Encoding would explode the number of features, making the dataset too large.
Ordinal Encoding is incorrect as there's no inherent order.
Frequency Encoding provides a way to convert a high-cardinality feature into a single numerical column without creating a massive feature space. It captures the "popularity" or "rarity" of a category, which can be a useful signal for the model.

---
#### Advantages
- Simple and Fast: It's very easy to understand and computationally cheap to implement.
- Handles High Cardinality: This is its main strength. It efficiently converts features with thousands of categories into a single numerical feature.
- No Target Leakage: This is a crucial advantage over Target Encoding. The encoding is calculated using only the feature itself (X), so there is no risk of leaking information from the target variable (y). This makes it much safer to use.
- Captures Importance/Rarity: The frequency of a category can be a useful piece of information. For example, a very popular product might have different characteristics than a niche one.

---
#### Disadvantages
- Collisions: This is the most significant drawback. If two different categories have the same frequency, they will be assigned the same encoded value. The model will then be unable to distinguish between them, leading to a loss of information. In our example, Samsung and Google both get encoded to 1.
- Doesn't Handle New Categories: If a category appears in the test set that was not present in the training set, its frequency is unknown. You would have to decide on a default value to assign it (e.g., 0 or 1).
No Order Information: It does not preserve any inherent order in the categories.

---
#### When to Use It
- For high-cardinality features where One-Hot Encoding is not feasible.
- As a safer, simpler alternative to Target Encoding, especially if you are worried about target leakage.
- When you believe the frequency or popularity of a category is a useful predictive signal.
- It often works well with tree-based models (like Random Forest, LightGBM, XGBoost) as they can easily find splits in the numerical frequency values.

---
#### When Not to Use It
- When the number of categories is small. One-Hot Encoding is generally safer and more expressive in this case, as it avoids collisions.
- When you have distinct categories that happen to have the same frequency but have a very different relationship with the target variable. The collision would hurt model performance.
- When preserving the unique identity of every category is critical.

---
#### Python code 

```
import pandas as pd

# Create a sample DataFrame
df = pd.DataFrame({
    'brand': ['Apple', 'Samsung', 'Apple', 'Google', 'Apple', 'Samsung', 'Xiaomi', 'Google', 'Apple', 'Xiaomi'],
    'purchased': [1, 0, 1, 1, 1, 0, 0, 0, 1, 1]
})

# --- Simple implementation on the whole dataset (for exploration) ---
frequency_map = df['brand'].value_counts().to_dict()
df['brand_freq_encoded'] = df['brand'].map(frequency_map)

print("--- Encoding on full dataset (for understanding) ---")
print(df)
print("-" * 50)


# --- Correct implementation for a Machine Learning pipeline ---
# Split data into train and test sets
train_df = df.sample(frac=0.7, random_state=42)
test_df = df.drop(train_df.index)

print("--- Correct ML Implementation ---")
print("Train DF:\n", train_df)
print("\nTest DF:\n", test_df)
print("-" * 20)

# 1. Learn the frequency map from the TRAINING data only
freq_map_train = train_df['brand'].value_counts().to_dict()
print("Frequency map learned from training data:\n", freq_map_train)

# 2. Apply the learned map to both the training and test sets
train_df['brand_encoded'] = train_df['brand'].map(freq_map_train)
test_df['brand_encoded'] = test_df['brand'].map(freq_map_train)

# 3. Handle potential new categories in the test set
# The 'Xiaomi' brand might not have been in the training set. In that case, its value would be NaN.
# We fill these NaNs with a default value, like 0 or 1.
test_df['brand_encoded'].fillna(0, inplace=True)


print("\nEncoded Train DF:\n", train_df)
print("\nEncoded Test DF:\n", test_df)
```