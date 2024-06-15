import numpy as np
from obj_to_dataframe import *


def read_nprim(nprim_file_name):
    with open(nprim_file_name, "rb+") as file:
        file_chunk = file.read()

    return file_chunk


def search_in_binary(binary_data, search_string):
    search_bytes = search_string.encode()  # Convert string to bytes
    position = binary_data.find(search_bytes)  # Find the position of the byte sequence

    if position != -1:
        return position
    else:
        return None


def remove_section(binary_data, start_position, end_position):
    """
    Remove a section of binary data between start_position and end_position.
    :param binary_data: The original binary data
    :param start_position: The starting position of the section to remove
    :param end_position: The ending position of the section to remove
    :return: New binary data with the specified section removed
    """
    if start_position < 0 or end_position > len(binary_data) or start_position >= end_position:
        raise ValueError("Invalid start or end position")

    # Extract parts before the start position and after the end position
    before_section = binary_data[:start_position]
    after_section = binary_data[end_position:]

    # Concatenate the two parts
    new_binary_data = before_section + after_section

    return new_binary_data


def insert_section(binary_data, start_position, second_position, appended_binary_data):
    """
    Insert a section of binary data at a specified position.
    :param binary_data: The original binary data
    :param start_position: The position to insert the new binary data
    :param appended_binary_data: The binary data to append
    :return: New binary data with the specified section inserted
    """
    if start_position < 0 or start_position > len(binary_data):
        raise ValueError("Invalid start position")

    # Extract parts before the start position and after the start position
    before_section = binary_data[:start_position]
    after_section = binary_data[second_position:]

    # Concatenate the parts with the new binary data in between
    new_binary_data = before_section + appended_binary_data + after_section

    return new_binary_data


