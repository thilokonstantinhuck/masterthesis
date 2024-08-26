import spectral.io.envi as envi
import numpy as np
import matplotlib.pyplot as plt

# Load the hyperspectral image with absorption data
hdr = "processed_image_EMSC.hdr"
img = envi.open(hdr)
image = img.load()

# Settings
minRatio = 0.9  # Adjust according to the range in your data
maxRatio = 1.75  # Adjust according to the range in your data
wavelength1 = 1080
wavelength2 = 1460

# Retrieve the wavelengths from the header metadata
wavelengths = np.array(img.metadata['wavelength'], dtype=np.float32)

# Find the indices of the specified wavelengths
index1 = np.argmin(np.abs(wavelengths - wavelength1))
index2 = np.argmin(np.abs(wavelengths - wavelength2))

# Ensure the arrays are explicitly cast to the same type
index1_data = np.array(image[:, :, index1], dtype=np.float32)
index2_data = np.array(image[:, :, index2], dtype=np.float32)

# Calculate the ratio of absorbance at the two wavelengths for each pixel
ratio_image = np.divide(index2_data, index1_data)  # Use np.divide to calculate the ratio

# Ensure that ratio_image is 2D
ratio_image = np.squeeze(ratio_image)  # Remove any singleton dimensions

# Create a binary mask based on the minRatio and maxRatio
binary_mask = np.where((ratio_image >= minRatio) & (ratio_image <= maxRatio), 1, 0)

# Display the ratio image and the binary mask side by side
plt.figure(figsize=(10, 7))

# Plot the ratio image
plt.subplot(1, 2, 1)
plt.imshow(ratio_image, cmap='gist_heat', vmin=minRatio, vmax=maxRatio)
plt.title(f'Ratio Image (between {wavelength1}nm and {wavelength2}nm)')
plt.axis('off')

# Plot the binary mask
plt.subplot(1, 2, 2)
plt.imshow(binary_mask, cmap='gray')
plt.title(f'Binary Mask (Ratio between {minRatio} and {maxRatio})')
plt.axis('off')

# Show the plot
plt.savefig('emscMaskAnalysis.png', dpi=1000)
plt.show()

# Save the binary mask as a PNG file
plt.imsave("emsc_binary_mask.png", binary_mask, cmap='gray')
