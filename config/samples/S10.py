filename = [
    "S10_SWIR_384_SN3151_9006us_2022-05-27T121223_raw_rad_float32.hdr",
    "s10_l_g2_SWIR_384_SN3151_3500us_2024-11-26T101321_raw_rad_float32.hdr",
    "s10_s_SWIR_384_SN3151_4800us_2024-11-26T110058_raw_rad_float32.hdr"
]

samplename = "S10"

#define area for white reference and background
# whiteArea = [(1900, 150), (2000, 330)]
backgroundArea = [(500, 100), (1600, 350)]

# Define the positions by specifying two points (top-left and bottom-right) with names
areasOfInterest = [[
    ((180, 130), 'T'),                       # T: Tail
    ((450, 255), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((450, 50), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((1650, 255), 'H'),                     # H: Head
    ((1650, 0), 'F2')            # F2: Belly with trimmed visceral fat
    ],[
    ((720, 160), 'T'),                       # T: Tail
    ((510, 220), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((520, 80), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((180, 180), 'H'),                     # H: Head
    ((200, 70), 'F2')            # F2: Belly with trimmed visceral fat
    ],[
    ((240, 140), 'T'),                       # T: Tail
    ((440, 90), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((420, 210), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((750, 120), 'H'),                     # H: Head
    ((720, 240), 'F2')            # F2: Belly with trimmed visceral fat
    ]
]
