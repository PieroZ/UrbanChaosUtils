import bpy
import os

output_directory = "C:/dev/workspaces/python/repo/UrbanChaosUtils/output/frames-per-anim-file/roper/tests/"

# Deselect all objects
bpy.ops.object.select_all(action='DESELECT')

# Rotation angles
rotation_x = 90
rotation_y = 180
rotation_z = 180

# Loop through all mesh objects in the scene
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        # Select the object
        obj.select_set(True)
        # Make it the active object
        bpy.context.view_layer.objects.active = obj

        # Store original rotation
        original_rotation = obj.rotation_euler.copy()

        # Apply the rotations
        obj.rotation_euler[0] += rotation_x * (3.14159265359 / 180)  # Convert degrees to radians
        obj.rotation_euler[1] += rotation_y * (3.14159265359 / 180)  # Convert degrees to radians
        obj.rotation_euler[2] += rotation_z * (3.14159265359 / 180)  # Convert degrees to radians

        # Define the output file path
        output_file = os.path.join(output_directory, f"{obj.name}.obj")

        # Export the selected object to OBJ
        bpy.ops.export_scene.obj(
            filepath=output_file,
            use_selection=True,
            use_materials=True
        )

        # Revert to original rotation
        obj.rotation_euler = original_rotation

        # Deselect the object
        obj.select_set(False)

print("Export completed!")