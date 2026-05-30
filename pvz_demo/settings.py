from __future__ import annotations

from enum import Enum


GRID_ROWS = 5
GRID_COLS = 9
INITIAL_SUN = 150


class PlantType(str, Enum):
    SUNFLOWER = "sunflower"
    PEASHOOTER = "peashooter"


PLANT_COSTS: dict[PlantType, int] = {
    PlantType.SUNFLOWER: 50,
    PlantType.PEASHOOTER: 100,
}
