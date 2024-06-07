import numpy as np
from obj_to_dataframe import *
import struct


def find_2byte_integer_in_bytearray(byte_array, value):
    # Convert the integer value to a 2-byte sequence (little-endian format)
    value_bytes = struct.pack('<H', value)

    # Search for the sequence in the bytearray
    index = byte_array.find(value_bytes)

    return index


class BodyPartMetaData:
    def __init__(self):
        self.name = ""
        self.s0 = 0
        self.e0 = 0
        self.sf3 = 0
        self.ef3 = 0
        self.sf4 = 0
        self.ef4 = 0


def find_body_part_by_name(body_parts, name):
    for body_part in body_parts:
        if body_part.name == name:
            return body_part
    return None


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


def update_metadata_in_binary(starting_point, data, points_offset, triangles_offset, quadrangles_offset):
    # Ensure data is a bytearray
    if isinstance(data, bytes):
        data = bytearray(data)

    starting_point += 32
    s0 = int.from_bytes(data[starting_point:starting_point + 4], "little")
    e0 = int.from_bytes(data[starting_point + 4:starting_point + 8], "little")
    point_count = e0 - s0

    cursor = starting_point + 8

    print(f's0={s0}')
    print(f'e0={e0}')

    data[starting_point:starting_point + 4] = (s0 + points_offset).to_bytes(4, byteorder='little')
    data[starting_point + 4:starting_point + 8] = (e0 + points_offset).to_bytes(4, byteorder='little')

    s0 = int.from_bytes(data[starting_point:starting_point + 4], "little")
    e0 = int.from_bytes(data[starting_point + 4:starting_point + 8], "little")

    print(f's0={s0}')
    print(f'e0={e0}')

    for p_id in range(point_count):
        cursor = cursor + 6

    sf3 = int.from_bytes(data[cursor:cursor + 4], "little")
    ef3 = int.from_bytes(data[cursor + 4:cursor + 8], "little")
    triangle_count = ef3 - sf3

    print(f'sf3={sf3}')
    print(f'ef3={ef3}')

    data[cursor:cursor + 4] = (sf3 + triangles_offset).to_bytes(4, byteorder='little')
    data[cursor + 4:cursor + 8] = (ef3 + triangles_offset).to_bytes(4, byteorder='little')

    sf3 = int.from_bytes(data[cursor:cursor + 4], "little")
    ef3 = int.from_bytes(data[cursor + 4:cursor + 8], "little")

    print(f'sf3={sf3}')
    print(f'ef3={ef3}')

    cursor = cursor + 8

    for t_id in range(triangle_count):

        point_a_id = int.from_bytes(data[cursor + 2:cursor + 4], "little")
        point_b_id = int.from_bytes(data[cursor + 4:cursor + 6], "little")
        point_c_id = int.from_bytes(data[cursor + 6:cursor + 8], "little")

        value_a = points_offset + point_a_id
        value_b = points_offset + point_b_id
        value_c = points_offset + point_c_id

        value_a_bytes = struct.pack('<H', value_a)
        value_b_bytes = struct.pack('<H', value_b)
        value_c_bytes = struct.pack('<H', value_c)

        data[cursor + 2:cursor + 4] = value_a_bytes
        data[cursor + 4:cursor + 6] = value_b_bytes
        data[cursor + 6:cursor + 8] = value_c_bytes

        # data[cursor + 2:cursor + 4] = (points_offset + point_a_id).to_bytes(4, byteorder='little')
        # data[cursor + 4:cursor + 6] = (points_offset + point_b_id).to_bytes(4, byteorder='little')
        # data[cursor + 6:cursor + 8] = (points_offset + point_c_id).to_bytes(4, byteorder='little')

        cursor = cursor + 28

    sf4 = int.from_bytes(data[cursor:cursor+4], "little")
    ef4 = int.from_bytes(data[cursor+4:cursor+8], "little")

    print(f'sf4={sf4}')
    print(f'ef4={ef4}')

    data[cursor:cursor + 4] = (sf4 + quadrangles_offset).to_bytes(4, byteorder='little')
    data[cursor + 4:cursor + 8] = (ef4 + quadrangles_offset).to_bytes(4, byteorder='little')

    sf4 = int.from_bytes(data[cursor:cursor + 4], "little")
    ef4 = int.from_bytes(data[cursor + 4:cursor + 8], "little")

    print(f'sf4={sf4}')
    print(f'ef4={ef4}')

    quadrangle_count = ef4 - sf4
    cursor = cursor + 8

    for t_id in range(quadrangle_count):
        point_a_id = int.from_bytes(data[cursor + 2:cursor + 4], "little")
        point_b_id = int.from_bytes(data[cursor + 4:cursor + 6], "little")
        point_c_id = int.from_bytes(data[cursor + 6:cursor + 8], "little")
        point_d_id = int.from_bytes(data[cursor + 8:cursor + 10], "little")

        value_a = points_offset + point_a_id
        value_b = points_offset + point_b_id
        value_c = points_offset + point_c_id
        value_d = points_offset + point_d_id

        value_a_bytes = struct.pack('<H', value_a)
        value_b_bytes = struct.pack('<H', value_b)
        value_c_bytes = struct.pack('<H', value_c)
        value_d_bytes = struct.pack('<H', value_d)

        data[cursor + 2:cursor + 4] = value_a_bytes
        data[cursor + 4:cursor + 6] = value_b_bytes
        data[cursor + 6:cursor + 8] = value_c_bytes
        data[cursor + 8:cursor + 10] = value_d_bytes


        # data[cursor + 2:cursor + 4] = (points_offset + point_a_id).to_bytes(4, byteorder='little')
        # data[cursor + 4:cursor + 6] = (points_offset + point_b_id).to_bytes(4, byteorder='little')
        # data[cursor + 6:cursor + 8] = (points_offset + point_c_id).to_bytes(4, byteorder='little')
        # data[cursor + 8:cursor + 10] = (points_offset + point_d_id).to_bytes(4, byteorder='little')

        cursor = cursor + 34

    return data


