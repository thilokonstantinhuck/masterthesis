filename = [
    "S7_SWIR_384_SN3151_9006us_2022-05-27T123341_raw_rad_float32.hdr",
    "s7_l_g2_SWIR_384_SN3151_3500us_2024-11-26T100438_raw_rad_float32.hdr",
    "s7_s_SWIR_384_SN3151_4800us_2024-11-26T110432_raw_rad_float32.hdr"
]

samplename = "S07"

#define area for white reference and background
# whiteArea = [(1900, 150), (2000, 330)]
backgroundArea = [(500, 100), (1600, 350)]

# Define the positions by specifying two points (top-left and bottom-right) with names
areasOfInterest = [[
    ((200, 70), 'T'),                       # T: Tail
    ((600, 200), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((600, 0), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((1700, 255), 'H'),                     # H: Head
    ((1630, 20), 'F2')            # F2: Belly with trimmed visceral fat
    ],[
    ((715, 170), 'T'),                       # T: Tail
    ((520, 210), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((530, 100), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((190, 160), 'H'),                     # H: Head
    ((220, 50), 'F2')            # F2: Belly with trimmed visceral fat
    ],[
    ((250, 130), 'T'),                       # T: Tail
    ((450, 90), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((440, 200), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((750, 145), 'H'),                     # H: Head
    ((700, 270), 'F2')            # F2: Belly with trimmed visceral fat
    ]
]

