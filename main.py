from config.generalParameters import imageFolder
import importlib
import os

# List of sample names
samples = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10",
           "S11", "S12", "S13", "S14", "S15", "S16", "S17", "S18"]


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

    imageFilePath = os.path.join(imageFolder, config.filename)

    # from scripts.module_06_visualization import areaPlotSpectra
    # areaPlotSpectra(samplename, [(50, 150), (100, 330)])
    #
    # # Create absorbance image of the Spectra
    # from scripts.module_01_preProcessing import absorbanceHDRcreation
    # absorbanceHDRcreation(imageFilePath, config.samplename)
    #
    # # Remove overlit Pixels, which are shown by a maxed out Value at some point in the Spectra
    # from scripts.module_01_preProcessing import overlit
    # overlit(imageFilePath, config.samplename)
    #
    # # Run EMSC on the data
    # from scripts.module_02_emscProcessing import emscHDRcreation
    # emscHDRcreation(config.samplename)
    #
    # # Seperate fish and background, creating a seperation mask and a plot
    # from scripts.module_04_masking import emscMaskCreation
    # emscMaskCreation(config.samplename)
    #
    # # combine masks
    # from scripts.module_04_masking import combineMasks
    # combineMasks(config.samplename)

    # analyze rectangles
    from scripts.module_04_masking import rectangleAnalysis
    rectangleAnalysis(config.samplename, config.areasOfInterest, config.backgroundArea)

    # # create cut masks
    # from scripts.module_04_masking import cutMaskCreation
    # cutMaskCreation(samplename, areasOfInterest)
    #
    # # create average plots
    # from scripts.module_06_visualization import averagePlotAreas
    # averagePlotAreas(samplename)

    # create dataframe
    # from scripts.module_07_tableCreation import exportDataFrame
    # exportDataFrame()

