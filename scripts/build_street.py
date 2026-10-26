import bpy, random
random.seed(42)
bpy.ops.wm.read_homefile(use_empty=True)

# Ground
bpy.ops.mesh.primitive_plane_add(size=1, location=(0,0,0))
ground = bpy.context.active_object
ground.name = "Ground"
ground.scale = (30, 8, 1)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Buildings along both sides
for side in (-1, 1):
    for i in range(8):
        x = -12 + i*3.5
        w = random.uniform(1.5, 3.0)
        d = random.uniform(1.5, 2.5)
        h = random.uniform(3, 7)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, side*(4 + d/2), h/2))
        b = bpy.context.active_object
        b.name = f"Building_{side}_{i}"
        b.scale = (w, d, h)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Tank (reuse parts)
def add_cube(name, loc, scale):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.active_object
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return o

def add_cyl(name, loc, radius, depth, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=loc)
    o = bpy.context.active_object
    o.name = name
    o.rotation_euler = rot
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    return o

# Tank parent empty for animation
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(-10, 0, 0.3))
tank = bpy.context.active_object
tank.name = "Tank"

# Hull
hull = add_cube("Hull", (0,0,0), (2,1,0.6))
hull.parent = tank
# Turret
turret = add_cyl("Turret", (0,0,0.6), 0.5, 0.4, (0,0,0))
turret.parent = tank
# Barrel
barrel = add_cyl("Barrel", (1.2,0,0.6), 0.1, 2.0, (0,1.5708,0))
barrel.parent = tank
# Tracks
for side, y in [("L",-0.7), ("R",0.7)]:
    tr = add_cube(f"Track_{side}", (-0.9, y, 0.15-0.3), (1.8,0.25,0.3))
    tr.parent = tank
# Wheels
for side, y in [("L",-0.7), ("R",0.7)]:
    for i in range(4):
        w = add_cyl(f"Wheel_{side}{i}", (-1.2+i*0.8, y, 0.15-0.3), 0.25, 0.2, (1.5708,0,0))
        w.parent = tank

# Animate tank along X: -10 to 10 over 120 frames (5s @24fps)
tank.location = (-10, 0, 0.3)
tank.keyframe_insert(data_path="location", frame=1)
tank.location = (10, 0, 0.3)
tank.keyframe_insert(data_path="location", frame=120)

# Camera 1: side view, frames 0-60
bpy.ops.object.camera_add(location=(0, -8, 3))
cam1 = bpy.context.active_object
cam1.name = "Camera1"
cam1.rotation_euler = (1.3, 0, 0)
# Camera 2: front-ish view, frames 60-120
bpy.ops.object.camera_add(location=(8, -6, 4))
cam2 = bpy.context.active_object
cam2.name = "Camera2"
cam2.rotation_euler = (1.2, 0, 0.9)

# Camera switching via markers
bpy.context.scene.camera = cam1
# Add marker at frame 60 bound to cam2
bpy.context.scene.frame_set(60)
marker = bpy.context.scene.timeline_markers.new("cut", frame=60)
marker.camera = cam2

# Light
bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))

# Viewport shading
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type == 'VIEW_3D':
            for sp in area.spaces:
                if sp.type == 'VIEW_3D':
                    sp.shading.type = 'MATERIAL'

bpy.ops.wm.save_as_mainfile(filepath="D:/ZCode/street_tank.blend")
print("SAVED street_tank.blend")
