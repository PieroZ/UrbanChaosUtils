import itertools

def parse_faces(input_data):
    faces = []
    lines = input_data.strip().split('\n')
    for line in lines:
        if 'xyz' in line:
            prefix, coords_str = line.split('(')
            coords_str = coords_str.strip(') ')
            coords = tuple(map(int, coords_str.split(',')))
            faces.append((prefix.strip(), coords))
    return faces

def generate_all_permutations(faces):
    # Generate all possible permutations of the indices 0, 1, 2
    permutations = list(itertools.permutations([0, 1, 2]))
    permuted_faces_groups = []

    for perm in permutations:
        permuted_group = []
        for face in faces:
            prefix, coords = face
            permuted_coords = [coords[i] for i in perm]
            permuted_group.append((prefix, tuple(permuted_coords)))
        permuted_faces_groups.append(permuted_group)

    return permuted_faces_groups

def format_face(face):
    prefix, coords = face
    coords_str = ', '.join(f'{coord:4}' for coord in coords)
    return f"{prefix} ({coords_str})"

def app(input_data):
    faces = parse_faces(input_data)
    all_permutations = generate_all_permutations(faces)

    for i, perm_group in enumerate(all_permutations):
        for face in perm_group:
            print(f'{format_face(face)} uv (   0,   1,   2) edge (1, 1, 1) group 1')
        print(i+1)


