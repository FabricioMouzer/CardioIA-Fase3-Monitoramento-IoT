#pragma once

#include <stddef.h>

// ============================================================================
// CardioIA Fase 3 — Buffer Circular FIFO para Resiliência Offline (Edge)
// ============================================================================
// Implementa uma fila circular estática (sem alocação dinâmica no heap para
// evitar fragmentação de memória no ESP32).
// - Capacidade padrão no projeto: 2.160 amostras (3 horas a 1 amostra / 5s),
//   ocupando exatamente 2.160 * 20 bytes = 43.200 bytes (43,2 KB) de SRAM.
// - Política de estouro (overflow): quando cheio, preserva as amostras mais
//   recentes, sobrescreve a amostra mais antiga (avançando head_) e incrementa
//   o contador auditável dropped_.
template <typename T, size_t Capacity>
class EdgeBuffer {
 public:
  static_assert(Capacity > 0, "EdgeBuffer requer capacidade maior que zero");

  // Insere uma nova amostra no final da fila (tail).
  // Retorna true se houve sobrescrita da amostra mais antiga por buffer cheio.
  bool push(const T& value) {
    bool overwritten = false;
    if (count_ == Capacity) {
      head_ = (head_ + 1) % Capacity;
      --count_;
      ++dropped_;
      overwritten = true;
    }

    const size_t tail = (head_ + count_) % Capacity;
    values_[tail] = value;
    ++count_;
    return overwritten;
  }

  // Remove e copia a amostra mais antiga (FIFO). Retorna false se vazio.
  bool pop(T& value) {
    if (count_ == 0) return false;
    value = values_[head_];
    head_ = (head_ + 1) % Capacity;
    --count_;
    return true;
  }

  // Inspeciona a amostra mais antiga sem removê-la da fila (usado antes do
  // envio MQTT para garantir que a amostra só seja descartada após aceite).
  bool front(T& value) const {
    if (count_ == 0) return false;
    value = values_[head_];
    return true;
  }

  // Confirma a remoção da amostra mais antiga após publicação MQTT bem-sucedida.
  bool discardFront() {
    if (count_ == 0) return false;
    head_ = (head_ + 1) % Capacity;
    --count_;
    return true;
  }

  size_t size() const { return count_; }
  constexpr size_t capacity() const { return Capacity; }
  unsigned long dropped() const { return dropped_; }
  bool empty() const { return count_ == 0; }

 private:
  T values_[Capacity]{};
  size_t head_ = 0;
  size_t count_ = 0;
  unsigned long dropped_ = 0;
};
