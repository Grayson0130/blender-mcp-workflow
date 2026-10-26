# 模型导入（Unity assetbundle → Blender）

## 步骤
1. 用 UnityPy 提取 mesh 为 OBJ：
   ```python
   import UnityPy
   env = UnityPy.load("model.assetbundle")
   for o in env.objects:
       if o.type.name == "Mesh":
           open(f"{o.read().m_Name}.obj","w").write(o.read().export())
   ```
2. 提取贴图：
   ```python
   for o in env.objects:
       if o.type.name == "Texture2D":
           o.read().image.save(f"{o.read().m_Name}.png")
   ```
3. Blender 导入：
   ```python
   bpy.ops.wm.obj_import(filepath="model.obj")
   ```
4. 创建材质并连接贴图节点。

详见 scripts/extract_full.py, build_textured.py
