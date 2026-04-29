# Selective Motion Blur
**(Versions Supported)**
5.0x, 5.1x

An addon that is able to render individual object motion blurring for EEVEE. Works for many objects, including lights and cameras!

Supports grease pencil motion blurring introduced in Blender Version 5.0+

## IMPORTANT

This addon is in its **EARLY BETA** stage. Recommended to save before rendering.

1. The viewport must be frozen while rendering.
2. Non motion-blur objects must have their instances realized, otherwise the instances won't render.
3. Modified, but not set, keyframes will be lost on render.
4. When Alt Render is enabled, GPU backend must be set to 'OpenGL'. Vulkan has a VRAM stacking issue. (Toggleable)
5. This addon may be incompatible with other addons that add object properties which affect the render.

Expect a slight delay before each frame that increases with every object set to not motion blur.

Report any issues [here](https://github.com/GitSauce2/blender_selective_motion_blur/issues)

## Default Keybinds

**F10** - Render an Image

**CTRL + F10** - Render an Animation

Go to (Preferences > Keymap) and search for 'F10' in "Key-Binding" to change them.

Render buttons are also available in Render Properties.

## Preferences

### Settings:
- **Write Image Render** - Save the rendered image to the output path
- **Force Render Engine** - Allow render engines other than EEVEE
### Alternative Render:
- **Use Alt Render** - Enable to maybe fix some bugs. Cannot view live render progress. Cannot cancel render
- **Force GPU Backend** - Allow backends other than OpenGL. Only for Alt Render
### Extra Features:
- **Print Status To Console** - The render status is printed to the console. Always on with Alt Render
- **Report Finished Render** - The render is reported as a UI box

## Selective Motion Blur Options - UI

### Render Properties

- **Enable Selective Motion Blur** - Enable the addon. Otherwise use the normal render method

- Render Image & Animation Buttons

### Object Properties

- **Motion Blur** - Enable or disable motion blur for this specific object. Blurs caused by camera movement still apply
- **True MBI** - True Motion Blur Immunity. Object will never motion blur, even when the camera is moving (Only available when Motion Blur is off)

## Known Issues
1. In Blender Version 5.0x, objects sometimes disappear when rendering with grease pencil motion blur and a grease pencil object has the "lineart" modifier. Enable "Use Alt Render" in the addon's preferences. This hasn't been documented in Blender 5.1x .
2. Console spam when rendering a curve with a greasepencil lineart modifier in the same scene. This also occurs when using the normal render and the curve is set to not render.
3. Console spam when rendering a metaball mother that is globally hidden in viewports. This also occurs when the metaball mother becomes globally hidden, or any other object becomes globally hidden while the metaball mother is globally hidden.

Report any issues [here](https://github.com/GitSauce2/blender_selective_motion_blur/issues)

## License
This addon's code derives from Blender's Source Code and is licensed under the GNU General Public License v3.0.