import spectral.io.envi as envi
import pickle
import importlib
import matplotlib.pyplot as plt
import numpy as np
from numpy.ma.extras import average
import pandas as pd
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression

# Load the data
file_path = 'data/average_data.csv'
dataGC = pd.read_csv(file_path)
evaluationColumn = "Lipid_%"

# Load the trained PLS model
model_filename = 'data/pls_model.pkl'
with open(model_filename, 'rb') as file:
    pls_model = pickle.load(file)

# positions to do validation on
# samples = ["S01", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "S12"] # r2 0.61
samples = ["S01", "S02", "S03", "S04", "S05", "S06"] # average R2 0.68 / median R2 0.63
# samples = ["S07", "S08", "S09", "S10", "S11", "S12"] # r2 0.63 / median R2 0.63
# samples = ["S13", "S14", "S15", "S16", "S17", "S18"] # r2 0.12
# samplesTest = ["S02"]

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
