using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Security.Cryptography;
using System.Text;
using System.Threading;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;

namespace CreativeAdapters.UnityBridge
{
    [InitializeOnLoad]
    public static class CreativeAdapterBridge
    {
        private const int MaxBodyBytes = 1024 * 1024;
        private const string SessionName = "unity";
        private const string Host = "127.0.0.1";

        private static readonly ConcurrentQueue<EvalTask> Tasks = new ConcurrentQueue<EvalTask>();
        private static TcpListener _listener;
        private static Thread _thread;
        private static string _token;
        private static bool _started;

        static CreativeAdapterBridge()
        {
            EditorApplication.delayCall += Start;
            EditorApplication.update += ProcessTasks;
            AssemblyReloadEvents.beforeAssemblyReload += Stop;
            EditorApplication.quitting += Stop;
        }

        private static void Start()
        {
            if (_started)
            {
                return;
            }

            _token = GenerateToken();
            _listener = new TcpListener(IPAddress.Loopback, 0);
            _listener.Start();

            int port = ((IPEndPoint)_listener.LocalEndpoint).Port;
            WriteSessionFile(port);

            _thread = new Thread(ServerLoop)
            {
                IsBackground = true,
                Name = "Creative Adapter Unity Bridge"
            };
            _thread.Start();
            _started = true;

            Debug.Log("Creative Adapter Bridge listening on 127.0.0.1:" + port);
        }

        private static void Stop()
        {
            RemoveSessionFile();
            try { _listener?.Stop(); } catch { }
            _listener = null;
            _started = false;
        }

        private static void ServerLoop()
        {
            while (_listener != null)
            {
                try
                {
                    using (TcpClient client = _listener.AcceptTcpClient())
                    {
                        HandleClient(client);
                    }
                }
                catch
                {
                    if (_listener == null)
                    {
                        return;
                    }
                }
            }
        }

        private static void HandleClient(TcpClient client)
        {
            client.ReceiveTimeout = 30000;
            client.SendTimeout = 30000;

            using (NetworkStream stream = client.GetStream())
            using (StreamReader reader = new StreamReader(stream, Encoding.UTF8, false, 1024, true))
            {
                string requestLine = reader.ReadLine();
                if (string.IsNullOrEmpty(requestLine))
                {
                    WriteResponse(stream, 400, JsonError("Empty request"));
                    return;
                }

                string[] parts = requestLine.Split(' ');
                string method = parts.Length > 0 ? parts[0] : "";
                string path = parts.Length > 1 ? parts[1] : "";

                Dictionary<string, string> headers = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
                string line;
                while (!string.IsNullOrEmpty(line = reader.ReadLine()))
                {
                    int colon = line.IndexOf(':');
                    if (colon > 0)
                    {
                        headers[line.Substring(0, colon).Trim()] = line.Substring(colon + 1).Trim();
                    }
                }

                if (method == "OPTIONS")
                {
                    WriteResponse(stream, 403, JsonError("CORS preflight is not supported."));
                    return;
                }

                if (method != "POST" || path != "/eval")
                {
                    WriteResponse(stream, 404, JsonError("Not found"));
                    return;
                }

                if (!headers.TryGetValue("X-Bridge-Token", out string token) || token != _token)
                {
                    WriteResponse(stream, 403, JsonError("Invalid bridge token"));
                    return;
                }

                int length = 0;
                if (!headers.TryGetValue("Content-Length", out string lengthText) ||
                    !int.TryParse(lengthText, out length) ||
                    length <= 0 ||
                    length > MaxBodyBytes)
                {
                    WriteResponse(stream, 413, JsonError("Invalid request size"));
                    return;
                }

                char[] bodyChars = new char[length];
                int offset = 0;
                while (offset < length)
                {
                    int count = reader.Read(bodyChars, offset, length - offset);
                    if (count <= 0)
                    {
                        break;
                    }
                    offset += count;
                }

                BridgeRequest request;
                try
                {
                    request = JsonUtility.FromJson<BridgeRequest>(new string(bodyChars, 0, offset));
                }
                catch (Exception ex)
                {
                    WriteResponse(stream, 400, JsonError("Invalid JSON request: " + ex.Message));
                    return;
                }

                if (request == null || string.IsNullOrWhiteSpace(request.script))
                {
                    WriteResponse(stream, 400, JsonError("Missing script"));
                    return;
                }

                EvalTask task = new EvalTask(request.script);
                Tasks.Enqueue(task);

                if (!task.Done.WaitOne(30000))
                {
                    WriteResponse(stream, 504, JsonError("Unity command timed out"));
                    return;
                }

                WriteResponse(stream, task.Ok ? 200 : 500, task.ResponseJson);
            }
        }

