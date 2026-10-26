import UnityPy
env = UnityPy.load("D:/vam1.22.1/vam1.22.1.0/Custom/Assets/MeshedVR/car_sedan.assetbundle")

# index by path_id
by_id = {o.path_id: o for o in env.objects}

# map mesh path_id -> gameobject path_id (via MeshFilter)
mesh_to_go = {}
for o in env.objects:
    if o.type.name == "MeshFilter":
        d = o.read()
        mesh_pptr = d.m_Mesh
        go_pptr = d.m_GameObject
        mesh_to_go[mesh_pptr.m_PathID] = go_pptr.m_PathID

# map gameobject -> list of material path_ids (via MeshRenderer)
go_to_mats = {}
for o in env.objects:
    if o.type.name == "MeshRenderer":
        d = o.read()
        go_pptr = d.m_GameObject
        mats = [m.m_PathID for m in d.m_Materials]
        go_to_mats[go_pptr.m_PathID] = mats

# now for each Mesh, find material
for o in env.objects:
    if o.type.name == "Mesh":
        d = o.read()
        go = mesh_to_go.get(o.path_id)
        mats = go_to_mats.get(go, [])
        mat_names = []
        for mid in mats:
            mo = by_id.get(mid)
            if mo:
                mat_names.append(mo.read().m_Name)
        # get main tex from first material
        main_tex = None
        if mats:
            mo = by_id.get(mats[0])
            if mo:
                md = mo.read()
                for name, te in md.m_SavedProperties.m_TexEnvs:
                    if name == "_MainTex" and te.m_Texture.m_PathID != 0:
                        to = by_id.get(te.m_Texture.m_PathID)
                        main_tex = to.read().m_Name if to else None
        print(f"Mesh {d.m_Name}: mats={mat_names}, mainTex={main_tex}")