def convert_nprim_binary_to_readable_data(starting_point, next_prim_point, data):

    null_terminated_pos = data[starting_point:].find(b'\00')
    name = data[starting_point:starting_point+null_terminated_pos].decode("utf-8")[:-1]
    starting_point += 32
    s0 = int.from_bytes(data[starting_point:starting_point+4], "little")
    e0 = int.from_bytes(data[starting_point+4:starting_point+8], "little")

    point_count = e0 - s0
    cursor = starting_point + 8

    points = []
    for p_id in range(point_count):
        x = np.int16(int.from_bytes(data[cursor:cursor+2], "little"))
        y = np.int16(int.from_bytes(data[cursor+2:cursor+4], "little"))
        z = np.int16(int.from_bytes(data[cursor+4:cursor+6], "little"))

        cursor = cursor + 6

        p_dict = {
            "x": x,
            "y": y,
            "z": z
        }
        points.append(p_dict)

    triangles = []

    sf3 = int.from_bytes(data[cursor:cursor+4], "little")
    ef3 = int.from_bytes(data[cursor+4:cursor+8], "little")

    # some sort of offset magic
    dp = next_prim_point - s0

    triangle_count = ef3 - sf3

    cursor = cursor + 8
    for t_id in range(triangle_count):
        texture_id_group = int.from_bytes(data[cursor:cursor + 1], "little")
        properties = int.from_bytes(data[cursor + 1:cursor + 2], "little")

        point_a_id = int.from_bytes(data[cursor + 2:cursor + 4], "little") + dp
        point_b_id = int.from_bytes(data[cursor + 4:cursor + 6], "little") + dp
        point_c_id = int.from_bytes(data[cursor + 6:cursor + 8], "little") + dp

        # U position of the point A on the texture grid (u)
        u_a = int.from_bytes(data[cursor + 8:cursor + 9], "little")
        # V position of the point A on the texture grid (v)
        v_a = int.from_bytes(data[cursor + 9:cursor + 10], "little")
        u_b = int.from_bytes(data[cursor + 10:cursor + 11], "little")
        v_b = int.from_bytes(data[cursor + 11:cursor + 12], "little")
        u_c = int.from_bytes(data[cursor + 12:cursor + 13], "little")
        v_c = int.from_bytes(data[cursor + 13:cursor + 14], "little")

        # Used for people
        bright_a = int.from_bytes(data[cursor + 14:cursor + 15], "little")
        bright_b = int.from_bytes(data[cursor + 15:cursor + 16], "little")
        bright_c = int.from_bytes(data[cursor + 16:cursor + 17], "little")
        cursor = cursor + 28
        # cursor = cursor + 28

        q_dict = {
            "texture_id_group": texture_id_group,
            "properties": properties,
            "point_a_id": point_a_id,
            "point_b_id": point_b_id,
            "point_c_id": point_c_id,
            "u_a": u_a,
            "v_a": v_a,
            "u_b": u_b,
            "v_b": v_b,
            "u_c": u_c,
            "v_c": v_c,
            "bright_a": bright_a,
            "bright_b": bright_b,
            "bright_c": bright_c
        }

        triangles.append(q_dict)

    quadrangles = []

    sf4 = int.from_bytes(data[cursor:cursor+4], "little")
    ef4 = int.from_bytes(data[cursor+4:cursor+8], "little")
    cursor = cursor + 8

    quadrangle_count = ef4 - sf4

    for q_id in range(quadrangle_count):
        texture_id_group = int.from_bytes(data[cursor:cursor + 1], "little")
        properties = int.from_bytes(data[cursor + 1:cursor + 2], "little")

        point_a_id = int.from_bytes(data[cursor + 2:cursor + 4], "little") + dp
        point_b_id = int.from_bytes(data[cursor + 4:cursor + 6], "little") + dp
        point_c_id = int.from_bytes(data[cursor + 6:cursor + 8], "little") + dp
        point_d_id = int.from_bytes(data[cursor + 8:cursor + 10], "little") + dp

        # U position of the point A on the texture grid (u)
        u_a = int.from_bytes(data[cursor + 10:cursor + 11], "little")
        # V position of the point A on the texture grid (v)
        v_a = int.from_bytes(data[cursor + 11:cursor + 12], "little")
        u_b = int.from_bytes(data[cursor + 12:cursor + 13], "little")
        v_b = int.from_bytes(data[cursor + 13:cursor + 14], "little")
        u_c = int.from_bytes(data[cursor + 14:cursor + 15], "little")
        v_c = int.from_bytes(data[cursor + 15:cursor + 16], "little")
        u_d = int.from_bytes(data[cursor + 16:cursor + 17], "little")
        v_d = int.from_bytes(data[cursor + 17:cursor + 18], "little")

        # Used for people
        bright_a = int.from_bytes(data[cursor + 18:cursor + 19], "little")
        bright_b = int.from_bytes(data[cursor + 19:cursor + 20], "little")
        bright_c = int.from_bytes(data[cursor + 20:cursor + 21], "little")
        bright_d = int.from_bytes(data[cursor + 21:cursor + 22], "little")
        cursor = cursor + 34
        # cursor = cursor + 28

        q_dict = {
            "texture_id_group": texture_id_group,
            "properties": properties,
            "point_a_id": point_a_id,
            "point_b_id": point_b_id,
            "point_c_id": point_c_id,
            "point_d_id": point_d_id,
            "u_a": u_a,
            "v_a": v_a,
            "u_b": u_b,
            "v_b": v_b,
            "u_c": u_c,
            "v_c": v_c,
            "u_d": u_d,
            "v_d": v_d,
            "bright_a": bright_a,
            "bright_b": bright_b,
            "bright_c": bright_c,
            "bright_d": bright_d
        }

        quadrangles.append(q_dict)

    next_prim_point += point_count

    return [points, quadrangles, triangles, name, cursor, next_prim_point]


