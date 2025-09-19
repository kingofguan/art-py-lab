import bpy
import numpy as np
import mathutils
import math
import random


# clear plane
for i in bpy.data.objects:
    bpy.data.objects.remove(i)
    
col = bpy.data.collections['Collection']

# ----- add srhink wrap -----
def add_shrinkwrap(data, target):
    # place everything on the groud
    con = data.constraints.new('SHRINKWRAP')
    con.target = target
    con.shrinkwrap_type = 'PROJECT'
    con.project_axis = 'NEG_Z'


def look_at(obj, target):
    # adjust facing of an object
    position = mathutils.Vector((obj.location[0], obj.location[1], obj.location[2]))
    target_position = mathutils.Vector((target[0], target[1], target[2]))
    default_direction = mathutils.Vector((0, -1, 0))
    
    direction = (target_position - position).normalized()
    angle = math.acos(default_direction.dot(direction))
    
    rotation = default_direction.cross(direction).normalized()
    obj.delta_rotation_euler = [0, 0, rotation[2] * angle]
    
    
def random_direction(obj):
    obj.delta_rotation_euler = [0, 0, random.uniform(0, math.pi * 2)]
    
    
def increase_random_size(obj):
    val = random.random()/1.5
    obj.delta_scale = [obj.delta_scale[0] + val, obj.delta_scale[1] + val, obj.delta_scale[2] + val]
    
    
def add_materials(obj, color):
    # give object new material
    mat = bpy.data.materials.new(name='Material')
    mat.diffuse_color = color
    mat.specular_intensity = 0
    mat.roughness = 1
    obj.data.materials.append(mat)
    
    
def is_near_objects(obj, arr, min_distance):
    # help detec overlapping objects
    position = mathutils.Vector((obj[0], obj[1], obj[2]))
    result = False
    for i in arr:
        if not result:
            target_position = mathutils.Vector((i[0], i[1], i[2]))
            direction = target_position - position
            distance = math.sqrt(math.pow(direction.x, 2) + math.pow(direction.y, 2))
            if min_distance >= distance:
                result = True
    return result

all_positions = []

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


# ----- add forest -----
# Add trees add locations according to beta distribution   
beta_a = .44
beta_b = .44

forest_size = 50
forest_scale = 50

# load number of trees
trees = []

# load tree models
with bpy.data.libraries.load('//Models/Pine.blend') as (data_from, data_to):
    data_to.objects.append(data_from.objects[0])
trees.append(data_to.objects[0])
for i in range(1, 6):
    with bpy.data.libraries.load(f'//Models/Tree{i}.blend') as (data_from, data_to):
        data_to.objects.append(data_from.objects[0])
    trees.append(data_to.objects[0])
    
beta_random = (
    np.random.default_rng().beta(beta_a, beta_b, size=(forest_size, 2)) * forest_scale
) - forest_size / 2

for i in np.unique(beta_random, axis=0):
#    obj = data_to.objects[0].copy()
    if not is_near_objects([i[0], i[1], 3], all_positions, 3):
        obj = trees[random.randint(0, len(trees) -1)].copy()
        obj.location = (i[0], i[1], 3)
        col.objects.link(obj)
        # place object on the ground (terrain)
        add_shrinkwrap(obj, plane_obj)
        random_direction(obj)
        increase_random_size(obj)
        all_positions.append([i[0], i[1], 3])
    
    
    # add cubes instead of the tree model:
#    bpy.ops.mesh.primitive_cube_add(
#        size=2, enter_editmode=False, align='WORLD',
#        location=(i[0], i[1], 3), scale=(0.3, 0.3, 1)
#    )


# ----- add towns -----
# number of objects + 1
town_size = 10
# spacing
town_scale = 10

town_position_x = 1.5
town_position_y = 3

# generate a circle of houses
# circle size - 1 number of cubes
t = np.linspace(0, 2*np.pi, town_size)
t = np.linspace(0, (2*np.pi/town_size) * (town_size - 1), town_size)
formula_x = ((town_scale * np.cos(t)) + town_position_x)[:, np.newaxis]
formula_y = ((town_scale * np.sin(t)) + town_position_y)[:, np.newaxis]

coor_set = np.hstack((formula_x, formula_y))

houses = []

# load house models
for i in ['', '1', '2', '3']:
    with bpy.data.libraries.load(f'//Models/House{i}.blend') as (data_from, data_to):
        data_to.objects.append(data_from.objects[0])
    houses.append(data_to.objects[0])

#with bpy.data.libraries.load('//Models/House.blend') as (data_from, data_to):
#    data_to.objects.append(data_from.objects[0])
    
for i in np.unique(coor_set, axis=0):
#    obj = data_to.objects[0].copy()
    obj = houses[random.randint(0, len(houses) -1)].copy()
    
    # get random position to center
    obj_position = mathutils.Vector((i[0], i[1], 4))
    center_position = mathutils.Vector((town_position_x, town_position_y, 4))
    direction = (obj_position - center_position).normalized() * random.randint(-1, 10)
    obj_position = obj_position + direction
    if not is_near_objects([obj_position[0], obj_position[1], 4], all_positions, 3):
        obj.location = (obj_position[0], obj_position[1], 4)
        
        # use circle position
    #    obj.location = (i[0], i[1], 3)

        col.objects.link(obj)
        # place object on the ground (terrain)
        add_shrinkwrap(obj, plane_obj)
        
        # pointing houses to town center
        look_at(obj, [town_position_x, town_position_y, 4])
        all_positions.append([obj_position[0], obj_position[1], 4])
        
    # add cubes instead of the house model:
#    bpy.ops.mesh.primitive_cube_add(
#        size=2, enter_editmode=False, align='WORLD',
#        location=(i[0], i[1], 3), scale=(0.3, 0.3, 1)
#    )

