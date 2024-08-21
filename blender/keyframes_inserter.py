import bpy
import mathutils
import json
import os
import glob
import math


def list_obj_files(directory):
    obj_files = glob.glob(os.path.join(directory, '*.obj'))
    return obj_files


def read_json_to_dict(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data


def clear_scene():
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            obj.select_set(True)
    bpy.ops.object.delete()


def import_obj(obj_path):
    file_loc = obj_path
    obj_name = os.path.splitext(os.path.basename(file_loc))[0]
    if obj_name in bpy.data.objects:
        bpy.data.objects[obj_name].select_set(True)
        bpy.ops.object.delete()

    ignored_list = ["rhand01", "rhand03", "rhand04", "rhand06", "rhand07", "lhand01", "lhand02"]

    if obj_name not in ignored_list:
        bpy.ops.import_scene.obj(filepath=file_loc)
        imported_object = bpy.context.selected_objects[0]
        imported_object.name = obj_name


def euler_to_degrees(euler):
    return [math.degrees(angle) for angle in euler]


def degrees_to_matrix(x_deg, y_deg, z_deg):
    x_rad = math.radians(x_deg)
    y_rad = math.radians(y_deg)
    z_rad = math.radians(z_deg)
    euler = mathutils.Euler((x_rad, y_rad, z_rad), 'XYZ')
    rotation_matrix = euler.to_matrix()
    return rotation_matrix


def vue_translation_vector(x, y, z):
    offset_x = x - 1
    vue_x = (offset_x * 100) / 256
    offset_y = y - 2
    vue_y = (offset_y * 100) / 256
    offset_z = z + 136
    vue_z = (offset_z * 100) / 256
    return [vue_x, vue_y, vue_z]


def order_vue_angles(angles):
    return [angles[0][0][0], angles[0][2][0], angles[0][1][0], angles[0][0][2], angles[0][2][2], angles[0][1][2],
            angles[0][0][1], angles[0][2][1], angles[0][1][1]]


def order_vue_angles_2(rotation_matrix):
    return [rotation_matrix[0][0], rotation_matrix[2][0], rotation_matrix[1][0], rotation_matrix[0][2],
            rotation_matrix[2][2], rotation_matrix[1][2], rotation_matrix[0][1], rotation_matrix[2][1],
            rotation_matrix[1][1]]


def apply_transformations(frame_no, rotation_dict, transform_dict):
    for key, value in rotation_dict.items():
        matrix = mathutils.Matrix((
            value[0][0],
            value[0][1],
            value[0][2]
        ))

        if key in bpy.data.objects:
            obj = bpy.data.objects[key]
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            bpy.ops.object.mode_set(mode='OBJECT')

            obj.rotation_euler = matrix.to_euler('XYZ')
            translation_vector = mathutils.Vector((
                transform_dict[key][0],
                transform_dict[key][1],
                transform_dict[key][2]
            ))
            obj.location = translation_vector

            obj.keyframe_insert(data_path='location', frame=frame_no)
            obj.keyframe_insert(data_path='rotation_euler', frame=frame_no)
            obj.select_set(False)
        else:
            print(f"Object {key} not found in the scene.")


def app(frame_nos):
    base_obj_directory = 'C:/dev/workspaces/python/urban chaos research/output/all-obj/roper/0/'
    obj_list = list_obj_files(base_obj_directory)
    clear_scene()
    for obj in obj_list:
        import_obj(obj)

    bpy.ops.object.select_all(action='DESELECT')

    for frame_no in frame_nos:
        print(f'Processing frame {frame_no}')
        rotation_json_file_path = f'C:/dev/workspaces/python/urban chaos research/output/body-part-offsets/roper/rotation_matrix_frame {frame_no}.json'
        translation_json_file_path = f'C:/dev/workspaces/python/urban chaos research/output/body-part-offsets/roper/frame {frame_no}.txt'

        rotation_dict = read_json_to_dict(rotation_json_file_path)
        transform_dict = read_json_to_dict(translation_json_file_path)

        apply_transformations(frame_no, rotation_dict, transform_dict)


if __name__ == '__main__':
    frame_nos = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]  # Specify the frames to load
    frame_nos = list(range(626))  # Specify the frames to load
    app(frame_nos)
    print('Animation created!')
