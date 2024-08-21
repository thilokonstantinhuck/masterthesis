import spectral.io.envi as envi
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread

# Load the image
hdr = "processed_image.hdr"
img = envi.open(hdr)
image = img.load()

# Load the binary mask
binary_mask = imread("final_combined_binary_mask.png")

# If binary_mask has multiple channels (e.g., RGB), reduce it to a single channel
if binary_mask.ndim == 3:
    binary_mask = np.mean(binary_mask, axis=2)  # Convert to grayscale by averaging the channels

plt.figure(figsize=(10, 10))
plt.imshow(binary_mask, cmap='gray')
plt.title(f'Binary Mask')
plt.axis('off')
plt.show()

# Ensure that the mask dimensions match the image dimensions
if binary_mask.shape != (img.nrows, img.ncols):
    raise ValueError("The binary mask dimensions do not match the image dimensions.")

# Print image dimensions
print(f"Number of rows: {img.nrows}")
print(f"Number of columns: {img.ncols}")

# Retrieve the wavelengths from the header metadata
wavelengths = np.array(img.metadata['wavelength'], dtype=np.float32)

# Plot the spectra for each pixel in the 100th column, excluding those that are masked out (binary mask = 0)
plt.figure(figsize=(10, 6))

column = 100  # Specify the column to use

for row in range(img.nrows):
    # Check if the pixel is included in the binary mask
    if binary_mask[row, column] == 1:
        spectra = image[row, column, :].squeeze()  # Get the spectra for each pixel in the column
        plt.plot(wavelengths, spectra, color='blue', alpha=0.1)  # Use transparency to avoid over-plotting

# Adding labels, title, and legend
plt.xlabel('Wavelength (nm)')
plt.ylabel('Absorbance')
plt.title(f'Spectra for 100th Column (Filtered by Binary Mask)')
plt.grid(True)

# Set the y-axis minimum to 0
plt.ylim(bottom=0)

# Save the plot with high resolution
plt.savefig('spectra_plot_filtered_4k.png', dpi=1000)
plt.show()
