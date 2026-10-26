import bpy
bpy.ops.wm.read_homefile(use_empty=True)
bpy.ops.import_scene.gltf(filepath="D:/ZCode/models/RobotExpressive.glb")
for o in list(bpy.context.scene.objects):
    if o.name == "Icosphere":
        bpy.data.objects.remove(o, do_unlink=True)
arm = None
for o in bpy.context.scene.objects:
    if o.type == 'ARMATURE':
        arm = o
        break
if not arm.animation_data:
    arm.animation_data_create()
arm.animation_data.action = None
sequence = ["Idle", "Walking", "Running", "Punch", "Jump", "Sitting", "Death"]
track = arm.animation_data.nla_tracks.new()
track.name = "ActionSequence"
t = 0
for name in sequence:
    action = bpy.data.actions.get(name)
    if action:
        strip = track.strips.new(name, t, action)
        strip.repeat = 1.0
        length = action.frame_range[1] - action.frame_range[0]
        t += int(length) + 1
        print(f"added {name} at {strip.frame_start}, len {length}")
scn = bpy.context.scene
scn.frame_start = 0
scn.frame_end = t
bpy.ops.object.camera_add(location=(4, -4, 2))
cam = bpy.context.active_object
cam.rotation_euler = (1.2, 0, 0.785)
scn.camera = cam
bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type == 'VIEW_3D':
            for sp in area.spaces:
                if sp.type == 'VIEW_3D':
                    sp.shading.type = 'MATERIAL'
arm.hide_set(True)
arm.hide_viewport = True
bpy.ops.wm.save_as_mainfile(filepath="D:/ZCode/robot_sequence.blend")
print("SAVED, total frames:", t)
