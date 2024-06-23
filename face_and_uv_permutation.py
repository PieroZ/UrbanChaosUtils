import re
from itertools import permutations


def parse_faces(input_data):
    face_pattern = re.compile(
        r"(Face: Material \d+ xyz \(\s*(\d+),\s*(\d+),\s*(\d+)\) uv \(\s*(\d+),\s*(\d+),\s*(\d+)\) edge \(\d+,\s*\d+,\s*\d+\) group \d+)"
    )
    faces = []
    for line in input_data.strip().split('\n'):
        match = face_pattern.match(line.strip())
        if match:
            face_str = match.group(1)
            xyz_values = tuple(map(int, match.groups()[1:4]))
            uv_values = tuple(map(int, match.groups()[4:7]))
            faces.append((face_str, xyz_values, uv_values))
    return faces


def generate_xyz_uv_variants(faces):
    xyz_permutations = list(permutations([0, 1, 2]))
    variants = []
    for perm in xyz_permutations:
        variant = []
        for face in faces:
            face_str, xyz_values, uv_values = face
            new_xyz = [xyz_values[i] for i in perm]
            new_uv = [uv_values[i] for i in perm]
            new_face = re.sub(
                r"xyz \(\s*\d+,\s*\d+,\s*\d+\) uv \(\s*\d+,\s*\d+,\s*\d+\)",
                f"xyz ({new_xyz[0]:4}, {new_xyz[1]:4}, {new_xyz[2]:4}) uv ({new_uv[0]:4}, {new_uv[1]:4}, {new_uv[2]:4})",
                face_str
            )
            variant.append(new_face)
        variants.append(variant)
    return variants


def generate_uv_only_variants(faces):
    uv_permutations = list(permutations([0, 1, 2]))
    variants = []
    for perm in uv_permutations:
        variant = []
        for face in faces:
            face_str, xyz_values, uv_values = face
            new_uv = [uv_values[i] for i in perm]
            new_face = re.sub(
                r"uv \(\s*\d+,\s*\d+,\s*\d+\)",
                f"uv ({new_uv[0]:4}, {new_uv[1]:4}, {new_uv[2]:4})",
                face_str
            )
            variant.append(new_face)
        variants.append(variant)
    return variants


