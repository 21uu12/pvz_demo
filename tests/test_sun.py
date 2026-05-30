from pvz_demo.game_state import GameState
from pvz_demo.settings import PlantType, SUN_VALUE, SUNFLOWER_INTERVAL
from pvz_demo.systems import (
    collect_sun_at,
    plant_at,
    spawn_sky_sun,
    update_sunflowers,
    update_suns,
)


def test_sky_sun_falls_until_target_y():
    state = GameState()
    sun = spawn_sky_sun(state, x=100, start_y=0, target_y=40)

    update_suns(state, dt=1.0)

    assert sun.y == 40
    assert sun in state.suns


def test_clicking_sun_collects_it_and_adds_sun_value():
    state = GameState(sun=0)
    spawn_sky_sun(state, x=100, start_y=50, target_y=50)

    collected = collect_sun_at(state, x=100, y=50)

    assert collected is True
    assert state.sun == SUN_VALUE
    assert state.suns == []


def test_clicking_empty_space_does_not_collect_sun():
    state = GameState(sun=0)
    spawn_sky_sun(state, x=100, start_y=50, target_y=50)

    collected = collect_sun_at(state, x=300, y=300)

    assert collected is False
    assert state.sun == 0
    assert len(state.suns) == 1


def test_expired_sun_is_removed():
    state = GameState()
    sun = spawn_sky_sun(state, x=100, start_y=50, target_y=50)

    update_suns(state, dt=sun.lifetime)

    assert state.suns == []


def test_sunflower_creates_sun_after_interval():
    state = GameState()
    plant_at(state, PlantType.SUNFLOWER, row=2, col=3)

    update_sunflowers(state, dt=SUNFLOWER_INTERVAL)

    assert len(state.suns) == 1
    assert state.suns[0].value == SUN_VALUE
    assert state.suns[0].row == 2
    assert state.suns[0].col == 3


def test_peashooter_does_not_create_sun():
    state = GameState()
    plant_at(state, PlantType.PEASHOOTER, row=2, col=3)

    update_sunflowers(state, dt=SUNFLOWER_INTERVAL)

    assert state.suns == []