        private static void ProcessTasks()
        {
            while (Tasks.TryDequeue(out EvalTask task))
            {
                try
                {
                    string resultJson = Execute(task.Script);
                    task.Ok = true;
                    task.ResponseJson = "{\"ok\":true,\"result\":" + resultJson + "}";
                }
                catch (Exception ex)
                {
                    task.Ok = false;
                    task.ResponseJson = "{\"ok\":false,\"error\":\"" + Escape(ex.Message) +
                        "\",\"traceback\":\"" + Escape(ex.ToString()) + "\"}";
                }
                finally
                {
                    task.Done.Set();
                }
            }
        }

        private static string Execute(string script)
        {
            UnityCommand command = JsonUtility.FromJson<UnityCommand>(script);
            if (command == null || string.IsNullOrWhiteSpace(command.action))
            {
                throw new InvalidOperationException("Unity command JSON must include an action.");
            }

            switch (command.action)
            {
                case "context":
                    return ContextJson();
                case "createPrimitive":
                    return CreatePrimitive(command);
                case "createGameObject":
                    return CreateGameObject(command);
                case "setTransform":
                    return SetTransform(command);
                case "setSelection":
                    return SetSelection(command);
                case "addComponent":
                    return AddComponent(command);
                case "executeMenuItem":
                    return ExecuteMenuItem(command);
                default:
                    throw new InvalidOperationException("Unsupported Unity command action: " + command.action);
            }
        }

        private static string ContextJson()
        {
            List<string> selection = new List<string>();
            foreach (GameObject selected in Selection.gameObjects)
            {
                selection.Add(selected.name);
            }

            Scene scene = SceneManager.GetActiveScene();
            return "{" +
                "\"app\":\"Unity\"," +
                "\"unityVersion\":\"" + Escape(Application.unityVersion) + "\"," +
                "\"projectPath\":\"" + Escape(Application.dataPath.Replace("/Assets", "")) + "\"," +
                "\"scene\":\"" + Escape(scene.name) + "\"," +
                "\"scenePath\":\"" + Escape(scene.path) + "\"," +
                "\"isPlaying\":" + Bool(EditorApplication.isPlaying) + "," +
                "\"activeObject\":\"" + Escape(Selection.activeGameObject ? Selection.activeGameObject.name : "") + "\"," +
                "\"selection\":" + StringArrayJson(selection) +
                "}";
        }

        private static string CreatePrimitive(UnityCommand command)
        {
            PrimitiveType type;
            if (!Enum.TryParse(command.primitiveType ?? "Cube", true, out type))
            {
                throw new InvalidOperationException("Unknown primitiveType: " + command.primitiveType);
            }

            GameObject obj = GameObject.CreatePrimitive(type);
            Undo.RegisterCreatedObjectUndo(obj, Label(command, "Create " + type));
            obj.name = string.IsNullOrWhiteSpace(command.name) ? type.ToString() : command.name;
            ApplyTransform(obj, command, true);
            ApplyRendererColor(obj, command.color);
            Selection.activeGameObject = obj;
            EditorSceneManager.MarkSceneDirty(obj.scene);
            return ObjectJson(obj);
        }

        private static string CreateGameObject(UnityCommand command)
        {
            GameObject obj = new GameObject(string.IsNullOrWhiteSpace(command.name) ? "Creative Adapter Object" : command.name);
            Undo.RegisterCreatedObjectUndo(obj, Label(command, "Create GameObject"));
            ApplyTransform(obj, command, true);
            Selection.activeGameObject = obj;
            EditorSceneManager.MarkSceneDirty(obj.scene);
            return ObjectJson(obj);
        }

        private static string SetTransform(UnityCommand command)
        {
            GameObject obj = ResolveObject(command);
            Undo.RecordObject(obj.transform, Label(command, "Set Transform"));
            ApplyTransform(obj, command, false);
            EditorSceneManager.MarkSceneDirty(obj.scene);
            return ObjectJson(obj);
        }

        private static string SetSelection(UnityCommand command)
        {
            GameObject obj = ResolveObject(command);
            Selection.activeGameObject = obj;
            return ObjectJson(obj);
        }

