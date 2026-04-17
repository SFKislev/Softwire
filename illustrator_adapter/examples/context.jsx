function jsonEscape(value) {
  return String(value)
    .replace(/\\/g, "\\\\")
    .replace(/"/g, '\\"')
    .replace(/\r/g, "\\r")
    .replace(/\n/g, "\\n")
    .replace(/\t/g, "\\t");
}

function jsonValue(value) {
  if (value === null || value === undefined) {
    return "null";
  }
  if (typeof value === "number" || typeof value === "boolean") {
    return String(value);
  }
  return '"' + jsonEscape(value) + '"';
}

function jsonObject(obj) {
  var parts = [];
  for (var key in obj) {
    if (obj.hasOwnProperty(key)) {
      parts.push('"' + jsonEscape(key) + '":' + jsonValue(obj[key]));
    }
  }
  return "{" + parts.join(",") + "}";
}

var doc = null;
var layerName = null;
var selectionCount = 0;
var firstSelectionType = null;

if (app.documents.length) {
  doc = app.activeDocument;
  try {
    layerName = doc.activeLayer ? doc.activeLayer.name : null;
  } catch (e) {
    layerName = null;
  }
  try {
    selectionCount = app.selection ? app.selection.length : 0;
    firstSelectionType = selectionCount ? app.selection[0].typename : null;
  } catch (e2) {
    selectionCount = 0;
    firstSelectionType = null;
  }
}

jsonObject({
  app: app.name,
  version: app.version,
  documents: app.documents.length,
  doc: doc ? doc.name : null,
  activeLayer: layerName,
  selectionCount: selectionCount,
  firstSelectionType: firstSelectionType
});