def convert_nprim_binary_to_readable_data(starting_point, next_prim_point, data):
    body_part_meta = BodyPartMetaData()

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

    # print(f'{name}')
    # print(f's0={s0},e0={e0},sf3={sf3},ef3={ef3},sf4={sf4},ef4={ef4}')

    body_part_meta.name = name
    body_part_meta.s0 = s0
    body_part_meta.e0 = e0
    body_part_meta.sf3 = sf3
    body_part_meta.ef3 = ef3
    body_part_meta.sf4 = sf4
    body_part_meta.ef4 = ef4

    return [points, quadrangles, triangles, name, cursor, next_prim_point, body_part_meta]


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

        df_quadrangles['bright_a'] = df_quadrangles['bright_a'].astype('int16')
        df_quadrangles['bright_b'] = df_quadrangles['bright_b'].astype('int16')
        df_quadrangles['bright_c'] = df_quadrangles['bright_c'].astype('int16')
        df_quadrangles['bright_d'] = df_quadrangles['bright_d'].astype('int16')

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

        df_triangles['bright_a'] = df_triangles['bright_a'].astype('int16')
        df_triangles['bright_b'] = df_triangles['bright_b'].astype('int16')
        df_triangles['bright_c'] = df_triangles['bright_c'].astype('int16')

        df_triangles['thing_index'] = df_triangles['thing_index'].astype('int16')
        df_triangles['col2'] = df_triangles['col2'].astype('int16')
        df_triangles['face_flags'] = df_triangles['face_flags'].astype('int16')
        df_triangles['type'] = df_triangles['type'].astype('int8')
        df_triangles['id'] = df_triangles['id'].astype('int8')


