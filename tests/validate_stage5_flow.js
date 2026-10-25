#!/usr/bin/env node
'use strict'

const assert = require('node:assert/strict')
const fs = require('node:fs')
const path = require('node:path')
const vm = require('node:vm')

const root = path.resolve(__dirname, '..')
const flows = JSON.parse(fs.readFileSync(path.join(root, 'node-red/flows.json'), 'utf8'))
const pkg = JSON.parse(fs.readFileSync(path.join(root, 'node-red/package.json'), 'utf8'))
let checks = 0

function ok (condition, message) {
  assert.ok(condition, message)
  checks += 1
}

function nodes (type) {
  return flows.filter((node) => node.type === type)
}

ok(pkg.dependencies['node-red'] === '5.0.9', 'Node-RED deve estar fixado')
ok(pkg.dependencies['@flowfuse/node-red-dashboard'] === '1.34.0', 'Dashboard deve estar fixado')
ok(nodes('ui-chart').length === 1, 'Deve existir um gráfico BPM')
ok(nodes('ui-gauge').length >= 2, 'Devem existir gauges de temperatura e umidade')
ok(nodes('ui-text').some((node) => node.name === 'Indicador de alerta'), 'Indicador visual ausente')

const prefix = 'cardioia/fase3/rm566777/cardioia-esp32-01/'
const mqttTopics = new Set(nodes('mqtt in').map((node) => node.topic))
for (const suffix of ['telemetria', 'alerta', 'status']) {
  ok(mqttTopics.has(prefix + suffix), `Tópico ${suffix} ausente`)
}
const broker = nodes('mqtt-broker')[0]
ok(broker.broker === 'broker.hivemq.com' && broker.port === '1883', 'Broker divergente')
ok(!broker.credentials && !broker.user && !broker.password, 'Credencial não permitida')

const processor = nodes('function').find((node) => node.name === 'Validar e distribuir telemetria')
ok(processor && processor.outputs === 8, 'Processador de telemetria inválido')
const execute = vm.runInNewContext(`(function (msg) { ${processor.func} })`)
const injects = Object.fromEntries(nodes('inject').map((node) => [node.name, JSON.parse(node.payload)]))

function processCase (name) {
  const result = execute({ payload: injects[name] })
  ok(Array.isArray(result) && result.length === 8, `${name}: saídas inválidas`)
  return result
}

let result = processCase('Teste NORMAL')
ok(result[0].payload === 80 && result[3].payload === 'NORMAL', 'Cenário normal falhou')
ok(result[6].payload === 'online (telemetria ativa) | fila: 0 | descartes: 0' &&
   result[6].ui_update.color === '#067647',
   'Telemetria válida não reafirmou o estado online')
result = processCase('Teste BPM ALTO')
ok(result[3].payload === 'BPM ALTO' && result[3].ui_update.color === '#b42318', 'BPM alto falhou')
result = processCase('Teste BPM BAIXO')
ok(result[3].payload === 'BPM BAIXO', 'BPM baixo falhou')
result = processCase('Teste TEMPERATURA ALTA')
ok(result[1].payload === 39 && result[3].payload === 'TEMPERATURA ALTA', 'Temperatura alta falhou')
result = processCase('Teste FALHA SENSOR')
ok(result[3].payload === 'FALHA DO SENSOR', 'Falha de sensor não sinalizada')
result = processCase('Teste LIMITES NORMAIS')
ok(result[0].payload === 120 && result[1].payload === 38 && result[3].payload === 'NORMAL', 'Limites inclusivos falharam')
result = processCase('Teste JSON INVÁLIDO')
ok(result.slice(0, 7).every((value) => value === null) &&
   /Campos ausentes|Contrato incompatível/.test(result[7].payload),
   'Contrato inválido não foi isolado')

const serialized = JSON.stringify(flows).toLowerCase()
for (const forbidden of ['mqtt_password', 'api_key', 'bearer ', '-----begin']) {
  ok(!serialized.includes(forbidden), `Segredo potencial encontrado: ${forbidden}`)
}

console.log(`Etapa 5: ${checks} verificações estruturais e lógicas aprovadas.`)
