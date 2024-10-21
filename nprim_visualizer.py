from pandastable import Table
import pandas as pd
import tkinter as tk
import numpy as np
import os
from pathlib import Path
import glob

from enum import Enum


pd.set_option('future.no_silent_downcasting', True)


collision_type_map = {
    0: "Normal",
    1: "None",
    2: "Tree",  # central cylindrical collision
    3: "Reduced"  # collision a bit smaller than the object
}


class PrimFormat(Enum):
    UNDEFINED = 0
    NPRIM = 1
    PRIM = 2


texture_set = set()


def determine_file_format(filename):
    """
    Determines the file format based on the filename.

    Args:
        filename (str): The name of the file.

    Returns:
        int: 1 if it's an nprim format, 2 if it's a prim format, 0 if it's something else.
    """

    # Get the base name of the file (removes directory path)
    basename = os.path.basename(filename)

    # Check the prefix of the filename
    if basename.startswith("nprim"):
        return 1
    elif basename.startswith("prim"):
        return 2
    else:
        return 0


def export_to_obj_format(filename, nprim_name, df_points, df_quadrangles, df_triangles):
    vertices = df_points[["x", "y", "z"]].to_string(index=False, header=False)
    vertices_as_list = vertices.split('\n')
    append_str = "v "
    vertices_as_list = [append_str + v for v in vertices_as_list]
    vertices_as_list = '\n'.join(vertices_as_list)


    quadrangles = df_quadrangles[["point_a_id", "point_b_id", "point_c_id", "point_d_id"]].to_string(index=False, header=False)

    # Path(filename).stem
    # file_wo_ext = os.path.splitext(filename)[0] + "/out/" + filename + ".obj"
    texture_file_numbers = []
    output_filename = "output/objs/retail/" + Path(filename).stem + "-" + nprim_name + '.obj'
    output_filename = output_filename.replace('\\r', '')
    uv_set = []
    uv_full_set = []
    textures_per_quad_face = []
    for index, row in df_quadrangles.iterrows():
        ua = row["u_a"]
        va = row["v_a"]
        ub = row["u_b"]
        vb = row["v_b"]
        uc = row["u_c"]
        vc = row["v_c"]
        ud = row["u_d"]
        vd = row["v_d"]
        texture_page = row["texture_id_group"]

        result_with_texture_page = (calc_uvs(ua, va, ub, vb, uc, vc, ud, vd, texture_page, texture_file_numbers))

        result = result_with_texture_page[1:]

        for r in result:
            uv_full_set.append(r)
            if r not in uv_set:
                uv_set.append(r)

        textures_per_quad_face.append(result_with_texture_page[0])

    texture_per_triangle_face = []
    triangles_uv_full_set = []
    for index, row in df_triangles.iterrows():
        ua = row["u_a"]
        va = row["v_a"]
        ub = row["u_b"]
        vb = row["v_b"]
        uc = row["u_c"]
        vc = row["v_c"]
        texture_page = row["texture_id_group"]

        result_with_texture_page = (calc_uvs_triangles(ua, va, ub, vb, uc, vc, texture_page, texture_file_numbers))

        result = result_with_texture_page[1:]

        for r in result:
            triangles_uv_full_set.append(r)

        texture_per_triangle_face.append(result_with_texture_page[0])

    # unique_data = [list(x) for x in set(tuple(x) for x in uv_set)]

    # print(uv_full_set)
    lines_per_material = {}
    with open(output_filename, "w") as output_file:
        output_file.write(vertices_as_list)

        # for uv in uv_set:
        for uv in uv_full_set:
            vt_line = f"\nvt {uv[0]} {uv[1]}"
            output_file.write(vt_line)

        for uv in triangles_uv_full_set:
            vt_line = f"\nvt {uv[0]} {uv[1]}"
            output_file.write(vt_line)

        # output_file.write("\nusemtl Material.001")
        for index, row in df_quadrangles.iterrows():
            a = (df_points[df_points["p_global_id"] == row["point_a_id"]].index.tolist())
            b = (df_points[df_points["p_global_id"] == row["point_b_id"]].index.tolist())
            c = (df_points[df_points["p_global_id"] == row["point_c_id"]].index.tolist())
            d = (df_points[df_points["p_global_id"] == row["point_d_id"]].index.tolist())

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
            line = f"\nf {str(a[0] + 1)}/{uvaid} {str(b[0] + 1)}/{uvbid} {str(d[0] + 1)}/{uvdid} {str(c[0] + 1)}/{uvcid}"
            if textures_per_quad_face[index] in lines_per_material:
                lines_per_material[textures_per_quad_face[index]].append(line)
            else:
                lines_per_material[textures_per_quad_face[index]] = []
                lines_per_material[textures_per_quad_face[index]].append(line)

            # output_file.write(line)

        for index, row in df_triangles.iterrows():
            a = (df_points[df_points["p_global_id"] == row["point_a_id"]].index.tolist())
            b = (df_points[df_points["p_global_id"] == row["point_b_id"]].index.tolist())
            c = (df_points[df_points["p_global_id"] == row["point_c_id"]].index.tolist())

            [ua, va] = triangles_uv_full_set[index*3]
            [ub, vb] = triangles_uv_full_set[index*3+1]
            [uc, vc] = triangles_uv_full_set[index*3+2]

            uvaid = triangles_uv_full_set.index([ua, va]) + 1 + len(uv_full_set)
            uvbid = triangles_uv_full_set.index([ub, vb]) + 1 + len(uv_full_set)
            uvcid = triangles_uv_full_set.index([uc, vc]) + 1 + len(uv_full_set)

            line = f"\nf {str(a[0] + 1)}/{uvaid} {str(b[0] + 1)}/{uvbid} {str(c[0] + 1)}/{uvcid}"

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

    output_material_filename = "output/objs/retail/" + Path(filename).stem + "-" + nprim_name + '.mtl'
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
            # map_Kd = f"map_Kd C:/Games/Urban Chaos/server/textures/shared/prims/tex{key:03d}hi.tga\n"
            map_Kd = f"map_Kd C:/Games/Urban Chaos/server/textures/shared/prims/tex{key:03d}hi.tga\n"
            texture_set.add(map_Kd)
            # map_Kd = f"map_Kd C:/UC_PROTOTYPE/UrbanChaos/server/textures/shared/prims/tex{key:03d}.tga\n"
            output_material_file.writelines([l1, l2, l3, l4, l5, l6, l7, l8, map_Kd])




            # [ua, va] = uv_full_set[index * 4]
            # [ub, vb] = uv_full_set[index * 4 + 1]
            # [uc, vc] = uv_full_set[index * 4 + 2]

    # print(quadrangles)
    # print(f'filename = {filename}')
    # print(f'texture_file_numbers = {texture_file_numbers}')
    # print(f'lines_per_material = {lines_per_material}')



