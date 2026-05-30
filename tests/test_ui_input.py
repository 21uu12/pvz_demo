from pvz_demo.game_state import GameState
from pvz_demo.input_handler import handle_click
from pvz_demo.layout import build_layout, cell_center, screen_to_cell
from pvz_demo.settings import PlantType
from pvz_demo.systems import spawn_sunflower_sun


def test_screen_to_cell_returns_lawn_cell():
    layout = build_layout(900, 600)
    x, y = cell_center(layout, row=2, col=3)

    assert screen_to_cell(layout, x, y) == (2, 3)


def test_screen_to_cell_returns_none_outside_lawn():
    layout = build_layout(900, 600)

    assert screen_to_cell(layout, 10, 10) is None


def test_clicking_sunflower_card_selects_sunflower():
    state = GameState()
    layout = build_layout(900, 600)
    x = layout.sunflower_card[0] + 5
    y = layout.sunflower_card[1] + 5

    handle_click(state, layout, x, y)

    assert state.selected_plant == PlantType.SUNFLOWER


def test_clicking_selected_plant_on_lawn_plants_it():
    state = GameState()
    layout = build_layout(900, 600)
    state.selected_plant = PlantType.SUNFLOWER
    x, y = cell_center(layout, row=1, col=2)

    handle_click(state, layout, x, y)

    assert state.get_plant(1, 2).plant_type == PlantType.SUNFLOWER
    assert state.selected_plant is None


def test_clicking_sunflower_sun_collects_it_from_cell_center():
    state = GameState(sun=0)
    layout = build_layout(900, 600)
    spawn_sunflower_sun(state, row=1, col=2)
    x, y = cell_center(layout, row=1, col=2)

    handle_click(state, layout, x, y)

    assert state.sun == 25
    assert state.suns == []
