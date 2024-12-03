import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cross_decomposition import PLSRegression

### Settings
list_targets = ['Lipid_%',
                'Saturated', #1
                'Unsaturated', #2
                'Monounsaturated', #3
                'Polyunsaturated', #4
                'Omega9', #5
                'Omega6', #6
                'Omega3', #7
                'HumanOmega3', #8
                'EPAandDHA', #9
                'C4:0', 'C6:0', 'C8:0', 'C10:0', 'C11:0', 'C12:0', #15
                'C14:0', 'C14:1n5', 'C15:0', 'C15:1n5', 'C16:0', #20
                'C16:1n7', 'C17:0', 'C17:1n7', 'C18:0', 'C18:1n9c', #25
                'C18:1n7', 'C18:2n6c', 'C18:2n6t', 'C18:3n3c', 'C18:3n6c', #30
                'C20:0', 'C20:1n9', 'C20:2n6', 'C20:3n3', 'C20:3n6', #35
                'C20:4n6', 'C20:5n3', 'C21:0', 'C22:0', 'C22:1n9', #40
                'C22:2n6', 'C22:5n3', 'C22:6n3', 'C23:0', 'C24:0', 'C24:1n9'] #46
target = list_targets[9] # 46 max
components = 14
# List of sample names
datasetChoice = 1
#samples = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17", "S18"]

### Load the data

# median coarse
file_path = f'exported_data_coarse_median_dataset{datasetChoice}.csv'
data_coarse = pd.read_csv(file_path)
# Define where the first wavlength is located
first_wavelength_coarse = 49
print("953...=" + data_coarse.columns[first_wavelength_coarse])
# X and y
X_coarse = data_coarse.iloc[:, first_wavelength_coarse:].values
y_coarse = data_coarse[target].values

# all replicate fine
file_path = f'exported_data_fine_dataset{datasetChoice}.csv'
data_fine = pd.read_csv(file_path)
# Define where the first wavlength is located
first_wavelength_fine = 53
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
plt.savefig(f"../plots/{datasetChoice}_plot_{target}_regression_coeffiecients.png", dpi=1000)
# Show the plot
plt.show()

# # Calculate the area under each curve
# area_coarse = np.trapezoid(np.abs(coefficients_coarse), wavelengths)
# area_fine = np.trapezoid(np.abs(coefficients_fine), wavelengths)
# print(f"Area under coarse model curve: {area_coarse}")
# print(f"Area under fine model curve: {area_fine}")
#
# # Scale each curve by the area of the other
# scaled_coarse = coefficients_coarse
# scaled_fine = coefficients_fine * (area_coarse/area_fine)
#
# # Plot the scaled regression coefficients for both models
# plt.figure(figsize=(10, 6))
# plt.plot(wavelengths, scaled_coarse, label='Coarse Model', color='blue', linewidth=2)
# plt.plot(wavelengths, scaled_fine, label='Scaled Fine Model', color='orange', linewidth=2)
# plt.axhline(0, color='gray', linestyle='--', linewidth=0.7)
#
# # Add labels and legend
# plt.xlabel('Wavelength (nm)', fontsize=12)
# plt.ylabel('Regression Coefficients', fontsize=12)
# plt.title(f'PLS Regression Coefficients for {target}', fontsize=14)
# plt.legend(fontsize=12)
# plt.grid(alpha=0.5)
# plt.tight_layout()
# plt.savefig(f"../plots/{datasetChoice}_plot_{target}_regression_coeffiecients.png", dpi=1000)
# # Show the scaled plot
# plt.show()
