filename = "S11_SWIR_384_SN3151_9006us_2022-05-27T120547_raw_rad_float32.hdr"

samplename = "S11"

#define area for white reference and background
# whiteArea = [(1900, 150), (2000, 330)]
backgroundArea = [(500, 100), (1600, 350)]

# Define the positions by specifying two points (top-left and bottom-right) with names
areasOfInterest = [
    ((170, 180), 'T'),                       # T: Tail
    ((550, 255), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((550, 70), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((1600, 255), 'H'),                     # H: Head
    ((1550, 0), 'F2')            # F2: Belly with trimmed visceral fat
]


