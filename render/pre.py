import bpy
from ..func import driver_disabler, fcurve_disabler, dr_fc_enabler
from .func_pre import mesh_mod, mesh_pre, mesh_post, reveal_parent_cols, flash_collections, modify_simplify, redo_simplify, apply_modcon, remove_gpkeys, parent_slots, dupe_mats
from .copy_attr import copy_attr

# Function for pre-render.
def SMB_pre():
    scene = bpy.context.scene
    prefs = bpy.context.preferences.addons['bl_ext.user_default.selective_motion_blur'].preferences
    
    motion_blur = scene.render.use_motion_blur
    shutter = scene.render.motion_blur_shutter
    
    # Temp change simplify viewport value to render value
    si = modify_simplify()
    
    # Flash all collections that are globally hidden in viewports
    # Fix for objs not duping correctly when hidden this way
    flash_collections()
    
    # For meshes
    rehide_vp = []
    col_lib = []
    mod_lib = []
    
    # List for dupes that need deleting. This list contains sublists.
    delete_lib = []
    
    # List for original objects that were duped. This list contains sublists.
    org_lib = []
    
    # Library for materials made that need deleting.
    del_mat_lib = []
    
    # Append objects first. We don't want to iterate through a list that has dupes being added.
    object_lib = []
    for obj in scene.objects:
        if obj.type != 'ARMATURE':
            if obj.type == 'MESH':
                mesh_pre(obj, rehide_vp, col_lib, mod_lib)
                
            elif obj.type == 'GREASEPENCIL':
                for mod in obj.modifiers:
                    if mod.type == 'LINEART' and not mod.is_baked: # Disallow lineart modifier
                        break
                else:
                    object_lib.append(obj)
                continue
                
            object_lib.append(obj)
    
    # Checks if global motion blur is enabled and working for this frame.
    if shutter > 0 and motion_blur:
        current_cam = scene.camera
        
        for obj in object_lib:
            
            if not obj.hide_render:
                # Make Motion Blur Immune duplicate if off
                if not obj.select_motion_blur.motion_blur:
                    
                    # Sublist for delete list
                    # index 0 = name
                    # index 1 = metaball data else None, name, and new name
                    # index 2 = org camera name else False
                    sublist = []
                    
                    if obj.type == 'MESH': # Use evaluated depsgraphs for meshes (Preserve Volume Compat for armatures)
                        
                        depsgraph = bpy.context.evaluated_depsgraph_get()
                        obj_eval = obj.evaluated_get(depsgraph)
                        
                        dup_mesh = bpy.data.meshes.new_from_object(obj_eval)
                        dup_obj = bpy.data.objects.new(obj.name, dup_mesh)
                        
                        sublist.extend([dup_obj, [None], False])
                        
                        dup_obj.matrix_world = obj.matrix_world
                        
                    else: # Everything else
                    
                        dup_obj = obj.copy()
                        
                        meta_data = None
                        meta_name = obj.name
                        
                        # Empties do not have data.
                        if obj.data:
                            objd = obj.data
                            dup_obj.data = objd.copy()
                            
                            if obj.type == 'META': # Make doppelganger to put in same meta family
                                obj.name = "SEL_MO_BLUR_META" # Org obj is renamed. Changed back later
                                dup_obj.name = meta_name
                                meta_data = obj.data.threshold
                                obj.data.threshold = 0
                            
                        sublist.append(dup_obj)
                        sublist.append([meta_data, meta_name, obj.name])
                        
                        # Unlink all actions and drivers if this duplicate has them.
                        if dup_obj.animation_data:
                            dup_obj.animation_data_clear()
                        
                        # Apply modifiers and constraints on duplicates.
                        apply_modcon(dup_obj)
                                    
                        # Clear parent while keeping transforms.
                        if dup_obj.parent:
                            w_matrix = dup_obj.matrix_world.copy()
                            dup_obj.parent = None
                            dup_obj.matrix_world = w_matrix
                            
                        # Add the same frame to the previous frame for grease pencils.
                        if obj.type == 'GREASEPENCIL':
                            remove_gpkeys(dup_obj)
                            
                        # Checks if the original object is the active camera. If it is, then it switches to the duplicate instead and appends them to the sublist.
                        if obj == scene.camera:
                            sublist.append(obj)
                            scene.camera = dup_obj
                            
                        else:
                            sublist.append(False)
                        
                    # Copy attributes
                    copy_attr(obj, dup_obj)
                    
                    # Make copies of materials to prevent motion blur bug. Does not solve objects without materials
                    if prefs.solve_matbug:
                        for slot in dup_obj.material_slots:
                            if slot.material:
                                new_mat = slot.material.copy()
                                
                                slot.material = new_mat
                                del_mat_lib.append(new_mat)
                                
                    # Checks if True MBI is enabled in the original object and not a camera.
                    if obj.select_motion_blur.true_mbi and obj.type != 'CAMERA':
                        
                        # Set the duplicated object's parent to the active camera while keeping global transforms.
                        # No need to do it if the active camera has motion blur off.
                        
                        if current_cam.select_motion_blur.motion_blur:
                            dup_obj.parent = current_cam
                            dup_obj.parent_type = 'OBJECT'
                            dup_obj.matrix_parent_inverse = current_cam.matrix_world.inverted()
                            
                    else: # Render parent feature
                        parent_slots(obj, dup_obj)
                    
                    # Place duplicates into the original object's collection.
                    for collection in obj.users_collection:
                        collection.objects.link(dup_obj)
                    
                    delete_lib.append(sublist)
                    
                    # Disable original object in the render if it is not metaball.
                    # index 0 = name
                    # index 1 = hide_render bool
                    # index 2 = driver path, else None
                    # index 3 = fcurve path, else None
                    # index 4 = list for mats (has sublists) else []
                    
                    org_sublist = []
                    if obj.type != 'META':
                        org_sublist.extend([obj,
                                            True,
                                            driver_disabler(obj, 'hide_render'),
                                            fcurve_disabler(obj, 'hide_render'),
                                           ]
                                          )
                        obj.hide_render = True
                    else:
                        org_sublist.extend([obj,
                                            False,
                                            None,
                                            None,
                                           ]
                                          )
                            
                    org_sublist.append(dupe_mats(obj) if prefs.solve_matbug else [])
                    org_lib.append(org_sublist)
            
            elif not obj.select_motion_blur.motion_blur: # Temp disable keyframes because motion blur data shows in objs not rendering
                org_lib.append([obj,
                                False,
                                None,
                                fcurve_disabler(obj, 'hide_render'),
                                dupe_mats(obj) if prefs.solve_matbug else [],
                               ]
                              )
            
        # Create an empty mesh object (not an empty) to parent to the active camera. Cameras with motion blur off do not need it.
        # To fix inconsistent blurring with objects that have armatures. I literally don't know why this happens.
        cam = scene.camera
        if cam.select_motion_blur.motion_blur:
            mesh_data = bpy.data.meshes.new(name="Mesh_For_Camera")
            cam_obj = bpy.data.objects.new(name="Object_For_Camera", object_data=mesh_data)
            delete_lib.append([cam_obj, [None], False])
            
            for collection in cam.users_collection:
                collection.objects.link(cam_obj)
            
            cam_obj.parent = cam
    
    redo_simplify(si)
    mesh_post(rehide_vp, col_lib, mod_lib)
    
    return delete_lib, org_lib, del_mat_lib
