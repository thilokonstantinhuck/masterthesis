filename = "S13_SWIR_384_SN3151_9006us_2022-06-13T123745_raw_rad_float32.hdr"

samplename = "S13"

#define area for white reference and background
# whiteArea = [(1900, 150), (2000, 330)]
backgroundArea = [(500, 100), (1600, 350)]

# Define the positions by specifying two points (top-left and bottom-right) with names
areasOfInterest = [
    ((1100, 100), (1200, 250), 'Tail'),                       # T: Tail
    ((750, 80), (850, 160), 'Norwegian_Quality_Cut1'),     # N1: Norwegian Quality Cut 1
    ((750, 250), (850, 330), 'Norwegian_Quality_Cut2'),     # N2: Norwegian Quality Cut 2
    ((0, 0), (100, 80), 'Head'),                     # H: Head
    ((0, 300), (100, 380), 'Belly_Fat_Trimmed')            # F2: Belly with trimmed visceral fat
]

