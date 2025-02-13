filename = [
    "S16_SWIR_384_SN3151_9006us_2022-06-13T124638_raw_rad_float32.hdr",
    "s16_l_g3_SWIR_384_SN3151_3500us_2024-11-26T102734_raw_rad_float32.hdr",
    "s16_s_SWIR_384_SN3151_4800us_2024-11-26T105116_raw_rad_float32.hdr"
]

samplename = "S16"

#define area for white reference and background
# whiteArea = [(1900, 150), (2000, 330)]
backgroundArea = [(500, 100), (1600, 350)]

# Define the positions by specifying two points (top-left and bottom-right) with names
areasOfInterest = [[
    ((1150, 200), 'T'),                       # T: Tail
    ((800, 10), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((800, 255), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((0, 10), 'H'),                     # H: Head
    ((0, 255), 'F1')            # F1: Belly with trimmed visceral fat
    ],[
    ((720, 190), 'T'),                       # T: Tail
    ((510, 230), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((520, 90), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((220, 230), 'H'),                     # H: Head
    ((230, 80), 'F1')            # F1: Belly with trimmed visceral fat
    ],[
    ((300, 150), 'T'),                       # T: Tail
    ((460, 100), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((450, 220), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((760, 90), 'H'),                     # H: Head
    ((760, 250), 'F1')            # F1: Belly with trimmed visceral fat
    ]
]