import pygame
import random
import numpy as np
from typing import List, Tuple

# Initialize Pygame
pygame.init()

# Constants
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
PREVIEW_SIZE = 4

# Calculate window dimensions
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 6)  # Extra space for next piece preview
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GHOST_GRAY = (50, 50, 50)  # Color for ghost piece
CYAN = (0, 255, 255)    # I piece
BLUE = (0, 0, 255)      # J piece
ORANGE = (255, 165, 0)  # L piece
YELLOW = (255, 255, 0)  # O piece
GREEN = (0, 255, 0)     # S piece
PURPLE = (128, 0, 128)  # T piece
RED = (255, 0, 0)       # Z piece

# Tetromino shapes
SHAPES = {
    'I': [[1, 1, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'Z': [[1, 1, 0], [0, 1, 1]]
}

COLORS = {
    'I': CYAN,
    'J': BLUE,
    'L': ORANGE,
    'O': YELLOW,
    'S': GREEN,
    'T': PURPLE,
    'Z': RED
}

class Tetromino:
    def __init__(self, shape_name: str):
        self.shape = SHAPES[shape_name]
        self.color = COLORS[shape_name]
        self.rotation = 0
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self) -> None:
        self.shape = list(zip(*self.shape[::-1]))

    def get_positions(self) -> List[Tuple[int, int]]:
        positions = []
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j]:
                    positions.append((self.x + j, self.y + i))
        return positions

class TetrisGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.game_over = False
        self.score = 0
        self.level = 1
        self.fall_speed = 1000  # Start with 1 second per fall
        self.last_fall_time = pygame.time.get_ticks()

    def new_piece(self) -> Tetromino:
        return Tetromino(random.choice(list(SHAPES.keys())))

    def valid_move(self, piece: Tetromino, x: int, y: int) -> bool:
        for i in range(len(piece.shape)):
            for j in range(len(piece.shape[i])):
                if piece.shape[i][j]:
                    new_x = x + j
                    new_y = y + i
                    if (new_x < 0 or new_x >= GRID_WIDTH or 
                        new_y >= GRID_HEIGHT or 
                        (new_y >= 0 and self.grid[new_y][new_x])):
                        return False
        return True

    def lock_piece(self) -> None:
        for x, y in self.current_piece.get_positions():
            if y >= 0:
                self.grid[y][x] = 1
        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        if not self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y):
            self.game_over = True

    def clear_lines(self) -> None:
        lines_cleared = 0
        for i in range(GRID_HEIGHT):
            if all(self.grid[i]):
                self.grid = np.delete(self.grid, i, 0)
                self.grid = np.vstack([np.zeros(GRID_WIDTH), self.grid])
                lines_cleared += 1
        
        if lines_cleared:
            self.score += (lines_cleared ** 2) * 100
            self.level = self.score // 1000 + 1
            self.fall_speed = max(100, 1000 - (self.level - 1) * 100)

    def get_ghost_position(self) -> List[Tuple[int, int]]:
        # Create a copy of current piece
        ghost_y = self.current_piece.y
        
        # Move the ghost piece down until it hits something
        while self.valid_move(self.current_piece, self.current_piece.x, ghost_y + 1):
            ghost_y += 1
            
        # Get the positions of the ghost piece
        ghost_positions = []
        for i in range(len(self.current_piece.shape)):
            for j in range(len(self.current_piece.shape[i])):
                if self.current_piece.shape[i][j]:
                    ghost_positions.append((self.current_piece.x + j, ghost_y + i))
        return ghost_positions

    def draw(self) -> None:
        self.screen.fill(BLACK)
        
        # Draw grid
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                pygame.draw.rect(self.screen, GRAY,
                               [x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE], 1)
                if self.grid[y][x]:
                    pygame.draw.rect(self.screen, WHITE,
                                   [x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE])

        # Draw ghost piece
        for x, y in self.get_ghost_position():
            if y >= 0:
                pygame.draw.rect(self.screen, GHOST_GRAY,
                               [x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE])
                pygame.draw.rect(self.screen, self.current_piece.color,
                               [x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE], 1)

        # Draw current piece
        for x, y in self.current_piece.get_positions():
            if y >= 0:
                pygame.draw.rect(self.screen, self.current_piece.color,
                               [x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE])

        # Draw next piece preview
        preview_x = GRID_WIDTH * BLOCK_SIZE + BLOCK_SIZE
        preview_y = BLOCK_SIZE
        pygame.draw.rect(self.screen, GRAY,
                        [preview_x, preview_y, PREVIEW_SIZE * BLOCK_SIZE, PREVIEW_SIZE * BLOCK_SIZE], 1)
        
        for i in range(len(self.next_piece.shape)):
            for j in range(len(self.next_piece.shape[i])):
                if self.next_piece.shape[i][j]:
                    pygame.draw.rect(self.screen, self.next_piece.color,
                                   [preview_x + j * BLOCK_SIZE,
                                    preview_y + i * BLOCK_SIZE,
                                    BLOCK_SIZE, BLOCK_SIZE])

        # Draw score and level
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        level_text = font.render(f'Level: {self.level}', True, WHITE)
        self.screen.blit(score_text, (preview_x, preview_y + 150))
        self.screen.blit(level_text, (preview_x, preview_y + 200))

        pygame.display.flip()

    def run(self) -> None:
        while not self.game_over:
            current_time = pygame.time.get_ticks()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.valid_move(self.current_piece, self.current_piece.x - 1, self.current_piece.y):
                            self.current_piece.x -= 1
                    elif event.key == pygame.K_RIGHT:
                        if self.valid_move(self.current_piece, self.current_piece.x + 1, self.current_piece.y):
                            self.current_piece.x += 1
                    elif event.key == pygame.K_UP:
                        rotated_shape = list(zip(*self.current_piece.shape[::-1]))
                        original_shape = self.current_piece.shape
                        self.current_piece.shape = rotated_shape
                        if not self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y):
                            self.current_piece.shape = original_shape
                    elif event.key == pygame.K_DOWN:
                        if self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y + 1):
                            self.current_piece.y += 1
                    elif event.key == pygame.K_SPACE:
                        while self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y + 1):
                            self.current_piece.y += 1
                        self.lock_piece()

            # Handle automatic falling
            if current_time - self.last_fall_time > self.fall_speed:
                if self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y + 1):
                    self.current_piece.y += 1
                else:
                    self.lock_piece()
                self.last_fall_time = current_time

            self.draw()
            self.clock.tick(60)

        # Game over screen
        font = pygame.font.Font(None, 48)
        game_over_text = font.render('Game Over!', True, WHITE)
        self.screen.blit(game_over_text, 
                        (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                         SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)

if __name__ == '__main__':
    game = TetrisGame()
    game.run()
    pygame.quit() 