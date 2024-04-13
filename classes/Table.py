import pygame
from pygame.math import Vector2
from misc.images import imgTable

class Table:
    def __init__(self, position: Vector2, size: int, map_width: int, map_height: int):
        self.position = position
        self._table_image = imgTable
        self._size = size
        self.seats_cells = []
        self.map_width = map_width
        self.map_height = map_height
        self.status = "Free"
        self.orders = []

        self.add_seat(Vector2(position.x - 1, position.y))
        self.add_seat(Vector2(position.x + 1, position.y))
        self.add_seat(Vector2(position.x, position.y - 1))
        self.add_seat(Vector2(position.x, position.y + 1))

    def add_seat(self, position: Vector2):
        if 0 <= position.x < self.map_width and 0 <= position.y < self.map_height:
            self.seats_cells.append(position)

    def render(self, display):
        display.blit(
            self._table_image,
            (self.position.x * self._size, self.position.y * self._size)
        )

    def add_order(self, order):
        self.orders.append(order)

    def is_occupied(self):
        return self.status == "Occupied"

    def is_empty(self):
        return self.status == "Free"