from __future__ import annotations

from pathlib import Path

import pygame

from pvz_demo.game_state import GameState
from pvz_demo.layout import Layout, cell_center
from pvz_demo.settings import PLANT_COSTS, PlantType


BACKGROUND = (120, 185, 224)
TOOLBAR = (37, 47, 45)
GRASS_A = (83, 166, 70)
GRASS_B = (74, 150, 65)
GRID_LINE = (45, 112, 49)
WHITE = (245, 245, 245)
BLACK = (25, 25, 25)
YELLOW = (250, 210, 58)
GOLD = (183, 138, 30)
SUNFLOWER = (234, 180, 36)
PEASHOOTER = (38, 130, 68)
PEA = (84, 205, 70)
ZOMBIE = (110, 112, 116)
SELECTED = (255, 255, 255)
GAME_OVER_OVERLAY = (30, 30, 30)
HEALTH_BG = (55, 55, 55)
HEALTH_FG = (76, 190, 88)
ASSET_DIR = Path(__file__).resolve().parent.parent / "assets" / "sprites"
_SPRITES = None


def draw_game(screen: pygame.Surface, state: GameState, layout: Layout, font: pygame.font.Font) -> None:
    screen.fill(BACKGROUND)
    draw_toolbar(screen, state, layout, font)
    draw_lawn(screen, layout)
    draw_entities(screen, state, layout, font)
    if state.is_game_over:
        draw_game_over(screen, layout, font)


def get_sprites() -> dict:
    global _SPRITES
    if _SPRITES is not None:
        return _SPRITES

    _SPRITES = {}
    for name in ("sunflower", "peashooter", "zombie", "sun", "pea"):
        path = ASSET_DIR / "{}.png".format(name)
        if path.exists():
            _SPRITES[name] = pygame.image.load(str(path)).convert_alpha()
    return _SPRITES