def main():
    input_data = '''
Face: Material 0 xyz (   3,   6,   4) uv (   2,   1,   0) edge (1, 1, 1) group 1
Face: Material 0 xyz (  18,   0,  16) uv (   5,   4,   3) edge (1, 1, 1) group 1
Face: Material 0 xyz (   1,   0,   2) uv (   7,   4,   6) edge (1, 1, 1) group 1
Face: Material 0 xyz (   5,   6,  13) uv (   9,   1,   8) edge (1, 1, 1) group 1
Face: Material 0 xyz (   6,   3,   1) uv (   1,   2,   7) edge (1, 1, 1) group 1
Face: Material 0 xyz (   2,  13,   6) uv (   6,   8,   1) edge (1, 1, 1) group 1
Face: Material 0 xyz (   9,   0,  12) uv (  11,   4,  10) edge (1, 1, 1) group 1
Face: Material 0 xyz (   1,   2,   6) uv (   7,   6,   1) edge (1, 1, 1) group 1
Face: Material 0 xyz (  15,   3,   4) uv (  12,   2,   0) edge (1, 1, 1) group 1
Face: Material 0 xyz (   3,  15,  16) uv (   2,  12,   3) edge (1, 1, 1) group 1
Face: Material 0 xyz (  12,   0,  18) uv (  10,   4,   5) edge (1, 1, 1) group 1
Face: Material 0 xyz (   3,  16,   1) uv (   2,   3,   7) edge (1, 1, 1) group 1
Face: Material 0 xyz (   6,   5,   4) uv (   1,   9,   0) edge (1, 1, 1) group 1
Face: Material 0 xyz (   0,   1,  16) uv (   4,   7,   3) edge (1, 1, 1) group 1
Face: Material 0 xyz (   0,   9,   2) uv (   4,  11,   6) edge (1, 1, 1) group 1
Face: Material 0 xyz (   9,  14,   2) uv (  15,  14,  13) edge (1, 1, 1) group 1
Face: Material 0 xyz (  18,  16,  19) uv (  18,  17,  16) edge (1, 1, 1) group 1
Face: Material 0 xyz (   5,  11,   4) uv (  21,  20,  19) edge (1, 1, 1) group 1
Face: Material 0 xyz (   7,   5,   8) uv (  23,  21,  22) edge (1, 1, 1) group 1
Face: Material 0 xyz (  13,   8,   5) uv (  24,  22,  21) edge (1, 1, 1) group 1
Face: Material 0 xyz (  13,  14,   8) uv (  24,  14,  22) edge (1, 1, 1) group 1
Face: Material 0 xyz (  14,   9,  10) uv (  14,  15,  25) edge (1, 1, 1) group 1
Face: Material 0 xyz (  11,   7,   4) uv (  20,  23,  19) edge (1, 1, 1) group 1
Face: Material 0 xyz (   7,  11,   5) uv (  23,  20,  21) edge (1, 1, 1) group 1
Face: Material 0 xyz (  10,   9,  12) uv (  25,  15,  26) edge (1, 1, 1) group 1
Face: Material 0 xyz (  14,  10,   8) uv (  14,  25,  22) edge (1, 1, 1) group 1
Face: Material 0 xyz (  17,   4,   7) uv (  27,  19,  23) edge (1, 1, 1) group 1
Face: Material 0 xyz (   4,  17,  15) uv (  19,  27,  28) edge (1, 1, 1) group 1
Face: Material 0 xyz (  17,  19,  15) uv (  27,  16,  28) edge (1, 1, 1) group 1
Face: Material 0 xyz (  20,  18,  19) uv (  29,  18,  16) edge (1, 1, 1) group 1
Face: Material 0 xyz (  12,  18,  20) uv (  26,  18,  29) edge (1, 1, 1) group 1
Face: Material 0 xyz (  17,  20,  19) uv (  27,  29,  16) edge (1, 1, 1) group 1
Face: Material 0 xyz (  20,  21,  12) uv (  29,  30,  26) edge (1, 1, 1) group 1
Face: Material 0 xyz (  17,  22,  21) uv (  27,  31,  30) edge (1, 1, 1) group 1
Face: Material 0 xyz (  20,  17,  21) uv (  29,  27,  30) edge (1, 1, 1) group 1
Face: Material 0 xyz (   7,  22,  17) uv (  23,  31,  27) edge (1, 1, 1) group 1
Face: Material 0 xyz (  21,  10,  12) uv (  30,  25,  26) edge (1, 1, 1) group 1
Face: Material 0 xyz (  21,  22,   8) uv (  30,  31,  22) edge (1, 1, 1) group 1
Face: Material 0 xyz (  10,  21,   8) uv (  25,  30,  22) edge (1, 1, 1) group 1
Face: Material 0 xyz (   7,   8,  22) uv (  23,  22,  31) edge (1, 1, 1) group 1
Face: Material 0 xyz (  14,  13,   2) uv (  14,  24,  13) edge (1, 1, 1) group 1
Face: Material 0 xyz (  16,  15,  19) uv (  17,  28,  16) edge (1, 1, 1) group 1
'''

    faces = parse_faces(input_data)

    # # Generate variants with permutations on both XYZ and UV values
    # xyz_uv_variants = generate_xyz_uv_variants(faces)
    # print("Variants with permutations on XYZ and UV values:\n")
    # for i, variant in enumerate(xyz_uv_variants):
    #     print(f"Variant {i + 1}:\n")
    #     for face in variant:
    #         print(face)
    #     print("\n")

    # Generate variants with permutations on UV values only
    uv_only_variants = generate_uv_only_variants(faces)
    print("Variants with permutations on UV values only:\n")
    for i, variant in enumerate(uv_only_variants):
        print(f"Variant {i + 1}:\n")
        for face in variant:
            print(face)
        print("\n")


if __name__ == '__main__':
    main()
