from config.generalParameters import imageFolder, subsquareSize
import importlib
import os
from config.generalParameters import emscWavelength1, emscWL1min, emscWL1max
from config.generalParameters import emscWavelength2, emscWL2min, emscWL2max
from config.generalParameters import emscWavelength3, emscWL3min, emscWL3max

# List of sample names
samples = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17", "S18"]
# samples = ["S01"]
# samples = ["S01","S02", "S03", "S04", "S05", "S06"]
# samples = ["S07", "S08", "S09", "S10", "S11", "S12"]
# samples = ["S13", "S14", "S15", "S16", "S17", "S18"]

# set Dataset to use (0,1 or 2)
dataSetChoice = 2

squareMaps =[
    [1, 48],
    [2, 24],
    [3, 16],
    [4, 12],
    [5, 10],
    [6, 8],
    [7, 7],
    [8, 6],
]

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

    # # 1 create hdrs
    # from scripts.module_02_emscProcessing import oneShotHDRcreation
    # oneShotHDRcreation(imageFilePath, config.samplename, dataSetChoice+1)
    #
    # # 2 create lowlight mask
    # from scripts.module_04_masking import lowlightMaskCreation
    # lowlightMaskCreation(config.samplename, dataSetChoice+1)
    #
    # # 3 combine masks
    # from scripts.module_04_masking import combineMasksNoEMSC
    # combineMasksNoEMSC(config.samplename, dataSetChoice+1)

    # # 4 adjust and create finemasks
    from scripts.module_04_masking import fineMasking, emscPicture, fineCutMaskCreation, cutMaskCreation
    # emscPicture(config.samplename,emscWavelength1,emscWL1min,emscWL1max, dataSetChoice+1)
    # fineMasking(config.samplename, config.areasOfInterest[dataSetChoice], subsquareSize[dataSetChoice], dataSetChoice+1)
    #for mapDef in squareMaps:
    #    fineCutMaskCreation(config.samplename, config.areasOfInterest[dataSetChoice], mapDef[1], mapDef[0], dataSetChoice+1)
    # cutMaskCreation(config.samplename, config.areasOfInterest[dataSetChoice], subsquareSize[dataSetChoice], dataSetChoice+1)
    #
    # # 5 plot average spectra
    from scripts.module_06_visualization import fineAveragePlotAreas, areaPlotSpectra
    # areaPlotSpectra(config.samplename, ((500,120),(600,140)), dataSetChoice+1)
    # fineAveragePlotAreas(config.samplename, dataSetChoice+1)

# create dataframe
granularity = 8
from scripts.module_07_tableCreation import exportDataFrameFine
exportDataFrameFine(dataSetChoice+1, granularity)

