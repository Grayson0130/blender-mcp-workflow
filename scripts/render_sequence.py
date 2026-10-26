import bpy
bpy.ops.wm.open_mainfile(filepath="D:/ZCode/robot_sequence.blend")
scn = bpy.context.scene
scn.frame_start = 0
scn.frame_end = 202
scn.render.filepath = "D:/ZCode/seq_"
scn.render.resolution_x = 1280
scn.render.resolution_y = 720
scn.render.image_settings.file_format = 'PNG'
bpy.ops.render.render(animation=True)
print("RENDER_DONE")
