import spectral.io.envi as envi
import numpy as np
import matplotlib.pyplot as plt
from fontTools.misc.textTools import tostr
from matplotlib.image import imread
import math
import pandas as pd

def exportDataFrame():
    # List of sample names
    samples = ["S01", "S02", "S03", "S04", "S05", "S06"]

    dfList = []

    for image in samples:
        dfList.append(createDataFrameAutomatic(image))

    # Concatenate all DataFrames into one
    final_df = pd.concat(dfList, ignore_index=True)

    # Export the final DataFrame to a CSV file
    final_df.to_csv(f'./data/median_exported_data.csv', index=False)

    print("Data exported successfully to exported_data.csv")


def createDataFrameAutomatic(samplename):
    # Load the image
    hdr = f"./tempImages/processed_image_{samplename}_absorbance_EMSC.hdr"
    img = envi.open(hdr)
    image = img.load()

    # Load the CSV file
    file_path = './data/data_GC.csv'
    gc_data = pd.read_csv(file_path)

    # create new dataframe that has medians of the data
    grouped_df = gc_data.groupby(['Fish ID', 'Position']).median(numeric_only=True).reset_index()
    gc_data = grouped_df[grouped_df['Fish ID'] == samplename]
    print(grouped_df)

    # Retrieve the wavelengths from the header metadata
    wavelengths = np.array(img.metadata['wavelength'], dtype=np.float32)

    # mask path and lists
    maskPath = f"./masks/binary_mask_partial"
    positions = ["H","T","F2","NQC1","NQC2"]

    rows = []

    # Loop through each mask, calculate the average spectrum, and save in table
    for pos in positions:
        print(f"({pos})({samplename})")
        for fineMask in range(25):
            # Load the binary mask
            maskPathFull = maskPath + "_" + samplename + "_" + pos + "_" + str(fineMask) + ".png"
            binary_mask = imread(maskPathFull)

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
            # print(f"({pos})({fineMask}): Number of valid/discarded pixels: {pixel_count} / {discarded_count}")


            # Calculate the average spectrum
            average_spectrum = accumulated_spectra / pixel_count

            idString = f"{samplename}_{pos}"
            data = [f"{fineMask}"] + gc_data[gc_data["Position"] == pos].iloc[0].tolist() + average_spectrum.tolist()
            rows.append(data)


    # Convert the wavelengths array to a list
    wavelengths_list = wavelengths.tolist()

    # Create empty dataframe
    headers = gc_data.columns.tolist()
    columns = ["FineMask"] + headers + wavelengths_list
    df = pd.DataFrame(rows, columns=columns)

    return df

def createDataFrame(samplename):
    # Load the image
    hdr = f"./tempImages/processed_image_{samplename}_absorbance_EMSC.hdr"
    img = envi.open(hdr)
    image = img.load()

    # Load the CSV file
    file_path = './data/data_GC.csv'
    fish_data = pd.read_csv(file_path)

    # Retrieve the wavelengths from the header metadata
    wavelengths = np.array(img.metadata['wavelength'], dtype=np.float32)



    # Define the masks and their corresponding labels
    maskPath = {
        f"./masks/binary_mask_partial_{samplename}_Norwegian_Quality_Cut1.png": "NQC1",
        f"./masks/binary_mask_partial_{samplename}_Norwegian_Quality_Cut2.png": "NQC2",
        f"./masks/binary_mask_partial_{samplename}_Belly_Fat_Trimmed.png": "F2",
        f"./masks/binary_mask_partial_{samplename}_Head.png": "H",
        f"./masks/binary_mask_partial_{samplename}_Tail.png": "T"
    }

    rows = []

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
        print(f"Number of valid/discarded pixels: {pixel_count} / {discarded_count}")

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