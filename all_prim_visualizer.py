import os.path

import numpy as np
import tkinter as tk
from pandastable import Table
from pathlib import Path
from GameKeyFrame import GameKeyFrame
from GameKeyFrameElement import GameKeyFrameElement
from GameFightCol import GameFightCol
import glob
import uc_matrix_utils

import json

texture_pack = "people"


def export_to_obj_format_with_uvs(filename, nprim_name, vertices, df_quadrangles, df_triangles):
    # vertices = df_points[["x", "y", "z"]].to_string(index=False, header=False)
    # vertices_as_list = vertices.split('\n')
    # append_str = "v "
    # vertices_as_list = [append_str + v for v in vertices_as_list]
    # vertices_as_list = '\n'.join(vertices_as_list)
    #
    #
    # quadrangles = df_quadrangles[["point_a_id", "point_b_id", "point_c_id", "point_d_id"]].to_string(index=False, header=False)

    # Path(filename).stem
    # file_wo_ext = os.path.splitext(filename)[0] + "/out/" + filename + ".obj"
    texture_file_numbers = []
    # output_filename = "output/baalrog/" + Path(filename).stem + "-" + nprim_name + '.obj'
    # output_filename = "output/baalrog/" + Path(filename).stem + '.obj'
    output_filename = filename
    output_filename = output_filename.replace('\\r', '')
    uv_set = []
    uv_full_set = []
    textures_per_quad_face = []
    texture_page_per_material = {}
    for index, row in enumerate(df_quadrangles):
        ua = row["u_a"]
        va = row["v_a"]
        ub = row["u_b"]
        vb = row["v_b"]
        uc = row["u_c"]
        vc = row["v_c"]
        ud = row["u_d"]
        vd = row["v_d"]
        texture_page = row["texture_id_group"]

        result_with_texture_page = (calc_uvs(ua, va, ub, vb, uc, vc, ud, vd, texture_page, texture_file_numbers, texture_page_per_material))

        result = result_with_texture_page[1:-1]

        for r in result:
            uv_full_set.append(r)
            if r not in uv_set:
                uv_set.append(r)

        textures_per_quad_face.append(result_with_texture_page[0])

    texture_per_triangle_face = []
    triangles_uv_full_set = []
    for index, row in enumerate(df_triangles):
        ua = row["u_a"]
        va = row["v_a"]
        ub = row["u_b"]
        vb = row["v_b"]
        uc = row["u_c"]
        vc = row["v_c"]
        texture_page = row["texture_id_group"]

        result_with_texture_page = (calc_uvs_triangles(ua, va, ub, vb, uc, vc, texture_page, texture_file_numbers, texture_page_per_material))

        result = result_with_texture_page[1:-1]

        for r in result:
            triangles_uv_full_set.append(r)

        texture_per_triangle_face.append(result_with_texture_page[0])

    # unique_data = [list(x) for x in set(tuple(x) for x in uv_set)]

    # print(uv_full_set)
    lines_per_material = {}
    with open(output_filename, "w") as output_file:
        # output_file.write(vertices_as_list)
        for v in vertices:
            output_file.write("v {} {} {}\n".format(v['x'], v['y'], v['z']))  # Vertex coordinates

        # for uv in uv_set:
        for uv in uv_full_set:
            vt_line = f"\nvt {uv[0]} {uv[1]}"
            output_file.write(vt_line)

        for uv in triangles_uv_full_set:
            vt_line = f"\nvt {uv[0]} {uv[1]}"
            output_file.write(vt_line)

        # output_file.write("\nusemtl Material.001")
        for index, row in enumerate(df_quadrangles):
            a = row['point_a_id']
            b = row['point_b_id']
            c = row['point_c_id']
            d = row['point_d_id']

            [ua, va] = uv_full_set[index*4]
            [ub, vb] = uv_full_set[index*4+1]
            [uc, vc] = uv_full_set[index*4+2]
            [ud, vd] = uv_full_set[index*4+3]

            uvaid = uv_full_set.index([ua, va]) + 1
            uvbid = uv_full_set.index([ub, vb]) + 1
            uvcid = uv_full_set.index([uc, vc]) + 1
            uvdid = uv_full_set.index([ud, vd]) + 1

            # uvaid = str(a[0] + 1)
            # uvbid = str(b[0] + 1)
            # uvcid = str(d[0] + 1)
            # uvdid = str(c[0] + 1)
            #
            # uvaid = str(index*4+1)
            # uvbid = str(index*4+1+1)
            # uvcid = str(index*4+2+1)
            # uvdid = str(index*4+3+1)

            # line = "\n" + "f " + str(a[0] + 1) + " " + str(b[0] + 1) + " " + str(d[0] + 1) + " " + str(c[0] + 1)
            # line = f"\nf {str(a)}/{uvaid} {str(b)}/{uvbid} {str(d)}/{uvdid} {str(c)}/{uvcid}"

            line = f"\nf {str(c)}/{uvcid} {str(d)}/{uvdid} {str(b)}/{uvbid} {str(a)}/{uvaid}"
            if textures_per_quad_face[index] in lines_per_material:
                lines_per_material[textures_per_quad_face[index]].append(line)
            else:
                lines_per_material[textures_per_quad_face[index]] = []
                lines_per_material[textures_per_quad_face[index]].append(line)

            # output_file.write(line)

        for index, row in enumerate(df_triangles):
            a = row['point_a_id']
            b = row['point_b_id']
            c = row['point_c_id']

            [ua, va] = triangles_uv_full_set[index*3]
            [ub, vb] = triangles_uv_full_set[index*3+1]
            [uc, vc] = triangles_uv_full_set[index*3+2]

            uvaid = triangles_uv_full_set.index([ua, va]) + 1 + len(uv_full_set)
            uvbid = triangles_uv_full_set.index([ub, vb]) + 1 + len(uv_full_set)
            uvcid = triangles_uv_full_set.index([uc, vc]) + 1 + len(uv_full_set)

            line = f"\nf {str(c)}/{uvcid} {str(b)}/{uvbid} {str(a)}/{uvaid}"

            if texture_per_triangle_face[index] in lines_per_material:
                lines_per_material[texture_per_triangle_face[index]].append(line)
            else:
                lines_per_material[texture_per_triangle_face[index]] = []
                lines_per_material[texture_per_triangle_face[index]].append(line)
            # output_file.write(line)

        for key, value in lines_per_material.items():
            material_line = f"\nusemtl Material.{key}"

            output_file.write(material_line)

            faces_lines = value
            for f_line in faces_lines:
                output_file.write(f_line)

    # output_material_filename = "output/dupa/" + Path(filename).stem + "-" + nprim_name + '.mtl'
    # output_material_filename = "output/baalrog/" + Path(filename).stem + '.mtl'
    output_material_filename = filename[:-4] + ".mtl"
    output_material_filename = output_material_filename.replace('\\r', '')
    with open(output_material_filename, "w") as output_material_file:
        for key, value in lines_per_material.items():
            material_line = f"\nnewmtl Material.{key}\n"
            output_material_file.write(material_line)
            l1 = "Ns 250.000000\n"
            l2 = "Ns 0.000000\n"
            l3 = "Ka 1.000000 1.000000 1.000000\n"
            l4 = "Ks 0.000000 0.000000 0.000000\n"
            l5 = "Ke 0.000000 0.000000 0.000000\n"
            l6 = "Ni 1.450000\n"
            l7 = "d 1.000000\n"
            l8 = f"illum 1\n"
            absolute_texture_path = "C:/Games/Urban Chaos/server/textures/shared/" + texture_page_per_material[key]
            # map_Kd = f"map_Kd C:/Games/Urban Chaos/server/textures/shared/people/tex{key:03d}hi.tga\n"
            map_Kd = f"map_Kd {absolute_texture_path}/tex{key:03d}hi.tga\n"

            output_material_file.writelines([l1, l2, l3, l4, l5, l6, l7, l8, map_Kd])

    # with open(output_material_filename, "w") as output_material_file:
    #     for key, value in texture_page_per_material.items():
    #         material_line = f"\nnewmtl Material.{key}\n"
    #         output_material_file.write(material_line)
    #         l1 = "Ns 250.000000\n"
    #         l2 = "Ns 0.000000\n"
    #         l3 = "Ka 1.000000 1.000000 1.000000\n"
    #         l4 = "Ks 0.000000 0.000000 0.000000\n"
    #         l5 = "Ke 0.000000 0.000000 0.000000\n"
    #         l6 = "Ni 1.450000\n"
    #         l7 = "d 1.000000\n"
    #         l8 = f"illum 1\n"
    #         absolute_texture_path = f"C:/Games/Urban Chaos/server/textures/shared/{value}"
    #         # map_Kd = f"map_Kd C:/Games/Urban Chaos/server/textures/shared/people/tex{key:03d}hi.tga\n"
    #         map_Kd = f"map_Kd {absolute_texture_path}/tex{key:03d}hi.tga\n"
    #
    #         output_material_file.writelines([l1, l2, l3, l4, l5, l6, l7, l8, map_Kd])


