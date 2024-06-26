import bpy
import mathutils
import json
import os
import glob
import time

def list_obj_files(directory):
    # Use glob to find all .obj files in the given directory
    obj_files = glob.glob(os.path.join(directory, '*.obj'))
    return obj_files

def read_json_to_dict(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data

def clear_scene():
    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Select only mesh objects in the current scene
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            obj.select_set(True)

    # Delete all selected objects
    bpy.ops.object.delete()

    print("All mesh objects have been removed from the scene.")

def import_obj(obj_path):
    file_loc = obj_path
    # Extract the name of the object from the file name
    obj_name = os.path.splitext(os.path.basename(file_loc))[0]
    
    # Check if an object with the same name already exists
    if obj_name in bpy.data.objects:
        bpy.data.objects[obj_name].select_set(True)
        bpy.ops.object.delete()

    # Import the object
    bpy.ops.import_scene.obj(filepath=file_loc)
    
    # Rename the imported object
    imported_object = bpy.context.selected_objects[0]
    imported_object.name = obj_name
    
    print('Imported name: ', imported_object.name)

def app(file_no):
    base_obj_directory = 'C:/dev/workspaces/python/urban chaos research/output/all-obj/roper/0/'
    obj_list = list_obj_files(base_obj_directory)
    clear_scene()
    for obj in obj_list:
        import_obj(obj)
        
    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')
    
    print(f'app called with = {file_no}')
    # Path to your JSON file
    rotation_json_file_path = f'C:/dev/workspaces/python/urban chaos research/output/body-part-offsets/roper/rotation_matrix_frame {file_no}.json'

    # Read the JSON file and store it in a dictionary
    rotation_dict = read_json_to_dict(rotation_json_file_path)

    # Print the dictionary to verify
    print(rotation_dict)
    
    translation_json_file_path = f'C:/dev/workspaces/python/urban chaos research/output/body-part-offsets/roper/frame {file_no}.txt'
    # Read the text file and store it in a dictionary
    transform_dict = read_json_to_dict(translation_json_file_path)

    for key, value in rotation_dict.items():
        print(key)
        print(value[0][1])
        matrix = mathutils.Matrix((
            value[0][0],
            value[0][1],
            value[0][2]
        ))

        # Check if the object exists
        if key in bpy.data.objects:
            # Get the mesh object
            obj = bpy.data.objects[key]
            
            # Select the object and set it as the active object
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)

            # Make sure we are in object mode to access and modify the mesh data
            bpy.ops.object.mode_set(mode='OBJECT')

            # Get the mesh data
            mesh = obj.data

            # Apply the matrix transformation to each vertex
            for vertex in mesh.vertices:
                original_coord = vertex.co
                new_coord = matrix @ original_coord
                translation_vector = mathutils.Vector((
                    transform_dict[key][0],
                    transform_dict[key][1],
                    transform_dict[key][2]
                ))
                print(translation_vector)
                newer_coord = new_coord + translation_vector
                vertex.co = newer_coord
            
            obj.select_set(False)
        else:
            print(f"Object {key} not found in the scene.")

def update_scene():
    global current_frame
    print(current_frame)
    app(current_frame)
    current_frame += 1
    
    if current_frame > 2:
        return None  # Stops the timer
    return 0.5  # Schedules the next update in 2 seconds

if __name__ == '__main__':
    
    
    # Initialize the global current frame variable
    current_frame = 0
      # Start the timer to update the scene
    bpy.app.timers.register(update_scene)
    print('yellow')