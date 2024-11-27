import spectral.io.envi as envi
import functions as fnc
import numpy as np
import matplotlib.pyplot as plt

# Load the image
hdr = r"C:\Users\thilohuc\OneDrive - Norwegian University of Life Sciences\Desktop\salmonMeasurements\s1_l_g1_SWIR_384_SN3151_2600us_2024-11-26T093313_raw_rad_float32.hdr"
img = envi.open(hdr)
image = img.load()

# Print image dimensions
nrows, ncols, nbands = image.shape
print(f"Number of rows: {nrows}")
print(f"Number of columns: {ncols}")
print(f"Number of bands: {nbands}")

# Calculate average spectra for reference
avg_white = fnc.average_spectra(image, (1900, 150), (2000, 330))
avg_background = fnc.average_spectra(image, (500, 100), (1600, 350))

# Initialize an array to hold the processed spectra
processed_image = np.zeros_like(image)

# Process the spectra
for column in range(ncols):
    for row in range(nrows):
        spectra = image[row, column, :].squeeze()  # Get the spectra for each pixel in the column
        processedSpectra = -np.log10(spectra / avg_white)  # Process the spectra
        processed_image[row, column, :] = processedSpectra  # Store the processed spectra

# Save the processed image in ENVI format
output_hdr = "processed_image_lab_test.hdr"
envi.save_image(output_hdr, processed_image, dtype=np.float32, interleave=img.metadata['interleave'],
                metadata=img.metadata, force=True)

print("Processed image saved successfully.")

# Load the processed image
hdrAbsorbance = "processed_image_lab_test.hdr"
imgAbsorbance = envi.open(hdrAbsorbance)
imageAbsorbance = imgAbsorbance.load()

# Retrieve the wavelengths from the header metadata
wavelengths = np.array(img.metadata['wavelength'], dtype=np.float32)

# Define a point (e.g., last row and last column)
point_row = 200
point_column = 200

# Extract the spectra for the defined point
spectra_at_point = imageAbsorbance[point_row, point_column, :]

# Plot the spectra for the selected point
plt.figure(figsize=(10, 6))
plt.plot(wavelengths, spectra_at_point, label=f"Spectra at point ({point_row}, {point_column})")
plt.xlabel("Wavelength (nm)")
plt.ylabel("Absorbance")
plt.title("Spectra of the Selected Pixel in the Hyperspectral Image")
plt.legend()
plt.grid(True)
plt.show()
