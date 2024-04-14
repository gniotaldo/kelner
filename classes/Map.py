import math
import random
from enum import Enum
import pygame
from pygame.math import Vector2
from misc.images import empty_cell, kitchen_cell
from misc.config import BAR

class Map:
    class Cell(Enum):
        EmptyCell = 'E'
        TableCell = 'T'
        KitchenCell = 'K'
        SeatCell = 'S'

    def image_for_cell(self, cell):
        if cell == Map.Cell.KitchenCell:
            return kitchen_cell
        else:
            return empty_cell

    def __init__(self, width, height, tile_size):
        self.map_grid = None

        self._width = width
        self._height = height
        self._tile_size = tile_size
        self.kitchen_cells = []
        self.table_cells = []
        self.set_map()

    def set_map(self):
        self.map_grid = [[self.Cell.EmptyCell for _ in range(self._height)] for _ in range(self._width)]
        for y in range(3):
            for x in range(BAR,BAR+3):
                self.map_grid[x][y] = self.Cell.KitchenCell

        for x in range(BAR,self._width):
            for y in range(self._height):
                if self.map_grid[x][y] == self.Cell.KitchenCell:
                    self.kitchen_cells.append((x, y))

        attempt = 0
        while attempt < 30:
            random_x = random.randint(BAR, self._width - 1)
            random_y = random.randint(BAR, self._height - 1)
            if self.map_grid[random_x][random_y] != self.Cell.TableCell and not any(
                    math.sqrt((random_x - tx) ** 2 + (random_y - ty) ** 2) <= 4 for tx, ty in self.table_cells
            ) and not any(
                    math.sqrt((random_x - kx) ** 2 + (random_y - ky) ** 2) <= 4 for kx, ky in self.kitchen_cells
            ):
                self.table_cells.append((random_x, random_y))

            else:
                attempt += 1

        for (x, y) in self.table_cells:
            neighbors_offsets = [(0, -1), (0, 1), (-1, 0), (1, 0)]

            for dx, dy in neighbors_offsets:
                neighbor_x, neighbor_y = x + dx, y + dy

                if BAR <= neighbor_x < self._width and 0 <= neighbor_y < self._height and self.map_grid[neighbor_x][neighbor_y] == self.Cell.EmptyCell:
                    self.map_grid[neighbor_x][neighbor_y] = self.Cell.SeatCell

    def get_initial_posistion_for_waiter(self):
        for y in range(self._height):
            for x in range(BAR,self._width):
                if self.map_grid[x][y] == self.Cell.EmptyCell:
                    return Vector2(x, y)
                if self.map_grid[x][y] != self.Cell.KitchenCell:
                    break
        return Vector2(0, 0)

    def render(self, display):
        for y in range(self._height):
            for x in range(5,self._width):
                display.blit(
                    self.image_for_cell(self.map_grid[x][y]),
                    (x * self._tile_size, y * self._tile_size)
                )
