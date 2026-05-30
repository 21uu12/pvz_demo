from __future__ import annotations

from pvz_demo.game_state import GameState
from pvz_demo.layout import Layout, cell_center, point_in_rect, screen_to_cell
from pvz_demo.settings import SUN_CLICK_RADIUS, PlantType
from pvz_demo.systems import collect_sun_at, plant_at


def handle_click(state: GameState, layout: Layout, x: int, y: int) -> None:
    if state.is_game_over:
        return

    if point_in_rect(x, y, layout.sunflower_card):
        state.selected_plant = PlantType.SUNFLOWER
        return

    if point_in_rect(x, y, layout.peashooter_card):
        state.selected_plant = PlantType.PEASHOOTER
        return

    if collect_visible_sun(state, layout, x, y):
        return

    cell = screen_to_cell(layout, x, y)
    if cell is None or state.selected_plant is None:
        return

    row, col = cell
    result = plant_at(state, state.selected_plant, row, col)
    if result.success:
        state.selected_plant = None


def collect_visible_sun(state: GameState, layout: Layout, x: int, y: int) -> bool:
    for sun in list(state.suns):
        if sun.row is None or sun.col is None:
            continue

        sun_x, sun_y = cell_center(layout, sun.row, sun.col)
        dx = sun_x - x
        dy = sun_y - y
        if dx * dx + dy * dy <= SUN_CLICK_RADIUS * SUN_CLICK_RADIUS:
            state.sun += sun.value
            state.suns.remove(sun)
            return True

    return collect_sun_at(state, x, y)
