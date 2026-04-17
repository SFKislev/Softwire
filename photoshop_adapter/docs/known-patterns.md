# Photoshop ExtendScript Known Patterns

This file is the curated high-signal reference for the first adapter test. Use
the full scripting reference when present, but prefer these patterns when they
match the request.

## Context

Use `examples/context.jsx`. It does not depend on a global `JSON` object.

## Open Liquify

Liquify can be opened with menu dispatch:

```jsx
app.runMenuItem(stringIDToTypeID("liquify"));
```

Photoshop may expose some filter parameters through Action Manager descriptors,
but the modal Liquify workspace is mostly opaque once opened. Do not claim brush
state was configured unless the exact descriptor was verified on this installed
Photoshop version.

## Set Active Layer Opacity And Blend Mode

```jsx
app.activeDocument.suspendHistory("Set layer opacity and blend mode", "main()");

function main() {
  var layer = app.activeDocument.activeLayer;
  layer.opacity = 40;
  layer.blendMode = BlendMode.MULTIPLY;
}
```

Common blend mode constants include:

- `BlendMode.NORMAL`
- `BlendMode.MULTIPLY`
- `BlendMode.SCREEN`
- `BlendMode.OVERLAY`
- `BlendMode.SOFTLIGHT`

## Create A Retouch Layer Above The Active Layer

```jsx
app.activeDocument.suspendHistory("Create Retouch layer", "main()");

function main() {
  var doc = app.activeDocument;
  var original = doc.activeLayer;
  var layer = doc.artLayers.add();
  layer.name = "Retouch";
  layer.move(original, ElementPlacement.PLACEBEFORE);
  doc.activeLayer = layer;
}
```

## Run A Photoshop Action

```jsx
app.doAction("Export for Web", "Default Actions");
```

The first argument is the action name. The second argument is the action set
name as it appears in Photoshop.
