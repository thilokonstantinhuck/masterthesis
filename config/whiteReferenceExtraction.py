import spectral.io.envi as envi
import numpy as np
import matplotlib.pyplot as plt
import pprint
import math

# Load the image
hdr = "C:/SALMONDATA/SWIR_Hyspex/All_converted_file/S6-R-G1_SWIR_384_SN3151_9006us_2022-05-02T120753_raw_rad_float32.hdr"
hdr = "C:/Users/thilohuc/PycharmProjects/masterthesis/tempImages/processed_image_S06_absorbance.hdr"
img = envi.open(hdr)
image = img.load()

# Retrieve the wavelengths from the header metadata
wavelengths = np.array(img.metadata['wavelength'], dtype=np.float32)

#define area for white reference area
whiteArea = ((1900, 150), (2000, 330))

#define area for fish reference area
whiteArea = ((750, 150), (1000, 330))

# Extract coordinates from whiteArea
(y1, x1), (y2, x2) = whiteArea

# Ensure coordinates are within image bounds
height, width, bands = image.shape
if x1 < 0 or x2 >= width or y1 < 0 or y2 >= height:
    print("One or more coordinates are out of bounds.")

count = 0  # Initialize a counter

# Plot spectra for all pixels in the specified area
plt.figure(figsize=(10, 6))
for x in range(x1, x2 + 1):
    for y in range(y1, y2 + 1):
        if count % 100 == 0:  # Plot only every 100th spectrum
            spectrum = image[y, x, :].squeeze()  # Extract the spectrum for each pixel (y, x)
            plt.plot(wavelengths, spectrum, label=f"Pixel ({x}, {y})")
        count += 1  # Increment the counter

# Label the plot
plt.title('Spectra of white Pixels')
plt.xlabel('Wavelength [nm]')
plt.ylabel('Intensity')
plt.show()

# Initialize an array to accumulate the spectra
accumulated_spectrum = np.zeros(image.shape[2], dtype=np.float32)
pixel_count = 0
discarded_count = 0

# Accumulate spectra for pixels within the binary mask

for x in range(x1, x2 + 1):
    for y in range(y1, y2 + 1):
        spectra = image[y, x, :].squeeze()
        if not any(math.isinf(x) for x in spectra):
            accumulated_spectrum += spectra
            pixel_count += 1
        else:
            discarded_count += 1

# print discarded and pixels
print(f"Number of valid pixels: {pixel_count}")
print(f"Number of discarded pixels: {discarded_count}")


# Calculate the average spectrum
average_spectrum = accumulated_spectrum / pixel_count

# Plot the average spectrum for this mask
plt.figure(figsize=(10, 6))
plt.plot(wavelengths, average_spectrum)
plt.xlabel('Wavelength (nm)')
plt.ylabel('Intensity')
plt.title(f'Average Spectra white reference')

plt.show()

pprint.pprint(average_spectrum)