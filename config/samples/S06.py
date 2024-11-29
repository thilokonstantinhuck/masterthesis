filename = [
    "S6-R-G1_SWIR_384_SN3151_9006us_2022-05-02T120753_raw_rad_float32.hdr",
    "s6_l_g1_SWIR_384_SN3151_3500us_2024-11-26T100249_raw_rad_float32.hdr",
    "s6_s_SWIR_384_SN3151_4800us_2024-11-26T110604_raw_rad_float32.hdr"
]

samplename = "S06"

#define area for white reference and background
whiteArea = [(1900, 150), (2000, 330)]
backgroundArea = [(500, 100), (1600, 350)]

# Define the positions by specifying two points (top-left and bottom-right) with names
areasOfInterest = [[
    ((250, 180), 'T'),                       # T: Tail
    ((550, 255), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((550, 70), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((1600, 255), 'H'),                     # H: Head
    ((1600, 0), 'F2')            # F2: Belly with trimmed visceral fat
    ],[
    ((730, 180), 'T'),                       # T: Tail
    ((530, 220), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((540, 90), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((240, 200), 'H'),                     # H: Head
    ((260, 60), 'F2')            # F2: Belly with trimmed visceral fat
    ],[
    ((320, 120), 'T'),                       # T: Tail
    ((460, 90), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((460, 190), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((770, 110), 'H'),                     # H: Head
    ((750, 230), 'F2')            # F2: Belly with trimmed visceral fat
    ]
]