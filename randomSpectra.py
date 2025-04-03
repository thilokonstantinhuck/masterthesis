import spectral.io.envi as envi
import numpy as np
import matplotlib.pyplot as plt

# Load the hyperspectral image
#hdr_path = r"C:\Users\thilohuc\PycharmProjects\masterthesis\tempImages\3_processed_image_S16_absorbance_EMSC.hdr"
hdr_path = r"C:\SALMONDATA\SWIR_Hyspex\130622\S16_SWIR_384_SN3151_9006us_2022-06-13T124638_raw.hdr"
img = envi.open(hdr_path)
image = img.load()

# Retrieve image dimensions
nrows, ncols, nbands = image.shape

# Retrieve the wavelengths from the header metadata
wavelengths = np.array(img.metadata['wavelength'], dtype=np.float32)


def get_random_spectra_from_box(start_row, start_col, box_size=100, sample_size=100):
    """
    Extracts random spectra from a defined 100x100 box starting from (start_row, start_col).
    """
    end_row = min(start_row + box_size, nrows)
    end_col = min(start_col + box_size, ncols)

    available_rows = np.arange(start_row, end_row)
    available_cols = np.arange(start_col, end_col)

    random_rows = np.random.choice(available_rows, sample_size, replace=True)
    random_cols = np.random.choice(available_cols, sample_size, replace=True)

    random_indices = np.column_stack((random_rows, random_cols))

    return np.array([image[row, col, :] for row, col in random_indices]).squeeze()


# Example usage
start_row, start_col = 550, 100  # Define top-left starting point of the 100x100 box
random_spectra = get_random_spectra_from_box(start_row, start_col)

# Plot the random spectra
plt.figure(figsize=(10, 6))
for spectrum in random_spectra:
    plt.plot(wavelengths, spectrum, alpha=0.5)

plt.xlabel("Wavelength (nm)")
plt.ylabel("Intensity")
plt.ylim(5000, 30000)
plt.title("100 Random Spectra from Hyperspectral Image")
plt.grid(True)
plt.show()
