import spectral.io.envi as envi
import pickle
import importlib
import numpy as np
from numpy.ma.extras import average
import pandas as pd
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression

# Settings
evaluationColumn = "EPAandDHA"
# evaluationColumn = "Lipid_%"

# Load the data
file_path = 'data/average_data.csv'
dataGC = pd.read_csv(file_path)

# Load the trained PLS model
model_filename = ('data/pls_model.pkl')
with open(model_filename, 'rb') as file:
    pls_model = pickle.load(file)

# Fat Concentration
# F1
# NC: 2 Result: 0.65 / NC: 3 Result:0.65 / NC: 4 Result: 0.65 / NC: 5 Result: 0.66 / NC: 6 Result: 0.67/ NC: 8 Result: 0.72 / NC: 10 Result: 0.69 / NC: 12 Result: 0.48
# samples = ["S01", "S02", "S03", "S04", "S05", "S06"]
# F2
# NC: 2 Result: 0.57 / NC: 3 Result:0.61 / NC: 4 Result: 0.63 / NC: 5 Result: 0.67 / NC: 6 Result: 0.67/ NC: 8 Result: 0.68 / NC: 9 Result: 0.63 / NC: 10 Result: 0.38 / NC: 12 Result: 0.24
# samples = ["S07", "S08", "S09", "S10", "S11", "S12"]
# F3
# NC: 2 Result: 0.46 / NC: 3 Result: 0.50 / NC: 4 Result: 0.60 / NC: 5 Result: 0.57 / NC: 6 Result: 0.49/ NC: 7 Result: 0.22
# samples = ["S13", "S14", "S15", "S16", "S17", "S18"]
# All Feeds
# NC: 1 Result: 0.43 / NC: 2 Result: 0.51 / NC: 3 Result: 0.53 / NC: 4 Result: 0.55 / NC: 5 Result: 0.56 / NC: 6 Result: 0.58 / NC: 7 Result: 0.59/ NC: 8 Result: 0.57 / NC: 9 Result: 0.50 / NC: 10 Result: 0.36
# samples = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17", "S18"]

# EPA and DHA Concentration
# F1
# NC: 1 Result: 0.43 / NC: 2 Result: 0.71 / NC: 3 Result: 0.72 / NC: 4 Result: 0.75 / NC: 5 Result: 0.77 / NC: 6 Result: 0.84 / NC: 7 Result: 0.85 / NC: 8 Result: 0.86 / NC: 10 Result: 0.87 / NC: 12 Result: 0.75/ NC: 15 Result: 0.64
# samples = ["S01", "S02", "S03", "S04", "S05", "S06"]
# F2
# NC: 4 Result: 0.48 / NC: 6 Result: 0.58 / NC: 8 Result: 0.62 / NC: 10 Result: 0.61 / NC: 12 Result: 0.62 / NC: 15 Result: 0.49
# samples = ["S07", "S08", "S09", "S10", "S11", "S12"]
# F3
# NC: 3 Result: 0.52 / NC: 4 Result: 0.57 / NC: 5 Result: 0.57 / NC: 6 Result: 0.63 / NC: 7 Result: 0.60 / NC: 8 Result: 0.56 / NC: 10 Result: 0.36 /
samples = ["S13", "S14", "S15", "S16", "S17", "S18"]
# All Feeds
# NC: 3 Result: 0.41 / NC: 4 Result: 0.49 / NC: 5 Result: 0.54 / NC: 6 Result: 0.53 / NC: 7 Result: 0.52 / NC: 10 Result: 0.28 /
# samples = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17", "S18"]

predicted = []
actual = []

# find slope and bias from all modelling samples

for sample in samples:
    print(sample)
    # Load the image
    hdr = f"./tempImages/processed_image_{sample}_absorbance_EMSC.hdr"
    img = envi.open(hdr)
    image = img.load()

    # Reshape the image data to be compatible with the model
    # The image is reshaped into (num_pixels, num_wavelengths)
    num_pixels = image.shape[0] * image.shape[1]
    num_wavelengths = image.shape[2]
    X = image.reshape((num_pixels, num_wavelengths))

    # Make predictions using the loaded model
    y_pred = pls_model.predict(X).flatten()

    # Reshape the predictions back to the original image shape (height, width)
    predicted_image = y_pred.reshape((image.shape[0], image.shape[1]))

    # Construct the module name dynamically
    module_name = f"config.samples.{sample}"

    # Dynamically import the module
    sample_config = importlib.import_module(module_name)
    positions = sample_config.areasOfInterest

    # Get the Reference Value for Position
    for position in positions:
        positionKey = position[1]
        positionX = position[0][1]
        positionY = position[0][0]


        predictedValues = predicted_image[positionY:positionY+124, positionX:positionX+124].flatten()
        filteredValues = []
        skippedAmount = 0
        used = 0
        for value in predictedValues:
            if value < -20:
                skippedAmount += 1
            elif value > 80:
                skippedAmount += 1
            else:
                filteredValues.append(value)
                used += 1

        predictedValue = average(filteredValues)
        referenceValue = dataGC[(dataGC["Position"] == positionKey) & (dataGC["Fish ID"] == sample)][evaluationColumn].iloc[0]
        print(f"{sample} {positionKey} / skipped:{skippedAmount} / used:{used} / predicted:{predictedValue} / actual:{referenceValue}")

        predicted.append(predictedValue)
        actual.append(referenceValue)

predicted = np.array(predicted)
actual = np.array(actual)

r2 = r2_score(actual, predicted)
print(f"R² SCORE: {r2}")

# Reshape the arrays to be 2D (required for scikit-learn)
actual = actual.reshape(-1, 1)
predicted = predicted.reshape(-1, 1)

# Create a linear regression model
model = LinearRegression()

# Fit the model
model.fit(actual, predicted)

# Get the slope and bias (intercept)
slope = model.coef_[0][0]
bias = model.intercept_[0]

print(f"Slope: {slope}")
print(f"Bias (Intercept): {bias}")

# Correct the predicted values
corrected_predicted = slope * predicted + bias

r2corrected = r2_score(actual, corrected_predicted)
print(f"R² SCORE with Slope/Bias: {r2corrected}")
