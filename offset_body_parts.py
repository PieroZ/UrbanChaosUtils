import os.path

import glob
import json
from pathlib import Path
import shutil

from itertools import zip_longest

import numpy as np


def calc_offset(parent_vector, child_vector):
    offset_vector = [0, 0, 0]
    offset_vector[0] = parent_vector[0] - child_vector[0]
    offset_vector[1] = parent_vector[1] - child_vector[1]
    offset_vector[2] = parent_vector[2] - child_vector[2]

    return offset_vector


def grab_obj(filename):
    with open(filename, 'r') as file:
        obj_content = file.readlines()

    return obj_content


def write_new_obj(filename, lines_from_old_obj, offsets):
    with open(filename, 'w') as file:
        for line in lines_from_old_obj:
            elements = line.split()

            if elements and elements[0] == 'v':
                # Extract x, y, z values
                x, y, z = map(float, elements[1:])

                # Apply offsets
                x += offsets[0]
                y += offsets[1]
                z += offsets[2]

                # Write the modified vertex to the output file
                file.write(f'v {x} {y} {z}\n')
            else:
                # Write non-vertex lines unchanged
                file.write(line)


def overwrite_vertices_in_obj(filename, lines_from_old_obj, new_vertices):
    with open(filename, 'w') as file:
        for line, new_vertex in zip_longest(lines_from_old_obj, new_vertices):
            elements = line.split()

            if elements and elements[0] == 'v':
                # Extract x, y, z values
                x, y, z = map(float, elements[1:])

                # Apply offsets
                x = new_vertex[0][0]
                y = new_vertex[0][1]
                z = new_vertex[0][2]

                # Write the modified vertex to the output file
                file.write(f'v {x} {y} {z}\n')
            else:
                # Write non-vertex lines unchanged
                file.write(line)


def copy_materials(src_dir, dst_dir):
    all_files_list = []
    for filename in glob.iglob(f'{src_dir}/*.mtl'):
        mtl_filename = os.path.basename(filename)
        all_files_list.append(filename)
        dst_path = dst_dir + "/" + mtl_filename

        shutil.copyfile(filename, dst_path)

    # print(all_files_list)


def grab_files_with_extension(directory, ext):
    all_files_list = []
    for filename in glob.iglob(f'{directory}{ext}'):
        all_files_list.append(os.path.basename(filename))

    return all_files_list


def grab_filepaths_with_extension(directory, ext):
    all_files_list = []
    for filename in glob.iglob(f'{directory}{ext}'):
        all_files_list.append(filename)

    return all_files_list


def read_json_file(filepath):
    # reading the data from the file
    with open(filepath) as f:
        data = f.read()

    # print("Data type before reconstruction : ", type(data))

    # reconstructing the data as a dictionary
    js = json.loads(data)

    # print("Data type after reconstruction : ", type(js))
    # print(js)

    return js


