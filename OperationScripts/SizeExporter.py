import bpy
import csv


class OBJECT_OT_export_size_data(bpy.types.Operator):
    """Export object data"""
    bl_idname = "object.export_size_data"
    bl_label = "Export Size Data"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        if not bpy.data.is_saved:
            self.report({'WARNING'}, 'please save before exporting')
            return {'CANCELLED'}
        file_path = bpy.path.abspath('//SizeExporter_Sizes.csv')
        
        try:
            with open(file_path, 'w', newline='', encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([
                    'Object Name', 'Collection Name', 'Material Name', 
                    'Sizes (W x D x H) mm'
                ])
                for index, obj in enumerate(bpy.context.scene.objects):
                    if index >= 1000:
                        break
                    if obj.type in ['MESH', 'CURVE', 'SURFACE', 'FONT', 'META']:
                        dimensions = obj.dimensions
                        dimensions_str = f'{round(dimensions[0] * 1000)} x {round(dimensions[1] * 1000)} x {round(dimensions[2] * 1000)}'
                        
                        collection_names = [
                            col.name for col in bpy.data.collections if obj.name in col.objects
                        ]
                        
                        collection_name_str = ','.join(collection_names) if collection_names else 'None'
                        
                        material_names = [
                            slot.material.name if slot.material else "None" 
                            for slot in obj.material_slots
                        ]
                        
                        material_names_str = ', '.join(material_names) if material_names else 'None'
                        
                        writer.writerow([obj.name, collection_name_str, material_names_str, dimensions_str])
                
                self.report({'INFO'}, f"Data exported to {file_path}")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to export data: {e}")
            return {'CANCELLED'}
        return {'FINISHED'}
    

class OBJECT_PT_size_exporter_panel(bpy.types.Panel):
    """Create a panel in the object properties window"""
    bl_label = "Size Exporter Panel"
    bl_idname = "OBJECT_PT_size_exporter_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SizeExporter"
    
    def draw(self, context):
        layout = self.layout
        layout.operator("object.export_size_data")


def register():
    bpy.utils.register_class(OBJECT_OT_export_size_data)
    bpy.utils.register_class(OBJECT_PT_size_exporter_panel)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_export_size_data)
    bpy.utils.unregister_class(OBJECT_PT_size_exporter_panel)
    
    
if __name__ == "__main__":
    register()
