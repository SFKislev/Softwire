# Unity Sources

- Unity Editor scripting API is available inside the running Editor through
  `UnityEditor` and `UnityEngine` assemblies.
- This adapter uses a project-local Editor package and a tokenized loopback TCP
  server. It does not rely on Unity Hub, Unity Cloud, or an external service.
- Unity does not provide a built-in string `eval` for arbitrary C# in the
  Editor. Extend the package with explicit bridge actions or project-local
  Editor scripts for behavior beyond the built-in command surface.
