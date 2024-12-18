from config.generalParameters import gcLength
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cross_decomposition import PLSRegression
from sklearn.metrics import r2_score, mean_absolute_error

### Settings
list_targets = [
    'Lipid_%',
    'Saturated',
    'Unsaturated',
    'Monounsaturated',
    'Polyunsaturated',
    'Omega9',
    'Omega6',
    'Omega3',
    'HumanOmega3',
    'EPAandDHA',
    'C4:0',
    'C6:0',
    'C8:0',
    'C10:0',
    'C11:0',
    'C12:0',
    'C14:0',
    'C14:1n5',
    'C15:0',
    'C15:1n5',
    'C16:0',
    'C16:1n7',
    'C17:0',
    'C17:1n7',
    'C18:0',
    'C18:1n9c',
    'C18:1n7',
    'C18:2n6c',
    'C18:2n6t',
    'C18:3n3c',
    'C18:3n6c',
    'C20:0',
    'C20:1n9',
    'C20:2n6',
    'C20:3n3',
    'C20:3n6',
    'C20:4n6',
    'C20:5n3',
    'C21:0',
    'C22:0',
    'C22:1n9',
    'C22:2n6',
    'C22:5n3',
    'C22:6n3',
    'C23:0',
    'C24:0',
    'C24:1n9',
    'T_Saturated', #47
    'T_Unsaturated',
    'T_Monounsaturated',
    'T_Polyunsaturated',
    'T_Omega9',
    'T_Omega6',
    'T_Omega3',
    'T_HumanOmega3',
    'T_EPAandDHA', #55
    'T_C4_0',
    'T_C6_0',
    'T_C8_0',
    'T_C10_0',
    'T_C11_0',
    'T_C12_0',
    'T_C14_0',
    'T_C14_1n5',
    'T_C15_0',
    'T_C15_1n5',
    'T_C16_0',
    'T_C16_1n7',
    'T_C17_0',
    'T_C17_1n7',
    'T_C18_0',
    'T_C18_1n9c',
    'T_C18_1n7',
    'T_C18_2n6c',
    'T_C18_2n6t',
    'T_C18_3n3c',
    'T_C18_3n6c',
    'T_C20_0',
    'T_C20_1n9',
    'T_C20_2n6',
    'T_C20_3n3',
    'T_C20_3n6',
    'T_C20_4n6',
    'T_C20_5n3',
    'T_C21_0',
    'T_C22_0',
    'T_C22_1n9',
    'T_C22_2n6',
    'T_C22_5n3',
    'T_C22_6n3',
    'T_C23_0',
    'T_C24_0',
    'T_C24_1n9'
]

targetChoice = 0
target = list_targets[targetChoice]
components = 1
# List of sample names
datasetChoice = 3
#samples = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17", "S18"]

### Load the data

# median coarse
file_path = f'exported_data_coarse_median_dataset{datasetChoice}.csv'
data_coarse = pd.read_csv(file_path)
# Define where the first wavlength is located
first_wavelength_coarse = gcLength
print("953...=" + data_coarse.columns[first_wavelength_coarse])

# all replicate fine
file_path = f'exported_data_fine_dataset{datasetChoice}.csv'
data_fine = pd.read_csv(file_path)
# Define where the first wavlength is located
first_wavelength_fine = first_wavelength_coarse+4
print("953...=" + data_fine.columns[first_wavelength_fine])

feedGroups = [["S01", "S02", "S03", "S04", "S05", "S06"],
              ["S07", "S08", "S09", "S10", "S11", "S12"],
              ["S13", "S14", "S15", "S16", "S17", "S18"]]

# Create subplots: 2 rows, 1 column
fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# Wavelengths for plotting
wavelengths = np.array(data_coarse.iloc[:, first_wavelength_coarse:].columns, dtype=float)

# X and y for coarse
X_coarse = data_coarse.iloc[:, first_wavelength_coarse:].values
y_coarse = data_coarse[target].values

# X and y for fine
X_fine = data_fine.iloc[:, first_wavelength_fine:].values
y_fine = data_fine[target].values

