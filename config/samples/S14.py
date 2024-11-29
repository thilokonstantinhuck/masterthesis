filename = [
    "S14_SWIR_384_SN3151_9006us_2022-06-13T124127_raw_rad_float32.hdr",
    "s14_l_g3_SWIR_384_SN3151_3500us_2024-11-26T102216_raw_rad_float32.hdr",
    "s14_s_SWIR_384_SN3151_4800us_2024-11-26T105456_raw_rad_float32.hdr"
]

samplename = "S14"

#define area for white reference and background
# whiteArea = [(1900, 150), (2000, 330)]
backgroundArea = [(500, 100), (1600, 350)]

# Define the positions by specifying two points (top-left and bottom-right) with names
areasOfInterest = [[
    ((1100, 130), 'T'),                       # T: Tail
    ((780, 30), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((780, 255), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((0, 0), 'H'),                     # H: Head
    ((0, 255), 'F2')            # F2: Belly with trimmed visceral fat
    ],[
    ((730, 180), 'T'),                       # T: Tail
    ((530, 220), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((540, 90), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((240, 200), 'H'),                     # H: Head
    ((260, 60), 'F2')            # F2: Belly with trimmed visceral fat
    ],[
    ((290, 120), 'T'),                       # T: Tail
    ((460, 90), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((450, 210), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((760, 100), 'H'),                     # H: Head
    ((730, 230), 'F2')            # F2: Belly with trimmed visceral fat
    ]
]