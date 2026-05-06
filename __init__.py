# ##### BEGIN GPL LICENSE BLOCK #####
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name" : "Selective Motion Blur",
    "author" : "SauceBees",
    "version" : (0, 6, 0),
    "blender" : (5, 0, 0),
    "location" : "Object/Render Properties > Selective Motion Blur Options",
    "description" : "Individual object motion blurring for EEVEE.",
    "warning" : "",
    "wiki_url" : "https://github.com/GitSauce2/selective_motion_blur",
    "tracker_url" : "https://github.com/GitSauce2/selective_motion_blur",
    "category" : "",
}

import bpy
from .preferences import SelectiveMotionBlur_preferences
from .properties import smb_main_properties, smb_object_properties, smb_parent_props
from .operators import render_OT_Image, render_OT_Anim
from .sub_op import smb_OT_parent_additem, smb_OT_parent_deleteitem, smb_OT_parent_moveitem
from .ui import SelectiveMotionBlurMain_PT_ui, SMB_UL_parent_list, SelectiveMotionBlur_PT_ui, SelectiveMotionBlur_PT_parent_slots

from bpy.types import Scene, Object
from bpy.props import PointerProperty, CollectionProperty, IntProperty

### REGISTER ###

classes = (
    SelectiveMotionBlur_preferences,
    smb_main_properties,
    smb_object_properties,
    smb_parent_props,
    SMB_UL_parent_list,
    SelectiveMotionBlurMain_PT_ui,
    SelectiveMotionBlur_PT_ui,
    SelectiveMotionBlur_PT_parent_slots,
    render_OT_Image,
    render_OT_Anim,
    smb_OT_parent_additem,
    smb_OT_parent_deleteitem,
    smb_OT_parent_moveitem,
)

addon_keymaps = []

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    Scene.select_motion_blur = PointerProperty(type= smb_main_properties)
    Object.select_motion_blur = PointerProperty(type= smb_object_properties)
    Object.smb_parent_obj = CollectionProperty(type= smb_parent_props)
    Object.smb_parent_index = IntProperty(name = "SMB Parent Slot", default= 0)
    
    key_config = bpy.context.window_manager.keyconfigs.addon
    
    if key_config:
        key_map = key_config.keymaps.new(name='Screen', space_type='EMPTY')
        
        key_image = key_map.keymap_items.new("render.smb_img",
                                             type='F10',
                                             value='PRESS',
                                             )
                                             
        key_anim = key_map.keymap_items.new("render.smb_anim",
                                             type='F10',
                                             value='PRESS',
                                             ctrl=True,
                                             )
                                             
        addon_keymaps.append((key_map, key_image, key_anim))

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
    del Scene.select_motion_blur
    del Object.select_motion_blur
    del Object.smb_parent_obj
    del Object.smb_parent_index
    
    for key_map, key_image, key_anim in addon_keymaps:
        key_map.keymap_items.remove(key_image)
        key_map.keymap_items.remove(key_anim)
        
        addon_keymaps.clear()
