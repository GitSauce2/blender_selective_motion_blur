import bpy

# Separate to make sure we ONLY get Blender's attr and subattr.
### Contains Blender attributes only
allowed_attr = (
    'id_type',
    'session_uid',
    'is_evaluated',
    'users',
    'is_embedded_data',
    'is_linked_packed',
    'is_missing',
    'is_runtime_data',
    'is_editable',
    'tag',
    'is_library_indirect',
    'library',
    'library_weak_reference',
    'asset_data',
    'override_library',
    'preview',
    'type',
    'mode',
    'bound_box',
    'track_axis',
    'up_axis',
    'material_slots',
    'shader_effects',
    'vertex_groups',
    'empty_display_type',
    'empty_display_size',
    'empty_image_offset',
    'image_user',
    'empty_image_depth',
    'show_empty_image_perspective',
    'show_empty_image_orthographic',
    'show_empty_image_only_axis_aligned',
    'use_empty_image_alpha',
    'empty_image_side',
    'add_rest_position_attribute',
    'pass_index',
    'color',
    'field',
    'collision',
    'soft_body',
    'particle_systems',
    'rigid_body',
    'rigid_body_constraint',
    'use_simulation_cache',
    'hide_viewport',
    'hide_select',
    'hide_render',
    'hide_probe_volume',
    'hide_probe_sphere',
    'hide_probe_plane',
    'hide_surface_pick',
    'show_instancer_for_render',
    'show_instancer_for_viewport',
    'visible_camera',
    'visible_diffuse',
    'visible_glossy',
    'visible_transmission',
    'visible_volume_scatter',
    'visible_shadow',
    'is_holdout',
    'is_shadow_catcher',
    'instance_type',
    'use_instance_vertices_rotation',
    'use_instance_faces_scale',
    'instance_faces_scale',
    'is_instancer',
    'display_type',
    'show_bounds',
    'display_bounds_type',
    'show_name',
    'show_axis',
    'show_texture_space',
    'show_wire',
    'show_all_edges',
    'use_grease_pencil_lights',
    'show_transparent',
    'show_in_front',
    'pose',
    'show_only_shape_key',
    'use_shape_key_edit_mode',
    'use_dynamic_topology_sculpting',
    'is_from_instancer',
    'is_from_set',
    'display',
    'lineart',
    'use_mesh_mirror_x',
    'use_mesh_mirror_y',
    'use_mesh_mirror_z',
    'lightgroup',
    'light_linking',
    'shadow_terminator_normal_offset',
    'shadow_terminator_geometry_offset',
    'shadow_terminator_shading_offset',
    'cycles',
    
    # From this addon
    'select_motion_blur',
    )

### Contains Blender subattributes only
allowed_subattr = (
    'type',
    'shape',
    'falloff_type',
    'texture_mode',
    'z_direction',
    'strength',
    'linear_drag',
    'harmonic_damping',
    'quadratic_drag',
    'flow',
    'wind_factor',
    'inflow',
    'size',
    'rest_length',
    'falloff_power',
    'distance_min',
    'distance_max',
    'radial_min',
    'radial_max',
    'radial_falloff',
    'texture_nabla',
    'noise',
    'seed',
    'use_min_distance',
    'use_max_distance',
    'use_radial_min',
    'use_radial_max',
    'use_object_coords',
    'use_global_coords',
    'use_2d_force',
    'use_root_coords',
    'apply_to_location',
    'apply_to_rotation',
    'use_absorption',
    'use_multiple_springs',
    'use_smoke_density',
    'use_gravity_falloff',
    'texture',
    'source_object',
    'guide_minimum',
    'guide_free',
    'use_guide_path_add',
    'use_guide_path_weight',
    'guide_clump_amount',
    'guide_clump_shape',
    'guide_kink_type',
    'guide_kink_axis',
    'guide_kink_frequency',
    'guide_kink_shape',
    'guide_kink_amplitude',
    'use',
    'damping_factor',
    'damping_random',
    'friction_factor',
    'friction_random',
    'permeability',
    'use_particle_kill',
    'stickiness',
    'thickness_inner',
    'thickness_outer',
    'damping',
    'absorption',
    'cloth_friction',
    'use_culling',
    'use_normal',
    'show_shadows',
    'usage',
    'use_crease_override',
    'crease_threshold',
    'use_intersection_priority_override',
    'intersection_priority',
    'receiver_collection',
    'blocker_collection',
    'use_motion_blur',
    'use_deform_motion',
    'motion_steps',
    'use_camera_cull',
    'use_distance_cull',
    'shadow_terminator_offset',
    'shadow_terminator_geometry_offset',
    'ao_distance',
    'is_caustics_caster',
    'is_caustics_receiver',
    
    # From this addon
    'motion_blur',
    )
    
######################################################
### ATTRIBUTES THAT WERE DELETED (For Reference) ###
# Taken from bl_rna.properties

# 'data', # Do not copy data
# 'animation_data', # Do not copy anim data
# 'active', # Prevent crash for objs that are unselectable
# 'instance_collection', # Prevent error
# 'parent', # Do not copy parent
# 'name', 'name_full', # Do not copy name
# 'rna_type', # Prevent infinite loop
# 'original', # Prevent infinite loop
# 'active_material', 'active_material_index', # Prevent material assignment bug

# 'location', 'rotation_quaternion', 'rotation_axis_angle', 'rotation_euler', 'rotation_mode', 'scale', 'dimensions', 'delta_location',
# 'delta_rotation_euler', 'delta_rotation_quaternion', 'delta_scale', 'lock_location', 'lock_rotation', 'lock_rotation_w', 'lock_rotations_4d',
# 'lock_scale', 'matrix_world', 'matrix_local', 'matrix_basis', 'matrix_parent_inverse', 'modifiers', 'constraints', # Do not copy attributes we already removed

# 'motion_path', 'selection_sets', 'active_selection_set', # UNTESTED
# 'use_fake_user', 'use_extra_user', # UNTESTED
# 'active_index', 'active_shape_key', 'active_shape_key_index', # UNTESTED
# 'parent_type', 'parent_vertices', 'parent_bone', 'use_parent_final_indices', 'use_camera_lock_parent', # UNTESTED

######################################################

def copy_attr(obj, target, iterate=allowed_attr):
    for attr in iterate:
        try:
            # For debugging
            #print(f"'{attr}', ({obj})")
            
            value = getattr(obj, attr)
            setattr(target, attr, value)
            
        except: # Find subattr if there are any
            try:
                # For debugging
                #print(f"'{attr}', ({obj})")
                
                pointer = getattr(obj, attr)
                t_pointer = getattr(target, attr)
                
                copy_attr(pointer, t_pointer, allowed_subattr)
                
            except:
                pass
