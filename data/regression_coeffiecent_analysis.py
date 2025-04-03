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
testFeed = 1
# positions = ["H","T","F1","NQC1","NQC2"]
# position_selection = positions[3]
#samples = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17", "S18"]

### Load the data

# median coarse
file_path = f'exported_data_coarse_median_dataset{datasetChoice}.csv'
data_coarse = pd.read_csv(file_path)
#data_coarse = data_coarse[data_coarse["Position"] == position_selection]
# Define where the first wavlength is located
first_wavelength_coarse = gcLength
print("953...=" + data_coarse.columns[first_wavelength_coarse])

# all replicate fine
file_path = f'exported_data_fine_dataset{datasetChoice}.csv'
data_fine = pd.read_csv(file_path)
#data_fine = data_fine[data_fine["Position"] == position_selection]
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

measured_calibration = []
predicted_calibration = []
measured_test = []
predicted_test = []

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
    r2_coarse_u = round(r2_score(y_test, y_predicted_coarse),2)
    r2_fine_u = round(r2_score(y_test, y_predicted_fine),2)
    # mean absolute error uncorrected
    mae_coarse_u = round(mean_absolute_error(y_test, y_predicted_coarse),2)
    mae_fine_u = round(mean_absolute_error(y_test, y_predicted_fine),2)
    # calculate means
    mean_measured_coarse = np.mean(y_test)
    mean_measured_fine = np.mean(y_test)
    mean_predicted_coarse = np.mean(y_predicted_coarse)
    mean_predicted_fine = np.mean(y_predicted_fine)
    # slope calculation
    slope_coarse = np.sum((y_predicted_coarse - mean_predicted_coarse) * (y_test - mean_measured_coarse)) / np.sum((y_predicted_coarse - mean_predicted_coarse) ** 2)
    slope_fine = np.sum((y_predicted_fine - mean_predicted_fine) * (y_test - mean_measured_fine)) / np.sum((y_predicted_fine - mean_predicted_fine) ** 2)
    # bias calculation
    bias_coarse = mean_measured_coarse - slope_coarse * mean_predicted_coarse
    bias_fine = mean_measured_fine - slope_fine * mean_predicted_fine
    #correction
    y_predicted_coarse_c = y_predicted_coarse * slope_coarse + bias_coarse
    y_predicted_fine_c = y_predicted_coarse * slope_fine + bias_fine
    # r2 score corrected
    r2_coarse_c = round(r2_score(y_test, y_predicted_coarse_c),2)
    r2_fine_c = round(r2_score(y_test, y_predicted_fine_c),2)
    # mean absolute error corrected
    mae_coarse_c = round(mean_absolute_error(y_test, y_predicted_coarse_c),2)
    mae_fine_c = round(mean_absolute_error(y_test, y_predicted_fine_c),2)


    # Plot on the first subplot (coarse) (R2: {r2_coarse_u}(C:{r2_coarse_c}), MAE{mae_coarse_u}(C:{mae_coarse_c}))
    axes[0].plot(wavelengths, coefficients_coarse, label=f'Coarse Model without Feed {feedCounter}', linewidth=2, alpha=0.6)
    # Plot on the second subplot (fine)(R2: {r2_fine_u}(C:{r2_fine_c}), MAE{mae_fine_u}(C:{mae_fine_c}))
    axes[1].plot(wavelengths, coefficients_fine, label=f'Fine Model without Feed {feedCounter}', linewidth=2, alpha=0.6)

    if feedCounter == testFeed:
        measured_calibration = y_fine
        predicted_calibration = pls_model_fine.predict(X_fine)
        measured_test = y_test
        predicted_test = y_predicted_fine

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
set_max = 28
set_min = -0.1
# Plot
plt.figure(figsize=(8, 6))
# Calibration set
plt.scatter(measured_calibration, predicted_calibration, color='grey', label='Calibration Set')
# Test set
plt.scatter(measured_test, predicted_test, color='blue', label='Test Set')
# Add 1:1 line for reference
plt.plot([set_min, set_max], [set_min, set_max], color='black', linestyle='--', label='1:1 Line')

# Labels and title
plt.xlabel(f'Measured {target} Concentration')
plt.ylabel(f'Predicted {target} Concentration')
plt.title(f'{target} Concentrations / Components: {components} / Set {datasetChoice} / Indep. Feed: {testFeed}') #  / Pos. {position_selection}
plt.legend()

# Adjust plot limits (if necessary)
plt.xlim(set_min, set_max)
plt.ylim(set_min, set_max)

# Show plot
plt.grid(True)
plt.show()