def read_nprim(nprim_file_name):
    file_chunk = None
    with open(nprim_file_name, "rb+") as file:
        # file_chunk.append(file.read())
        file_chunk = file.read()

    return file_chunk


def create_blank_nprim_dataframe():
    df = pd.DataFrame(columns=['Signature', 'Name', 'FirstPointID', 'LastPointID', 'PointCount', 'FirstQuadrangleID', 'LastQuadrangleID',
                               'QQuadrangleCount', 'FirstTriangleID', 'LastTriangleID', 'TriangleCount', 'CollisionType', 'Radius', 'X', 'Y', 'Z', 'Next',
                               'Previous'])

    return df


# Function to safely cast to int16
def safe_int16(value):
    # Clamp the value to the range of int16
    if value > 32767:
        value -= 65536
    return np.int16(value)


def convert_nprim_binary_to_readable_data(data, prim_version):
    readable_data = []
    cursor = 0

    if prim_version == PrimFormat.NPRIM.value:
        signature = int.from_bytes(data[0:2], "little")
        null_terminated_pos = data.find(b'\00')
        name = data[2:null_terminated_pos-1].decode("utf-8")
        first_point_id = int.from_bytes(data[34: 36], "little")
        last_point_id = int.from_bytes(data[36: 38], "little")
        first_quadrangle_id = int.from_bytes(data[38: 40], "little")
        last_quadrangle_id = int.from_bytes(data[40: 42], "little")
        first_triangle_id = int.from_bytes(data[42: 44], "little")
        last_triangle_id = int.from_bytes(data[44: 46], "little")
        collision_type = int.from_bytes(data[46:47], "little")
        reaction_to_impact_by_vehicle = int.from_bytes(data[47:48], "little")
        shadow_type = int.from_bytes(data[48:49], "little")
        various_properties = int.from_bytes(data[49:50], "little")
        cursor = 50
    elif prim_version == PrimFormat.PRIM.value:
        null_terminated_pos = data.find(b'\00')
        name = data[0:null_terminated_pos - 1].decode("utf-8")
        first_point_id = int.from_bytes(data[32: 34], "little")
        last_point_id = int.from_bytes(data[34: 36], "little")
        first_quadrangle_id = int.from_bytes(data[36: 38], "little")
        last_quadrangle_id = int.from_bytes(data[38: 40], "little")
        first_triangle_id = int.from_bytes(data[40: 42], "little")
        last_triangle_id = int.from_bytes(data[42: 44], "little")
        collision_type = int.from_bytes(data[44:45], "little")
        reaction_to_impact_by_vehicle = int.from_bytes(data[45:46], "little")
        shadow_type = int.from_bytes(data[46:47], "little")
        various_properties = int.from_bytes(data[47:48], "little")
        cursor = 56

    collision_type = collision_type_map[collision_type]

    point_count = last_point_id - first_point_id
    quadrangle_count = last_quadrangle_id - first_quadrangle_id
    triangle_count = last_triangle_id - first_triangle_id

    if prim_version == PrimFormat.NPRIM.value:
        nprim_dict = {
            "signature": signature,
            "name": name,
            "first_point_id": first_point_id,
            "last_point_id": last_point_id,
            "point_count": point_count,

            "first_quadrangle_id": first_quadrangle_id,
            "last_quadrangle_id": last_quadrangle_id,
            "quadrangle_count": quadrangle_count,

            "first_triangle_id": first_triangle_id,
            "last_triangle_id": last_triangle_id,
            "triangle_count": triangle_count,

            "collision_type": collision_type,
            "reaction_to_impact_by_vehicle": reaction_to_impact_by_vehicle,
            "shadow_type": shadow_type,
            "various_properties": various_properties
        }
    elif prim_version == PrimFormat.PRIM.value:
        nprim_dict = {
            "name": name,
            "first_point_id": first_point_id,
            "last_point_id": last_point_id,
            "point_count": point_count,

            "first_quadrangle_id": first_quadrangle_id,
            "last_quadrangle_id": last_quadrangle_id,
            "quadrangle_count": quadrangle_count,

            "first_triangle_id": first_triangle_id,
            "last_triangle_id": last_triangle_id,
            "triangle_count": triangle_count,

            "collision_type": collision_type,
            "reaction_to_impact_by_vehicle": reaction_to_impact_by_vehicle,
            "shadow_type": shadow_type,
            "various_properties": various_properties
        }

    readable_data.append(nprim_dict)

    points = []
    for p_id in range(point_count):
        p_global_id = first_point_id + p_id
        # x = np.int16(int.from_bytes(data[cursor:cursor+2], "little"))
        # y = np.int16(int.from_bytes(data[cursor+2:cursor+4], "little"))
        # z = np.int16(int.from_bytes(data[cursor+4:cursor+6], "little"))

        # Fixing the lines with safe clamping and casting
        x = safe_int16(int.from_bytes(data[cursor:cursor + 2], "little"))
        y = safe_int16(int.from_bytes(data[cursor + 2:cursor + 4], "little"))
        z = safe_int16(int.from_bytes(data[cursor + 4:cursor + 6], "little"))

        cursor = cursor + 6

        p_dict = {
            "p_global_id": p_global_id,
            "x": x,
            "y": y,
            "z": z
        }
        points.append(p_dict)
        result = ' '.join(f'{value:02f}' for value in p_dict.values())
        # print(result)

    triangles = []
    for t_id in range(triangle_count):
        texture_id_group = int.from_bytes(data[cursor:cursor + 1], "little")
        properties = int.from_bytes(data[cursor + 1:cursor + 2], "little")

        point_a_id = int.from_bytes(data[cursor + 2:cursor + 4], "little")
        point_b_id = int.from_bytes(data[cursor + 4:cursor + 6], "little")
        point_c_id = int.from_bytes(data[cursor + 6:cursor + 8], "little")

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
    for q_id in range(quadrangle_count):
        texture_id_group = int.from_bytes(data[cursor:cursor+1], "little")
        properties = int.from_bytes(data[cursor+1:cursor+2], "little")

        point_a_id = int.from_bytes(data[cursor+2:cursor+4], "little")
        point_b_id = int.from_bytes(data[cursor+4:cursor+6], "little")
        point_c_id = int.from_bytes(data[cursor+6:cursor+8], "little")
        point_d_id = int.from_bytes(data[cursor+8:cursor+10], "little")

        # U position of the point A on the texture grid (u)
        u_a = int.from_bytes(data[cursor+10:cursor+11], "little")
        # V position of the point A on the texture grid (v)
        v_a = int.from_bytes(data[cursor+11:cursor+12], "little")
        u_b = int.from_bytes(data[cursor+12:cursor+13], "little")
        v_b = int.from_bytes(data[cursor+13:cursor+14], "little")
        u_c = int.from_bytes(data[cursor+14:cursor+15], "little")
        v_c = int.from_bytes(data[cursor+15:cursor+16], "little")
        u_d = int.from_bytes(data[cursor+16:cursor+17], "little")
        v_d = int.from_bytes(data[cursor+17:cursor+18], "little")

        # Used for people
        bright_a = int.from_bytes(data[cursor+18:cursor+19], "little")
        bright_b = int.from_bytes(data[cursor+19:cursor+20], "little")
        bright_c = int.from_bytes(data[cursor+20:cursor+21], "little")
        bright_d = int.from_bytes(data[cursor+21:cursor+22], "little")
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

    # triangles
    # for t_id in range(triangle_count):
    #     t_texture_page = int.from_bytes(data[cursor:cursor+1])

    # print(points)
    return [readable_data, points, quadrangles, triangles]


