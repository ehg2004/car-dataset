import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Load dataset from CSV (replace 'your_dataset.csv' with the actual file)
df = pd.read_csv('processed_dataset1.csv')

# Select numerical features for clustering (modify as needed)
numeric_features = df.select_dtypes(include=[np.number])

# Drop rows with missing values (optional)
numeric_features = numeric_features.dropna()

# Normalize the dataset
scaler = StandardScaler()
X_scaled = scaler.fit_transform(numeric_features)

# Reduce dimensionality using PCA (for faster computation)
pca = PCA(n_components=4,)  # Reduce to 2 features
X_reduced = pca.fit_transform(X_scaled)

# Try k values from 2 to 10
k_values = range(2, 11)
silhouette_scores = []

for k in k_values:
    print(f"calculating k={k}")
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)
    score = silhouette_score(X_reduced, labels, sample_size=min(10000, len(X_reduced)))  # Limit to 1000 samples    print(k)
    silhouette_scores.append(score)

# Find the best k
best_k = k_values[np.argmax(silhouette_scores)]

# Plot silhouette scores
plt.figure(figsize=(8, 4))
plt.plot(k_values, silhouette_scores, marker='o', linestyle='--')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Score for Different k Values')
plt.grid()
plt.show()
    

# Perform k-Means with the best k
best_kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
best_labels = best_kmeans.fit_predict(X_reduced)

# Scatter plot of PCA-reduced features
plt.figure(figsize=(8, 6))
plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=best_labels, cmap='viridis', alpha=0.6)
plt.scatter(best_kmeans.cluster_centers_[:, 0], best_kmeans.cluster_centers_[:, 1], 
            c='red', marker='X', s=200, label='Centroids')
plt.xlabel('PCA Feature 1')
plt.ylabel('PCA Feature 2')
plt.title(f'Best k-Means Clustering (k={best_k})')
plt.legend()
plt.show()
