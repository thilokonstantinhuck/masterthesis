filename = "S6-R-G1_SWIR_384_SN3151_9006us_2022-05-02T120753_raw_rad_float32.hdr"

samplename = "S06"

#define area for white reference and background
whiteArea = [(1900, 150), (2000, 330)]
backgroundArea = [(500, 100), (1600, 350)]

# Define the positions by specifying two points (top-left and bottom-right) with names
areasOfInterest = [
    ((300, 150), (400, 300), 'Tail'),                       # T: Tail
    ((750, 300), (850, 380), 'Norwegian_Quality_Cut1'),     # N1: Norwegian Quality Cut 1
    ((750, 100), (850, 180), 'Norwegian_Quality_Cut2'),     # N2: Norwegian Quality Cut 2
    ((1600, 300), (1700, 380), 'Head'),                     # H: Head
    ((1500, 0), (1600, 80), 'Belly_Fat_Trimmed')            # F2: Belly with trimmed visceral fat
]

