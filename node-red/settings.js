/** Configuração local reproduzível. Não contém credenciais. */
module.exports = {
  flowFile: "flows.json",
  uiHost: "0.0.0.0",
  uiPort: process.env.PORT || 1880,
  // Em produção, desabilita o editor e todos os endpoints administrativos.
  // O dashboard continua disponível pelos endpoints HTTP dos nós.
  httpAdminRoot: process.env.NODE_RED_DISABLE_ADMIN === "true" ? false : "/",
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