def only_in_death_does_duty_end():
    pelvis00 = np.array([
        [0.94716243, 0.2739726, -0.16634051],
        [-0.27592955, 0.962818, 0.01956947],
        [0.16438356, 0.02544031, 0.98630137]
    ])

    lfemur00 = np.array([
        [0.90802348, -0.38551859, -0.17612524],
        [0.31311155, 0.89236791, -0.33072407],
        [0.27984344, 0.24266145, 0.9295499]
    ])

    ltibia00 = np.array([
        [0.90606654, -0.29745597, -0.30528376],
        [0.31506849, 0.94911937, 0.02152642],
        [0.27984344, -0.11545988, 0.95303327]
    ])

    lfoot00 = np.array([
        [0.97455969, 0.02544031, -0.23091977],
        [-0.01565558, 0.99804305, 0.05283757],
        [0.22896282, -0.05088063, 0.97260274]
    ])

    torso00 = np.array([
        [0.97260274, -0.19765166, 0.1369863],
        [0.20939335, 0.97455969, -0.08414873],
        [-0.11937378, 0.10763209, 0.98825832]
    ])

    rhumorus00 = np.array([
        [0.76908023, 0.41682975, 0.48336595],
        [-0.48923679, 0.87279843, 0.02152642],
        [-0.4148728, -0.25440313, 0.87671233]
    ])

    rradius00 = np.array([
        [0.78082192, -0.62426614, 0.05283757],
        [0.54990215, 0.64383562, -0.53620352],
        [0.29745597, 0.44618395, 0.84540117]
    ])

    rhand00 = np.array([
        [0.98434442, 0.1702544, 0.0665362],
        [-0.04109589, 0.56164384, -0.82778865],
        [-0.18003914, 0.81017613, 0.55968689]
    ])

    lhumorus00 = np.array([
        [0.97260274, 0.03131115, 0.23679061],
        [-0.06849315, 0.98825832, 0.14285714],
        [-0.23287671, -0.15655577, 0.96086106]
    ])

    lradius00 = np.array([
        [0.95694716, -0.16829746, 0.23874755],
        [0.09001957, 0.95107632, 0.29745597],
        [-0.27984344, -0.26418787, 0.92563601]
    ])

    lhand00 = np.array([
        [0.97064579, 0.08219178, 0.22896282],
        [-0.1369863, 0.9667319, 0.22504892],
        [-0.2035225, -0.25048924, 0.94716243]
    ])

    skull00 = np.array([
        [0.63796477, -0.09784736, -0.76712329],
        [0.18003914, 0.98434442, 0.02544031],
        [0.74951076, -0.15655577, 0.64579256]
    ])

    rfemur00 = np.array([
        [0.98434442, 0.01956947, -0.18199609],
        [-0.02348337, 1., -0.00782779],
        [0.18003914, 0.00978474, 0.98434442]
    ])

    rtibia00 = np.array([
        [0.98434442, 0.01956947, -0.17612524],
        [-0.00978474, 0.99804305, 0.07240705],
        [0.17612524, -0.07240705, 0.98238748]
    ])

    rfoot00 = np.array([
        [0.95107632, -0.02348337, 0.31311155],
        [0.01565558, 1., 0.01761252],
        [-0.31506849, -0.01174168, 0.95107632]
    ])

    hikari_ga_nagareru = {"pelvis00": pelvis00,
                          "lfemur00": lfemur00,
                          "ltibia00": ltibia00,
                          "lfoot00": lfoot00,
                          "torso00": torso00,
                          "rhumorus00": rhumorus00,
                          "rradius00": rradius00,
                          "rhand00": rhand00,
                          "lhumorus00": lhumorus00,
                          "lradius00": lradius00,
                          "lhand00": lhand00,
                          "skull00": skull00,
                          "rfemur00": rfemur00,
                          "rtibia00": rtibia00,
                          "rfoot00": rfoot00}

    for key, value in hikari_ga_nagareru.items():
        # prim_data_path = "output/all-obj/darci1/0/" + key + ".obj"
        prim_data_path = "output/frames-per-anim-file/darci1/0/" + key + ".obj"

        new_prim_data_path = "output/frames-per-anim-file/darci1/0/PZI_" + key + ".obj"

        obj_vertices = read_vertex(prim_data_path)
        np_array = np.asarray(obj_vertices, dtype=np.float32)

        new_vertices = []
        for vertex in np_array:
            just_shoot_me_in_the_face = np.matmul(value, vertex)
            print(just_shoot_me_in_the_face)
            new_vertices.append(just_shoot_me_in_the_face)

        lines_from_original_obj = grab_obj(prim_data_path)
        overwrite_vertices_in_obj(new_prim_data_path, lines_from_original_obj, new_vertices)


def tests2():
    only_in_death_does_duty_end()


def test():
    # filepaths = grab_all_files_in_directory("output/body-part-offsets/anim003/*")
    #
    # for filepath in filepaths:
    #     read_json_file(filepath)

    prim_data_path = "output/all-obj/darci1/0/pelvis00.obj"
    obj_vertices = read_vertex(prim_data_path)
    np_array = np.asarray(obj_vertices, dtype=np.float32)

    print(np_array)

    rot_matrices = np.array([
        [0.94716243, 0.2739726, -0.16634051],
        [-0.27592955, 0.962818, 0.01956947],
        [0.16438356, 0.02544031, 0.98630137]
    ])

    just_shoot_me_in_the_face = np.matmul(np_array[0], rot_matrices)

    print(just_shoot_me_in_the_face)


