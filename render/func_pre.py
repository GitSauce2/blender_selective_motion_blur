import bpy
from ..func import driver_disabler, fcurve_disabler, dr_fc_enabler

from mathutils import Matrix

def mesh_mod(obj, modlist, mod, attr, t_attr, path):
    modlist.append(getattr(mod, attr))
    
    modlist.append(driver_disabler(obj, path))
    modlist.append(fcurve_disabler(obj, path))
    setattr(mod, attr, t_attr)
    
def mesh_pre(obj, rehide_vp, col_lib, mod_lib):
    scene = bpy.context.scene
    
    # Reveal object's collection and its parents recursive
    # Objects can have multiple collections that must be enabled
    # Must do this before iterating to encompass all objects
    # Fix for modifiers not calculating when parent cols are hidden
    
    # Reveal the object itself too
    rehide_vp.append([obj, obj.hide_viewport, driver_disabler(obj, 'hide_viewport')])
    
    obj.hide_viewport = False
    
    for obj_col in obj.users_collection:
        if obj_col != scene.collection:
            col_lib.append(reveal_parent_cols(obj_col, scene.collection, []))
        else:
            col_lib.append(None)
    
    # Temp disable modifier drivers and set viewport levels to match render levels if applicable
    for mod in obj.modifiers:
        # index 0 = modifier
        # index 1 = original viewport setting
        # index 2,3 = viewport driver, fcurve, else None, None
        # index 4 = original editmode setting else None
        # index 5,6 = editmode driver, fcurve, else None, None
        # index 4 = original levels value else None
        # index 8,9 = levels driver, fcurve, else None, None
        
        mod_sublist = [mod]
        
        mesh_mod(obj, mod_sublist, mod, 'show_viewport', mod.show_render, f'modifiers["{mod.name}"].show_viewport')
        
        try:
            mesh_mod(obj, mod_sublist, mod, 'show_in_editmode', mod.show_render, f'modifiers["{mod.name}"].show_in_editmode')
        except:
            mod_sublist.extend([None, None, None])
            
        try:
            mesh_mod(obj, mod_sublist, mod, 'levels', mod.render_levels, f'modifiers["{mod.name}"].levels')
        except:
            mod_sublist.extend([None, None, None])
            
        mod_lib.append(mod_sublist)

def mesh_post(rehide_vp, col_lib, mod_lib):
    # Set back to original
    for mod_sublist in mod_lib:
        mod = mod_sublist[0]
        
        mod.show_viewport = mod_sublist[1]
            
        dr_fc_enabler(mod_sublist[2], mod_sublist[3])
            
        if mod_sublist[4] != None:
            mod.show_in_editmode = mod_sublist[4]
            
        dr_fc_enabler(mod_sublist[5], mod_sublist[6])
            
        if mod_sublist[7] != None:
            mod.levels = mod_sublist[7]
            
        dr_fc_enabler(mod_sublist[8], mod_sublist[9])
            
    # Rehide objs
    for obj_sublist in rehide_vp:
        
        obj_sublist[0].hide_viewport = obj_sublist[1]
        
        dr_fc_enabler(obj_sublist[2], None)
    
    # Rehide collections
    for col_sub in col_lib:
        if col_sub:
            for col in col_sub:
                col.hide_viewport = True
    
def reveal_parent_cols(obj_col, collection, list=[], call=True):
    for col in collection.children:
        if col == obj_col or reveal_parent_cols(obj_col, col, list, False):
            if col.hide_viewport:
                list.append(col)
                col.hide_viewport = False
            return list if call else True
    return None
    
def flash_collections():
    scene = bpy.context.scene
    col_to_hide = []
    for col in scene.collection.children_recursive:
        if col.hide_viewport:
            col.hide_viewport = False
            col_to_hide.append(col)
    
    bpy.context.view_layer.update()
    for col in col_to_hide:
        col.hide_viewport = True
        
def modify_simplify():
    scene = bpy.context.scene
    si = []
    if scene.render.use_simplify:
        si.append(scene.render.simplify_subdivision)
        
        si.append(driver_disabler(scene, 'render.simplify_subdivision'))
        si.append(fcurve_disabler(scene, 'render.simplify_subdivision'))
        
        scene.render.simplify_subdivision = scene.render.simplify_subdivision_render
        
    return si
    
def redo_simplify(si):
    scene = bpy.context.scene
    if si != []:
        scene.render.simplify_subdivision = si[0]
        
        if si[2]:
            fcurve = si[2]
            fcurve.mute = False
        
        if si[1]:
            driver = si[1]
            driver.mute = False
            
def apply_modcon(dup_obj):
    with bpy.context.temp_override(object=dup_obj):
        m = 0
        while m < len(dup_obj.modifiers):
            modifier_name = dup_obj.modifiers[m].name
            try:
                if dup_obj.modifiers[m].show_render:
                    bpy.ops.object.modifier_apply(modifier=modifier_name)
                else:
                    m += 1
            except RuntimeError:
                m += 1
                      
        c = 0
        while c < len(dup_obj.constraints):
            constraint_name = dup_obj.constraints[c].name
            try:
                if dup_obj.constraints[c].enabled:
                    bpy.ops.constraint.apply(constraint=constraint_name)
                else:
                    c += 1
            except RuntimeError:
                c += 1
                
def remove_gpkeys(dup_obj):
    scene = bpy.context.scene
    
    current_frame = scene.frame_current
    previous_frame = current_frame - 1
    
    for layer in dup_obj.data.layers:
        for frame in layer.frames:
            if frame.frame_number == current_frame:
                while True:
                    try:
                        layer.frames.copy(current_frame, previous_frame)
                        break
                        
                    except:
                        layer.frames.remove(previous_frame)
                        
                break

def parent_slots(obj, dup_obj):
    for parent_index in obj.smb_parent_obj:
        enable = parent_index.parent_enable
        target_parent = parent_index.target_parent
        
        if enable and target_parent and target_parent != obj:
            dup_obj.parent = target_parent
            
            target_bone = parent_index.target_bone
            if target_parent.type == 'ARMATURE' and target_bone:
                try:
                    bone = target_parent.pose.bones[target_bone]
                    
                    for scale_index in bone.scale:
                        if scale_index == 0:
                            print(f'ERR - {obj.name}: "{bone.name}" bone has a scale value of {scale_index}! Using "{target_parent.name}" armature instead.')
                            break
                    
                    else:
                        dup_obj.parent_type = 'BONE'
                        dup_obj.parent_bone = target_bone
                        
                        loc, rot, scale = bone.matrix.decompose() # Object follows bone tail. Offset to head.
                        
                        eval = bone.tail - bone.head

                        loc[0] += eval[0]
                        loc[1] += eval[1]
                        loc[2] += eval[2]

                        new_matrix = Matrix.LocRotScale(loc, rot, scale)
                        
                        dup_obj.matrix_parent_inverse = (target_parent.matrix_world @ new_matrix).inverted()
                        break
                except:
                    print(f'Error Setting "{obj.name}" Parent: Does the "{target_bone}" bone exist on the "{target_parent.name}" armature?')
            
            dup_obj.parent_type = 'OBJECT'
            dup_obj.matrix_parent_inverse = target_parent.matrix_world.inverted()
            
            break

# Make copies of materials to prevent motion blur bug. Does not solve objects without materials
def dupe_mats(obj):
    mat_sublist = []
    for slot in obj.material_slots:
        if slot.material:
            dup_mat = slot.material.copy()
            
            org_mat = slot.material
            slot.material = dup_mat
            mat_sublist.append([org_mat, dup_mat, slot.slot_index])
    
    return mat_sublist
