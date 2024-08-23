import spectral.io.envi as envi
import numpy as np
import functions as fnc
from scipy.optimize import least_squares
import matplotlib.pyplot as plt


def normalize_spectrum(spectrum):
    return (spectrum - np.mean(spectrum)) / np.std(spectrum)


def emsc_spectrum(observed_spectrum, reference_spectrum, degree=2):
    """
    Perform Extended Multiplicative Signal Correction (EMSC) on a single spectrum.
    """
    observed_spectrum = normalize_spectrum(observed_spectrum)
    reference_spectrum = normalize_spectrum(reference_spectrum)

    # Create the design matrix with polynomial terms
    X = np.vstack([reference_spectrum ** i for i in range(degree + 1)]).T

    def model_func(coeffs):
        return (observed_spectrum - np.dot(X, coeffs)).ravel()

    # Fit the model using least squares
    model = least_squares(model_func, np.ones(X.shape[1]))

    # Corrected spectrum
    corrected_spectrum = observed_spectrum - (np.dot(X, model.x)) + model.x[0]

    return corrected_spectrum
# Example of applying EMSC to a hyperspectral image
def apply_emsc(hyperspectral_image, reference_spectrum, degree=2):
    """
    Apply EMSC to each pixel in a hyperspectral image.

    Parameters:
    hyperspectral_image (np.array): Hyperspectral image (3D array with shape (rows, cols, wavelengths)).
    reference_spectrum (np.array): The reference spectrum.
    degree (int): Degree of polynomial for baseline correction (default is 2).

    Returns:
    np.array: The corrected hyperspectral image.
    """
    corrected_image = np.zeros_like(hyperspectral_image)

    for i in range(hyperspectral_image.shape[0]):
        for j in range(hyperspectral_image.shape[1]):
            corrected_image[i, j, :] = emsc_spectrum(hyperspectral_image[i, j, :], reference_spectrum, degree=degree)

    return corrected_image


# Example usage:
# Assuming you have a hyperspectral image and a reference spectrum
# hyperspectral_image = np.random.rand(100, 100, 200)  # Replace with your actual data
# reference_spectrum = np.mean(hyperspectral_image, axis=(0, 1))  # or any chosen reference

# corrected_image = apply_emsc(hyperspectral_image, reference_spectrum)
# Calculate average spectra for reference

# Load the hyperspectral image with absorption data
hdr = "processed_image.hdr"
img = envi.open(hdr)
image = img.load()

avg_white = fnc.average_spectra(image, (1900, 150), (2000, 330))

corrected_image = apply_emsc(image, avg_white)

# Retrieve the wavelengths from the header metadata
wavelengths = np.array(img.metadata['wavelength'], dtype=np.float32)

plt.figure(figsize=(12, 8))

column = 100

for row in range(corrected_image.shape[0]):
    plt.plot(wavelengths, corrected_image[row, column, :])

# Adding labels, title, grid, and legend
plt.xlabel('Wavelength (nm)')
plt.ylabel('Absorbance')
plt.title('EMSC corrected Spectra')
plt.grid(True)

# Set the y-axis minimum to 0
plt.ylim(bottom=0)

# Save the plot with high resolution
plt.savefig('EMSC.png', dpi=1000)
plt.show()