import socket, json, time
code = '''
import bpy
bpy.ops.wm.read_homefile(use_empty=True)
ret = bpy.ops.wm.obj_import(filepath="D:/ZCode/car_sedan.obj")
print("IMPORT_RESULT", ret)

bpy.ops.wm.save_as_mainfile(filepath="D:/ZCode/car_sedan.blend")
print("SAVED")
'''
req = {"type": "execute", "code": code, "strict_json": False}
s = socket.create_connection(("127.0.0.1", 9876), timeout=10)
s.sendall((json.dumps(req) + "\x00").encode())
# wait for response
buf = b""
deadline = time.time() + 60
while time.time() < deadline:
    try:
        s.settimeout(1)
        chunk = s.recv(4096)
        if not chunk:
            break
        buf += chunk
        if b"\x00" in buf:
            break
    except socket.timeout:
        continue
s.close()
print("=== RESPONSE ===")
print(buf.decode(errors="replace"))
