import json
import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class Stage2StructureTests(unittest.TestCase):
    def test_required_files_exist(self):
        for relative in (
            "wokwi/sketch.ino",
            "wokwi/alert_logic.h",
            "wokwi/diagram.json",
            "wokwi/libraries.txt",
            "docs/ETAPA_2_PLANO_TESTES.md",
        ):
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_circuit_has_two_sensors_and_led(self):
        diagram = json.loads((ROOT / "wokwi/diagram.json").read_text(encoding="utf-8"))
        part_types = {part["type"] for part in diagram["parts"]}
        self.assertIn("wokwi-esp32-devkit-v1", part_types)
        self.assertIn("wokwi-dht22", part_types)
        self.assertIn("wokwi-potentiometer", part_types)
        self.assertIn("wokwi-led", part_types)

    def test_required_connections(self):
        diagram = json.loads((ROOT / "wokwi/diagram.json").read_text(encoding="utf-8"))
        pairs = {(item[0], item[1]) for item in diagram["connections"]}
        self.assertIn(("esp:D15", "dht:SDA"), pairs)
        self.assertIn(("esp:D34", "bpm:SIG"), pairs)
        self.assertIn(("esp:D2", "alertLed:A"), pairs)

    def test_firmware_matches_stage2_contract(self):
        sketch = (ROOT / "wokwi/sketch.ino").read_text(encoding="utf-8")
        logic = (ROOT / "wokwi/alert_logic.h").read_text(encoding="utf-8")
        for token in (
            "#include <DHTesp.h>",
            "SAMPLE_INTERVAL_MS = 5000",
            "sensor_valid=%s",
            "TEST dht_fault=on",
            "TEST dht_fault=off",
            "processTestCommands();",
        ):
            self.assertIn(token, sketch)
        for token in ("BPM_LOW = 50", "BPM_HIGH = 120", "TEMP_HIGH_C = 38.0F"):
            self.assertIn(token, logic)
        self.assertNotIn("PubSubClient", sketch)
        self.assertNotIn("WiFi.begin", sketch)

    def test_library_is_explicit(self):
        libraries = (ROOT / "wokwi/libraries.txt").read_text(encoding="utf-8")
        self.assertEqual(libraries.strip(), "DHT sensor library for ESPx")

    def test_continuous_evidence_is_preserved(self):
        log = (ROOT / "evidencias/etapa-2/E2-03-transicoes-continuas.txt")
        alert_capture = ROOT / "evidencias/etapa-2/E2-03-alerta-normal-sem-reinicio.jpg"
        dht_capture = ROOT / "evidencias/etapa-2/E2-04-dht-falha-recuperacao-sem-reinicio.jpg"

        self.assertTrue(log.is_file())
        content = log.read_text(encoding="utf-8")
        for token in (
            "alert=high_bpm",
            "alert=sensor_error",
            "TEST dht_fault=off",
            "alert=normal",
            "Desvio relativo: +0,36%",
        ):
            self.assertIn(token, content)

        expected_hashes = {
            alert_capture: "f5acb69ba69f060175a091f3e70d969359081ed6a0e85a75db1b73095e1a2e2c",
            dht_capture: "77575d137daf0d43ef742b69c7efacb09a4a5c3ea01d6f2575759005c9fe0e40",
        }
        for path, expected in expected_hashes.items():
            self.assertTrue(path.is_file())
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected)


if __name__ == "__main__":
    unittest.main()
