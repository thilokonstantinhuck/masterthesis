filename = "S8_SWIR_384_SN3151_9006us_2022-05-27T122625_raw_rad_float32.hdr"

samplename = "S08"

#define area for white reference and background
# whiteArea = [(1900, 150), (2000, 330)]
backgroundArea = [(500, 100), (1600, 350)]

# Define the positions by specifying two points (top-left and bottom-right) with names
areasOfInterest = [
    ((300, 100), (400, 250), 'Tail'),                       # T: Tail
    ((750, 200), (850, 280), 'Norwegian_Quality_Cut1'),     # N1: Norwegian Quality Cut 1
    ((750, 50), (850, 130), 'Norwegian_Quality_Cut2'),     # N2: Norwegian Quality Cut 2
    ((1600, 250), (1700, 330), 'Head'),                     # H: Head
    ((1500, 0), (1600, 80), 'Belly_Fat_Trimmed')            # F2: Belly with trimmed visceral fat
]

