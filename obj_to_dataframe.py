import pandas as pd


def grab_dst_textures(obj_filepath):
    dst_textures = []
    mtl_names = []
    mtl_file_path = (obj_filepath[:-4] + '.mtl')
    lines = extract_obj_file(mtl_file_path)
    for line in lines:
        if line.startswith("map_Kd "):
            dst_textures.append(line[7:])
        elif line.startswith("newmtl "):
            mtl_names.append(line[7:-1])

    return [dst_textures, mtl_names]


def extract_texture_number_from_texture_filename(texture_filename):
    return int(texture_filename[-9:-6])
    # return int(texture_filename[-10:-7])


def calculate_texture_page_and_uv_offsets(texture_file_number):
    page = texture_file_number + 64 * 11
    texture_page = int(page / 64)
    base_page = (texture_page - 11) * 64
    remainder = texture_file_number - base_page
    u_offset = remainder % 8
    v_offset = int(remainder / 8)

    result = (texture_page, u_offset, v_offset)

    return result


def extract_obj_file(obj_filepath):
    with open(obj_filepath, "r") as file:
        obj_file_content = file.readlines()

    return obj_file_content


def remove_new_line_character(line):
    line = line.replace('\n', '')

    return line


def split_points(line):
    split_lines = line.split(' ')

    return split_lines


def split_faces(line):
    split_lines = line.split(' ')

    return split_lines


def extract_points(obj_file_content):
    x_list = []
    y_list = []
    z_list = []
    scale = 1
    y_offset = 1

    # u_list = []
    # v_list = []

    uv_list = []

    for line in obj_file_content:
        if line.startswith("vn"):
            pass
            # print("Ignore vn")
        elif line.startswith("vt"):
            line = remove_new_line_character(line)
            [v_text, u, v] = split_points(line)
            # u_list.append(float(u))
            # v_list.append(float(v))
            uv_precision = 32
            uv_tuple = (int(float(u)*uv_precision), int(uv_precision - float(v)*uv_precision))
            uv_list.append(uv_tuple)
        elif line.startswith("v"):
            line = remove_new_line_character(line)
            [v_text, x, y, z] = split_points(line)
            # x_list.append(float(x))
            # y_list.append(float(y))
            # z_list.append(float(z))

            x_list.append(float(x) * scale)
            y_list.append(float(y) * scale + y_offset)
            z_list.append(float(z) * scale)
            # x_list.append(float(x) * 20)
            # y_list.append(float(y) * 20+80)
            # z_list.append(float(z) * 20)
            # x_list.append(float(x) * 100)
            # y_list.append(float(y) * 100 + 50)
            # z_list.append(float(z) * 100)

    d = {'x': x_list, 'y': y_list, 'z': z_list}
    df_points = pd.DataFrame(d)

    # d_uv = {'y': u_list, 'v': v_list}
    # df_uvs = pd.DataFrame(d_uv)

    return [df_points, uv_list]


def extract_first_value_from_obj_face(face):
    return face[0:face.find('/')]


def extract_second_value_from_obj_face(face):
    split_values = face.split('/')

    return int(split_values[1])


def assign_material_to_face(face_line_idx, material_line_id_dict):
    pass


