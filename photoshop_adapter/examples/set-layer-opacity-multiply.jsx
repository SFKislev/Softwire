app.activeDocument.suspendHistory("Set layer opacity and blend mode", "main()");

function main() {
  var layer = app.activeDocument.activeLayer;
  layer.opacity = 40;
  layer.blendMode = BlendMode.MULTIPLY;
}
