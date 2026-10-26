import bpy, os, json, glob
bpy.ops.wm.read_homefile(use_empty=True)

mapping = json.load(open("D:/ZCode/car_parts/mapping.json"))

for mesh_name, tex_name in mapping.items():
    obj_path = f"D:/ZCode/car_parts/{mesh_name}.obj"
    if not os.path.exists(obj_path):
        continue
    bpy.ops.wm.obj_import(filepath=obj_path)
    # imported objects are selected; get active
    obj = bpy.context.active_object
    if obj is None:
        # fallback: last mesh object
        objs = [o for o in bpy.context.scene.objects if o.type=='MESH']
        obj = objs[-1]
    # create material
    mat = bpy.data.materials.new(name=mesh_name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    tex_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
    if tex_name:
        img_path = f"D:/ZCode/car_textures/{tex_name}.png"
        if os.path.exists(img_path):
            img = bpy.data.images.load(img_path)
            tex_node.image = img
    # connect
    mat.node_tree.links.new(tex_node.outputs["Color"], bsdf.inputs["Base Color"])
    # assign
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

# set viewport shading to material preview
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'MATERIAL'

bpy.ops.wm.save_as_mainfile(filepath="D:/ZCode/car_sedan_textured.blend")
print("SAVED textured blend")
