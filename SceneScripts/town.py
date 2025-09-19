import bpy
import numpy as np
import random
import mathutils

from utils import add_shrinkwrap, look_at, is_near_objects


def generate_town(col, terrain_obj, all_positions):
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
            add_shrinkwrap(obj, terrain_obj)
            
            # pointing houses to town center
            look_at(obj, [town_position_x, town_position_y, 4])
            all_positions.append([obj_position[0], obj_position[1], 4])


