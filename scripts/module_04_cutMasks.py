import matplotlib.pyplot as plt
from matplotlib.image import imread
import matplotlib.patches as patches
import numpy as np
from PIL import Image

def cutMaskCreation(samplename, rectangles):
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

    # Customize the plot as needed
    ax.set_title(f'Binary Mask {samplename} with Rectangles')
    ax.axis('on')  # Show the axes

    # Save the plot as an image file
    fig.savefig(f"./plots/plot_{samplename}_combined_mask.png", dpi=300, bbox_inches='tight')

    # Display the plot
    plt.show()

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
