filename = "S5-R-G1_SWIR_384_SN3151_9006us_2022-05-02T121208_raw_rad_float32.hdr"

samplename = "S05"

#define area for white reference and background
whiteArea = [(1700, 300), (1900, 380)]
backgroundArea = [(500, 100), (1600, 350)]

# Define the positions by specifying two points (top-left and bottom-right) with names
areasOfInterest = [
    ((0, 245), 'T'),                       # T: Tail
    ((400, 250), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((350, 70), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((1490, 80), 'H'),                     # H: Head
    ((1200, 0), 'F2')            # F2: Belly with trimmed visceral fat
]
