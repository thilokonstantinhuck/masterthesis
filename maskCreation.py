import spectral.io.envi as envi
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imsave

# Load the hyperspectral image with absorption data
hdr = "processed_image.hdr"
img = envi.open(hdr)
image = img.load()

# Retrieve the wavelengths from the header metadata
wavelengths = np.array(img.metadata['wavelength'], dtype=np.float32)

# Select only the bands with wavelengths up to 1350 nm
band_indices = np.where(wavelengths <= 1350)[0]
image_filtered = image[:, :, band_indices]

# Calculate the average absorption across the selected band for each pixel
average_absorption = np.mean(image_filtered, axis=2)

# Normalize the average absorption to the range [0, 255] for creating a grayscale image
average_absorption_normalized = (average_absorption - np.min(average_absorption)) / \
                                (np.max(average_absorption) - np.min(average_absorption)) * 255
average_absorption_normalized = average_absorption_normalized.astype(np.uint8)

# Plot the grayscale mask
plt.figure(figsize=(10, 10))
plt.imshow(average_absorption_normalized, cmap='gray')
plt.title('Grayscale Mask (Average Absorption up to 1350 nm)')
plt.axis('off')
plt.show()

# Save the grayscale mask as a PNG image
imsave('grayscale_absorption_mask.png', average_absorption_normalized, cmap='gray')

print("Grayscale absorption mask saved successfully.")
