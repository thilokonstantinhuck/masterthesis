# Path to image data

imageFolder = r"C:\SALMONDATA\SWIR_Hyspex\All_converted_file"

# Settings Lighting Detection
overlitDefinition = 0.75
lowlightDefinition = 0.03
lowlightWavelength = 1080

# Settings EMSC
# Adjust according to the range in your data, so that you get a clear seperation from fish and background
emscMinRatio = 0.9
emscMaxRatio = 1.3
emscWavelength1 = 1080
emscWavelength2 = 1460