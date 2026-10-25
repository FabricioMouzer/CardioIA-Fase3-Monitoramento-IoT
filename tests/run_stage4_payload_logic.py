"""Compila o formatador C++ e valida os JSONs produzidos."""

import json
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HEADER = ROOT / "wokwi/mqtt_payload.h"

PROGRAM = r'''
#include <iostream>
#include "mqtt_payload.h"

int main() {
  char telemetry[512];
  TelemetryPayloadInput input{42, 210000, 36.7F, 58.2F, 82, true, 0,
                              "normal", "live", 0, 0};
  int telemetryLength = formatTelemetryJson(telemetry, sizeof(telemetry), input);
  if (telemetryLength <= 0 || telemetryLength >= static_cast<int>(sizeof(telemetry))) return 1;
  std::cout << telemetry << "\n";

  char status[256];
  int statusLength = formatStatusJson(status, sizeof(status), "online", 3, 1, 220000);
  if (statusLength <= 0 || statusLength >= static_cast<int>(sizeof(status))) return 2;
  std::cout << status << "\n";
  return 0;
}
'''


def main() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        source = Path(temporary) / "payload_test.cpp"
        binary = Path(temporary) / "payload_test"
        source.write_text(PROGRAM, encoding="utf-8")
        subprocess.run(
            ["g++", "-std=c++11", "-Wall", "-Wextra", "-Werror",
             f"-I{HEADER.parent}", str(source), "-o", str(binary)],
            check=True,
        )
        lines = subprocess.check_output([str(binary)], text=True).splitlines()

    telemetry, status = map(json.loads, lines)
    required = {
        "schema_version", "device_id", "sequence", "captured_uptime_ms",
        "temperature_c", "humidity_pct", "bpm", "sensor_valid",
        "alert_code", "alert", "source", "buffer_pending", "dropped_samples",
    }
    assert required == set(telemetry)
    assert telemetry["schema_version"] == 1
    assert telemetry["device_id"] == "cardioia-esp32-01"
    assert telemetry["sequence"] == 42
    assert telemetry["source"] == "live"
    assert telemetry["sensor_valid"] is True
    assert status == {
        "schema_version": 1,
        "device_id": "cardioia-esp32-01",
        "state": "online",
        "buffer_pending": 3,
        "dropped_samples": 1,
        "uptime_ms": 220000,
    }
    print("Payload MQTT: 13 campos de telemetria e status JSON aprovados.")


if __name__ == "__main__":
    main()
