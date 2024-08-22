import spectral.io.envi as envi
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread

# Settings
minRatio = 5
maxRatio = 8
wavelength1 = 1080
wavelength2 = 1460

# Load the image
hdr = "processed_image.hdr"
img = envi.open(hdr)
image = img.load()

# Load the binary mask
binary_mask = imread("binary_mask.png")

# If binary_mask has multiple channels (e.g., RGB), reduce it to a single channel
if binary_mask.ndim == 3:
    binary_mask = np.mean(binary_mask, axis=2)  # Convert to grayscale by averaging the channels

# Retrieve the wavelengths from the header metadata
wavelengths = np.array(img.metadata['wavelength'], dtype=np.float32)

# Find the indices of the specified wavelengths
index1 = np.argmin(np.abs(wavelengths - wavelength1))
index2 = np.argmin(np.abs(wavelengths - wavelength2))
print(wavelengths[index1], wavelengths[index2])
print(image[500,100,index2] / image[500,100,index1])

# Ensure the arrays are explicitly cast to the same type
index1_data = np.array(image[:, :, index1], dtype=np.float32)
index2_data = np.array(image[:, :, index2], dtype=np.float32)

# Calculate the ratio of absorbance at the two wavelengths for each pixel
ratio_image = np.divide(index2_data, index1_data + 1e-10)  # Use np.divide to calculate the ratio

# Ensure that ratio_image is 2D
ratio_image = np.squeeze(ratio_image)  # Remove any singleton dimensions

# Create a new mask based on the ratio criteria
ratio_mask = ((ratio_image >= minRatio) & (ratio_image <= maxRatio)).astype(np.uint8)

# Combine the ratio mask with the existing binary mask
combined_mask = binary_mask * ratio_mask  # Element-wise multiplication

# Optionally, save or display the new combined mask
plt.figure(figsize=(10, 10))
plt.imshow(combined_mask, cmap='gray')
plt.title(f'Combined Mask (Ratio between {minRatio} and {maxRatio})')
plt.axis('off')
plt.show()

# Save the combined mask as a new binary mask image
plt.imsave('combined_binary_mask.png', combined_mask, cmap='gray')

print("Combined mask created and saved successfully.")

# Additional check to ensure the mask is binary (0 or 1)
combined_mask[combined_mask != 1] = 0

# Optionally, save or display the new combined mask
plt.figure(figsize=(10, 10))
plt.imshow(combined_mask, cmap='gray')
plt.title(f'Final Combined Mask (Ratio between {minRatio} and {maxRatio})')
plt.axis('off')
plt.show()

# Save the final combined mask as a new binary mask image
plt.imsave('final_combined_binary_mask.png', combined_mask, cmap='gray')

print("Final combined mask created and saved successfully.")
