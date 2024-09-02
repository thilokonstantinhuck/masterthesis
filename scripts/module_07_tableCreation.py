import spectral.io.envi as envi
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread
import math
import pandas as pd

def exportDataFrame():
    samples = ["S01", "S02", "S03", "S05", "S06", "S07"]

    dfList = []

    for image in samples:
        dfList.append(createDataFrame(image))

    # Concatenate all DataFrames into one
    final_df = pd.concat(dfList, ignore_index=True)

    # Print the final DataFrame
    print(final_df)

def createDataFrame(samplename):
    # Load the image
    hdr = f"./tempImages/processed_image_{samplename}_absorbance.hdr"
    img = envi.open(hdr)
    image = img.load()


    # Retrieve the wavelengths from the header metadata
    wavelengths = np.array(img.metadata['wavelength'], dtype=np.float32)

    rows = []


    # Define the masks and their corresponding labels
    masks = {
        f"./masks/binary_mask_partial_{samplename}_Tail.png": "T",
        f"./masks/binary_mask_partial_{samplename}_Norwegian_Quality_Cut1.png": "NQC1",
        f"./masks/binary_mask_partial_{samplename}_Norwegian_Quality_Cut2.png": "NQC2",
        f"./masks/binary_mask_partial_{samplename}_Head.png": "H",
        f"./masks/binary_mask_partial_{samplename}_Belly_Fat_Trimmed.png": "F2"
    }

    # Loop through each mask, calculate the average spectrum, and save in table
    for mask_file, label in masks.items():
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

        # Append the new row to the existing DataFrame
        data = [samplename, label] + average_spectrum.tolist()
        rows.append(data)
        # new_row_df = pd.DataFrame([data], columns=columns)
        # df = pd.concat([df, new_row_df], ignore_index=True)

    # Convert the wavelengths array to a list
    wavelengths_list = wavelengths.tolist()

    # Create empty dataframe
    columns = ["Fish ID", "Position"] + wavelengths_list
    df = pd.DataFrame(rows, columns = columns)

    return df