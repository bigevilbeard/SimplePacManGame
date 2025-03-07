# Simple Pacman Game

A classic Pacman arcade game built with Python and Pygame. Navigate through the maze, collect dots, and avoid the ghosts!

![Pacman Game Screenshot](screenshot.png)

## Features

- Classic Pacman gameplay mechanics
- Animated Pacman character with mouth movement
- Four colorful ghosts with AI movement
- Maze with walls and collectible dots
- Score tracking and lives system
- Game over and win conditions

## Requirements

- Python 3.x
- Pygame

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/pacman-game.git
   cd pacman-game
   ```

2. Install the required dependencies:
   ```
   pip install pygame
   ```

3. Run the game:
   ```
   python pacman_game.py
   ```

## How to Play

- Use the **arrow keys** to control Pacman's movement
- Collect all dots in the maze to win
- Avoid the ghosts - if they catch you, you'll lose a life
- You have 3 lives to complete the game
- Press **ESC** to quit the game
- Press **R** to restart after game over or winning

## How It Works

The game is built using Pygame and consists of several key components:

### Game Structure
- The game uses a grid-based maze represented by a 2D array
- Each cell can be a wall (1) or a path with a dot (0)
- The game runs at 60 FPS with a main loop handling updates and rendering

### Pacman
- Controlled by the player using arrow keys
- Moves through the maze collecting dots
- Features animated mouth opening and closing
- Has collision detection with walls and dots

### Ghosts
- Four ghosts with different colors (Red, Pink, Cyan, Orange)
- Move randomly through the maze
- Change direction when hitting walls
- Cause the player to lose a life upon collision

### Scoring System
- Each dot collected adds 10 points to the score
- Game tracks remaining dots to determine win condition

## Code Structure

- `pacman_game.py`: Main game file containing all game logic
- Game initialization and setup
- Pacman and Ghost classes
- Maze rendering and collision detection
- Game loop and event handling

## Customization

You can customize various aspects of the game by modifying the constants at the top of the file:
- `WIDTH`, `HEIGHT`: Screen dimensions
- `GRID_SIZE`: Size of each maze cell
- `PACMAN_SPEED`, `GHOST_SPEED`: Movement speeds
- `maze`: Layout of the game maze

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by the classic Pacman arcade game
- Built with Pygame, a set of Python modules designed for writing video games
