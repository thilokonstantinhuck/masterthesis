import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cross_decomposition import PLSRegression

### Settings
# target = "C20:1n9"
#target = "EPAandDHA"
target = "Lipid_%"
components = 5
# List of sample names
datasetChoice = 3
samples = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17", "S18"]

### Load the data

# median coarse
file_path = f'exported_data_coarse_median_dataset{datasetChoice}.csv'
data_coarse = pd.read_csv(file_path)
# Define where the first wavlength is located
first_wavelength_coarse = 41
print("953...=" + data_coarse.columns[first_wavelength_coarse])
# X and y
X_coarse = data_coarse.iloc[:, first_wavelength_coarse:].values
y_coarse = data_coarse[target].values

# all replicate fine
file_path = f'exported_data_fine_dataset{datasetChoice}.csv'
data_fine = pd.read_csv(file_path)
# Define where the first wavlength is located
first_wavelength_fine = 46
print("953...=" + data_fine.columns[first_wavelength_fine])
# X and y
X_fine = data_fine.iloc[:, first_wavelength_fine:].values
y_fine = data_fine[target].values

# Model with specific number of components selected
pls_model_coarse = PLSRegression(n_components=components)
pls_model_fine = PLSRegression(n_components=components)

# Train the PLS model on the train set
pls_model_coarse.fit(X_coarse, y_coarse)
pls_model_fine.fit(X_fine, y_fine)

#wavelengths for printing
wavelengths = np.array(data_coarse.iloc[:, first_wavelength_coarse:].columns, dtype=float)

# Get regression coefficients for each model
coefficients_coarse = pls_model_coarse.coef_.flatten()
coefficients_fine = pls_model_fine.coef_.flatten()

# Plot the regression coefficients for both models
plt.figure(figsize=(10, 6))
plt.plot(wavelengths, coefficients_coarse, label='Coarse Model', color='blue', linewidth=2)
plt.plot(wavelengths, coefficients_fine, label='Fine Model', color='orange', linewidth=2)
plt.axhline(0, color='gray', linestyle='--', linewidth=0.7)

# Add labels and legend
plt.xlabel('Wavelength (nm)', fontsize=12)
plt.ylabel('Regression Coefficients', fontsize=12)
plt.title(f'PLS Regression Coefficients for {target}', fontsize=14)
plt.legend(fontsize=12)
plt.grid(alpha=0.5)
plt.tight_layout()

# Show the plot
plt.show()

# Calculate the area under each curve
area_coarse = np.trapezoid(np.abs(coefficients_coarse), wavelengths)
area_fine = np.trapezoid(np.abs(coefficients_fine), wavelengths)
print(f"Area under coarse model curve: {area_coarse}")
print(f"Area under fine model curve: {area_fine}")

# Scale each curve by the area of the other
scaled_coarse = coefficients_coarse
scaled_fine = coefficients_fine * (area_coarse/area_fine)

# Plot the scaled regression coefficients for both models
plt.figure(figsize=(10, 6))
plt.plot(wavelengths, scaled_coarse, label='Coarse Model', color='blue', linewidth=2)
plt.plot(wavelengths, scaled_fine, label='Scaled Fine Model', color='orange', linewidth=2)
plt.axhline(0, color='gray', linestyle='--', linewidth=0.7)

# Add labels and legend
plt.xlabel('Wavelength (nm)', fontsize=12)
plt.ylabel('Regression Coefficients', fontsize=12)
plt.title(f'PLS Regression Coefficients for {target}', fontsize=14)
plt.legend(fontsize=12)
plt.grid(alpha=0.5)
plt.tight_layout()

# Show the scaled plot
plt.show()
