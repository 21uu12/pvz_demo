from pvz_demo.game_state import GameState
from pvz_demo.settings import (
    PEA_DAMAGE,
    PEASHOOTER_COOLDOWN,
    PlantType,
    ZOMBIE_DAMAGE_PER_SECOND,
    ZOMBIE_HEALTH,
)
from pvz_demo.systems import (
    find_plant_for_zombie_to_eat,
    has_zombie_ahead,
    plant_at,
    resolve_pea_hits,
    spawn_pea,
    spawn_zombie,
    update_peas,
    update_peashooters,
    update_zombies,
)


def test_peashooter_detects_zombie_in_same_row_ahead():
    state = GameState()
    spawn_zombie(state, row=2, x=8)

    assert has_zombie_ahead(state, row=2, x=3) is True


def test_peashooter_ignores_zombie_in_other_row():
    state = GameState()
    spawn_zombie(state, row=1, x=8)

    assert has_zombie_ahead(state, row=2, x=3) is False


def test_peashooter_ignores_zombie_behind_it():
    state = GameState()
    spawn_zombie(state, row=2, x=1)

    assert has_zombie_ahead(state, row=2, x=3) is False


def test_peashooter_fires_after_cooldown_when_zombie_is_ahead():
    state = GameState()
    plant_at(state, PlantType.PEASHOOTER, row=2, col=3)
    spawn_zombie(state, row=2, x=8)

    update_peashooters(state, dt=PEASHOOTER_COOLDOWN)

    assert len(state.peas) == 1
    assert state.peas[0].row == 2
    assert state.peas[0].x == 3


def test_peashooter_does_not_fire_without_target():
    state = GameState()
    plant_at(state, PlantType.PEASHOOTER, row=2, col=3)

    update_peashooters(state, dt=PEASHOOTER_COOLDOWN)

    assert state.peas == []


def test_pea_moves_right():
    state = GameState()
    pea = spawn_pea(state, row=2, x=3)

    update_peas(state, dt=1.0)

    assert pea.x > 3


def test_zombie_moves_left():
    state = GameState()
    zombie = spawn_zombie(state, row=2, x=8)

    update_zombies(state, dt=1.0)

    assert zombie.x < 8


def test_zombie_stops_and_damages_plant_when_it_reaches_plant():
    state = GameState()
    plant_at(state, PlantType.SUNFLOWER, row=2, col=3)
    zombie = spawn_zombie(state, row=2, x=3.2)
    original_x = zombie.x

    update_zombies(state, dt=1.0)

    assert zombie.x == original_x
    assert state.get_plant(2, 3).health == 100 - ZOMBIE_DAMAGE_PER_SECOND


def test_zombie_removes_destroyed_plant():
    state = GameState()
    plant_at(state, PlantType.SUNFLOWER, row=2, col=3)
    state.get_plant(2, 3).health = ZOMBIE_DAMAGE_PER_SECOND
    spawn_zombie(state, row=2, x=3.2)

    update_zombies(state, dt=1.0)

    assert state.get_plant(2, 3) is None


def test_zombie_continues_after_plant_is_destroyed():
    state = GameState()
    plant_at(state, PlantType.SUNFLOWER, row=2, col=3)
    state.get_plant(2, 3).health = ZOMBIE_DAMAGE_PER_SECOND
    zombie = spawn_zombie(state, row=2, x=3.2)
    update_zombies(state, dt=1.0)
    x_after_eating = zombie.x

    update_zombies(state, dt=1.0)

    assert zombie.x < x_after_eating


def test_zombie_eats_nearest_reached_plant_in_same_row():
    state = GameState()
    plant_at(state, PlantType.SUNFLOWER, row=2, col=2)
    plant_at(state, PlantType.PEASHOOTER, row=2, col=3)
    zombie = spawn_zombie(state, row=2, x=3.2)

    target = find_plant_for_zombie_to_eat(state, zombie)

    assert target == state.get_plant(2, 3)


def test_pea_hit_damages_zombie_and_removes_pea():
    state = GameState()
    spawn_zombie(state, row=2, x=5)
    spawn_pea(state, row=2, x=5)

    resolve_pea_hits(state)

    assert state.peas == []
    assert state.zombies[0].health == ZOMBIE_HEALTH - PEA_DAMAGE


def test_zombie_is_removed_when_health_reaches_zero():
    state = GameState()
    zombie = spawn_zombie(state, row=2, x=5)
    zombie.health = PEA_DAMAGE
    spawn_pea(state, row=2, x=5)

    resolve_pea_hits(state)

    assert state.peas == []
    assert state.zombies == []
