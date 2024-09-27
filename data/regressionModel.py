import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score

# Load the data
file_path = 'dataEdited.csv'
data = pd.read_csv(file_path)

# Define the sample name to split off for the test set
sample_name = 'S03'

# Split off the test set where Fish ID is equal to the sample name "S08"
test_set = data[data['Fish ID'] == sample_name]

# The remaining data will be used for training and validation
train_val_set = data[data['Fish ID'] != sample_name]

# Extract the hyperspectral data (from 5th column onward) and target variable (C20:5n3)
X = train_val_set.iloc[:, 4:].values  # Hyperspectral data for training and validation
y = train_val_set['C20:5n3'].values   # Target variable for training and validation

X_test = test_set.iloc[:, 4:].values            # Hyperspectral data for test set
y_test = test_set['C20:5n3'].values             # Target variable for test set

# Train-test split (90% train, 10% test)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.1, random_state=42)

# Implementing Ridge Regression with Cross-Validation
ridge_model = Ridge(alpha=0.0001)  # You can tune alpha based on your needs
kf = KFold(n_splits=5, shuffle=True, random_state=44)

# Perform cross-validation
cv_scores = cross_val_score(ridge_model, X, y, cv=kf, scoring='neg_mean_squared_error')
mean_cv_mse = -np.mean(cv_scores)
std_cv_mse = np.std(cv_scores)

print(f"Mean CV MSE: {mean_cv_mse}, Std CV MSE: {std_cv_mse}")

# Train the Ridge model on the full training set
ridge_model.fit(X, y)

# Make predictions on the test set
y_pred_ridge = ridge_model.predict(X_test)

# Evaluate the performance on the test set
mse_test_ridge = mean_squared_error(y_test, y_pred_ridge)
r2_test_ridge = r2_score(y_test, y_pred_ridge)

print(f"Test MSE (Ridge): {mse_test_ridge}")
print(f"Test R^2 (Ridge): {r2_test_ridge}")

# Plotting the results
# 1. Predicted vs True values (Test set)
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred_ridge, alpha=0.7, color='b')
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', lw=2)
plt.xlabel("True Values (C20:5n3)")
plt.ylabel("Predicted Values (C20:5n3)")
plt.title("Predicted vs True Values (Test Set)")
plt.show()

# 2. Residuals Plot (Test set)
residuals = y_test - y_pred_ridge
plt.figure(figsize=(8, 6))
plt.scatter(y_pred_ridge, residuals, alpha=0.7, color='purple')
plt.axhline(0, color='red', linestyle='--')
plt.xlabel("Predicted Values")
plt.ylabel("Residuals")
plt.title("Residuals Plot (Test Set)")
plt.show()