def write_obj_file(vertices, triangle_faces, quadrangle_faces, filename):
    with open(filename, 'w') as file:
        for v in vertices:
            file.write("v {} {} {}\n".format(v['x'], v['y'], v['z']))  # Vertex coordinates

        for f in triangle_faces:
            file.write("f {} {} {}\n".format(f['point_a_id'], f['point_b_id'], f['point_c_id']))  # Face indices

        for f in quadrangle_faces:
            file.write("f {} {} {} {}\n".format(f['point_a_id'], f['point_b_id'], f['point_d_id'], f['point_c_id']))  # Face indices

        # for vertex_group in vertices:
        #     for vertex in vertex_group:
        #         f.write("v {} {} {}\n".format(*vertex))  # Vertex coordinates
        #         # f.write("v {} {} 1.0\n".format(vertex[0]*vertex[2], vertex[1]*vertex[2]))  # Vertex coordinates
        #
        #     # f.write("\n")  # Separate vertex groups
        #
        # for i in range(0, len(vertices)):
        #     f.write("f {} {} {}\n".format(i * 3 + 1, i * 3 + 2, i * 3 + 3))  # Face indices


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


def calc_av_uv_triangle(a, b, c):
    return (a + b + c) / 3


def calc_av_uv(a, b, c, d):
    return (a + b + c + d) >> 2


