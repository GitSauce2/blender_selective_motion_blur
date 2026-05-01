import bpy
from bpy.types import Operator
from bpy.props import EnumProperty

class smb_OT_parent_additem(Operator):
    bl_idname = "selective_motion_blur.ui_add_parent"
    bl_label = ""
    bl_description = 'Add an optional parent slot for this object. This object will parent itself to the given object (if enabled) during the render. Only works if "Motion Blur" & "True MBI" are disabled'
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}
    
    def execute(self, context):
        context.object.smb_parent_obj.add()
        return {'FINISHED'}
    
class smb_OT_parent_deleteitem(Operator):
    bl_idname = "selective_motion_blur.ui_delete_parent"
    bl_label = ""
    bl_description = "Delete a parent slot"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}
    
    def execute(self, context):
        ui_list = context.object.smb_parent_obj
        index = context.object.smb_parent_index
        
        ui_list.remove(index)
        context.object.smb_parent_index = min(max(0, index - 1), len(ui_list) - 1)
        
        return {'FINISHED'}
    
class smb_OT_parent_moveitem(Operator):
    bl_idname = "selective_motion_blur.ui_move_parent"
    bl_label = ""
    bl_description = "Move a parent slot"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}
                                    
    direction_enum : EnumProperty(items=[
                                       ('UP', 'Up', ""),
                                       ('DOWN', 'Down', ""),
                                        ]
                                 )
        
    def move_index(self):
        index = bpy.context.object.smb_parent_index
        list_length = len(bpy.context.object.smb_parent_obj) - 1
        new_index = index + (-1 if self.direction_enum == 'UP' else 1)
    
        bpy.context.object.smb_parent_index = max(0, min(new_index, list_length))
    
    def execute(self, context):
        ui_list = context.object.smb_parent_obj
        index = context.object.smb_parent_index
        
        neighbor = index + (-1 if self.direction_enum == 'UP' else 1)
        ui_list.move(neighbor, index)
        self.move_index()
        
        return {'FINISHED'}
