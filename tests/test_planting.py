from pvz_demo.game_state import GameState
from pvz_demo.settings import INITIAL_SUN, PLANT_COSTS, PlantType
from pvz_demo.systems import plant_at


def test_can_plant_when_sun_is_enough_and_cell_is_empty():
    state = GameState()

    result = plant_at(state, PlantType.SUNFLOWER, row=2, col=3)

    assert result.success is True
    assert result.reason == "ok"
    assert state.get_plant(2, 3) is not None
    assert state.get_plant(2, 3).plant_type == PlantType.SUNFLOWER


def test_planting_success_spends_sun():
    state = GameState()

    plant_at(state, PlantType.PEASHOOTER, row=0, col=0)

    assert state.sun == INITIAL_SUN - PLANT_COSTS[PlantType.PEASHOOTER]


def test_cannot_plant_when_sun_is_not_enough():
    state = GameState(sun=25)

    result = plant_at(state, PlantType.PEASHOOTER, row=1, col=1)

    assert result.success is False
    assert result.reason == "not_enough_sun"
    assert state.get_plant(1, 1) is None
    assert state.sun == 25


def test_cannot_plant_twice_in_the_same_cell():
    state = GameState()
    plant_at(state, PlantType.SUNFLOWER, row=4, col=8)
    sun_after_first_plant = state.sun

    result = plant_at(state, PlantType.PEASHOOTER, row=4, col=8)

    assert result.success is False
    assert result.reason == "cell_occupied"
    assert state.get_plant(4, 8).plant_type == PlantType.SUNFLOWER
    assert state.sun == sun_after_first_plant


def test_cannot_plant_outside_grid():
    state = GameState()

    result = plant_at(state, PlantType.SUNFLOWER, row=5, col=0)

    assert result.success is False
    assert result.reason == "outside_grid"
    assert state.plants == {}
    assert state.sun == INITIAL_SUN
