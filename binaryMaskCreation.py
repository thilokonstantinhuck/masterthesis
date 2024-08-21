from matplotlib.image import imread, imsave
import numpy as np
import matplotlib.pyplot as plt

# Settings
threshold_value = 0.7  # Threshold value to exclude pixels

# Load the grayscale mask
maskThreshold = imread("grayscale_absorption_mask.png")

# If maskThreshold has multiple channels (e.g., RGB), reduce it to a single channel
if maskThreshold.ndim == 3:
    maskThreshold = np.mean(maskThreshold, axis=2)  # Convert to grayscale by averaging the channels

# Create the binary mask by applying the threshold
binary_mask = (maskThreshold >= threshold_value).astype(np.uint8)

# Display the binary mask
plt.figure(figsize=(10, 10))
plt.imshow(binary_mask, cmap='gray')
plt.title(f'Binary Mask (Threshold = {threshold_value})')
plt.axis('off')
plt.show()

# Save the binary mask as a PNG image
imsave('binary_mask.png', binary_mask, cmap='gray')

print("Binary mask created and saved successfully.")
