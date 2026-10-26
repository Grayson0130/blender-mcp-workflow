using System;
using System.IO;
using System.Net;
using System.Text;
using System.Threading;
using BepInEx;
using UnityEngine;

namespace VaMMcpBridge
{
    [BepInPlugin("com.grayson.vammcpbridge", "VaM MCP Bridge", "0.1.0")]
    public class VaMMcpBridge : BaseUnityPlugin
    {
        private HttpListener listener;
        private Thread thread;
        private const int Port = 8099;
        private const string ExportDir = @"D:\ZCode\vam_export";

        void Awake()
        {
            Directory.CreateDirectory(ExportDir);
            listener = new HttpListener();
            listener.Prefixes.Add("http://127.0.0.1:" + Port.ToString() + "/");
            listener.Start();
            thread = new Thread(ListenLoop) { IsBackground = true };
            thread.Start();
            Logger.LogInfo("VaM MCP Bridge listening on port " + Port.ToString());
        }

        void OnDestroy()
        {
            try { listener.Stop(); } catch { }
        }

        void ListenLoop()
        {
            while (listener.IsListening)
            {
                try
                {
                    var ctx = listener.GetContext();
                    Handle(ctx);
                }
                catch { }
            }
        }

        void Handle(HttpListenerContext ctx)
        {
            string path = ctx.Request.Url.AbsolutePath.ToLowerInvariant();
            string response = "{}";
            if (path == "/status")
            {
                response = "{\"status\":\"ok\"}";
            }
            else if (path == "/export")
            {
                // Export all meshes in the scene to OBJ files
                int count = 0;
                try
                {
                    var allFilters = UnityEngine.Object.FindObjectsOfType<MeshFilter>();
                    foreach (var mf in allFilters)
                    {
                        var mesh = mf.sharedMesh;
                        if (mesh == null) continue;
                        string name = mf.gameObject.name;
                        // sanitize
                        foreach (char c in Path.GetInvalidFileNameChars()) name = name.Replace(c, '_');
                        string outPath = Path.Combine(ExportDir, name + ".obj");
                        WriteObj(mesh, outPath);
                        count++;
                    }
                    response = "{\"exported\":" + count.ToString() + ",\"dir\":\""+ ExportDir.Replace("\\","\\\\") + "\"}";
                }
                catch (Exception e)
                {
                    response = "{\"error\":\""+ e.Message.Replace("\"", "'") + "\"}";
                }
            }
            else
            {
                response = "{\"error\":\"unknown endpoint\"}";
            }
            var bytes = Encoding.UTF8.GetBytes(response);
            ctx.Response.ContentType = "application/json";
            ctx.Response.OutputStream.Write(bytes, 0, bytes.Length);
            ctx.Response.Close();
        }

        static void WriteObj(Mesh mesh, string path)
        {
            using (var w = new StreamWriter(path))
            {
                w.WriteLine("# exported by VaM MCP Bridge");
                foreach (var v in mesh.vertices)
                    w.WriteLine("v " + v.x + " " + v.y + " " + v.z);
                foreach (var n in mesh.normals)
                    w.WriteLine("vn " + n.x + " " + n.y + " " + n.z);
                foreach (var uv in mesh.uv)
                    w.WriteLine("vt " + uv.x + " " + uv.y);
                for (int i = 0; i < mesh.triangles.Length; i += 3)
                {
                    int a = mesh.triangles[i] + 1;
                    int b = mesh.triangles[i + 1] + 1;
                    int c = mesh.triangles[i + 2] + 1;
                    w.WriteLine("f " + a + "/" + a + "/" + a + " " + b + "/" + b + "/" + b + " " + c + "/" + c + "/" + c);
                }
            }
        }
    }
}
