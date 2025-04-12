#ifndef POKERENGINE_PLAYER_HPP
#define POKERENGINE_PLAYER_HPP

#include <any>
#include <cstdint>
#include <string>
#include <vector>

#include <magic_enum/magic_enum.hpp>
#include <pybind11/pybind11.h>

#include "enums.hpp"
#include "pokerengine.hpp"

namespace pokerengine {
struct player {
  int32_t stack;
  int32_t bet;
  int32_t round_bet;
  enums::state state;

  std::string id;

  std::optional< std::map< std::string, pybind11::object > > parameters{ std::nullopt };

  auto operator<=>(const player &other) const noexcept -> std::strong_ordering = delete;
  auto operator==(const player &other) const noexcept -> bool = default;

  explicit operator std::string() const {
    using namespace std::literals;

    return "Player<stack="s + std::to_string(stack) + ", round_bet="s + std::to_string(round_bet) +
                    ", bet="s + std::to_string(bet) + ", stack="s + std::to_string(stack) + ", state="s +
                    std::string{ magic_enum::enum_name(state) } + ", id="s + id + ">"s;
  }
};
} // namespace pokerengine
#endif // POKERENGINE_PLAYER_HPP
