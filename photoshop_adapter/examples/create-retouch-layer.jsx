app.activeDocument.suspendHistory("Create Retouch layer", "main()");

function main() {
  var doc = app.activeDocument;
  var original = doc.activeLayer;
  var layer = doc.artLayers.add();
  layer.name = "Retouch";
  layer.move(original, ElementPlacement.PLACEBEFORE);
  doc.activeLayer = layer;
}
