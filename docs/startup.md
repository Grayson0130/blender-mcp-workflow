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

## 局域网访问（LAN）

为了让局域网其他设备通过 MCP 操作本机 Blender：

1. 桥接监听地址改为 `0.0.0.0`（已修改 `DEFAULT_HOST` 和 `bg_server.py`）
2. 防火墙放行端口 5000（已添加规则 `Blender MCP 5000`）
3. 其他设备的 MCP 客户端配置：
   ```json
   {
     "mcp": {
       "servers": {
         "blender": {
           "type": "stdio",
           "command": "python",
           "args": ["-m", "blmcp"],
           "enabled": true,
           "env": {
             "BLENDER_MCP_HOST": "192.168.66.86",
             "BLENDER_MCP_PORT": "5000"
           }
         }
       }
     }
   }
   ```
   （将 `192.168.66.86` 替换为本机实际 LAN IP）
4. 其他设备需安装 `blender-mcp` Python 包（`pip install blender-mcp`）

### 本机 LAN IP
- `192.168.66.86`（主局域网）
- `10.0.1.1` / `100.77.2.100`（其他接口）
