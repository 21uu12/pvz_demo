from __future__ import annotations

from enum import Enum


GRID_ROWS = 5
GRID_COLS = 9
INITIAL_SUN = 150
SUN_VALUE = 25
SKY_SUN_FALL_SPEED = 80
SUN_LIFETIME = 8.0
SUN_CLICK_RADIUS = 28
SUNFLOWER_INTERVAL = 7.0
PEASHOOTER_COOLDOWN = 1.5
PEA_SPEED = 220
PEA_DAMAGE = 20
ZOMBIE_HEALTH = 100
ZOMBIE_SPEED = 12
HIT_DISTANCE = 18
GAME_OVER_X = 0


class PlantType(str, Enum):
    SUNFLOWER = "sunflower"
    PEASHOOTER = "peashooter"


PLANT_COSTS: dict[PlantType, int] = {
    PlantType.SUNFLOWER: 50,
    PlantType.PEASHOOTER: 100,
}