def adjust_datatypes_in_dataframes(df_points, df_triangles, df_quadrangles):

    df_points['x'] = df_points['x'].astype('int16')
    df_points['y'] = df_points['y'].astype('int16')
    df_points['z'] = df_points['z'].astype('int16')

    if not df_quadrangles.empty:
        df_quadrangles['texture_id_group'] = df_quadrangles['texture_id_group'].astype('int8')
        df_quadrangles['properties'] = df_quadrangles['properties'].astype('int8')

        df_quadrangles['point_a_id'] = df_quadrangles['point_a_id'].astype('int16')
        df_quadrangles['point_b_id'] = df_quadrangles['point_b_id'].astype('int16')
        df_quadrangles['point_c_id'] = df_quadrangles['point_c_id'].astype('int16')
        df_quadrangles['point_d_id'] = df_quadrangles['point_d_id'].astype('int16')
        df_quadrangles['u_a'] = df_quadrangles['u_a'].astype('uint8')
        df_quadrangles['v_a'] = df_quadrangles['v_a'].astype('uint8')
        df_quadrangles['u_b'] = df_quadrangles['u_b'].astype('uint8')
        df_quadrangles['v_b'] = df_quadrangles['v_b'].astype('uint8')
        df_quadrangles['u_c'] = df_quadrangles['u_c'].astype('uint8')
        df_quadrangles['v_c'] = df_quadrangles['v_c'].astype('uint8')
        df_quadrangles['u_d'] = df_quadrangles['u_d'].astype('uint8')
        df_quadrangles['v_d'] = df_quadrangles['v_d'].astype('uint8')

        df_quadrangles['bright_a'] = df_quadrangles['bright_a'].astype('int8')
        df_quadrangles['bright_b'] = df_quadrangles['bright_b'].astype('int8')
        df_quadrangles['bright_c'] = df_quadrangles['bright_c'].astype('int8')
        df_quadrangles['bright_d'] = df_quadrangles['bright_d'].astype('int8')

        df_quadrangles['thing_index'] = df_quadrangles['thing_index'].astype('int16')
        df_quadrangles['col2'] = df_quadrangles['col2'].astype('int16')
        df_quadrangles['face_flags'] = df_quadrangles['face_flags'].astype('int16')
        df_quadrangles['type'] = df_quadrangles['type'].astype('int8')
        df_quadrangles['id'] = df_quadrangles['id'].astype('int8')

    if not df_triangles.empty:
        df_triangles['texture_id_group'] = df_triangles['texture_id_group'].astype('int8')
        df_triangles['properties'] = df_triangles['properties'].astype('int8')

        df_triangles['point_a_id'] = df_triangles['point_a_id'].astype('int16')
        df_triangles['point_b_id'] = df_triangles['point_b_id'].astype('int16')
        df_triangles['point_c_id'] = df_triangles['point_c_id'].astype('int16')
        df_triangles['u_a'] = df_triangles['u_a'].astype('uint8')
        df_triangles['v_a'] = df_triangles['v_a'].astype('uint8')
        df_triangles['u_b'] = df_triangles['u_b'].astype('uint8')
        df_triangles['v_b'] = df_triangles['v_b'].astype('uint8')
        df_triangles['u_c'] = df_triangles['u_c'].astype('uint8')
        df_triangles['v_c'] = df_triangles['v_c'].astype('uint8')

        df_triangles['bright_a'] = df_triangles['bright_a'].astype('int8')
        df_triangles['bright_b'] = df_triangles['bright_b'].astype('int8')
        df_triangles['bright_c'] = df_triangles['bright_c'].astype('int8')

        df_triangles['thing_index'] = df_triangles['thing_index'].astype('int16')
        df_triangles['col2'] = df_triangles['col2'].astype('int16')
        df_triangles['face_flags'] = df_triangles['face_flags'].astype('int16')
        df_triangles['type'] = df_triangles['type'].astype('int8')
        df_triangles['id'] = df_triangles['id'].astype('int8')


