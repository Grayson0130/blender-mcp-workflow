import UnityPy, os
results = []
# scan assetbundles
for root,_,files in os.walk("D:/vam1.22.1"):
    for f in files:
        if not f.endswith(".assetbundle"): continue
        p = os.path.join(root,f)
        try:
            env = UnityPy.load(p)
        except Exception:
            continue
        for o in env.objects:
            if o.type.name != "Mesh": continue
            d = o.read()
            try:
                vc = len(d.m_Vertices) if hasattr(d,'m_Vertices') and d.m_Vertices else 0
            except Exception:
                vc = 0
            if vc >= 5000:
                results.append((vc, p, d.m_Name))
# also scan sharedassets
for i in range(8):
    p = f"D:/vam1.22.1/vam1.22.1.0/VaM_Data/sharedassets{i}.assets"
    try:
        env = UnityPy.load(p)
    except Exception:
        continue
    for o in env.objects:
        if o.type.name != "Mesh": continue
        d = o.read()
        try:
            vc = len(d.m_Vertices) if hasattr(d,'m_Vertices') and d.m_Vertices else 0
        except Exception:
            vc = 0
        if vc >= 5000:
            results.append((vc, p, d.m_Name))
results.sort(reverse=True)
print("top meshes by vertex count:")
for vc,p,name in results[:20]:
    print(f"{vc:6d}  {name}  ({p})")
