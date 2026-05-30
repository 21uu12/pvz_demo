from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from pvz_demo.settings import GRID_COLS, GRID_ROWS


TOOLBAR_HEIGHT = 96
CARD_WIDTH = 132
CARD_HEIGHT = 58
CARD_GAP = 12
SUN_CARD_X = 170
CARD_TOP = 20
LAWN_MARGIN = 24


@dataclass
class Layout:
    width: int
    height: int
    lawn_x: int
    lawn_y: int
    cell_size: int
    lawn_width: int
    lawn_height: int
    sunflower_card: Tuple[int, int, int, int]
    peashooter_card: Tuple[int, int, int, int]


def build_layout(width: int, height: int) -> Layout:
    available_width = max(1, width - LAWN_MARGIN * 2)
    available_height = max(1, height - TOOLBAR_HEIGHT - LAWN_MARGIN)
    cell_size = max(32, min(available_width // GRID_COLS, available_height // GRID_ROWS))
    lawn_width = cell_size * GRID_COLS
    lawn_height = cell_size * GRID_ROWS
    lawn_x = (width - lawn_width) // 2
    lawn_y = TOOLBAR_HEIGHT + max(0, (available_height - lawn_height) // 2)
    sunflower_card = (SUN_CARD_X, CARD_TOP, CARD_WIDTH, CARD_HEIGHT)
    peashooter_card = (SUN_CARD_X + CARD_WIDTH + CARD_GAP, CARD_TOP, CARD_WIDTH, CARD_HEIGHT)
    return Layout(
        width=width,
        height=height,
        lawn_x=lawn_x,
        lawn_y=lawn_y,
        cell_size=cell_size,
        lawn_width=lawn_width,
        lawn_height=lawn_height,
        sunflower_card=sunflower_card,
        peashooter_card=peashooter_card,
    )


def point_in_rect(x: int, y: int, rect: Tuple[int, int, int, int]) -> bool:
    rect_x, rect_y, rect_w, rect_h = rect
    return rect_x <= x <= rect_x + rect_w and rect_y <= y <= rect_y + rect_h


def screen_to_cell(layout: Layout, x: int, y: int) -> Optional[Tuple[int, int]]:
    if not (
        layout.lawn_x <= x < layout.lawn_x + layout.lawn_width
        and layout.lawn_y <= y < layout.lawn_y + layout.lawn_height
    ):
        return None
    col = (x - layout.lawn_x) // layout.cell_size
    row = (y - layout.lawn_y) // layout.cell_size
    return int(row), int(col)


def cell_center(layout: Layout, row: int, col: float) -> Tuple[int, int]:
    x = layout.lawn_x + int((col + 0.5) * layout.cell_size)
    y = layout.lawn_y + int((row + 0.5) * layout.cell_size)
    return x, y
