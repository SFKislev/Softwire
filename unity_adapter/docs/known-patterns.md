# Unity Known Patterns

## Context

```powershell
Get-Content unity_adapter/examples/context.json -Raw | python unity_adapter/unity_bridge.py --stdin
```

## Create a primitive

```json
{
  "action": "createPrimitive",
  "primitiveType": "Cube",
  "name": "Blockout Cube",
  "x": 0,
  "y": 0.5,
  "z": 0,
  "scaleX": 1,
  "scaleY": 1,
  "scaleZ": 1,
  "color": "#1267ff",
  "undoLabel": "Creative Adapter: Create blockout cube"
}
```

Supported `primitiveType` values are Unity's `PrimitiveType` names, including
`Cube`, `Sphere`, `Capsule`, `Cylinder`, `Plane`, and `Quad`.

## Transform an object

Targets resolve by `path`, then `name`, then the active selected GameObject.

```json
{
  "action": "setTransform",
  "name": "Blockout Cube",
  "setPosition": true,
  "setScale": true,
  "x": 0,
  "y": 1,
  "z": 2,
  "scaleX": 2,
  "scaleY": 1,
  "scaleZ": 2,
  "undoLabel": "Creative Adapter: Move blockout cube"
}
```

## Execute a Unity menu item

```json
{
  "action": "executeMenuItem",
  "menuItem": "GameObject/Light/Directional Light"
}
```

## Add a component

```json
{
  "action": "addComponent",
  "name": "Player",
  "componentType": "Rigidbody"
}
```
