from __future__ import annotations

import pygame

from pvz_demo.game_state import GameState
from pvz_demo.layout import Layout, cell_center
from pvz_demo.settings import PLANT_COSTS, PlantType


BACKGROUND = (126, 190, 230)
TOOLBAR = (42, 48, 56)
GRASS_A = (83, 166, 70)
GRASS_B = (74, 150, 65)
GRID_LINE = (45, 112, 49)
WHITE = (245, 245, 245)
BLACK = (25, 25, 25)
YELLOW = (250, 210, 58)
SUNFLOWER = (234, 180, 36)
PEASHOOTER = (38, 130, 68)
PEA = (84, 205, 70)
ZOMBIE = (110, 112, 116)
SELECTED = (255, 255, 255)
GAME_OVER_OVERLAY = (30, 30, 30)


def draw_game(screen: pygame.Surface, state: GameState, layout: Layout, font: pygame.font.Font) -> None:
    screen.fill(BACKGROUND)
    draw_toolbar(screen, state, layout, font)
    draw_lawn(screen, layout)
    draw_entities(screen, state, layout, font)
    if state.is_game_over:
        draw_game_over(screen, layout, font)


def draw_toolbar(screen: pygame.Surface, state: GameState, layout: Layout, font: pygame.font.Font) -> None:
    pygame.draw.rect(screen, TOOLBAR, (0, 0, layout.width, 96))
    sun_text = font.render("Sun: {}".format(state.sun), True, WHITE)
    screen.blit(sun_text, (16, 68))
    draw_card(screen, font, layout.sunflower_card, "Sunflower", PLANT_COSTS[PlantType.SUNFLOWER], state.selected_plant == PlantType.SUNFLOWER)
    draw_card(screen, font, layout.peashooter_card, "Peashooter", PLANT_COSTS[PlantType.PEASHOOTER], state.selected_plant == PlantType.PEASHOOTER)


def draw_card(screen: pygame.Surface, font: pygame.font.Font, rect, name: str, cost: int, selected: bool) -> None:
    color = (75, 91, 78) if not selected else (102, 122, 92)
    pygame.draw.rect(screen, color, rect, border_radius=6)
    pygame.draw.rect(screen, SELECTED if selected else BLACK, rect, width=2, border_radius=6)
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
    for plant in state.plants.values():
        x, y = cell_center(layout, plant.row, plant.col)
        rect = (x - layout.cell_size // 3, y - layout.cell_size // 3, layout.cell_size * 2 // 3, layout.cell_size * 2 // 3)
        color = SUNFLOWER if plant.plant_type == PlantType.SUNFLOWER else PEASHOOTER
        pygame.draw.rect(screen, color, rect, border_radius=6)
        label = "S" if plant.plant_type == PlantType.SUNFLOWER else "P"
        screen.blit(font.render(label, True, BLACK), (x - 6, y - 10))

    for sun in state.suns:
        if sun.row is not None and sun.col is not None:
            x, y = cell_center(layout, sun.row, sun.col)
        else:
            x, y = int(sun.x), int(sun.y)
        pygame.draw.circle(screen, YELLOW, (x, y), max(12, layout.cell_size // 6))

    for pea in state.peas:
        x, y = cell_center(layout, pea.row, pea.x)
        pygame.draw.circle(screen, PEA, (x, y), max(5, layout.cell_size // 12))

    for zombie in state.zombies:
        x, y = cell_center(layout, zombie.row, zombie.x)
        rect = (x - layout.cell_size // 4, y - layout.cell_size // 3, layout.cell_size // 2, layout.cell_size * 2 // 3)
        pygame.draw.rect(screen, ZOMBIE, rect, border_radius=4)
        health = font.render(str(zombie.health), True, WHITE)
        screen.blit(health, (x - 12, y - layout.cell_size // 2))


def draw_game_over(screen: pygame.Surface, layout: Layout, font: pygame.font.Font) -> None:
    overlay = pygame.Surface((layout.width, layout.height), pygame.SRCALPHA)
    overlay.fill((*GAME_OVER_OVERLAY, 160))
    screen.blit(overlay, (0, 0))
    text = font.render("Game Over", True, WHITE)
    screen.blit(text, (layout.width // 2 - text.get_width() // 2, layout.height // 2 - text.get_height() // 2))
