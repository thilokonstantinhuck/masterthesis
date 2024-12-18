filename = [
    "S9_SWIR_384_SN3151_9006us_2022-05-27T121717_raw_rad_float32.hdr",
    "s9_l_g2_SWIR_384_SN3151_3500us_2024-11-26T101022_raw_rad_float32.hdr",
    "s9_s_SWIR_384_SN3151_4800us_2024-11-26T110223_raw_rad_float32.hdr"
]

samplename = "S09"

#define area for white reference and background
# whiteArea = [(1900, 150), (2000, 330)]
backgroundArea = [(500, 100), (1600, 350)]

# Define the positions by specifying two points (top-left and bottom-right) with names
areasOfInterest = [[
    ((200, 90), 'T'),                       # T: Tail
    ((600, 215), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((600, 10), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((1670, 255), 'H'),                     # H: Head
    ((1630, 20), 'F1')            # F1: Belly with trimmed visceral fat
    ],[
    ((720, 145), 'T'),                       # T: Tail
    ((520, 190), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((530, 80), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((250, 165), 'H'),                     # H: Head
    ((260, 60), 'F1')            # F1: Belly with trimmed visceral fat
    ],[
    ((300, 130), 'T'),                       # T: Tail
    ((470, 100), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((460, 190), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((755, 110), 'H'),                     # H: Head
    ((750, 220), 'F1')            # F1: Belly with trimmed visceral fat
    ]
]

