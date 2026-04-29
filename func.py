import bpy
from bpy_extras import anim_utils

def driver_disabler(target, path):
    if target.animation_data:
        driver = target.animation_data.drivers.find(path)
        if driver and not driver.mute:
            driver.mute = True
            return driver
    return None

def fcurve_disabler(target, path):
    anim_data = target.animation_data
    if anim_data and anim_data.action and anim_data.action_slot:
        channelbag = anim_utils.action_get_channelbag_for_slot(anim_data.action, anim_data.action_slot)
        fcurve = channelbag.fcurves.find(path)
        if fcurve and not fcurve.mute:
            fcurve.mute = True
            return fcurve
    return None
    
def dr_fc_enabler(driver, fcurve):
    for anim in driver, fcurve:
        if anim:
            anim.mute = False
        
def print_status(string=''):
    prefs = bpy.context.preferences.addons['bl_ext.user_default.selective_motion_blur'].preferences
    if prefs.print_status or prefs.alt_render:
        print(string)