import bpy
from .operators import render_OT_Image, render_OT_Anim

### USER INTERFACE ###

class SelectiveMotionBlurMain_PT_ui(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_label = "Selective Motion Blur Options"
    bl_idname = "SELECTIVE_MOTION_BLUR_MAIN_PT_ui"
    bl_context = "render"
    
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

class SelectiveMotionBlur_PT_ui(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_label = "Selective Motion Blur Options"
    bl_idname = "SELECTIVE_MOTION_BLUR_PT_ui"
    bl_context = "object"
    
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