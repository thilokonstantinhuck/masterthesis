import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cross_decomposition import PLSRegression
from sklearn.metrics import r2_score

### Settings
list_targets = ['Lipid_%',
                'Saturated', #1
                'Unsaturated', #2
                'Monounsaturated', #3
                'Polyunsaturated', #4
                'Omega9', #5
                'Omega6', #6
                'Omega3', #7
                'HumanOmega3', #8
                'EPAandDHA', #9
                'C4:0', 'C6:0', 'C8:0', 'C10:0', 'C11:0', 'C12:0', #15
                'C14:0', 'C14:1n5', 'C15:0', 'C15:1n5', 'C16:0', #20
                'C16:1n7', 'C17:0', 'C17:1n7', 'C18:0', 'C18:1n9c', #25
                'C18:1n7', 'C18:2n6c', 'C18:2n6t', 'C18:3n3c', 'C18:3n6c', #30
                'C20:0', 'C20:1n9', 'C20:2n6', 'C20:3n3', 'C20:3n6', #35
                'C20:4n6', 'C20:5n3', 'C21:0', 'C22:0', 'C22:1n9', #40
                'C22:2n6', 'C22:5n3', 'C22:6n3', 'C23:0', 'C24:0', 'C24:1n9'] #46
target = list_targets[25] # 46 max
# Components range to graph and calculate
compFirst = 1
compLast = 25
# List of sample names
datasetChoice = 3
samples = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17", "S18"]

### Load the data

# median coarse
file_path = f'exported_data_coarse_median_dataset{datasetChoice}.csv'
data_coarse = pd.read_csv(file_path)
r2_score_list_test_coarse = []
r2_score_list_train_coarse = []
# Define where the first wavlength is located
first_wavelength_coarse = 49
print(data_coarse.columns[first_wavelength_coarse])

# all replicate fine
file_path = f'exported_data_fine_dataset{datasetChoice}.csv'
data_fine = pd.read_csv(file_path)
r2_score_list_test_fine = []
r2_score_list_train_fine = []
# Define where the first wavlength is located
first_wavelength_fine = 53
print(data_fine.columns[first_wavelength_fine])

for i in range(compFirst, compLast + 1):

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

    predictedTest = np.array(predictedTest)
    actualTest = np.array(actualTest)

    r2test = r2_score(actualTest, predictedTest)
    r2_score_list_test_coarse.append(r2test)

    predictedTrain = np.array(predictedTrain)
    actualTrain = np.array(actualTrain)

    r2train = r2_score(actualTrain, predictedTrain)
    r2_score_list_train_coarse.append(r2train)

    print(f"R² SCORE coarse for {i} Components: {r2test}")

for i in range(compFirst, compLast + 1):

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

    predictedTest = np.array(predictedTest)
    actualTest = np.array(actualTest)

    r2test = r2_score(actualTest, predictedTest)
    r2_score_list_test_fine.append(r2test)

    predictedTrain = np.array(predictedTrain)
    actualTrain = np.array(actualTrain)

    r2train = r2_score(actualTrain, predictedTrain)
    r2_score_list_train_fine.append(r2train)

    print(f"R² SCORE fine for {i} Components: {r2test}")

# Plot the R² scores for each number of components
plt.figure(figsize=(10, 6))
plt.plot(range(compFirst, compLast + 1), r2_score_list_test_coarse, marker='o', linestyle='-', color='b', label="Test Coarse")
plt.plot(range(compFirst, compLast + 1), r2_score_list_train_coarse, marker='o', linestyle='-', color='r', label="Train Coarse")
plt.plot(range(compFirst, compLast + 1), r2_score_list_test_fine, marker='x', linestyle='-', color='g', label="Test Fine")
plt.plot(range(compFirst, compLast + 1), r2_score_list_train_fine, marker='x', linestyle='-', color='y', label="Train Fine")
plt.xlabel('Number of Components')
plt.ylabel('R² Score')
plt.title(f'R² Score vs Components in PLS Model for {target} in Dataset {datasetChoice} using LOOCV')
plt.xticks(range(compFirst, compLast + 1))  # Ensure each component is marked on the x-axis
plt.grid(True)
plt.ylim(0,1)
plt.yticks(np.arange(0, 1.1, 0.1))
plt.legend()
plt.savefig(f"../plots/{datasetChoice}_plot_{target}_modelR2.png", dpi=1000)
plt.show()
