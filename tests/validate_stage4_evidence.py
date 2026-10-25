#!/usr/bin/env python3
"""Valida as evidências reais da Etapa 4 sem depender do broker ao vivo."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WOKWI = ROOT / "evidencias/etapa-4/E4-05-log-wokwi-serial.txt"
SUBSCRIBER = ROOT / "evidencias/etapa-4/E4-06-log-assinante-hivemq.txt"

TOPIC_ROOT = "cardioia/fase3/rm566777/cardioia-esp32-01"
REQUIRED_FIELDS = {
    "schema_version",
    "device_id",
    "sequence",
    "captured_uptime_ms",
    "temperature_c",
    "humidity_pct",
    "bpm",
    "sensor_valid",
    "alert_code",
    "alert",
    "source",
    "buffer_pending",
    "dropped_samples",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def json_objects(text: str) -> list[dict]:
    objects: list[dict] = []
    for line in text.splitlines():
        start = line.find("{")
        if start < 0:
            continue
        try:
            objects.append(json.loads(line[start:]))
        except json.JSONDecodeError:
            continue
    return objects


def main() -> None:
    wokwi = WOKWI.read_text(encoding="utf-8")
    subscriber = SUBSCRIBER.read_text(encoding="utf-8")
    checks = 0

    require("MQTT_CONNECT_RESULT connected=true state=0" in wokwi,
            "Conexão MQTT não comprovada")
    checks += 1
    require("MQTT_STATUS state=online retained=true accepted=true" in wokwi,
            "Status retido não comprovado")
    checks += 1
    require(re.search(r"MQTT_PUBLISH seq=\d+ source=live .*accepted=true", wokwi),
            "Publicação ao vivo não comprovada")
    checks += 1
    require('"alert":"high_bpm"' in wokwi and "alert=true accepted=true" in wokwi,
            "Alerta de BPM alto não comprovado")
    checks += 1

    require("CONNECTIVITY state=disabled source=serial pending=0" in wokwi,
            "Desconexão controlada não comprovada")
    checks += 1
    require("CONNECTIVITY state=enabled source=serial pending=4" in wokwi,
            "Reconexão com quatro pendências não comprovada")
    checks += 1
    for sequence, pending_after in zip(range(32, 36), range(3, -1, -1)):
        token = (f"MQTT_PUBLISH seq={sequence} source=buffered "
                 f"telemetry=true alert=true accepted=true pending_after={pending_after}")
        require(token in wokwi, f"FIFO ausente ou fora de ordem na sequência {sequence}")
    checks += 4
    require("SYNC_DONE sent=4 pending=0 dropped_samples=0" in wokwi,
            "Sincronização final não zerou o buffer")
    checks += 1

    for suffix in ("telemetria", "alerta", "status"):
        require(f"Topic: {TOPIC_ROOT}/{suffix}" in subscriber,
                f"Assinante não recebeu o tópico {suffix}")
    checks += 3
    require("Retained" in subscriber and '"state":"offline_unexpected"' in subscriber,
            "Assinante não comprovou uma mensagem de status retida")
    checks += 1

    payloads = [obj for obj in json_objects(subscriber) if "sequence" in obj]
    require(payloads, "Nenhum payload JSON de telemetria foi extraído")
    require(all(REQUIRED_FIELDS <= obj.keys() for obj in payloads),
            "Há payload externo sem todos os 13 campos")
    checks += 2
    require(any(obj.get("alert") == "high_bpm" and obj.get("bpm") == 180
                for obj in payloads), "Alerta externo high_bpm ausente")
    checks += 1
    buffered = {obj.get("sequence") for obj in payloads
                if obj.get("source") == "buffered"}
    require({32, 33, 34, 35} <= buffered,
            "Assinante não recebeu todas as quatro amostras sincronizadas")
    checks += 1
    require(all(obj.get("schema_version") == 1 and
                obj.get("device_id") == "cardioia-esp32-01"
                for obj in payloads), "Versão ou device_id divergente")
    checks += 1

    print(f"Etapa 4: {checks} verificações de evidência MQTT aprovadas.")


if __name__ == "__main__":
    main()
