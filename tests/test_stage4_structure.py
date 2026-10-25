import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class Stage4StructureTests(unittest.TestCase):
    def test_required_files_exist(self):
        for relative in (
            "wokwi/mqtt_payload.h",
            "docs/ETAPA_4_BLUEPRINT.md",
            "docs/ETAPA_4_PLANO_TESTES.md",
            "docs/ETAPA_4_VALIDACAO.md",
            "docs/ETAPA_4_CONCLUSAO.md",
            "tests/run_stage4_payload_logic.py",
            "tests/validate_stage4_evidence.py",
        ):
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_topics_match_approved_contract(self):
        sketch = (ROOT / "wokwi/sketch.ino").read_text(encoding="utf-8")
        prefix = "cardioia/fase3/rm566777/cardioia-esp32-01/"
        for suffix in ("telemetria", "alerta", "status"):
            self.assertIn(prefix + suffix, sketch)

    def test_connection_configuration(self):
        sketch = (ROOT / "wokwi/sketch.ino").read_text(encoding="utf-8")
        for token in (
            '#include <PubSubClient.h>',
            '#include <WiFi.h>',
            'WIFI_SSID[] = "Wokwi-GUEST"',
            'MQTT_HOST[] = "broker.hivemq.com"',
            "MQTT_PORT = 1883",
            "RECONNECT_INTERVAL_MS = 5000",
            "mqttClient.setBufferSize(512)",
        ):
            self.assertIn(token, sketch)

    def test_retention_and_resilience_contract(self):
        sketch = (ROOT / "wokwi/sketch.ino").read_text(encoding="utf-8")
        self.assertIn("TOPIC_STATUS, payload, retained", sketch)
        self.assertIn("TOPIC_TELEMETRY, payload, false", sketch)
        self.assertIn("TOPIC_ALERT, payload, false", sketch)
        self.assertIn("offlineBuffer.front(sample)", sketch)
        self.assertIn("if (!publishSample", sketch)
        self.assertIn("offlineBuffer.discardFront()", sketch)

    def test_no_secret_literals(self):
        sketch = (ROOT / "wokwi/sketch.ino").read_text(encoding="utf-8").lower()
        for forbidden in ("mqtt_password", "api_key", "bearer ", "-----begin"):
            self.assertNotIn(forbidden, sketch)

    def test_stage4_gate_is_closed(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        plan = (ROOT / "docs/ETAPA_4_PLANO_TESTES.md").read_text(encoding="utf-8")
        conclusion = (ROOT / "docs/ETAPA_4_CONCLUSAO.md").read_text(encoding="utf-8")
        self.assertIn("Etapas 0 a 4 confirmadas e finalizadas", readme)
        self.assertNotIn("- [ ] **T4-", plan)
        self.assertIn("FECHADO — ETAPA CONFIRMADA E FINALIZADA", plan)
        self.assertIn("Etapa 5 está tecnicamente", conclusion)
        self.assertIn("não foi iniciada", conclusion)


if __name__ == "__main__":
    unittest.main()
