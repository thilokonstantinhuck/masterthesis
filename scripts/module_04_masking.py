import matplotlib.pyplot as plt
import spectral.io.envi as envi
from matplotlib.image import imread
import matplotlib.patches as patches
import numpy as np
from PIL import Image
from config.generalParameters import lowlightWavelength, lowlightDefinition
from config.generalParameters import emscWavelength1, emscWavelength2, emscWavelength3

def emscMaskCreation(samplename,emscWavelength, wlMin, wlMax):
    # Load the hyperspectral image with absorption data
    hdr = f"./tempImages/processed_image_{samplename}_absorbance_EMSC.hdr"
    img = envi.open(hdr)
    image = img.load()

    # Retrieve the wavelengths from the header metadata
    wavelengths = np.array(img.metadata['wavelength'], dtype=np.float32)

    # Find the indices of the specified wavelengths
    index = np.argmin(np.abs(wavelengths - emscWavelength))

    # Ensure the arrays are explicitly cast to the same type
    index_data = np.array(image[:, :, index], dtype=np.float32)

    # Ensure that ratio_image is 2D
    index_image = np.squeeze(index_data)  # Remove any singleton dimensions

    # Create a binary mask based on the minRatio and maxRatio
    binary_mask = np.where((index_image >= wlMin) & (index_image <= wlMax), 1, 0).astype(np.uint8) * 255

    # Display the ratio image and the binary mask side by side
    plt.figure(figsize=(10, 7))

    # Plot the ratio image
    plt.subplot(1, 2, 1)
    plt.imshow(index_image, cmap='gist_heat', vmin=wlMin, vmax=wlMax)
    plt.title(f'Image {samplename} at {emscWavelength} between {wlMin} and {wlMax}')
    plt.axis('off')

    # Plot the binary mask
    plt.subplot(1, 2, 2)
    plt.imshow(binary_mask, cmap='gray')
    plt.title(f'Binary Mask {samplename} at {emscWavelength}')
    plt.axis('off')

    # Show the plot
    plt.savefig(f"./plots/plot_{samplename}_emsc_mask_{emscWavelength}.png", dpi=1000)
    plt.show()

    # Convert the mask to an image and save as PNG
    mask_image = Image.fromarray(binary_mask)
    mask_image.save(f"./masks/binary_mask_{samplename}_emsc_{emscWavelength}.png")
    print(f"EMSC mask {samplename} {emscWavelength}nm saved successfully.")

def combineEMSCMasks(samplename):
    # Load the binary masks
    binary_mask_emsc1 = imread(f"./masks/binary_mask_{samplename}_emsc_{emscWavelength1}.png")
    binary_mask_emsc2 = imread(f"./masks/binary_mask_{samplename}_emsc_{emscWavelength2}.png")
    binary_mask_emsc3 = imread(f"./masks/binary_mask_{samplename}_emsc_{emscWavelength3}.png")

    # Combine the masks
    combined_mask = binary_mask_emsc1 * binary_mask_emsc2 * binary_mask_emsc3

    # Convert the combined mask to uint8 format for saving
    combined_mask_uint8 = (combined_mask * 255).astype(np.uint8)

    # Save the final combined mask as a grayscale image using PIL
    combined_mask_image = Image.fromarray(combined_mask_uint8, mode='L')
    combined_mask_image.save(f"./masks/binary_mask_{samplename}_emsc.png")

    print(f"Combined emsc mask {samplename} created and saved successfully.")

