from config.generalParameters import gcLength
import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, Flatten, Dense, Input

### Settings
target = 'T_EPAandDHA'
datasetChoice = 3

### Load the data
# median coarse
file_path = f'../exported_data_coarse_median_dataset{datasetChoice}.csv'
data_coarse = pd.read_csv(file_path)
# Define where the first wavlength is located
first_wavelength_coarse = gcLength

# all replicate fine
file_path = f'../exported_data_fine_dataset{datasetChoice}.csv'
data_fine = pd.read_csv(file_path)
# Define where the first wavlength is located
first_wavelength_fine = first_wavelength_coarse+4

samples = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17", "S18"]
test_mse_list = []

for sample in samples:
    print(sample)
    ## Train Model
    data_fine_train = data_fine[~(data_fine["Fish_ID"] == sample)]
    # X and y for test
    X_train = data_fine_train.iloc[:, first_wavelength_fine:].values
    y_train = data_fine_train[target].values

    ## Test the models
    data_coarse_test = data_coarse[data_coarse["Fish_ID"] == sample]
    # X and y for test
    X_test = data_coarse_test.iloc[:, first_wavelength_coarse:].values
    y_test = data_coarse_test[target].values

    # Define the 1D CNN model
    model = Sequential([
        Input(shape=(X_train.shape[1], 1)),
        Conv1D(filters=8, kernel_size=32, activation='relu',padding='same', strides=2),
        Flatten(),
        Dense(1)  # Output layer for regression
    ])

    # Compile the model
    model.compile(optimizer='adam', loss='mse', metrics=['mse'])

    # Train the model
    history = model.fit(X_train, y_train, epochs=5, batch_size=32, validation_split=0.2)

    # Evaluate the model
    test_loss, test_mse = model.evaluate(X_test, y_test)
    print(f"Test Loss: {test_loss}, Test mse: {test_mse}")
    test_mse_list.append(test_mse)

print(np.mean(test_mse_list))