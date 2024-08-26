import numpy as np
import spectral.io.envi as envi
from PIL import Image

# Settings
overlitDefinition = 0.75

# Load the image
hdr = r"D:\Salmon_HSI_NP_15032023\SWIR_Hyspex\All_converted_file\S6-R-G1_SWIR_384_SN3151_9006us_2022-05-02T120753_raw_rad_float32.hdr"
img = envi.open(hdr)
image = img.load()

# Create the mask
# If any channel in a pixel is above the overlitDefinition, the mask will be 0 (black), otherwise 1 (white)
mask = np.all(image <= overlitDefinition, axis=-1).astype(np.uint8) * 255

# Convert the mask to an image and save as PNG
mask_image = Image.fromarray(mask)
mask_image.save("maskOverlit.png")

print("Processed mask saved successfully.")

# Initialize an array to hold the processed spectra
processed_image = np.copy(image)  # Start with a copy of the original image
nrows, ncols, nbands = image.shape

# Process the spectra
for column in range(ncols):
    for row in range(nrows):
        # Check if any channel in this pixel exceeds the overlitDefinition
        if np.any(image[row, column, :] > overlitDefinition):
            # Set all channels for this pixel to 1
            processed_image[row, column, :] = 1.0

# Save the processed image in ENVI format
output_hdr = "processed_image_overlit.hdr"
envi.save_image(output_hdr, processed_image, dtype=np.float32, interleave=img.metadata['interleave'],
                metadata=img.metadata, force=True)

print("Processed image saved successfully.")