def calc_final_uv(a, base_a):
    a = a - base_a
    a = a/32
    # print(a)
    if a == 31:
        a = 32
    return a


def calc_uvs_triangles(u0, v0, u1, v1, u2, v2, texture_page, texture_numbers, texture_page_per_material):
    global texture_pack
    TEXTURE_NORM_SIZE = 32
    TEXTURE_NORM_SQUARES = 8
    av_u = calc_av_uv_triangle(u0, u1, u2)
    av_v = calc_av_uv_triangle(v0, v1, v2)
    av_u = int(av_u/TEXTURE_NORM_SIZE)
    av_v = int(av_v/TEXTURE_NORM_SIZE)

    base_u = av_u * TEXTURE_NORM_SIZE
    base_v = av_v * TEXTURE_NORM_SIZE

    final_u0 = calc_final_uv(u0, base_u)
    final_v0 = calc_final_uv(v0, base_v)
    final_u1 = calc_final_uv(u1, base_u)
    final_v1 = calc_final_uv(v1, base_v)
    final_u2 = calc_final_uv(u2, base_u)
    final_v2 = calc_final_uv(v2, base_v)

    page = av_u + av_v * TEXTURE_NORM_SQUARES + texture_page * TEXTURE_NORM_SQUARES * TEXTURE_NORM_SQUARES
    # print(f'page = {page}')

    if page < 64 * 9:
        texture_page_offset = 64*8
        texture_pack = "insides"
        texture_dir = "insides"
    elif page < 64 * 11:
        texture_page_offset = 64*9
        texture_pack = "people"
        texture_dir = "people"
    elif page < 64 * 18:
        texture_page_offset = 64*11
        texture_pack = "prims"
        texture_dir = "prims"
    elif page < 64 * 21:
        texture_page_offset = 64*18
        texture_pack = "people2"
        texture_dir = "people2"
    else:
        texture_page_offset = 0
        texture_pack = "UNDEFINED"
        texture_dir = "UNDEFINED"

    texture_img_no = page - texture_page_offset
    if texture_img_no not in texture_numbers:
        texture_numbers.append(texture_img_no)
    # print(f'texture_img={texture_img_no}')

    # final_u0 = abs(1 - final_u0)
    final_v0 = abs(1 - final_v0)
    # final_u1 = abs(1 - final_u1)
    final_v1 = abs(1 - final_v1)
    # final_u2 = abs(1 - final_u2)
    final_v2 = abs(1 - final_v2)
    # final_u3 = abs(1 - final_u3)

    texture_page_per_material[texture_img_no] = texture_dir


    return [texture_img_no, [final_u0, final_v0], [final_u1, final_v1], [final_u2, final_v2], texture_dir]


