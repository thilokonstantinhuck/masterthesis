import cv2
import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt

# Step 1: Load the image
image = cv2.imread('japaneseFlag.jfif')

# Step 2: Get the dimensions of the image
height, width, _ = image.shape

# Step 3: Extract the Red channel
red_channel = image[:, :, 1]  # OpenCV uses BGR, the red channel is index 1

# Visualize the clustered band image
plt.figure(figsize=(10, 10))
plt.imshow(red_channel, cmap='jet')
plt.title(f'Red Channel')
plt.axis('on')
plt.colorbar()
plt.show()

# Step 4: Create the feature matrix: [Red, X, Y]
X = np.zeros((height * width, 3))

for y in range(height):
    for x in range(width):
        red = red_channel[y, x]
        X[y * width + x] = [red, x, y]

# Step 5: Apply DBSCAN
dbscan = DBSCAN(eps=10, min_samples=50).fit(X)

# Step 6: Reshape the labels back into the image shape
labels = dbscan.labels_.reshape(height, width)

# Step 7: Create a mask showing the top 3 clusters in different colors
unique_labels, counts = np.unique(labels, return_counts=True)

# Ignore noise label (-1) if present
sorted_indices = np.argsort(-counts)  # Sort clusters by size, descending
top_3_clusters = unique_labels[sorted_indices[:5]]  # Get top 3 clusters (plus noise label if present)

# Initialize a color mask
color_mask = np.zeros((height, width, 3), dtype=np.uint8)

# Define colors for the clusters
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Red, Green, Blue

# Assign colors to each of the top 3 clusters
for idx, label in enumerate(top_3_clusters):
    if label != -1:  # Exclude noise
        color_mask[labels == label] = colors[idx % len(colors)]

# Step 8: Display the original image and the color mask
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title('Original Image')

plt.subplot(1, 2, 2)
plt.imshow(color_mask)
plt.title('Top 3 Clusters Mask in Colors')
plt.show()
