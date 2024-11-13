import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.cross_decomposition import PLSRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler
from scipy import stats

# Load the data
file_path = 'exported_data_all.csv'
data = pd.read_csv(file_path)

#select one feed group
samples = ["S01", "S02", "S03", "S04", "S05", "S06"]
# samples = ["S07", "S08", "S09", "S10", "S11", "S12"]
# samples = ["S13", "S14", "S15", "S16", "S17", "S18"]
data = data[data['Fish ID'].isin(samples)]

# select number of components
n_components=3
# Define the sample name to split off for the test set
sample_name = 'S01'
# Define the target name for the modelling
target = "EPAandDHA"
# target = "Lipid_%"
# Define where the first wavlength is located
firstWL = 46
print(data.columns[firstWL])

# Split off the test set where Fish ID is equal to the sample name
test_set = data[data['Fish ID'] == sample_name]

# The remaining data will be used for training and validation
train_val_set = data[data['Fish ID'] != sample_name]

# Extract the hyperspectral data (from 5th column onward) and target variable (C20:5n3)
X = train_val_set.iloc[:, firstWL:].values  # Hyperspectral data for training and validation
y = train_val_set[target].values  # Target variable for training and validation

X_test = test_set.iloc[:, firstWL:].values  # Hyperspectral data for test set
y_test = test_set[target].values  # Target variable for test set

# Train-test split (90% train, 10% validation)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.1, random_state=42)

# Model with specific number of components selected
pls_model = PLSRegression(n_components=n_components)  # Adjust n_components as needed

# Perform cross-validation for PLS using R2 scoring
kf = KFold(n_splits=5, shuffle=True, random_state=44)
cv_scores_pls = cross_val_score(pls_model, X_train, y_train, cv=kf, scoring='r2')
mean_cv_r2_pls = np.mean(cv_scores_pls)
std_cv_r2_pls = np.std(cv_scores_pls)

print(f"Mean CV R^2 (PLS): {mean_cv_r2_pls}, Std CV R^2 (PLS): {std_cv_r2_pls}")

# Train the PLS model on the training set
pls_model.fit(X_train, y_train)

# Make predictions on the validation set using PLS
y_pred_val = pls_model.predict(X_val)

# Evaluate the performance on the validation set for PLS
mse_val_pls = mean_squared_error(y_val, y_pred_val)
r2_val_pls = r2_score(y_val, y_pred_val)
mae_val_pls = mean_absolute_error(y_val, y_pred_val)

print(f"Validation MSE (PLS): {mse_val_pls}")
print(f"Validation R^2 (PLS): {r2_val_pls}")
print(f"Validation MAE (PLS): {mae_val_pls}")

# Retrain the PLS model on the train/val set
pls_model.fit(X, y)

# Save the trained PLS model
# model_filename = 'pls_model_EPADHA.pkl'
model_filename = 'pls_model.pkl'
with open(model_filename, 'wb') as file:
    pickle.dump(pls_model, file)

# Make predictions on the test set using PLS
y_pred_pls = pls_model.predict(X_test).flatten()

# Slope and bias correction
slope, intercept, r_value, p_value, std_err = stats.linregress(y_test, y_pred_pls)
y_pred_corrected = (y_pred_pls - intercept) / slope

# Split up test set into the different positions
positions = [
    ["T", "pink"],
    ["NQC1", "blue"],
    ["NQC2", "green"],
    ["H", "purple"],
    ["F2", "orange"]
]

# Residuals Plot (Before Correction)
residuals_pls = y_test - y_pred_pls
plt.figure(figsize=(8, 6))
plt.scatter(y_pred_pls, residuals_pls, alpha=0.7, color='orange')
plt.axhline(0, color='red', linestyle='--')
plt.xlabel("Predicted Values")
plt.ylabel("Residuals")
plt.title("Residuals Plot (Test Set) - PLS Regression (Before Correction)")
plt.show()

# Residuals Plot (After Correction)
residuals_corrected = y_test - y_pred_corrected
plt.figure(figsize=(8, 6))
plt.scatter(y_pred_corrected, residuals_corrected, alpha=0.7, color='green')
plt.axhline(0, color='red', linestyle='--')
plt.xlabel("Corrected Predicted Values")
plt.ylabel("Residuals")
plt.title("Residuals Plot (Test Set) - PLS Regression (After Correction)")
plt.show()

# Plotting the results for PLS with different Positions
plt.figure(figsize=(8, 6))
for position_code, color in positions:
    mask = test_set['Position'].str.contains(position_code)
    plt.scatter(y_test[mask], y_pred_corrected[mask], alpha=0.7, color=color, label=position_code)

plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', lw=2, label="Ideal Fit")
plt.xlabel(f"True Values ({target})")
plt.ylabel(f"Corrected Predicted Values ({target})")
plt.title("Predicted vs True Values (Test Set) - PLS Regression by Position (After Correction)")
plt.legend()
plt.show()

# Calculate and print R^2 score for the entire test set
r2_test_corrected = r2_score(y_test, y_pred_corrected)
print(f"R^2 for the entire test set (After Correction): {r2_test_corrected}")

# extract column names as wavelengths
wavelengths = train_val_set.columns[firstWL:].astype(float)  # Adjust this if necessary to match your data structure

# Plot regression coefficients
coefficients = pls_model.coef_.flatten()
plt.figure(figsize=(10, 6))
plt.plot(wavelengths, coefficients, marker='o', linestyle='-', color='b')
plt.fill_between(wavelengths, 0, coefficients, where=(coefficients >= 0), color='skyblue', alpha=0.5)
plt.fill_between(wavelengths, 0, coefficients, where=(coefficients < 0), color='lightcoral', alpha=0.5)
plt.xlabel("Wavelength")
plt.ylabel("Coefficient Value")
plt.title(f"PLS Regression Coefficients{n_components}")
plt.tight_layout()
plt.show()