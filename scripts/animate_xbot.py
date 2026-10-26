import bpy
bpy.ops.wm.read_homefile(use_empty=True)
bpy.ops.import_scene.gltf(filepath="D:/ZCode/models/Xbot.glb")
arm = None
for o in bpy.context.scene.objects:
    if o.type == 'ARMATURE':
        arm = o
        break
action = bpy.data.actions.get('walk')
if action and arm:
    if not arm.animation_data:
        arm.animation_data_create()
    arm.animation_data.action = action
    print("set action:", action.name)
scn = bpy.context.scene
scn.frame_start = 0
scn.frame_end = 30
bpy.ops.object.camera_add(location=(4, -4, 2))
cam = bpy.context.active_object
cam.rotation_euler = (1.2, 0, 0.785)
scn.camera = cam
bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
scn.render.filepath = "D:/ZCode/xbot_walk_"
scn.render.resolution_x = 1280
scn.render.resolution_y = 720
scn.render.image_settings.file_format = 'PNG'
bpy.ops.render.render(animation=True)
print("RENDER_ANIM_DONE")
