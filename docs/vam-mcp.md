# VaM MCP Bridge (BepInEx 插件)

## 安装
将 `plugins/VaMMcpBridge/VaMMcpBridge.dll` 复制到：
`D:\vam1.22.1\vam1.22.1.0\BepInEx\plugins\`

启动 VaM 后，插件在端口 8099 启动 HTTP 服务。

## 端点
- `GET /status` → `{"status":"ok"}`
- `GET /export` → 导出场景中所有 MeshFilter 的 mesh 为 OBJ 到 `D:\ZCode\vam_export\`，返回 `{"exported":N,"dir":"..."}`

## 使用
ZCode 可通过 HTTP 调用 `http://127.0.0.1:8099/export` 触发导出，然后用 Blender 导入生成的 OBJ。

## 编译
```
C:\Windows\Microsoft.NET\Framework\v3.5\csc.exe /target:library /out:VaMMcpBridge.dll VaMMcpBridge.cs \
  /reference:...\BepInEx.dll /reference:...\UnityEngine.dll \
  /reference:...\UnityEngine.CoreModule.dll /reference:...\Assembly-CSharp.dll
```
