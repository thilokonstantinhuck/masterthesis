import spectral.io.envi as envi
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread

# Load the image
hdr = "processed_image.hdr"
img = envi.open(hdr)
image = img.load()

# Define the masks and their corresponding labels
masks = {
    "Tail_mask.png": "Tail",
    "Norwegian_Quality_Cut1_mask.png": "Norwegian Quality Cut 1",
    "Norwegian_Quality_Cut2_mask.png": "Norwegian Quality Cut 2",
    "Head_mask.png": "Head",
    "Belly_Fat_Trimmed_mask.png": "Belly with Trimmed Visceral Fat",
    "final_combined_binary_mask.png": "Whole Fish Masked"
}

# Retrieve the wavelengths from the header metadata
wavelengths = np.array(img.metadata['wavelength'], dtype=np.float32)

plt.figure(figsize=(12, 8))

# Loop through each mask, calculate the average spectrum, and plot
for mask_file, label in masks.items():
    # Load the binary mask
    binary_mask = imread(mask_file)

    # If binary_mask has multiple channels (e.g., RGB), reduce it to a single channel
    if binary_mask.ndim == 3:
        binary_mask = np.mean(binary_mask, axis=2)  # Convert to grayscale by averaging the channels

    # Ensure that the mask dimensions match the image dimensions
    if binary_mask.shape != (img.nrows, img.ncols):
        raise ValueError(f"The binary mask dimensions for {label} do not match the image dimensions.")

    # Initialize an array to accumulate the spectra
    accumulated_spectra = np.zeros(image.shape[2], dtype=np.float32)
    pixel_count = 0

    # Accumulate spectra for pixels within the binary mask
    for column in range(img.ncols):
        for row in range(img.nrows):
            # Check if the pixel is included in the binary mask
            if binary_mask[row, column] == 1:
                spectra = image[row, column, :].squeeze()
                accumulated_spectra += spectra
                pixel_count += 1

    # Calculate the average spectrum
    average_spectrum = accumulated_spectra / pixel_count

    # Plot the average spectrum for this mask
    plt.plot(wavelengths, average_spectrum, label=label)

# Adding labels, title, grid, and legend
plt.xlabel('Wavelength (nm)')
plt.ylabel('Absorbance')
plt.title('Average Spectra for Different Regions')
plt.grid(True)
plt.legend()

# Set the y-axis minimum to 0
plt.ylim(bottom=0)

# Save the plot with high resolution
plt.savefig('average_spectra_all_regions.png', dpi=1000)
plt.show()
