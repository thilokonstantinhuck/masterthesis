import numpy as np
import spectral.io.envi as envi
from PIL import Image
from config.generalParameters import overlitDefinition

def overlit(imageFilePath, samplename):
    # Load the image
    img = envi.open(imageFilePath)
    image = img.load()

    # Create the mask
    # If any channel in a pixel is above the overlitDefinition, the mask will be 0 (black), otherwise 1 (white)
    mask = np.all(image <= overlitDefinition, axis=-1).astype(np.uint8) * 255

    # Convert the mask to an image and save as PNG
    mask_image = Image.fromarray(mask)
    mask_image.save(f"./masks/binary_mask_{samplename}_overlit.png")

    print(f"Overlit mask {samplename} saved successfully.")

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
    output_hdr = f"./tempImages/processed_image_{samplename}_overlit.hdr"
    envi.save_image(output_hdr, processed_image, dtype=np.float32, interleave=img.metadata['interleave'],
                    metadata=img.metadata, force=True)

    print(f"Overlit processed image {samplename} saved successfully.")
