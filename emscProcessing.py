import spectral.io.envi as envi
import numpy as np
import functions as fnc
from biospectools import EMSC
import matplotlib.pyplot as plt

# Load the hyperspectral image with absorption data
hdr = "processed_image_overlit.hdr"
img = envi.open(hdr)
image = img.load()

avg_white = fnc.average_spectra(image, (1900, 150), (2000, 330))
avg_background = fnc.average_spectra(image, (500, 100), (1600, 350))

# Retrieve the wavelengths from the header metadata
wavelengths = np.array(img.metadata['wavelength'], dtype=np.float32)

emscTransformer = EMSC(avg_white, wavelengths)

correctedSpectra = emscTransformer.transform(image)

# Save the processed image in ENVI format
output_hdr = "processed_image_EMSC.hdr"
envi.save_image(output_hdr, correctedSpectra, dtype=np.float32, interleave=img.metadata['interleave'],
                metadata=img.metadata, force=True)

print("Processed image saved successfully.")

# plt.figure(figsize=(12, 8))
#
# column = 100
#
# for row in range(correctedSpectra.shape[0]):
#     plt.plot(wavelengths, correctedSpectra[row, column, :])
#
# # Adding labels, title, grid, and legend
# plt.xlabel('Wavelength (nm)')
# plt.ylabel('Intensity')
# plt.title('EMSC corrected Spectra')
# plt.grid(True)
#
# # Save the plot with high resolution
# plt.savefig('EMSC.png', dpi=1000)
# plt.show()
#
# for row in range(image.shape[0]):
#     plt.plot(wavelengths, image[row, column, :].squeeze())
#
# # Adding labels, title, grid, and legend
# plt.xlabel('Wavelength (nm)')
# plt.ylabel('Intensity')
# plt.title('plain Spectra')
# plt.grid(True)
#
#
#
# # Save the plot with high resolution
# plt.savefig('plainSpectra.png', dpi=1000)
# plt.show()