def prepare_binary_data(df_points, df_quadrangles, df_triangles, previous_meta_data):
    # Initialize a bytearray to accumulate the binary data
    binary_data = bytearray()
    s0 = previous_meta_data.s0
    e0 = s0 + len(df_points)

    # s0 = 0
    # e0 = len(df_points)

    binary_data.extend(s0.to_bytes(4, byteorder='little'))
    binary_data.extend(e0.to_bytes(4, byteorder='little'))

    # Write the data to the bytearray
    for index, series in df_points.iterrows():
        binary_data.extend(df_points['x'][index].tobytes())
        binary_data.extend(df_points['y'][index].tobytes())
        binary_data.extend(df_points['z'][index].tobytes())

    sf3 = previous_meta_data.sf3
    ef3 = sf3 + len(df_triangles)

    # sf3 = 0
    # ef3 = len(df_triangles)

    binary_data.extend(sf3.to_bytes(4, byteorder='little'))
    binary_data.extend(ef3.to_bytes(4, byteorder='little'))

    for index, series in df_triangles.iterrows():
        binary_data.extend(df_triangles['texture_id_group'][index].tobytes())
        binary_data.extend(df_triangles['properties'][index].tobytes())

        # binary_data.extend((df_triangles['point_a_id'][index]+s0).tobytes())
        # binary_data.extend((df_triangles['point_b_id'][index]+s0).tobytes())
        # binary_data.extend((df_triangles['point_c_id'][index]+s0).tobytes())

        binary_data.extend(struct.pack('<H', df_triangles['point_a_id'][index] + s0 - 1))
        binary_data.extend(struct.pack('<H', df_triangles['point_b_id'][index] + s0 - 1))
        binary_data.extend(struct.pack('<H', df_triangles['point_c_id'][index] + s0 - 1))

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

        # # padding
        # for i in range(3):
        #     binary_data.extend("\0".encode('utf-8'))

    # sf4 = 0
    # ef4 = len(df_quadrangles)

    sf4 = previous_meta_data.sf4
    ef4 = sf4 + len(df_quadrangles)

    binary_data.extend(sf4.to_bytes(4, byteorder='little'))
    binary_data.extend(ef4.to_bytes(4, byteorder='little'))

    for index, series in df_quadrangles.iterrows():
        binary_data.extend(df_quadrangles['texture_id_group'][index].tobytes())
        binary_data.extend(df_quadrangles['properties'][index].tobytes())

        # binary_data.extend((df_quadrangles['point_a_id'][index]+s0).tobytes())
        # binary_data.extend((df_quadrangles['point_b_id'][index]+s0).tobytes())
        # binary_data.extend((df_quadrangles['point_d_id'][index]+s0).tobytes())
        # binary_data.extend((df_quadrangles['point_c_id'][index]+s0).tobytes())

        binary_data.extend(struct.pack('<H', df_quadrangles['point_a_id'][index] + s0 - 1))
        binary_data.extend(struct.pack('<H', df_quadrangles['point_b_id'][index] + s0 - 1))
        binary_data.extend(struct.pack('<H', df_quadrangles['point_c_id'][index] + s0 - 1))
        binary_data.extend(struct.pack('<H', df_quadrangles['point_d_id'][index] + s0 - 1))

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

    points_delta = e0 - previous_meta_data.e0
    triangles_delta = ef3 - previous_meta_data.ef3
    quadrangles_delta = ef4 - previous_meta_data.ef4

    return [binary_data, points_delta, triangles_delta, quadrangles_delta]


def prepare_binary_data_old(df_points, df_quadrangles, df_triangles):
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


# body parts count
def prim_count(cursor, binary_data):
    save_type = int.from_bytes(binary_data[cursor:cursor+4], "little")
    s0 = int.from_bytes(binary_data[cursor+4:cursor+8], "little")
    e0 = int.from_bytes(binary_data[cursor+8:cursor+12], "little")

    cursor += 12
    prims_count = e0 - s0

    return [cursor, prims_count]


