from config.generalParameters import imageFolder
from config.S01 import filename, samplename, areasOfInterest, backgroundArea

import os

imageFilePath = os.path.join(imageFolder, filename)

# Create absorbance image of the Spectra
from scripts.module_01_preProcessing import absorbanceHDRcreation
absorbanceHDRcreation(imageFilePath, samplename)

# Remove overlit Pixels, which are shown by a maxed out Value at some point in the Spectra
from scripts.module_01_preProcessing import overlit
overlit(imageFilePath, samplename)

# Run EMSC on the data
from scripts.module_02_emscProcessing import emscHDRcreation
emscHDRcreation(samplename)

# Seperate fish and background, creating a seperation mask and a plot
from scripts.module_04_masking import emscMaskCreation
emscMaskCreation(samplename)

# combine masks
from scripts.module_04_masking import combineMasks
combineMasks(samplename)

# analyze rectangles
from scripts.module_04_masking import rectangleAnalysis
rectangleAnalysis(samplename, areasOfInterest, backgroundArea)

# create cut masks
from scripts.module_04_masking import cutMaskCreation
cutMaskCreation(samplename, areasOfInterest)

# create average plots
from scripts.module_06_visualization import averagePlotAreas
averagePlotAreas(samplename)
