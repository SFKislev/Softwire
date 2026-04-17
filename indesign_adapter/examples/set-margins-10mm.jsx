var result = "";

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

if (!app.documents.length) {
  throw new Error("No active InDesign document.");
}

var doc = app.activeDocument;
var oldUnits = app.scriptPreferences.measurementUnit;

try {
  app.scriptPreferences.measurementUnit = MeasurementUnits.MILLIMETERS;
  doc.marginPreferences.top = 10;
  doc.marginPreferences.bottom = 10;
  doc.marginPreferences.left = 10;
  doc.marginPreferences.right = 10;

  result = jsonObject({
    doc: doc.name,
    margins: "10mm",
    top: doc.marginPreferences.top,
    bottom: doc.marginPreferences.bottom,
    left: doc.marginPreferences.left,
    right: doc.marginPreferences.right
  });
} finally {
  app.scriptPreferences.measurementUnit = oldUnits;
}

result;
