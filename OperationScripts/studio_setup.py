import bpy

bpy.ops.mesh.primitive_plane_add(size=15, enter_editmode=True, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

for obj in bpy.context.selected_objects:
    obj.name = 'background_geo'
    obj.data.name = 'background_geo'
    

bpy.ops.mesh.subdivide(number_cuts=3)

# set to interactive mode
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)


for v in [15, 14, 13, 2, 3]:
    bpy.data.objects['background_geo'].data.vertices[v].co.z += 8.0
    
#bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    
    
bpy.ops.object.subdivision_set(level=2)
bpy.ops.object.shade_smooth()



# add camera

bpy.ops.object.camera_add(
    enter_editmode=False, align='VIEW', location=(0, -6, 1), 
    rotation=(1.5708, 0, 0), scale=(1, 1, 1)
)


# add monkey
bpy.ops.mesh.primitive_monkey_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 1), scale=(1, 1, 1))

bpy.ops.object.subdivision_set(level=2)
bpy.ops.object.shade_smooth()



# add light (press z in camera mode to render)

bpy.ops.object.light_add(
    type='AREA', radius=1, align='WORLD', location=(-2.7, 2.5, 3.3), scale=(1, 1, 1),
    rotation=(1.0472, 0.174533, -0.872665)
)

bpy.context.object.data.energy = 100

for obj in bpy.context.selected_objects:
    obj.name = 'key_light'
    obj.data.name = 'key_light'


bpy.ops.object.light_add(
    type='AREA', radius=1, align='WORLD', location=(3.2, -3.2, 2.4), scale=(1, 1, 1),
    rotation=(1.309, -0.261799, 0.872665)
)

bpy.context.object.data.energy = 30

for obj in bpy.context.selected_objects:
    obj.name = 'fill_light'
    obj.data.name = 'fill_light'