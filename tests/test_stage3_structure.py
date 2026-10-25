import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class Stage3StructureTests(unittest.TestCase):
    def test_required_files_exist(self):
        for relative in (
            "wokwi/edge_buffer.h",
            "docs/ETAPA_3_BLUEPRINT.md",
            "docs/ETAPA_3_PLANO_TESTES.md",
            "tests/run_stage3_buffer_logic.py",
        ):
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_button_exists_and_is_connected_to_gpio4(self):
        diagram = json.loads((ROOT / "wokwi/diagram.json").read_text(encoding="utf-8"))
        parts = {part["id"]: part["type"] for part in diagram["parts"]}
        pairs = {(item[0], item[1]) for item in diagram["connections"]}
        self.assertEqual(parts.get("offlineButton"), "wokwi-pushbutton")
        self.assertIn(("esp:D4", "offlineButton:1.l"), pairs)
        self.assertIn(("offlineButton:2.l", "esp:GND.2"), pairs)

    def test_capacity_and_retention_contract(self):
        sketch = (ROOT / "wokwi/sketch.ino").read_text(encoding="utf-8")
        blueprint = (ROOT / "docs/ETAPA_3_BLUEPRINT.md").read_text(encoding="utf-8")
        self.assertIn("OFFLINE_BUFFER_CAPACITY = 2160", sketch)
        self.assertIn("SAMPLE_INTERVAL_MS = 5000", sketch)
        self.assertIn("2.160 × 5 s = 3 horas", (ROOT / "docs/ETAPA_3_PLANO_TESTES.md").read_text(encoding="utf-8"))
        self.assertIn("Retenção nominal", blueprint)

    def test_offline_and_sync_observability(self):
        sketch = (ROOT / "wokwi/sketch.ino").read_text(encoding="utf-8")
        for token in (
            "CONNECTIVITY state=%s",
            "BUFFER_STORE seq=%lu",
            "SYNC_START pending=%u",
            "CLOUD_SEND seq=%lu",
            "SYNC_DONE sent=%u pending=%u",
            'setConnectivity(false, "serial")',
            'setConnectivity(true, "serial")',
        ):
            self.assertIn(token, sketch)

    def test_overflow_is_explicit(self):
        header = (ROOT / "wokwi/edge_buffer.h").read_text(encoding="utf-8")
        sketch = (ROOT / "wokwi/sketch.ino").read_text(encoding="utf-8")
        self.assertIn("++dropped_", header)
        self.assertIn("head_ = (head_ + 1) % Capacity", header)
        self.assertIn("dropped_samples=%lu", sketch)
        self.assertIn('overwritten ? "true" : "false"', sketch)

    def test_stage4_is_not_started(self):
        sketch = (ROOT / "wokwi/sketch.ino").read_text(encoding="utf-8")
        self.assertNotIn("PubSubClient", sketch)
        self.assertNotIn("WiFi.begin", sketch)
        self.assertNotIn("broker.hivemq.com", sketch)

    def test_gate_is_closed(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        plan = (ROOT / "docs/ETAPA_3_PLANO_TESTES.md").read_text(encoding="utf-8")
        conclusion = (ROOT / "docs/ETAPA_3_CONCLUSAO.md").read_text(encoding="utf-8")
        self.assertIn(
            "| 3 | Resiliência offline no Edge | Confirmada e finalizada", readme
        )
        self.assertNotIn("- [ ] **T3-", plan)
        self.assertIn("FECHADO — ETAPA CONFIRMADA", plan)
        self.assertIn("✅ ETAPA 3 CONFIRMADA E FINALIZADA", conclusion)


if __name__ == "__main__":
    unittest.main()
