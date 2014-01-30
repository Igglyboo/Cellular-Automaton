import pygame
import sys
from random import randint
from pygame.locals import *

width = 600
height = 1000
cell_size = 10
cell_width = width / cell_size
cell_height = height / cell_size
grid_color = (255, 255, 255)
dead_color = (0, 0, 0)
alive_color = (255, 0, 0)
selected_cell = (47, 47)
born = set([3])
survives = set([2, 3])

display_surface = pygame.display.set_mode((width, height))
display_surface.fill(dead_color)


def main():
    pygame.init()
    pygame.display.set_caption('Conway\'s Game of Life')

    grid = {}
    for x in range(cell_width):
        for y in range(cell_height):
            grid[x, y] = 0

    for cell in grid:
        grid[cell] = 0

    color_grid(grid)
    game_of_life(grid)

    start = False

    while True:

        if start:
            grid = game_of_life(grid)

        pygame.display.update()


        for event in pygame.event.get():
            if event.type == QUIT:
                if not start:
                    start = True
                    break
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                grid[event.pos[0]/cell_size, event.pos[1]/cell_size] = not grid[event.pos[0]/cell_size, event.pos[1]/cell_size]


        color_grid(grid)


def color_grid(grid):

    for cell in grid:
        if grid[cell] == 0:
            pygame.draw.rect(display_surface, dead_color, (cell[0] * cell_size, cell[1] * cell_size, cell_size, cell_size))
        else:
            pygame.draw.rect(display_surface, alive_color, (cell[0] * cell_size, cell[1] * cell_size, cell_size, cell_size))

    for i in range(0, width, cell_size):
        pygame.draw.line(display_surface, grid_color, (0, i), (width, i))
        pygame.draw.line(display_surface, grid_color, (i, 0), (i, height))


def game_of_life(grid):

    new_grid = {}

    for cell in grid:
        neighbors = get_neighbors(cell, grid)
        if grid[cell] == 1:
            if neighbors in survives:
                new_grid[cell] = 1
            else:
                new_grid[cell] = 0
        else:
            if neighbors in born:
                new_grid[cell] = 1
            else:
                new_grid[cell] = 0

    return new_grid


def get_neighbors(cell, grid):

    neighbors = 0

    for x in range(-1, 2):
        for y in range(-1, 2):
            x1, y1 = cell[0] + x, cell[1] + y
            if x1 == -1:
                x1 = cell_width -1
            elif x1 == cell_width:
                x1 = 0
            if y1 == -1:
                y1 = cell_height -1
            elif y1 == cell_height:
                y1 = 0
            cell_to_check = (x1, y1)
            if cell_to_check != cell:
                neighbors += grid[cell_to_check]

    return neighbors


if __name__ == "__main__":
    main()
else:
    sys.exit()