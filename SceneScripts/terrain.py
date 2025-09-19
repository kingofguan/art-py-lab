import bpy
import numpy as np

from utils import add_materials


def generate_terrain(col):
    # ----- add terrain -----
    plane_mesh = bpy.data.meshes.new('my_plane')
    plane_obj = bpy.data.objects.new(plane_mesh.name, plane_mesh)

    my_verts = []
    my_edges = []
    my_faces = []

    size = 11
    scale = 60

    period = np.linspace(0, 2*np.pi, size) * 2
    np_coor = None

    for i in range(size):
        x = np.repeat(i, size)[:, np.newaxis]
        y = np.arange(size)[:, np.newaxis]
        
        # randomize terrain heights at vertices for elevation
        base_z = np.repeat(0, size)[:, np.newaxis]
        random_z = np.random.default_rng().random(size)[:, np.newaxis] / 2
        # add a sin like up and down shape
        sin_z_x = np.sin(np.repeat(period[i], size))[:, np.newaxis]
        sin_z_y = np.sin(period)[:, np.newaxis]
        
        z = base_z + random_z + sin_z_x + sin_z_y
        
        coor_set = np.hstack((x, y, z))
        
        if np_coor is None:
            np_coor = np.copy(coor_set)
        else:
            np_coor = np.concatenate((np_coor, coor_set))
            
    for id, i in enumerate(np_coor):
        x = (i[0] * (scale / 10)) - (scale/2)
        y = (i[1] * (scale / 10)) - (scale/2)
        z = i[2] - 1
        
        my_verts.append([x, y, z])
        
        if (id > size) & (id % size != 0):
            my_faces.append([id, id-1, id-size-1, id-size])

    plane_mesh.from_pydata(my_verts, my_edges, my_faces)

    add_materials(plane_obj, (0.495, 0.8, 0.087, 1))

    col.objects.link(plane_obj)

    return plane_obj


