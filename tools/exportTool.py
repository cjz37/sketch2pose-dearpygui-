import copy
import numpy as np
import open3d as o3d
from tkinter.filedialog import asksaveasfilename
import shutil
import os


def exportTool():
    file_path = asksaveasfilename(title="Sketch2Pose export 3D model window",
                                  initialfile="New Model",
                                  filetypes=[("OBJ (*.obj)", "*.obj"), ("STL (*.stl)", "*.stl"),
                                             ("PLY (*.ply)", "*.ply")],
                                  defaultextension="*.obj")

    if file_path:
        mesh = o3d.io.read_triangle_mesh("./output/temp_file/us.ply")
        if not mesh:
            return

        if file_path[-4:] == ".stl":
            quart = np.array([-1.6, 0.1, 0]).T
            thQuart = mesh.get_rotation_matrix_from_xyz(quart)
            mesh.rotate(thQuart)

            verts = np.asarray(mesh.vertices)
            mesh.vertices = o3d.utility.Vector3dVector(verts)
            mesh.compute_vertex_normals()
        else:
            quart = np.array([3.2, 0.1, 0]).T
            thQuart = mesh.get_rotation_matrix_from_xyz(quart)
            mesh.rotate(thQuart)

        print(f"Export: {file_path}")
        o3d.io.write_triangle_mesh(file_path, mesh)
