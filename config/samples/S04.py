filename = [
    "S4-R-G1_SWIR_384_SN3151_9006us_2022-05-02T121643_raw_rad_float32.hdr",
    "s4_l_g1_SWIR_384_SN3151_3500us_2024-11-26T095736_raw_rad_float32.hdr",
    "s4_s_SWIR_384_SN3151_4800us_2024-11-26T110907_raw_rad_float32.hdr"
]

samplename = "S04"

#define area for white reference and background
whiteArea = [(200, 10), (300, 50)]
backgroundArea = [(500, 100), (1600, 350)]

# Define the positions by specifying two points (top-left and bottom-right) with names
areasOfInterest = [[
    ((250, 200), 'T'),                       # T: Tail
    ((700, 255), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((700, 80), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((1750, 255), 'H'),                     # H: Head
    ((1720, 100), 'F2')            # F2: Belly with trimmed visceral fat
    ],[
    ((730, 180), 'T'),                       # T: Tail
    ((530, 220), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((540, 90), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((240, 200), 'H'),                     # H: Head
    ((260, 60), 'F2')            # F2: Belly with trimmed visceral fat
    ],[
    ((320, 90), 'T'),                       # T: Tail
    ((470, 80), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((470, 180), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((780, 90), 'H'),                     # H: Head
    ((760, 220), 'F2')            # F2: Belly with trimmed visceral fat
    ]
]