        private static string AddComponent(UnityCommand command)
        {
            if (string.IsNullOrWhiteSpace(command.componentType))
            {
                throw new InvalidOperationException("addComponent requires componentType.");
            }

            GameObject obj = ResolveObject(command);
            Type componentType = FindType(command.componentType);
            if (componentType == null || !typeof(Component).IsAssignableFrom(componentType))
            {
                throw new InvalidOperationException("Component type not found: " + command.componentType);
            }

            Component component = Undo.AddComponent(obj, componentType);
            EditorSceneManager.MarkSceneDirty(obj.scene);
            return "{\"object\":" + ObjectJson(obj) + ",\"component\":\"" + Escape(component.GetType().FullName) + "\"}";
        }

        private static string ExecuteMenuItem(UnityCommand command)
        {
            if (string.IsNullOrWhiteSpace(command.menuItem))
            {
                throw new InvalidOperationException("executeMenuItem requires menuItem.");
            }

            bool executed = EditorApplication.ExecuteMenuItem(command.menuItem);
            return "{\"menuItem\":\"" + Escape(command.menuItem) + "\",\"executed\":" + Bool(executed) + "}";
        }

        private static GameObject ResolveObject(UnityCommand command)
        {
            if (!string.IsNullOrWhiteSpace(command.path))
            {
                GameObject byPath = GameObject.Find(command.path);
                if (byPath != null)
                {
                    return byPath;
                }
            }

            if (!string.IsNullOrWhiteSpace(command.name))
            {
                GameObject byName = GameObject.Find(command.name);
                if (byName != null)
                {
                    return byName;
                }
            }

            if (Selection.activeGameObject != null)
            {
                return Selection.activeGameObject;
            }

            throw new InvalidOperationException("No target object found. Provide name/path or select an object.");
        }

        private static void ApplyTransform(GameObject obj, UnityCommand command, bool defaults)
        {
            if (defaults || command.setPosition)
            {
                obj.transform.position = new Vector3(command.x, command.y, command.z);
            }

            if (defaults || command.setScale)
            {
                float sx = command.scaleX == 0 ? 1 : command.scaleX;
                float sy = command.scaleY == 0 ? sx : command.scaleY;
                float sz = command.scaleZ == 0 ? sx : command.scaleZ;
                obj.transform.localScale = new Vector3(sx, sy, sz);
            }

            if (defaults || command.setRotation)
            {
                obj.transform.eulerAngles = new Vector3(command.rotationX, command.rotationY, command.rotationZ);
            }
        }

        private static void ApplyRendererColor(GameObject obj, string colorText)
        {
            if (string.IsNullOrWhiteSpace(colorText))
            {
                return;
            }

            Renderer renderer = obj.GetComponent<Renderer>();
            if (renderer == null)
            {
                return;
            }

            if (!ColorUtility.TryParseHtmlString(colorText, out Color color))
            {
                throw new InvalidOperationException("Invalid color: " + colorText);
            }

            Material material = new Material(Shader.Find("Universal Render Pipeline/Lit") ?? Shader.Find("Standard"));
            material.color = color;
            renderer.sharedMaterial = material;
        }

        private static Type FindType(string typeName)
        {
            foreach (var assembly in AppDomain.CurrentDomain.GetAssemblies())
            {
                Type type = assembly.GetType(typeName);
                if (type != null)
                {
                    return type;
                }

                foreach (Type candidate in assembly.GetTypes())
                {
                    if (candidate.Name == typeName)
                    {
                        return candidate;
                    }
                }
            }
            return null;
        }

        private static void WriteResponse(Stream stream, int status, string body)
        {
            byte[] bodyBytes = Encoding.UTF8.GetBytes(body);
            string reason = status == 200 ? "OK" : "Error";
            string header =
                "HTTP/1.1 " + status.ToString(CultureInfo.InvariantCulture) + " " + reason + "\r\n" +
                "Content-Type: application/json\r\n" +
                "Content-Length: " + bodyBytes.Length.ToString(CultureInfo.InvariantCulture) + "\r\n" +
                "Connection: close\r\n\r\n";
            byte[] headerBytes = Encoding.ASCII.GetBytes(header);
            stream.Write(headerBytes, 0, headerBytes.Length);
            stream.Write(bodyBytes, 0, bodyBytes.Length);
        }

