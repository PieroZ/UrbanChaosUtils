import bpy
import os
import math
import mathutils


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
    translation = mathutils.Vector((2.0, 3.0, 4.0))

    # Apply the transformations
    obj.matrix_world = obj.matrix_world @ mathutils.Matrix.Translation(translation) @ rotation.to_matrix().to_4x4()

    print(f"Transformed location: {obj.location}")
    print(f"Transformed rotation: {obj.rotation_euler}")


def calculate_relative_transformation(initial_matrix, current_matrix):
    # Calculate the relative transformation matrix
    relative_matrix = current_matrix @ initial_matrix.inverted()
    return relative_matrix


if __name__ == '__main__':
    # Example usage
    base_obj_directory = 'C:/dev/workspaces/python/urban chaos research/output/all-obj/roper/0/'
    obj_list = ['torso00.obj']  # List of objects to import, for demonstration purposes

    # Manually clear all objects in the scene before importing
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    for obj_file in obj_list:
        obj_path = os.path.join(base_obj_directory, obj_file)
        imported_object = import_obj(obj_path)

        # Store the initial transformation matrix
        initial_matrix = get_transformation_matrix(imported_object)

        # Apply transformations
        apply_transformations(imported_object)

        # Get the current transformation matrix
        current_matrix = get_transformation_matrix(imported_object)

        # Calculate the relative transformation
        relative_matrix = calculate_relative_transformation(initial_matrix, current_matrix)

        # Extract translation and rotation from the relative matrix
        translation = relative_matrix.to_translation()
        rotation = relative_matrix.to_euler('XYZ')

        # Convert rotation angles from radians to degrees
        rotation_degrees = [math.degrees(angle) for angle in rotation]

        print(f"Initial matrix: {initial_matrix}")
        print(f"Current matrix: {current_matrix}")
        print(f"Relative matrix: {relative_matrix}")
        print(f"Relative translation: {translation}")
        print(f"Relative rotation (in degrees): {rotation_degrees}")
