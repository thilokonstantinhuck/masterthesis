filename = [
    "S13_SWIR_384_SN3151_9006us_2022-06-13T123745_raw_rad_float32.hdr",
    "s13_l_g3_SWIR_384_SN3151_3500us_2024-11-26T101955_raw_rad_float32.hdr",
    "s13_s_SWIR_384_SN3151_4800us_2024-11-26T105610_raw_rad_float32.hdr"
]

samplename = "S13"

#define area for white reference and background
# whiteArea = [(1900, 150), (2000, 330)]
backgroundArea = [(500, 100), (1600, 350)]


# Define the positions by specifying two points (top-left and bottom-right) with names
areasOfInterest = [[
    ((1100, 120), 'T'),                       # T: Tail
    ((800, 0), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((800, 255), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((0, 0), 'H'),                     # H: Head
    ((0, 255), 'F1')            # F1: Belly with trimmed visceral fat
    ],[
    ((710, 140), 'T'),                       # T: Tail
    ((510, 190), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((520, 60), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((200, 180), 'H'),                     # H: Head
    ((220, 40), 'F1')            # F1: Belly with trimmed visceral fat
    ],[
    ((300, 130), 'T'),                       # T: Tail
    ((460, 80), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((450, 200), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((775, 95), 'H'),                     # H: Head
    ((740, 240), 'F1')            # F1: Belly with trimmed visceral fat
    ]
]