def prepare_binary_data(df_points, df_quadrangles, df_triangles):
    # Initialize a bytearray to accumulate the binary data
    binary_data = bytearray()
    s0 = 0
    e0 = len(df_points)

    binary_data.extend(s0.to_bytes(4, byteorder='little'))
    binary_data.extend(e0.to_bytes(4, byteorder='little'))

    # Write the data to the bytearray
    for index, series in df_points.iterrows():
        binary_data.extend(df_points['x'][index].tobytes())
        binary_data.extend(df_points['y'][index].tobytes())
        binary_data.extend(df_points['z'][index].tobytes())

    sf3 = 0
    ef3 = len(df_triangles)

    binary_data.extend(sf3.to_bytes(4, byteorder='little'))
    binary_data.extend(ef3.to_bytes(4, byteorder='little'))

    for index, series in df_triangles.iterrows():
        binary_data.extend(df_triangles['texture_id_group'][index].tobytes())
        binary_data.extend(df_triangles['properties'][index].tobytes())

        binary_data.extend(df_triangles['point_a_id'][index].tobytes())
        binary_data.extend(df_triangles['point_b_id'][index].tobytes())
        binary_data.extend(df_triangles['point_c_id'][index].tobytes())

        binary_data.extend(df_triangles['u_a'][index].tobytes())
        binary_data.extend(df_triangles['v_a'][index].tobytes())
        binary_data.extend(df_triangles['u_b'][index].tobytes())
        binary_data.extend(df_triangles['v_b'][index].tobytes())
        binary_data.extend(df_triangles['u_c'][index].tobytes())
        binary_data.extend(df_triangles['v_c'][index].tobytes())

        binary_data.extend(df_triangles['bright_a'][index].tobytes())
        binary_data.extend(df_triangles['bright_b'][index].tobytes())
        binary_data.extend(df_triangles['bright_c'][index].tobytes())

        binary_data.extend(df_triangles['thing_index'][index].tobytes())
        binary_data.extend(df_triangles['col2'][index].tobytes())
        binary_data.extend(df_triangles['face_flags'][index].tobytes())
        binary_data.extend(df_triangles['type'][index].tobytes())
        binary_data.extend(df_triangles['id'][index].tobytes())

        # padding
        for i in range(3):
            binary_data.extend("\0".encode('utf-8'))

    sf4 = 0
    ef4 = len(df_quadrangles)

    binary_data.extend(sf4.to_bytes(4, byteorder='little'))
    binary_data.extend(ef4.to_bytes(4, byteorder='little'))


    for index, series in df_quadrangles.iterrows():
        binary_data.extend(df_quadrangles['texture_id_group'][index].tobytes())
        binary_data.extend(df_quadrangles['properties'][index].tobytes())

        binary_data.extend(df_quadrangles['point_a_id'][index].tobytes())
        binary_data.extend(df_quadrangles['point_b_id'][index].tobytes())
        binary_data.extend(df_quadrangles['point_d_id'][index].tobytes())
        binary_data.extend(df_quadrangles['point_c_id'][index].tobytes())

        binary_data.extend(df_quadrangles['u_a'][index].tobytes())
        binary_data.extend(df_quadrangles['v_a'][index].tobytes())
        binary_data.extend(df_quadrangles['u_b'][index].tobytes())
        binary_data.extend(df_quadrangles['v_b'][index].tobytes())
        binary_data.extend(df_quadrangles['u_d'][index].tobytes())
        binary_data.extend(df_quadrangles['v_d'][index].tobytes())
        binary_data.extend(df_quadrangles['u_c'][index].tobytes())
        binary_data.extend(df_quadrangles['v_c'][index].tobytes())

        binary_data.extend(df_quadrangles['bright_a'][index].tobytes())
        binary_data.extend(df_quadrangles['bright_b'][index].tobytes())
        binary_data.extend(df_quadrangles['bright_d'][index].tobytes())
        binary_data.extend(df_quadrangles['bright_c'][index].tobytes())

        binary_data.extend(df_quadrangles['thing_index'][index].tobytes())
        binary_data.extend(df_quadrangles['col2'][index].tobytes())
        binary_data.extend(df_quadrangles['face_flags'][index].tobytes())
        binary_data.extend(df_quadrangles['type'][index].tobytes())
        binary_data.extend(df_quadrangles['id'][index].tobytes())

        # padding
        for i in range(4):
            binary_data.extend("\0".encode('utf-8'))

    return binary_data


def faces_count(df_faces):
    return len(df_faces)


def app():
    input_all_filename = "darci1.all"
    input_obj = "res/objs/gta3_skull.obj"
    binary_data = read_nprim("res/all/" + input_all_filename)
    found_at = search_in_binary(binary_data, "skull")
    [points, quadrangles, triangles, name, cursor, next_prim_point] = \
        convert_nprim_binary_to_readable_data(found_at, 0, binary_data)

    print(f'cursor={cursor}')

    binary_cut = remove_section(binary_data, found_at, cursor)

    print(f'len(binary_data)={len(binary_data)}')
    print(f'len(binary_cut)={len(binary_cut)}')
    #
    [df_points, df_triangles, df_quadrangles] = extract_obj_to_df(input_obj)
    #
    # triangle_faces_count = faces_count(df_triangles)
    # quadrangle_faces_count = faces_count(df_quadrangles)
    adjust_datatypes_in_dataframes(df_points, df_triangles, df_quadrangles)

    new_binary_body_part = prepare_binary_data(df_points, df_quadrangles, df_triangles)
    # print(binary_result)
    # print(found_at)

    # start_position = 10
    # appended_binary_data = b'new binary data'
    #
    new_binary_data = insert_section(binary_data, found_at+32, cursor, new_binary_body_part)
    # print(binary_data)
    #
    # Save the new binary data to a file (optional)
    with open('darci1.all', 'wb') as file:
        file.write(new_binary_data)


if __name__ == '__main__':
    app()