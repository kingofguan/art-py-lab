import bpy
import bmesh
import math

my_cursor_location = bpy.context.scene.cursor.location
x_cursor = my_cursor_location.x
y_cursor = my_cursor_location.y
z_cursor = my_cursor_location.z

x_rotation = math.radians(90)

cube_object = bpy.data.objects.get('Cube')

all_objs = bpy.context.scene.objects
for obj in all_objs:
    if 'cube' in obj.name.lower():
        bpy.data.objects.remove(obj, do_unlink=True)

if cube_object:
    bpy.data.objects.remove(cube_object, do_unlink=True)

bpy.ops.mesh.primitive_cube_add(
    size=2,
    calc_uvs=True,
    enter_editmode=False,
    align='WORLD',
    location=(x_cursor, y_cursor, z_cursor),
    rotation=(x_rotation, 0, 0),
    scale=(1, 1, 1)
)

cube_object = bpy.context.object.data

bm = bmesh.new()
bm.from_mesh(cube_object)

bm.verts.ensure_lookup_table()
for v in [3, 7, 6, 2]:
    bm.verts[v].co.y -= 1.0

bm.to_mesh(cube_object)
bm.free()