# Selective Motion Blur
**(Versions Supported)**
5.0x, 5.1x

An addon that is able to render individual object motion blurring for EEVEE. Works for many objects, including lights and cameras!

Supports grease pencil motion blurring introduced in Blender Version 5.0+

## IMPORTANT

This addon is in its **EARLY BETA** stage. Recommended to save before rendering.

1. The addon only works with its built-in renders.
2. The viewport must be frozen while rendering.
3. Non motion-blur objects must have their instances realized, otherwise the instances won't render.
4. Modified, but not set, keyframes will be **lost** on render.
5. When Alt Render is enabled, GPU backend must be set to 'OpenGL'. Vulkan has a VRAM stacking issue. (Toggleable)
6. This addon may be incompatible with other addons that add object properties which affect the render.

Expect a slight delay before each frame that increases with every object set to not motion blur. The time this addon records includes this delay, as well as the time it takes to write a render.

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
- **Use Alt Render** - An alternative render method. Cannot view live render progress. Cannot cancel render
- **Force GPU Backend** - Allow backends other than OpenGL. Only for Alt Render
### Extra Features:
- **Print Status To Console** - The render status is printed to the console. Always on with Alt Render
- **Report Finished Render** - The render is reported as a UI box
- **Solve Motion Blur Material Bug** - Solves a Blender bug that causes incorrect motion blur if there are two objects sharing the same material and the objects are in separate collections. Uses a lot of memory, and doesn't work on objects without materials

## Selective Motion Blur Options - UI

### Render Properties

- **Enable Selective Motion Blur** - Enable the addon. Otherwise use the normal render method

- Render Image & Animation Buttons

### Object Properties

- **Motion Blur** - Enable or disable motion blur for this specific object. Blurs caused by camera movement still apply
- **True MBI** - True Motion Blur Immunity. Object will never motion blur, even when the camera is moving (Only available when Motion Blur is off)
- **Parent Slots** - Set temporary parents for objects during the render. Prevents self motion-blurring while inheriting movement from other objects/bones (Only available when the above properties are off)

## Known Issues
1. Console spam when rendering a curve with a greasepencil lineart modifier in the same scene. This also occurs when using the normal render and the curve is set to not render.
2. Console spam when rendering a metaball mother that is globally hidden in viewports. This also occurs when the metaball mother becomes globally hidden, or any other object becomes globally hidden while the metaball mother is globally hidden.

Report any issues [here](https://github.com/GitSauce2/blender_selective_motion_blur/issues)

## License
This addon's code derives from Blender's Source Code and is licensed under the GNU General Public License v3.0.