def app():
    input_all_filename = "roper.all"
    # input_obj = "res/objs/gta3_skull.obj"
    input_obj = "res/objs/hostage_skull.obj"
    body_part_name = "skull00"
    binary_data = read_nprim("res/all/" + input_all_filename)
    found_at = search_in_binary(binary_data, body_part_name)

    cursor = 8
    [cursor, prims_count] = prim_count(cursor, binary_data)
    body_part_start_end_point_dict = {}
    names_ordered = []
    body_parts_meta = []
    for i in range(prims_count):
        [points, quadrangles, triangles, name, cursor, next_prim_point,  body_part_meta] = \
            convert_nprim_binary_to_readable_data(cursor, 0, binary_data)
        body_part_start_end_point_dict[name] = [body_part_meta.s0, body_part_meta.e0, body_part_meta.sf3, body_part_meta.ef3, body_part_meta.sf4, body_part_meta.ef4]
        body_parts_meta.append(body_part_meta)
        names_ordered.append(name)

    [a, b, c, d, skull_obj_end_cursor, e, f] = \
        convert_nprim_binary_to_readable_data(found_at, 0, binary_data)


    print(names_ordered.index(body_part_name))
    print(body_part_start_end_point_dict)
    print(names_ordered)
    print(f'cursor={cursor}')

    # Sorting the dictionary by the first value in the list
    # sorted_result = dict(sorted(body_part_start_end_point_dict.items(), key=lambda item: item.value[0]))
    sorted_result = dict(sorted(body_part_start_end_point_dict.items(), key=lambda item: item[1][0]))

    print(sorted_result)


    #
    [df_points, df_triangles, df_quadrangles] = extract_obj_to_df(input_obj)
    #
    # triangle_faces_count = faces_count(df_triangles)
    # quadrangle_faces_count = faces_count(df_quadrangles)
    adjust_datatypes_in_dataframes(df_points, df_triangles, df_quadrangles)

    modified_body_part = find_body_part_by_name(body_parts_meta, body_part_name)
    [new_binary_body_part, points_delta, triangles_delta, quadrangles_delta] = prepare_binary_data(df_points, df_quadrangles, df_triangles, modified_body_part)

    # value_to_find = 9977
    #
    # index = find_2byte_integer_in_bytearray(new_binary_body_part, value_to_find)
    # if index != -1:
    #     print(f"Value {value_to_find} found at index {index}")
    # else:
    #     print(f"Value {value_to_find} not found")

    # new_binary_body_part = prepare_binary_data_old(df_points, df_quadrangles, df_triangles)
    # print(binary_result)
    # print(found_at)

    # start_position = 10
    # appended_binary_data = b'new binary data'
    #


    # print(binary_data)
    #
    # Save the new binary data to a file (optional)

    # update_metadata_in_binary(found_at, binary_data)

    # print(f'found_at = {found_at}')
    for name in names_ordered:
        cursor_at = search_in_binary(binary_data, name)
        # print(cursor_at)
        # We need to update metadata for points appearing after the modified body part
        if cursor_at > found_at:
            binary_data = update_metadata_in_binary(cursor_at, binary_data, points_delta, triangles_delta, quadrangles_delta)

    binary_cut = remove_section(binary_data, found_at, skull_obj_end_cursor)

    print(f'len(binary_data)={len(binary_data)}')
    print(f'len(binary_cut)={len(binary_cut)}')
    new_binary_data = insert_section(binary_data, found_at+32, skull_obj_end_cursor, new_binary_body_part)

    with open(input_all_filename, 'wb') as file:
        file.write(new_binary_data)


def app2():
    input_all_filename = "roper.all"
    binary_data = read_nprim(input_all_filename)
    cursor = 8
    [cursor, prims_count] = prim_count(cursor, binary_data)
    body_part_start_end_point_dict = {}
    names_ordered = []
    body_parts_meta = []
    for i in range(prims_count):
        [points, quadrangles, triangles, name, cursor, next_prim_point, body_part_meta] = \
            convert_nprim_binary_to_readable_data(cursor, 0, binary_data)


if __name__ == '__main__':
    app()