def blit_fit(
    screen: pygame.Surface,
    image: pygame.Surface,
    center_x: int,
    center_y: int,
    max_width: int,
    max_height: int,
) -> None:
    width, height = image.get_size()
    scale = min(max_width / width, max_height / height)
    new_size = (max(1, int(width * scale)), max(1, int(height * scale)))
    scaled = pygame.transform.smoothscale(image, new_size)
    screen.blit(scaled, (center_x - new_size[0] // 2, center_y - new_size[1] // 2))


def draw_toolbar(screen: pygame.Surface, state: GameState, layout: Layout, font: pygame.font.Font) -> None:
    pygame.draw.rect(screen, TOOLBAR, (0, 0, layout.width, 96))
    pygame.draw.rect(screen, (69, 88, 65), (16, 20, 132, 58), border_radius=8)
    pygame.draw.circle(screen, YELLOW, (42, 49), 16)
    pygame.draw.circle(screen, GOLD, (42, 49), 16, width=2)
    sun_text = font.render("Sun: {}".format(state.sun), True, WHITE)
    screen.blit(sun_text, (66, 38))
    draw_card(screen, font, layout.sunflower_card, "Sunflower", PLANT_COSTS[PlantType.SUNFLOWER], state.selected_plant == PlantType.SUNFLOWER)
    draw_card(screen, font, layout.peashooter_card, "Peashooter", PLANT_COSTS[PlantType.PEASHOOTER], state.selected_plant == PlantType.PEASHOOTER)


def draw_card(screen: pygame.Surface, font: pygame.font.Font, rect, name: str, cost: int, selected: bool) -> None:
    color = (72, 93, 79) if not selected else (104, 133, 91)
    pygame.draw.rect(screen, color, rect, border_radius=6)
    pygame.draw.rect(screen, SELECTED if selected else (30, 38, 34), rect, width=2, border_radius=6)
    label = font.render(name, True, WHITE)
    price = font.render(str(cost), True, YELLOW)
    screen.blit(label, (rect[0] + 8, rect[1] + 8))
    screen.blit(price, (rect[0] + 8, rect[1] + 32))


def draw_lawn(screen: pygame.Surface, layout: Layout) -> None:
    for row in range(5):
        for col in range(9):
            rect = (
                layout.lawn_x + col * layout.cell_size,
                layout.lawn_y + row * layout.cell_size,
                layout.cell_size,
                layout.cell_size,
            )
            pygame.draw.rect(screen, GRASS_A if (row + col) % 2 == 0 else GRASS_B, rect)
            pygame.draw.rect(screen, GRID_LINE, rect, width=1)


def draw_entities(screen: pygame.Surface, state: GameState, layout: Layout, font: pygame.font.Font) -> None:
    sprites = get_sprites()
    for plant in state.plants.values():
        x, y = cell_center(layout, plant.row, plant.col)
        sprite_name = "sunflower" if plant.plant_type == PlantType.SUNFLOWER else "peashooter"
        if sprite_name in sprites:
            blit_fit(screen, sprites[sprite_name], x, y - layout.cell_size // 10, int(layout.cell_size * 0.9), int(layout.cell_size * 0.95))
        else:
            rect = (x - layout.cell_size // 3, y - layout.cell_size // 3, layout.cell_size * 2 // 3, layout.cell_size * 2 // 3)
            color = SUNFLOWER if plant.plant_type == PlantType.SUNFLOWER else PEASHOOTER
            pygame.draw.rect(screen, color, rect, border_radius=6)
            label = "S" if plant.plant_type == PlantType.SUNFLOWER else "P"
            screen.blit(font.render(label, True, BLACK), (x - 6, y - 10))
        draw_health_bar(screen, x - layout.cell_size // 3, y + layout.cell_size // 3 + 4, layout.cell_size * 2 // 3, plant.health / 100)

    for sun in state.suns:
        if sun.row is not None and sun.col is not None:
            x, y = cell_center(layout, sun.row, sun.col)
        else:
            x, y = int(sun.x), int(sun.y)
        if "sun" in sprites:
            blit_fit(screen, sprites["sun"], x, y, int(layout.cell_size * 0.58), int(layout.cell_size * 0.58))
        else:
            pygame.draw.circle(screen, YELLOW, (x, y), max(12, layout.cell_size // 6))

    for pea in state.peas:
        x, y = cell_center(layout, pea.row, pea.x)
        if "pea" in sprites:
            blit_fit(screen, sprites["pea"], x, y, int(layout.cell_size * 0.18), int(layout.cell_size * 0.18))
        else:
            pygame.draw.circle(screen, PEA, (x, y), max(5, layout.cell_size // 12))

    for zombie in state.zombies:
        x, y = cell_center(layout, zombie.row, zombie.x)
        if "zombie" in sprites:
            blit_fit(screen, sprites["zombie"], x, y - layout.cell_size // 8, int(layout.cell_size * 0.85), int(layout.cell_size * 1.2))
        else:
            rect = (x - layout.cell_size // 4, y - layout.cell_size // 3, layout.cell_size // 2, layout.cell_size * 2 // 3)
            pygame.draw.rect(screen, ZOMBIE, rect, border_radius=4)
        health = font.render(str(int(zombie.health)), True, WHITE)
        screen.blit(health, (x - 12, y - layout.cell_size // 2))
        draw_health_bar(screen, x - layout.cell_size // 4, y + layout.cell_size // 3 + 4, layout.cell_size // 2, zombie.health / 100)


def draw_health_bar(screen: pygame.Surface, x: int, y: int, width: int, ratio: float) -> None:
    ratio = max(0.0, min(1.0, ratio))
    pygame.draw.rect(screen, HEALTH_BG, (x, y, width, 5), border_radius=2)
    pygame.draw.rect(screen, HEALTH_FG, (x, y, int(width * ratio), 5), border_radius=2)


def draw_game_over(screen: pygame.Surface, layout: Layout, font: pygame.font.Font) -> None:
    overlay = pygame.Surface((layout.width, layout.height), pygame.SRCALPHA)
    overlay.fill((*GAME_OVER_OVERLAY, 160))
    screen.blit(overlay, (0, 0))
    text = font.render("Game Over", True, WHITE)
    screen.blit(text, (layout.width // 2 - text.get_width() // 2, layout.height // 2 - text.get_height() // 2))