def calc_uvs(u0, v0, u1, v1, u2, v2, u3, v3, texture_page, texture_numbers, texture_page_per_material):
    global texture_pack
    TEXTURE_NORM_SIZE = 32
    TEXTURE_NORM_SQUARES = 8
    av_u = calc_av_uv(u0, u1, u2, u3)
    av_v = calc_av_uv(v0, v1, v2, v3)
    av_u = int(av_u/TEXTURE_NORM_SIZE)
    av_v = int(av_v/TEXTURE_NORM_SIZE)

    base_u = av_u * TEXTURE_NORM_SIZE
    base_v = av_v * TEXTURE_NORM_SIZE

    final_u0 = calc_final_uv(u0, base_u)
    final_v0 = calc_final_uv(v0, base_v)
    final_u1 = calc_final_uv(u1, base_u)
    final_v1 = calc_final_uv(v1, base_v)
    final_u2 = calc_final_uv(u2, base_u)
    final_v2 = calc_final_uv(v2, base_v)
    final_u3 = calc_final_uv(u3, base_u)
    final_v3 = calc_final_uv(v3, base_v)

    page = av_u + av_v * TEXTURE_NORM_SQUARES + texture_page * TEXTURE_NORM_SQUARES * TEXTURE_NORM_SQUARES
    # print(f'page = {page}')

    if page < 64 * 9:
        texture_page_offset = 64*8
        texture_pack = "insides"
        texture_dir = "insides"
    elif page < 64 * 11:
        texture_page_offset = 64*9
        texture_pack = "people"
        texture_dir = "people"
    elif page < 64 * 18:
        texture_page_offset = 64*11
        texture_pack = "prims"
        texture_dir = "prims"
    elif page < 64 * 21:
        texture_page_offset = 64*18
        texture_pack = "people2"
        texture_dir = "people2"
    else:
        texture_page_offset = 0
        texture_pack = "UNDEFINED"
        texture_dir = "UNDEFINED"

    texture_img_no = page-texture_page_offset

    if texture_img_no not in texture_numbers:
        texture_numbers.append(texture_img_no)
    # print(f'texture_img={texture_img_no}')

    # final_u0 = abs(1 - final_u0)
    final_v0 = abs(1 - final_v0)
    # final_u1 = abs(1 - final_u1)
    final_v1 = abs(1 - final_v1)
    # final_u2 = abs(1 - final_u2)
    final_v2 = abs(1 - final_v2)
    # final_u3 = abs(1 - final_u3)
    final_v3 = abs(1 - final_v3)

    texture_page_per_material[texture_img_no] = texture_dir

    return [texture_img_no, [final_u0, final_v0], [final_u1, final_v1], [final_u2, final_v2], [final_u3, final_v3], texture_dir]


def read_nprim(nprim_file_name):
    with open(nprim_file_name, "rb+") as file:
        file_chunk = file.read()

    return file_chunk


def gui(df, df_points, df_quadrangles, df_triangles):
    root = tk.Tk()
    root.title('nprim visualizer')

    frame = tk.Frame(root)
    frame.pack(fill='both', expand=True)

    pt = Table(frame, dataframe=df)
    pt.show()

    # pt.setColumnColors(cols=0, clr='red')
    # pt.setColumnColors(cols=[1, 2], clr='green')
    # pt.setColumnColors(cols=[-1], clr='#a0a0ff')

    # tk.Button(root, text="Points coordinates", command=lambda: open_points(df_points)).pack(pady=10)
    # tk.Button(root, text="Triangles coordinates", command=lambda: open_points(df_triangles)).pack(pady=10)
    # tk.Button(root, text="Quadrangles", command=lambda: open_quadrangles(df_quadrangles)).pack(pady=10)
    root.mainloop()


def multiprim_count(cursor, binary_data):
    multiprims_count = int.from_bytes(binary_data[cursor:cursor+4], "little")

    cursor += 4

    return [cursor, multiprims_count]


