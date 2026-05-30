from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from pvz_demo.settings import PlantType


@dataclass
class Plant:
    plant_type: PlantType
    row: int
    col: int
    health: int = 100
    sun_timer: float = 0.0
    shoot_timer: float = 0.0


@dataclass
class Sun:
    x: float
    y: float
    target_y: float
    value: int
    lifetime: float
    fall_speed: float
    age: float = 0.0
    row: Optional[int] = None
    col: Optional[int] = None

    def contains_point(self, x: float, y: float, radius: float) -> bool:
        dx = self.x - x
        dy = self.y - y
        return dx * dx + dy * dy <= radius * radius


@dataclass
class Zombie:
    row: int
    x: float
    health: int
    speed: float


@dataclass
class Pea:
    row: int
    x: float
    damage: int
    speed: float
