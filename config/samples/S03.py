filename = [
    "S3-R-G1_SWIR_384_SN3151_9006us_2022-05-02T121354_raw_rad_float32.hdr",
    "s3_l_g1_SWIR_384_SN3151_3500us_2024-11-26T095441_raw_rad_float32.hdr",
    "s3_s_SWIR_384_SN3151_4800us_2024-11-26T111049_raw_rad_float32.hdr"
]

samplename = "S03"

#define area for white reference and background
whiteArea = [(200, 10), (300, 50)]
backgroundArea = [(500, 100), (1600, 350)]

# Define the positions by specifying two points (top-left and bottom-right) with names
areasOfInterest = [[
    ((250, 170), 'T'),                       # T: Tail
    ((700, 245), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((700, 40), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((1750, 240), 'H'),                     # H: Head
    ((1700, 0), 'F1')            # F1: Belly with trimmed visceral fat
    ],[
    ((690, 190), 'T'),                       # T: Tail
    ((480, 230), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((500, 110), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((190, 200), 'H'),                     # H: Head
    ((220, 60), 'F1')            # F1: Belly with trimmed visceral fat
    ],[
    ((300, 130), 'T'),                       # T: Tail
    ((460, 100), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((450, 220), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((760, 110), 'H'),                     # H: Head
    ((720, 240), 'F1')            # F1: Belly with trimmed visceral fat
    ]
]