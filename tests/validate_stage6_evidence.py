#!/usr/bin/env python3
"""Valida as evidências do teste integrado e repetível da Etapa 6."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidencias" / "etapa-6"
LOG_A = (EVIDENCE / "E6-03-execucao-a-log.txt").read_text(encoding="utf-8")
LOG_B = (EVIDENCE / "E6-08-execucao-b-log.txt").read_text(encoding="utf-8")
checks = 0


def require(condition: bool, message: str) -> None:
    global checks
    assert condition, message
    checks += 1


def contains(log: str, fragment: str) -> None:
    require(fragment in log, f"Trecho ausente: {fragment}")


def in_order(log: str, fragments: list[str]) -> None:
    cursor = 0
    for fragment in fragments:
        position = log.find(fragment, cursor)
        require(position >= cursor, f"Ordem inválida ou trecho ausente: {fragment}")
        cursor = position + len(fragment)


# Integridade básica dos arquivos visuais.
images = [
    "E6-02-execucao-a-bpm-alto.jpg",
    "E6-04-execucao-a-wokwi.jpg",
    "E6-05-execucao-a-sincronizada.jpg",
    "E6-06-execucao-b-bpm-baixo.jpg",
    "E6-07-execucao-b-falha-dht.jpg",
    "E6-09-execucao-b-wokwi.jpg",
    "E6-10-execucao-b-final-normal.jpg",
]
require(all((EVIDENCE / name).stat().st_size > 50_000 for name in images), "Captura vazia ou incompleta")
require(all((EVIDENCE / name).read_bytes().startswith(b"\xff\xd8\xff") for name in images), "JPEG inválido")

# Execução A: normal → BPM alto → normal → offline → sincronização → live.
contains(LOG_A, "SAMPLE seq=2 uptime_ms=9148 temp=36.5C humidity=55.0% bpm=110 sensor_valid=true alert_code=0 alert=normal")
contains(LOG_A, "SAMPLE seq=4 uptime_ms=19153 temp=36.5C humidity=55.0% bpm=163 sensor_valid=true alert_code=2 alert=high_bpm")
contains(LOG_A, "SAMPLE seq=10 uptime_ms=49194 temp=36.5C humidity=55.0% bpm=110 sensor_valid=true alert_code=0 alert=normal")
contains(LOG_A, "CONNECTIVITY state=disabled source=serial pending=0")
for sequence, pending in zip(range(12, 21), range(1, 10)):
    contains(LOG_A, f"BUFFER_STORE seq={sequence} reason=network_disabled pending={pending} capacity=2160 dropped_samples=0 overwritten=false")
sync_a = LOG_A[LOG_A.rfind("CONNECTIVITY state=enabled source=serial pending=9") :]
contains(sync_a, "SYNC_START pending=9 dropped_samples=0")
in_order(
    sync_a,
    [
        f"MQTT_PUBLISH seq={sequence} source=buffered telemetry=true alert=true accepted=true pending_after={pending}"
        for sequence, pending in zip(range(12, 21), range(8, -1, -1))
    ],
)
contains(sync_a, "SYNC_DONE sent=9 pending=0 dropped_samples=0")
contains(sync_a, "MQTT_PUBLISH seq=21 source=live telemetry=true alert=true accepted=true pending_after=0")

# Execução B: reinício independente, BPM baixo, falha/recuperação e limites inclusivos.
contains(LOG_B, "SAMPLE seq=1 uptime_ms=1718 temp=36.5C humidity=55.0% bpm=110 sensor_valid=true alert_code=0 alert=normal")
contains(LOG_B, "SAMPLE seq=5 uptime_ms=23740 temp=36.5C humidity=55.0% bpm=42 sensor_valid=true alert_code=1 alert=low_bpm")
in_order(
    LOG_B,
    [
        "SAMPLE seq=5 uptime_ms=23740 temp=36.5C humidity=55.0% bpm=42 sensor_valid=true alert_code=1 alert=low_bpm",
        "SAMPLE seq=10 uptime_ms=48774 temp=-999.0C humidity=-1.0% bpm=110 sensor_valid=false alert_code=8 alert=sensor_error",
        "SAMPLE seq=14 uptime_ms=68801 temp=36.5C humidity=55.0% bpm=110 sensor_valid=true alert_code=0 alert=normal",
    ],
)
contains(LOG_B, "SAMPLE seq=20 uptime_ms=98831 temp=36.5C humidity=55.0% bpm=50 sensor_valid=true alert_code=0 alert=normal")
contains(LOG_B, "SAMPLE seq=21 uptime_ms=103838 temp=36.5C humidity=55.0% bpm=120 sensor_valid=true alert_code=0 alert=normal")
contains(LOG_B, "SAMPLE seq=26 uptime_ms=128861 temp=38.0C humidity=55.0% bpm=120 sensor_valid=true alert_code=0 alert=normal")
contains(LOG_B, "SAMPLE seq=28 uptime_ms=138872 temp=36.5C humidity=55.0% bpm=110 sensor_valid=true alert_code=0 alert=normal")
require("dropped_samples=1" not in LOG_A + LOG_B, "Foi detectado descarte de amostra")
require("SAMPLE seq=1 " in LOG_A and "SAMPLE seq=1 " in LOG_B, "Reinício da sequência não comprovado nas duas execuções")

print(f"Etapa 6: {checks} verificações de evidência integrada aprovadas.")
