"""Valida a evidência real do ciclo online → offline → sincronização."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "evidencias/etapa-3/E3-06-log-final-ciclo-correlacionado.txt"


def sequences(pattern: str, content: str) -> list[int]:
    return [int(value) for value in re.findall(pattern, content)]


def main() -> None:
    content = LOG.read_text(encoding="utf-8")
    stored = sequences(r"BUFFER_STORE seq=(\d+)", content)
    synchronized = sequences(r"CLOUD_SEND seq=(\d+) source=buffered", content)

    assert content.count("BOOT CardioIA") == 1
    assert "EDGE_BUFFER capacity=2160 interval_ms=5000 retention_hours=3" in content
    assert "CONNECTIVITY state=offline source=serial pending=0" in content
    assert stored == [2, 3, 4]
    assert "CONNECTIVITY state=online source=serial pending=3" in content
    assert "SYNC_START pending=3 dropped_samples=0" in content
    assert synchronized == stored
    assert len(synchronized) == len(set(synchronized))
    assert "SYNC_DONE sent=3 pending=0 dropped_samples=0" in content
    assert "CLOUD_SEND seq=1 source=live" in content

    print("Runtime Etapa 3: 10/10 verificações aprovadas; sem duplicação ou perda.")


if __name__ == "__main__":
    main()
