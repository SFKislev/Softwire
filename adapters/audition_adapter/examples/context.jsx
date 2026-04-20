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

  function safeEval(label, expression) {
    try {
      return eval(expression);
    } catch (e) {
      return null;
    }
  }

  var activeDocumentName = safeEval("activeDocumentName", "app.activeDocument ? app.activeDocument.name : null");
  var activeDocumentPath = safeEval("activeDocumentPath", "app.activeDocument && app.activeDocument.path ? app.activeDocument.path : null");
  var activeSessionName = safeEval("activeSessionName", "app.activeSession ? app.activeSession.name : null");
  var version = safeEval("version", "app.version");
  var build = safeEval("build", "app.build");

  var parts = [
    pair("app", "Audition", false),
    pair("version", version, false),
    pair("build", build, false),
    pair("activeDocument", activeDocumentName, false),
    pair("activeDocumentPath", activeDocumentPath, false),
    pair("activeSession", activeSessionName, false)
  ];
  return "{" + parts.join(",") + "}";
}())
