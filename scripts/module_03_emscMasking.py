import spectral.io.envi as envi
import numpy as np
import matplotlib.pyplot as plt
from config.generalParameters import emscMinRatio, emscMaxRatio, emscWavelength1, emscWavelength2

def emscProcessing(samplename):
    # Load the hyperspectral image with absorption data
    hdr = f".\\tempImages\\processed_image_{samplename}_EMSC.hdr"
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
    binary_mask = np.where((ratio_image >= emscMinRatio) & (ratio_image <= emscMaxRatio), 1, 0)

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

    # Save the binary mask as a PNG file
    plt.imsave(f"./masks/binary_mask_{samplename}_emsc.png", binary_mask, cmap='gray')
    print(f"EMSC mask {samplename} saved successfully.")
