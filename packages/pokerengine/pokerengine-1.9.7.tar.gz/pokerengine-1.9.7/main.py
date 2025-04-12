from pokerengine.engine import EngineTraits, EngineRake01

engine = EngineRake01(engine_traits=EngineTraits(sb_bet=10, bb_bet=20, bb_mult=20, min_raise=20))
engine.add_player(stack=400, id="1", parameters=None)
engine.add_player(stack=400, id="2", parameters=None)
engine.start(is_new_game=True)

engine.execute(player_action=engine.possible_actions[1])
engine.execute(player_action=engine.possible_actions[1])

print(engine.pay_noshowdown())

for player in engine.players:
    print(player.stack)
    print(player.bet)
