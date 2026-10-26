import bpy, os
bpy.ops.wm.open_mainfile(filepath="D:/ZCode/car_sedan.blend")
# Add camera
bpy.ops.object.camera_add(location=(8, -8, 5))
cam = bpy.context.active_object
cam.rotation_euler = (1.0, 0.0, 0.785)
bpy.context.scene.camera = cam
# Add sun light
bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
sun = bpy.context.active_object
sun.data.energy = 3.0
# Render settings
scn = bpy.context.scene
scn.render.filepath = "D:/ZCode/car_sedan_render.png"
scn.render.resolution_x = 1920
scn.render.resolution_y = 1080
scn.render.image_settings.file_format = 'PNG'
bpy.ops.render.render(write_still=True)
print("RENDER_DONE ->", scn.render.filepath)
