filename = [
    "S8_SWIR_384_SN3151_9006us_2022-05-27T122625_raw_rad_float32.hdr",
    "s8_l_g2_SWIR_384_SN3151_3500us_2024-11-26T100805_raw_rad_float32.hdr",
    "s8_s_SWIR_384_SN3151_4800us_2024-11-26T110326_raw_rad_float32.hdr"
]

samplename = "S08"

#define area for white reference and background
# whiteArea = [(1900, 150), (2000, 330)]
backgroundArea = [(500, 100), (1600, 350)]


# Define the positions by specifying two points (top-left and bottom-right) with names
areasOfInterest = [[
    ((200, 110), 'T'),                       # T: Tail
    ((550, 205), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((550, 0), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((1680, 205), 'H'),                     # H: Head
    ((1600, 0), 'F2')            # F2: Belly with trimmed visceral fat
    ],[
    ((720, 140), 'T'),                       # T: Tail
    ((560, 180), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((570, 70), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((270, 160), 'H'),                     # H: Head
    ((280, 40), 'F2')            # F2: Belly with trimmed visceral fat
    ],[
    ((270, 130), 'T'),                       # T: Tail
    ((440, 90), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((430, 200), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((720, 90), 'H'),                     # H: Head
    ((720, 215), 'F2')            # F2: Belly with trimmed visceral fat
    ]
]

