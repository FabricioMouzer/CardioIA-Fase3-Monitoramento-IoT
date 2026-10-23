import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def main() -> None:
    required = [
        "docs/ETAPA_1_MATRIZ_REQUISITOS.md",
        "docs/ETAPA_1_ARQUITETURA.md",
        "docs/ETAPA_1_CONTRATO_MQTT.md",
        "docs/ETAPA_1_AUDITORIA_PR10.md",
        "docs/ETAPA_1_REVISAO_GRUPO.md",
        "data/exemplo-telemetria-v1.json",
    ]
    for path in required:
        assert (ROOT / path).is_file(), path

    contract = read("docs/ETAPA_1_CONTRATO_MQTT.md")
    prefix = "cardioia/fase3/rm566777/cardioia-esp32-01"
    for suffix in ("telemetria", "alerta", "status"):
        assert f"{prefix}/{suffix}" in contract

    architecture = read("docs/ETAPA_1_ARQUITETURA.md")
    for term in ("DHT22", "Potenciômetro", "2.160", "FlowFuse Dashboard 2.0"):
        assert term in architecture

    payload = json.loads(read("data/exemplo-telemetria-v1.json"))
    required_fields = {
        "schema_version", "device_id", "sequence", "captured_uptime_ms",
        "temperature_c", "humidity_pct", "bpm", "sensor_valid",
        "alert_code", "alert", "source", "buffer_pending", "dropped_samples",
    }
    assert set(payload) == required_fields
    assert payload["schema_version"] == 1
    assert payload["device_id"] == "cardioia-esp32-01"
    assert 40 <= payload["bpm"] <= 180
    assert payload["source"] in {"live", "buffered"}

    review = read("docs/ETAPA_1_REVISAO_GRUPO.md")
    assert review.count("Aguardando confirmação") == 4
    print("Etapa 1: 6 arquivos, 3 tópicos e contrato JSON validados.")


if __name__ == "__main__":
    main()
