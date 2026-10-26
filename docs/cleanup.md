# 模型清理

- 删除场景所有 mesh 对象：在 Blender 中 Select All → Delete
- 或加载空 blend 文件：`bpy.ops.wm.read_homefile(use_empty=True)`
- 清理未使用的数据块：`bpy.ops.outliner.orphans_purge()`
