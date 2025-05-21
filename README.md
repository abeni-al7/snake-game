# Snake Game

## Introduction

This is a classic Snake game implemented in Python using the PyOpenGL library for graphics. The player controls a snake that grows by eating apples, and the game ends if the snake hits the boundaries or itself.

## Features

- Classic snake gameplay.
- Selectable difficulty levels (1-9, plus a challenging level 0).
- Dynamic game speed: The game becomes faster as your score increases.
- Current score display.
- Persistent high score: Your best score is saved and displayed.
- Sound effects for eating apples and game over.
- Visual grid to aid movement.
- Game over screen displaying the final score.
- Option to return to the main menu after a game over.

## Usage

### Prerequisites

Ensure you have Python installed. You will also need the libraries listed in [requirements.txt](c%3A%5CUsers%5C25192%5CDesktop%5Csnake-game%5Crequirements.txt):
- PyOpenGL
- PyOpenGL-accelerate

You can install them using pip:
```bash
pip install -r requirements.txt
```

### Running the Game

To start the game, navigate to the project directory in your terminal and run:
```bash
python snake_game.py
```

### How to Play

1.  **Difficulty Selection:**
    *   When the game starts, you will be prompted to select a difficulty level.
    *   Press keys `1` through `9` for corresponding difficulty levels (1 being the slowest, 9 being faster).
    *   Press `0` for the hardest difficulty level.

2.  **Controlling the Snake:**
    *   Use the **W, A, S, D** keys or the **Arrow Keys** to change the snake's direction:
        *   `W` or `Up Arrow`: Move Up
        *   `S` or `Down Arrow`: Move Down
        *   `A` or `Left Arrow`: Move Left
        *   `D` or `Right Arrow`: Move Right
    *   The snake cannot immediately reverse its direction (e.g., if moving right, you cannot immediately move left).

3.  **Objective:**
    *   Guide the snake to eat the red apples that appear on the screen.
    *   Each apple eaten increases your score and the snake's length.
    *   Avoid colliding with the game window's borders or the snake's own body.

4.  **Game Over:**
    *   If the snake collides with a wall or itself, the game ends.
    *   Your final score will be displayed.
    *   If your score is higher than the current high score, it will be updated.
    *   The game will automatically return to the difficulty selection screen after a short delay.

5.  **Exiting the Game:**
    *   Press the `ESC` key at any time to close the game.
