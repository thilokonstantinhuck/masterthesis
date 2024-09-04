import spectral.io.envi as envi
import numpy as np
from biospectools import EMSC
from config.whiteReference import whiteReference
from config.bioReference import bioReference


# def average_spectra(imageIN, coordinates):
#     # Extract the coordinates
#     smallXY_row, smallXY_col = coordinates[0]
#     bigXY_row, bigXY_col = coordinates[1]
#
#     # Extract the region of spectra, including the bottom-right indices correctly
#     region_spectra = imageIN[smallXY_row:bigXY_row + 1, smallXY_col:bigXY_col + 1, :]
#
#     # Calculate the average spectra along the first two axes (rows and columns)
#     avg_spectra = np.mean(region_spectra, axis=(0, 1))
#
#     return avg_spectra

def emscHDRcreation(samplename):
    # Load the hyperspectral image with absorption data
    hdr = f".\\tempImages\\processed_image_{samplename}_overlit.hdr"
    img = envi.open(hdr)
    image = img.load()

    # Retrieve the wavelengths from the header metadata
    wavelengths = np.array(img.metadata['wavelength'], dtype=np.float32)

    emscTransformer = EMSC(whiteReference, wavelengths)

    correctedSpectra = emscTransformer.transform(image)

    # Save the processed image in ENVI format
    output_hdr = f".\\tempImages\\processed_image_{samplename}_EMSC.hdr"
    envi.save_image(output_hdr, correctedSpectra, dtype=np.float32, interleave=img.metadata['interleave'],
                    metadata=img.metadata, force=True)

    print(f"EMSC image {samplename} saved successfully.")

def emscAbsorbanceHDRcreation(samplename):
    # Load the hyperspectral image with absorption data
    hdr = f".\\tempImages\\processed_image_{samplename}_absorbance.hdr"
    img = envi.open(hdr)
    image = img.load()

    # Retrieve the wavelengths from the header metadata
    wavelengths = np.array(img.metadata['wavelength'], dtype=np.float32)

    emscTransformer = EMSC(bioReference, wavelengths)

    correctedSpectra = emscTransformer.transform(image)

    # Save the processed image in ENVI format
    output_hdr = f".\\tempImages\\processed_image_{samplename}_absorbance_EMSC.hdr"
    envi.save_image(output_hdr, correctedSpectra, dtype=np.float32, interleave=img.metadata['interleave'],
                    metadata=img.metadata, force=True)

    print(f"EMSC absorbance image {samplename} saved successfully.")

def oneShotHDRcreation(originalFile, samplename):
    # Load the hyperspectral image with absorption data
    img = envi.open(originalFile)
    image = img.load()

    # Initialize an array to hold the processed absorbance spectra
    processed_absorbance_image = np.zeros_like(image)
    nrows, ncols, nbands = image.shape

    # Process the spectra
    for column in range(ncols):
        for row in range(nrows):
            spectra = image[row, column, :].squeeze()  # Get the spectra for each pixel in the column
            processedSpectra = -np.log10(spectra / whiteReference)  # Process the spectra
            processedSpectra[np.isinf(processedSpectra)] = 5 # Replace inf values with 5
            processed_absorbance_image[row, column, :] = processedSpectra  # Store the processed spectra

    # Retrieve the wavelengths from the header metadata
    wavelengths = np.array(img.metadata['wavelength'], dtype=np.float32)

    emscTransformer = EMSC(bioReference, wavelengths)

    correctedSpectra = emscTransformer.transform(processed_absorbance_image)

    # Save the processed image in ENVI format
    output_hdr = f".\\tempImages\\processed_image_{samplename}_absorbance_EMSC_OS.hdr"
    envi.save_image(output_hdr, correctedSpectra, dtype=np.float32, interleave=img.metadata['interleave'],
                    metadata=img.metadata, force=True)

    print(f"EMSC absorbance Oneshot image {samplename} saved successfully.")