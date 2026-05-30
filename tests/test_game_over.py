from pvz_demo.game_state import GameState
from pvz_demo.systems import spawn_zombie, update_combat, update_game_over


def test_game_continues_when_zombie_has_not_reached_left_edge():
    state = GameState()
    spawn_zombie(state, row=2, x=1)

    update_game_over(state)

    assert state.is_game_over is False


def test_game_over_when_zombie_reaches_left_edge():
    state = GameState()
    spawn_zombie(state, row=2, x=0)

    update_game_over(state)

    assert state.is_game_over is True


def test_game_over_when_zombie_passes_left_edge():
    state = GameState()
    spawn_zombie(state, row=2, x=-1)

    update_game_over(state)

    assert state.is_game_over is True


def test_combat_update_checks_game_over_after_zombies_move():
    state = GameState()
    spawn_zombie(state, row=2, x=1)

    update_combat(state, dt=4.0)

    assert state.is_game_over is True
