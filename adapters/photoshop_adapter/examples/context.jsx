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

var ctx = {
  app: app.name,
  version: app.version,
  documents: app.documents.length,
  doc: app.documents.length ? app.activeDocument.name : null,
  activeLayer: app.documents.length ? app.activeDocument.activeLayer.name : null,
  hasSelection: false,
  currentTool: app.currentTool,
  foregroundColor: app.foregroundColor.rgb.hexValue
};

if (app.documents.length) {
  try {
    var bounds = app.activeDocument.selection.bounds;
    ctx.hasSelection = bounds && bounds.length === 4;
  } catch (e) {
    ctx.hasSelection = false;
  }
}

jsonObject(ctx);