def read_vertex(filename):
    vertices = []
    with open(filename, 'r') as file:
        lines_from_old_obj = file.readlines()
        for line in lines_from_old_obj:
            elements = line.split()

            if elements and elements[0] == 'v':
                # Extract x, y, z values
                x, y, z = map(float, elements[1:])

                # print(f'{x}, {y}, {z}')

                vertices.append([x, y, z])

    return vertices


def apply_rotations(rotation_files, anim_file):
    for index, filepath in enumerate(rotation_files):
        rotation_json = read_json_file(filepath)

        for key, value in rotation_json.items():
            prim_data_path = "output/all-obj/" + anim_file + "/0/" + key + ".obj"

            actual_index = int(filepath[filepath.find('rotation_matrix_frame')+len('rotation_matrix_frame')+1:-5])
            # prim_data_path = "output/frames-per-anim-file/darci1/" + str(index) + "/" + key + ".obj"

            # new_prim_data_path = "output/frames-per-anim-file/darci1/0/PZI_" + key + ".obj"

            # we override existing file
            frame_path = "output/frames-per-anim-file/" + anim_file + "/" + str(actual_index)
            new_prim_data_path = "output/frames-per-anim-file/" + anim_file + "/" + str(actual_index) + "/" + key + ".obj"

            Path(frame_path).mkdir(parents=True, exist_ok=True)

            obj_vertices = read_vertex(prim_data_path)
            np_array = np.asarray(obj_vertices, dtype=np.float32)

            numpy_value = np.asarray(value, dtype=np.float32)

            new_vertices = []
            for vertex in np_array:
                just_shoot_me_in_the_face = np.matmul(numpy_value, vertex)
                # print(just_shoot_me_in_the_face)
                new_vertices.append(just_shoot_me_in_the_face)

            lines_from_original_obj = grab_obj(prim_data_path)
            overwrite_vertices_in_obj(new_prim_data_path, lines_from_original_obj, new_vertices)


def app():
    # baalrog
    anim_file = "anim003"

    # doggy
    anim_file = "anim013"
    # anim_file = "gargoyle"

    # anim_file = "banesuit"
    anim_file = "TESTdarci1"


    body_parts_offsets_filepaths = grab_filepaths_with_extension("output/body-part-offsets/" + anim_file + "/*", '.txt')
    rotation_files = grab_filepaths_with_extension("output/body-part-offsets/" + anim_file + "/*", '.json')

    # body_parts_offsets_filepaths = ["output/body-part-offsets/" + anim_file + "/frame 0.txt"]
    anim_directory_results_path = "output/frames-per-anim-file/" + anim_file
    Path(anim_directory_results_path).mkdir(parents=True, exist_ok=True)

    apply_rotations(rotation_files, anim_file)

    for index, filepath in enumerate(body_parts_offsets_filepaths):
        part_name_offset_dict = read_json_file(filepath)
        actual_index = int(filepath[filepath.find('frame ')+len('frame '):-4])
        single_frame_result_path = anim_directory_results_path + "/" + str(actual_index)
        Path(single_frame_result_path).mkdir(parents=True, exist_ok=True)

        for body_part_name, offset in part_name_offset_dict.items():
            body_part_name = body_part_name
            # body_part_obj_path = "output/all-obj/" + anim_file + "/0/" + body_part_name + ".obj"

            # body_part_obj_path = single_frame_result_path + "/PZI_" + body_part_name + ".obj"
            body_part_obj_path = single_frame_result_path + "/" + body_part_name + ".obj"

            # body_part_obj_path = "output/all-obj/BAALROG/with-textures/" + body_part_name
            lines = grab_obj(body_part_obj_path)
            # left femur
            # base_position = [10, 91, 1]
            # right femur
            # base_position = [-5, 89, 4]
            # parent_base_position = [0, 101, -3]
            # offset_vector = calc_offset(parent_base_position, base_position)
            offset_vector = offset
            # pzi_output_file_name = single_frame_result_path + "/DUPA_" + body_part_name + ".obj"
            # we override existing file so we don't have to rename it later
            pzi_output_file_name = single_frame_result_path + "/" + body_part_name + ".obj"
            write_new_obj(pzi_output_file_name, lines, offset_vector)

            src_dir = "output/all-obj/" + anim_file + "/0"
            copy_materials(src_dir, single_frame_result_path)
            # print(index)
        print(index)


if __name__ == '__main__':
    app()
