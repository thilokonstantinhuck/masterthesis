import spectral.io.envi as envi
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from matplotlib.image import imread

# Load the hyperspectral image
hdr = "tempImages/processed_image_S02_EMSC.hdr"
img = envi.open(hdr)
image = img.load()

# Load the binary mask
binary_mask = imread(f"masks/binary_mask_S02_combined.png")

# Convert the mask to a single channel if necessary (in case of RGB)
if binary_mask.ndim == 3:  # If the mask has multiple channels (e.g., RGB)
    binary_mask = binary_mask[:, :, 0]  # Use only one channel

# Ensure the mask is binary (0 or 1)
binary_mask = (binary_mask > 0).astype(np.uint8)

# Retrieve the wavelengths from the header metadata
wavelengths = np.array(img.metadata['wavelength'], dtype=np.float32)

# Select only the bands with wavelengths up to 1350 nm
# band_indices = np.where(wavelengths <= 1350)[0]
# image = image[:, :, band_indices]

# Print image dimensions
nrows, ncols, nbands = image.shape
print(f"Number of rows: {nrows}")
print(f"Number of columns: {ncols}")
print(f"Number of bands: {nbands}")

# Flatten the image to (nrows * ncols, nbands)
flat_image = image.reshape(-1, nbands)

# Flatten the binary mask and apply it to filter the pixels used in PCA
flat_mask = binary_mask.flatten()
flat_image_masked = flat_image[flat_mask == 1]

# Apply PCA only on the masked pixels
pca = PCA(n_components=3)
pca_result = pca.fit_transform(flat_image_masked)

# Get the explained variance for each component
explained_variance = pca.explained_variance_ratio_

# Initialize an empty array to store the first three PCA components for the entire image
pca_image = np.zeros((nrows * ncols, 3))

# Fill in the first three PCA components only for the masked pixels
pca_image[flat_mask == 1] = pca_result[:, :3]

# Reshape the PCA result to the original image dimensions
pca_image = pca_image.reshape((nrows, ncols, 3))

# Normalize each PCA component to the range [0, 255] for visualization
pca_image_normalized = np.zeros_like(pca_image)
for i in range(3):
    pca_image_normalized[..., i] = (pca_image[..., i] - np.min(pca_image[..., i])) / \
                                   (np.max(pca_image[..., i]) - np.min(pca_image[..., i])) * 255

pca_image_normalized = pca_image_normalized.astype(np.uint8)

# Plot each PCA component separately with the explained variance in the title
plt.figure(figsize=(18, 6))

for i in range(3):
    plt.subplot(1, 4, i + 1)
    plt.imshow(pca_image_normalized[..., i], cmap='gray')
    plt.title(f'PCA Component {i + 1}\nVariance Explained: {explained_variance[i] * 100:.2f}%')
    plt.axis('off')

# Display the RGB image using the first three PCA components
plt.subplot(1, 4, 4)
plt.imshow(pca_image_normalized)
plt.title('RGB Image from First Three PCA Components')
plt.axis('off')

plt.show()

# Save each PCA component as separate images and the combined RGB image
for i in range(3):
    plt.imsave(f'pca_component_{i + 1}.png', pca_image_normalized[..., i], cmap='gray')
plt.imsave('pca_rgb_image.png', pca_image_normalized)

print("PCA components and RGB image created and saved successfully.")
