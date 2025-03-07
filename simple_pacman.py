#!/usr/bin/env python3
import os
import random
import time
import sys
import termios
import tty
import select

class SimplePacman:
    def __init__(self):
        self.width = 20
        self.height = 10
        self.score = 0
        self.lives = 3
        self.level = 1
        self.game_over = False
        self.win = False
        self.init_game()
    
    def init_game(self):
        # Create empty board
        self.board = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        
        # Create walls
        for y in range(self.height):
            for x in range(self.width):
                if (y == 0 or y == self.height - 1 or 
                    x == 0 or x == self.width - 1 or
                    (y % 3 == 0 and x % 5 == 0 and 
                     y > 1 and y < self.height - 2 and
                     x > 1 and x < self.width - 2)):
                    self.board[y][x] = '#'
        
        # Create dots
        self.dots_count = 0
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.board[y][x] == ' ':
                    self.board[y][x] = '.'
                    self.dots_count += 1
        
        # Create pacman
        self.pacman_y = self.height // 2
        self.pacman_x = self.width // 2
        self.pacman_char = '>'
        if self.board[self.pacman_y][self.pacman_x] == '.':
            self.board[self.pacman_y][self.pacman_x] = ' '
            self.dots_count -= 1
        
        # Create ghosts
        self.ghosts = []
        ghost_positions = [
            (1, 1),
            (1, self.width - 2),
            (self.height - 2, 1),
            (self.height - 2, self.width - 2)
        ]
        for y, x in ghost_positions:
            self.ghosts.append([y, x])
            if self.board[y][x] == '.':
                self.board[y][x] = ' '
                self.dots_count -= 1
    
    def draw_board(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Draw header
        print(f"Score: {self.score}  Lives: {self.lives}  Level: {self.level}")
        print("-" * (self.width + 2))
        
        # Draw board
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                # Draw pacman
                if y == self.pacman_y and x == self.pacman_x:
                    line += self.pacman_char
                # Draw ghosts
                elif any(y == ghost[0] and x == ghost[1] for ghost in self.ghosts):
                    line += 'M'
                # Draw board elements
                else:
                    line += self.board[y][x]
            print(line)
        
        print("-" * (self.width + 2))
        
        # Game status messages
        if self.game_over:
            print("GAME OVER! Press 'r' to restart or 'q' to quit")
        elif self.win:
            print(f"YOU WIN LEVEL {self.level}! Press 'n' for next level")
        else:
            print("Controls: WASD or arrow keys (q to quit)")
    
    def move_pacman(self, direction):
        new_y, new_x = self.pacman_y, self.pacman_x
        
        # Set pacman character based on direction
        if direction == 'up':
            new_y -= 1
            self.pacman_char = '^'
        elif direction == 'right':
            new_x += 1
            self.pacman_char = '>'
        elif direction == 'down':
            new_y += 1
            self.pacman_char = 'v'
        elif direction == 'left':
            new_x -= 1
            self.pacman_char = '<'
        
        # Check if new position is valid
        if self.board[new_y][new_x] != '#':
            self.pacman_y, self.pacman_x = new_y, new_x
            
            # Check if pacman ate a dot
            if self.board[new_y][new_x] == '.':
                self.board[new_y][new_x] = ' '
                self.score += 10
                self.dots_count -= 1
                
                # Check if all dots are eaten
                if self.dots_count <= 0:
                    self.win = True
    
    def move_ghosts(self):
        directions = ['up', 'right', 'down', 'left']
        
        for ghost in self.ghosts:
            # Choose a random direction
            direction = random.choice(directions)
            new_y, new_x = ghost[0], ghost[1]
            
            if direction == 'up':
                new_y -= 1
            elif direction == 'right':
                new_x += 1
            elif direction == 'down':
                new_y += 1
            elif direction == 'left':
                new_x -= 1
            
            # Check if new position is valid
            if self.board[new_y][new_x] != '#' and not any(new_y == g[0] and new_x == g[1] for g in self.ghosts):
                ghost[0], ghost[1] = new_y, new_x
            
            # Check if ghost caught pacman
            if ghost[0] == self.pacman_y and ghost[1] == self.pacman_x:
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
                else:
                    # Reset positions
                    self.pacman_y = self.height // 2
                    self.pacman_x = self.width // 2
                    break
    
    def next_level(self):
        self.level += 1
        self.win = False
        self.init_game()
    
    def get_key(self):
        """Get a single keypress without blocking."""
        if select.select([sys.stdin], [], [], 0.1)[0]:
            return sys.stdin.read(1)
        return None

    def run(self):
        # Set up terminal for non-blocking input
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setcbreak(sys.stdin.fileno())
            
            while True:
                self.draw_board()
                
                # Handle input
                key = self.get_key()
                
                if key == 'q':
                    break
                elif key == 'r' and self.game_over:
                    self.score = 0
                    self.lives = 3
                    self.level = 1
                    self.game_over = False
                    self.init_game()
                elif key == 'n' and self.win:
                    self.next_level()
                elif key == 'w' or key == 'A':  # Up
                    self.move_pacman('up')
                elif key == 'd' or key == 'C':  # Right
                    self.move_pacman('right')
                elif key == 's' or key == 'B':  # Down
                    self.move_pacman('down')
                elif key == 'a' or key == 'D':  # Left
                    self.move_pacman('left')
                
                if not self.game_over and not self.win:
                    self.move_ghosts()
                
                time.sleep(0.2)  # Game speed
        
        finally:
            # Restore terminal settings
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

if __name__ == "__main__":
    game = SimplePacman()
    try:
        game.run()
    except KeyboardInterrupt:
        pass
    finally:
        # Make sure to restore terminal
        os.system('clear' if os.name == 'posix' else 'cls')
        print("Thanks for playing!")