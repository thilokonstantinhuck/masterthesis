filename = [
    "S5-R-G1_SWIR_384_SN3151_9006us_2022-05-02T121208_raw_rad_float32.hdr",
    "s5_l_g1_SWIR_384_SN3151_3500us_2024-11-26T100013_raw_rad_float32.hdr",
    "s5_s_SWIR_384_SN3151_4800us_2024-11-26T110710_raw_rad_float32.hdr"
]

samplename = "S05"

#define area for white reference and background
whiteArea = [(1700, 300), (1900, 380)]
backgroundArea = [(500, 100), (1600, 350)]

# Define the positions by specifying two points (top-left and bottom-right) with names
areasOfInterest = [[
    ((0, 245), 'T'),                       # T: Tail
    ((400, 250), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((350, 70), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((1490, 80), 'H'),                     # H: Head
    ((1200, 0), 'F2')            # F2: Belly with trimmed visceral fat
    ],[
    ((300, 150), 'T'),                       # T: Tail
    ((800, 250), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((800, 80), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((1850, 250), 'H'),                     # H: Head
    ((1850, 0), 'F2')            # F2: Belly with trimmed visceral fat
    ],[
    ((300, 130), 'T'),                       # T: Tail
    ((460, 90), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((460, 200), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((750, 110), 'H'),                     # H: Head
    ((720, 235), 'F2')            # F2: Belly with trimmed visceral fat
    ]
]