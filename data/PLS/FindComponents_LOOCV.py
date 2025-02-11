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

targetChoice = 9
target = list_targets[targetChoice]
# Components range to graph and calculate
compFirst = 1
compLast = 25
datasetChoice = 3

samples = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17", "S18"]
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

##Coarse
for i in range(compFirst, compLast + 1):
    print(f"{i}_coarse")

    # Model with specific number of components selected
    pls_model = PLSRegression(n_components=i)

    predictedTest = []
    predictedTrain = []
    actualTest = []
    actualTrain = []

    for sample in samples:
        train_X = data_coarse[data_coarse["Fish_ID"] != sample].iloc[:, first_wavelength_coarse:].values
        test_X = data_coarse[data_coarse["Fish_ID"] == sample].iloc[:, first_wavelength_coarse:].values
        train_y = data_coarse[data_coarse["Fish_ID"] != sample][target].values
        test_y = data_coarse[data_coarse["Fish_ID"] == sample][target].values

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

    # Train Score Calculation
    r2_score_list_train_coarse.append(r2_score(actualTrain, predictedTrain))
    mae_list_train_coarse.append(mean_absolute_error(actualTrain, predictedTrain))
    mse_list_train_coarse.append(mean_squared_error(actualTrain, predictedTrain))

    ##test
    predictedTest = np.array(predictedTest)
    actualTest = np.array(actualTest)

    # R2 Score Calculation
    r2_score_list_test_coarse.append(r2_score(actualTest, predictedTest))
    mae_list_test_coarse.append(mean_absolute_error(actualTest, predictedTest))
    mse_list_test_coarse.append(mean_squared_error(actualTest, predictedTest))

    # Bias Calculation (Mean Error)
    bias_test = np.mean(predictedTest) - np.mean(actualTrain)
    bias_list_test_coarse.append(bias_test)

    # Bias corrected R2 Score Calculation
    r2_bias_corrected = r2_score(actualTest, predictedTest-bias_test)
    r2_score_list_test_coarse_bias_corrected.append(r2_bias_corrected)

##Fine
for i in range(compFirst, compLast + 1):
    print(f"{i}_fine")

    # Model with specific number of components selected
    pls_model = PLSRegression(n_components=i)

    predictedTest = []
    predictedTrain = []
    actualTest = []
    actualTrain = []

    for sample in samples:
        train_X = data_fine[data_fine["Fish_ID"] != sample].iloc[:, first_wavelength_fine:].values
        test_X = data_coarse[data_coarse["Fish_ID"] == sample].iloc[:, first_wavelength_coarse:].values
        train_y = data_fine[data_fine["Fish_ID"] != sample][target].values
        test_y = data_coarse[data_coarse["Fish_ID"] == sample][target].values

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

    # Train Score Calculation
    r2_score_list_train_fine.append(r2_score(actualTrain, predictedTrain))
    mae_list_train_fine.append(mean_absolute_error(actualTrain, predictedTrain))
    mse_list_train_fine.append(mean_squared_error(actualTrain, predictedTrain))

    ##test
    predictedTest = np.array(predictedTest)
    actualTest = np.array(actualTest)

    # R2 Score Calculation
    r2_score_list_test_fine.append(r2_score(actualTest, predictedTest))
    mae_list_test_fine.append(mean_absolute_error(actualTest, predictedTest))
    mse_list_test_fine.append(mean_squared_error(actualTest, predictedTest))

    # Bias Calculation (Mean Error)
    bias_test = np.mean(predictedTest) - np.mean(actualTrain)
    bias_list_test_fine.append(bias_test)

    # Bias corrected R2 Score Calculation
    r2_bias_corrected = r2_score(actualTest, (predictedTest - bias_test))
    r2_score_list_test_fine_bias_corrected.append(r2_bias_corrected)

# Plot the R² scores and Bias for each number of components
plt.figure(figsize=(12, 12))

# # MAE
# plt.subplot(4, 1, 1)
# plt.plot(range(compFirst, compLast + 1), mae_list_train_coarse, marker='o', linestyle='-', label="Train Coarse", color="blue")
# plt.plot(range(compFirst, compLast + 1), mae_list_test_coarse, marker='o', linestyle='-', label="Test Coarse", color="red")
# plt.plot(range(compFirst, compLast + 1), mae_list_train_fine, marker='x', linestyle='-', label="Train Fine", color="skyblue")
# plt.plot(range(compFirst, compLast + 1), mae_list_test_fine, marker='x', linestyle='-', label="Test Fine", color="salmon")
# plt.xlabel('Number of Components')
# plt.ylabel('Mean Absolute Error')
# plt.title(f'MAE vs Components for {target} (mean:{mean} std:{std} in Dataset {datasetChoice} using LOOCV')
# plt.xticks(range(compFirst, compLast + 1))  # Ensure each component is marked on the x-axis
# plt.grid(True)
# plt.legend()

