from __future__ import annotations

from dataclasses import dataclass

from pvz_demo.game_state import GameState
from pvz_demo.models import Pea, Plant, Sun, Zombie
from pvz_demo.settings import (
    GAME_OVER_X,
    HIT_DISTANCE,
    PLANT_COSTS,
    PEA_DAMAGE,
    PEA_SPEED,
    PEASHOOTER_COOLDOWN,
    SKY_SUN_FALL_SPEED,
    SUN_CLICK_RADIUS,
    SUN_LIFETIME,
    SUN_VALUE,
    SUNFLOWER_INTERVAL,
    PlantType,
    ZOMBIE_HEALTH,
    ZOMBIE_SPEED,
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


def spawn_zombie(state: GameState, row: int, x: float) -> Zombie:
    zombie = Zombie(row=row, x=x, health=ZOMBIE_HEALTH, speed=ZOMBIE_SPEED)
    state.zombies.append(zombie)
    return zombie


def has_zombie_ahead(state: GameState, row: int, x: float) -> bool:
    return any(zombie.row == row and zombie.x > x for zombie in state.zombies)


def spawn_pea(state: GameState, row: int, x: float) -> Pea:
    pea = Pea(row=row, x=x, damage=PEA_DAMAGE, speed=PEA_SPEED)
    state.peas.append(pea)
    return pea


def update_peashooters(state: GameState, dt: float) -> None:
    for plant in state.plants.values():
        if plant.plant_type != PlantType.PEASHOOTER:
            continue

        if not has_zombie_ahead(state, plant.row, plant.col):
            plant.shoot_timer = 0.0
            continue

        plant.shoot_timer += dt
        if plant.shoot_timer >= PEASHOOTER_COOLDOWN:
            plant.shoot_timer -= PEASHOOTER_COOLDOWN
            spawn_pea(state, plant.row, float(plant.col))


def update_zombies(state: GameState, dt: float) -> None:
    for zombie in state.zombies:
        zombie.x -= zombie.speed * dt


def update_peas(state: GameState, dt: float) -> None:
    for pea in state.peas:
        pea.x += pea.speed * dt


def resolve_pea_hits(state: GameState) -> None:
    active_peas = []
    for pea in state.peas:
        hit_zombie = None
        for zombie in state.zombies:
            if zombie.row == pea.row and abs(zombie.x - pea.x) <= HIT_DISTANCE:
                hit_zombie = zombie
                break

        if hit_zombie is None:
            active_peas.append(pea)
            continue

        hit_zombie.health -= pea.damage

    state.peas = active_peas
    state.zombies = [zombie for zombie in state.zombies if zombie.health > 0]


def update_combat(state: GameState, dt: float) -> None:
    update_peashooters(state, dt)
    update_zombies(state, dt)
    update_peas(state, dt)
    resolve_pea_hits(state)
    update_game_over(state)


def update_game_over(state: GameState) -> None:
    if any(zombie.x <= GAME_OVER_X for zombie in state.zombies):
        state.is_game_over = True