def combineMasks(samplename):
    # Load the binary masks
    binary_mask_overlit = imread(f"./masks/binary_mask_{samplename}_overlit.png")
    binary_mask_emsc = imread(f"./masks/binary_mask_{samplename}_emsc.png")
    binary_mask_lowlight = imread(f"./masks/binary_mask_{samplename}_lowlight.png")

    # Combine the masks
    combined_mask = binary_mask_emsc * binary_mask_overlit * binary_mask_lowlight

    # Find the pixels where each mask differs (i.e., where a mask has value 0 while others are 1)
    diff_mask_emsc = np.logical_and(binary_mask_emsc == 0,
                                    np.logical_or(binary_mask_overlit == 1, binary_mask_lowlight == 1))
    diff_mask_overlit = np.logical_and(binary_mask_overlit == 0,
                                       np.logical_or(binary_mask_emsc == 1, binary_mask_lowlight == 1))
    diff_mask_lowlight = np.logical_and(binary_mask_lowlight == 0,
                                        np.logical_or(binary_mask_emsc == 1, binary_mask_overlit == 1))

    # Prepare the images for plotting
    mask1_display = np.stack([binary_mask_emsc, binary_mask_emsc, binary_mask_emsc], axis=-1)
    mask2_display = np.stack([binary_mask_overlit, binary_mask_overlit, binary_mask_overlit], axis=-1)
    mask3_display = np.stack([binary_mask_lowlight, binary_mask_lowlight, binary_mask_lowlight], axis=-1)

    # Highlight the differences in red for each mask
    mask1_display[diff_mask_emsc] = [1, 0, 0]  # Red color for different pixels in EMSC mask
    mask2_display[diff_mask_overlit] = [1, 0, 0]  # Red color for different pixels in Overlit mask
    mask3_display[diff_mask_lowlight] = [1, 0, 0]  # Red color for different pixels in Lowlight mask

    # Plotting
    fig, axes = plt.subplots(1, 3, figsize=(10, 5))
    axes[0].imshow(mask1_display)
    axes[0].set_title(f"EMSC Mask for {samplename}")
    axes[0].axis('off')

    axes[1].imshow(mask2_display)
    axes[1].set_title(f"Overlit Mask for {samplename}")
    axes[1].axis('off')

    axes[2].imshow(mask3_display)
    axes[2].set_title(f"Lowlight Mask for {samplename}")
    axes[2].axis('off')

    plt.savefig(f"./plots/plot_{samplename}_mask_combination_analysis.png", dpi=1000)
    plt.show()

    # Convert the combined mask to uint8 format for saving
    combined_mask_uint8 = (combined_mask * 255).astype(np.uint8)

    # Save the final combined mask as a grayscale image using PIL
    combined_mask_image = Image.fromarray(combined_mask_uint8, mode='L')
    combined_mask_image.save(f"./masks/binary_mask_{samplename}_combined.png")

    print(f"Final combined mask {samplename} created and saved successfully.")

def combineMasksNoEMSC(samplename):
    # Load the binary masks
    binary_mask_overlit = imread(f"./masks/binary_mask_{samplename}_overlit.png")
    binary_mask_lowlight = imread(f"./masks/binary_mask_{samplename}_lowlight.png")

    # Combine the masks
    combined_mask = binary_mask_overlit * binary_mask_lowlight

    # Prepare the images for plotting
    mask2_display = np.stack([binary_mask_overlit, binary_mask_overlit, binary_mask_overlit], axis=-1)
    mask3_display = np.stack([binary_mask_lowlight, binary_mask_lowlight, binary_mask_lowlight], axis=-1)

    # Plotting
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    axes[0].imshow(mask2_display)
    axes[0].set_title(f"Overlit Mask for {samplename}")
    axes[0].axis('off')

    axes[1].imshow(mask3_display)
    axes[1].set_title(f"Lowlight Mask for {samplename}")
    axes[1].axis('off')

    plt.savefig(f"./plots/plot_{samplename}_mask_combination_analysis.png", dpi=1000)
    plt.show()

    # Convert the combined mask to uint8 format for saving
    combined_mask_uint8 = (combined_mask * 255).astype(np.uint8)

    # Save the final combined mask as a grayscale image using PIL
    combined_mask_image = Image.fromarray(combined_mask_uint8, mode='L')
    combined_mask_image.save(f"./masks/binary_mask_{samplename}_combined.png")

    print(f"Final combined mask {samplename} created and saved successfully.")

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


def lowlightMaskCreation(samplename):
    # Load the hyperspectral image with absorption data
    hdr = f"./tempImages/processed_image_{samplename}_absorbance_EMSC.hdr"
    img = envi.open(hdr)
    image = img.load()

    # Retrieve the wavelengths from the header metadata
    wavelengths = np.array(img.metadata['wavelength'], dtype=np.float32)

    # Find the index of the specified lowlight wavelength
    index = np.argmin(np.abs(wavelengths - lowlightWavelength))

    # Ensure the array is explicitly cast to the same type
    lowlight_data = np.array(image[:, :, index], dtype=np.float32)

    # Create a binary mask where the values are below the lowlightDefinition
    lowlight_mask = np.where(lowlight_data < lowlightDefinition, 0, 1).astype(np.uint8) * 255

    # Ensure lowlight_mask is a 2D array
    if lowlight_mask.ndim == 3 and lowlight_mask.shape[-1] == 1:
        lowlight_mask = lowlight_mask.squeeze(axis=-1)

    # Display the lowlight mask
    plt.figure(figsize=(6, 6))
    plt.imshow(lowlight_mask, cmap='gray')
    plt.title(f'Lowlight Mask {samplename} (Wavelength {lowlightWavelength}nm)')
    plt.axis('off')

    # Save the plot as an image file
    plt.savefig(f"./plots/plot_{samplename}_lowlight_mask.png", dpi=1000)
    plt.show()

    # Convert the mask to an image and save as PNG
    mask_image = Image.fromarray(lowlight_mask, mode='L')
    mask_image.save(f"./masks/binary_mask_{samplename}_lowlight.png")

    print(f"Lowlight mask for {samplename} saved successfully.")