if __name__ == '__main__':

    input_data = """\
    Face: Material 0 xyz ( 318, 317, 316)
Face: Material 0 xyz ( 321, 320, 319)
Face: Material 0 xyz ( 359, 358, 357)
Face: Material 0 xyz ( 464, 463, 462)
Face: Material 0 xyz ( 465, 464, 462)
Face: Material 0 xyz (   2,   1,   0)
Face: Material 0 xyz (   5,   4,   3)
Face: Material 0 xyz (   8,   7,   6)
Face: Material 0 xyz (  11,  10,   9)
Face: Material 0 xyz (  14,  13,  12)
Face: Material 0 xyz (  17,  16,  15)
Face: Material 0 xyz (  20,  19,  18)
Face: Material 0 xyz (  22,  21,  20)
Face: Material 0 xyz (  22,  23,  21)
Face: Material 0 xyz (  22,  24,  23)
Face: Material 0 xyz (  24,  25,  23)
Face: Material 0 xyz (  27,  26,  23)
Face: Material 0 xyz (  28,  23,  26)
Face: Material 0 xyz (  28,  26,  29)
Face: Material 0 xyz (  26,  27,  30)
Face: Material 0 xyz (  26,  30,  31)
Face: Material 0 xyz (  31,  32,  26)
Face: Material 0 xyz (  31,  33,  32)
Face: Material 0 xyz (  34,  33,  31)
Face: Material 0 xyz (  31,  30,  34)
Face: Material 0 xyz (  35,  33,  34)
Face: Material 0 xyz (  34,  30,  36)
Face: Material 0 xyz (  27,  37,  30)
Face: Material 0 xyz (  30,  37,  36)
Face: Material 0 xyz (  36,  38,  34)
Face: Material 0 xyz (  38,  39,  34)
Face: Material 0 xyz (  40,  38,  36)
Face: Material 0 xyz (  37,  40,  36)
Face: Material 0 xyz (  38,  40,  41)
Face: Material 0 xyz (  42,  38,  41)
Face: Material 0 xyz (  43,  41,  40)
Face: Material 0 xyz (  44,  40,  37)
Face: Material 0 xyz (  27,  45,  37)
Face: Material 0 xyz (  45,  44,  37)
Face: Material 0 xyz (  44,  46,  40)
Face: Material 0 xyz (  40,  46,  43)
Face: Material 0 xyz (  45,  47,  44)
Face: Material 0 xyz (  44,  47,  46)
Face: Material 0 xyz (  48,  46,  47)
Face: Material 0 xyz (  49,  43,  46)
Face: Material 0 xyz (  49,  46,  50)
Face: Material 0 xyz (  51,  43,  49)
Face: Material 0 xyz (  52,  43,  51)
Face: Material 0 xyz (  45,  53,  47)
Face: Material 0 xyz (  53,  54,  47)
Face: Material 0 xyz (  45,  55,  53)
Face: Material 0 xyz (  56,  53,  55)
Face: Material 0 xyz (  55,  45,  57)
Face: Material 0 xyz (  45,  27,  57)
Face: Material 0 xyz (  57,  58,  55)
Face: Material 0 xyz (  55,  58,  59)
Face: Material 0 xyz (  55,  59,  60)
Face: Material 0 xyz (  58,  61,  59)
Face: Material 0 xyz (  61,  62,  59)
Face: Material 0 xyz (  61,  63,  62)
Face: Material 0 xyz (  58,  64,  61)
Face: Material 0 xyz (  64,  63,  61)
Face: Material 0 xyz (  57,  64,  58)
Face: Material 0 xyz (  64,  65,  63)
Face: Material 0 xyz (  57,  66,  64)
Face: Material 0 xyz (  57,  27,  66)
Face: Material 0 xyz (  66,  67,  64)
Face: Material 0 xyz (  66,  68,  67)
Face: Material 0 xyz (  67,  68,  69)
Face: Material 0 xyz (  66,  27,  70)
Face: Material 0 xyz (  71,  70,  27)
Face: Material 0 xyz (  70,  71,  72)
Face: Material 0 xyz (  75,  74,  73)
Face: Material 0 xyz (  78,  77,  76)
Face: Material 0 xyz (  81,  80,  79)
Face: Material 0 xyz (  84,  83,  82)
Face: Material 0 xyz (  87,  86,  85)
Face: Material 0 xyz (  41,  87,  88)
Face: Material 0 xyz (  35,  90,  89)
Face: Material 0 xyz (  92,  91,  42)
Face: Material 0 xyz (  94,  93,  42)
Face: Material 0 xyz (  42,  95,  94)
Face: Material 0 xyz (  98,  97,  96)
Face: Material 0 xyz ( 101, 100,  99)
Face: Material 0 xyz ( 104, 103, 102)
Face: Material 0 xyz ( 107, 106, 105)
Face: Material 0 xyz ( 109, 108, 105)
Face: Material 0 xyz ( 112, 111, 110)
Face: Material 0 xyz ( 114, 113, 110)
Face: Material 0 xyz ( 116, 114, 115)
Face: Material 0 xyz ( 116, 117, 114)
Face: Material 0 xyz ( 114, 117, 118)
Face: Material 0 xyz ( 114, 118, 119)
Face: Material 0 xyz ( 118, 120, 119)
Face: Material 0 xyz ( 116, 121, 117)
Face: Material 0 xyz ( 121, 122, 117)
Face: Material 0 xyz ( 122, 123, 117)
Face: Material 0 xyz ( 117, 123, 124)
Face: Material 0 xyz ( 122, 125, 123)
Face: Material 0 xyz ( 122, 126, 125)
Face: Material 0 xyz ( 121, 126, 122)
Face: Material 0 xyz ( 127, 126, 121)
Face: Material 0 xyz ( 116, 127, 121)
Face: Material 0 xyz ( 128, 126, 127)
Face: Material 0 xyz ( 127, 116, 129)
Face: Material 0 xyz ( 129, 130, 127)
Face: Material 0 xyz ( 129, 116, 131)
Face: Material 0 xyz ( 133, 132, 131)
Face: Material 0 xyz ( 134, 132, 133)
Face: Material 0 xyz ( 134, 135, 132)
Face: Material 0 xyz ( 134, 136, 135)
Face: Material 0 xyz ( 135, 138, 137)
Face: Material 0 xyz ( 136, 140, 139)
Face: Material 0 xyz ( 143, 142, 141)
Face: Material 0 xyz ( 146, 145, 144)
Face: Material 0 xyz ( 144, 148, 147)
Face: Material 0 xyz ( 148, 149, 147)
Face: Material 0 xyz ( 149, 148, 150)
Face: Material 0 xyz ( 148, 151, 150)
Face: Material 0 xyz ( 152, 149, 150)
Face: Material 0 xyz ( 149, 153, 147)
Face: Material 0 xyz ( 154, 147, 153)
Face: Material 0 xyz ( 155, 147, 154)
Face: Material 0 xyz ( 155, 154, 156)
Face: Material 0 xyz ( 153, 149, 157)
Face: Material 0 xyz ( 157, 149, 158)
Face: Material 0 xyz ( 159, 153, 157)
Face: Material 0 xyz ( 154, 153, 159)
Face: Material 0 xyz ( 157, 160, 159)
Face: Material 0 xyz ( 156, 154, 161)
Face: Material 0 xyz ( 161, 154, 159)
Face: Material 0 xyz ( 156, 161, 162)
Face: Material 0 xyz ( 156, 162, 163)
Face: Material 0 xyz ( 162, 161, 164)
Face: Material 0 xyz ( 161, 159, 164)
Face: Material 0 xyz ( 164, 165, 162)
Face: Material 0 xyz ( 159, 166, 164)
Face: Material 0 xyz ( 166, 159, 167)
Face: Material 0 xyz ( 166, 168, 164)
Face: Material 0 xyz ( 164, 168, 169)
Face: Material 0 xyz ( 166, 170, 168)
Face: Material 0 xyz ( 166, 171, 170)
Face: Material 0 xyz ( 172, 170, 171)
Face: Material 0 xyz ( 173, 172, 171)
Face: Material 0 xyz ( 175, 167, 174)
Face: Material 0 xyz ( 158, 176, 174)
Face: Material 0 xyz ( 176, 158, 177)
Face: Material 0 xyz ( 158, 179, 178)
Face: Material 0 xyz ( 181, 176, 180)
Face: Material 0 xyz ( 184, 183, 182)
Face: Material 0 xyz ( 187, 186, 185)
Face: Material 0 xyz ( 189, 186, 188)
Face: Material 0 xyz ( 192, 191, 190)
Face: Material 0 xyz ( 195, 194, 193)
Face: Material 0 xyz ( 197, 196, 151)
Face: Material 0 xyz ( 200, 199, 198)
Face: Material 0 xyz ( 202, 200, 201)
Face: Material 0 xyz ( 204, 203, 202)
Face: Material 0 xyz ( 203, 205, 202)
Face: Material 0 xyz ( 207, 205, 206)
Face: Material 0 xyz ( 208, 205, 207)
Face: Material 0 xyz ( 210, 209, 208)
Face: Material 0 xyz ( 210, 211, 209)
Face: Material 0 xyz ( 212, 210, 208)
Face: Material 0 xyz ( 211, 210, 213)
Face: Material 0 xyz ( 212, 213, 210)
Face: Material 0 xyz ( 214, 213, 212)
Face: Material 0 xyz ( 215, 213, 214)
Face: Material 0 xyz ( 214, 160, 215)
Face: Material 0 xyz ( 160, 217, 216)
Face: Material 0 xyz ( 220, 219, 218)
Face: Material 0 xyz ( 219, 222, 221)
Face: Material 0 xyz ( 222, 223, 221)
Face: Material 0 xyz ( 225, 224, 219)
Face: Material 0 xyz ( 225, 226, 224)
Face: Material 0 xyz ( 227, 226, 225)
Face: Material 0 xyz ( 230, 229, 228)
Face: Material 0 xyz ( 228, 232, 231)
Face: Material 0 xyz ( 228, 233, 232)
Face: Material 0 xyz ( 233, 234, 232)
Face: Material 0 xyz ( 231, 236, 235)
Face: Material 0 xyz ( 238, 234, 237)
Face: Material 0 xyz ( 238, 237, 239)
Face: Material 0 xyz ( 240, 239, 237)
Face: Material 0 xyz ( 242, 238, 241)
Face: Material 0 xyz ( 241, 243, 242)
Face: Material 0 xyz ( 245, 241, 244)
Face: Material 0 xyz ( 244, 246, 245)
Face: Material 0 xyz ( 246, 247, 245)
Face: Material 0 xyz ( 247, 248, 245)
Face: Material 0 xyz ( 249, 245, 248)
Face: Material 0 xyz ( 250, 247, 246)
Face: Material 0 xyz ( 246, 244, 250)
Face: Material 0 xyz ( 251, 247, 250)
Face: Material 0 xyz ( 247, 251, 252)
Face: Material 0 xyz ( 253, 252, 251)
Face: Material 0 xyz ( 251, 250, 253)
Face: Material 0 xyz ( 252, 253, 254)
Face: Material 0 xyz ( 255, 254, 253)
Face: Material 0 xyz ( 256, 250, 244)
Face: Material 0 xyz ( 250, 256, 253)
Face: Material 0 xyz ( 253, 257, 255)
Face: Material 0 xyz ( 253, 256, 257)
Face: Material 0 xyz ( 244, 257, 256)
Face: Material 0 xyz ( 258, 255, 257)
Face: Material 0 xyz ( 257, 244, 259)
Face: Material 0 xyz ( 261, 260, 258)
Face: Material 0 xyz ( 260, 261, 262)
Face: Material 0 xyz ( 264, 262, 263)
Face: Material 0 xyz ( 259, 266, 265)
Face: Material 0 xyz ( 268, 266, 267)
Face: Material 0 xyz ( 270, 269, 259)
Face: Material 0 xyz ( 271, 259, 269)
Face: Material 0 xyz ( 271, 269, 272)
Face: Material 0 xyz ( 272, 274, 273)
Face: Material 0 xyz ( 277, 276, 275)
Face: Material 0 xyz ( 152, 279, 278)
Face: Material 0 xyz ( 282, 281, 280)
Face: Material 0 xyz ( 285, 284, 283)
Face: Material 0 xyz ( 288, 287, 286)
Face: Material 0 xyz ( 291, 290, 289)
Face: Material 0 xyz ( 294, 293, 292)
Face: Material 0 xyz ( 292, 296, 295)
Face: Material 0 xyz ( 298, 295, 297)
Face: Material 0 xyz ( 300, 298, 299)
Face: Material 0 xyz ( 302, 301, 299)
Face: Material 0 xyz ( 301, 304, 303)
Face: Material 0 xyz ( 307, 306, 305)
Face: Material 0 xyz ( 309, 308, 306)
Face: Material 0 xyz (  56, 310, 308)
Face: Material 0 xyz ( 312,  56, 311)
Face: Material 0 xyz ( 315, 314, 313)
Face: Material 0 xyz ( 324, 323, 322)
Face: Material 0 xyz ( 327, 326, 325)
Face: Material 0 xyz ( 330, 329, 328)
Face: Material 0 xyz ( 333, 332, 331)
Face: Material 0 xyz ( 336, 335, 334)
Face: Material 0 xyz ( 339, 338, 337)
Face: Material 0 xyz ( 341, 339, 340)
Face: Material 0 xyz ( 342, 339, 341)
Face: Material 0 xyz ( 345, 344, 343)
Face: Material 0 xyz ( 348, 347, 346)
Face: Material 0 xyz (  39, 350, 349)
Face: Material 0 xyz ( 353, 352, 351)
Face: Material 0 xyz ( 356, 355, 354)
Face: Material 0 xyz ( 362, 361, 360)
Face: Material 0 xyz ( 365, 364, 363)
Face: Material 0 xyz ( 368, 367, 366)
Face: Material 0 xyz ( 371, 370, 369)
Face: Material 0 xyz ( 374, 373, 372)
Face: Material 0 xyz ( 377, 376, 375)
Face: Material 0 xyz ( 380, 379, 378)
Face: Material 0 xyz ( 383, 382, 381)
Face: Material 0 xyz ( 386, 385, 384)
Face: Material 0 xyz ( 389, 388, 387)
Face: Material 0 xyz ( 392, 391, 390)
Face: Material 0 xyz ( 395, 394, 393)
Face: Material 0 xyz ( 398, 397, 396)
Face: Material 0 xyz ( 401, 400, 399)
Face: Material 0 xyz ( 404, 403, 402)
Face: Material 0 xyz ( 406, 405,  54)
Face: Material 0 xyz ( 409, 408, 407)
Face: Material 0 xyz ( 407, 411, 410)
Face: Material 0 xyz ( 411, 413, 412)
Face: Material 0 xyz ( 416, 415, 414)
Face: Material 0 xyz ( 419, 418, 417)
Face: Material 0 xyz ( 422, 421, 420)
Face: Material 0 xyz ( 425, 424, 423)
Face: Material 0 xyz ( 428, 427, 426)
Face: Material 0 xyz ( 431, 430, 429)
Face: Material 0 xyz ( 434, 433, 432)
Face: Material 0 xyz ( 433, 435, 432)
Face: Material 0 xyz ( 438, 437, 436)
Face: Material 0 xyz ( 438, 436, 439)
Face: Material 0 xyz ( 439, 440, 438)
Face: Material 0 xyz ( 443, 442, 441)
Face: Material 0 xyz ( 442, 444, 441)
Face: Material 0 xyz ( 442, 445, 444)
Face: Material 0 xyz ( 448, 447, 446)
Face: Material 0 xyz ( 446, 447, 449)
Face: Material 0 xyz ( 452, 451, 450)
Face: Material 0 xyz ( 453, 450, 451)
Face: Material 0 xyz ( 456, 455, 454)
Face: Material 0 xyz ( 455, 457, 454)
Face: Material 0 xyz ( 460, 459, 458)
Face: Material 0 xyz ( 460, 461, 459)
Face: Material 0 xyz ( 466, 464, 465)
Face: Material 0 xyz ( 469, 468, 467)
Face: Material 0 xyz ( 467, 470, 469)
Face: Material 0 xyz ( 473, 472, 471)
Face: Material 0 xyz ( 471, 474, 473)
Face: Material 0 xyz ( 477, 476, 475)
Face: Material 0 xyz ( 478, 475, 476)
Face: Material 0 xyz ( 475, 478, 479)
Face: Material 0 xyz ( 482, 481, 480)
Face: Material 0 xyz ( 482, 483, 481)
Face: Material 0 xyz ( 486, 485, 484)
Face: Material 0 xyz ( 487, 484, 485)
Face: Material 0 xyz ( 490, 489, 488)
Face: Material 0 xyz ( 491, 489, 490)"""

    another_input_data = '''
    Face: Material 0 xyz (   4,   6,   3) uv (   0,   1,   2) edge (1, 1, 1) group 1
Face: Material 0 xyz (  16,   0,  18) uv (   3,   4,   5) edge (1, 1, 1) group 1
Face: Material 0 xyz (   2,   0,   1) uv (   6,   4,   7) edge (1, 1, 1) group 1
Face: Material 0 xyz (  13,   6,   5) uv (   8,   1,   9) edge (1, 1, 1) group 1
Face: Material 0 xyz (   1,   3,   6) uv (   7,   2,   1) edge (1, 1, 1) group 1
Face: Material 0 xyz (   6,  13,   2) uv (   1,   8,   6) edge (1, 1, 1) group 1
Face: Material 0 xyz (  12,   0,   9) uv (  10,   4,  11) edge (1, 1, 1) group 1
Face: Material 0 xyz (   6,   2,   1) uv (   1,   6,   7) edge (1, 1, 1) group 1
Face: Material 0 xyz (   4,   3,  15) uv (   0,   2,  12) edge (1, 1, 1) group 1
Face: Material 0 xyz (  16,  15,   3) uv (   3,  12,   2) edge (1, 1, 1) group 1
Face: Material 0 xyz (  18,   0,  12) uv (   5,   4,  10) edge (1, 1, 1) group 1
Face: Material 0 xyz (   1,  16,   3) uv (   7,   3,   2) edge (1, 1, 1) group 1
Face: Material 0 xyz (   4,   5,   6) uv (   0,   9,   1) edge (1, 1, 1) group 1
Face: Material 0 xyz (  16,   1,   0) uv (   3,   7,   4) edge (1, 1, 1) group 1
Face: Material 0 xyz (   2,   9,   0) uv (   6,  11,   4) edge (1, 1, 1) group 1
Face: Material 0 xyz (   2,  14,   9) uv (  13,  14,  15) edge (1, 1, 1) group 1
Face: Material 0 xyz (  19,  16,  18) uv (  16,  17,  18) edge (1, 1, 1) group 1
Face: Material 0 xyz (   4,  11,   5) uv (  19,  20,  21) edge (1, 1, 1) group 1
Face: Material 0 xyz (   8,   5,   7) uv (  22,  21,  23) edge (1, 1, 1) group 1
Face: Material 0 xyz (   5,   8,  13) uv (  21,  22,  24) edge (1, 1, 1) group 1
Face: Material 0 xyz (   8,  14,  13) uv (  22,  14,  24) edge (1, 1, 1) group 1
Face: Material 0 xyz (  10,   9,  14) uv (  25,  15,  14) edge (1, 1, 1) group 1
Face: Material 0 xyz (   4,   7,  11) uv (  19,  23,  20) edge (1, 1, 1) group 1
Face: Material 0 xyz (   5,  11,   7) uv (  21,  20,  23) edge (1, 1, 1) group 1
Face: Material 0 xyz (  12,   9,  10) uv (  26,  15,  25) edge (1, 1, 1) group 1
Face: Material 0 xyz (   8,  10,  14) uv (  22,  25,  14) edge (1, 1, 1) group 1
Face: Material 0 xyz (   7,   4,  17) uv (  23,  19,  27) edge (1, 1, 1) group 1
Face: Material 0 xyz (  15,  17,   4) uv (  28,  27,  19) edge (1, 1, 1) group 1
Face: Material 0 xyz (  15,  19,  17) uv (  28,  16,  27) edge (1, 1, 1) group 1
Face: Material 0 xyz (  19,  18,  20) uv (  16,  18,  29) edge (1, 1, 1) group 1
Face: Material 0 xyz (  20,  18,  12) uv (  29,  18,  26) edge (1, 1, 1) group 1
Face: Material 0 xyz (  19,  20,  17) uv (  16,  29,  27) edge (1, 1, 1) group 1
Face: Material 0 xyz (  12,  21,  20) uv (  26,  30,  29) edge (1, 1, 1) group 1
Face: Material 0 xyz (  21,  22,  17) uv (  30,  31,  27) edge (1, 1, 1) group 1
Face: Material 0 xyz (  21,  17,  20) uv (  30,  27,  29) edge (1, 1, 1) group 1
Face: Material 0 xyz (  17,  22,   7) uv (  27,  31,  23) edge (1, 1, 1) group 1
Face: Material 0 xyz (  12,  10,  21) uv (  26,  25,  30) edge (1, 1, 1) group 1
Face: Material 0 xyz (   8,  22,  21) uv (  22,  31,  30) edge (1, 1, 1) group 1
Face: Material 0 xyz (   8,  21,  10) uv (  22,  30,  25) edge (1, 1, 1) group 1
Face: Material 0 xyz (  22,   8,   7) uv (  31,  22,  23) edge (1, 1, 1) group 1
Face: Material 0 xyz (   2,  13,  14) uv (  13,  24,  14) edge (1, 1, 1) group 1
Face: Material 0 xyz (  19,  15,  16) uv (  16,  28,  17) edge (1, 1, 1) group 1'''

    app(another_input_data)
