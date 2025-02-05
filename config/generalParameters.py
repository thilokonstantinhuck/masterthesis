# GC data length coarse
gcLength = 95

# Path to image data

imageFolder = [
    r"C:\SALMONDATA\SWIR_Hyspex\All_converted_file",
    r"C:\Users\thilohuc\OneDrive - Norwegian University of Life Sciences\Desktop\Salmon_Data_November_24_full\3_RAW_converted_ordered\second_dataset",
    r"C:\Users\thilohuc\OneDrive - Norwegian University of Life Sciences\Desktop\Salmon_Data_November_24_full\3_RAW_converted_ordered\third_dataset"
]

subsquareSize = [25,10,10]

# Settings Lighting Detection
overlitDefinition = 0.75

# as we are in absorbance now this is ectually high light, need to do something else
lowlightDefinition = 1
lowlightWavelength = 1460

# Settings EMSC
# Adjust according to the range in your data, so that you get a clear seperation from fish and background
emscWavelength1 = 980
emscWL1min = 0.35
emscWL1max = 0.6
emscWavelength2 = 1280
emscWL2min = 0.8
emscWL2max = 1.2
emscWavelength3 = 1460
emscWL3min = 1.7
emscWL3max = 2.15