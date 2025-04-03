import spectral.io.envi as envi
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# Load the hyperspectral image
hdr = "tempImages/1_processed_image_S16_absorbance_EMSC.hdr"
img = envi.open(hdr)
image = img.load()

# Print image dimensions
nrows, ncols, nbands = image.shape
print(f"Number of rows: {nrows}")
print(f"Number of columns: {ncols}")
print(f"Number of bands: {nbands}")

# Flatten the image to (nrows * ncols, nbands)
flat_image = image.reshape(-1, nbands)

# Apply PCA
pca = PCA(n_components=3)
pca_result = pca.fit_transform(flat_image)
explained_variance = pca.explained_variance_ratio_

# Extract the first PCA component
first_pca_component = pca_result[:, 0].reshape((nrows, ncols))

# Rotate the image
first_pca_component = np.rot90(first_pca_component, k=3)

# Plot the first PCA component
plt.figure(figsize=(8, 2.2))
plt.imshow(first_pca_component, cmap='inferno', vmin=-4, vmax=0.5)
#plt.colorbar(label='Intensity')
plt.title(f'First PCA Component, Variance Explained: {explained_variance[0] * 100:.2f}%')
plt.axis('off')
plt.tight_layout()  # Adjust layout to minimize borders
plt.show()

print(f"First PCA component explains {explained_variance[0] * 100:.2f}% of the variance.")
