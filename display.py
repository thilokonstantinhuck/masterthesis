import spectral.io.envi as envi
import numpy as np
import matplotlib.pyplot as plt
import functions as fnc

hdr = r"D:\Salmon_HSI_NP_15032023\SWIR_Hyspex\All_converted_file\S6-R-G1_SWIR_384_SN3151_9006us_2022-05-02T120753_raw_rad_float32.hdr"
# hdr = r'D:\Salmon_HSI_NP_15032023\Moving_Camera_Specim_swir\270522\scripted_S11-6.hdr'
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

avg_white = fnc.average_spectra(image, (1900, 150), (2000, 330))
avg_background = fnc.average_spectra(image, (500, 100), (1600, 350))

# Retrieve the wavelengths from the header metadata
wavelengths = np.array(img.metadata['wavelength'], dtype=np.float32)

# Plot the spectra for each point
plt.figure(figsize=(10, 6))


for (row, col) in points:
    spectra = image[row, col, :].squeeze()  # Ensure it's a 1-dimensional array

    # plotSpectra = np.log10(1 / (spectra / avg_white))
    # plotSpectra = np.log10(1 / (spectra / avg_background))
    # plotSpectra = spectra / avg_white
    # plotSpectra = spectra / avg_background
    plotSpectra = avg_white - spectra

    plt.plot(wavelengths, plotSpectra, label=f'Pixel ({row}, {col})')

plt.plot(wavelengths, avg_white, linestyle='dotted', label=f'average')
plt.axvline(x=1360)
plt.axvline(x=1400)
plt.axvline(x=1810)
# Adding labels, title, and legend
plt.xlabel('Wavelength (nm)')
plt.ylabel('reflectance')
plt.title('(white-spectra) and white')
# plt.legend()
plt.grid(True)

# Save the plot with high resolution
plt.savefig('spectra_plot_4k.png', dpi=1000)
plt.show()
