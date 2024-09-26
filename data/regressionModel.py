import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score

# Load the data
file_path = 'dataEdited.csv'
data = pd.read_csv(file_path)

# Data Preprocessing
# Select hyperspectral data (from the 5th column onward) and target variable (C20:5n3)
X = data.iloc[:, 4:].values  # Hyperspectral data
y = data['C20:5n3'].values   # Target variable

# Train-test split (90% train, 10% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Implementing Lasso Regression with Cross-Validation
lasso_model = Ridge(alpha=0.001)  # You can tune alpha based on your needs
kf = KFold(n_splits=5, shuffle=True, random_state=44)

# Perform cross-validation
cv_scores = cross_val_score(lasso_model, X, y, cv=kf, scoring='neg_mean_squared_error')
mean_cv_mse = -np.mean(cv_scores)
std_cv_mse = np.std(cv_scores)

print(f"Mean CV MSE: {mean_cv_mse}, Std CV MSE: {std_cv_mse}")

# Train the Lasso model on the full training set
lasso_model.fit(X_train, y_train)

# Make predictions on the test set
y_pred_lasso = lasso_model.predict(X_test)

# Evaluate the performance on the test set
mse_test_lasso = mean_squared_error(y_test, y_pred_lasso)
r2_test_lasso = r2_score(y_test, y_pred_lasso)

print(f"Test MSE (Lasso): {mse_test_lasso}")
print(f"Test R^2 (Lasso): {r2_test_lasso}")

# Plotting the results
# 1. Predicted vs True values (Test set)
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred_lasso, alpha=0.7, color='b')
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', lw=2)
plt.xlabel("True Values (C20:5n3)")
plt.ylabel("Predicted Values (C20:5n3)")
plt.title("Predicted vs True Values (Test Set)")
plt.show()

# 2. Residuals Plot (Test set)
residuals = y_test - y_pred_lasso
plt.figure(figsize=(8, 6))
plt.scatter(y_pred_lasso, residuals, alpha=0.7, color='purple')
plt.axhline(0, color='red', linestyle='--')
plt.xlabel("Predicted Values")
plt.ylabel("Residuals")
plt.title("Residuals Plot (Test Set)")
plt.show()
