# PVZ Demo

A small Python learning project inspired by Plants vs. Zombies.

Current stage:

- 5x9 lawn data structure
- Sun resource
- Sunflower and peashooter planting rules
- Sky and sunflower sun collection
- Zombie, pea, combat, and game-over rules
- Pygame placeholder UI
- Pytest tests for core rules and basic UI input

## Install

```powershell
python -m pip install -r requirements.txt
```

If your network uses Clash on port `7897`, use:

```powershell
python -m pip install --proxy http://127.0.0.1:7897 -r requirements.txt
```

## Run Game

```powershell
python main.py
```

## Run Tests

```powershell
python -m pytest tests
```
