from config.generalParameters import imageFolder
from config.S6 import filename
from config.S6 import samplename
import os

imageFilePath = os.path.join(imageFolder, filename)

# Remove overlit Pixels, which are shown by a maxed out Value at some point in the Spectra
from scripts import module_01_overlitRemoval

# Run EMSC to seperate fish and background, creating a seperation mask and a plot
