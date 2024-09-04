import numpy as np
import spectral.io.envi as envi
from PIL import Image
from config.generalParameters import overlitDefinition
from config.whiteReference import whiteReference

def average_spectra(imageIN, coordinates):
    # Extract the coordinates
    smallXY_row, smallXY_col = coordinates[0]
    bigXY_row, bigXY_col = coordinates[1]

    # Extract the region of spectra, including the bottom-right indices correctly
    region_spectra = imageIN[smallXY_row:bigXY_row + 1, smallXY_col:bigXY_col + 1, :]

    # Calculate the average spectra along the first two axes (rows and columns)
    avg_spectra = np.mean(region_spectra, axis=(0, 1))

    return avg_spectra

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

def absorbanceHDRcreation(imageFilePath, samplename):
    # Load the image
    img = envi.open(imageFilePath)
    image = img.load()

    # Initialize an array to hold the processed spectra
    processed_image = np.zeros_like(image)
    nrows, ncols, nbands = image.shape

    # Process the spectra
    for column in range(ncols):
        for row in range(nrows):
            spectra = image[row, column, :].squeeze()  # Get the spectra for each pixel in the column
            processedSpectra = -np.log10(spectra / whiteReference)  # Process the spectra
            processedSpectra[np.isinf(processedSpectra)] = 5 # Replace inf values with 5
            processed_image[row, column, :] = processedSpectra  # Store the processed spectra

    # Save the processed image in ENVI format
    output_hdr = f"./tempImages/processed_image_{samplename}_absorbance.hdr"
    envi.save_image(output_hdr, processed_image, dtype=np.float32, interleave=img.metadata['interleave'],
                    metadata=img.metadata, force=True)

    print(f"Absorbance image {samplename} saved successfully.")