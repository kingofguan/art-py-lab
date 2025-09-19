import bpy
import csv

heading = []
graph_points = []
date_list = []

with open('C:/Users/guanj/OneDrive/Desktop/BlenderLab/Python_Blender/CSV/stock_data.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    heading = next(csv_reader)
    
    for row in csv_reader:
        graph_points.append(float(row[4]) * 5)
        date_list.append(row[0])
        
print("date_list = ", date_list)
print("graph_points = ", graph_points)

# create a list from 100 to 1200
width_x = 10 * 5
graph_x = []
for b in range(len(date_list)):
    graph_x.append(width_x)
    width_x += 10 * 5
    
print("graph_x =", graph_x)

# add curve to main database
the_curve_object = bpy.data.curves.new('CurveObject', type='CURVE')

the_curve_object.dimensions = '3D'
spline_object = the_curve_object.splines.new(type='POLY')

spline_object.points.add(len(graph_points)-1)

for point in range(len(graph_points)):
    y = graph_points[point]
    x = graph_x[point]
    spline_object.points[point].co = (x, y, 0, 1)
    
curve_obj = bpy.data.objects.new("crv_line", the_curve_object)
bpy.context.scene.collection.objects.link(curve_obj)

bpy.context.view_layer.objects.active = curve_obj

curve_list = []
curve_list.append(curve_obj)

for object in curve_list:
    # controlling animation by setting beginning/end frames
    bpy.context.object.data.bevel_depth = 2
    bpy.context.scene.frame_set(1)
    the_curve_object.bevel_factor_end = 0
    the_curve_object.keyframe_insert(data_path='bevel_factor_end')
    bpy.context.scene.frame_set(250)
    the_curve_object.bevel_factor_end = 1
    the_curve_object.keyframe_insert(data_path='bevel_factor_end')
    bpy.context.scene.frame_end = 250
    

# create materials
color_list_1 = [0.8, 0.0, 0.004, 1.0]
color_list_2 = [0.004, 0.0, 0.8, 1.0]
color_list_3 = [0.076, 0.883, 0.906, 1.0]
color_list_4 = [0.017, 0.8, 0.0, 1.0]

curve_obj = bpy.context.active_object
# set material to be new material m curve
curve_material = bpy.data.materials.new(name='M_curve')
# set use node property
curve_material.use_nodes = True
# add node to node tree such that we can access
nodes = curve_material.node_tree.nodes
# change curve object's material to curve material
curve_obj.active_material = curve_material
# set mat output to output node
mat_output = nodes.get('Material Output')
# create emission shader
node_type = nodes.new(type='ShaderNodeEmission')
node_type.inputs[0].default_value = (color_list_4)
node_type.inputs[1].default_value = 20
link = curve_material.node_tree.links.new
link(mat_output.inputs[0], node_type.outputs[0])

# adding dates to scence
for b, obj in zip(date_list, graph_x):
    each_text = b
    position_x = obj
    
    bpy.ops.object.text_add(radius = 10)
    bpy.context.active_object
    bpy.context.object.data.align_x = 'CENTER'
    bpy.context.object.data.body = each_text
    bpy.ops.transform.translate(value=(position_x, -5, 0))
    
    #curve_obj = bpy.context.active_object
    # set material to be new material date
    date_material = bpy.data.materials.new(name='M_date')
    # set use node property
    date_material.use_nodes = True
    # add node to node tree such that we can access
    nodes = date_material.node_tree.nodes
    # change curve object's material to curve material
    bpy.context.object.active_material = date_material
    # set mat output to output node
    mat_output = nodes.get('Material Output')
    # create emission shader
    node_type = nodes.new(type='ShaderNodeEmission')
    node_type.inputs[0].default_value = (color_list_2)
    node_type.inputs[1].default_value = 20
    link = date_material.node_tree.links.new
    link(mat_output.inputs[0], node_type.outputs[0])
    
# change background color
bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)

# adding a camera
cam_location_list = [250, 100, 100]
scene_cam = bpy.data.cameras.new('Camera')
cam_obj = bpy.data.objects.new('Camera', scene_cam)
bpy.context.scene.collection.objects.link(cam_obj)
cam_obj.data.type = 'ORTHO'
cam_obj.data.ortho_scale = 800
cam_obj.location.x = cam_location_list[0]
cam_obj.location.y = cam_location_list[1]
cam_obj.location.z = cam_location_list[2]
    