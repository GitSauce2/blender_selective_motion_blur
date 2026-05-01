import bpy
from .operators import render_OT_Image, render_OT_Anim

from bpy.types import Panel, UIList

### USER INTERFACE ###

class SelectiveMotionBlurMain_PT_ui(Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_label = "Selective Motion Blur Options"
    bl_idname = "SELECTIVE_MOTION_BLUR_MAIN_PT_ui"
    bl_context = "render"
    bl_options = {'DEFAULT_CLOSED'} 
    
    def draw(self, context):
        scene = context.scene
        smb = scene.select_motion_blur
        
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = True
        col = layout.column()
        
        row = col.row()
        row.prop(smb, "smb_enable")
        row = col.row()
        row = col.row()
        
        box = layout.box()
        col = box.column(align=True)
        row = col.row()
        row.operator("render.smb_img", emboss=True, text="Render Image", icon='RENDER_STILL')
        row = col.row()
        row.operator("render.smb_anim", emboss=True, text="Render Animation", icon='RENDER_ANIMATION')

class SMB_UL_parent_list(UIList):
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            
            row = layout.row(align=True)
            row.prop(item, "target_parent", text="")
            if item.target_parent and item.target_parent.type == 'ARMATURE':
                row.prop_search(item, "target_bone", item.target_parent.data, "bones", text="")
                
            row.prop(item, "parent_enable", text="")
            
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon='OBJECT_DATA')

class SelectiveMotionBlur_PT_ui(Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_label = "Selective Motion Blur"
    bl_idname = "SELECTIVE_MOTION_BLUR_PT_ui"
    bl_context = "object"
    bl_options = {'DEFAULT_CLOSED'} 
    
    @classmethod
    def poll(self, context):
        if context.object.type != "ARMATURE":
            return True
        else:
            return False
    
    def draw(self, context):
        obj = context.object
        obj_type = obj.type
        
        scene = context.scene
        smb_scene = scene.select_motion_blur.smb_enable
        
        smb = obj.select_motion_blur
        
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = True
        col = layout.column()
        
        if not smb_scene:
            row = col.row()
            row.label(text='* SMB is OFF!', translate=False)
            
        for mod in obj.modifiers:
            if mod.type == 'LINEART' and not mod.is_baked:
                row = col.row()
                row.label(text="* Greasepencils with non-baked lineart", translate=False)
                row = col.row()
                row.label(text="  modifiers can't be directly affected!", translate=False)
        
        row = col.row()
        row.prop(smb, "motion_blur")
        
        if obj_type != 'CAMERA':
            row = col.row()
            row.active = smb.motion_blur == False
            row.prop(smb, "true_mbi")
            
class SelectiveMotionBlur_PT_parent_slots(Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_label = "Parent Slots"
    bl_idname = "SELECTIVE_MOTION_BLUR_PT_parent_slots"
    bl_parent_id = "SELECTIVE_MOTION_BLUR_PT_ui"
    bl_context = "object"
    bl_options = {'DEFAULT_CLOSED'}
            
    def draw(self, context):
        obj = context.object
        
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        
        box = layout.box()
        col = box.column()
        
        row = col.row()
        row.label(text="Object's Render Parent Slots:", translate=False)
        row = col.row()
        row.template_list("SMB_UL_parent_list", "SMB Parent List", obj,
                          "smb_parent_obj", obj, "smb_parent_index")
        col = row.column()
        col.operator("selective_motion_blur.ui_add_parent", icon='ADD')
        
        if len(obj.smb_parent_obj) > 0:
            col.operator("selective_motion_blur.ui_delete_parent", icon='REMOVE')
            col.operator('selective_motion_blur.ui_move_parent', icon='TRIA_UP').direction_enum = 'UP'
            col.operator('selective_motion_blur.ui_move_parent', icon='TRIA_DOWN').direction_enum = 'DOWN'
