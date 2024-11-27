filename = "S18_SWIR_384_SN3151_9006us_2022-06-13T125153_raw_rad_float32.hdr"
filename = [
    "S18_SWIR_384_SN3151_9006us_2022-06-13T125153_raw_rad_float32.hdr",
    "s18_l_g3_SWIR_384_SN3151_3500us_2024-11-26T103208_raw_rad_float32.hdr",
    "s18_s_SWIR_384_SN3151_4800us_2024-11-26T104136_raw_rad_float32.hdr"
]
samplename = "S18"

#define area for white reference and background
# whiteArea = [(1900, 150), (2000, 330)]
backgroundArea = [(500, 100), (1600, 350)]

# Define the positions by specifying two points (top-left and bottom-right) with names
areasOfInterest = [[
    ((1250, 160), 'T'),                       # T: Tail
    ((800, 0), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((800, 255), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((0, 0), 'H'),                     # H: Head
    ((0, 255), 'F2')            # F2: Belly with trimmed visceral fat
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
