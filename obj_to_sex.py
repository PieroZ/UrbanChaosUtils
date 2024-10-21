import os.path
import glob


def parse_obj(file_path):
    vertices = []
    texture_vertices = []
    faces = []
    materials = []

    current_material = None
    material_index = 0

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('v '):
                vertices.append(tuple(map(float, line.split()[1:])))
            elif line.startswith('vt '):
                texture_vertices.append(tuple(map(float, line.split()[1:])))
            elif line.startswith('usemtl '):
                material_name = line.split()[1]
                if material_name not in materials:
                    materials.append(material_name)
                current_material = materials.index(material_name) + 1
            elif line.startswith('f '):
                face_elements = line.split()[1:]
                face_vertices = []
                face_textures = []
                for element in face_elements:
                    v, t = map(int, element.split('/')[:2])
                    face_vertices.append(v - 1)
                    face_textures.append(t - 1)
                faces.append((current_material, face_vertices, face_textures))

    return vertices, texture_vertices, faces, materials


def write_custom_format(file_path, vertices, texture_vertices, faces, materials, obj_name):
    with open(file_path, 'a') as file:
        file.write("# ============================================================\n")
        file.write("#\n")
        file.write(f"# Triangle mesh     : {obj_name}\n")
        file.write(f"#     Num faces     : {len(faces)}\n")
        file.write(f"#     Num points    : {len(vertices)}\n")
        file.write(f"#     Num materials : {len(materials)}\n")
        file.write("#\n")
        file.write("# ============================================================\n")
        file.write(f"Triangle mesh: {obj_name}\n")
        file.write("Pivot: (   -0.6849,   52.7643,   41.1971)\n")
        file.write("Matrix: (1.0000, 0.0000, 0.0000, 0.0000, 1.0000, 0.0000, 0.0000, 0.0000, 1.0000)\n")

        for material in materials:
            file.write(
                f"Material: DiffuseRGB (0.5000,0.5000,0.5000), shininess 0.25, shinstr 0.05, Single sided, Filtered alpha, filename {material}.tga\n")

        for i, vertex in enumerate(vertices):
            file.write(f"Vertex: ({vertex[0]:10.4f}, {vertex[1]:10.4f}, {vertex[2]:10.4f})\n")

        for i, texture_vertex in enumerate(texture_vertices):
            file.write(f"Texture Vertex: ({texture_vertex[0]:10.4f}, {1+texture_vertex[1]:10.4f})\n")

        for face in faces:
            material, face_vertices, face_textures = face
            file.write(
                # f"Face: Material {material:2} xyz ({face_vertices[0]:4},{face_vertices[1]:4},{face_vertices[2]:4}) uv ({face_textures[0]:4},{face_textures[1]:4},{face_textures[2]:4}) edge (1, 1, 1) group 1\n")
                f"Face: Material 0 xyz ({face_vertices[0]:4},{face_vertices[1]:4},{face_vertices[2]:4}) uv ({face_textures[0]:4},{face_textures[1]:4},{face_textures[2]:4}) edge (1, 1, 1) group 1\n")
                # f"Face: Material 0 xyz ({face_vertices[1]:4},{face_vertices[2]:4},{face_vertices[0]:4}) uv ({face_textures[1]:4},{face_textures[2]:4},{face_textures[0]:4}) edge (1, 1, 1) group 1\n")


def convert_obj_to_custom_format(input_file, output_file, obj_name):
    vertices, texture_vertices, faces, materials = parse_obj(input_file)
    write_custom_format(output_file, vertices, texture_vertices, faces, materials, obj_name)


def clear_file(file):
    if os.path.exists(file):
        raw = open(file, "r+")
        raw.seek(0)
        raw.truncate()


def grab_files_with_extension(directory, ext):
    all_files_list = []
    for filename in glob.iglob(f'{directory}{ext}'):
        all_files_list.append(os.path.basename(filename))

    return all_files_list


def app():
    obj_input_dir = "res/objs/turret/"
    # obj_input_dir = "output/frames-per-anim-file/roper/tests/"
    # obj_input_dir = "res/objs/handmade/1/"
    output_file = 'res/sex/turret.sex'

    # obj_input_path = "output/frames-per-anim-file/RETAIL_DARCI1/1/pelvis00.obj"

    obj_input_path_list = grab_files_with_extension(obj_input_dir, "*.obj")
    # print(obj_input_path_list)

    clear_file(output_file)

    for obj in obj_input_path_list:
        obj_input_path = f'{obj_input_dir}{obj}'
        convert_obj_to_custom_format(obj_input_path, output_file, obj[:-4])

    print('Sex is Done')


if __name__ == '__main__':
    app()

