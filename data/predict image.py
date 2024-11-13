import spectral.io.envi as envi
import pickle
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os

# change here
samplename = "S06"
ROI = [
    [240, 750],
    [243, 750],
    [245, 750],
    [240, 752],
    [243, 752],
    [245, 752],
    [240, 754],
    [243, 754],
    [245, 754],
    [240, 756],
    [243, 756],
    [245, 756],
]

# Load the trained PLS model
model_filename = 'pls_model.pkl'
with open(model_filename, 'rb') as file:
    pls_model = pickle.load(file)

# Load the original image
# filename = "S6-R-G1_SWIR_384_SN3151_9006us_2022-05-02T120753_raw_rad_float32.hdr"
# imageFolder = r"C:\SALMONDATA\SWIR_Hyspex\All_converted_file"
# hdr = os.path.join(imageFolder, filename)

hdr = f"../tempImages/processed_image_{samplename}_absorbance_EMSC.hdr"

img = envi.open(hdr)
image = img.load()

# Reshape the image data to be compatible with the model
# The image is reshaped into (num_pixels, num_wavelengths)
num_pixels = image.shape[0] * image.shape[1]
num_wavelengths = image.shape[2]
X = image.reshape((num_pixels, num_wavelengths))

# Make predictions using the loaded model
y_pred = pls_model.predict(X).flatten()

# Reshape the predictions back to the original image shape (height, width)
predicted_image = y_pred.reshape((image.shape[0], image.shape[1]))

# Set grayscale limits for the predicted image
min_val, max_val = 0, 30  # Adjust these values as needed

# Scale the predicted image to the specified grayscale limits and save as PNG
scaled_image = np.clip((predicted_image - min_val) * 255 / (max_val - min_val), 0, 255).astype(np.uint8)
cv2.imwrite(f"predicted_image_{samplename}.png", scaled_image)

# Retrieve the wavelengths from the header metadata
wavelengths = np.array(img.metadata['wavelength'], dtype=np.float32).flatten()

# Plot the predicted values as an image and the spectra of selected pixels
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 20), gridspec_kw={'width_ratios': [1, 2]})

# Plot the predicted image
cax = ax1.imshow(predicted_image, cmap='viridis', vmin=-1, vmax=30)
fig.colorbar(cax, ax=ax1, label="Predicted %")
ax1.set_title("Lipid Prediction")
ax1.set_xlabel("Width")
ax1.set_ylabel("Height")

# Mark the selected ROI pixels in red
for pixel in ROI:
    ax1.plot(pixel[0], pixel[1], 'ro')

# Plot the spectrum at the selected positions
for pixel in ROI:
    ax2.plot(wavelengths, image[pixel[1], pixel[0], :].flatten(), label=f"Pixel ({pixel[0]}, {pixel[1]}), Value of {round(predicted_image[pixel[1], pixel[0]],2)}")

ax2.set_xlabel("Wavelength (nm)")
ax2.set_ylabel("Absorbance")
ax2.set_title("Spectra of Selected Pixels")
#ax2.set_ylim([-0.01, 0.3])  # Set y-axis limits for ax2
ax2.set_ylim([-0.1, 3])  # Set y-axis limits for ax2
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()