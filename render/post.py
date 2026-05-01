import bpy
from ..func import dr_fc_enabler

# Function for post-render.
def SMB_post(delete_lib, org_lib, del_mat_lib):
    scene = bpy.context.scene
    bdata = bpy.data
    motion_blur = scene.render.use_motion_blur
    shutter = scene.render.motion_blur_shutter
    
    # Delete materials created by the script.
    for mat in del_mat_lib:
        bdata.materials.remove(mat)
    
    # Library for deleting data.
    datalib = []
    
    for sublist in delete_lib:
        obj = sublist[0]
        
        # Store this object's data. If not empty.
        if obj.data:
            datalib.append(obj.data)
        
        # If this object is a duped camera, switch the active camera back to the original camera. (Only active cams are duped)
        if sublist[2]:
            scene.camera = sublist[2]
        
        # Delete the object.
        bdata.objects.remove(obj, do_unlink=True)
        
        # Reset metaballs.
        if sublist[1][0] != None: # Could be 0
            meta_obj = bdata.objects[sublist[1][2]]
            meta_obj.name = sublist[1][1]
            meta_obj.data.threshold = sublist[1][0]
    
    # Delete orphaned datas. Empties do not have data.
    datas = [d for d in datalib if d.users == 0]
    bdata.batch_remove(datas)
            
    # Reenable render for original objects.
    for sublist in org_lib:
        obj = sublist[0]
        
        if sublist[1]:
            obj.hide_render = False
        
        dr_fc_enabler(sublist[2], sublist[3])
        
        for mat_sub in sublist[4]:
            org_mat = mat_sub[0]
            dup_mat = mat_sub[1]
            
            obj.material_slots[mat_sub[2]].material = org_mat
            bdata.materials.remove(dup_mat)
    
def cleanup_post(li, original_frame=None):
    scene = bpy.context.scene
    
    # Set the frame back to what it was before rendering. (Non-error animation only)
    if original_frame != None: # Might be zero
        scene = bpy.context.scene
        scene.frame_set(original_frame)
    
    if li:
        scene.render.use_lock_interface = False
