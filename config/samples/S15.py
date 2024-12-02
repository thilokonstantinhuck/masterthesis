filename = [
    "S15_SWIR_384_SN3151_9006us_2022-06-13T124449_raw_rad_float32.hdr",
    "s15_l_g3_SWIR_384_SN3151_3500us_2024-11-26T102532_raw_rad_float32.hdr",
    "s15_s_SWIR_384_SN3151_4800us_2024-11-26T105233_raw_rad_float32.hdr"
]

samplename = "S15"

#define area for white reference and background
# whiteArea = [(1900, 150), (2000, 330)]
backgroundArea = [(500, 100), (1600, 350)]

# Define the positions by specifying two points (top-left and bottom-right) with names
areasOfInterest = [[
    ((1100, 180), 'T'),                       # T: Tail
    ((800, 30), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((800, 255), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((0, 35), 'H'),                     # H: Head
    ((0, 255), 'F1')            # F1: Belly with trimmed visceral fat
    ],[
    ((710, 160), 'T'),                       # T: Tail
    ((510, 180), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((520, 70), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((220, 160), 'H'),                     # H: Head
    ((235, 40), 'F1')            # F1: Belly with trimmed visceral fat
    ],[
    ((285, 125), 'T'),                       # T: Tail
    ((460, 90), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((450, 200), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((750, 110), 'H'),                     # H: Head
    ((720, 240), 'F1')            # F1: Belly with trimmed visceral fat
    ]
]