def fineMasking(samplename, centerPoints):
    # Load the binary mask
    binary_mask = imread(f"./plots/plot_{samplename}_emsc.png")

    # Create a figure and axis to plot the image
    fig, ax = plt.subplots(figsize=(10, 20))  # Adjust the figure size to match the aspect ratio

    # Display the image
    ax.imshow(binary_mask, cmap='gray')

    # Draw each rectangle
    subsquare_size = 25  # Example predefined width and height
    numberOfSubsquares = 5

    for top_left, name in centerPoints:
        for row in range(numberOfSubsquares):
            for col in range(numberOfSubsquares):
                width = subsquare_size
                height = subsquare_size
                rect = patches.Rectangle((top_left[1]+col*subsquare_size, top_left[0]+row*subsquare_size), width, height, linewidth=1, edgecolor='r', facecolor='none')

                ax.add_patch(rect)

    # Customize the plot as needed
    ax.set_title(f'Binary Mask {samplename} with Rectangles')
    ax.axis('on')  # Show the axes

    # Save the plot as an image file
    fig.savefig(f"./plots/plot_{samplename}_combined_mask.png", dpi=300, bbox_inches='tight')

    # Display the plot
    plt.show()

def emscPicture(samplename, emscWavelength, wlMin, wlMax):
    # Load the hyperspectral image with absorption data
    hdr = f"./tempImages/processed_image_{samplename}_absorbance_EMSC.hdr"
    img = envi.open(hdr)
    image = img.load()

    # Retrieve the wavelengths from the header metadata
    wavelengths = np.array(img.metadata['wavelength'], dtype=np.float32)

    # Find the index of the specified wavelength
    index = np.argmin(np.abs(wavelengths - emscWavelength))

    # Ensure the arrays are explicitly cast to the same type
    index_data = np.array(image[:, :, index], dtype=np.float32)

    # Ensure that index_image is 2D
    index_image = np.squeeze(index_data)  # Remove any singleton dimensions

    # Show the image with a colormap
    plt.figure(figsize=(4, 6))
    plt.imshow(index_image, cmap='gist_heat', vmin=0.4, vmax=0.7)
    plt.colorbar(label=f'Absorbance at {emscWavelength}nm')
    plt.title(f'EMSC Image at {emscWavelength}nm for {samplename}')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')

    # Save the figure
    plt.savefig(f"./plots/plot_{samplename}_emsc_{emscWavelength}.png")
    plt.show()

    # Convert the normalized image to an 8-bit grayscale PNG for further use
    emsc_image = Image.fromarray((index_image * 255).astype(np.uint8))
    emsc_image.save(f"./plots/plot_{samplename}_emsc.png")
    print(f"EMSC Picture {samplename} {emscWavelength}nm saved successfully.")

def fineCutMaskCreation(samplename, centerPoints):
    # Load the binary mask
    binary_mask = imread(f"./masks/binary_mask_{samplename}_combined.png")

    # Draw each rectangle
    subsquare_size = 25  # Example predefined width and height
    numberOfSubsquares = 5

    for top_left, name in centerPoints:
        for row in range(numberOfSubsquares):
            for col in range(numberOfSubsquares):
                # Create a mask of the same dimensions as the original binary mask
                mask = np.zeros_like(binary_mask)
                squareID = (row*5)+col
                x = top_left[1]+col*subsquare_size
                y = top_left[0]+row*subsquare_size
                # Fill in the rectangle area with the original mask's values
                mask[y:y+subsquare_size, x:x+subsquare_size] = binary_mask[y:y+subsquare_size, x:x+subsquare_size]

                # Convert the mask to uint8 (assuming mask is binary)
                mask = (mask * 255).astype(np.uint8)

                # Convert the mask to an image and save as PNG
                mask_image = Image.fromarray(mask)
                mask_image.save(f"./masks/binary_mask_partial_{samplename}_{name}_{squareID}.png")

                print(f"Mask for {samplename} {name} {squareID} saved")