import spectral.io.envi as envi
import importlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cross_decomposition import PLSRegression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

### Settings

# target = "EPAandDHA"
target = "Lipid_%"

selectedArea = "NQC1"

compFirst = 14
compLast = 15

# Define where the first wavlength is located
firstWL = 46

# samples = ["S01", "S02", "S03", "S04", "S05", "S06"]
# samples = ["S07", "S08", "S09", "S10", "S11", "S12"]
# samples = ["S13", "S14", "S15", "S16", "S17", "S18"]
samples = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17", "S18"]


### Load the data
# GC averaged
file_pathGC = 'average_data.csv'
dataGC = pd.read_csv(file_pathGC)
# model
file_path = 'exported_data_all.csv'
data = pd.read_csv(file_path)

data = data[(data["Position"] != selectedArea)]

# Extract the hyperspectral data
X = data.iloc[:, firstWL:].values  # Hyperspectral data for training and validation
y = data[target].values  # Target variable for training and validation

r2_score_list = []

for i in range(compFirst, compLast + 1):

    # Model with specific number of components selected
    pls_model = PLSRegression(n_components=i)  # Adjust n_components as needed

    # Train the PLS model on the train/val set
    pls_model.fit(X, y)

    predicted = []
    actual = []

    # find slope and bias from all modelling samples

    for sample in samples:
        print(sample)
        # Load the image
        hdr = f"../tempImages/processed_image_{sample}_absorbance_EMSC.hdr"
        img = envi.open(hdr)
        image = img.load()

        # Construct the module name dynamically
        module_name = f"config.samples.{sample}"

        # Dynamically import the module
        sample_config = importlib.import_module(module_name)
        positions = sample_config.areasOfInterest

        # Get the Reference Value for Position
        for position in positions:
            positionKey = position[1]
            if positionKey == selectedArea:
                positionX = position[0][1]
                positionY = position[0][0]

                allSpectra = image[positionY:positionY + 124, positionX:positionX + 124].flatten()

                # Reshape the flattened list to have the individual spectra as rows
                # Assuming your hyperspectral image has 'num_bands' bands, and the block is 124x124 pixels
                num_bands = image.shape[-1]  # Number of bands in the hyperspectral image

                reshapedSpectra = allSpectra.reshape(-1, num_bands)

                # Calculate the average spectrum by taking the mean across all pixels
                averageSpectrum = np.mean(reshapedSpectra, axis=0)

                # Reshape the spectrum to a 2D array with one sample
                averageSpectrum = averageSpectrum.reshape(1, -1)

                #predict the spectra
                y_pred = pls_model.predict(averageSpectrum)

                # get the reference Value
                y_actual = \
                dataGC[(dataGC["Position"] == positionKey) & (dataGC["Fish ID"] == sample)][target].iloc[0]

                print(
                    f"{sample} {positionKey} / predicted: {y_pred[0]} / actual: {y_actual}")

                predicted.append(y_pred)
                actual.append(y_actual)



    predicted = np.array(predicted)
    actual = np.array(actual)

    # Reshape the arrays to be 2D (required for scikit-learn)
    actual_reshaped = actual.reshape(-1, 1)
    predicted_reshaped = predicted.reshape(-1, 1)

    # Create a linear regression model
    regression_model = LinearRegression()

    # Fit the model
    regression_model.fit(actual_reshaped, predicted_reshaped)

    # Get the slope and bias (intercept)
    slope = regression_model.coef_[0][0]
    bias = regression_model.intercept_[0]

    print(f"Slope: {slope}")
    print(f"Bias (Intercept): {bias}")

    # Correct the predicted values
    corrected_predicted = slope * predicted + bias

    # Calculate the R² score for corrected predicted values
    r2_corrected = r2_score(actual, corrected_predicted)
    print(f"R² SCORE with Slope/Bias Correction: {r2_corrected}")

    r2 = r2_score(actual, predicted)
    r2_score_list.append(r2)

    print(f"R² SCORE for {i} Components: {r2}")

# Plot the R² scores for each number of components
plt.figure(figsize=(10, 6))
plt.plot(range(compFirst, compLast + 1), r2_score_list, marker='o', linestyle='-', color='b')
plt.xlabel('Number of Components')
plt.ylabel('R² Score')
plt.title('R² Score vs Number of Components in PLS Model')
plt.xticks(range(compFirst, compLast + 1))  # Ensure each component is marked on the x-axis
plt.grid(True)
plt.show()