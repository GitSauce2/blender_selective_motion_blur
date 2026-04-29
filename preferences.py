import bpy
from bpy.types import AddonPreferences
from bpy.props import BoolProperty

class SelectiveMotionBlur_preferences(AddonPreferences):
    bl_idname = __package__
    
    # Preferences
    
    write_image : BoolProperty(name="Write Image Render",
                               default=False,
                               description='Save the rendered image to the output path',
                               )
                                         
    force_engine : BoolProperty(name="Force Render Engine",
                                default=False,
                                description='Allow rendering using render engines other than EEVEE. The Selective Motion Blur addon was developed primarily for EEVEE Next! **USE AT YOUR OWN RISK**',
                                )
                                         
    # Alternative Render
    
    alt_render : BoolProperty(name="Use Alt Render",
                              default=False,
                              description='Use an alternative render method that might fix problems. Cannot view live render progress or cancel the render. Open the system console before rendering',
                              )
                                         
    force_backend : BoolProperty(name="Force GPU Backend",
                                 default=False,
                                 description='When Alt Render is enabled, allow the use of non-OpenGL (Vulkan) as the GPU backend. Be wary of VRAM stacking! **USE AT YOUR OWN RISK**',
                                 )
                                 
    # Extra Features
    
    print_status : BoolProperty(name="Print Status To Console",
                                default=False,
                                description='Print the status of the render to the console. If Alt Render is enabled, this is done regardless of this setting',
                                )
    
    give_report : BoolProperty(name="Report Finished Render",
                               default=False,
                               description='Report the render in the form of a UI box',
                               )
                               
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        
        box = layout.box()
        box.label(text="Settings:")
        col = box.column()
        
        row = col.row()
        row.prop(self, "write_image")
        row = col.row()
        row.prop(self, "force_engine")
        
        box = layout.box()
        box.label(text="Alternative Render:")
        col = box.column()
        
        row = col.row()
        row.prop(self, "alt_render")
        row = col.row()
        row.active = self.alt_render
        row.prop(self, "force_backend")
        
        box = layout.box()
        box.label(text="Extra Features:")
        col = box.column()
        
        row = col.row()
        row.prop(self, "print_status")
        row = col.row()
        row.prop(self, "give_report")