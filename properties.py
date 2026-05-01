import bpy
from bpy.types import PropertyGroup, Object
from bpy.props import BoolProperty, PointerProperty, StringProperty

class smb_main_properties(PropertyGroup):
    
    smb_enable : BoolProperty(name="Enable Selective Motion Blur",
                              default=True,
                              description='Enable the Selective Motion Blur Script. If disabled, use normal render instead',
                              options=set()
                             )

class smb_object_properties(PropertyGroup):
    
    motion_blur : BoolProperty(name="Motion Blur",
                               default=True,
                               description='Enable motion blur for this object',
                              )
    
    true_mbi : BoolProperty(name="True MBI",
                            default=False,
                            description='Enable True Motion Blur Immunity for this object. Only works if "Motion Blur" is disabled',
                           )
                                         
class smb_parent_props(PropertyGroup):
    
    target_parent : PointerProperty(name="Target Parent",
                                    type=Object,
                                    description='Select another object that the current object will temporarily parent to when rendering. Only works if "Motion Blur" & "True MBI" are disabled. Does not consider the parent\'s motion blur. Will be skipped if it\'s the current object or unassigned',
                                   )
                                
    target_bone : StringProperty(name="Target Bone",
                                 description="Select a bone for this armature. Will use the object if none are assigned, this bone doesn't exist, or this bone has a 0.0 scale value",
                                )
                                
    parent_enable : BoolProperty(name="Enable Parent",
                                 default=True,
                                 description='Use this parent for the render. Only the highest enabled and valid parent in the list takes effect',
                                )
