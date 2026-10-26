import UnityPy, os, json, re
env = UnityPy.load("D:/vam1.22.1/vam1.22.1.0/Custom/Assets/MeshedVR/car_sedan.assetbundle")
by_id = {o.path_id: o for o in env.objects}

mesh_to_go = {}
for o in env.objects:
    if o.type.name == "MeshFilter":
        d = o.read()
        mesh_to_go[d.m_Mesh.m_PathID] = d.m_GameObject.m_PathID

go_to_mats = {}
for o in env.objects:
    if o.type.name == "MeshRenderer":
        d = o.read()
        go_to_mats[d.m_GameObject.m_PathID] = [m.m_PathID for m in d.m_Materials]

def safe(s): return re.sub(r'[^A-Za-z0-9_\-]', '_', s)

# Export textures
tex_files = {}
for o in env.objects:
    if o.type.name == "Texture2D":
        d = o.read()
        name = safe(d.m_Name)
        path = f"D:/ZCode/car_textures/{name}.png"
        d.image.save(path)
        tex_files[o.path_id] = name
        print("tex:", name, d.m_Width, "x", d.m_Height)

# For each mesh, export OBJ + record texture
mapping = {}
for o in env.objects:
    if o.type.name != "Mesh":
        continue
    d = o.read()
    mesh_name = safe(d.m_Name)
    go = mesh_to_go.get(o.path_id)
    mats = go_to_mats.get(go, [])
    main_tex_name = None
    if mats:
        mo = by_id.get(mats[0])
        if mo:
            md = mo.read()
            for tname, te in md.m_SavedProperties.m_TexEnvs:
                if tname == "_MainTex" and te.m_Texture.m_PathID != 0:
                    to = by_id.get(te.m_Texture.m_PathID)
                    if to:
                        main_tex_name = tex_files.get(to.path_id)
    # export mesh
    obj_path = f"D:/ZCode/car_parts/{mesh_name}.obj"
    with open(obj_path, "w") as f:
        f.write(d.export())
    mapping[mesh_name] = main_tex_name
    print("mesh:", mesh_name, "->", main_tex_name)

with open("D:/ZCode/car_parts/mapping.json", "w") as f:
    json.dump(mapping, f, indent=2)
print("DONE")
