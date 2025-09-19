import bpy
import mathutils
import math
import random


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


