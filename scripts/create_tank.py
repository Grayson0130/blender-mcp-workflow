# Tank white model creation via Blender MCP bridge
# Run this in Blender (factory startup or via bridge)
import bpy

# Clear scene
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)

# Hull
bpy.ops.mesh.primitive_cube_add(size=1, location=(0,0,0.3))
hull = bpy.context.active_object
hull.name = "Hull"
hull.scale = (2.0, 1.0, 0.6)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Turret
bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=0.4, location=(0,0,0.9))
turret = bpy.context.active_object
turret.name = "Turret"

# Barrel
bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=2.0, location=(1.2,0,0.9))
barrel = bpy.context.active_object
barrel.name = "Barrel"
barrel.rotation_euler = (0, 1.5708, 0)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

# Tracks
for side, y in [("L", -0.7), ("R", 0.7)]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.9, y, 0.15))
    t = bpy.context.active_object
    t.name = f"Track_{side}"
    t.scale = (1.8, 0.25, 0.3)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Wheels
for side, y in [("L", -0.7), ("R", 0.7)]:
    for i in range(4):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=0.2, location=(-1.2 + i*0.8, y, 0.15))
        w = bpy.context.active_object
        w.name = f"Wheel_{side}{i}"
        w.rotation_euler = (1.5708, 0, 0)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

# Camera
bpy.ops.object.camera_add(location=(6, -6, 4))
cam = bpy.context.active_object
cam.rotation_euler = (1.1, 0, 0.785)
bpy.context.scene.camera = cam

# Light
bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))

# Viewport shading
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type == 'VIEW_3D':
            for sp in area.spaces:
                if sp.type == 'VIEW_3D':
                    sp.shading.type = 'MATERIAL'

bpy.ops.wm.save_as_mainfile(filepath="D:/ZCode/tank.blend")
print("SAVED tank.blend")
