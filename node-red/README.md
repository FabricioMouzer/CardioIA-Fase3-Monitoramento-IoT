# Node-RED — Dashboard CardioIA

## Componentes

- Node-RED 5.0.9;
- `@flowfuse/node-red-dashboard` 1.34.0;
- MQTT público HiveMQ, sem autenticação e somente com dados sintéticos;
- flow exportado em `flows.json`.

## Instalação reproduzível

No terminal, dentro desta pasta:

```bash
npm install
npm start
```

No Windows, os mesmos comandos funcionam no PowerShell ou Prompt de Comando,
desde que Node.js esteja instalado. Não utilizar `sudo` no Windows.

Editor local: `http://127.0.0.1:1880/`  
Dashboard: `http://127.0.0.1:1880/dashboard/monitoramento`

## Testes determinísticos

O flow contém botões de injeção para:

- estado normal;
- BPM alto;
- BPM baixo;
- temperatura alta;
- falha do sensor;
- valores exatamente nos limites;
- contrato JSON incompatível.

Os botões existem para produzir evidências repetíveis. Eles não representam
pacientes ou medições reais.

## Segurança

Não há credenciais. O broker público e a porta 1883 não devem receber dados
reais. Para produção seriam obrigatórios TLS, autenticação, autorização por
tópico e proteção do editor Node-RED.
