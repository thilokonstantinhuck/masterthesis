filename = [
    "S12_SWIR_384_SN3151_9006us_2022-05-27T115725_raw_rad_float32.hdr",
    "s12_l_g2_SWIR_384_SN3151_3500us_2024-11-26T101739_raw_rad_float32.hdr",
    "s12_s_SWIR_384_SN3151_4800us_2024-11-26T105759_raw_rad_float32.hdr"
]

samplename = "S12"

#define area for white reference and background
# whiteArea = [(1900, 150), (2000, 330)]
backgroundArea = [(500, 100), (1600, 350)]

# Define the positions by specifying two points (top-left and bottom-right) with names
areasOfInterest = [[
    ((50, 110), 'T'),                       # T: Tail
    ((500, 225), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((500, 10), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((1650, 255), 'H'),                     # H: Head
    ((1650, 10), 'F2')            # F2: Belly with trimmed visceral fat
    ],[
    ((300, 150), 'T'),                       # T: Tail
    ((800, 250), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((800, 80), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((1850, 250), 'H'),                     # H: Head
    ((1850, 0), 'F2')            # F2: Belly with trimmed visceral fat
    ],[
    ((230, 135), 'T'),                       # T: Tail
    ((430, 90), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((430, 210), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((750, 100), 'H'),                     # H: Head
    ((715, 240), 'F2')            # F2: Belly with trimmed visceral fat
    ]
]
