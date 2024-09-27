import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.cross_decomposition import PLSRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.linear_model import LinearRegression

# Load the data
file_path = 'dataEdited.csv'
data = pd.read_csv(file_path)

# Define the sample name to split off for the test set
sample_name = 'S03'
position = "NQC1"

# Split off the test set where Fish ID is equal to the sample name "S06"
# test_set = data[(data['Fish ID'] == sample_name) & (data['Position'] == position)]
test_set = data[data['Fish ID'] == sample_name]

# The remaining data will be used for training and validation
# train_val_set = data[(data['Fish ID'] != sample_name) & (data['Position'] == position)]
train_val_set = data[data['Fish ID'] != sample_name]

# Extract the hyperspectral data (from 5th column onward) and target variable (C20:5n3)
X = train_val_set.iloc[:, 4:].values  # Hyperspectral data for training and validation
y = train_val_set['C20:5n3'].values  # Target variable for training and validation

X_test = test_set.iloc[:, 4:].values  # Hyperspectral data for test set
y_test = test_set['C20:5n3'].values  # Target variable for test set

# Train-test split (90% train, 10% test)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.1, random_state=42)

# Implementing PLS Regression with Cross-Validation
pls_model = PLSRegression(n_components=10)  # You can adjust n_components based on the data

kf = KFold(n_splits=5, shuffle=True, random_state=44)

# Perform cross-validation for PLS
cv_scores_pls = cross_val_score(pls_model, X, y, cv=kf, scoring='neg_mean_squared_error')
mean_cv_mse_pls = -np.mean(cv_scores_pls)
std_cv_mse_pls = np.std(cv_scores_pls)

print(f"Mean CV MSE (PLS): {mean_cv_mse_pls}, Std CV MSE (PLS): {std_cv_mse_pls}")

# Train the PLS model on the full training set
pls_model.fit(X, y)

# Make predictions on the test set using PLS
y_pred_pls = pls_model.predict(X_test).ravel()

# Evaluate the performance on the test set for PLS (Before Slope and Bias Correction)
mse_test_pls = mean_squared_error(y_test, y_pred_pls)
r2_test_pls = r2_score(y_test, y_pred_pls)
mae_test_pls = mean_absolute_error(y_test, y_pred_pls)

print(f"Test MSE (PLS): {mse_test_pls}")
print(f"Test R^2 (PLS): {r2_test_pls}")
print(f"Test MAE (PLS): {mae_test_pls}")

# Slope and Bias Correction using Linear Regression
linear_model = LinearRegression()

# Fit the linear regression model using predicted values to correct slope and bias
linear_model.fit(y_pred_pls.reshape(-1, 1), y_test)

# Extract slope (coefficient) and bias (intercept)
slope = linear_model.coef_[0]
bias = linear_model.intercept_

print(f"Slope (correction factor): {slope}")
print(f"Bias (intercept): {bias}")

# Apply the slope and bias correction
y_pred_corrected = slope * y_pred_pls + bias

# Evaluate the corrected predictions
mse_corrected = mean_squared_error(y_test, y_pred_corrected)
r2_corrected = r2_score(y_test, y_pred_corrected)
mae_corrected = mean_absolute_error(y_test, y_pred_corrected)

print(f"Corrected Test MSE: {mse_corrected}")
print(f"Corrected Test R^2: {r2_corrected}")
print(f"Corrected Test MAE: {mae_corrected}")

# Plotting the results for PLS (before and after correction)
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred_pls, alpha=0.7, color='blue', label="Original Predictions")
plt.scatter(y_test, y_pred_corrected, alpha=0.7, color='green', label="Corrected Predictions")
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', lw=2, label="Ideal Fit")
plt.xlabel("True Values (C20:5n3)")
plt.ylabel("Predicted Values (C20:5n3)")
plt.title("Predicted vs True Values (Test Set) - PLS (with Slope and Bias Correction)")
plt.legend()
plt.show()

# Residuals Plot (Corrected)
residuals_corrected = y_test - y_pred_corrected
plt.figure(figsize=(8, 6))
plt.scatter(y_pred_corrected, residuals_corrected, alpha=0.7, color='orange')
plt.axhline(0, color='red', linestyle='--')
plt.xlabel("Corrected Predicted Values")
plt.ylabel("Residuals")
plt.title("Residuals Plot (Test Set) - PLS (Corrected)")
plt.show()

# Assuming the 5th column onward are the hyperspectral data columns (wavelengths), extract those column names as wavelengths
wavelengths = train_val_set.columns[4:]  # Adjust this if necessary to match your data structure

# Get the coefficients from the PLS model
pls_coefficients = pls_model.coef_.ravel()

# Plot the coefficients for PLS
plt.figure(figsize=(10, 6))
plt.plot(wavelengths, pls_coefficients, label="PLS Coefficients", color='blue', marker='o', alpha=0.7)
plt.xlabel("Wavelengths")
plt.ylabel("Regression Coefficients")
plt.title("PLS Regression Coefficients")
plt.xticks(rotation=90)  # Rotate x-axis labels if wavelengths are long
plt.legend()
plt.tight_layout()
plt.show()
