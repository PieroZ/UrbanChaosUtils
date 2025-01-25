import bpy
import os

# Settings
image_filename = "tex359hi.tga"
texture_image_path = f"C:\\dev\\workspaces\\repo clones\\Clean-UrbanChaos\\MuckyFoot-UrbanChaos\\fallen\\Release\\server\\textures\\shared\\prims\\{image_filename}"
output_folder = "C:\\dev\\workspaces\\repo clones\\Clean-UrbanChaos\\MuckyFoot-UrbanChaos\\fallen\\Release\\server\\textures\\shared\\prims\\output-test"
chunk_size = 64

# Load the texture image
image = bpy.data.images.load(texture_image_path)


# Split the texture into chunks
def split_texture(image, chunk_size, output_folder):
    width, height = image.size
    chunk_count_x = width // chunk_size
    chunk_count_y = height // chunk_size

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    chunk_paths = []

    # Iterate over the chunks and save them
    for x in range(chunk_count_x):
        for y in range(chunk_count_y):
            chunk_name = f"image_filename_{x}_{y}.tga"
            chunk_path = os.path.join(output_folder, chunk_name)
            chunk_image = bpy.data.images.new(chunk_name, width=chunk_size, height=chunk_size)

            # Copy pixel data from the original image to the chunk
            pixels = list(image.pixels)  # Convert to list for slicing
            chunk_pixels = [0.0] * (chunk_size * chunk_size * 4)
            for cx in range(chunk_size):
                for cy in range(chunk_size):
                    src_x = x * chunk_size + cx
                    src_y = y * chunk_size + cy
                    src_index = (src_y * width + src_x) * 4
                    dest_index = (cy * chunk_size + cx) * 4
                    chunk_pixels[dest_index:dest_index + 4] = pixels[src_index:src_index + 4]

            # Assign the chunk's pixel data and save it
            chunk_image.pixels = chunk_pixels
            chunk_image.filepath_raw = chunk_path
            chunk_image.file_format = 'TARGA'
            chunk_image.save()
            bpy.data.images.remove(chunk_image)  # Remove from Blender to save memory
            chunk_paths.append(chunk_path)

    return chunk_paths


# Update UVs and create materials
def update_uvs_and_materials(obj, chunk_size, texture_size, chunk_paths):
    mesh = obj.data
    uv_layer = mesh.uv_layers.active.data

    # Create materials for each chunk
    materials = []
    for path in chunk_paths:
        material_name = os.path.basename(path).split(".")[0]
        mat = bpy.data.materials.new(name=material_name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]

        # Load the corresponding image texture
        tex_image = bpy.data.images.load(path)
        tex_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        tex_node.image = tex_image
        mat.node_tree.links.new(bsdf.inputs["Base Color"], tex_node.outputs["Color"])
        materials.append(mat)

    # Assign materials to the object
    obj.data.materials.clear()
    for mat in materials:
        obj.data.materials.append(mat)

    # Update UVs and assign materials to polygons
    scale_factor = chunk_size / texture_size
    chunk_count_x = texture_size // chunk_size
    for poly in mesh.polygons:
        # Calculate the chunk coordinates for this polygon
        poly_uvs = [uv_layer[loop_index].uv for loop_index in poly.loop_indices]
        avg_uv = sum((uv.x for uv in poly_uvs)) / len(poly_uvs), sum((uv.y for uv in poly_uvs)) / len(poly_uvs)
        chunk_x = int(avg_uv[0] * chunk_count_x)
        chunk_y = int(avg_uv[1] * chunk_count_x)

        # Clamp chunk indices to ensure they are within bounds
        chunk_x = max(0, min(chunk_x, chunk_count_x - 1))
        chunk_y = max(0, min(chunk_y, chunk_count_x - 1))

        # Assign material based on the chunk
        mat_index = chunk_y * chunk_count_x + chunk_x
        poly.material_index = mat_index

        # Adjust UV coordinates for the current chunk
        for loop_index in poly.loop_indices:
            uv = uv_layer[loop_index].uv
            uv.x = (uv.x - chunk_x * scale_factor) / scale_factor
            uv.y = (uv.y - chunk_y * scale_factor) / scale_factor

            # Clamp UV coordinates to [0, 1]
            uv.x = max(0.0, min(uv.x, 1.0))
            uv.y = max(0.0, min(uv.y, 1.0))


# Apply the functions
obj = bpy.context.object  # Assumes the model is the active object
chunk_paths = split_texture(image, chunk_size, output_folder)
update_uvs_and_materials(obj, chunk_size, image.size[0], chunk_paths)
