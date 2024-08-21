import spectral.io.envi as envi
import numpy as np
import matplotlib.pyplot as plt
import functions as fnc

# Load the image
hdr = r"D:\Salmon_HSI_NP_15032023\SWIR_Hyspex\All_converted_file\S6-R-G1_SWIR_384_SN3151_9006us_2022-05-02T120753_raw_rad_float32.hdr"
img = envi.open(hdr)
image = img.load()

# Print image dimensions
print(f"Number of rows: {img.nrows}")
print(f"Number of columns: {img.ncols}")

# Calculate average spectra for reference
avg_white = fnc.average_spectra(image, (1900, 150), (2000, 330))
avg_background = fnc.average_spectra(image, (500, 100), (1600, 350))

# Retrieve the wavelengths from the header metadata
wavelengths = np.array(img.metadata['wavelength'], dtype=np.float32)
print(wavelengths)

# Plot the spectra for each pixel in the 100th column
plt.figure(figsize=(10, 6))

column = 100  # Specify the column to use
for row in range(img.nrows):
    spectra = image[row, column, :].squeeze()  # Get the spectra for each pixel in the column

    # Modify the spectra according to your needs
    plotSpectra = avg_white - spectra

    plt.plot(wavelengths, plotSpectra, color='blue', alpha=0.1)  # Use transparency to avoid over-plotting

# Plot the average white spectrum
plt.plot(wavelengths, avg_white, linestyle='dotted', color='red', linewidth=2, label='Average White')

# Adding vertical lines, labels, title, and legend
plt.axvline(x=1360, color='black', linestyle='--')
plt.axvline(x=1400, color='black', linestyle='--')
plt.axvline(x=1810, color='black', linestyle='--')

plt.xlabel('Wavelength (nm)')
plt.ylabel('Reflectance')
plt.title('Spectra for 100th Column')
plt.grid(True)
plt.legend()

# Set the y-axis minimum to 0
plt.ylim(bottom=0)

# Save the plot with high resolution
plt.savefig('spectra_plot_4k.png', dpi=1000)
plt.show()
