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

function setPathAppearance(item, color) {
  if (item.typename === "PathItem") {
    item.stroked = true;
    item.strokeColor = color;
    item.strokeWidth = 1;
    item.filled = false;
    return 1;
  }
  if (item.typename === "CompoundPathItem") {
    var changed = 0;
    for (var i = 0; i < item.pathItems.length; i++) {
      changed += setPathAppearance(item.pathItems[i], color);
    }
    return changed;
  }
  if (item.typename === "GroupItem") {
    var groupChanged = 0;
    for (var j = 0; j < item.pageItems.length; j++) {
      groupChanged += setPathAppearance(item.pageItems[j], color);
    }
    return groupChanged;
  }
  return 0;
}

if (!app.documents.length) {
  throw new Error("No active Illustrator document.");
}
if (!app.selection || !app.selection.length) {
  throw new Error("No selected Illustrator items.");
}

var black = new RGBColor();
black.red = 0;
black.green = 0;
black.blue = 0;

var changed = 0;
for (var i = 0; i < app.selection.length; i++) {
  changed += setPathAppearance(app.selection[i], black);
}

jsonObject({
  doc: app.activeDocument.name,
  selectedItems: app.selection.length,
  changedPathItems: changed,
  strokeWidth: 1,
  strokeColor: "000000",
  fill: "none"
});