def extract_faces(obj_file_content, uv_list, mtl_offsets_dict):

    texture_page = 14
    quadrangle_texture_page_list = []
    quadrangle_a_list = []
    quadrangle_b_list = []
    quadrangle_c_list = []
    quadrangle_d_list = []

    quadrangle_u_a_list = []
    quadrangle_u_b_list = []
    quadrangle_u_c_list = []
    quadrangle_u_d_list = []
    quadrangle_v_a_list = []
    quadrangle_v_b_list = []
    quadrangle_v_c_list = []
    quadrangle_v_d_list = []

    triangle_texture_page_list = []
    triangle_a_list = []
    triangle_b_list = []
    triangle_c_list = []

    triangle_u_a_list = []
    triangle_u_b_list = []
    triangle_u_c_list = []
    triangle_v_a_list = []
    triangle_v_b_list = []
    triangle_v_c_list = []

    material_line_occurrence_dict = {}
    previous_material = ''
    changing_material_points = []
    i = 0
    for i, line in enumerate(obj_file_content):
        if line.startswith("usemtl"):
            # lines below i should use this material until the eof or until next material appears
            if not material_line_occurrence_dict:
                material_line_occurrence_dict[line[7:-1]] = [i]
                previous_material = line[7:-1]
                changing_material_points.append(i)
            else:
                material_line_occurrence_dict[previous_material].extend([i - 1])
                material_line_occurrence_dict[line[7:-1]] = [i]
                previous_material = line[7:-1]
                changing_material_points.append(i)

    material_line_occurrence_dict[previous_material].extend([i])

    currently_used_material = None
    for i, line in enumerate(obj_file_content):
        if i in changing_material_points:
            for key, value in material_line_occurrence_dict.items():
                if i in range(value[0], value[1]):
                    currently_used_material = key
                    # print(mtl_offsets_dict[currently_used_material])

        if line.startswith("f"):
            line = remove_new_line_character(line)
            faces = split_faces(line)
            if len(faces) == 5:
                [f_name, a, b, c, d] = faces
                quadrangle_texture_page_list.append(mtl_offsets_dict[currently_used_material][0])

                uv_constant_multiplier = 32

                quadrangle_a_list.append((extract_first_value_from_obj_face(a)))
                quadrangle_b_list.append((extract_first_value_from_obj_face(b)))
                quadrangle_c_list.append((extract_first_value_from_obj_face(c)))
                quadrangle_d_list.append((extract_first_value_from_obj_face(d)))

                uv_a_id = extract_second_value_from_obj_face(a) - 1
                uv_list[uv_a_id] = list(uv_list[uv_a_id])
                temp_u = uv_list[uv_a_id][0] + mtl_offsets_dict[currently_used_material][1] * uv_constant_multiplier
                temp_v = uv_list[uv_a_id][1] + mtl_offsets_dict[currently_used_material][2] * uv_constant_multiplier

                quadrangle_u_a_list.append(temp_u)
                quadrangle_v_a_list.append(temp_v)

                uv_b_id = extract_second_value_from_obj_face(b) - 1
                uv_list[uv_b_id] = list(uv_list[uv_b_id])
                temp_u = uv_list[uv_b_id][0] + mtl_offsets_dict[currently_used_material][1] * uv_constant_multiplier
                temp_v = uv_list[uv_b_id][1] + mtl_offsets_dict[currently_used_material][2] * uv_constant_multiplier

                quadrangle_u_b_list.append(temp_u)
                quadrangle_v_b_list.append(temp_v)

                uv_c_id = extract_second_value_from_obj_face(c) - 1
                uv_list[uv_c_id] = list(uv_list[uv_c_id])
                temp_u = uv_list[uv_c_id][0] + mtl_offsets_dict[currently_used_material][1] * uv_constant_multiplier
                temp_v = uv_list[uv_c_id][1] + mtl_offsets_dict[currently_used_material][2] * uv_constant_multiplier

                quadrangle_u_c_list.append(temp_u)
                quadrangle_v_c_list.append(temp_v)

                uv_d_id = extract_second_value_from_obj_face(d) - 1
                uv_list[uv_d_id] = list(uv_list[uv_d_id])
                temp_u = uv_list[uv_d_id][0] + mtl_offsets_dict[currently_used_material][1] * uv_constant_multiplier
                temp_v = uv_list[uv_d_id][1] + mtl_offsets_dict[currently_used_material][2] * uv_constant_multiplier

                quadrangle_u_d_list.append(temp_u)
                quadrangle_v_d_list.append(temp_v)

                # print(f"average uv = {(uv_list[uv_a_id][0] + uv_list[uv_b_id][0] + uv_list[uv_c_id][0] + uv_list[uv_d_id][0])/4}")

            elif len(faces) == 4:
                [f_name, a, b, c] = faces
                triangle_texture_page_list.append(mtl_offsets_dict[currently_used_material][0])

                uv_constant_multiplier = 32

                triangle_a_list.append((extract_first_value_from_obj_face(a)))
                triangle_b_list.append((extract_first_value_from_obj_face(b)))
                triangle_c_list.append((extract_first_value_from_obj_face(c)))

                uv_a_id = extract_second_value_from_obj_face(a) - 1
                uv_list[uv_a_id] = list(uv_list[uv_a_id])
                temp_u = uv_list[uv_a_id][0] + mtl_offsets_dict[currently_used_material][1] * uv_constant_multiplier
                temp_v = uv_list[uv_a_id][1] + mtl_offsets_dict[currently_used_material][2] * uv_constant_multiplier

                triangle_u_a_list.append(temp_u)
                triangle_v_a_list.append(temp_v)

                uv_b_id = extract_second_value_from_obj_face(b) - 1
                uv_list[uv_b_id] = list(uv_list[uv_b_id])
                temp_u = uv_list[uv_b_id][0] + mtl_offsets_dict[currently_used_material][1] * uv_constant_multiplier
                temp_v = uv_list[uv_b_id][1] + mtl_offsets_dict[currently_used_material][2] * uv_constant_multiplier

                triangle_u_b_list.append(temp_u)
                triangle_v_b_list.append(temp_v)

                uv_c_id = extract_second_value_from_obj_face(c) - 1
                uv_list[uv_c_id] = list(uv_list[uv_c_id])
                temp_u = uv_list[uv_c_id][0] + mtl_offsets_dict[currently_used_material][1] * uv_constant_multiplier
                temp_v = uv_list[uv_c_id][1] + mtl_offsets_dict[currently_used_material][2] * uv_constant_multiplier

                triangle_u_c_list.append(temp_u)
                triangle_v_c_list.append(temp_v)

    quadrangles_dict = {
        # "texture_id_group": [texture_page] * len(quadrangle_a_list),
        "texture_id_group": quadrangle_texture_page_list,
        "properties": [2] * len(quadrangle_a_list),
        "point_a_id": quadrangle_b_list,
        "point_b_id": quadrangle_a_list,
        "point_c_id": quadrangle_d_list,
        "point_d_id": quadrangle_c_list,
        # "u_a": [0] * len(quadrangle_a_list),
        # "v_a": [0] * len(quadrangle_a_list),
        # "u_b": [0] * len(quadrangle_a_list),
        # "v_b": [0] * len(quadrangle_a_list),
        # "u_c": [0] * len(quadrangle_a_list),
        # "v_c": [0] * len(quadrangle_a_list),
        # "u_d": [0] * len(quadrangle_a_list),
        # "v_d": [0] * len(quadrangle_a_list),
        "u_a": quadrangle_u_a_list,
        "v_a": quadrangle_v_a_list,
        "u_b": quadrangle_u_b_list,
        "v_b": quadrangle_v_b_list,
        "u_c": quadrangle_u_c_list,
        "v_c": quadrangle_v_c_list,
        "u_d": quadrangle_u_d_list,
        "v_d": quadrangle_v_d_list,

        # "u_c": quadrangle_u_c_list,
        # "v_c": quadrangle_v_c_list,
        # "u_d": quadrangle_u_d_list,
        # "v_d": quadrangle_v_d_list,
        "bright_a": [64] * len(quadrangle_a_list),
        "bright_b": [0] * len(quadrangle_a_list),
        "bright_c": [64] * len(quadrangle_a_list),
        "bright_d": [0] * len(quadrangle_a_list),
        "thing_index": [0] * len(quadrangle_a_list),
        "col2": [64] * len(quadrangle_a_list),
        "face_flags": [0] * len(quadrangle_a_list),
        "type": [0] * len(quadrangle_a_list),
        "id": [0] * len(quadrangle_a_list)
    }

    df_quadrangles = pd.DataFrame(quadrangles_dict)

    triangles_dict = {
        # "texture_id_group": [texture_page] * len(triangle_a_list),
        "texture_id_group": triangle_texture_page_list,
        "properties": [2] * len(triangle_a_list),
        "point_a_id": triangle_c_list,
        "point_b_id": triangle_b_list,
        "point_c_id": triangle_a_list,
        # "u_a": [0] * len(triangle_a_list),
        # "v_a": [0] * len(triangle_a_list),
        # "u_b": [0] * len(triangle_a_list),
        # "v_b": [0] * len(triangle_a_list),
        # "u_c": [0] * len(triangle_a_list),
        # "v_c": [0] * len(triangle_a_list),

        "u_a": triangle_u_a_list,
        "v_a": triangle_v_a_list,
        "u_b": triangle_u_b_list,
        "v_b": triangle_v_b_list,
        "u_c": triangle_u_c_list,
        "v_c": triangle_v_c_list,
        "bright_a": [0] * len(triangle_a_list),
        "bright_b": [0] * len(triangle_a_list),
        "bright_c": [0] * len(triangle_a_list),
        "thing_index": [0] * len(triangle_a_list),
        "col2": [0] * len(triangle_a_list),
        "face_flags": [61696] * len(triangle_a_list),
        "type": [0] * len(triangle_a_list),
        "id": [0] * len(triangle_a_list)
    }

    df_triangles = pd.DataFrame(triangles_dict)

    return [df_triangles, df_quadrangles]


def extract_obj_to_df(obj_filepath):
    [dst_textures, mtl_names] = grab_dst_textures(obj_filepath)
    texture_numbers = []
    mtl_offsets_dict = {}
    for dst_texture in dst_textures:
        texture_numbers.append((extract_texture_number_from_texture_filename(dst_texture)))

    for texture_number, mtl_name in zip(texture_numbers, mtl_names):
        uv_tuple_offsets = calculate_texture_page_and_uv_offsets(texture_number)
        mtl_offsets_dict[mtl_name] = uv_tuple_offsets

    obj_file_content = extract_obj_file(obj_filepath)
    [df_points, uv_list] = extract_points(obj_file_content)
    [df_triangles, df_quadrangles] = extract_faces(obj_file_content, uv_list, mtl_offsets_dict)

    return [df_points, df_triangles, df_quadrangles]


if __name__ == '__main__':
    extract_obj_to_df("res/objs/test_uv_cube.obj")
