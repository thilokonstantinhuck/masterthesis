import spectral.io.envi as envi
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread


# def whiteAreaPlotSpectra(samplename, whiteArea):
#     # Load the image
#     hdr = f"./tempImages/processed_image_{samplename}_overlit.hdr"
#     img = envi.open(hdr)
#     image = img.load()
#
#     # Retrieve the wavelengths from the header metadata
#     wavelengths = np.array(img.metadata['wavelength'], dtype=np.float32)
#
#     # Extract coordinates from whiteArea
#     (y1, x1), (y2, x2) = whiteArea
#
#     # Ensure coordinates are within image bounds
#     height, width, bands = image.shape
#     if x1 < 0 or x2 >= width or y1 < 0 or y2 >= height:
#         print("One or more coordinates are out of bounds.")
#         return
#
#     count = 0  # Initialize a counter
#
#     # Plot spectra for all pixels in the specified area
#     plt.figure(figsize=(10, 6))
#     for x in range(x1, x2 + 1):
#         for y in range(y1, y2 + 1):
#             if count % 100 == 0:  # Plot only every 100th spectrum
#                 spectrum = image[y, x, :].squeeze()  # Extract the spectrum for each pixel (y, x)
#                 plt.plot(wavelengths, spectrum, label=f"Pixel ({x}, {y})")
#             count += 1  # Increment the counter
#
#     # Label the plot
#     plt.title(f'Spectra of white Pixels in {samplename}')
#     plt.xlabel('Wavelength [nm]')
#     plt.ylabel('Intensity')
#     plt.show()


def averagePlotAreas(samplename):
    # Load the image
    hdr = f"./tempImages/processed_image_{samplename}_absorbance.hdr"
    img = envi.open(hdr)
    image = img.load()

    # Define the masks and their corresponding labels
    masks = {
        f"./masks/binary_mask_partial_{samplename}_Tail.png": "Tail",
        f"./masks/binary_mask_partial_{samplename}_Norwegian_Quality_Cut1.png": "Norwegian Quality Cut 1",
        f"./masks/binary_mask_partial_{samplename}_Norwegian_Quality_Cut2.png": "Norwegian Quality Cut 2",
        f"./masks/binary_mask_partial_{samplename}_Head.png": "Head",
        f"./masks/binary_mask_partial_{samplename}_Belly_Fat_Trimmed.png": "Belly with Trimmed Visceral Fat",
        f"./masks/binary_mask_{samplename}_combined.png": "Whole Fish Masked"
    }

    # Retrieve the wavelengths from the header metadata
    wavelengths = np.array(img.metadata['wavelength'], dtype=np.float32)

    plt.figure(figsize=(12, 8))

    # Loop through each mask, calculate the average spectrum, and plot
    for mask_file, label in masks.items():
        # Load the binary mask
        binary_mask = imread(mask_file)

        # Ensure that the mask dimensions match the image dimensions
        if binary_mask.shape != (img.nrows, img.ncols):
            raise ValueError(f"The binary mask dimensions for {label} do not match the image dimensions.")

        # Initialize an array to accumulate the spectra
        accumulated_spectra = np.zeros(image.shape[2], dtype=np.float32)
        pixel_count = 0

        # Accumulate spectra for pixels within the binary mask
        for column in range(img.ncols):
            for row in range(img.nrows):
                # Check if the pixel is included in the binary mask
                if binary_mask[row, column] == 1:
                    spectra = image[row, column, :].squeeze()
                    accumulated_spectra += spectra
                    pixel_count += 1

        # Calculate the average spectrum
        average_spectrum = accumulated_spectra / pixel_count

        # Plot the average spectrum for this mask
        plt.plot(wavelengths, average_spectrum, label=label)

    # Adding labels, title, grid, and legend
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Absorbance')
    plt.title(f'Average Spectra for Different Regions Sample {samplename}')
    plt.grid(True)
    plt.legend()

    # Set the y-axis minimum to 0
    # plt.ylim(bottom=0)

    # Save the plot with high resolution
    plt.savefig(f"./plots/plot_{samplename}_all_regions_averages.png", dpi=1000)
    plt.show()
