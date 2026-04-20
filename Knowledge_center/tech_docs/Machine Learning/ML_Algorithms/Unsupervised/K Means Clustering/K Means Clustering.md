## K Means clustering

K-Means is an unsupervised machine learning algorithm used for clustering data into distinct groups based on similarity. It is widely applied in tasks like market segmentation, image compression, and document clustering. The algorithm aims to minimize the variance within clusters while maximizing the difference between clusters.

What is K-Means Clustering?
The objective of K-Means is to partition a dataset into K distinct, non-overlapping clusters. It tries to group the data in such a way that data points within the same cluster are very similar, while data points in different clusters are very different.

It achieves this by finding and updating cluster "centers," known as centroids.

---

#### How K-Means Works: The Algorithm
The K-Means algorithm is an iterative process that can be broken down into a few simple steps. Imagine it as a dance between assigning points to groups and then moving the center of those groups.

Step 1: Choose K. You, the user, must first specify the number of clusters (K) you want to find in the data. This is a critical hyperparameter.

Step 2: Initialize Centroids. The algorithm randomly selects K data points from your dataset and designates them as the initial cluster centroids. (A smarter initialization method called k-means++ is often used to improve results, but the concept is the same).

Step 3: Assign Points to Clusters. The algorithm goes through each data point and calculates its distance to every centroid (usually using Euclidean distance). It then assigns the data point to the cluster whose centroid is closest.

Step 4: Update Centroids. Once all points have been assigned to a cluster, the algorithm recalculates the position of the K centroids. The new position of a centroid is the mean (average) of all the data points assigned to its cluster. This is where the "Means" in K-Means comes from.

Step 5: Repeat and Converge. Steps 3 and 4 are repeated iteratively. With each iteration, the centroids shift, and points may get reassigned to different clusters. This process continues until the centroids no longer move significantly, or the cluster assignments stabilize. At this point, the algorithm has converged, and the final clusters are formed.

---

#### Advantages of K-Means
- Simplicity and Speed: It is very easy to understand and implement. It is also computationally very fast and efficient, especially for large datasets.
- Scalability: It scales well to large numbers of samples (n).
- Guaranteed Convergence: The algorithm is guaranteed to converge to a solution (though not necessarily the best possible solution).

---

#### Disadvantages of K-Means
- You Must Choose K Manually: The biggest drawback is that you have to specify the number of clusters, K. This can be difficult if you don't have prior knowledge of the data. The Elbow Method is a common technique used to help find a good value for K.
- Sensitive to Initial Centroid Placement: The random initialization of centroids can lead to different final clusters. To mitigate this, the algorithm is usually run multiple times with different random initializations, and the best result is chosen.
- Assumes Spherical, Equally Sized Clusters: This is a critical limitation. K-Means works by minimizing the distance to a central point, so it implicitly assumes that clusters are circular or spherical and roughly the same size. It performs poorly on clusters with complex shapes (e.g., elongated ovals, crescents) or varying densities.
- Sensitive to Feature Scaling: Just like KNN, K-Means uses distance calculations. Therefore, it is essential to scale your data before applying the algorithm to prevent features with larger scales from dominating the distance metric.
- Sensitive to Outliers: Outliers can pull a centroid towards them, distorting the final cluster.

---

#### When to Use K-Means
- Customer Segmentation: Grouping customers based on purchasing behavior, demographics, or website activity (e.g., "high-spending recent visitors," "low-spending infrequent visitors").
- Document Clustering: Grouping articles, books, or news stories by topic.
- Image Compression (Color Quantization): Reducing the number of colors in an image by clustering similar colors together and replacing them with the cluster's centroid color.
- As a Preprocessing Step: Can be used to create a new categorical feature for a supervised learning model (e.g., "which cluster does this data point belong to?").

---

#### When Not to Use K-Means
- When clusters have complex shapes or different densities. For these cases, more advanced algorithms like DBSCAN (Density-Based Spatial Clustering of Applications with Noise) are a much better choice.
- When the dataset contains many outliers.
- When you have categorical data. K-Means relies on distance metrics that are not well-defined for categorical features.

---

#### Pyrhon code

```
# Step 1: Import necessary libraries
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Step 2: Generate synthetic data
# make_blobs is great for testing clustering algorithms because we know the "true" number of clusters.
X, y = make_blobs(n_samples=300, centers=4, cluster_std=0.8, random_state=42)

# Visualize the generated data
plt.figure(figsize=(8, 6))
plt.scatter(X[:, 0], X[:, 1], s=50)
plt.title("Raw Unclustered Data")
plt.show()

# Step 3: Scale the data (important for K-Means)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 4: Use the Elbow Method to find the optimal K
# We will calculate the "inertia" for a range of K values.
# Inertia is the sum of squared distances of samples to their closest cluster center.
inertia = []
k_range = range(1, 11)

for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10) # n_init=10 to run 10 times with different seeds
    kmeans.fit(X_scaled)
    inertia.append(kmeans.inertia_)

# Plot the Elbow curve
plt.figure(figsize=(8, 6))
plt.plot(k_range, inertia, marker='o')
plt.xlabel('Number of clusters (K)')
plt.ylabel('Inertia')
plt.title('The Elbow Method')
plt.xticks(k_range)
plt.grid(True)
plt.show()

# From the plot, the "elbow" is clearly at K=4. After this point, the inertia decreases much more slowly.

# Step 5: Run K-Means with the optimal K
optimal_k = 4
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
kmeans.fit(X_scaled)
y_kmeans = kmeans.predict(X_scaled)

# Step 6: Visualize the results
plt.figure(figsize=(8, 6))
# Plot the data points, colored by their assigned cluster
plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=y_kmeans, s=50, cmap='viridis')

# Plot the final centroids
centers = kmeans.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c='red', s=200, alpha=0.75, marker='X', label='Centroids')
plt.title(f'K-Means Clustering with K={optimal_k}')
plt.legend()
plt.show()
```