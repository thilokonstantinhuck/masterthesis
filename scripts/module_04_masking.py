import matplotlib.pyplot as plt
import spectral.io.envi as envi
from matplotlib.image import imread
import matplotlib.patches as patches
import numpy as np
from PIL import Image
from config.generalParameters import emscMinRatio, emscMaxRatio, emscWavelength1, emscWavelength2

def emscMaskCreation(samplename):
    # Load the hyperspectral image with absorption data
    hdr = f"./tempImages/processed_image_{samplename}_EMSC.hdr"
    img = envi.open(hdr)
    image = img.load()

    # Retrieve the wavelengths from the header metadata
    wavelengths = np.array(img.metadata['wavelength'], dtype=np.float32)

    # Find the indices of the specified wavelengths
    index1 = np.argmin(np.abs(wavelengths - emscWavelength1))
    index2 = np.argmin(np.abs(wavelengths - emscWavelength2))

    # Ensure the arrays are explicitly cast to the same type
    index1_data = np.array(image[:, :, index1], dtype=np.float32)
    index2_data = np.array(image[:, :, index2], dtype=np.float32)

    # Calculate the ratio of absorbance at the two wavelengths for each pixel
    ratio_image = np.divide(index2_data, index1_data)  # Use np.divide to calculate the ratio

    # Ensure that ratio_image is 2D
    ratio_image = np.squeeze(ratio_image)  # Remove any singleton dimensions

    # Create a binary mask based on the minRatio and maxRatio
    binary_mask = np.where((ratio_image >= emscMinRatio) & (ratio_image <= emscMaxRatio), 1, 0).astype(np.uint8) * 255

    # Display the ratio image and the binary mask side by side
    plt.figure(figsize=(10, 7))

    # Plot the ratio image
    plt.subplot(1, 2, 1)
    plt.imshow(ratio_image, cmap='gist_heat', vmin=emscMinRatio, vmax=emscMaxRatio)
    plt.title(f'Ratio Image (between {emscWavelength1}nm and {emscWavelength2}nm)')
    plt.axis('off')

    # Plot the binary mask
    plt.subplot(1, 2, 2)
    plt.imshow(binary_mask, cmap='gray')
    plt.title(f'Binary Mask (Ratio between {emscMinRatio} and {emscMaxRatio})')
    plt.axis('off')

    # Show the plot
    plt.savefig(f"./plots/plot_{samplename}_emsc_mask.png", dpi=1000)
    plt.show()

    # Convert the mask to an image and save as PNG
    mask_image = Image.fromarray(binary_mask)
    mask_image.save(f"./masks/binary_mask_{samplename}_emsc.png")
    print(f"EMSC mask {samplename} saved successfully.")

def combineMasks(samplename):
    # Load the binary masks
    binary_mask_overlit = imread(f"./masks/binary_mask_{samplename}_overlit.png")
    binary_mask_emsc = imread(f"./masks/binary_mask_{samplename}_emsc.png")

    # Combine the masks
    combined_mask = binary_mask_emsc * binary_mask_overlit

    # Find the pixels where the masks differ
    diff_mask_1 = np.logical_and(binary_mask_emsc == 1, binary_mask_overlit == 0)
    diff_mask_2 = np.logical_and(binary_mask_emsc == 0, binary_mask_overlit == 1)

    # Prepare the images for plotting
    mask1_display = np.stack([binary_mask_emsc, binary_mask_emsc, binary_mask_emsc], axis=-1)
    mask2_display = np.stack([binary_mask_overlit, binary_mask_overlit, binary_mask_overlit], axis=-1)

    # Highlight the differences in red
    mask1_display[diff_mask_1] = [1, 0, 0]  # Red color for different pixels
    mask2_display[diff_mask_2] = [1, 0, 0]  # Red color for different pixels

    # Plotting
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    axes[0].imshow(mask1_display)
    axes[0].set_title(f"EMSC Mask for {samplename}")
    axes[0].axis('off')

    axes[1].imshow(mask2_display)
    axes[1].set_title(f"Overlit Mask for {samplename}")
    axes[1].axis('off')

    plt.savefig(f"./plots/plot_{samplename}_mask_combination_analysis.png", dpi=1000)
    plt.show()

    # Convert the combined mask to uint8 format for saving
    combined_mask_uint8 = (combined_mask * 255).astype(np.uint8)

    # Save the final combined mask as a grayscale image using PIL
    combined_mask_image = Image.fromarray(combined_mask_uint8, mode='L')
    combined_mask_image.save(f"./masks/binary_mask_{samplename}_combined.png")

    print("Final combined mask created and saved successfully.")

def rectangleAnalysis(samplename, rectangles, backgroundArea):

    # Load the binary mask
    binary_mask = imread(f"./masks/binary_mask_{samplename}_combined.png")

    # Create a figure and axis to plot the image
    fig, ax = plt.subplots(figsize=(10, 20))  # Adjust the figure size to match the aspect ratio

    # Display the image
    ax.imshow(binary_mask, cmap='gray')

    # Draw each rectangle
    for top_left, bottom_right, name in rectangles:
        width = bottom_right[1] - top_left[1]
        height = bottom_right[0] - top_left[0]
        # Note: patches.Rectangle expects (x, y) to be the lower-left corner
        rect = patches.Rectangle((top_left[1], top_left[0]), width, height, linewidth=2, edgecolor='r', facecolor='none')
        ax.add_patch(rect)

    # widthWhite = whiteArea[1][1] - whiteArea[0][1]
    # heightWhite = whiteArea[1][0] - whiteArea[0][0]
    # rect = patches.Rectangle((whiteArea[0][1], whiteArea[0][0]), widthWhite, heightWhite, linewidth=2, edgecolor='b', facecolor='none')
    # ax.add_patch(rect)

    # Customize the plot as needed
    ax.set_title(f'Binary Mask {samplename} with Rectangles')
    ax.axis('on')  # Show the axes

    # Save the plot as an image file
    fig.savefig(f"./plots/plot_{samplename}_combined_mask.png", dpi=300, bbox_inches='tight')

    # Display the plot
    plt.show()

def cutMaskCreation(samplename, rectangles):
    # Load the binary mask
    binary_mask = imread(f"./masks/binary_mask_{samplename}_combined.png")

    # Create and save individual masks for each rectangle
    for top_left, bottom_right, name in rectangles:
        # Create a mask of the same dimensions as the original binary mask
        mask = np.zeros_like(binary_mask)

        # Fill in the rectangle area with the original mask's values
        mask[top_left[0]:bottom_right[0], top_left[1]:bottom_right[1]] = binary_mask[top_left[0]:bottom_right[0],
                                                                         top_left[1]:bottom_right[1]]

        # Convert the mask to uint8 (assuming mask is binary)
        mask = (mask * 255).astype(np.uint8)

        # Convert the mask to an image and save as PNG
        mask_image = Image.fromarray(mask)
        mask_image.save(f"./masks/binary_mask_partial_{samplename}_{name}.png")

        print(f"Mask for {samplename} {name} saved")