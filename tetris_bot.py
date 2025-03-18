import pygame
import numpy as np
from tetris import TetrisGame, Tetromino, GRID_WIDTH, GRID_HEIGHT, SHAPES, COLORS
import time

class TetrisBot:
    def __init__(self, game):
        self.game = game
        self.weights = {
            'holes': -4.0,      # Penalty for holes
            'bumpiness': -2.0,  # Penalty for uneven surface
            'height': -3.0,     # Penalty for high stacks
            'lines': 3.0        # Reward for complete lines
        }

    def get_holes(self, grid):
        """Count the number of holes in the grid."""
        holes = 0
        for col in range(GRID_WIDTH):
            block_found = False
            for row in range(GRID_HEIGHT):
                if grid[row][col]:
                    block_found = True
                elif block_found:
                    holes += 1
        return holes

    def get_bumpiness(self, grid):
        """Calculate the bumpiness of the surface."""
        heights = []
        for col in range(GRID_WIDTH):
            for row in range(GRID_HEIGHT):
                if grid[row][col]:
                    heights.append(GRID_HEIGHT - row)
                    break
            else:
                heights.append(0)
        
        bumpiness = 0
        for i in range(len(heights) - 1):
            bumpiness += abs(heights[i] - heights[i + 1])
        return bumpiness

    def get_height(self, grid):
        """Calculate the total height of all columns."""
        total_height = 0
        for col in range(GRID_WIDTH):
            for row in range(GRID_HEIGHT):
                if grid[row][col]:
                    total_height += GRID_HEIGHT - row
                    break
        return total_height

    def get_complete_lines(self, grid):
        """Count the number of complete lines."""
        complete_lines = 0
        for row in range(GRID_HEIGHT):
            if all(grid[row]):
                complete_lines += 1
        return complete_lines

    def evaluate_position(self, grid):
        """Evaluate the current position using multiple metrics."""
        holes = self.get_holes(grid)
        bumpiness = self.get_bumpiness(grid)
        height = self.get_height(grid)
        complete_lines = self.get_complete_lines(grid)

        score = (
            self.weights['holes'] * holes +
            self.weights['bumpiness'] * bumpiness +
            self.weights['height'] * height +
            self.weights['lines'] * complete_lines
        )
        return score

    def simulate_move(self, piece, x, y, grid):
        """Simulate a move and return the resulting grid."""
        # Create a copy of the grid
        new_grid = grid.copy()
        
        # Add the piece to the grid
        for i in range(len(piece.shape)):
            for j in range(len(piece.shape[i])):
                if piece.shape[i][j]:
                    new_y = y + i
                    new_x = x + j
                    if 0 <= new_y < GRID_HEIGHT and 0 <= new_x < GRID_WIDTH:
                        new_grid[new_y][new_x] = 1
        
        return new_grid

    def find_best_move(self):
        """Find the best move for the current piece."""
        best_score = float('-inf')
        best_move = None
        current_piece = self.game.current_piece

        # Try all possible positions and rotations
        for rotation in range(4):
            # Try all possible x positions
            for x in range(-2, GRID_WIDTH + 2):
                # Create a copy of the piece for simulation
                piece_copy = Tetromino(list(SHAPES.keys())[list(SHAPES.values()).index(current_piece.shape)])
                piece_copy.x = x
                piece_copy.y = 0

                # Apply rotation
                for _ in range(rotation):
                    piece_copy.rotate()

                # Check if the move is valid
                if not self.game.valid_move(piece_copy, x, 0):
                    continue

                # Find the lowest possible y position
                y = 0
                while self.game.valid_move(piece_copy, x, y + 1):
                    y += 1

                # Simulate the move
                new_grid = self.simulate_move(piece_copy, x, y, self.game.grid)
                
                # Evaluate the position
                score = self.evaluate_position(new_grid)
                
                if score > best_score:
                    best_score = score
                    best_move = (x, y, rotation)

        return best_move

    def execute_move(self):
        """Execute the best move found."""
        if not self.game.current_piece:
            return

        best_move = self.find_best_move()
        if best_move is None:
            return

        target_x, target_y, target_rotation = best_move
        current_piece = self.game.current_piece

        # Apply rotation
        current_rotation = 0
        while current_rotation < target_rotation:
            rotated_shape = list(zip(*current_piece.shape[::-1]))
            if self.game.valid_move(current_piece, current_piece.x, current_piece.y):
                current_piece.shape = rotated_shape
            current_rotation += 1

        # Move horizontally
        while current_piece.x < target_x:
            if self.game.valid_move(current_piece, current_piece.x + 1, current_piece.y):
                current_piece.x += 1
        while current_piece.x > target_x:
            if self.game.valid_move(current_piece, current_piece.x - 1, current_piece.y):
                current_piece.x -= 1

        # Move down
        while self.game.valid_move(current_piece, current_piece.x, current_piece.y + 1):
            current_piece.y += 1

        # Lock the piece
        self.game.lock_piece()

def main():
    game = TetrisGame()
    bot = TetrisBot(game)
    
    # Modify the game loop to use the bot
    while not game.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.game_over = True
        
        # Let the bot make a move
        bot.execute_move()
        
        # Draw the game state
        game.draw()
        pygame.display.flip()
        
        # Control game speed
        game.clock.tick(60)
        
        # Add a small delay to make the bot's moves visible
        time.sleep(0.1)

    # Game over screen
    font = pygame.font.Font(None, 48)
    game_over_text = font.render('Game Over!', True, (255, 255, 255))
    game.screen.blit(game_over_text, 
                    (game.screen.get_width() // 2 - game_over_text.get_width() // 2,
                     game.screen.get_height() // 2 - game_over_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()

if __name__ == '__main__':
    main() 