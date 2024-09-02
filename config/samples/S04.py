filename = "S4-R-G1_SWIR_384_SN3151_9006us_2022-05-02T121643_raw_rad_float32.hdr"

samplename = "S04"

#define area for white reference and background
whiteArea = [(200, 10), (300, 50)]
backgroundArea = [(500, 100), (1600, 350)]

# Define the positions by specifying two points (top-left and bottom-right) with names
areasOfInterest = [
    ((250, 180), (400, 300), 'Tail'),                       # T: Tail
    ((750, 300), (850, 380), 'Norwegian_Quality_Cut1'),     # N1: Norwegian Quality Cut 1
    ((750, 120), (850, 200), 'Norwegian_Quality_Cut2'),     # N2: Norwegian Quality Cut 2
    ((1700, 270), (1800, 360), 'Head'),                     # H: Head
    ((1650, 0), (1750, 80), 'Belly_Fat_Trimmed')            # F2: Belly with trimmed visceral fat
]
