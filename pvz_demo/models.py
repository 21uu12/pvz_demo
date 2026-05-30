from __future__ import annotations

from dataclasses import dataclass

from pvz_demo.settings import PlantType


@dataclass
class Plant:
    plant_type: PlantType
    row: int
    col: int
    health: int = 100
