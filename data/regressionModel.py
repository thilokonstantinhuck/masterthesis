import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from scipy import stats

# Load the data
file_path = 'exported_data.csv'
data = pd.read_csv(file_path)
data = data[data['Fish ID'].isin(["S01", "S02", "S03", "S04", "S05", "S06"])]

# Define the sample name to split off for the test set
sample_name = 'S03'
# Define the target name for the modelling
target = "Lipid_%"

# Split off the test set where Fish ID is equal to the sample name
test_set = data[data['Fish ID'] == sample_name]

# The remaining data will be used for training and validation
train_val_set = data[data['Fish ID'] != sample_name]

# Extract the hyperspectral data (from 5th column onward) and target variable (C20:5n3)
X = train_val_set.iloc[:, 45:].values  # Hyperspectral data for training and validation
y = train_val_set[target].values  # Target variable for training and validation

X_test = test_set.iloc[:, 45:].values  # Hyperspectral data for test set
y_test = test_set[target].values  # Target variable for test set

# z-Score outlier removal per fish and sampling site
filtered_indices = []
for fish_id in train_val_set['Fish ID'].unique():
    fish_data = train_val_set[train_val_set['Fish ID'] == fish_id]
    for site in fish_data['Position'].unique():
        site_data = fish_data[fish_data['Position'] == site]
        X_site = site_data.iloc[:, 45:].values
        z_scores_site = np.abs(stats.zscore(X_site))
        worst_indices = np.argsort(np.max(z_scores_site, axis=1))[-15:]
        mask = np.ones(len(site_data), dtype=bool)
        mask[worst_indices] = False
        filtered_indices.extend(site_data[mask].index)

train_val_set_filtered = train_val_set.loc[filtered_indices]
X = train_val_set_filtered.iloc[:, 45:].values
y = train_val_set_filtered[target].values

# Train-test split (90% train, 10% validation)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.1, random_state=42)

# Implementing Ridge Regression with Cross-Validation
ridge_model = Ridge(alpha=1.0)  # Adjust alpha as needed

# Perform cross-validation for Ridge
kf = KFold(n_splits=5, shuffle=True, random_state=44)
cv_scores_ridge = cross_val_score(ridge_model, X_train, y_train, cv=kf, scoring='neg_mean_squared_error')
mean_cv_mse_ridge = -np.mean(cv_scores_ridge)
std_cv_mse_ridge = np.std(cv_scores_ridge)

print(f"Mean CV MSE (Ridge): {mean_cv_mse_ridge}, Std CV MSE (Ridge): {std_cv_mse_ridge}")

# Train the Ridge model on the training set
ridge_model.fit(X_train, y_train)

# Make predictions on the validation set using Ridge
y_pred_val = ridge_model.predict(X_val)

# Evaluate the performance on the validation set for Ridge
mse_val_ridge = mean_squared_error(y_val, y_pred_val)
r2_val_ridge = r2_score(y_val, y_pred_val)
mae_val_ridge = mean_absolute_error(y_val, y_pred_val)

print(f"Validation MSE (Ridge): {mse_val_ridge}")
print(f"Validation R^2 (Ridge): {r2_val_ridge}")
print(f"Validation MAE (Ridge): {mae_val_ridge}")

# Make predictions on the test set using Ridge
y_pred_ridge = ridge_model.predict(X_test)

# Evaluate the performance on the test set for Ridge
mse_test_ridge = mean_squared_error(y_test, y_pred_ridge)
r2_test_ridge = r2_score(y_test, y_pred_ridge)
mae_test_ridge = mean_absolute_error(y_test, y_pred_ridge)

print(f"Test MSE (Ridge): {mse_test_ridge}")
print(f"Test R^2 (Ridge): {r2_test_ridge}")
print(f"Test MAE (Ridge): {mae_test_ridge}")

# Plotting the results for Ridge
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred_ridge, alpha=0.7, color='blue', label="Ridge Predictions")
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', lw=2, label="Ideal Fit")
plt.xlabel(f"True Values ({target})")
plt.ylabel(f"Predicted Values ({target})")
plt.title("Predicted vs True Values (Test Set) - Ridge Regression")
plt.legend()
plt.show()

# Residuals Plot
residuals_ridge = y_test - y_pred_ridge
plt.figure(figsize=(8, 6))
plt.scatter(y_pred_ridge, residuals_ridge, alpha=0.7, color='orange')
plt.axhline(0, color='red', linestyle='--')
plt.xlabel("Predicted Values")
plt.ylabel("Residuals")
plt.title("Residuals Plot (Test Set) - Ridge Regression")
plt.show()