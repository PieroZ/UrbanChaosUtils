import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtOpenGL import QGLWidget
from PyQt5.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import os


class ModelViewer(QGLWidget):
    def __init__(self, parent=None):
        super(ModelViewer, self).__init__(parent)
        self.vertices = []
        self.faces = []
        self.tex_coords = []  # Texture coordinates
        self.textures = []    # List of texture IDs
        self.current_texture = None
        self.camera_distance = 5.0
        self.rotation = [0, 0]
        self.pan = [0, 0]
        self.last_mouse_pos = None

    def load_model(self, obj_file):
        self.vertices = []
        self.faces = []
        self.tex_coords = []
        self.textures = []
        self.current_texture = None

        mtl_file = None

        # Read the .obj file
        with open(obj_file, 'r') as f:
            for line in f:
                if line.startswith('v '):  # Vertex definition
                    parts = line.split()
                    self.vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
                elif line.startswith('vt '):  # Texture coordinate definition
                    parts = line.split()
                    self.tex_coords.append([float(parts[1]), float(parts[2])])
                elif line.startswith('f '):  # Face definition
                    parts = line.split()
                    face = []
                    for p in parts[1:]:
                        vals = p.split('/')
                        face.append((int(vals[0]) - 1, int(vals[1]) - 1 if len(vals) > 1 and vals[1] else None))
                    self.faces.append(face)
                elif line.startswith('mtllib '):  # Material file reference
                    mtl_file = line.split()[1].strip()

        # Load the material file if it exists
        if mtl_file:
            self.load_materials(mtl_file, obj_file)

        self.updateGL()

    def load_materials(self, mtl_file, obj_file):
        """ Load materials (including textures) from the .mtl file. """
        obj_dir = os.path.dirname(obj_file)  # Get the directory of the .obj file
        mtl_path = os.path.join(obj_dir, mtl_file)

        if not os.path.exists(mtl_path):
            print(f"Material file not found: {mtl_path}")
            return

        with open(mtl_path, 'r') as f:
            for line in f:
                if line.startswith('map_Kd '):  # Diffuse texture map
                    texture_file = ' '.join(line.split()[1:]).strip()

                    # Check if texture_file is an absolute path
                    if os.path.isabs(texture_file):
                        texture_path = texture_file  # Use the absolute path directly
                    else:
                        texture_path = os.path.join(obj_dir, texture_file)  # Prepend obj_dir if relative

                    # Load the texture
                    self.current_texture = self.load_texture(texture_path)

    def load_texture(self, texture_path):
        """ Load texture image using Pillow and bind it to OpenGL. """
        try:
            img = Image.open(texture_path)
            img = img.convert('RGB')  # Convert image to RGB if it has an alpha channel
            img_data = np.array(list(img.getdata()), np.uint8)
            texture_id = glGenTextures(1)

            glBindTexture(GL_TEXTURE_2D, texture_id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

            return texture_id
        except Exception as e:
            print(f"Failed to load texture: {texture_path}, Error: {e}")
            return None

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_TEXTURE_2D)  # Enable 2D textures

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / h, 1, 100)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Apply camera transformations
        glTranslatef(self.pan[0], self.pan[1], -self.camera_distance)
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)

        # Bind the current texture if available
        if self.current_texture:
            glBindTexture(GL_TEXTURE_2D, self.current_texture)

        # Render the model with texture mapping
        glBegin(GL_TRIANGLES)
        for face in self.faces:
            for vertex_idx, tex_idx in face:
                if tex_idx is not None:
                    glTexCoord2fv(self.tex_coords[tex_idx])  # Apply texture coordinates
                glVertex3fv(self.vertices[vertex_idx])  # Apply vertex
        glEnd()

    def mousePressEvent(self, event):
        self.last_mouse_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self.last_mouse_pos is None:
            return

        dx = event.x() - self.last_mouse_pos.x()
        dy = event.y() - self.last_mouse_pos.y()

        # Left button for rotation
        if event.buttons() & Qt.LeftButton:
            self.rotation[0] += dy / 2.0
            self.rotation[1] += dx / 2.0

        # Right button for panning
        elif event.buttons() & Qt.RightButton:
            self.pan[0] += dx / 100.0
            self.pan[1] -= dy / 100.0

        self.last_mouse_pos = event.pos()
        self.updateGL()

    def wheelEvent(self, event):
        # Zoom in/out
        self.camera_distance -= event.angleDelta().y() / 120.0
        if self.camera_distance < 1.0:
            self.camera_distance = 1.0  # Set a minimum zoom level
        self.updateGL()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.viewer = ModelViewer(self)
        self.setCentralWidget(self.viewer)
        self.setWindowTitle("3D Model Viewer with Textures")
        self.resize(800, 600)

        # Add a menu to open .obj files
        self.menu = self.menuBar().addMenu('File')
        self.open_action = self.menu.addAction('Open .obj file')
        self.open_action.triggered.connect(self.open_file)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open 3D Model", "", "OBJ Files (*.obj)")
        if file_name:
            self.viewer.load_model(file_name)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