# MSE
plt.subplot(4, 1, 1)
plt.plot(range(compFirst, compLast + 1), mse_list_train_coarse, marker='o', linestyle='-', label="Train Coarse", color="blue")
plt.plot(range(compFirst, compLast + 1), mse_list_test_coarse, marker='o', linestyle='-', label="Test Coarse", color="red")
plt.plot(range(compFirst, compLast + 1), mse_list_train_fine, marker='x', linestyle='-', label="Train Fine", color="skyblue")
plt.plot(range(compFirst, compLast + 1), mse_list_test_fine, marker='x', linestyle='-', label="Test Fine", color="salmon")
plt.xlabel('Number of Components')
plt.ylabel('Mean Squared Error')
plt.title(f'MSE vs Components for {target} (mean:{mean} std:{std} in Dataset {datasetChoice} using LOOCV')
plt.xticks(range(compFirst, compLast + 1))  # Ensure each component is marked on the x-axis
plt.grid(True)
plt.legend()


# R2 Scores
plt.subplot(4, 1, 2)
plt.plot(range(compFirst, compLast + 1), r2_score_list_train_coarse, marker='o', linestyle='-', label="Train Coarse", color="blue")
plt.plot(range(compFirst, compLast + 1), r2_score_list_test_coarse, marker='o', linestyle='-', label="Test Coarse", color="red")
plt.plot(range(compFirst, compLast + 1), r2_score_list_train_fine, marker='x', linestyle='-', label="Train Fine", color="skyblue")
plt.plot(range(compFirst, compLast + 1), r2_score_list_test_fine, marker='x', linestyle='-', label="Test Fine", color="salmon")
plt.xlabel('Number of Components')
plt.ylabel('R² Score')
plt.title(f'R² Score vs Components in PLS Model for {target} in Dataset {datasetChoice} using LOOCV')
plt.xticks(range(compFirst, compLast + 1))  # Ensure each component is marked on the x-axis
plt.grid(True)
plt.ylim(0, 1)
plt.yticks(np.arange(0, 1, 0.1))
plt.legend()

# R2 Scores corrected
plt.subplot(4, 1, 3)
plt.plot(range(compFirst, compLast + 1), r2_score_list_train_coarse, marker='o', linestyle='-', label="Train Coarse", color="blue")
plt.plot(range(compFirst, compLast + 1), r2_score_list_test_coarse_bias_corrected, marker='o', linestyle='-', label="Test Coarse", color="red")
plt.plot(range(compFirst, compLast + 1), r2_score_list_train_fine, marker='x', linestyle='-', label="Train Fine", color="skyblue")
plt.plot(range(compFirst, compLast + 1), r2_score_list_test_fine_bias_corrected, marker='x', linestyle='-', label="Test Fine", color="salmon")
plt.xlabel('Number of Components')
plt.ylabel('R² Score')
plt.title(f'corrected R² Score vs Components in PLS Model for {target} in Dataset {datasetChoice} using LOOCV')
plt.xticks(range(compFirst, compLast + 1))  # Ensure each component is marked on the x-axis
plt.grid(True)
plt.ylim(0, 1)
plt.yticks(np.arange(0, 1, 0.1))
plt.legend()

# Bias
plt.subplot(4, 1, 4)
plt.plot(range(compFirst, compLast + 1), bias_list_test_coarse, marker='o', linestyle='-', label="Test Coarse", color="red")
plt.plot(range(compFirst, compLast + 1), bias_list_test_fine, marker='x', linestyle='-', label="Test Fine", color="salmon")
plt.axhline(y=0, linestyle='-', color='green')
plt.xlabel('Number of Components')
plt.ylabel('Bias (Mean Error)')
plt.title(f'Bias vs Components in PLS Model for {target} in Dataset {datasetChoice} using LOOCV')
plt.xticks(range(compFirst, compLast + 1))  # Ensure each component is marked on the x-axis
plt.grid(True)
plt.legend()



plt.tight_layout()
plt.savefig(f"../../plots/crossvalidation/plot_modelR2_bias_{targetChoice}_{datasetChoice}.png", dpi=1000)
plt.show()
