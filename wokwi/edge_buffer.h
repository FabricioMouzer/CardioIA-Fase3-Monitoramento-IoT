#pragma once

#include <stddef.h>

// FIFO circular de capacidade fixa. Quando cheio, preserva as amostras mais
// recentes, substitui a mais antiga e registra o descarte explicitamente.
template <typename T, size_t Capacity>
class EdgeBuffer {
 public:
  static_assert(Capacity > 0, "EdgeBuffer requer capacidade maior que zero");

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

  bool pop(T& value) {
    if (count_ == 0) return false;
    value = values_[head_];
    head_ = (head_ + 1) % Capacity;
    --count_;
    return true;
  }

  bool front(T& value) const {
    if (count_ == 0) return false;
    value = values_[head_];
    return true;
  }

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
