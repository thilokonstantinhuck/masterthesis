import spectral.io.envi as envi
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread
import math


def areaPlotSpectra(samplename, area):
    # Load the image
    hdr = (f"./tempImages/processed_image_{samplename}_absorbance_EMSC"
           f".hdr")
    img = envi.open(hdr)
    image = img.load()

    # Load the binary mask
    binary_mask = imread(f"./masks/binary_mask_{samplename}_combined.png")

    # Retrieve the wavelengths from the header metadata
    wavelengths = np.array(img.metadata['wavelength'], dtype=np.float32)

    # Extract coordinates from whiteArea
    (y1, x1), (y2, x2) = area

    # Ensure coordinates are within image bounds
    height, width, bands = image.shape
    if x1 < 0 or x2 >= width or y1 < 0 or y2 >= height:
        print("One or more coordinates are out of bounds.")
        return

    count = 0  # Initialize a counter

    # Plot spectra for all pixels in the specified area
    plt.figure(figsize=(10, 6))
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            if binary_mask[y][x] == 1:
                if count % 100 == 0:  # Plot only every 100th spectrum
                    spectrum = image[y, x, :].squeeze()  # Extract the spectrum for each pixel (y, x)
                    plt.plot(wavelengths, spectrum, label=f"Pixel ({x}, {y})")
                count += 1  # Increment the counter

    # Label the plot
    plt.title(f'Spectra of every 100 Pixels in {samplename}')
    plt.xlabel('Wavelength [nm]')
    plt.ylabel('Intensity')
    plt.show()


def averagePlotAreas(samplename):
    # Load the image
    hdr = f"./tempImages/processed_image_{samplename}_absorbance_EMSC.hdr"
    img = envi.open(hdr)
    image = img.load()

    # Define the masks and their corresponding labels
    masks = [
        (f"./masks/binary_mask_partial_{samplename}_Tail.png", "Tail", "pink"),
        (f"./masks/binary_mask_partial_{samplename}_Norwegian_Quality_Cut1.png", "Norwegian Quality Cut 1", "blue"),
        (f"./masks/binary_mask_partial_{samplename}_Norwegian_Quality_Cut2.png", "Norwegian Quality Cut 2", "green"),
        (f"./masks/binary_mask_partial_{samplename}_Head.png", "Head", "purple"),
        (f"./masks/binary_mask_partial_{samplename}_Belly_Fat_Trimmed.png", "Belly Trimmed Visceral Fat", "orange"),
        (f"./masks/binary_mask_{samplename}_combined.png", "Whole Fish Masked", "red")
    ]

    # Retrieve the wavelengths from the header metadata
    wavelengths = np.array(img.metadata['wavelength'], dtype=np.float32)

    plt.figure(figsize=(12, 8))

    # Loop through each mask, calculate the average spectrum, and plot
    for mask in masks:
        mask_file = mask[0]
        mask_label = mask[1]
        mask_color = mask[2]
        # Load the binary mask
        binary_mask = imread(mask_file)

        # Initialize an array to accumulate the spectra
        accumulated_spectra = np.zeros(image.shape[2], dtype=np.float32)
        pixel_count = 0
        discarded_count = 0

        # Accumulate spectra for pixels within the binary mask
        for column in range(img.ncols):
            for row in range(img.nrows):
                # Check if the pixel is included in the binary mask
                if binary_mask[row, column] == 1:
                    spectra = image[row, column, :].squeeze()
                    if not any(math.isinf(x) for x in spectra):
                        accumulated_spectra += spectra
                        pixel_count += 1
                    else:
                        discarded_count += 1

        # print discarded and pixels
        print(f"Number of valid pixels: {pixel_count}")
        print(f"Number of discarded pixels: {discarded_count}")

        # Calculate the average spectrum
        average_spectrum = accumulated_spectra / pixel_count

        # Plot the average spectrum for this mask
        plt.plot(wavelengths, average_spectrum, label=mask_label, color=mask_color)

    # Adding labels, title, grid, and legend
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Absorbance')
    plt.title(f'Average Spectra for Different Regions Sample {samplename}')
    plt.grid(True)
    plt.ylim(0, 2.8)  # Set the upper y-limit manually
    plt.legend(loc='lower right')

    # Save the plot with high resolution
    plt.savefig(f"./plots/plot_{samplename}_all_regions_averages.png", dpi=1000)
    plt.show()
