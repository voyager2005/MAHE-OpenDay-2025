import pygame
import random
import sys

# Constants
ROWS, COLS = 8, 8
WIDTH = 600
CELL_SIZE = WIDTH // COLS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (50, 50, 255)
GREY = (180, 180, 180)

pygame.init()
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Maze Game - You Solve 8x8!")

# Maze Cell
class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.walls = [True, True, True, True]  # top, right, bottom, left
        self.visited = False

    def draw(self, win):
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE

        if self.visited:
            pygame.draw.rect(win, WHITE, (x, y, CELL_SIZE, CELL_SIZE))

        if self.walls[0]:
            pygame.draw.line(win, BLACK, (x, y), (x + CELL_SIZE, y), 2)
        if self.walls[1]:
            pygame.draw.line(win, BLACK, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)
        if self.walls[2]:
            pygame.draw.line(win, BLACK, (x + CELL_SIZE, y + CELL_SIZE), (x, y + CELL_SIZE), 2)
        if self.walls[3]:
            pygame.draw.line(win, BLACK, (x, y + CELL_SIZE), (x, y), 2)

    def highlight(self, color):
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE
        pygame.draw.rect(WIN, color, (x + 3, y + 3, CELL_SIZE - 6, CELL_SIZE - 6))

def index(row, col):
    if row < 0 or col < 0 or row >= ROWS or col >= COLS:
        return None
    return row * COLS + col

def generate_maze(grid):
    stack = []
    current = grid[0]
    current.visited = True

    while True:
        neighbors = []

        def get_unvisited(r, c):
            i = index(r, c)
            if i is not None and not grid[i].visited:
                return grid[i]
            return None

        top = get_unvisited(current.row - 1, current.col)
        right = get_unvisited(current.row, current.col + 1)
        bottom = get_unvisited(current.row + 1, current.col)
        left = get_unvisited(current.row, current.col - 1)

        if top: neighbors.append(("top", top))
        if right: neighbors.append(("right", right))
        if bottom: neighbors.append(("bottom", bottom))
        if left: neighbors.append(("left", left))

        if neighbors:
            direction, next_cell = random.choice(neighbors)
            stack.append(current)

            # Knock down walls
            if direction == "top":
                current.walls[0] = False
                next_cell.walls[2] = False
            elif direction == "right":
                current.walls[1] = False
                next_cell.walls[3] = False
            elif direction == "bottom":
                current.walls[2] = False
                next_cell.walls[0] = False
            elif direction == "left":
                current.walls[3] = False
                next_cell.walls[1] = False

            current = next_cell
            current.visited = True
        elif stack:
            current = stack.pop()
        else:
            break

def draw_grid(grid, player, start_cell, end_cell):
    WIN.fill(GREY)
    for cell in grid:
        cell.draw(WIN)
    start_cell.highlight(GREEN)
    end_cell.highlight(RED)
    player.highlight(BLUE)
    pygame.display.update()

def main():
    grid = [Cell(r, c) for r in range(ROWS) for c in range(COLS)]
    generate_maze(grid)

    player = grid[0]
    start_cell = grid[0]
    end_cell = grid[-1]

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(30)
        draw_grid(grid, player, start_cell, end_cell)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                r, c = player.row, player.col
                current = grid[index(r, c)]

                if event.key == pygame.K_UP and not current.walls[0]:
                    player = grid[index(r - 1, c)]
                if event.key == pygame.K_RIGHT and not current.walls[1]:
                    player = grid[index(r, c + 1)]
                if event.key == pygame.K_DOWN and not current.walls[2]:
                    player = grid[index(r + 1, c)]
                if event.key == pygame.K_LEFT and not current.walls[3]:
                    player = grid[index(r, c - 1)]

                if player == end_cell:
                    print("🎉 You solved the maze!")
                    pygame.time.delay(1000)
                    run = False

    pygame.quit()

if __name__ == "__main__":
    main()
