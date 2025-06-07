import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def load_obj(file_path="../demo_3d/model_problems/engine/cube/cube_emp.obj"):
    vertices = []
    faces = []
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('v '):
                vertices.append(list(map(float, line.strip().split()[1:4])))
            elif line.startswith('f '):
                faces.append([int(i.split('/')[0]) - 1 for i in line.strip().split()[1:4]])
    return np.array(vertices), np.array(faces)

vertices, faces = load_obj("../demo_3d/model_problems/engine/cube/cube_emp.obj")

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
mesh = Poly3DCollection(vertices[faces], alpha=0.5, edgecolor='k')
ax.add_collection3d(mesh)
ax.set_xlim3d(vertices[:, 0].min(), vertices[:, 0].max())
ax.set_ylim3d(vertices[:, 1].min(), vertices[:, 1].max())
ax.set_zlim3d(vertices[:, 2].min(), vertices[:, 2].max())
plt.show()
