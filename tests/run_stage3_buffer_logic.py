"""Compila e executa a mesma estrutura FIFO usada pelo firmware da Etapa 3."""

import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HEADER = ROOT / "wokwi/edge_buffer.h"

TEST_PROGRAM = r'''
#include <assert.h>
#include "edge_buffer.h"

struct TestSample { unsigned long sequence; };

int main() {
  EdgeBuffer<TestSample, 3> buffer;
  TestSample sample{};

  assert(buffer.capacity() == 3);
  assert(buffer.empty());
  assert(!buffer.pop(sample));

  assert(!buffer.push({1}));
  assert(!buffer.push({2}));
  assert(!buffer.push({3}));
  assert(buffer.size() == 3);
  assert(buffer.dropped() == 0);

  assert(buffer.push({4}));
  assert(buffer.size() == 3);
  assert(buffer.dropped() == 1);

  assert(buffer.pop(sample) && sample.sequence == 2);
  assert(buffer.pop(sample) && sample.sequence == 3);
  assert(buffer.pop(sample) && sample.sequence == 4);
  assert(buffer.empty());
  assert(!buffer.pop(sample));

  assert(!buffer.push({5}));
  assert(buffer.pop(sample) && sample.sequence == 5);
  assert(buffer.dropped() == 1);
  return 0;
}
'''


def main() -> None:
    assert HEADER.is_file(), HEADER
    with tempfile.TemporaryDirectory() as temporary:
        source = Path(temporary) / "stage3_buffer_test.cpp"
        binary = Path(temporary) / "stage3_buffer_test"
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
    print("Lógica FIFO C++: 18 verificações aprovadas.")


if __name__ == "__main__":
    main()
