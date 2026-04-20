(function () {
  var APP_NAME = "after_effects";
  var EXTENSION_ID = "com.creativeadapters.aftereffects.panel";
  var SESSION_FILE = "after_effects.json";
  var statusEl = document.getElementById("status");
  var MAX_BODY_BYTES = 1024 * 1024;

  function setStatus(message) {
    statusEl.textContent = message;
  }

  function sendJson(response, statusCode, payload) {
    response.writeHead(statusCode, {
      "Content-Type": "application/json"
    });
    response.end(JSON.stringify(payload));
  }

  function timingSafeEqual(a, b) {
    if (!a || !b || a.length !== b.length) {
      return false;
    }
    var mismatch = 0;
    for (var i = 0; i < a.length; i++) {
      mismatch |= a.charCodeAt(i) ^ b.charCodeAt(i);
    }
    return mismatch === 0;
  }

  function evalScript(script, callback) {
    window.__adobe_cep__.evalScript(script, function (result) {
      callback(result);
    });
  }

  function normalizeResult(result) {
    if (result === null || result === undefined || result === "") {
      return null;
    }
    try {
      return JSON.parse(result);
    } catch (e) {
      return String(result);
    }
  }

  try {
    evalScript('try { app.setExtensionPersistent("' + EXTENSION_ID + '", 1); "ok"; } catch (e) { "persistence unavailable: " + e; }', function () {});

    var http = require("http");
    var crypto = require("crypto");
    var fs = require("fs");
    var path = require("path");
    var token = crypto.randomBytes(32).toString("hex");

    function sessionDirectory() {
      var root = process.env.APPDATA || process.env.HOME || process.env.USERPROFILE;
      if (!root) {
        throw new Error("No user profile directory is available for the bridge session file.");
      }
      return path.join(root, "creative-adapters");
    }

    function writeSessionFile(port) {
      var dir = sessionDirectory();
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir);
      }
      var session = {
        app: APP_NAME,
        url: "http://127.0.0.1:" + port + "/eval",
        host: "127.0.0.1",
        port: port,
        token: token,
        createdAt: new Date().toISOString()
      };
      fs.writeFileSync(path.join(dir, SESSION_FILE), JSON.stringify(session, null, 2), "utf8");
    }

    var server = http.createServer(function (request, response) {
      if (request.method === "OPTIONS") {
        sendJson(response, 403, { ok: false, error: "CORS preflight is not supported." });
        return;
      }
      if (request.method !== "POST" || request.url !== "/eval") {
        sendJson(response, 404, { ok: false, error: "Not found" });
        return;
      }
      if (!timingSafeEqual(request.headers["x-bridge-token"], token)) {
        sendJson(response, 403, { ok: false, error: "Invalid bridge token" });
        return;
      }

      var body = "";
      var bodyBytes = 0;
      request.on("data", function (chunk) {
        bodyBytes += chunk.length;
        if (bodyBytes > MAX_BODY_BYTES) {
          request.destroy();
          return;
        }
        body += chunk;
      });
      request.on("end", function () {
        var payload;
        try {
          payload = JSON.parse(body);
        } catch (e) {
          sendJson(response, 400, { ok: false, error: "Invalid JSON request" });
          return;
        }
        if (!payload.script || !payload.script.trim()) {
          sendJson(response, 400, { ok: false, error: "Missing script" });
          return;
        }

        evalScript(payload.script, function (result) {
          if (result === "EvalScript error.") {
            sendJson(response, 500, { ok: false, error: result });
            return;
          }
          sendJson(response, 200, { ok: true, result: normalizeResult(result) });
        });
      });
    });

    server.listen(0, "127.0.0.1", function () {
      var port = server.address().port;
      writeSessionFile(port);
      setStatus("Listening on 127.0.0.1:" + port);
    });
    server.on("error", function (error) {
      setStatus("Bridge failed: " + error.message);
    });
  } catch (error) {
    setStatus("Node.js is unavailable in CEP: " + error.message);
  }
}());
