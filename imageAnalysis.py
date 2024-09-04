from PIL import Image

# Load the image
# image = Image.open('C:/Users/thilohuc/PycharmProjects/masterthesis/masks/binary_mask_partial_S06_Belly_Fat_Trimmed.png')
image = Image.open('C:/Users/thilohuc/PycharmProjects/masterthesis/masks/binary_mask_S06_lowlight.png')
# image = Image.open('C:/Users/thilohuc/PycharmProjects/masterthesis/masks/binary_mask_S06_overlit.png')
# image = Image.open('C:/Users/thilohuc/PycharmProjects/masterthesis/masks/binary_mask_S06_combined.png')
# Print image mode
print(f"Image mode: {image.mode}")

# Determine number of channels based on mode
channels = len(image.getbands())
print(f"Number of channels: {channels}")