def fill_dataframe_with_nprim_data(nprim_filename, df):
    data = read_nprim(nprim_filename)

    prim_version = determine_file_format(nprim_filename)

    [readable_data, points, quadrangles, triangles] = convert_nprim_binary_to_readable_data(data, prim_version)
    df = pd.DataFrame.from_records(readable_data)
    df_points = pd.DataFrame.from_records(points)
    df_quadrangles = pd.DataFrame.from_records(quadrangles)
    df_triangles = pd.DataFrame.from_records(triangles)

    return [df, df_points, df_quadrangles, df_triangles]


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

    tk.Button(root, text="Points coordinates", command=lambda: open_points(df_points)).pack(pady=10)
    tk.Button(root, text="Triangles coordinates", command=lambda: open_points(df_triangles)).pack(pady=10)
    tk.Button(root, text="Quadrangles", command=lambda: open_quadrangles(df_quadrangles)).pack(pady=10)
    root.mainloop()


def open_points(df_points):
    w2 = tk.Toplevel()
    w2.title("Modal window")
    w2.geometry("700x700")

    frame = tk.Frame(w2)
    frame.pack(fill='both', expand=True)

    pt = Table(frame, dataframe=df_points)
    pt.show()


def open_quadrangles(df_quadrangles):
    w2 = tk.Toplevel()
    w2.title("Modal window")
    w2.geometry("700x700")

    frame = tk.Frame(w2)
    frame.pack(fill='both', expand=True)

    pt = Table(frame, dataframe=df_quadrangles)
    pt.show()


