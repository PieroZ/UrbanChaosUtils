def prepare_tex_data(triangles_dict, quadrangles_dict):
    tex_data = bytearray()
    tex_data_cursor = 0

    # version = 1
    triangles_count = len(triangles_dict)
    quadrangle_count = len(quadrangles_dict)
    # tex_data[tex_data_cursor:tex_data_cursor + 4] = version.to_bytes(4, byteorder='little')
    tex_data[tex_data_cursor:tex_data_cursor + 2] = quadrangle_count.to_bytes(2, byteorder='little')

    tex_data_cursor = tex_data_cursor + 2
    for i in quadrangles_dict:
        tex_data[tex_data_cursor:tex_data_cursor + 1] = i['draw_flags'].to_bytes(1, byteorder='little')
        tex_data[tex_data_cursor + 1:tex_data_cursor + 3] = i['col_2'].to_bytes(2, byteorder='little')
        tex_data[tex_data_cursor + 3:tex_data_cursor + 4] = i['texture_page'].to_bytes(1, byteorder='little')
        tex_data[tex_data_cursor + 4:tex_data_cursor + 6] = i['face_flags'].to_bytes(2, byteorder='little')

        tex_data[tex_data_cursor + 6:tex_data_cursor + 7] = i['u_a'].to_bytes(1, byteorder='little')
        tex_data[tex_data_cursor + 7:tex_data_cursor + 8] = i['v_a'].to_bytes(1, byteorder='little')
        tex_data[tex_data_cursor + 8:tex_data_cursor + 9] = i['u_b'].to_bytes(1, byteorder='little')
        tex_data[tex_data_cursor + 9:tex_data_cursor + 10] = i['v_b'].to_bytes(1, byteorder='little')
        tex_data[tex_data_cursor + 10:tex_data_cursor + 11] = i['u_c'].to_bytes(1, byteorder='little')
        tex_data[tex_data_cursor + 11:tex_data_cursor + 12] = i['v_c'].to_bytes(1, byteorder='little')
        tex_data[tex_data_cursor + 12:tex_data_cursor + 13] = i['u_d'].to_bytes(1, byteorder='little')
        tex_data[tex_data_cursor + 13:tex_data_cursor + 14] = i['v_d'].to_bytes(1, byteorder='little')

        tex_data_cursor = tex_data_cursor + 14

    tex_data[tex_data_cursor + 4:tex_data_cursor + 6] = triangles_count.to_bytes(2, byteorder='little')

    tex_data_cursor = tex_data_cursor + 6

    for i in triangles_dict:
        tex_data[tex_data_cursor:tex_data_cursor + 1] = i['draw_flags'].to_bytes(1, byteorder='little')
        tex_data[tex_data_cursor + 1:tex_data_cursor + 3] = i['col_2'].to_bytes(2, byteorder='little')
        tex_data[tex_data_cursor + 3:tex_data_cursor + 4] = i['texture_page'].to_bytes(1, byteorder='little')
        tex_data[tex_data_cursor + 4:tex_data_cursor + 6] = i['face_flags'].to_bytes(2, byteorder='little')

        tex_data[tex_data_cursor + 6:tex_data_cursor + 7] = i['u_a'].to_bytes(1, byteorder='little')
        tex_data[tex_data_cursor + 7:tex_data_cursor + 8] = i['v_a'].to_bytes(1, byteorder='little')
        tex_data[tex_data_cursor + 8:tex_data_cursor + 9] = i['u_b'].to_bytes(1, byteorder='little')
        tex_data[tex_data_cursor + 9:tex_data_cursor + 10] = i['v_b'].to_bytes(1, byteorder='little')
        tex_data[tex_data_cursor + 10:tex_data_cursor + 11] = i['u_c'].to_bytes(1, byteorder='little')
        tex_data[tex_data_cursor + 11:tex_data_cursor + 12] = i['v_c'].to_bytes(1, byteorder='little')

        tex_data_cursor = tex_data_cursor + 12

    return tex_data


