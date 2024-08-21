import spectral.io.envi as envi
import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from skimage import morphology

# Load the hyperspectral image
hdr = r"D:\Salmon_HSI_NP_15032023\SWIR_Hyspex\All_converted_file\S6-R-G1_SWIR_384_SN3151_9006us_2022-05-02T120753_raw_rad_float32.hdr"
img = envi.open(hdr)
hsi_image = img.load()

# Specify the band you want to use for clustering (e.g., band 50)
band_index = 23  # Change this to the band index you want to use (0-based index)

# Extract the specified band
band_image = hsi_image[:, :, band_index]

# Visualize the clustered band image
plt.figure(figsize=(10, 10))
plt.imshow(band_image, cmap='jet', vmin=0.35, vmax=0.05)
plt.title(f'Image - Band {band_index} (with Position)')
plt.axis('on')
plt.colorbar()
plt.show()

# Get the spatial coordinates
rows, cols = band_image.shape
x, y = np.indices((rows, cols))

# Reshape the band image and coordinates to a 2D array (num_pixels, 3)
# Here, each pixel is represented by its (row, col, spectral_value)
features = np.stack([x.ravel(), y.ravel(), band_image.ravel()], axis=1)

# Perform DBSCAN clustering on the augmented feature space
# eps: maximum distance between two samples for one to be considered as in the neighborhood of the other
# min_samples: minimum number of samples in a neighborhood for a point to be considered as a core point
dbscan = DBSCAN(eps=5, min_samples=5, n_jobs=-1)  # Adjust parameters as needed
dbscan_labels = dbscan.fit_predict(features)

# Reshape the clustering result back to the original band image shape
clustered_band_image = dbscan_labels.reshape(band_image.shape)

# Visualize the clustered band image
plt.figure(figsize=(10, 10))
plt.imshow(clustered_band_image, cmap='jet')
plt.title(f'DBSCAN Clustered Image - Band {band_index} (with Position)')
plt.axis('off')
plt.show()

# Identify and separate the main cluster
# Here, you can choose the cluster you are interested in based on visual inspection or other criteria
target_cluster = 1  # Example: assuming cluster 1 is the one you are interested in

# Create a mask for the target cluster
mask = clustered_band_image == target_cluster

# Optionally, perform morphological operations to refine the mask
refined_mask = morphology.opening(mask, morphology.disk(3))

# Visualize the separated cluster
plt.figure(figsize=(10, 10))
plt.imshow(refined_mask, cmap='gray')
plt.title(f'Separated Cluster - Band {band_index} (with Position)')
plt.axis('off')
plt.show()

# Optional: Apply the mask to the original image or perform further analysis
# For example, applying the mask to the original image across all bands:
separated_cluster = hsi_image * refined_mask[:, :, np.newaxis]
