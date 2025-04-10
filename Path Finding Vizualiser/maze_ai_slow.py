import pygame
import random
import heapq
import sys
import time

# Maze Settings
ROWS, COLS = 8, 8
WIDTH = 600
CELL_SIZE = WIDTH // COLS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (50, 50, 255)
GREY = (200, 200, 200)
YELLOW = (255, 255, 0)

pygame.init()
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Maze Solver - Slowed Down 8x8 A*")

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.walls = [True, True, True, True]
        self.visited = False
        self.color = WHITE

    def draw(self, win):
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE
        pygame.draw.rect(win, self.color, (x, y, CELL_SIZE, CELL_SIZE))
        if self.walls[0]:
            pygame.draw.line(win, BLACK, (x, y), (x + CELL_SIZE, y), 2)
        if self.walls[1]:
            pygame.draw.line(win, BLACK, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)
        if self.walls[2]:
            pygame.draw.line(win, BLACK, (x + CELL_SIZE, y + CELL_SIZE), (x, y + CELL_SIZE), 2)
        if self.walls[3]:
            pygame.draw.line(win, BLACK, (x, y + CELL_SIZE), (x, y), 2)

    def get_pos(self):
        return (self.row, self.col)

    def __lt__(self, other):
        return False

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

def get_neighbors(cell, grid):
    neighbors = []
    row, col = cell.row, cell.col

    def is_valid(r, c, wall_dir):
        i = index(r, c)
        if i is not None:
            if wall_dir == 0 and not cell.walls[0]:
                neighbors.append(grid[i])
            elif wall_dir == 1 and not cell.walls[1]:
                neighbors.append(grid[i])
            elif wall_dir == 2 and not cell.walls[2]:
                neighbors.append(grid[i])
            elif wall_dir == 3 and not cell.walls[3]:
                neighbors.append(grid[i])

    is_valid(row - 1, col, 0)
    is_valid(row, col + 1, 1)
    is_valid(row + 1, col, 2)
    is_valid(row, col - 1, 3)

    return neighbors

def h(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.color = BLUE
        draw()
        pygame.time.wait(100)

def a_star(draw, grid, start, end):
    count = 0
    open_set = []
    heapq.heappush(open_set, (0, count, start))
    came_from = {}

    g_score = {cell: float("inf") for cell in grid}
    g_score[start] = 0

    f_score = {cell: float("inf") for cell in grid}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current = heapq.heappop(open_set)[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.color = RED
            start.color = GREEN
            return True

        for neighbor in get_neighbors(current, grid):
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())

                if neighbor not in open_set_hash:
                    count += 1
                    heapq.heappush(open_set, (f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.color = YELLOW

        draw()
        pygame.time.wait(100)  # slow down step

    return False

def draw_grid(grid):
    WIN.fill(GREY)
    for cell in grid:
        cell.draw(WIN)
    pygame.display.update()

def main():
    grid = [Cell(r, c) for r in range(ROWS) for c in range(COLS)]
    generate_maze(grid)

    start = grid[0]
    end = grid[-1]
    start.color = GREEN
    end.color = RED

    def draw():
        draw_grid(grid)

    a_star(draw, grid, start, end)
    pygame.time.wait(1000)

    run = True
    while run:
        draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

if __name__ == "__main__":
    main()
