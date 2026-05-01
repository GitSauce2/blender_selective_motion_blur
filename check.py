import bpy
from .func import print_status
from .exception import *

def checklist():
    scene = bpy.context.scene
    prefs = bpy.context.preferences.addons['bl_ext.user_default.selective_motion_blur'].preferences
    
    # Check if the active GPU is using OpenGL. If it isn't, stop the script and tell the user to restart Blender with OpenGL enabled.
    # We need this because of the VRAM stacking issue using Vulkan. Alt Render Only.
    backend_type = bpy.context.preferences.system.gpu_backend
    altr_enable = prefs.alt_render
    backend_enable = prefs.force_backend
    if backend_type != "OPENGL" and not backend_enable and altr_enable:
        MessengerError(f"GPU backend type is set to '{backend_type}'! Please set to OpenGL in (Edit > Preferences > System) and restart Blender, or force GPU in the addon's Preferences.", "WARNING: Alternative Render - Not Using OpenGL", 'ERROR', True)
    
    engine_type = scene.render.engine
    engine_enable = prefs.force_engine
    if engine_type != 'BLENDER_EEVEE' and not engine_enable:
        MessengerError(f"Render Engine is set to '{engine_type}'! Please set the render engine to EEVEE, or force it in the addon's Preferences.", "WARNING: Not Using EEVEE", 'ERROR', True)
    
    # Check for an active camera.
    if scene.camera == None:
        MessengerError("*There is no active camera in this scene! Please set an active camera.*", "ERR: Camera", 'ERROR', True)
        
    # Check for locked interface. Enable it if disabled.
    li = False
    if not scene.render.use_lock_interface:
        print_status("*Lock Interface was set to False! Temporarily setting to True...*")
        scene.render.use_lock_interface = True
        li = True
    
    return li
