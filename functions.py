import numpy as np


def average_spectra(imageIN, smallXY, bigXY):
    # Extract the coordinates
    smallXY_row, smallXY_col = smallXY
    bigXY_row, bigXY_col = bigXY

    # Extract the region of spectra, including the bottom-right indices correctly
    region_spectra = imageIN[smallXY_row:bigXY_row + 1, smallXY_col:bigXY_col + 1, :]

    # Calculate the average spectra along the first two axes (rows and columns)
    avg_spectra = np.mean(region_spectra, axis=(0, 1))

    return avg_spectra