def grab_all_nprm_filenames():
    prims_filenames = []
    for root, dirs, files in os.walk("res/nprims"):
        for file in files:
            if file.endswith(".prm"):
                prims_filenames.append(os.path.join(root, file))

    return prims_filenames


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


def calc_uvs_triangles(u0, v0, u1, v1, u2, v2, texture_page, texture_numbers):
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

    texture_img_no = page-64*11
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

    return [texture_img_no, [final_u0, final_v0], [final_u1, final_v1], [final_u2, final_v2]]


def calc_uvs(u0, v0, u1, v1, u2, v2, u3, v3, texture_page, texture_numbers):
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

    texture_img_no = page-64*11

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

    return [texture_img_no, [final_u0, final_v0], [final_u1, final_v1], [final_u2, final_v2], [final_u3, final_v3]]




# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡾⠋⠉⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠃⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⢀⡏⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣠⣤⣤⣤⣤⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⡏⠀⠀⠀⠀⢸⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡤⠴⠒⠊⠉⠉⠀⠀⣿⣿⣿⠿⠋⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⢀⡠⠼⠴⠒⠒⠒⠒⠦⠤⠤⣄⣀⠀⢀⣠⠴⠚⠉⠀⠀⠀⠀⠀⠀⠀⠀⣼⠿⠋⠁⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⣇⠔⠂⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢨⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀⣀⡤⠖⠋⠁⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⢰⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⠤⠒⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⢀⡟⠀⣠⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⢻⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⡤⠤⢴
# ⠀⠀⠀⠀⠀⠀⣸⠁⣾⣿⣀⣽⡆⠀⠀⠀⠀⠀⠀⠀⢠⣾⠉⢿⣦⠀⠀⠀⢸⡀⠀⠀⢀⣠⠤⠔⠒⠋⠉⠉⠀⠀⠀⠀⢀⡞
# ⠀⠀⠀⠀⠀⢀⡏⠀⠹⠿⠿⠟⠁⠀⠰⠦⠀⠀⠀⠀⠸⣿⣿⣿⡿⠀⠀⠀⢘⡧⠖⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼⠀
# ⠀⠀⠀⠀⠀⣼⠦⣄⠀⠀⢠⣀⣀⣴⠟⠶⣄⡀⠀⠀⡀⠀⠉⠁⠀⠀⠀⠀⢸⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠁⠀
# ⠀⠀⠀⠀⢰⡇⠀⠈⡇⠀⠀⠸⡾⠁⠀⠀⠀⠉⠉⡏⠀⠀⠀⣠⠖⠉⠓⢤⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠃⠀⠀
# ⠀⠀⠀⠀⠀⢧⣀⡼⠃⠀⠀⠀⢧⠀⠀⠀⠀⠀⢸⠃⠀⠀⠀⣧⠀⠀⠀⣸⢹⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡰⠃⠀⠀⠀
# ⠀⠀⠀⠀⠀⠈⢧⡀⠀⠀⠀⠀⠘⣆⠀⠀⠀⢠⠏⠀⠀⠀⠀⠈⠳⠤⠖⠃⡟⠀⠀⠀⢾⠛⠛⠛⠛⠛⠛⠛⠛⠁⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠙⣆⠀⠀⠀⠀⠈⠦⣀⡴⠋⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⠙⢦⠀⠀⠘⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⢠⡇⠙⠦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠴⠋⠸⡇⠈⢳⡀⠀⢹⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⡼⣀⠀⠀⠈⠙⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⣷⠴⠚⠁⠀⣀⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⡴⠁⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣆⡴⠚⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⣼⢷⡆⠀⣠⡴⠧⣄⣇⠀⠀⠀⠀⠀⠀⠀⢲⠀⡟⠀⠀⠀⠀⠀⠀⠀⢀⡇⣠⣽⢦⣄⢀⣴⣶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⡿⣼⣽⡞⠁⠀⠀⠀⢹⡀⠀⠀⠀⠀⠀⠀⠈⣷⠃⠀⠀⠀⠀⠀⠀⠀⣼⠉⠁⠀⠀⢠⢟⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⣷⠉⠁⢳⠀⠀⠀⠀⠈⣧⠀⠀⠀⠀⠀⠀⠀⣻⠀⠀⠀⠀⠀⠀⠀⣰⠃⠀⠀⠀⠀⠏⠀⠀⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠹⡆⠀⠈⡇⠀⠀⠀⠀⠘⣆⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⣰⠃⠀⠀⠀⠀⠀⠀⠀⣸⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⢳⡀⠀⠙⠀⠀⠀⠀⠀⠘⣆⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⣰⠃⠀⠀⠀⠀⢀⡄⠀⢠⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⢳⡀⣰⣀⣀⣀⠀⠀⠀⠘⣦⣀⠀⠀⠀⡇⠀⠀⠀⢀⡴⠃⠀⠀⠀⠀⠀⢸⡇⢠⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠉⠉⠀⠀⠈⠉⠉⠉⠙⠻⠿⠾⠾⠻⠓⢦⠦⡶⡶⠿⠛⠛⠓⠒⠒⠚⠛⠛⠁⠀⠀



