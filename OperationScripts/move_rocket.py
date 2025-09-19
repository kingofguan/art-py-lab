import bpy
import bmesh

space_object = bpy.data.objects.get('Space_Craft')

#if space_object:
#    bpy.data.objects.remove(space_object, do_unlink=True)

#bpy.ops.mesh.primitive_cube_add(
#    size=2,
#    calc_uvs=True,
#    enter_editmode=False,
#    align='WORLD',
#    location=(x_cursor, y_cursor, z_cursor),
#    rotation=(0, 0, 0),
#    scale=(1, 1, 1)
#)

my_cursor_location = bpy.context.scene.cursor.location

my_cursor_location.x = 0
my_cursor_location.y = 0 
my_cursor_location.z = 1

space_object.location.x = my_cursor_location.x
space_object.location.y = my_cursor_location.y
space_object.location.z = my_cursor_location.z

#cube_object = bpy.context.object.data

#bm = bmesh.new()
#bm.from_mesh(cube_object)

#bm.verts.ensure_lookup_table()
#for v in [3, 7, 6, 2]:
#    bm.verts[v].co.y -= 1.0

#bm.to_mesh(cube_object)
#bm.free()