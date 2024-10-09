filename = "S8_SWIR_384_SN3151_9006us_2022-05-27T122625_raw_rad_float32.hdr"

samplename = "S08"

#define area for white reference and background
# whiteArea = [(1900, 150), (2000, 330)]
backgroundArea = [(500, 100), (1600, 350)]

# Define the positions by specifying two points (top-left and bottom-right) with names
areasOfInterest = [
    ((200, 110), 'T'),                       # T: Tail
    ((550, 205), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((550, 0), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((1680, 205), 'H'),                     # H: Head
    ((1600, 0), 'F2')            # F2: Belly with trimmed visceral fat
]


