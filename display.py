import spectral.io.envi as envi
import numpy as np
import matplotlib.pyplot as plt


def average_spectra(imageIN, top_left, bottom_right):
    # Extract the coordinates
    top_left_row, top_left_col = top_left
    bottom_right_row, bottom_right_col = bottom_right

    # Extract the region of spectra, including the bottom-right indices correctly
    region_spectra = imageIN[top_left_row:bottom_right_row + 1, top_left_col:bottom_right_col + 1, :]

    # Calculate the average spectra along the first two axes (rows and columns)
    avg_spectra = np.mean(region_spectra, axis=(0, 1))

    return avg_spectra

hdr = r'D:\Salmon_HSI_NP_15032023\SWIR_Hyspex\All_converted_file\S6-R-G1_SWIR_384_SN3151_9006us_2022-05-02T120753_raw_rad_float32.hdr'
#hdr = r'D:\Salmon_HSI_NP_15032023\Moving_Camera_Specim_swir\270522\scripted_S11-6.hdr'
img = envi.open(hdr)
image = img.load()

print(img.nrows)
print(img.ncols)

# List of points to plot (each point is a tuple of (row, col))
points = [
    (1400, 149), (1400, 150), (1400, 151),
    (1000, 149), (1000, 150), (1000, 151),
    (1200, 149), (1200, 150), (1200, 151),

    (1400, 249), (1400, 250), (1400, 251),
    (1800, 249), (1800, 250), (1800, 251),
    (1801, 249), (1801, 250), (1801, 251)
]

avg_spectrum = average_spectra(image, (1900, 150), (2000, 330))

# Retrieve the wavelengths from the header metadata
wavelengths = np.array(img.metadata['wavelength'], dtype=np.float32)

# Plot the spectra for each point
plt.figure(figsize=(10, 6))

for (row, col) in points:
    spectra = image[row, col, :].squeeze()  # Ensure it's a 1-dimensional array
    plt.plot(wavelengths, np.log10(1/(spectra/avg_spectrum)), label=f'Pixel ({row}, {col})')

#plt.plot(wavelengths, avg_spectrum, linestyle='dotted', label=f'average')

# Adding labels, title, and legend
plt.xlabel('Wavelength (nm)')
plt.ylabel('Reflectance')
plt.title('Spectra for Multiple Pixels')
#plt.legend()
plt.grid(True)

# Save the plot with high resolution
plt.savefig('spectra_plot_4k.png', dpi=1000)  # 300 dpi for high resolution
plt.show()
