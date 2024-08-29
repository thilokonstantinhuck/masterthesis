import matplotlib.pyplot as plt
from matplotlib.image import imread
import numpy as np
from PIL import Image

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
