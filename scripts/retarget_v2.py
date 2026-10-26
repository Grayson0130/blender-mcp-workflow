import bpy
bpy.ops.wm.read_homefile(use_empty=True)

# Import Xbot
bpy.ops.import_scene.gltf(filepath="D:/ZCode/models/Xbot.glb")
xbot_arm = None
for o in bpy.context.scene.objects:
    if o.type=='ARMATURE' and 'Armature' in o.name:
        xbot_arm = o
        break
# Import RobotExpressive
bpy.ops.import_scene.gltf(filepath="D:/ZCode/models/RobotExpressive.glb")
robot_arm = None
for o in bpy.context.scene.objects:
    if o.type=='ARMATURE' and 'RobotArmature' in o.name:
        robot_arm = o
        break

print("Xbot scale:", xbot_arm.scale, "Robot scale:", robot_arm.scale)

bone_map = {
    "Hips": "mixamorig:Hips",
    "Abdomen": "mixamorig:Spine",
    "Torso": "mixamorig:Spine1",
    "Neck": "mixamorig:Neck",
    "Head": "mixamorig:Head",
    "Shoulder.L": "mixamorig:LeftShoulder",
    "UpperArm.L": "mixamorig:LeftArm",
    "LowerArm.L": "mixamorig:LeftForeArm",
    "Palm2.L": "mixamorig:LeftHand",
    "UpperLeg.L": "mixamorig:LeftUpLeg",
    "LowerLeg.L": "mixamorig:LeftLeg",
    "Foot.L": "mixamorig:LeftFoot",
    "Shoulder.R": "mixamorig:RightShoulder",
    "UpperArm.R": "mixamorig:RightArm",
    "LowerArm.R": "mixamorig:RightForeArm",
    "Palm2.R": "mixamorig:RightHand",
    "UpperLeg.R": "mixamorig:RightUpLeg",
    "LowerLeg.R": "mixamorig:RightLeg",
    "Foot.R": "mixamorig:RightFoot",
}

# Set robot action to Punch
punch_action = bpy.data.actions.get("Punch")
if punch_action:
    if not robot_arm.animation_data:
        robot_arm.animation_data_create()
    robot_arm.animation_data.action = punch_action

# Add constraints (world space) on Xbot bones
for src, dst in bone_map.items():
    if src not in robot_arm.data.bones or dst not in xbot_arm.data.bones:
        continue
    pb = xbot_arm.pose.bones[dst]
    c = pb.constraints.new('COPY_ROTATION')
    c.target = robot_arm
    c.subtarget = src
    c.target_space = 'WORLD'
    c.owner_space = 'WORLD'
# Copy location for root
pb = xbot_arm.pose.bones["mixamorig:Hips"]
c = pb.constraints.new('COPY_LOCATION')
c.target = robot_arm
c.subtarget = "Hips"
c.target_space = 'WORLD'
c.owner_space = 'WORLD'

# Bake
bpy.context.view_layer.objects.active = xbot_arm
bpy.ops.object.mode_set(mode='POSE')
frame_start = int(punch_action.frame_range[0])
frame_end = int(punch_action.frame_range[1])
bpy.ops.nla.bake(frame_start=frame_start, frame_end=frame_end, step=1, only_selected=False, visual_keying=True, clear_constraints=True, bake_types={'POSE'})
print("baked punch")
bpy.ops.object.mode_set(mode='OBJECT')

# Remove RobotExpressive objects to clean scene
for o in list(bpy.context.scene.objects):
    if o.name.startswith(('RootNode','RobotArmature','Foot.','Torso','Head','Shoulder','UpperArm','LowerArm','Palm','Middle','Thumb','Index','Ring','UpperLeg','LowerLeg','PoleTarget','Foot.')):
        bpy.data.objects.remove(o, do_unlink=True)
# also remove empties/icosphere from robot
for o in list(bpy.context.scene.objects):
    if o.type == 'EMPTY' and o.name.endswith('_end'):
        bpy.data.objects.remove(o, do_unlink=True)

# hide armature
xbot_arm.hide_set(True)
xbot_arm.hide_viewport = True

# camera
bpy.ops.object.camera_add(location=(2.5, -2.5, 1.5))
cam = bpy.context.active_object
cam.rotation_euler = (1.2, 0, 0.785)
bpy.context.scene.camera = cam
# light
bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))

bpy.ops.wm.save_as_mainfile(filepath="D:/ZCode/xbot_punch_v2.blend")
print("SAVED xbot_punch_v2.blend")
print("remaining objects:", [o.name for o in bpy.context.scene.objects])
