from __future__ import annotations

from dataclasses import dataclass

from pvz_demo.game_state import GameState
from pvz_demo.models import Plant, Sun
from pvz_demo.settings import (
    PLANT_COSTS,
    SKY_SUN_FALL_SPEED,
    SUN_CLICK_RADIUS,
    SUN_LIFETIME,
    SUN_VALUE,
    SUNFLOWER_INTERVAL,
    PlantType,
)


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


def spawn_sky_sun(state: GameState, x: float, start_y: float, target_y: float) -> Sun:
    sun = Sun(
        x=x,
        y=start_y,
        target_y=target_y,
        value=SUN_VALUE,
        lifetime=SUN_LIFETIME,
        fall_speed=SKY_SUN_FALL_SPEED,
    )
    state.suns.append(sun)
    return sun


def spawn_sunflower_sun(state: GameState, row: int, col: int) -> Sun:
    sun = Sun(
        x=float(col),
        y=float(row),
        target_y=float(row),
        value=SUN_VALUE,
        lifetime=SUN_LIFETIME,
        fall_speed=0,
        row=row,
        col=col,
    )
    state.suns.append(sun)
    return sun


def update_suns(state: GameState, dt: float) -> None:
    active_suns = []
    for sun in state.suns:
        sun.age += dt
        if sun.y < sun.target_y:
            sun.y = min(sun.target_y, sun.y + sun.fall_speed * dt)
        if sun.age < sun.lifetime:
            active_suns.append(sun)
    state.suns = active_suns


def collect_sun_at(state: GameState, x: float, y: float) -> bool:
    for sun in list(state.suns):
        if sun.contains_point(x, y, SUN_CLICK_RADIUS):
            state.sun += sun.value
            state.suns.remove(sun)
            return True
    return False


def update_sunflowers(state: GameState, dt: float) -> None:
    for plant in state.plants.values():
        if plant.plant_type != PlantType.SUNFLOWER:
            continue

        plant.sun_timer += dt
        if plant.sun_timer >= SUNFLOWER_INTERVAL:
            plant.sun_timer -= SUNFLOWER_INTERVAL
            spawn_sunflower_sun(state, plant.row, plant.col)
