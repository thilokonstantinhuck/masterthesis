filename = "S5-R-G1_SWIR_384_SN3151_9006us_2022-05-02T121208_raw_rad_float32.hdr"

samplename = "S05"

#define area for white reference and background
whiteArea = [(1700, 300), (1900, 380)]
backgroundArea = [(500, 100), (1600, 350)]

# Define the positions by specifying two points (top-left and bottom-right) with names
areasOfInterest = [
    ((200, 280), (300, 380), 'Tail'),                       # T: Tail
    ((600, 300), (700, 380), 'Norwegian_Quality_Cut1'),     # N1: Norwegian Quality Cut 1
    ((550, 120), (650, 200), 'Norwegian_Quality_Cut2'),     # N2: Norwegian Quality Cut 2
    ((1400, 120), (1600, 200), 'Head'),                     # H: Head
    ((1250, 0), (1500, 80), 'Belly_Fat_Trimmed')            # F2: Belly with trimmed visceral fat
]

