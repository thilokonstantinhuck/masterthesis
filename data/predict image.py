import spectral.io.envi as envi
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cross_decomposition import PLSRegression
import cv2

## Settings
number_of_components = 5

# Set grayscale limits depending on the target for the predicted image
# target = "Lipid_%"
# min_val, max_val = 0, 25  # Adjust these values as needed
target = "EPAandDHA"
min_val, max_val = 1, 15  # Adjust these values as needed


datasetChoice = 3
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

##Dataset

# median coarse
file_path = f'exported_data_coarse_median_dataset{datasetChoice}.csv'
data_coarse = pd.read_csv(file_path)
# Define where the first wavlength is located
first_wavelength_coarse = 41
print(data_coarse.columns[first_wavelength_coarse])
X_coarse = data_coarse.iloc[:, first_wavelength_coarse:].values
y_coarse = data_coarse[target].values

# all replicate fine
file_path = f'exported_data_fine_dataset{datasetChoice}.csv'
data_fine = pd.read_csv(file_path)
# Define where the first wavlength is located
first_wavelength_fine = 46
print(data_fine.columns[first_wavelength_fine])
X_fine = data_fine.iloc[:, first_wavelength_fine:].values
y_fine = data_fine[target].values


hdr = f"../tempImages/{datasetChoice}_processed_image_{samplename}_absorbance_EMSC.hdr"
img = envi.open(hdr)
image = img.load()

## Model Creation
pls_model_fine = PLSRegression(n_components=number_of_components)
pls_model_fine.fit(X_fine, y_fine)
pls_model_coarse = PLSRegression(n_components=number_of_components)
pls_model_coarse.fit(X_coarse, y_coarse)

# Reshape the image data to be compatible with the model
# The image is reshaped into (num_pixels, num_wavelengths)
num_pixels = image.shape[0] * image.shape[1]
num_wavelengths = image.shape[2]
X = image.reshape((num_pixels, num_wavelengths))

# Make predictions using the loaded model
y_pred_coarse = pls_model_coarse.predict(X).flatten()
y_pred_fine = pls_model_fine.predict(X).flatten()

# Reshape the predictions back to the original image shape (height, width)
predicted_image_coarse = y_pred_coarse.reshape((image.shape[0], image.shape[1]))
predicted_image_fine = y_pred_fine.reshape((image.shape[0], image.shape[1]))



# Scale the predicted image to the specified grayscale limits and save as PNG
predicted_image_coarse_scaled = np.clip((predicted_image_coarse - min_val) * 255 / (max_val - min_val), 0, 255).astype(np.uint8)
predicted_image_fine_scaled = np.clip((predicted_image_fine - min_val) * 255 / (max_val - min_val), 0, 255).astype(np.uint8)
cv2.imwrite(f"../plots/{datasetChoice}_{samplename}_{target}_{number_of_components}_coarse.png", predicted_image_coarse_scaled)
cv2.imwrite(f"../plots/{datasetChoice}_{samplename}_{target}_{number_of_components}_fine.png", predicted_image_fine_scaled)

# # Retrieve the wavelengths from the header metadata
# wavelengths = np.array(img.metadata['wavelength'], dtype=np.float32).flatten()
#
# # Plot the predicted values as an image and the spectra of selected pixels
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 20), gridspec_kw={'width_ratios': [1, 2]})
#
# # Plot the predicted image
# cax = ax1.imshow(predicted_image, cmap='viridis', vmin=-1, vmax=30)
# fig.colorbar(cax, ax=ax1, label="Predicted %")
# ax1.set_title("Lipid Prediction")
# ax1.set_xlabel("Width")
# ax1.set_ylabel("Height")
#
# # Mark the selected ROI pixels in red
# for pixel in ROI:
#     ax1.plot(pixel[0], pixel[1], 'ro')
#
# # Plot the spectrum at the selected positions
# for pixel in ROI:
#     ax2.plot(wavelengths, image[pixel[1], pixel[0], :].flatten(), label=f"Pixel ({pixel[0]}, {pixel[1]}), Value of {round(predicted_image[pixel[1], pixel[0]],2)}")
#
# ax2.set_xlabel("Wavelength (nm)")
# ax2.set_ylabel("Absorbance")
# ax2.set_title("Spectra of Selected Pixels")
# #ax2.set_ylim([-0.01, 0.3])  # Set y-axis limits for ax2
# ax2.set_ylim([-0.1, 3])  # Set y-axis limits for ax2
# ax2.legend()
# ax2.grid(True)
#
# plt.tight_layout()
# plt.show()