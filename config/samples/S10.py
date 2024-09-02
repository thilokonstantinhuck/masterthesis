filename = "S10_SWIR_384_SN3151_9006us_2022-05-27T121223_raw_rad_float32.hdr"

samplename = "S10"

#define area for white reference and background
# whiteArea = [(1900, 150), (2000, 330)]
backgroundArea = [(500, 100), (1600, 350)]

# Define the positions by specifying two points (top-left and bottom-right) with names
areasOfInterest = [
    ((200, 150), (300, 300), 'Tail'),                       # T: Tail
    ((750, 260), (850, 340), 'Norwegian_Quality_Cut1'),     # N1: Norwegian Quality Cut 1
    ((750, 80), (850, 160), 'Norwegian_Quality_Cut2'),     # N2: Norwegian Quality Cut 2
    ((1600, 280), (1700, 360), 'Head'),                     # H: Head
    ((1600, 0), (1700, 80), 'Belly_Fat_Trimmed')            # F2: Belly with trimmed visceral fat
]

