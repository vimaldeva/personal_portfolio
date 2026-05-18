## K Nearest Neighbors
K-Nearest Neighbors (KNN) is a supervised machine learning algorithm used for classification and regression tasks. It predicts the output for a new data point by analyzing the 'k' nearest data points in the training dataset. The algorithm is simple, non-parametric, and instance-based, making it versatile for various applications.

---

#### How K-Nearest Neighbors (KNN) Works
The core principle of KNN is "tell me who your neighbors are, and I'll tell you who you are." It operates on the idea that data points with similar features will have similar outcomes.

Here’s the step-by-step process for making a prediction for a new, unseen data point:

Choose a Value for K: First, you must choose a value for "K," which represents the number of nearest neighbors to consider. This is a critical hyperparameter.

Calculate Distances: The algorithm calculates the distance between the new data point and every single point in the training dataset. The most common distance metric used is Euclidean Distance (the straight-line distance between two points), but others like Manhattan distance can also be used.

Identify the K-Nearest Neighbors: The algorithm identifies the "K" training data points that are closest (have the smallest distance) to the new point.

Make a Prediction:

For Classification (KNeighborsClassifier): The algorithm takes a majority vote among the K-nearest neighbors. The new data point is assigned to the class that is most common among its K neighbors. For example, if K=5 and 3 of the neighbors are 'Class A' and 2 are 'Class B', the new point will be classified as 'Class A'.
For Regression (KNeighborsRegressor): The algorithm takes the average of the target values of the K-nearest neighbors. For example, if K=5 and the house prices of the 5 nearest neighbors are $200k, $210k, $190k, $220k, and $205k, the predicted price for the new house would be the average of these values.

Choosing the right k is crucial:

A small k (e.g., 1) may lead to overfitting.

A large k may result in underfitting.

---

#### Advantages of KNN
- Extremely Simple and Intuitive: It's one of the easiest machine learning algorithms to understand and explain.
- No Training Phase: KNN is a "lazy learner." It doesn't perform any computation during the training phase; it simply stores the entire dataset. This makes the "training" process instantaneous.
- Adapts Easily: As new data becomes available, it can be added to the dataset without needing to retrain a model from scratch.
- Naturally Handles Multi-Class Problems: The voting mechanism works just as easily for problems with more than two classes.
- Can Model Complex Boundaries: With a small value of K, it can learn very complex, non-linear decision boundaries.

---

#### Disadvantages of KNN
- Computationally Expensive at Prediction Time: This is its biggest drawback. Because it has to compute the distance to every single training point for each new prediction, it can be very slow if the training dataset is large.
- Highly Sensitive to Irrelevant Features (Curse of Dimensionality): In high-dimensional spaces, the concept of "distance" becomes less meaningful. Irrelevant features can easily dominate the distance calculation, leading to poor performance.
- Requires Feature Scaling: KNN is highly sensitive to the scale of the data. Features with larger ranges (e.g., salary) will have a much larger impact on the distance calculation than features with smaller ranges (e.g., age). Therefore, it is crucial to scale your data (e.g., using StandardScaler or MinMaxScaler) before using KNN.
- Must Choose an Optimal K: The performance of the model is highly dependent on the choice of K.
- A small K (e.g., K=1) makes the model very sensitive to noise and can lead to overfitting.
- A large K makes the decision boundary smoother but can lead to underfitting (oversimplifying the model).
- Large Memory Requirement: It needs to store the entire training dataset in memory, which can be a problem for very large datasets.

---
#### When to Use KNN
- On Small to Medium-Sized Datasets: It works best when the dataset is not too large, so prediction times remain reasonable.
- When Interpretability is Simple: While not interpretable in the same way as a Decision Tree, you can easily inspect the neighbors of a new point to understand why a certain prediction was made.
- As a Baseline Model: Due to its simplicity, it's a great algorithm to use as a baseline to compare against more complex models.
- For Problems with a Clear "Neighborhood" Concept: It's a natural fit for problems where local similarity is a strong predictor, such as recommendation systems ("users who liked this also liked...").

---
#### When Not to Use KNN
- On Large Datasets: The slow prediction speed makes it impractical for large-scale applications.
=- On High-Dimensional Datasets: It suffers from the "curse of dimensionality." As the number of features grows, the distance between points becomes less meaningful.
- When Prediction Speed is Critical: For real-time applications that require fast predictions, KNN is generally not a good choice.
- When the Dataset Has a Lot of Noise or Irrelevant Features.

---
#### Python code

```
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.preprocessing import StandardScaler

iris = load_iris()
X = iris.data
y = iris.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Step 4: Scale the features (CRUCIAL for KNN)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Step 5: Create and train the KNN model
# We'll start with a common choice for K, like K=5.
knn_classifier = KNeighborsClassifier(n_neighbors=5)

# KNN doesn't really "train" but "fits" by storing the data.
knn_classifier.fit(X_train_scaled, y_train)

# Step 6: Make predictions on the scaled test data
y_pred = knn_classifier.predict(X_test_scaled)

# Step 7: Evaluate the model's performance
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy (with K=5): {accuracy:.2f}")

# Display the confusion matrix
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=iris.target_names)
disp.plot()
plt.title("Confusion Matrix for KNN (K=5)")
plt.show()

# Step 8: Find the optimal value for K
# A common way is to test a range of K values and see which one performs best.
k_range = range(1, 31)
k_scores = []

for k in k_range:
    knn = KNeighborsClassifier(n_neighbors=k)
    # Use cross-validation to get a more robust score for each K
    scores = cross_val_score(knn, X_train_scaled, y_train, cv=5, scoring='accuracy')
    k_scores.append(scores.mean())

# Plot the results to find the "elbow"
plt.figure(figsize=(10, 6))
plt.plot(k_range, k_scores, marker='o')
plt.xlabel('Value of K for KNN')
plt.ylabel('Cross-Validated Accuracy')
plt.title('Finding the Optimal K')
plt.xticks(k_range)
plt.grid(True)
plt.show()

# Find the K with the highest score
optimal_k = k_range[np.argmax(k_scores)]
print(f"\nThe optimal value for K is: {optimal_k}")
```