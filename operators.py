import bpy
import time

from bpy.types import Operator

from .render.pre import SMB_pre
from .render.post import SMB_post, cleanup_post
from .func import print_status
from .check import checklist
from .exception import *

# GLOBAL
render_complete = False
render_cancel = False

def smb_complete(scene): # Handler for render completion. Ensures the timer doesn't execute early
    global render_complete
    render_complete = True
    bpy.app.handlers.render_complete.remove(smb_complete)
    bpy.app.handlers.render_cancel.remove(smb_cancel)

def smb_cancel(scene): # Handler for cancelling render
    global render_cancel
    render_cancel = True
    bpy.app.handlers.render_cancel.remove(smb_cancel)
    bpy.app.handlers.render_complete.remove(smb_complete)
    
# LOCAL FUNC

def time_converter(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    
    time = f"{seconds:.2f} sec"
    
    if minutes > 0:
        time = f"{int(minutes):02d} min : {time}"
        if hours > 0:
            time = f"{int(hours):02d} hr{'s' if hours > 1 else ''} : {time}"
    
    return time

def end_img_report(self, render_time):
    prefs = bpy.context.preferences.addons['bl_ext.user_default.selective_motion_blur'].preferences
    scene = bpy.context.scene
    current_frame = scene.frame_current
    
    report = f"Finished Rendering Frame: {current_frame} | Time - {time_converter(render_time)}"
    
    if prefs.give_report:
        MessengerError(report, "Selective Motion Blur", 'INFO', False)
    elif prefs.alt_render:
        self.report({'INFO'}, report)
    else:
        print_status(report)
        
def end_anim_report(self, render_time, start_frame, end_frame, step_frame):
    prefs = bpy.context.preferences.addons['bl_ext.user_default.selective_motion_blur'].preferences
    report = f"Finished Rendering Frames: {start_frame}-{end_frame} | Frame Step: {step_frame} | Total Render Time - {time_converter(render_time)}" 

    if prefs.give_report:
        print("")
        print("##########")
        print("")
        MessengerError(report, "Selective Motion Blur", 'INFO', False)
    elif prefs.alt_render:
        self.report({'INFO'}, report)
    else:
        print_status(report)


### OPERATORS ###

# Render Image
# Note that pre handlers are not reliable because this script modifies data.
class render_OT_Image(Operator):
    """Render an Image using Selective Motion Blur. This will reset modified, but not set, keyframes"""
    bl_idname = "render.smb_img"
    bl_label = "Render Image SMB"
    bl_options = {"REGISTER", "INTERNAL"}
    
    def execute(self,context):
        try:
            
            scene = context.scene
            prefs = context.preferences.addons['bl_ext.user_default.selective_motion_blur'].preferences
            
            if scene.select_motion_blur.smb_enable:
            
                start_time = time.perf_counter()
                
                li = checklist()
                
                print_status("")
                print_status("<Initializing SMB Image Render!>")
                
                scene.frame_set(scene.frame_current) # Reset frame
                
                delete_lib, org_lib, del_mat_lib = SMB_pre()
                    
                print_status("<Rendering Image...>")

                def img_method(invoke=True):
                    global render_complete, render_cancel
                    if not bpy.app.is_job_running('RENDER') and (render_complete or render_cancel) or not invoke:
                        
                        print_status("<Finalizing...>" if not render_cancel else "<Cancelling...>")
                        SMB_post(delete_lib, org_lib, del_mat_lib)
                        cleanup_post(li)
                        
                        # Calculate stats and give report.
                        end_time = time.perf_counter()
                        render_time = end_time - start_time
                        if not render_cancel:
                            end_img_report(self, render_time)
                            
                        else:
                            report = f"Render Cancelled! | Time - {time_converter(render_time)}"
                            
                            if prefs.give_report:
                                MessengerError(report, "Selective Motion Blur", 'INFO', False)
                            else:
                                print_status(report)
                                
                        return None
                        
                    return 0.001
                
                if not prefs.alt_render:
                    global render_complete, render_cancel
                    render_complete = render_cancel = False
                    
                    bpy.app.handlers.render_complete.append(smb_complete)
                    bpy.app.handlers.render_cancel.append(smb_cancel)
                    
                    bpy.ops.render.render('INVOKE_DEFAULT', write_still=prefs.write_image) # Render
                    bpy.app.timers.register(img_method) # Use timers instead of post handlers because handlers MAY cause external addon errors
                    
                else:
                    bpy.ops.render.render(write_still=prefs.write_image) # Render
                    img_method(False)
                
            else: # Use default render method if disabled.
                bpy.ops.render.render('INVOKE_DEFAULT', write_still=prefs.write_image)
        
        except ExitSafe:
            return {'CANCELLED'}
        
        return {'FINISHED'}
    
# Render Animation
# Note that pre handlers are not reliable because this script modifies data.
class render_OT_Anim(Operator):
    """Render an Animation using Selective Motion Blur. This will reset modified, but not set, keyframes"""
    bl_idname = "render.smb_anim"
    bl_label = "Render Animation SMB"
    bl_options = {"REGISTER", "INTERNAL"}
        
    def execute(self,context):
        #print("DEV : Testb4Try")
        try:
        
            scene = context.scene
            view = context.preferences.view
            prefs = context.preferences.addons['bl_ext.user_default.selective_motion_blur'].preferences
            
            if scene.select_motion_blur.smb_enable:
                li = checklist()
                
                step_frame = scene.frame_step
                if step_frame == 0:
                    MessengerError("*Stepped frame is set to 0! Cancelled render to prevent infinite loop. Increase Step Frame or consider rendering an image instead.*", "ERR: Stepped Frame", 'ERROR', True)
                
                # Get stuff.
                original_frame = scene.frame_current
                start_frame = scene.frame_start
                end_frame = scene.frame_end
                
                original_display = view.render_display_type

                start_time = time.perf_counter()
                print_status("")
                print_status(f"<Beginning to Render Frames: {start_frame}-{end_frame} to ({scene.render.filepath}) | Frame Step: {step_frame}{' | Force close Blender to cancel.' if prefs.alt_render else ''}>")
                
                scene.frame_set(start_frame)
                    
                print_status("")
                i = end_frame - start_frame + 1
                    
                def anim_method(i, delete_lib, org_lib, del_mat_lib, tframe_start):
                    global render_complete, render_cancel
                    if not bpy.app.is_job_running('RENDER') and (render_complete or render_cancel):
                    
                        current_frame = scene.frame_current
                        
                        SMB_post(delete_lib, org_lib, del_mat_lib)
                        
                        end_time = time.perf_counter()
                        render_time = end_time - start_time
                        if not render_cancel:
                            
                            tframe_end = time.perf_counter()
                            
                            render_frame_time = tframe_end - tframe_start
                            
                            print_status(f"Time: {time_converter(render_frame_time)}")
                            print_status("")
                            
                            current_frame += step_frame
                            scene.frame_set(current_frame)
                            i -= step_frame
                            
                            if i > 0:
                                anim_loop(i, display=False)
                                
                            else:
                                view.render_display_type = original_display
                                print_status("<Finalizing...>")
                                cleanup_post(li, original_frame)
                                
                                # Calculate stats and give report.
                                end_anim_report(self, render_time, start_frame, end_frame, step_frame)
                        else:
                            view.render_display_type = original_display
                            print_status("<Cancelling...>")
                            cleanup_post(li, original_frame)
                            
                            report = f"Animation Render Cancelled! | Total Render Time: {time_converter(render_time)}"
                            
                            if prefs.give_report:
                                MessengerError(report, "Selective Motion Blur", 'INFO', False)
                            else:
                                print_status(report)
                            
                        return None
                    
                    return 0.001

                def anim_loop(i, display=True, invoke=True):
                    scene = bpy.context.scene
                    current_frame = scene.frame_current
                    print_status(f"--- Frame:{current_frame} ---")
                    
                    tframe_start = time.perf_counter()
                    
                    delete_lib, org_lib, del_mat_lib = SMB_pre()
                        
                    print_status("<Rendering...>") # Use animation=True instead of write_still=True because
                                                   # write_still saves in the next render if the render op
                                                   # is called
                    if invoke: # Use invoke method
                        if not display:
                            view.render_display_type = 'NONE'
                            
                        global render_complete, render_cancel
                        render_complete = render_cancel = False
                        
                        bpy.app.handlers.render_complete.append(smb_complete)
                        bpy.app.handlers.render_cancel.append(smb_cancel)
                        
                        scene.frame_start = current_frame
                        scene.frame_end = current_frame
                        bpy.ops.render.render('INVOKE_DEFAULT', animation=True) # Render
                        scene.frame_start = start_frame
                        scene.frame_end = end_frame
                        
                        bpy.app.timers.register(lambda: anim_method(i, delete_lib, org_lib, del_mat_lib, tframe_start)) # Use timers instead of post handlers because handlers MAY cause external addon errors
                        
                    else: # Use non-invoke method
                        scene.frame_start = current_frame
                        scene.frame_end = current_frame
                        bpy.ops.render.render(animation=True) # Render
                        scene.frame_start = start_frame
                        scene.frame_end = end_frame
                        
                        SMB_post(delete_lib, org_lib, del_mat_lib)
                        
                        tframe_end = time.perf_counter()
                        
                        render_frame_time = tframe_end - tframe_start
                        
                        print_status(f"Time: {time_converter(render_frame_time)}")
                        print_status("")
                        
                        current_frame += step_frame
                        scene.frame_set(current_frame)
                        i -= step_frame
                    
                        return i
                
                if not prefs.alt_render:
                    anim_loop(i)
                    
                else:
                    while i > 0:
                        i = anim_loop(i, invoke=False)
                        view.render_display_type = 'NONE'
                    view.render_display_type = original_display
                    
                    print_status("<Finalizing...>")
                    cleanup_post(li, original_frame)
                    
                    # Calculate stats and give report.
                    end_time = time.perf_counter()
                    render_time = end_time - start_time
                    end_anim_report(self, render_time, start_frame, end_frame, step_frame)
                
            else: # Use default render method if disabled.
                bpy.ops.render.render('INVOKE_DEFAULT', animation=True)
        
        except ExitSafe:
            return {'CANCELLED'}
        
        return {'FINISHED'}
