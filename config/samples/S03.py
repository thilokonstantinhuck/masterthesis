filename = "S3-R-G1_SWIR_384_SN3151_9006us_2022-05-02T121354_raw_rad_float32.hdr"

samplename = "S03"

#define area for white reference and background
whiteArea = [(200, 10), (300, 50)]
backgroundArea = [(500, 100), (1600, 350)]

# Define the positions by specifying two points (top-left and bottom-right) with names
areasOfInterest = [
    ((250, 170), 'T'),                       # T: Tail
    ((700, 245), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((700, 40), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((1750, 240), 'H'),                     # H: Head
    ((1700, 0), 'F2')            # F2: Belly with trimmed visceral fat
]

