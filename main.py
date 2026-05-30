from __future__ import annotations

import random
import sys

import pygame

from pvz_demo.game_state import GameState
from pvz_demo.input_handler import handle_click
from pvz_demo.layout import build_layout
from pvz_demo.renderer import draw_game
from pvz_demo.settings import GRID_COLS, GRID_ROWS
from pvz_demo.systems import (
    spawn_sky_sun,
    spawn_zombie,
    update_combat,
    update_sunflowers,
    update_suns,
)


WINDOW_SIZE = (900, 600)
FPS = 60
SKY_SUN_INTERVAL = 4.0
ZOMBIE_INTERVAL = 6.0


def main() -> int:
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
    pygame.display.set_caption("PVZ Demo")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 20)
    state = GameState()
    sky_sun_timer = 1.0
    zombie_timer = 2.0

    while True:
        dt = clock.tick(FPS) / 1000.0
        layout = build_layout(*screen.get_size())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                return 0
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                handle_click(state, layout, *event.pos)

        if not state.is_game_over:
            sky_sun_timer -= dt
            zombie_timer -= dt

            if sky_sun_timer <= 0:
                x = random.randint(layout.lawn_x + 20, layout.lawn_x + layout.lawn_width - 20)
                target_y = random.randint(layout.lawn_y + 20, layout.lawn_y + layout.lawn_height // 2)
                spawn_sky_sun(state, x=x, start_y=20, target_y=target_y)
                sky_sun_timer = SKY_SUN_INTERVAL

            if zombie_timer <= 0:
                row = random.randrange(GRID_ROWS)
                spawn_zombie(state, row=row, x=GRID_COLS - 0.5)
                zombie_timer = ZOMBIE_INTERVAL

            update_suns(state, dt)
            update_sunflowers(state, dt)
            update_combat(state, dt)

        draw_game(screen, state, layout, font)
        pygame.display.flip()


if __name__ == "__main__":
    sys.exit(main())
