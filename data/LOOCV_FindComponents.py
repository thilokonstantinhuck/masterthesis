import spectral.io.envi as envi
import importlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cross_decomposition import PLSRegression
from sklearn.metrics import r2_score

### Settings
target = "C18:2n6c"
# target = "Lipid_%"
# Components range to graph and calculate
compFirst = 1
compLast = 25
# Define where the first wavlength is located
firstWL = 46
# List of sample names
samples = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17", "S18"]

### Load the data
# median coarse
file_path = 'exported_data_coarse_median.csv'
data = pd.read_csv(file_path)

r2_score_list_components = []

for i in range(compFirst, compLast + 1):

    # Model with specific number of components selected
    pls_model = PLSRegression(n_components=i)

    predicted = []
    actual = []

    for sample in samples:
        train_X = data[data["Fish ID"] != sample].iloc[:, firstWL:].values
        test_X = data[data["Fish ID"] == sample].iloc[:, firstWL:].values
        train_y = data[data["Fish ID"] != sample][target].values
        test_y = data[data["Fish ID"] == sample][target].values

        # Train the PLS model on the train set
        pls_model.fit(train_X, train_y)

        # Predict on the test set
        y_pred = pls_model.predict(test_X)

        predicted.extend(y_pred.flatten())  # Append the predicted values
        actual.extend(test_y.flatten())  # Append the actual values

    predicted = np.array(predicted)
    actual = np.array(actual)

    r2 = r2_score(actual, predicted)
    r2_score_list_components.append(r2)

    print(f"R² SCORE for {i} Components: {r2}")

# Plot the R² scores for each number of components
plt.figure(figsize=(10, 6))
plt.plot(range(compFirst, compLast + 1), r2_score_list_components, marker='o', linestyle='-', color='b')
plt.xlabel('Number of Components')
plt.ylabel('R² Score')
plt.title(f'R² Score vs Number of Components in PLS Model for {target} using LOOCV')
plt.xticks(range(compFirst, compLast + 1))  # Ensure each component is marked on the x-axis
plt.grid(True)
plt.show()
