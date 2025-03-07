import pygame
import random
import sys
import math

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 40
PACMAN_SPEED = 4
GHOST_SPEED = 3
DOT_SIZE = 8

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Pacman")
clock = pygame.time.Clock()

# Game variables
score = 0
lives = 3
game_over = False
game_won = False
font = pygame.font.SysFont(None, 36)

# Define the maze layout (1 = wall, 0 = path with dot)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Calculate the total number of dots
total_dots = sum(row.count(0) for row in maze)
dots_collected = 0

# Create a copy of the maze to track eaten dots
dots = [[1 if cell == 1 else 0 for cell in row] for row in maze]

# Pacman class
class Pacman:
    def __init__(self):
        self.x = GRID_SIZE * 1.5
        self.y = GRID_SIZE * 1.5
        self.direction = "right"
        self.next_direction = "right"
        self.mouth_angle = 45
        self.mouth_opening = True
        
    def update(self):
        # Try to change direction if requested
        if self.can_move(self.next_direction):
            self.direction = self.next_direction
        
        # Move in the current direction if possible
        if self.can_move(self.direction):
            if self.direction == "right":
                self.x += PACMAN_SPEED
            elif self.direction == "left":
                self.x -= PACMAN_SPEED
            elif self.direction == "up":
                self.y -= PACMAN_SPEED
            elif self.direction == "down":
                self.y += PACMAN_SPEED
        
        # Animate mouth
        if self.mouth_opening:
            self.mouth_angle += 3
            if self.mouth_angle >= 45:
                self.mouth_opening = False
        else:
            self.mouth_angle -= 3
            if self.mouth_angle <= 0:
                self.mouth_opening = True
        
        # Check for dot collection
        self.collect_dots()
    
    def can_move(self, direction):
        # Calculate grid position
        grid_x = int(self.x / GRID_SIZE)
        grid_y = int(self.y / GRID_SIZE)
        
        # Check if centered enough to turn
        centered_x = abs((self.x % GRID_SIZE) - GRID_SIZE / 2) < PACMAN_SPEED
        centered_y = abs((self.y % GRID_SIZE) - GRID_SIZE / 2) < PACMAN_SPEED
        
        # Check if the next cell in the desired direction is a wall
        if direction == "right" and (centered_y or direction == self.direction):
            return grid_x + 1 < len(maze[0]) and maze[grid_y][grid_x + 1] != 1
        elif direction == "left" and (centered_y or direction == self.direction):
            return grid_x - 1 >= 0 and maze[grid_y][grid_x - 1] != 1
        elif direction == "up" and (centered_x or direction == self.direction):
            return grid_y - 1 >= 0 and maze[grid_y - 1][grid_x] != 1
        elif direction == "down" and (centered_x or direction == self.direction):
            return grid_y + 1 < len(maze) and maze[grid_y + 1][grid_x] != 1
        return False
    
    def collect_dots(self):
        global score, dots_collected
        grid_x = int(self.x / GRID_SIZE)
        grid_y = int(self.y / GRID_SIZE)
        
        if 0 <= grid_y < len(dots) and 0 <= grid_x < len(dots[0]):
            if dots[grid_y][grid_x] == 0:
                dots[grid_y][grid_x] = 2  # Mark as eaten
                score += 10
                dots_collected += 1
    
    def draw(self):
        # Draw Pacman as a circle with a mouth
        angle_offset = 0
        if self.direction == "right":
            angle_offset = 0
        elif self.direction == "down":
            angle_offset = 90
        elif self.direction == "left":
            angle_offset = 180
        elif self.direction == "up":
            angle_offset = 270
            
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), GRID_SIZE // 2)
        
        # Draw the mouth
        start_angle = angle_offset - self.mouth_angle
        end_angle = angle_offset + self.mouth_angle
        
        # Convert angles to radians and draw the mouth as a polygon
        mouth_points = [(self.x, self.y)]
        for angle in range(int(start_angle), int(end_angle) + 1, 10):
            rad = angle * 3.14159 / 180
            x = self.x + (GRID_SIZE // 2) * math.cos(rad)
            y = self.y + (GRID_SIZE // 2) * math.sin(rad)
            mouth_points.append((x, y))
        
        if len(mouth_points) > 2:
            pygame.draw.polygon(screen, BLACK, mouth_points)
        
        # Draw the eye
        eye_x = self.x - math.sin(math.radians(angle_offset)) * (0.3 * GRID_SIZE // 2)
        eye_y = self.y - math.cos(math.radians(angle_offset)) * (0.3 * GRID_SIZE // 2)
        pygame.draw.circle(screen, BLACK, (int(eye_x), int(eye_y)), 3)

# Ghost class
class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.direction = random.choice(["right", "left", "up", "down"])
        self.speed = GHOST_SPEED
        
    def update(self):
        # Try to continue in the current direction
        if not self.can_move(self.direction):
            # Find possible directions
            possible_directions = []
            for direction in ["right", "left", "up", "down"]:
                if self.can_move(direction):
                    possible_directions.append(direction)
            
            if possible_directions:
                self.direction = random.choice(possible_directions)
        
        # Move in the current direction
        if self.direction == "right":
            self.x += self.speed
        elif self.direction == "left":
            self.x -= self.speed
        elif self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed
    
    def can_move(self, direction):
        # Calculate grid position
        grid_x = int(self.x / GRID_SIZE)
        grid_y = int(self.y / GRID_SIZE)
        
        # Check if centered enough to turn
        centered_x = abs((self.x % GRID_SIZE) - GRID_SIZE / 2) < self.speed
        centered_y = abs((self.y % GRID_SIZE) - GRID_SIZE / 2) < self.speed
        
        # Check if the next cell in the desired direction is a wall
        if direction == "right" and (centered_y or direction == self.direction):
            return grid_x + 1 < len(maze[0]) and maze[grid_y][grid_x + 1] != 1
        elif direction == "left" and (centered_y or direction == self.direction):
            return grid_x - 1 >= 0 and maze[grid_y][grid_x - 1] != 1
        elif direction == "up" and (centered_x or direction == self.direction):
            return grid_y - 1 >= 0 and maze[grid_y - 1][grid_x] != 1
        elif direction == "down" and (centered_x or direction == self.direction):
            return grid_y + 1 < len(maze) and maze[grid_y + 1][grid_x] != 1
        return False
    
    def draw(self):
        # Draw ghost body
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), GRID_SIZE // 2)
        
        # Draw the bottom part of the ghost
        rect = pygame.Rect(
            int(self.x - GRID_SIZE // 2),
            int(self.y),
            GRID_SIZE,
            GRID_SIZE // 2
        )
        pygame.draw.rect(screen, self.color, rect)
        
        # Draw eyes
        eye_offset = GRID_SIZE // 5
        pygame.draw.circle(screen, WHITE, (int(self.x - eye_offset), int(self.y - eye_offset)), 5)
        pygame.draw.circle(screen, WHITE, (int(self.x + eye_offset), int(self.y - eye_offset)), 5)
        
        # Draw pupils
        pupil_offset = 2
        if self.direction == "right":
            pupil_x_offset = pupil_offset
        elif self.direction == "left":
            pupil_x_offset = -pupil_offset
        else:
            pupil_x_offset = 0
            
        pupil_y_offset = pupil_offset if self.direction == "down" else (-pupil_offset if self.direction == "up" else 0)
        
        pygame.draw.circle(screen, BLACK, (int(self.x - eye_offset + pupil_x_offset), 
                                          int(self.y - eye_offset + pupil_y_offset)), 2)
        pygame.draw.circle(screen, BLACK, (int(self.x + eye_offset + pupil_x_offset), 
                                          int(self.y - eye_offset + pupil_y_offset)), 2)

# Create game objects
pacman = Pacman()
ghosts = [
    Ghost(GRID_SIZE * 10, GRID_SIZE * 5, RED),
    Ghost(GRID_SIZE * 8, GRID_SIZE * 5, PINK),
    Ghost(GRID_SIZE * 12, GRID_SIZE * 5, CYAN),
    Ghost(GRID_SIZE * 10, GRID_SIZE * 6, ORANGE)
]

# Draw the maze
def draw_maze():
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            if maze[y][x] == 1:
                pygame.draw.rect(screen, BLUE, rect)
            elif dots[y][x] == 0:  # Draw dots only if not eaten
                dot_rect = pygame.Rect(
                    x * GRID_SIZE + (GRID_SIZE - DOT_SIZE) // 2,
                    y * GRID_SIZE + (GRID_SIZE - DOT_SIZE) // 2,
                    DOT_SIZE, DOT_SIZE
                )
                pygame.draw.ellipse(screen, WHITE, dot_rect)

# Check for collisions between pacman and ghosts
def check_collisions():
    global lives, game_over
    for ghost in ghosts:
        distance = pygame.math.Vector2(pacman.x - ghost.x, pacman.y - ghost.y).length()
        if distance < GRID_SIZE:
            lives -= 1
            if lives <= 0:
                game_over = True
            else:
                # Reset positions
                pacman.x = GRID_SIZE * 1.5
                pacman.y = GRID_SIZE * 1.5
                pacman.direction = "right"
                pacman.next_direction = "right"
                return True
    return False

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                pacman.next_direction = "right"
            elif event.key == pygame.K_LEFT:
                pacman.next_direction = "left"
            elif event.key == pygame.K_UP:
                pacman.next_direction = "up"
            elif event.key == pygame.K_DOWN:
                pacman.next_direction = "down"
            elif event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_r and (game_over or game_won):
                # Reset game
                score = 0
                lives = 3
                game_over = False
                game_won = False
                dots_collected = 0
                dots = [[1 if cell == 1 else 0 for cell in row] for row in maze]
                pacman = Pacman()
                ghosts = [
                    Ghost(GRID_SIZE * 10, GRID_SIZE * 5, RED),
                    Ghost(GRID_SIZE * 8, GRID_SIZE * 5, PINK),
                    Ghost(GRID_SIZE * 12, GRID_SIZE * 5, CYAN),
                    Ghost(GRID_SIZE * 10, GRID_SIZE * 6, ORANGE)
                ]
    
    # Update game state if not game over
    if not game_over and not game_won:
        pacman.update()
        
        # Check if all dots are collected
        if dots_collected >= total_dots:
            game_won = True
        
        # Update ghosts and check for collisions
        if not check_collisions():
            for ghost in ghosts:
                ghost.update()
            check_collisions()
    
    # Draw everything
    screen.fill(BLACK)
    draw_maze()
    pacman.draw()
    for ghost in ghosts:
        ghost.draw()
    
    # Draw score and lives
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, HEIGHT - 40))
    screen.blit(lives_text, (WIDTH - 120, HEIGHT - 40))
    
    # Draw game over or win message
    if game_over:
        game_over_text = font.render("GAME OVER! Press R to restart", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - 180, HEIGHT // 2))
    elif game_won:
        win_text = font.render("YOU WIN! Press R to restart", True, YELLOW)
        screen.blit(win_text, (WIDTH // 2 - 160, HEIGHT // 2))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()