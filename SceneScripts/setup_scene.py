import bpy


def initialize_scene():
    # clear plane
    for i in bpy.data.objects:
        bpy.data.objects.remove(i)
    
    col = bpy.data.collections['Collection']
    return col


