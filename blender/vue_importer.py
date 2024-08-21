import bpy
import os
import math
import mathutils
import json
import glob
import re


def process_multiple_kfs(kfs_id_list, character):
    #    do_import(454, 'darci1')
    vue_filepath = 'C:/dev/workspaces/repo clones/Clean-UrbanChaos/MuckyFoot-UrbanChaos/fallen/Release/data/Troper.vue'

    #    extract_current_pose_to_vue(414)
    with open(vue_filepath, 'r') as vue_file:
        vue_content = vue_file.read()

    new_frame_id = extract_frame_number(vue_content) + 1

    for kfs_id in kfs_id_list:
        do_import(kfs_id, character)
        extract_current_pose_to_vue(new_frame_id, vue_filepath)
        new_frame_id = new_frame_id + 1


def list_obj_files(directory):
    # Use glob to find all .obj files in the given directory
    obj_files = glob.glob(os.path.join(directory, '*.obj'))
    return obj_files


def import_obj(obj_path):
    file_loc = obj_path
    # Extract the name of the object from the file name
    obj_name = os.path.splitext(os.path.basename(file_loc))[0]

    # Check if an object with the same name already exists
    if obj_name in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[obj_name], do_unlink=True)

    # Import the object
    bpy.ops.import_scene.obj(filepath=file_loc)

    # Get the newly imported object
    imported_objects = [obj for obj in bpy.context.selected_objects if obj.name.startswith(obj_name)]
    if not imported_objects:
        raise RuntimeError(f"Failed to import object: {obj_name}")
    imported_object = imported_objects[0]

    # Rename the imported object
    imported_object.name = obj_name
    return imported_object


def get_transformation_matrix(obj):
    return obj.matrix_world.copy()  # Ensure a copy of the matrix is returned


def apply_transformations(obj):
    # Example transformations (customize these transformations as needed)
    print(f"Original location: {obj.location}")
    print(f"Original rotation: {obj.rotation_euler}")

    # Apply a 45-degree rotation around the Z axis and a translation
    rotation = mathutils.Euler((0, 0, math.radians(45)), 'XYZ')
    translation = mathutils.Vector((200.0, 3.0, 4.0))

    # Apply the transformations
    obj.matrix_world = obj.matrix_world @ mathutils.Matrix.Translation(translation) @ rotation.to_matrix().to_4x4()


def print_coordinates(obj):
    if obj is None:
        print("No object selected.")
    else:
        print(f"Object Name: {obj.name}")

        # Print Object Coordinates (Local Space)
        print("\nObject Coordinates (Local Space):")
        for vert in obj.data.vertices:
            print(f"Vertex {vert.index}: {vert.co}")

        # Print World Coordinates
        print("\nWorld Coordinates:")
        for vert in obj.data.vertices:
            world_coord = obj.matrix_world @ vert.co
            print(f"Vertex {vert.index}: {world_coord}")


def euler_to_degrees(euler):
    # Convert Euler angles from radians to degrees
    return [math.degrees(angle) for angle in euler]


