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

def find_shared_edges(faces):
    edge_to_faces = {}
    for face_index, (_, face_vertices, _) in enumerate(faces):
        edges = [(face_vertices[i], face_vertices[(i + 1) % 3]) for i in range(3)]
        for edge in edges:
            sorted_edge = tuple(sorted(edge))
            if sorted_edge not in edge_to_faces:
                edge_to_faces[sorted_edge] = []
            edge_to_faces[sorted_edge].append(face_index)
    return edge_to_faces

def assign_edge_values(faces, edge_to_faces):
    edge_values_list = []

    for face_index, (_, face_vertices, _) in enumerate(faces):
        edge_values = [1, 1, 1]  # Default to 1 (not shared)
        edges = [(face_vertices[i], face_vertices[(i + 1) % 3]) for i in range(3)]
        for i, edge in enumerate(edges):
            sorted_edge = tuple(sorted(edge))
            if len(edge_to_faces[sorted_edge]) > 1:
                edge_values[i] = 0  # Shared edge
        edge_values_list.append(edge_values)

    return edge_values_list

def write_custom_format(file_path, vertices, texture_vertices, faces, materials, edge_values_list, obj_name):
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
            file.write(f"Texture Vertex: ({texture_vertex[0]:10.4f}, {texture_vertex[1]:10.4f})\n")

        for i, face in enumerate(faces):
            material, face_vertices, face_textures = face
            edge_values = edge_values_list[i]
            file.write(
                f"Face: Material {0:2} xyz ({face_vertices[0]:4},{face_vertices[1]:4},{face_vertices[2]:4}) uv ({face_textures[0]:4},{face_textures[1]:4},{face_textures[2]:4}) edge ({edge_values[0]}, {edge_values[1]}, {edge_values[2]}) group 1\n")

def convert_obj_to_custom_format(input_file, output_file, obj_name):
    vertices, texture_vertices, faces, materials = parse_obj(input_file)
    edge_to_faces = find_shared_edges(faces)
    edge_values_list = assign_edge_values(faces, edge_to_faces)
    write_custom_format(output_file, vertices, texture_vertices, faces, materials, edge_values_list, obj_name)

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
    obj_input_dir = "output/frames-per-anim-file/roper/tests/"
    output_file = 'my_roper.sex'

    obj_input_path_list = grab_files_with_extension(obj_input_dir, "*.obj")

    clear_file(output_file)

    for obj in obj_input_path_list:
        obj_input_path = f'{obj_input_dir}{obj}'
        convert_obj_to_custom_format(obj_input_path, output_file, obj[:-4])

if __name__ == '__main__':
    app()