# body parts count
def prim_count(cursor, binary_data):
    save_type = int.from_bytes(binary_data[cursor:cursor+4], "little")
    s0 = int.from_bytes(binary_data[cursor+4:cursor+8], "little")
    e0 = int.from_bytes(binary_data[cursor+8:cursor+12], "little")

    cursor += 12
    prims_count = e0 - s0

    return [cursor, prims_count]


def load_insert_game_chunk(cursor, binary_data, all_filename, prims_count, body_parts):

    save_type = int.from_bytes(binary_data[cursor:cursor+4], "little")
    cursor += 4
    ElementCount = int.from_bytes(binary_data[cursor:cursor+4], "little")
    MaxPeopleTypes = int.from_bytes(binary_data[cursor+4:cursor+6], "little")
    MaxAnimFrames = int.from_bytes(binary_data[cursor+6:cursor+8], "little")
    MaxElements = int.from_bytes(binary_data[cursor+8:cursor+12], "little")
    MaxKeyFrames = int.from_bytes(binary_data[cursor+12:cursor+14], "little")
    MaxFightCols = int.from_bytes(binary_data[cursor+14:cursor+16], "little")

    cursor += 16
    PeopleTypesArray = []

    for i in range(MaxPeopleTypes):
        PeopleTypes = []
        for j in range(20):
            BodyDef = int.from_bytes(binary_data[cursor:cursor + 1], "little")
            cursor += 1
            PeopleTypes.append(BodyDef)

        PeopleTypesArray.append(PeopleTypes)

    check = int.from_bytes(binary_data[cursor:cursor+2], "little")

    addr1 = int.from_bytes(binary_data[cursor+2:cursor+6], "little")

    # struct GameKeyFrame
    # {
    # UBYTE XYZIndex;
    # UBYTE TweenStep;
    # SWORD Flags;
    # GameKeyFrameElement * FirstElement = nullptr;
    # GameKeyFrame * PrevFrame = nullptr, *NextFrame = nullptr;
    # GameFightCol * Fight = nullptr;
    # };

    cursor += 6
    AnimKeyFrames = []
    for i in range(MaxKeyFrames):
        single_anim_key_frame = GameKeyFrame()
        single_anim_key_frame.XYZIndex = int.from_bytes(binary_data[cursor:cursor + 1], "little")
        single_anim_key_frame.TweenStep = int.from_bytes(binary_data[cursor+1:cursor + 2], "little")
        single_anim_key_frame.Flags = int.from_bytes(binary_data[cursor+2:cursor + 4], "little")
        single_anim_key_frame.FirstElement = int.from_bytes(binary_data[cursor+4:cursor + 8], "little")
        single_anim_key_frame.PrevFrame = int.from_bytes(binary_data[cursor+8:cursor + 12], "little")
        single_anim_key_frame.NextFrame = int.from_bytes(binary_data[cursor+12:cursor + 16], "little")
        single_anim_key_frame.Fight = int.from_bytes(binary_data[cursor+16:cursor + 20], "little")

        cursor += 20

        AnimKeyFrames.append(single_anim_key_frame)

    # cursor += 16

    check = int.from_bytes(binary_data[cursor:cursor+2], "little")
    addr2 = int.from_bytes(binary_data[cursor+2:cursor+6], "little")

    cursor += 6

    TheElements = []
    for i in range(MaxElements):
        single_game_key_frame_element = GameKeyFrameElement()
        single_game_key_frame_element.CMatrix0 = int.from_bytes(binary_data[cursor:cursor + 4], "little", signed=True)
        single_game_key_frame_element.CMatrix1 = int.from_bytes(binary_data[cursor+4:cursor + 8], "little", signed=True)
        single_game_key_frame_element.CMatrix2 = int.from_bytes(binary_data[cursor+8:cursor + 12], "little", signed=True)
        single_game_key_frame_element.OffsetX = int.from_bytes(binary_data[cursor+12:cursor + 14], "little", signed=True)
        single_game_key_frame_element.OffsetY = int.from_bytes(binary_data[cursor+14:cursor + 16], "little", signed=True)
        single_game_key_frame_element.OffsetZ = int.from_bytes(binary_data[cursor+16:cursor + 18], "little", signed=True)
        single_game_key_frame_element.Pad = int.from_bytes(binary_data[cursor+18:cursor + 20], "little")

        TheElements.append(single_game_key_frame_element)

        cursor += 20

    check = int.from_bytes(binary_data[cursor:cursor+2], "little")
    cursor += 2

    AnimList = []
    for i in range(MaxAnimFrames):
        GameKeyFrameStructPointer = int.from_bytes(binary_data[cursor:cursor + 4], "little")
        # single_anim_key_frame = GameKeyFrame()
        # single_anim_key_frame.XYZIndex = int.from_bytes(binary_data[cursor:cursor + 1], "little")
        # single_anim_key_frame.TweenStep = int.from_bytes(binary_data[cursor + 1:cursor + 2], "little")
        # single_anim_key_frame.Flags = int.from_bytes(binary_data[cursor + 2:cursor + 4], "little")
        # single_anim_key_frame.FirstElement = int.from_bytes(binary_data[cursor + 4:cursor + 8], "little")
        # single_anim_key_frame.PrevFrame = int.from_bytes(binary_data[cursor + 8:cursor + 12], "little")
        # single_anim_key_frame.NextFrame = int.from_bytes(binary_data[cursor + 12:cursor + 16], "little")
        # single_anim_key_frame.Fight = int.from_bytes(binary_data[cursor + 16:cursor + 20], "little")

        cursor += 4

        AnimList.append(GameKeyFrameStructPointer)

    check = int.from_bytes(binary_data[cursor:cursor + 2], "little")
    addr3 = int.from_bytes(binary_data[cursor+2:cursor+6], "little")
    cursor += 6

    FightCols = []
    for i in range(MaxFightCols):
        single_game_fight_col = GameFightCol()
        single_game_fight_col.Dist1 = int.from_bytes(binary_data[cursor:cursor + 2], "little")
        single_game_fight_col.Dist2 = int.from_bytes(binary_data[cursor+2:cursor + 4], "little")

        single_game_fight_col.Angle = int.from_bytes(binary_data[cursor+4:cursor + 5], "little")
        single_game_fight_col.Priority = int.from_bytes(binary_data[cursor+5:cursor + 6], "little")
        single_game_fight_col.Damage = int.from_bytes(binary_data[cursor+6:cursor + 7], "little")
        single_game_fight_col.Tween = int.from_bytes(binary_data[cursor+7:cursor + 8], "little")

        single_game_fight_col.AngleHitFrom = int.from_bytes(binary_data[cursor+8:cursor + 9], "little")
        single_game_fight_col.Height = int.from_bytes(binary_data[cursor+9:cursor + 10], "little")
        single_game_fight_col.Width = int.from_bytes(binary_data[cursor+10:cursor + 11], "little")
        single_game_fight_col.Dummy = int.from_bytes(binary_data[cursor+11:cursor + 12], "little")

        single_game_fight_col.Next = int.from_bytes(binary_data[cursor + 12:cursor + 16], "little")

        cursor += 16

        FightCols.append(single_game_fight_col)

    check = int.from_bytes(binary_data[cursor:cursor + 2], "little")

    # body_parts_count = 17
    # body_parts_count = prims_count
    body_parts_count = ElementCount
    elements_chunks = [TheElements[x:x+body_parts_count] for x in range(0, len(TheElements), body_parts_count)]
    # body_parts_offsets_dict = util_print(elements_chunks[0], body_parts)

    for index, chunk in enumerate(elements_chunks):
        [body_parts_offsets_dict, rotation_json_string] = util_print(chunk, body_parts)
        if body_parts_offsets_dict:
            results_path = "output/body-part-offsets/" + all_filename[:-4]
            Path(results_path).mkdir(parents=True, exist_ok=True)
            frame_path = results_path + "/frame " + str(index) + ".txt"
            rotation_frame_path = results_path + "/rotation_matrix_frame " + str(index) + ".json"

            write_to_file(frame_path, body_parts_offsets_dict)
            write_to_file(rotation_frame_path, rotation_json_string)

    # util_print(TheElements[0:17])

    return [cursor]


