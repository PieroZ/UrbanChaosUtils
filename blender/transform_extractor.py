import bpy
import mathutils
import json
import os

def extract_translations_rotations():
    translation_dict = {}
    rotation_dict = {}

    # Iterate over all objects in the scene
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            # Extract translation (location) and rotation (rotation_quaternion) for each object
            translation = obj.location
            rotation = obj.rotation_quaternion

            # Store translation and rotation in dictionaries
            translation_dict[obj.name] = translation
            rotation_dict[obj.name] = rotation

    return translation_dict, rotation_dict

def quaternion_to_list(quaternion):
    return [quaternion.w, quaternion.x, quaternion.y, quaternion.z]

def write_dict_to_json(data_dict, file_path):
    # Convert Vector and Quaternion objects to lists
    for key, value in data_dict.items():
        if isinstance(value, mathutils.Vector):
            data_dict[key] = [value.x, value.y, value.z]
        elif isinstance(value, mathutils.Quaternion):
            data_dict[key] = quaternion_to_list(value)

    # Write the modified dictionary to a JSON file
    with open(file_path, 'w') as file:
        json.dump(data_dict, file, indent=4)

def main():
    # Extract translations and rotations
    translation_dict, rotation_dict = extract_translations_rotations()

    # Write translations and rotations to JSON files
    write_dict_to_json(translation_dict, 'translations.json')
    write_dict_to_json(rotation_dict, 'rotations.json')

    print("Translations and rotations extracted and saved to JSON files.")

if __name__ == '__main__':
    current_directory = os.getcwd()
    print("Current Directory:", current_directory)
    main()