import bpy
import os


# Set the directory containing your .obj files
input_dir = "C:/dev/workspaces/python/repo/UrbanChaosUtils/output/objs/Prototype"
output_dir = "C:/dev/workspaces/repo clones/web-3dmodel-threejs/models/files"

# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Iterate over all .obj files in the directory
for filename in os.listdir(input_dir):
    if filename.endswith(".obj"):
        obj_file = os.path.join(input_dir, filename)
        base_name = os.path.splitext(filename)[0]  # Get the file name without extension

        # Create a new directory for the .gltf file
        output_subdir = os.path.join(output_dir, base_name)
        if not os.path.exists(output_subdir):
            os.makedirs(output_subdir)

        # Import the .obj file into Blender
        bpy.ops.import_scene.obj(filepath=obj_file)

        # Define the output .gltf file path
        gltf_file = os.path.join(output_subdir, "scene.gltf")

        # Export the scene to .gltf
        bpy.ops.export_scene.gltf(filepath=gltf_file, export_format='GLTF_SEPARATE')

        # Clean up the scene (remove all objects) for the next import
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)

print("Conversion complete!")