# Model with specific number of components selected
pls_model_coarse = PLSRegression(n_components=components)
pls_model_fine = PLSRegression(n_components=components)

# Train the PLS models
pls_model_coarse.fit(X_coarse, y_coarse)
pls_model_fine.fit(X_fine, y_fine)

# Get regression coefficients
coefficients_coarse = pls_model_coarse.coef_.flatten()
coefficients_fine = pls_model_fine.coef_.flatten()

# Plot on the first subplot (coarse)
axes[0].plot(wavelengths, coefficients_coarse, label=f'Coarse Model all Feeds', linewidth=2, color='black')
# Plot on the second subplot (fine)
axes[1].plot(wavelengths, coefficients_fine, label=f'Fine Model Comp.) all Feeds', linewidth=2, color='black')

feedCounter = 1

for feed in feedGroups:
    data_coarse_train = data_coarse[~data_coarse["Fish_ID"].isin(feed)]
    data_fine_train = data_fine[~data_fine["Fish_ID"].isin(feed)]

    # X and y for coarse
    X_coarse = data_coarse_train.iloc[:, first_wavelength_coarse:].values
    y_coarse = data_coarse_train[target].values

    # X and y for fine
    X_fine = data_fine_train.iloc[:, first_wavelength_fine:].values
    y_fine = data_fine_train[target].values

    # Model with specific number of components selected
    pls_model_coarse = PLSRegression(n_components=components)
    pls_model_fine = PLSRegression(n_components=components)

    # Train the PLS models
    pls_model_coarse.fit(X_coarse, y_coarse)
    pls_model_fine.fit(X_fine, y_fine)

    # Get regression coefficients
    coefficients_coarse = pls_model_coarse.coef_.flatten()
    coefficients_fine = pls_model_fine.coef_.flatten()

    ## Test the models
    data_coarse_test = data_coarse[data_coarse["Fish_ID"].isin(feed)]
    # X and y for test
    X_test = data_coarse_test.iloc[:, first_wavelength_coarse:].values
    y_test = data_coarse_test[target].values
    # predict
    y_predicted_coarse = pls_model_coarse.predict(X_test)
    y_predicted_fine = pls_model_fine.predict(X_test)
    # r2 score uncorrected
    r2_coarse = r2_score(y_test, y_predicted_coarse)
    r2_fine = r2_score(y_test, y_predicted_fine)
    # mean absolute error
    mae_coarse = mean_absolute_error(y_test, y_predicted_coarse)
    mae_fine = mean_absolute_error(y_test, y_predicted_fine)

    # Plot on the first subplot (coarse)
    axes[0].plot(wavelengths, coefficients_coarse, label=f'Coarse Model (R2: {r2_coarse}, MAE{mae_coarse}) without Feed {feedCounter}', linewidth=2, alpha=0.6)
    # Plot on the second subplot (fine)
    axes[1].plot(wavelengths, coefficients_fine, label=f'Fine Model (R2: {r2_fine}, MAE{mae_fine}) without Feed {feedCounter}', linewidth=2, alpha=0.6)

    feedCounter += 1

# Add horizontal line at y=0
for ax in axes:
    ax.axhline(0, color='gray', linestyle='--', linewidth=0.7)
    ax.grid(alpha=0.5)

# Customize the first subplot (coarse)
axes[0].set_title(f'Set {datasetChoice} PLS Regression Coefficients ({components} Comp.) for {target} (Coarse)', fontsize=14)
axes[0].set_ylabel('Regression Coefficients', fontsize=12)
axes[0].legend(fontsize=10)

# Customize the second subplot (fine)
axes[1].set_title(f'Set {datasetChoice} PLS Regression Coefficients ({components} Comp.) for {target} (Fine)', fontsize=14)
axes[1].set_xlabel('Wavelength (nm)', fontsize=12)
axes[1].set_ylabel('Regression Coefficients', fontsize=12)
axes[1].legend(fontsize=10)

# Adjust layout and save the plot
plt.tight_layout()
plt.savefig(f"../plots/regression/plot_regression_coefficients_{target}_{datasetChoice}_{components}.png", dpi=1000)

# Show the plots
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
