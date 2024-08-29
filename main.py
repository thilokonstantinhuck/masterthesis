from config.generalParameters import imageFolder
from config.S02 import filename, samplename, areasOfInterest, whiteArea, backgroundArea

import os

imageFilePath = os.path.join(imageFolder, filename)

# Create absorbance image of the Spectra
from scripts.module_01_preProcessing import absorbanceHDRcreation
absorbanceHDRcreation(imageFilePath, samplename, whiteArea)

# Remove overlit Pixels, which are shown by a maxed out Value at some point in the Spectra
from scripts.module_01_preProcessing import overlit
overlit(imageFilePath, samplename)

# Run EMSC on the data
from scripts.module_02_emscProcessing import emsc_transformation
emsc_transformation(whiteArea, samplename)

# Seperate fish and background, creating a seperation mask and a plot
from scripts.module_03_emscMasking import emscProcessing
emscProcessing(samplename)

# combine masks
from scripts.module_05_maskCombination import combineMasks
combineMasks(samplename)

# create cut masks
from scripts.module_04_cutMasks import cutMaskCreation
cutMaskCreation(samplename, areasOfInterest)

# create average plots
from scripts.module_06_visualization import averagePlotAreas
averagePlotAreas(samplename)
