import bpy
from bpy.types import PropertyGroup
from bpy.props import BoolProperty

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