def util_print(elements, body_parts):
    # baalrog_body_parts = ['hips.obj', 'rthigh.obj', 'rshin.obj', 'rheel.obj', 'rtoe.obj',
    #                       'body.obj', 'rshoulder.obj', 'rforarm.obj', 'rfist.obj', 'head.obj',
    #                       'lshoulder.obj', 'lforarm.obj', 'lfist.obj', 'lthigh.obj',
    #                       'lshin.obj', 'lheel.obj', 'ltoe.obj']

    # concated_string = 'part_name_offset_dict = {'
    concated_string = '{'
    rotation_json_string = "{"
    for part, elem in zip(body_parts, elements):
        concated_string = concated_string + '"' + part + '": [' + str(elem.OffsetX) + ',' \
                          + str(elem.OffsetY) + ',' + str(elem.OffsetZ) + '],\n'
        cm = np.array([elem.CMatrix0, elem.CMatrix1, elem.CMatrix2], dtype=np.int32)
        print(part)
        rotation_matrix = uc_matrix_utils.uncompress_matrix(cm)

        rotation_json_string = rotation_json_string + '"' + part + '": [' + str(rotation_matrix) + '],\n'
        # point_
        # np.matmul()

    # remove new line and comma from the last line
    concated_string = concated_string[:-2]
    concated_string = concated_string + ' } '

    rotation_json_string = rotation_json_string[:-2]
    rotation_json_string = rotation_json_string + ' } '

    # print(rotation_json_string)

    return [concated_string, rotation_json_string]


