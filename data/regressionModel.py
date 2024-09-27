import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.linear_model import Ridge, Lasso
from sklearn.metrics import mean_squared_error, r2_score

# Load the data
file_path = 'dataEdited.csv'
data = pd.read_csv(file_path)

# Define the sample name to split off for the test set
sample_name = 'S06'

# Split off the test set where Fish ID is equal to the sample name "S08"
test_set = data[data['Fish ID'] == sample_name]

# The remaining data will be used for training and validation
train_val_set = data[data['Fish ID'] != sample_name]

# Extract the hyperspectral data (from 5th column onward) and target variable (C20:5n3)
X = train_val_set.iloc[:, 4:].values            # Hyperspectral data for training and validation
y = train_val_set['C20:5n3'].values             # Target variable for training and validation

X_test = test_set.iloc[:, 4:].values            # Hyperspectral data for test set
y_test = test_set['C20:5n3'].values             # Target variable for test set

# Train-test split (90% train, 10% test)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.1, random_state=42)

# Implementing Ridge Regression with Cross-Validation
ridge_model = Ridge(alpha=0.001)  # You can tune alpha based on your needs
lasso_model = Lasso(alpha=0.01)  # You can also tune alpha based on your needs

kf = KFold(n_splits=5, shuffle=True, random_state=44)

# Perform cross-validation for Ridge
cv_scores_ridge = cross_val_score(ridge_model, X, y, cv=kf, scoring='neg_mean_squared_error')
mean_cv_mse_ridge = -np.mean(cv_scores_ridge)
std_cv_mse_ridge = np.std(cv_scores_ridge)

print(f"Mean CV MSE (Ridge): {mean_cv_mse_ridge}, Std CV MSE (Ridge): {std_cv_mse_ridge}")

# Perform cross-validation for Lasso
cv_scores_lasso = cross_val_score(lasso_model, X, y, cv=kf, scoring='neg_mean_squared_error')
mean_cv_mse_lasso = -np.mean(cv_scores_lasso)
std_cv_mse_lasso = np.std(cv_scores_lasso)

print(f"Mean CV MSE (Lasso): {mean_cv_mse_lasso}, Std CV MSE (Lasso): {std_cv_mse_lasso}")

# Train the Ridge model on the full training set
ridge_model.fit(X, y)

# Train the Lasso model on the full training set
lasso_model.fit(X, y)

# Make predictions on the test set using Ridge
y_pred_ridge = ridge_model.predict(X_test)

# Make predictions on the test set using Lasso
y_pred_lasso = lasso_model.predict(X_test)

# Evaluate the performance on the test set for Ridge
mse_test_ridge = mean_squared_error(y_test, y_pred_ridge)
r2_test_ridge = r2_score(y_test, y_pred_ridge)

# Evaluate the performance on the test set for Lasso
mse_test_lasso = mean_squared_error(y_test, y_pred_lasso)
r2_test_lasso = r2_score(y_test, y_pred_lasso)

print(f"Test MSE (Ridge): {mse_test_ridge}")
print(f"Test R^2 (Ridge): {r2_test_ridge}")

print(f"Test MSE (Lasso): {mse_test_lasso}")
print(f"Test R^2 (Lasso): {r2_test_lasso}")

# Plotting the results for Ridge
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred_ridge, alpha=0.7, color='b')
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', lw=2)
plt.xlabel("True Values (C20:5n3)")
plt.ylabel("Predicted Values (C20:5n3)")
plt.title("Predicted vs True Values (Test Set) - Ridge")
plt.show()

# Plotting the results for Lasso
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred_lasso, alpha=0.7, color='green')
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', lw=2)
plt.xlabel("True Values (C20:5n3)")
plt.ylabel("Predicted Values (C20:5n3)")
plt.title("Predicted vs True Values (Test Set) - Lasso")
plt.show()

# Residuals Plot (Ridge)
residuals_ridge = y_test - y_pred_ridge
plt.figure(figsize=(8, 6))
plt.scatter(y_pred_ridge, residuals_ridge, alpha=0.7, color='purple')
plt.axhline(0, color='red', linestyle='--')
plt.xlabel("Predicted Values")
plt.ylabel("Residuals")
plt.title("Residuals Plot (Test Set) - Ridge")
plt.show()

# Residuals Plot (Lasso)
residuals_lasso = y_test - y_pred_lasso
plt.figure(figsize=(8, 6))
plt.scatter(y_pred_lasso, residuals_lasso, alpha=0.7, color='orange')
plt.axhline(0, color='red', linestyle='--')
plt.xlabel("Predicted Values")
plt.ylabel("Residuals")
plt.title("Residuals Plot (Test Set) - Lasso")
plt.show()

# Assuming the 5th column onward are the hyperspectral data columns (wavelengths), extract those column names as wavelengths
wavelengths = train_val_set.columns[4:]  # Adjust this if necessary to match your data structure


# Get the coefficients from both Ridge and Lasso
ridge_coefficients = ridge_model.coef_
lasso_coefficients = lasso_model.coef_

# Plot the coefficients for Ridge and Lasso
plt.figure(figsize=(10, 6))
plt.plot(wavelengths, ridge_coefficients, label="Ridge Coefficients", color='blue', marker='o', alpha=0.7)
plt.plot(wavelengths, lasso_coefficients, label="Lasso Coefficients", color='green', marker='x', alpha=0.7)
plt.xlabel("Wavelengths")
plt.ylabel("Regression Coefficients")
plt.title("Ridge vs Lasso Regression Coefficients")
plt.xticks(rotation=90)  # Rotate x-axis labels if wavelengths are long
plt.legend()
plt.tight_layout()
plt.show()