        private static string GenerateToken()
        {
            byte[] bytes = new byte[32];
            using (RandomNumberGenerator rng = RandomNumberGenerator.Create())
            {
                rng.GetBytes(bytes);
            }
            StringBuilder builder = new StringBuilder(bytes.Length * 2);
            foreach (byte value in bytes)
            {
                builder.Append(value.ToString("x2"));
            }
            return builder.ToString();
        }

        private static string SessionDirectory()
        {
            string root = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData);
            return Path.Combine(root, "creative-adapters");
        }

        private static string SessionPath()
        {
            return Path.Combine(SessionDirectory(), SessionName + ".json");
        }

        private static void WriteSessionFile(int port)
        {
            Directory.CreateDirectory(SessionDirectory());
            string payload = "{" +
                "\"app\":\"unity\"," +
                "\"url\":\"http://" + Host + ":" + port.ToString(CultureInfo.InvariantCulture) + "/eval\"," +
                "\"host\":\"" + Host + "\"," +
                "\"port\":" + port.ToString(CultureInfo.InvariantCulture) + "," +
                "\"token\":\"" + _token + "\"," +
                "\"createdAt\":\"" + DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ") + "\"" +
                "}";
            string tempPath = SessionPath() + ".tmp";
            File.WriteAllText(tempPath, payload, Encoding.UTF8);
            if (File.Exists(SessionPath()))
            {
                File.Delete(SessionPath());
            }
            File.Move(tempPath, SessionPath());
        }

        private static void RemoveSessionFile()
        {
            try
            {
                if (File.Exists(SessionPath()))
                {
                    File.Delete(SessionPath());
                }
            }
            catch { }
        }

        private static string ObjectJson(GameObject obj)
        {
            Vector3 p = obj.transform.position;
            Vector3 s = obj.transform.localScale;
            Vector3 r = obj.transform.eulerAngles;
            return "{" +
                "\"name\":\"" + Escape(obj.name) + "\"," +
                "\"path\":\"" + Escape(GetPath(obj)) + "\"," +
                "\"position\":[" + Number(p.x) + "," + Number(p.y) + "," + Number(p.z) + "]," +
                "\"scale\":[" + Number(s.x) + "," + Number(s.y) + "," + Number(s.z) + "]," +
                "\"rotation\":[" + Number(r.x) + "," + Number(r.y) + "," + Number(r.z) + "]" +
                "}";
        }

        private static string GetPath(GameObject obj)
        {
            string path = obj.name;
            Transform current = obj.transform.parent;
            while (current != null)
            {
                path = current.name + "/" + path;
                current = current.parent;
            }
            return path;
        }

        private static string Label(UnityCommand command, string fallback)
        {
            return string.IsNullOrWhiteSpace(command.undoLabel) ? fallback : command.undoLabel;
        }

        private static string JsonError(string message)
        {
            return "{\"ok\":false,\"error\":\"" + Escape(message) + "\"}";
        }

        private static string StringArrayJson(List<string> values)
        {
            List<string> escaped = new List<string>();
            foreach (string value in values)
            {
                escaped.Add("\"" + Escape(value) + "\"");
            }
            return "[" + string.Join(",", escaped.ToArray()) + "]";
        }

        private static string Escape(string value)
        {
            if (string.IsNullOrEmpty(value))
            {
                return "";
            }
            return value.Replace("\\", "\\\\").Replace("\"", "\\\"").Replace("\r", "\\r").Replace("\n", "\\n");
        }

        private static string Bool(bool value)
        {
            return value ? "true" : "false";
        }

        private static string Number(float value)
        {
            return value.ToString("R", CultureInfo.InvariantCulture);
        }

        [Serializable]
        private class BridgeRequest
        {
            public string script;
        }

        [Serializable]
        private class UnityCommand
        {
            public string action;
            public string name;
            public string path;
            public string primitiveType;
            public string componentType;
            public string menuItem;
            public string color;
            public string undoLabel;
            public float x;
            public float y;
            public float z;
            public float scaleX;
            public float scaleY;
            public float scaleZ;
            public float rotationX;
            public float rotationY;
            public float rotationZ;
            public bool setPosition;
            public bool setScale;
            public bool setRotation;
        }

        private class EvalTask
        {
            public readonly string Script;
            public readonly ManualResetEvent Done = new ManualResetEvent(false);
            public bool Ok;
            public string ResponseJson;

            public EvalTask(string script)
            {
                Script = script;
            }
        }
    }
}
