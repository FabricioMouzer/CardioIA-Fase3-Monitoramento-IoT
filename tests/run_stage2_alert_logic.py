"""Compila e executa a lógica C++ usada diretamente pelo firmware."""

import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HEADER = ROOT / "wokwi/alert_logic.h"

TEST_PROGRAM = r'''
#include <assert.h>
#include "alert_logic.h"

int main() {
  assert(calculateAlert(36.5F, 80, true) == ALERT_NONE);
  assert(calculateAlert(38.0F, 50, true) == ALERT_NONE);
  assert(calculateAlert(38.0F, 120, true) == ALERT_NONE);
  assert(calculateAlert(36.5F, 49, true) == ALERT_BPM_LOW);
  assert(calculateAlert(36.5F, 121, true) == ALERT_BPM_HIGH);
  assert(calculateAlert(38.1F, 80, true) == ALERT_TEMP_HIGH);
  assert(calculateAlert(0.0F, 80, false) == ALERT_SENSOR_ERROR);
  assert(calculateAlert(39.0F, 130, true) ==
         (ALERT_TEMP_HIGH | ALERT_BPM_HIGH));
  return 0;
}
'''


def main() -> None:
    assert HEADER.is_file(), HEADER
    with tempfile.TemporaryDirectory() as temporary:
        source = Path(temporary) / "stage2_alert_test.cpp"
        binary = Path(temporary) / "stage2_alert_test"
        source.write_text(TEST_PROGRAM, encoding="utf-8")
        subprocess.run(
            [
                "g++",
                "-std=c++11",
                "-Wall",
                "-Wextra",
                "-Werror",
                f"-I{HEADER.parent}",
                str(source),
                "-o",
                str(binary),
            ],
            check=True,
        )
        subprocess.run([str(binary)], check=True)
    print("Lógica C++: 8 cenários de alerta aprovados.")


if __name__ == "__main__":
    main()