def extract_tex_sections_from_all(starting_point, data):

    null_terminated_pos = data[starting_point:].find(b'\00')
    name = data[starting_point:starting_point+null_terminated_pos].decode("utf-8")[:-1]
    starting_point += 32
    s0 = int.from_bytes(data[starting_point:starting_point+4], "little")
    e0 = int.from_bytes(data[starting_point+4:starting_point+8], "little")

    point_count = e0 - s0
    cursor = starting_point + 8

    for p_id in range(point_count):
        cursor = cursor + 6

    triangles = []

    sf3 = int.from_bytes(data[cursor:cursor+4], "little")
    ef3 = int.from_bytes(data[cursor+4:cursor+8], "little")

    triangle_count = ef3 - sf3

    cursor = cursor + 8
    for t_id in range(triangle_count):
        # TexturePage?
        texture_page = int.from_bytes(data[cursor:cursor + 1], "little")
        # texture_id_group = int.from_bytes(data[cursor:cursor + 1], "little")
        # DrawFlags?
        draw_flags = int.from_bytes(data[cursor + 1:cursor + 2], "little")
        # properties = int.from_bytes(data[cursor + 1:cursor + 2], "little")

        # U position of the point A on the texture grid (u)
        u_a = int.from_bytes(data[cursor + 8:cursor + 9], "little")
        # V position of the point A on the texture grid (v)
        v_a = int.from_bytes(data[cursor + 9:cursor + 10], "little")
        u_b = int.from_bytes(data[cursor + 10:cursor + 11], "little")
        v_b = int.from_bytes(data[cursor + 11:cursor + 12], "little")
        u_c = int.from_bytes(data[cursor + 12:cursor + 13], "little")
        v_c = int.from_bytes(data[cursor + 13:cursor + 14], "little")

        thing_index = int.from_bytes(data[cursor + 20:cursor + 22], "little")
        col_2 = int.from_bytes(data[cursor + 22:cursor + 24], "little")
        face_flags = int.from_bytes(data[cursor + 24:cursor + 26], "little")
        type = int.from_bytes(data[cursor + 26:cursor + 27], "little")
        id = int.from_bytes(data[cursor + 27:cursor + 28], "little")

        # bright - 6 bytes 20
        # ThingIndex 2 bytes 22
        # Col2 2 bytes 24
        # FaceFlags 2 bytes 26
        # Type 1 byte 27
        # ID 1 byte 28


        cursor = cursor + 28
        # cursor = cursor + 28

        q_dict = {
            "texture_page": texture_page,
            "draw_flags": draw_flags,
            "u_a": u_a,
            "v_a": v_a,
            "u_b": u_b,
            "v_b": v_b,
            "u_c": u_c,
            "v_c": v_c,
            "col_2": col_2,
            "face_flags": face_flags


        }

        triangles.append(q_dict)

    quadrangles = []

    sf4 = int.from_bytes(data[cursor:cursor+4], "little")
    ef4 = int.from_bytes(data[cursor+4:cursor+8], "little")
    cursor = cursor + 8

    quadrangle_count = ef4 - sf4

    for q_id in range(quadrangle_count):
        texture_page = int.from_bytes(data[cursor:cursor + 1], "little")
        draw_flags = int.from_bytes(data[cursor + 1:cursor + 2], "little")

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
        bright_a = int.from_bytes(data[cursor + 18:cursor + 20], "little")
        bright_b = int.from_bytes(data[cursor + 20:cursor + 22], "little")
        bright_c = int.from_bytes(data[cursor + 22:cursor + 24], "little")
        bright_d = int.from_bytes(data[cursor + 24:cursor + 26], "little")

        thing_index = int.from_bytes(data[cursor + 26:cursor + 28], "little")
        col_2 = int.from_bytes(data[cursor + 28:cursor + 30], "little")
        face_flags = int.from_bytes(data[cursor + 30:cursor + 32], "little")
        type = int.from_bytes(data[cursor + 32:cursor + 33], "little")
        id = int.from_bytes(data[cursor + 33:cursor + 34], "little")

        cursor = cursor + 34
        # cursor = cursor + 28

        q_dict = {
            "texture_page": texture_page,
            "draw_flags": draw_flags,
            "u_a": u_a,
            "v_a": v_a,
            "u_b": u_b,
            "v_b": v_b,
            "u_c": u_c,
            "v_c": v_c,
            "u_d": u_d,
            "v_d": v_d,
            "col_2": col_2,
            "face_flags": face_flags
        }

        quadrangles.append(q_dict)

    # next_prim_point += point_count

    return [quadrangles, triangles, name, cursor]


def prim_count(cursor, binary_data):
    save_type = int.from_bytes(binary_data[cursor:cursor+4], "little")
    s0 = int.from_bytes(binary_data[cursor+4:cursor+8], "little")
    e0 = int.from_bytes(binary_data[cursor+8:cursor+12], "little")

    cursor += 12
    prims_count = e0 - s0

    return [cursor, prims_count]


def read_binary(binary_file_path):
    with open(binary_file_path, "rb+") as file:
        file_chunk = file.read()

    return file_chunk


def app():
    input_all_file_name = 'darci1.all'
    input_all_file_path = f'res/all/{input_all_file_name}'
    output_name = f'output/tex/gta3.tex'

    debug_output_name = f'output/tex/roper_day_by_day_DEBUG_'

    all_binary_content = read_binary(input_all_file_path)

    cursor = 8
    [cursor, body_part_count] = prim_count(cursor, all_binary_content)
    tex_data = bytearray()
    version = 1
    tex_data[0:4] = version.to_bytes(4, byteorder='little')
    for i in range(body_part_count):
        [quadrangles, triangles, name, cursor] = extract_tex_sections_from_all(cursor, all_binary_content)
        body_part_tex_data = prepare_tex_data(triangles, quadrangles)
        tex_data.extend(body_part_tex_data)

        debug_output_name_final = f'{debug_output_name}{i}.tex'

        # with open(debug_output_name_final, 'wb') as file:
        #     file.write(body_part_tex_data)

        # print(''.join('{:02x}'.format(x) for x in body_part_tex_data))

        # hex_str = body_part_tex_data.hex()
        # print(hex_str)

    with open(output_name, 'wb') as file:
        file.write(tex_data)


if __name__ == '__main__':
    app()
