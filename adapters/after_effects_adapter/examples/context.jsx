(function () {
  function escapeString(value) {
    if (value === null || value === undefined) return "";
    return String(value)
      .replace(/\\/g, "\\\\")
      .replace(/"/g, '\\"')
      .replace(/\r/g, "\\r")
      .replace(/\n/g, "\\n");
  }

  function pair(name, value, isNumberOrBool) {
    if (value === null || value === undefined) {
      return '"' + name + '":null';
    }
    if (isNumberOrBool) {
      return '"' + name + '":' + value;
    }
    return '"' + name + '":"' + escapeString(value) + '"';
  }

  var project = app.project;
  var activeItem = project ? project.activeItem : null;
  var file = project && project.file ? project.file.fsName : null;
  var parts = [
    pair("app", "After Effects", false),
    pair("version", app.version, false),
    pair("project", project ? project.name : null, false),
    pair("projectFile", file, false),
    pair("numItems", project ? project.numItems : null, true),
    pair("activeItem", activeItem ? activeItem.name : null, false),
    pair("activeItemType", activeItem ? activeItem.typeName : null, false)
  ];
  return "{" + parts.join(",") + "}";
}())
