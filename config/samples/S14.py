filename = "S14_SWIR_384_SN3151_9006us_2022-06-13T124127_raw_rad_float32.hdr"

samplename = "S14"

#define area for white reference and background
# whiteArea = [(1900, 150), (2000, 330)]
backgroundArea = [(500, 100), (1600, 350)]

# Define the positions by specifying two points (top-left and bottom-right) with names
areasOfInterest = [
    ((1100, 130), 'T'),                       # T: Tail
    ((780, 30), 'NQC1'),     # N1: Norwegian Quality Cut 1
    ((780, 255), 'NQC2'),     # N2: Norwegian Quality Cut 2
    ((0, 0), 'H'),                     # H: Head
    ((0, 255), 'F2')            # F2: Belly with trimmed visceral fat
]
