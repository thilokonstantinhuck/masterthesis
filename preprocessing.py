import spectral.io.envi as envi
import functions as fnc
import numpy as np

# Load the image
hdr = r"D:\Salmon_HSI_NP_15032023\SWIR_Hyspex\All_converted_file\S6-R-G1_SWIR_384_SN3151_9006us_2022-05-02T120753_raw_rad_float32.hdr"
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
        processedSpectra = np.log10(avg_white / spectra)  # Process the spectra
        processed_image[row, column, :] = processedSpectra  # Store the processed spectra

# Save the processed image in ENVI format
output_hdr = "processed_image.hdr"
envi.save_image(output_hdr, processed_image, dtype=np.float32, interleave=img.metadata['interleave'],
                metadata=img.metadata, force=True)

print("Processed image saved successfully.")
