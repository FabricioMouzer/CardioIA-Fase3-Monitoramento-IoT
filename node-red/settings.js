/** Configuração local reproduzível. Não contém credenciais. */
module.exports = {
  flowFile: "flows.json",
  uiPort: process.env.PORT || 1880,
  diagnostics: { enabled: false, ui: false },
  runtimeState: { enabled: false, ui: false },
  editorTheme: {
    projects: { enabled: false },
    tours: false
  },
  functionExternalModules: false,
  exportGlobalContextKeys: false,
  logging: {
    console: { level: "info", metrics: false, audit: false }
  }
};
