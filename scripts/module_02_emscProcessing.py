import spectral.io.envi as envi
import numpy as np
from biospectools import EMSC
from config.whiteReference import whiteReference


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