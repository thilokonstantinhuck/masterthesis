filename = [
    "S2-R-G1_SWIR_384_SN3151_9006us_2022-05-02T120329_raw_rad_float32.hdr",
    "s2_l_g1_SWIR_384_SN3151_3500us_2024-11-26T095057_raw_rad_float32.hdr",
    "s2_s_SWIR_384_SN3151_4800us_2024-11-26T111200_raw_rad_float32.hdr"
]

samplename = "S02"

#define area for white reference and background
whiteArea = [(10, 50), (100, 200)]
backgroundArea = [(500, 100), (1600, 350)]

# Define the positions by specifying two points (top-left and bottom-right) with names
areasOfInterest = [[
    ((450, 150), 'T'),                       # T: Tail
    ((900, 250), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((900, 20), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((1880, 250), 'H'),                     # H: Head
    ((1880, 0), 'F2')            # F2: Belly with trimmed visceral fat
    ],[
    ((730, 180), 'T'),                       # T: Tail
    ((530, 220), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((540, 90), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((240, 200), 'H'),                     # H: Head
    ((260, 60), 'F2')            # F2: Belly with trimmed visceral fat
    ],[
    ((310, 115), 'T'),                       # T: Tail
    ((460, 80), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((450, 200), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((760, 110), 'H'),                     # H: Head
    ((740, 240), 'F2')            # F2: Belly with trimmed visceral fat
    ]
]