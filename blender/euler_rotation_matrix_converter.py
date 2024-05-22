import bpy
import mathutils
import json
import os
import math


def extract_translations_rotations():
    translation_dict = {}
    rotation_dict = {}

    # Iterate over all objects in the scene
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            # Extract translation (location) and rotation (rotation_quaternion) for each object
            translation = obj.location
            rotation_quaternion = obj.rotation_quaternion
            rotation_euler = rotation_quaternion.to_euler('XYZ')

            # Store translation and rotation in dictionaries
            translation_dict[obj.name] = translation
            rotation_dict[obj.name] = rotation_euler

            print(f'Rotation Euler angles for {obj.name}: {rotation_euler}')

    return translation_dict, rotation_dict

def quaternion_to_list(quaternion):
    return [quaternion.w, quaternion.x, quaternion.y, quaternion.z]

def matrix_to_euler(matrix):
    # Convert a list of lists to a mathutils.Matrix object
    mat = mathutils.Matrix(matrix)
    # Convert the rotation matrix to Euler angles (XYZ order)
    euler = mat.to_euler('XYZ')
    return euler

def euler_to_degrees(euler):
    # Convert Euler angles from radians to degrees
    return [math.degrees(angle) for angle in euler]

def write_dict_to_json(data_dict, file_path):
    # Convert Vector and Euler objects to lists
    for key, value in data_dict.items():
        if isinstance(value, mathutils.Vector):
            data_dict[key] = [value.x, value.y, value.z]
        elif isinstance(value, mathutils.Euler):
            data_dict[key] = [value.x, value.y, value.z]

    # Write the modified dictionary to a JSON file
    with open(file_path, 'w') as file:
        json.dump(data_dict, file, indent=4)
        
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


def main():
    # Extract translations and rotations
    translation_dict, rotation_dict = extract_translations_rotations()

    # Write translations and rotations to JSON files
    write_dict_to_json(translation_dict, 'translations.json')
    write_dict_to_json(rotation_dict, 'rotations.json')

    print("Translations and rotations extracted and saved to JSON files.")

# Test the conversion function with your provided rotation matrix
if __name__ == '__main__':
    current_directory = os.getcwd()
    print("Current Directory:", current_directory)
    
    # Your provided rotation matrix for testing
#    rotation_matrix = [
#        [0.9980430528375733, 0.009784735812133072, 0.07632093933463796],
#        [-0.01761252446183953, 0.9960861056751468, 0.08610567514677103],
#        [-0.07827788649706457, -0.09001956947162426, 0.9941291585127201]
#    ]
    
    # skull00
    rotation_matrix = [
        [1.0, -0.005870841487279843, 0.023483365949119372],
        [-0.003913894324853229, 0.9726027397260274, 0.23679060665362034],
        [-0.0273972602739726, -0.23874755381604695, 0.9726027397260274]
    ]
    
    euler_angles = matrix_to_euler(rotation_matrix)
    euler_angles_degrees = euler_to_degrees(euler_angles)

    print(f'Converted Euler angles for skull00 (radians): {euler_angles}')
    print(f'Converted Euler angles for skull00 (degrees): {euler_angles_degrees}')
    
    
        
    # Test the function
    x_deg, y_deg, z_deg = -13.7923, 1.5708, -0.2242
    rotation_matrix = degrees_to_matrix(x_deg, y_deg, z_deg)
    print(f"Rotation matrix for Euler angles ({x_deg}, {y_deg}, {z_deg}) degrees:")
    print(rotation_matrix)
    
    
    #main()
