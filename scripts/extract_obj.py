import UnityPy, re
env = UnityPy.load("D:/vam1.22.1/vam1.22.1.0/Custom/Assets/MeshedVR/car_sedan.assetbundle")
out = "D:/ZCode/car_sedan.obj"
all_v = []
all_f = []
mesh_count = 0
for o in env.objects:
    if o.type.name != "Mesh":
        continue
    d = o.read()
    s = d.export()
    # parse
    verts = []
    faces = []
    for line in s.splitlines():
        if line.startswith("v "):
            verts.append(line)
        elif line.startswith("f "):
            faces.append(line)
    if not verts:
        continue
    mesh_count += 1
    v0 = len(all_v)
    all_v.extend(verts)
    for f in faces:
        # adjust indices
        parts = f.split()
        new = ["f"]
        for p in parts[1:]:
            # p may be like "1" or "1/2/3"
            idx = p.split("/")[0]
            new.append(str(int(idx) + v0))
            # keep tex/normal if present
            if "/" in p:
                rest = p.split("/", 1)[1]
                new[-1] = new[-1] + "/" + rest
        all_f.append(" ".join(new))

with open(out, "w") as fh:
    fh.write("# car_sedan extracted from VaM assetbundle\n")
    for v in all_v:
        fh.write(v + "\n")
    for f in all_f:
        fh.write(f + "\n")
print("meshes:", mesh_count, "verts:", len(all_v), "faces:", len(all_f))
print("written:", out)
