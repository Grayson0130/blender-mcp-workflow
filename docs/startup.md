# Blender + MCP 启动

## 安装 MCP 客户端
```
pip install "C:/Users/Administrator/AppData/Local/uv/cache/sdists-v9/git/00fd2c7999a3b96c/03004fd0216bfe5e/blender_mcp-1.0.0-py3-none-any.whl"
pip install "mcp>=1.2.0,<2"
```

## ZCode MCP 配置（config.json）
```json
{
  "mcp": {
    "servers": {
      "blender": {
        "type": "stdio",
        "command": "C:/Python314/python.exe",
        "args": ["-m", "blmcp"],
        "enabled": true,
        "timeoutMs": 60000,
        "env": {"BLENDER_MCP_HOST": "localhost", "BLENDER_MCP_PORT": "5000"}
      }
    }
  }
}
```

## 启动 Blender GUI（桥接自动启动）
```
"C:\Program Files\Blender Foundation\Blender 5.1\blender.exe" --online-mode <file.blend>
```
端口 5000 监听即表示桥接就绪。

## 注意
- 9876 被 Windows 保留端口范围占用，使用 5000
- blmcp 插件需在用户偏好中启用
- 启动脚本 `blender_mcp_bg_server.py` 仅在 background 模式运行阻塞循环
