# import threading
# from pathlib import Path
# import argparse
# import pyvista as pv
#
#
# def parse_args():
#     parser = argparse.ArgumentParser()
#
#     parser.add_argument(
#         "--image-path",
#         type=str,
#         required=True,
#         help="filepath",
#     )
#
#     return parser.parse_args()
#
#
# def show_model(image_path):
#     filename = image_path.split('/')[-1].split('.')[0]
#     ply_path = "./output/" + filename
#     path = Path(ply_path)
#     path.mkdir(exist_ok=True, parents=True)
#     if (path / "us.ply").is_file():
#
#         # pyvista
#         mesh = pv.read(ply_path + "/us.ply")
#         # cpos = mesh.plot()
#
#         kinds = [
#         ]
#         centers = [
#             (0, 1, 0),
#             (0, 0, 0),
#             (0, 2, 0),
#             (-1, 0, 0),
#             (-1, 2, 0),
#         ]
#         solids = [pv.PlatonicSolid(kind, radius=0.4, center=center) for kind, center in zip(kinds, centers)]
#         solids.append(mesh)
#         p = pv.Plotter(window_size=[700, 700])
#         for ind, solid in enumerate(solids):
#             # only use smooth shading for the teapot
#             smooth_shading = ind == len(solids) - 1
#             p.add_mesh(
#                 solid, color='silver', smooth_shading=smooth_shading, specular=1.0, specular_power=10
#             )
#         p.view_vector((5.0, 2, 3))
#         p.enable_shadows()
#         p.show()
#
#
# def main(image_path):
#     show_model(image_path)
#     print("Open 3D model")
#
#
# if __name__ == '__main__':
#     args = parse_args()
#     print(args)
#     main(args.image_path)


# ------------------ use open3d ------------------
import copy
import numpy as np
import open3d as o3d
import argparse
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--image-path",
        type=str,
        required=True,
        help="filepath",
    )

    return parser.parse_args()


def show_pkl(path):
    filename = path.split('/')[-1].split('.')[0]
    ply_path = "./output/" + filename
    path = Path(ply_path)
    path.mkdir(exist_ok=True, parents=True)
    if (path / "us.ply").is_file():
        mesh = o3d.io.read_triangle_mesh(ply_path + "/us.ply")

    quart = np.array([3.2, 0.1, 0]).T

    thQuart = mesh.get_rotation_matrix_from_xyz(quart)
    mesh.rotate(thQuart)

    print(mesh)
    print('Vertices:')
    print(np.asarray(mesh.vertices))
    print('Triangles:')
    print(np.asarray(mesh.triangles))

    verts = np.asarray(mesh.vertices)

    mesh.vertices = o3d.utility.Vector3dVector(verts)
    mesh.compute_vertex_normals()
    mesh.paint_uniform_color([0.2, 0.2, 0.2])

    print("Open 3D model")
    o3d.visualization.draw([mesh], title='Model Viewer', width=800, height=850)


if __name__ == "__main__":
    args = parse_args()
    print(args)
    show_pkl(args.image_path)
