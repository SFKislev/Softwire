try {
  app.setExtensionPersistent("com.creativeadapters.premiere.panel", 1);
} catch (e) {
  // Older or restricted hosts may not expose persistence.
}
