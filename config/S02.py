filename = "S2-R-G1_SWIR_384_SN3151_9006us_2022-05-02T120329_raw_rad_float32.hdr"

samplename = "S02"

#define area for white reference and background
whiteArea = [(10, 50), (100, 200)]
backgroundArea = [(500, 100), (1600, 350)]

# Define the positions by specifying two points (top-left and bottom-right) with names
areasOfInterest = [
    ((500, 150), (600, 300), 'Tail'),                       # T: Tail
    ((950, 300), (1050, 380), 'Norwegian_Quality_Cut1'),     # N1: Norwegian Quality Cut 1
    ((950, 120), (1050, 200), 'Norwegian_Quality_Cut2'),     # N2: Norwegian Quality Cut 2
    ((1900, 300), (2000, 380), 'Head'),                     # H: Head
    ((1750, 0), (2000, 80), 'Belly_Fat_Trimmed')            # F2: Belly with trimmed visceral fat
]

