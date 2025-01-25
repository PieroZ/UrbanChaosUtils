import struct

from obj_to_dataframe import *


def faces_count(df_faces):
    return len(df_faces)


def create_tex_from_dataframes(output_tex_filename, df_quadrangles, df_triangles):
    with open(output_tex_filename, "wb+") as file:
        save_type = 1
        # save_type_bytes = bytearray(save_type)
        #
        # file.write(save_type_bytes)

        triangle_faces_count = faces_count(df_triangles)
        quadrangle_faces_count = faces_count(df_quadrangles)

        file.write(struct.pack('1l', save_type))
        file.write(struct.pack('1h', quadrangle_faces_count))

        # for i in range(quadrangle_faces_count):
        for index, series in df_quadrangles.iterrows():
            file.write(struct.pack('1B', df_quadrangles['properties'][index]))

        file.write(struct.pack('1h', triangle_faces_count))
        for index, series in df_triangles.iterrows():
            file.write(struct.pack('1B', df_triangles['properties'][index]))
            file.write(struct.pack('1h', df_triangles['col2'][index]))
            file.write(struct.pack('1B', df_triangles['texture_id_group'][index]))
            file.write(struct.pack('1h', df_triangles['face_flags'][index]))

            file.write(struct.pack('1B', df_triangles['u_a'][index]))
            file.write(struct.pack('1B', df_triangles['v_a'][index]))
            file.write(struct.pack('1B', df_triangles['u_b'][index]))
            file.write(struct.pack('1B', df_triangles['v_b'][index]))
            file.write(struct.pack('1B', df_triangles['u_c'][index]))
            file.write(struct.pack('1B', df_triangles['v_c'][index]))

        return
        file.write(df['signature'][0].tobytes())
        file.write(df['name'][0].encode('utf-8'))
        file.write("\n".encode('utf-8'))
        blanks_count = 31 - len(df['name'][0])
        for i in range(blanks_count):
            file.write("\0".encode('utf-8'))
        file.write(df['first_point_id'][0].tobytes())
        file.write(df['last_point_id'][0].tobytes())
        file.write(df['first_quadrangle_id'][0].tobytes())
        file.write(df['last_quadrangle_id'][0].tobytes())
        file.write(df['first_triangle_id'][0].tobytes())
        file.write(df['last_triangle_id'][0].tobytes())
        file.write(df['collision_type'][0].tobytes())
        file.write(df['reaction_to_impact_by_vehicle'][0].tobytes())
        file.write(df['shadow_type'][0].tobytes())
        file.write(df['various_properties'][0].tobytes())
        for index, series in df_points.iterrows():
            file.write(df_points['x'][index].tobytes())
            file.write(df_points['y'][index].tobytes())
            file.write(df_points['z'][index].tobytes())

        for index, series in df_triangles.iterrows():
            file.write(df_triangles['texture_id_group'][index].tobytes())
            file.write(df_triangles['properties'][index].tobytes())

            file.write(df_triangles['point_a_id'][index].tobytes())
            file.write(df_triangles['point_b_id'][index].tobytes())
            file.write(df_triangles['point_c_id'][index].tobytes())

            file.write(df_triangles['u_a'][index].tobytes())
            file.write(df_triangles['v_a'][index].tobytes())
            file.write(df_triangles['u_b'][index].tobytes())
            file.write(df_triangles['v_b'][index].tobytes())
            file.write(df_triangles['u_c'][index].tobytes())
            file.write(df_triangles['v_c'][index].tobytes())

            file.write(df_triangles['bright_a'][index].tobytes())
            file.write(df_triangles['bright_b'][index].tobytes())
            file.write(df_triangles['bright_c'][index].tobytes())

            file.write(df_triangles['thing_index'][index].tobytes())
            file.write(df_triangles['col2'][index].tobytes())
            file.write(df_triangles['face_flags'][index].tobytes())
            file.write(df_triangles['type'][index].tobytes())
            file.write(df_triangles['id'][index].tobytes())

            # padding
            for i in range(3):
                file.write("\0".encode('utf-8'))

        for index, series in df_quadrangles.iterrows():
            file.write(df_quadrangles['texture_id_group'][index].tobytes())
            file.write(df_quadrangles['properties'][index].tobytes())

            file.write(df_quadrangles['point_a_id'][index].tobytes())
            file.write(df_quadrangles['point_b_id'][index].tobytes())
            file.write(df_quadrangles['point_d_id'][index].tobytes())
            file.write(df_quadrangles['point_c_id'][index].tobytes())

            file.write(df_quadrangles['u_a'][index].tobytes())
            file.write(df_quadrangles['v_a'][index].tobytes())
            file.write(df_quadrangles['u_b'][index].tobytes())
            file.write(df_quadrangles['v_b'][index].tobytes())
            file.write(df_quadrangles['u_d'][index].tobytes())
            file.write(df_quadrangles['v_d'][index].tobytes())
            file.write(df_quadrangles['u_c'][index].tobytes())
            file.write(df_quadrangles['v_c'][index].tobytes())

            file.write(df_quadrangles['bright_a'][index].tobytes())
            file.write(df_quadrangles['bright_b'][index].tobytes())
            file.write(df_quadrangles['bright_d'][index].tobytes())
            file.write(df_quadrangles['bright_c'][index].tobytes())

            file.write(df_quadrangles['thing_index'][index].tobytes())
            file.write(df_quadrangles['col2'][index].tobytes())
            file.write(df_quadrangles['face_flags'][index].tobytes())
            file.write(df_quadrangles['type'][index].tobytes())
            file.write(df_quadrangles['id'][index].tobytes())

            # padding
            for i in range(4):
                file.write("\0".encode('utf-8'))


def app():
    # user defined obj
    [df_points, df_triangles, df_quadrangles] = extract_obj_to_df("res/objs/pziTurret/turret.obj")

    # print(df_triangles)
    create_tex_from_dataframes("output/tex/turret.tex", df_quadrangles, df_triangles)
    print("Tex is Done")
    # adjust_datatypes_in_dataframes(df, df_points, df_triangles, df_quadrangles)
    # points_count = get_points_count(df_points)


if __name__ == '__main__':
    app()
