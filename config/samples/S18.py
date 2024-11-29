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
    ((730, 180), 'T'),                       # T: Tail
    ((530, 220), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((540, 90), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((240, 200), 'H'),                     # H: Head
    ((260, 60), 'F2')            # F2: Belly with trimmed visceral fat
    ],[
    ((290, 130), 'T'),                       # T: Tail
    ((460, 90), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((450, 220), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((760, 110), 'H'),                     # H: Head
    ((740, 240), 'F2')            # F2: Belly with trimmed visceral fat
    ]
]
