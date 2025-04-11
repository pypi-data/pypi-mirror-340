from __future__ import annotations

from typing import List

from pokerengine.enums import Action, Position
from pokerengine.engine import EngineRake01, EngineTraits, PlayerAction


def print_actions(actions: List[PlayerAction]) -> None:
    for action in actions:
        print(action.action.name, action.position.name, action.amount)


engine = EngineRake01(engine_traits=EngineTraits(sb_bet=10, bb_bet=20, bb_mult=15, min_raise=20))
engine.add_player(stack=300, id="1", parameters=None)
engine.add_player(stack=300, id="2", parameters=None)

engine.start(is_new_game=False)

print_actions(engine.possible_actions)
print("\n")
engine.execute(player_action=PlayerAction(
    action=Action.RAISE,
    position=Position.SB,
    amount=20,
))
print(engine.pot, engine.engine_traits.min_raise)
print_actions(engine.possible_actions)
print("\n")
engine.execute(player_action=PlayerAction(
    action=Action.RAISE,
    position=Position.BB,
    amount=60,
))
print(engine.pot, engine.engine_traits.min_raise)
print_actions(engine.possible_actions)
print("\n")
engine.execute(player_action=PlayerAction(
    action=Action.RAISE,
    position=Position.SB,
    amount=50,
))
print(engine.pot, engine.engine_traits.min_raise)
print_actions(engine.possible_actions)
print("\n")