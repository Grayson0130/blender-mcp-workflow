import bpy
bpy.ops.wm.open_mainfile(filepath="D:/ZCode/xbot_punch_v2.blend")
keep = {"Armature", "Beta_Joints", "Beta_Surface", "Camera", "Sun"}
names = [o.name for o in bpy.context.scene.objects if o.name not in keep]
for n in names:
    o = bpy.data.objects.get(n)
    if o:
        bpy.data.objects.remove(o, do_unlink=True)
        print("removed", n)
arm = bpy.data.objects.get("Armature")
if arm:
    arm.hide_set(True)
    arm.hide_viewport = True
bpy.ops.wm.save_as_mainfile(filepath="D:/ZCode/xbot_punch_v2.blend")
print("SAVED")
