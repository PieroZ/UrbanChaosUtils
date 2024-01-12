from nprim_visualizer import *
from obj_to_dataframe import *
import time
import shutil


def tictoc(func):
    def wrapper():
        t1 = time.time()
        func()
        t2 = time.time()-t1
        print(f' {func.__name__} ran in {t2} seconds')
    return wrapper


class NprimModifier:
    def __init__(self, new_first_global_point_id):
        self.new_first_global_point_id = new_first_global_point_id
        self.new_first_quad_id = 0
        self.new_first_triangle_id = 0
        self.nprim_output_path = ''
        self.nprim_output_filename = ''


def user_input(nprim_modifier):
    nprim_modifier.new_first_global_point_id = 32000
    nprim_modifier.new_first_quad_id = 26000
    nprim_modifier.new_first_triangle_id = 25000

    nprim_modifier.nprim_output_filename = 'nprim200.prm'
    nprim_modifier.nprim_output_path = 'output/modified_nprims/' + nprim_modifier.nprim_output_filename
    # nprim_modifier.nprim_output_path = 'output/modified_nprims/test_cube.prm'


def adjust_datatypes_in_dataframes(df, df_points, df_triangles, df_quadrangles):
    df['signature'] = df['signature'].astype('int16')
    df['first_point_id'] = df['first_point_id'].astype('int16')
    df['last_point_id'] = df['last_point_id'].astype('int16')
    df['first_quadrangle_id'] = df['first_quadrangle_id'].astype('int16')
    df['last_quadrangle_id'] = df['last_quadrangle_id'].astype('int16')
    df['first_triangle_id'] = df['first_triangle_id'].astype('int16')
    df['last_triangle_id'] = df['last_triangle_id'].astype('int16')

    # df['collision_type'] = df['collision_type'].astype('int8')
    df['collision_type'] = 1
    df['collision_type'] = df['collision_type'].astype('int8')
    df['reaction_to_impact_by_vehicle'] = df['reaction_to_impact_by_vehicle'].astype('int8')
    df['shadow_type'] = df['shadow_type'].astype('int8')
    df['various_properties'] = df['various_properties'].astype('int8')

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


def adjust_name_to_32bytes(df):
    name_bytes_count = len(df['name'][0])
    blanks_count = 31 - name_bytes_count

    df['name'] = df['name'] + "\0A"

    for i in range(blanks_count):
        df['name'] += "\0"


def get_points_count(df_points):
    count = len(df_points)

    return count


def normalize_df_ids(df, df_quadrangles, df_triangles, first_point_id):
    if not df_quadrangles.empty:
        df_quadrangles['point_a_id'] -= first_point_id
        df_quadrangles['point_b_id'] -= first_point_id
        df_quadrangles['point_c_id'] -= first_point_id
        df_quadrangles['point_d_id'] -= first_point_id

    if not df_triangles.empty:
        df_triangles['point_a_id'] -= first_point_id
        df_triangles['point_b_id'] -= first_point_id
        df_triangles['point_c_id'] -= first_point_id

    if not df.empty:
        df['first_point_id'] -= first_point_id
        df['last_point_id'] -= first_point_id


def create_nprim_from_dataframes(output_nprim_filename, df, df_points, df_quadrangles, df_triangles):
    with open(output_nprim_filename, "wb+") as file:
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


def add_user_defined_global_id(df, df_quadrangles, df_triangles, new_first_global_point_id,
                               new_first_quad_id, new_first_triangle_id, points_count, triangle_count, quadrangle_count):
    if not df_quadrangles.empty:
        df_quadrangles['point_a_id'] = df_quadrangles['point_a_id'] + new_first_global_point_id - 1
        df_quadrangles['point_b_id'] = df_quadrangles['point_b_id'] + new_first_global_point_id - 1
        df_quadrangles['point_c_id'] = df_quadrangles['point_c_id'] + new_first_global_point_id - 1
        df_quadrangles['point_d_id'] = df_quadrangles['point_d_id'] + new_first_global_point_id - 1

    if not df_triangles.empty:
        df_triangles['point_a_id'] = df_triangles['point_a_id'] + new_first_global_point_id - 1
        df_triangles['point_b_id'] = df_triangles['point_b_id'] + new_first_global_point_id - 1
        df_triangles['point_c_id'] = df_triangles['point_c_id'] + new_first_global_point_id - 1

    if not df.empty:
        df['first_point_id'] = new_first_global_point_id
        df['last_point_id'] = new_first_global_point_id + points_count

        df['first_quadrangle_id'] = new_first_quad_id
        df['last_quadrangle_id'] = new_first_quad_id + quadrangle_count

        df['first_triangle_id'] = new_first_triangle_id
        df['last_triangle_id'] = new_first_triangle_id + triangle_count


def faces_count(df_faces):
    return len(df_faces)


@tictoc
def app():
    df = None
    nprim_modifier = NprimModifier(0)
    user_input(nprim_modifier)

    sc_game_dir = 'C:/dev/workspaces/repo clones/Clean-UrbanChaos/MuckyFoot-UrbanChaos/fallen/Release/server/prims/'

    dst_file = sc_game_dir + nprim_modifier.nprim_output_filename

    # nprim = "res/nprims/nprim216.prm"
    # nprim = "res/nprims/nprim150.prm"  # police car
    nprim = "res/nprims/" + nprim_modifier.nprim_output_filename  # knife
    [df, df_points, df_quadrangles, df_triangles] = fill_dataframe_with_nprim_data(nprim, df)

    # user defined obj
    [df_points, df_triangles, df_quadrangles] = extract_obj_to_df("res/objs/baby_yoda.obj")

    triangle_faces_count = faces_count(df_triangles)
    quadrangle_faces_count = faces_count(df_quadrangles)

    adjust_datatypes_in_dataframes(df, df_points, df_triangles, df_quadrangles)
    # adjust_name_to_32bytes(df)
    points_count = get_points_count(df_points)

    # This seems redundant now
    # normalize_df_ids(df, df_quadrangles, df_triangles, df['first_point_id'][0])

    add_user_defined_global_id(df, df_quadrangles, df_triangles, nprim_modifier.new_first_global_point_id,
                               nprim_modifier.new_first_triangle_id, nprim_modifier.new_first_quad_id, points_count,
                               triangle_faces_count, quadrangle_faces_count)

    adjust_datatypes_in_dataframes(df, df_points, df_triangles, df_quadrangles)

    create_nprim_from_dataframes(nprim_modifier.nprim_output_path, df, df_points, df_quadrangles, df_triangles)

    # for i, filename in enumerate(glob.iglob(f'{sc_game_dir}/nprim*.prm')):
    #     shutil.copyfile(nprim_modifier.nprim_output_path, filename)
    #     if i > 79:
    #         break

    shutil.copyfile(nprim_modifier.nprim_output_path, dst_file)


if __name__ == '__main__':
    app()