def write_to_file(filepath, content):
    with open(filepath, "w") as output_file:
        output_file.write(content)


def grab_all_files_as_list(dir_path):
    all_files_list = []
    for filename in glob.iglob(f'{dir_path}/*.all'):
        all_files_list.append(os.path.basename(filename))

    return all_files_list


def app():
    # binary_data = read_nprim("pzi_prim337.pzi")
    # binary_data = read_nprim("all/DARCI1.all")
    all_filename_list = (grab_all_files_as_list("res/all/"))
    # all_filename_list = ["banesuit.all"]
    all_filename_list = ["anim003.all"]

    # all_filename = "anim002.all"
    for all_filename in all_filename_list:
        # all_filename = "DARCI1.all"
        binary_data = read_nprim("res/all/" + all_filename)
        # binary_data = read_nprim("all/anim001.all")

        cursor = 4
        [cursor, multiprims_count] = multiprim_count(cursor, binary_data)
        cursor = 8

        for k in range(multiprims_count):
        # for k in range(1):
            results_path = "output/all-obj/" + all_filename[:-4] + "/" + str(k)
            Path(results_path).mkdir(parents=True, exist_ok=True)
            [cursor, prims_count] = prim_count(cursor, binary_data)
            next_prim_point = 1
            names = []
            for i in range(prims_count):
                [df_points, df_quadrangles, df_triangles, name, cursor, next_prim_point] =\
                    convert_nprim_binary_to_readable_data(cursor, next_prim_point, binary_data)
                next_prim_point = 1
                output_file_name = results_path + "/" + name + ".obj"
                names.append(name)
                export_to_obj_format_with_uvs(output_file_name, name, df_points, df_quadrangles, df_triangles)

                # texture_file_numbers = []
                # for index, row in enumerate(df_triangles):
                #     ua = row["u_a"]
                #     va = row["v_a"]
                #     ub = row["u_b"]
                #     vb = row["v_b"]
                #     uc = row["u_c"]
                #     vc = row["v_c"]
                #     texture_page = row["texture_id_group"]
                #
                #     result_with_texture_page = (
                #         calc_uvs_triangles(ua, va, ub, vb, uc, vc, texture_page, texture_file_numbers))
                # print(texture_file_numbers)

                # write_obj_file(df_points, df_triangles, df_quadrangles, output_file_name)
        # gui(df_points, df_quadrangles, df_triangles, df_triangles)

        load_insert_game_chunk(cursor, binary_data, all_filename, prims_count, names)

        print(names)


def test_read_rotation_json():
    filepath = "output/body-part-offsets/darci1/rotation_matrix_frame 0.json"
    # reading the data from the file
    with open(filepath) as f:
        data = f.read()

    # print("Data type before reconstruction : ", type(data))

    # reconstructing the data as a dictionary
    js = json.loads(data)

    for b_part in js.keys():
        print(np.asarray(js[b_part], dtype=np.float32))


if __name__ == '__main__':
    app()
