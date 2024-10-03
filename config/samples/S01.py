filename = "S1-R-G1_SWIR_384_SN3151_9006us_2022-05-02T120939_raw_rad_float32.hdr"

samplename = "S01"

#define area for white reference and background
whiteArea = [(0, 0), (50, 330)]
backgroundArea = [(500, 100), (1600, 350)]

# Define the positions by specifying two points (top-left and bottom-right) with names
areasOfInterest = [
    ((300, 150), 'Tail'),                       # T: Tail
    ((800, 300), 'Norwegian_Quality_Cut1'),     # N1: Norwegian Quality Cut 1
    ((800, 120), 'Norwegian_Quality_Cut2'),     # N2: Norwegian Quality Cut 2
    ((1900, 300), 'Head'),                     # H: Head
    ((1900, 0), 'Belly_Fat_Trimmed')            # F2: Belly with trimmed visceral fat
]

