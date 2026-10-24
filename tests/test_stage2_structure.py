import json
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


if __name__ == "__main__":
    unittest.main()
