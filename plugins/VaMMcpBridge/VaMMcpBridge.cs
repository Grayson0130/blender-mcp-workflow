using System;
using System.Collections;
using System.IO;
using System.Net;
using System.Reflection;
using System.Text;
using System.Threading;
using System.Collections.Generic;
using BepInEx;
using UnityEngine;

namespace VaMMcpBridge
{
    [BepInPlugin("com.grayson.vammcpbridge", "VaM MCP Bridge", "0.2.0")]
    public class VaMMcpBridge : BaseUnityPlugin
    {
        private HttpListener listener;
        private Thread thread;
        private const int Port = 8099;
        private const string ExportDir = @"D:\ZCode\vam_export";
        private const string LogFile = @"D:\ZCode\vam_bridge.log";
        private readonly List<Action> pending = new List<Action>();
        private readonly object plock = new object();

        void Log(string msg)
        {
            try { File.AppendAllText(LogFile, DateTime.Now.ToString("HH:mm:ss") + " " + msg + "\n"); } catch { }
        }

        void Awake()
        {
            Directory.CreateDirectory(ExportDir);
            listener = new HttpListener();
            listener.Prefixes.Add("http://127.0.0.1:" + Port.ToString() + "/");
            listener.Start();
            thread = new Thread(ListenLoop) { IsBackground = true };
            thread.Start();
            Log("Bridge started on port " + Port);
        }

        void Update()
        {
            List<Action> batch = null;
            lock (plock) { if (pending.Count > 0) { batch = new List<Action>(pending); pending.Clear(); } }
            if (batch != null) foreach (var a in batch) { try { a(); } catch (Exception e) { Log("Update action error: " + e.Message); } }
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
                catch (Exception e) { Log("Listen error: " + e.Message); }
            }
        }

        Type FindType(string name)
        {
            foreach (var asm in AppDomain.CurrentDomain.GetAssemblies())
            {
                try
                {
                    var t = asm.GetType(name);
                    if (t != null) return t;
                    foreach (var tt in asm.GetTypes())
                    {
                        if (tt.Name == name) return tt;
                    }
                }
                catch { }
            }
            return null;
        }

        object GetSuperController()
        {
            var t = FindType("SuperController");
            if (t == null) { Log("SuperController type not found"); return null; }
            var field = t.GetField("singleton", BindingFlags.Public | BindingFlags.Static);
            if (field != null) return field.GetValue(null);
            var m = typeof(UnityEngine.Object).GetMethod("FindObjectOfType", new Type[] { typeof(Type) });
            return m.Invoke(null, new object[] { t });
        }

        T RunOnMainThread<T>(Func<T> func)
        {
            T result = default(T);
            var done = new ManualResetEvent(false);
            lock (plock) { pending.Add(() => { try { result = func(); } catch (Exception e) { Log("mainthread error: " + e.Message); } done.Set(); }); }
            done.WaitOne(5000);
            return result;
        }

        string ListAtoms()
        {
            var sc = GetSuperController();
            if (sc == null) return "{\"error\":\"no SuperController\"}";
            var t = sc.GetType();
            var m = t.GetMethod("GetAtoms", BindingFlags.Public | BindingFlags.Instance | BindingFlags.NonPublic);
            IEnumerable r = null;
            if (m != null) r = m.Invoke(sc, null) as IEnumerable;
            if (r == null)
            {
                var f = t.GetField("atoms", BindingFlags.Public | BindingFlags.Instance | BindingFlags.NonPublic);
                if (f != null) r = f.GetValue(sc) as IEnumerable;
            }
            if (r == null) return "{\"error\":\"no atoms accessor\"}";
            var sb = new StringBuilder("[");
            bool first = true;
            foreach (var a in r)
            {
                if (!first) sb.Append(",");
                first = false;
                var at = a.GetType();
                var uidField = at.GetField("uid") ?? at.GetField("name") ?? at.GetField("atomName");
                string val = uidField != null ? uidField.GetValue(a).ToString() : a.ToString();
                sb.Append("\"" + val.Replace("\"", "'") + "\"");
            }
            sb.Append("]");
            return "{\"atoms\":" + sb.ToString() + "}";
        }

        string GetCategories()
        {
            var sc = GetSuperController();
            if (sc == null) return "{\"error\":\"no SuperController\"}";
            var t = sc.GetType();
            var m = t.GetMethod("GetAtomCategories", BindingFlags.Public | BindingFlags.Instance | BindingFlags.NonPublic);
            if (m == null) return "{\"error\":\"GetAtomCategories not found\"}";
            try
            {
                var r = m.Invoke(sc, null);
                if (r is IEnumerable)
                {
                    var sb = new StringBuilder("[");
                    bool first = true;
                    foreach (var c in (IEnumerable)r)
                    {
                        if (!first) sb.Append(",");
                        first = false;
                        sb.Append("\"" + c.ToString().Replace("\"", "'") + "\"");
                    }
                    sb.Append("]");
                    return "{\"categories\":" + sb.ToString() + "}";
                }
                return "{\"categories\":\"" + (r == null ? "null" : r.ToString().Replace("\"", "'")) + "\"}";
            }
            catch (Exception e) { return "{\"error\":\"" + e.Message.Replace("\"", "'") + "\"}"; }
        }

