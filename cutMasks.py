import matplotlib.pyplot as plt
from matplotlib.image import imread
import matplotlib.patches as patches
import numpy as np

# Load the binary mask
binary_mask = imread("final_combined_binary_mask.png")

# Create a figure and axis to plot the image
fig, ax = plt.subplots(figsize=(10, 20))  # Adjust the figure size to match the aspect ratio

# Display the image
ax.imshow(binary_mask, cmap='gray')

# Define the rectangles by specifying two points (top-left and bottom-right) with names
rectangles = [
    ((300, 150), (400, 300), 'Tail'),  # T: Tail
    ((750, 300), (850, 380), 'Norwegian_Quality_Cut1'),  # N1: Norwegian Quality Cut 1
    ((750, 120), (850, 200), 'Norwegian_Quality_Cut2'),  # N2: Norwegian Quality Cut 2
    ((1500, 300), (1600, 380), 'Head'),  # H: Head
    ((1500, 0), (1600, 80), 'Belly_Fat_Trimmed')  # F2: Belly with trimmed visceral fat
]

# Draw each rectangle
for top_left, bottom_right, name in rectangles:
    width = bottom_right[1] - top_left[1]
    height = bottom_right[0] - top_left[0]
    # Note: patches.Rectangle expects (x, y) to be the lower-left corner
    rect = patches.Rectangle((top_left[1], top_left[0]), width, height, linewidth=2, edgecolor='r', facecolor='none')
    ax.add_patch(rect)

# Customize the plot as needed
ax.set_title('Binary Mask with Rectangles')
ax.axis('on')  # Show the axes

# Save the plot as an image file
fig.savefig('binary_mask_with_rectangles.png', dpi=300, bbox_inches='tight')

# Display the plot
plt.show()

# Create and save individual masks for each rectangle
for top_left, bottom_right, name in rectangles:
    # Create a mask of the same dimensions as the original binary mask
    mask = np.zeros_like(binary_mask)

    # Fill in the rectangle area with the original mask's values
    mask[top_left[0]:bottom_right[0], top_left[1]:bottom_right[1]] = binary_mask[top_left[0]:bottom_right[0],
                                                                     top_left[1]:bottom_right[1]]
    # Set the alpha channel to 255 (fully opaque)
    mask[:, :, 3] = 1  # Assuming the fourth channel is the alpha channel

    # Save the mask with a filename derived from the rectangle's name
    filename = f'{name}_mask.png'
    plt.imsave(filename, mask, cmap='gray')

    print(f"Mask saved as {filename}")
