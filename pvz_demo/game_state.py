from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple

from pvz_demo.models import Plant
from pvz_demo.settings import GRID_COLS, GRID_ROWS, INITIAL_SUN, PlantType


@dataclass
class GameState:
    sun: int = INITIAL_SUN
    rows: int = GRID_ROWS
    cols: int = GRID_COLS
    plants: Dict[Tuple[int, int], Plant] = field(default_factory=dict)
    selected_plant: Optional[PlantType] = None
    is_game_over: bool = False

    def is_inside_grid(self, row: int, col: int) -> bool:
        return 0 <= row < self.rows and 0 <= col < self.cols

    def get_plant(self, row: int, col: int) -> Optional[Plant]:
        return self.plants.get((row, col))