def app():
    prims_filenames = grab_all_nprm_filenames()
    df = create_blank_nprim_dataframe()
    nprim = "res/nprims/nprim001.prm"
    # for p in prims_filenames:
    # nprim = "res/nprims/nprim058.prm"

    nprim = "res/nprims/retail/prim138.prm"


    # nprim = "res/nprims/nprim216.prm" # switch
    # nprim = "res/nprims/nprim074.prm" # helibody
    # nprim = "res/nprims/nprim260.prm" # helibody
    # nprim = "res/nprims/nprim162.prm" # helibody
    # nprim = "res/nprims/nprim120.prm"
    # nprim = "res/nprims/nprim162.prm" # stopsign
    # nprim = "res/nprims/nprim143.prm" # gun
    # nprim = "res/nprims/nprim036.prm" #
    single_nprm = True
    # calc_uvs(105, 47, 98, 38, 119, 47, 126, 38)
    if single_nprm:
        [df, df_points, df_quadrangles, df_triangles] = fill_dataframe_with_nprim_data(nprim, df)
        nprim_name = (df['name'].to_string(index=False, header=False))
        export_to_obj_format(nprim, nprim_name, df_points, df_quadrangles, df_triangles)
        gui(df, df_points, df_quadrangles, df_triangles)
    else:
        nprims_directory = 'res/nprims/retail/'
        # nprims_directory = 'res/nprims/'
        for filename in glob.iglob(f'{nprims_directory}/*.prm'):
            print(filename)
            # if filename == 'res/nprims/prototype\prim046.prm' or filename == 'res/nprims/prototype\prim080.prm'\
            #         or filename == 'res/nprims/prototype\prim105.prm' or filename == 'res/nprims/prototype\prim106.prm'\
            #         or filename == 'res/nprims/prototype\prim131.prm' or filename == 'res/nprims/prototype\prim132.prm':
            #     continue
            [df, df_points, df_quadrangles, df_triangles] = fill_dataframe_with_nprim_data(filename, df)
            nprim_name = (df['name'].to_string(index=False, header=False))
            export_to_obj_format(filename, nprim_name, df_points, df_quadrangles, df_triangles)

    print(texture_set)


if __name__ == '__main__':
    app()
