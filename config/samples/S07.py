filename = "S7_SWIR_384_SN3151_9006us_2022-05-27T123341_raw_rad_float32.hdr"

samplename = "S07"

#define area for white reference and background
# whiteArea = [(1900, 150), (2000, 330)]
backgroundArea = [(500, 100), (1600, 350)]

# Define the positions by specifying two points (top-left and bottom-right) with names
areasOfInterest = [
    ((200, 70), 'T'),                       # T: Tail
    ((600, 200), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((600, 0), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((1700, 255), 'H'),                     # H: Head
    ((1630, 20), 'F2')            # F2: Belly with trimmed visceral fat
]


