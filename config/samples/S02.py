filename = "S2-R-G1_SWIR_384_SN3151_9006us_2022-05-02T120329_raw_rad_float32.hdr"

samplename = "S02"

#define area for white reference and background
whiteArea = [(10, 50), (100, 200)]
backgroundArea = [(500, 100), (1600, 350)]

# Define the positions by specifying two points (top-left and bottom-right) with names
areasOfInterest = [
    ((450, 150), 'T'),                       # T: Tail
    ((900, 250), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((900, 20), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((1880, 250), 'H'),                     # H: Head
    ((1880, 0), 'F2')            # F2: Belly with trimmed visceral fat
]
