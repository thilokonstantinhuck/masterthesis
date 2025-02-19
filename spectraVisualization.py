import spectral.io.envi as envi
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# Load the hyperspectral image
hdr_path = r"C:\Users\thilohuc\PycharmProjects\masterthesis\tempImages\1_processed_image_S06_absorbance_EMSC.hdr"
img = envi.open(hdr_path)
image = img.load()

# Retrieve image dimensions
nrows, ncols, nbands = image.shape

# Retrieve the wavelengths from the header metadata
wavelengths = np.array(img.metadata['wavelength'], dtype=np.float32)

# Reshape the image for PCA (flatten spatial dimensions)
reshaped_image = image.reshape(-1, nbands)

# Apply PCA to reduce dimensions to 3 components
pca = PCA(n_components=3)
principal_components = pca.fit_transform(reshaped_image)

# Reshape back to original spatial dimensions
pca_component1 = principal_components[:, 0].reshape(nrows, ncols)

# Manually define min/max limits for component 1 visualization
min_value = 0
max_value = 3

# Define two points to highlight
point1 = (710, 240)  # (row, column)
point2 = (750, 245)  # (row, column)

# Extract the spectra for both points
spectra_point1 = image[point1[0], point1[1], :].squeeze()
spectra_point2 = image[point2[0], point2[1], :].squeeze()

# Create a figure with subplots
fig, ax = plt.subplots(1, 2, figsize=(8, 8))

# Display the PCA component 1 image with inferno colormap
cmap = ax[0].imshow(pca_component1, cmap='inferno', vmin=min_value, vmax=max_value)
ax[0].scatter([point1[1]], [point1[0]], color='red', marker='o', s=50, label="Point 1 (Red)")
ax[0].scatter([point2[1]], [point2[0]], color='blue', marker='o', s=50, label="Point 2 (Blue)")
ax[0].set_title("PCA Component 1 (Inferno Colormap)")
ax[0].legend()
ax[0].axis("off")

# Plot the spectra for both points in the same plot
ax[1].plot(wavelengths, spectra_point1, color='red', label=f"Normal Spectra at {point1}")
ax[1].plot(wavelengths, spectra_point2, color='blue', label=f"Droplet 1 at {point2}")
ax[1].set_xlabel("Wavelength (nm)")
ax[1].set_ylabel("Absorbance")
ax[1].set_title("Normal Absorbance vs Droplet")
ax[1].legend()
ax[1].grid(True)

plt.tight_layout()
plt.show()
