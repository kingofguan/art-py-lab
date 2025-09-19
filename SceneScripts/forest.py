import bpy
import numpy as np
import random

from utils import add_shrinkwrap, random_direction, increase_random_size, is_near_objects


def generate_forest(col, terrain_obj, all_positions):
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
            add_shrinkwrap(obj, terrain_obj)
            random_direction(obj)
            increase_random_size(obj)
            all_positions.append([i[0], i[1], 3])


