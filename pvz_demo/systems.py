from __future__ import annotations

from dataclasses import dataclass

from pvz_demo.game_state import GameState
from pvz_demo.models import Plant
from pvz_demo.settings import PLANT_COSTS, PlantType


@dataclass(frozen=True)
class PlantingResult:
    success: bool
    reason: str


def can_plant(state: GameState, plant_type: PlantType, row: int, col: int) -> PlantingResult:
    if not state.is_inside_grid(row, col):
        return PlantingResult(False, "outside_grid")

    if state.get_plant(row, col) is not None:
        return PlantingResult(False, "cell_occupied")

    cost = PLANT_COSTS[plant_type]
    if state.sun < cost:
        return PlantingResult(False, "not_enough_sun")

    return PlantingResult(True, "ok")


def plant_at(state: GameState, plant_type: PlantType, row: int, col: int) -> PlantingResult:
    result = can_plant(state, plant_type, row, col)
    if not result.success:
        return result

    cost = PLANT_COSTS[plant_type]
    state.sun -= cost
    state.plants[(row, col)] = Plant(plant_type=plant_type, row=row, col=col)
    return result
