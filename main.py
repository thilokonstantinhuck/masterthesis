from config.generalParameters import imageFolder
from config.S6 import filename
from config.S6 import samplename
from config.S6 import whiteArea as referenceArea

import os

imageFilePath = os.path.join(imageFolder, filename)

# Remove overlit Pixels, which are shown by a maxed out Value at some point in the Spectra
from scripts.module_01_overlitRemoval import overlit
overlit(imageFilePath, samplename)

# Run EMSC on the data
from scripts.module_02_emscProcessing import emsc_transformation
emsc_transformation(referenceArea, samplename)

# Seperate fish and background, creating a seperation mask and a plot
from scripts.module_03_emscMasking import emscProcessing
emscProcessing(samplename)
