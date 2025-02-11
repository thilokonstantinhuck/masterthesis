from config.generalParameters import gcLength
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cross_decomposition import PLSRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

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
# Components range to graph and calculate
components = 4
datasetChoice = 3
samples = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17", "S18"]
feedGroups = [["S01", "S02", "S03", "S04", "S05", "S06"],
              ["S07", "S08", "S09", "S10", "S11", "S12"],
              ["S13", "S14", "S15", "S16", "S17", "S18"]]
feedTest = 2
### Load the data

# median coarse
file_path = f'../exported_data_coarse_median_dataset{datasetChoice}.csv'
data_coarse = pd.read_csv(file_path)
mean = round(data_coarse[target].mean(), 3)
std = round(data_coarse[target].std(), 3)
r2_score_list_test_coarse = []
r2_score_list_train_coarse = []
mae_list_test_coarse = []
mae_list_train_coarse = []
mse_list_test_coarse = []
mse_list_train_coarse = []
bias_list_test_coarse = []
r2_score_list_test_coarse_bias_corrected = []
# Define where the first wavlength is located
first_wavelength_coarse = gcLength
print(data_coarse.columns[first_wavelength_coarse])

# all replicate fine
file_path = f'../exported_data_fine_dataset{datasetChoice}.csv'
data_fine = pd.read_csv(file_path)
r2_score_list_test_fine = []
r2_score_list_train_fine = []
mae_list_test_fine = []
mae_list_train_fine = []
mse_list_test_fine = []
mse_list_train_fine = []
bias_list_test_fine = []
r2_score_list_test_fine_bias_corrected = []
# Define where the first wavlength is located
first_wavelength_fine = first_wavelength_coarse+4
print(data_fine.columns[first_wavelength_fine])

# Model with specific number of components selected
pls_model = PLSRegression(n_components=components)

predictedTest = []
predictedTrain = []
actualTest = []
actualTrain = []

train_X = data_fine[~(data_fine["Fish_ID"].isin(feedGroups[feedTest]))].iloc[:, first_wavelength_fine:].values
test_X = data_coarse[(data_coarse["Fish_ID"].isin(feedGroups[feedTest]))].iloc[:, first_wavelength_coarse:].values
train_y = data_fine[~(data_fine["Fish_ID"].isin(feedGroups[feedTest]))][target].values
test_y = data_coarse[(data_coarse["Fish_ID"].isin(feedGroups[feedTest]))][target].values

# Train the PLS model on the train set
pls_model.fit(train_X, train_y)

# Predict on both
y_pred_train = pls_model.predict(train_X)
y_pred_test = pls_model.predict(test_X)

predictedTrain.extend(y_pred_train.flatten())  # Append the predicted values
actualTrain.extend(train_y.flatten())  # Append the actual values

predictedTest.extend(y_pred_test.flatten())  # Append the predicted values
actualTest.extend(test_y.flatten())  # Append the actual values

##train
predictedTrain = np.array(predictedTrain)
actualTrain = np.array(actualTrain)

##test
predictedTest = np.array(predictedTest)
actualTest = np.array(actualTest)


# Define manual limits
x_min, x_max = 0, 30  # Adjust these as needed
y_min, y_max = 0, 30 # Adjust these as needed

# Plot the actual and predicted against each other, train in blue test in red
plt.figure(figsize=(6, 6))

# Training data (blue)
plt.scatter(actualTrain, predictedTrain, color='blue', label='Train')

# Test data (red)
plt.scatter(actualTest, predictedTest, color='red', label='Test')

# Reference line (perfect prediction)
plt.plot([x_min, x_max], [y_min, y_max], linestyle="--", color="black", label="Perfect Prediction")

# Set axis limits
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)

plt.xlabel("Actual Lipid %")
plt.ylabel("Predicted Lipid %")
plt.legend()
plt.title("Actual vs Predicted Values for Fine model with 4 LV with R2 = 0.83")
plt.show()