        string AddAtom(string type)
        {
            var sc = GetSuperController();
            if (sc == null) return "{\"error\":\"no SuperController\"}";
            var t = sc.GetType();
            foreach (var name in new string[] { "AddAtomByTypeForceSelect", "AddAtomByType" })
            {
                MethodInfo m = null;
                foreach (var cand in t.GetMethods(BindingFlags.Public | BindingFlags.Instance | BindingFlags.NonPublic))
                {
                    if (cand.Name == name) { m = cand; break; }
                }
                if (m == null) continue;
                var ps = m.GetParameters();
                Log("AddAtom method: " + name + " params=" + ps.Length);
                foreach (var pp in ps) Log("  param: " + pp.Name + " : " + pp.ParameterType.FullName);
                try
                {
                    object[] args;
                    if (ps.Length == 1) args = new object[] { type };
                    else if (ps.Length == 2) args = new object[] { type, true };
                    else if (ps.Length == 4) args = new object[] { type, true, true, true };
                    else args = new object[ps.Length];
                    var r = m.Invoke(sc, args);
                    return "{\"result\":\"" + (r == null ? "null" : r.ToString().Replace("\"", "'")) + "\"}";
                }
                catch (Exception e) { Log("AddAtom error: " + e.Message); return "{\"error\":\"" + e.Message.Replace("\"", "'") + "\"}"; }
            }
            return "{\"error\":\"AddAtomByType not found\"}";
        }

        void Handle(HttpListenerContext ctx)
        {
            string path = ctx.Request.Url.AbsolutePath.ToLowerInvariant();
            string query = ctx.Request.Url.Query;
            string response = "{}";
            try
            {
                if (path == "/status")
                {
                    response = "{\"status\":\"ok\"}";
                }
                else if (path == "/atoms")
                {
                    response = RunOnMainThread(() => ListAtoms());
                }
                else if (path == "/categories")
                {
                    response = RunOnMainThread(() => GetCategories());
                }
                else if (path == "/addatom")
                {
                    string type = "Person";
                    if (query.Contains("type="))
                    {
                        int i = query.IndexOf("type=") + 5;
                        int j = query.IndexOf("&", i);
                        if (j < 0) j = query.Length;
                        type = Uri.UnescapeDataString(query.Substring(i, j - i));
                    }
                    Log("addatom type=" + type);
                    response = RunOnMainThread(() => AddAtom(type));
                }
                else if (path == "/meshes")
                {
                    response = RunOnMainThread(() =>
                    {
                        var sb = new StringBuilder("[");
                        bool first = true;
                        foreach (var mf in UnityEngine.Object.FindObjectsOfType<MeshFilter>())
                        {
                            if (mf.sharedMesh == null) continue;
                            if (!first) sb.Append(",");
                            first = false;
                            sb.Append("{\"name\":\"" + mf.gameObject.name.Replace("\"", "'") + "\",\"type\":\"MeshFilter\",\"verts\":" + mf.sharedMesh.vertexCount.ToString() + "}");
                        }
                        foreach (var smr in Resources.FindObjectsOfTypeAll<SkinnedMeshRenderer>())
                        {
                            if (smr.sharedMesh == null) continue;
                            if (!first) sb.Append(",");
                            first = false;
                            sb.Append("{\"name\":\"" + smr.gameObject.name.Replace("\"", "'") + "\",\"type\":\"Skinned\",\"verts\":" + smr.sharedMesh.vertexCount.ToString() + "}");
                        }
                        sb.Append("]");
                        return sb.ToString();
                    });
                }
                else if (path == "/export")
                {
                    response = RunOnMainThread(() =>
                    {
                        int count = 0;
                        var allFilters = UnityEngine.Object.FindObjectsOfType<MeshFilter>();
                        foreach (var mf in allFilters)
                        {
                            var mesh = mf.sharedMesh;
                            if (mesh == null) continue;
                            string name = mf.gameObject.name;
                            foreach (char c in Path.GetInvalidFileNameChars()) name = name.Replace(c, '_');
                            string outPath = Path.Combine(ExportDir, name + ".obj");
                            WriteObj(mesh, outPath);
                            count++;
                        }
                        var allSkinned = Resources.FindObjectsOfTypeAll<SkinnedMeshRenderer>();
                        foreach (var smr in allSkinned)
                        {
                            var mesh = smr.sharedMesh;
                            if (mesh == null) continue;
                            string name = smr.gameObject.name + "_skinned";
                            foreach (char c in Path.GetInvalidFileNameChars()) name = name.Replace(c, '_');
                            string outPath = Path.Combine(ExportDir, name + ".obj");
                            WriteObj(mesh, outPath);
                            count++;
                        }
                        return "{\"exported\":" + count.ToString() + ",\"dir\":\""+ ExportDir.Replace("\\","\\\\") + "\"}";
                    });
                }
                else
                {
                    response = "{\"error\":\"unknown endpoint\"}";
                }
            }
            catch (Exception e)
            {
                Log("Handle error: " + e.Message);
                response = "{\"error\":\"" + e.Message.Replace("\"", "'") + "\"}";
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
