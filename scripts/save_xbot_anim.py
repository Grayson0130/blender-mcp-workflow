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
bpy.ops.wm.save_as_mainfile(filepath="D:/ZCode/xbot_walk.blend")
print("SAVED xbot_walk.blend")
