# Blender MCP 工作流

本仓库记录在 Windows 上通过 MCP 驱动 Blender 的操作脚本与说明，包括：
- 程序启动（Blender + MCP 桥接）
- 模型导入（Unity assetbundle → OBJ → Blender，含贴图）
- 模型清理
- 材质/贴图处理

## 环境
- Blender 5.1.2（`C:\Program Files\Blender Foundation\Blender 5.1\`）
- Python 3.14 + `blender-mcp` 1.0.0（MCP 客户端）
- MCP 桥接端口：5000（9876 被 Windows 保留端口范围占用）

## 目录
- `scripts/`：Python 脚本
- `docs/`：操作说明

## 快速开始
1. 启动 Blender GUI（自动启动 MCP 桥接）：
   ```
   "C:\Program Files\Blender Foundation\Blender 5.1\blender.exe" --online-mode <file.blend>
   ```
2. MCP 客户端连接 `localhost:5000`。
3. 导入模型见 `docs/import.md`。

详见 docs。
