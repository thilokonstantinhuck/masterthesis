import spectral.io.envi as envi
import importlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cross_decomposition import PLSRegression
from sklearn.metrics import r2_score

### Settings
# target = "C20:1n9"
# target = "EPAandDHA"
target = "Lipid_%"
# Components range to graph and calculate
compFirst = 1
compLast = 25
# Define where the first wavlength is located
firstWL = 46
# List of sample names
datasetChoice = 3
samples = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17", "S18"]

### Load the data
# median coarse
file_path = f'exported_data_coarse_median_dataset{datasetChoice}.csv'
data = pd.read_csv(file_path)

r2_score_list_Test = []
r2_score_list_Train = []

for i in range(compFirst, compLast + 1):

    # Model with specific number of components selected
    pls_model = PLSRegression(n_components=i)

    predictedTest = []
    predictedTrain = []
    actualTest = []
    actualTrain = []

    for sample in samples:
        train_X = data[data["Fish ID"] != sample].iloc[:, firstWL:].values
        test_X = data[data["Fish ID"] == sample].iloc[:, firstWL:].values
        train_y = data[data["Fish ID"] != sample][target].values
        test_y = data[data["Fish ID"] == sample][target].values

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
    r2_score_list_Test.append(r2test)

    predictedTrain = np.array(predictedTrain)
    actualTrain = np.array(actualTrain)

    r2train = r2_score(actualTrain, predictedTrain)
    r2_score_list_Train.append(r2train)

    print(f"R² SCORE for {i} Components: {r2test}")

# Plot the R² scores for each number of components
plt.figure(figsize=(10, 6))
plt.plot(range(compFirst, compLast + 1), r2_score_list_Test, marker='o', linestyle='-', color='b', label="Test")
plt.plot(range(compFirst, compLast + 1), r2_score_list_Train, marker='o', linestyle='-', color='r', label="Train")
plt.xlabel('Number of Components')
plt.ylabel('R² Score')
plt.title(f'R² Score vs Components in PLS Model for {target} in Dataset {datasetChoice} using LOOCV')
plt.xticks(range(compFirst, compLast + 1))  # Ensure each component is marked on the x-axis
plt.grid(True)
plt.ylim(0,1)
plt.yticks(np.arange(0, 1.1, 0.1))
plt.legend()
plt.show()
