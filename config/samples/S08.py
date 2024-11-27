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
    ((300, 150), 'T'),                       # T: Tail
    ((800, 250), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((800, 80), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((1850, 250), 'H'),                     # H: Head
    ((1850, 0), 'F2')            # F2: Belly with trimmed visceral fat
    ],[
    ((300, 130), 'T'),                       # T: Tail
    ((460, 80), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((450, 200), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((760, 90), 'H'),                     # H: Head
    ((720, 240), 'F2')            # F2: Belly with trimmed visceral fat
    ]
]

