from config.generalParameters import imageFolder, subsquareSize
import importlib
import os
from config.generalParameters import emscWavelength1, emscWL1min, emscWL1max
from config.generalParameters import emscWavelength2, emscWL2min, emscWL2max
from config.generalParameters import emscWavelength3, emscWL3min, emscWL3max

# List of sample names
# samples = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17", "S18"]
samples = ["S18"]
# samples = ["S01","S02", "S03", "S04", "S05", "S06"]
# samples = ["S07", "S08", "S09", "S10", "S11", "S12"]
# samples = ["S13", "S14", "S15", "S16", "S17", "S18"]

# set Dataset to use (0,1 or 2)
dataSetChoice = 2


def load_sample_config(sampleName):
    # Construct the module name dynamically
    module_name = f"config.samples.{sampleName}"

    # Dynamically import the module
    sample_module = importlib.import_module(module_name)

    # Return the imported module
    return sample_module

for sample in samples:
    # Load the specific module
    config = load_sample_config(sample)

    imageFilePath = os.path.join(imageFolder[dataSetChoice], config.filename[dataSetChoice])

    # 1 create hdrs
    from scripts.module_02_emscProcessing import oneShotHDRcreation
    oneShotHDRcreation(imageFilePath, config.samplename)

    # 2 create lowlight mask
    from scripts.module_04_masking import lowlightMaskCreation
    lowlightMaskCreation(config.samplename)

    # 3 combine masks
    from scripts.module_04_masking import combineMasksNoEMSC
    combineMasksNoEMSC(config.samplename)

    # # 4 adjust and create finemasks
    from scripts.module_04_masking import fineMasking, emscPicture, fineCutMaskCreation, cutMaskCreation
    emscPicture(config.samplename,emscWavelength1,emscWL1min,emscWL1max)
    fineMasking(config.samplename, config.areasOfInterest[dataSetChoice], subsquareSize[dataSetChoice])
    fineCutMaskCreation(config.samplename, config.areasOfInterest[dataSetChoice], subsquareSize[dataSetChoice])
    # OR
    # cutMaskCreation(config.samplename, config.areasOfInterest)

    # 5 plot average spectra
    from scripts.module_06_visualization import fineAveragePlotAreas
    fineAveragePlotAreas(config.samplename)

# create dataframe
# from scripts.module_07_tableCreation import exportDataFrame
# exportDataFrame()