def read_json_to_dict(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data


def degrees_to_matrix(x_deg, y_deg, z_deg):
    # Convert degrees to radians
    x_rad = math.radians(x_deg)
    y_rad = math.radians(y_deg)
    z_rad = math.radians(z_deg)

    # Create an Euler object from the radians
    euler = mathutils.Euler((x_rad, y_rad, z_rad), 'XYZ')

    # Convert the Euler object to a 3x3 rotation matrix
    rotation_matrix = euler.to_matrix()

    return rotation_matrix


def rotate_degrees_x(degrees):
    # Create a rotation matrix for 90 degrees around the X axis
    rotation_angle = math.radians(degrees)
    rotation_matrix = mathutils.Matrix.Rotation(rotation_angle, 4, 'X')
    return rotation_matrix


def apply_rotation_to_object(obj, rotation_matrix):
    # Apply the rotation matrix to the object's matrix_world
    obj.matrix_world = rotation_matrix @ obj.matrix_world


def apply_transformations_from_file(file_no, obj, mesh_name, character_name):
    rotation_json_file_path = f'C:/dev/workspaces/python/repo/UrbanChaosUtils/output/body-part-offsets/{character_name}/rotation_matrix_frame {file_no}.json'
    # Read the JSON file and store it in a dictionary
    rotation_dict = read_json_to_dict(rotation_json_file_path)
    translation_json_file_path = f'C:/dev/workspaces/python/repo/UrbanChaosUtils/output/body-part-offsets/{character_name}/frame {file_no}.txt'
    transform_dict = read_json_to_dict(translation_json_file_path)

    for key, value in rotation_dict.items():
        if mesh_name in key:
            rotation_matrix = mathutils.Matrix((
                value[0][0],
                value[0][1],
                value[0][2]
            ))

            # Get the mesh object
            obj = bpy.data.objects[key]

            # Get the translation vector
            translation_vector = mathutils.Vector((
                transform_dict[key][0],
                transform_dict[key][1],
                transform_dict[key][2]
            ))

            # Construct the transformation matrix
            transformation_matrix = mathutils.Matrix.Translation(translation_vector) @ rotation_matrix.to_4x4()

            # Apply the additional 90-degree rotation around the X axis
            rotation_90_x = rotate_degrees_x(90)
            transformation_matrix = rotation_90_x @ transformation_matrix

            # Apply the transformation to the object's matrix_world
            obj.matrix_world = transformation_matrix

            print(file_no)
            obj.keyframe_insert(data_path='location', frame=file_no)
            obj.keyframe_insert(data_path='rotation_euler', frame=file_no)


def calculate_relative_transformation(initial_matrix, current_matrix):
    # Calculate the relative transformation matrix
    relative_matrix = current_matrix @ initial_matrix.inverted()
    return relative_matrix


def vue_translation_vector(x, y, z):
    #    print(f'vue_x arg = {x}')
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


def extract_frame_number(vue_content):
    # Define the regular expression pattern to match the frame number
    pattern = r'frame (\d+)'

    # Search for the pattern in the content
    match = re.findall(pattern, vue_content)

    # Convert the matched frame numbers to integers and return the highest one
    if match:
        frame_numbers = list(map(int, match))
        return max(frame_numbers)
    else:
        return None


def extract_current_pose_to_vue(frame_no, output_filepath):
    print(f'')
    print(f'')
    print(f'')
    # Iterate over all objects in the scene

    with open(output_filepath, 'a') as output_vue_file:
        output_vue_file.write(f'\nframe {frame_no}\n')
        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                rotation_90_x = rotate_degrees_x(-90)
                apply_rotation_to_object(obj, rotation_90_x)
                #            transformation_matrix = rotation_90_x @ transformation_matrix

                #            # Apply the transformation to the object's matrix_world
                #            obj.matrix_world = transformation_matrix

                vue_x, vue_y, vue_z = vue_translation_vector(obj.location[0], obj.location[1], obj.location[2])
                euler_angles_degrees = euler_to_degrees(obj.rotation_euler)

                rotation_matrix = degrees_to_matrix(euler_angles_degrees[0], euler_angles_degrees[1],
                                                    euler_angles_degrees[2])
                ordered_vue_matrix = order_vue_angles_2(rotation_matrix)
                vue_entry = f'transform "{obj.name}" {ordered_vue_matrix[0]:.3f} {ordered_vue_matrix[1]:.3f} {ordered_vue_matrix[2]:.3f} {ordered_vue_matrix[3]:.3f} {ordered_vue_matrix[4]:.3f} {ordered_vue_matrix[5]:.3f} {ordered_vue_matrix[6]:.3f} {ordered_vue_matrix[7]:.3f} {ordered_vue_matrix[8]:.3f} {vue_x:.3f} {vue_z:.3f} {vue_y:.3f}\n'

                # print(vue_entry)
                output_vue_file.write(vue_entry)

                rotation_90_x = rotate_degrees_x(90)
                apply_rotation_to_object(obj, rotation_90_x)


def do_import(keyframes_list, character_name, model_id):
    # Example usage
    base_obj_directory = f'C:/dev/workspaces/python/repo/UrbanChaosUtils/output/all-obj/{character_name}/{model_id}/'

    print(base_obj_directory)

    # Check if mesh should be ignored
    ignored_list = ["rhand01", "rhand03", "rhand04", "rhand06", "rhand07", "lhand01", "lhand02"]

    obj_list = list_obj_files(base_obj_directory)  # List of objects to import, for demonstration purposes
    #    obj_list = ['torso00.obj']  # List of objects to import, for demonstration purposes

    # Manually clear all objects in the scene before importing
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    for obj_file in obj_list:
        ignore = False
        for ignored_element in ignored_list:
            if ignored_element in obj_file:
                ignore = True

        if not ignore:
            obj_path = os.path.join(base_obj_directory, obj_file)
            imported_object = import_obj(obj_path)

            # Store the initial transformation matrix
            initial_matrix = get_transformation_matrix(imported_object)

            for keyframe_no in keyframes_list:
                # Apply transformations
                apply_transformations_from_file(keyframe_no, imported_object, imported_object.name, character_name)
                #        apply_transformations(imported_object)

                # Get the current transformation matrix
                current_matrix = get_transformation_matrix(imported_object)

                # Calculate the relative transformation
                relative_matrix = calculate_relative_transformation(initial_matrix, current_matrix)

                # Extract translation and rotation from the relative matrix
                translation = relative_matrix.to_translation()
                rotation = relative_matrix.to_euler('XYZ')

                # Convert rotation angles from radians to degrees
                rotation_degrees = [math.degrees(angle) for angle in rotation]


#            print(f"Initial matrix: {initial_matrix}")
#            print(f"Current matrix: {current_matrix}")
#            print(f"Relative matrix: {relative_matrix}")
#            print(f"Relative translation: {translation}")
#            print(f"Relative rotation (in degrees): {rotation_degrees}")
#        print_coordinates(imported_object)
if __name__ == '__main__':
    keyframes_list = list(range(19))
    model_id = 0
    model_name = 'van'
    do_import(keyframes_list, model_name, model_id)

#    extract_current_pose_to_vue(414)
#    kfs_ids = [131, 132, 133, 134, 135, 136, 137]
#    character = 'darci1'
#    process_multiple_kfs(kfs_ids,character)