from pygame.math import Vector2
import pygame
from classes.Table import Table
from typing import List
from misc.images import imgFreeSeat, imgTakenSeat

class Seat:

    def __init__(self, position: Vector2, size: int, tables: List[Table]):
        self.position = position
        self.status = "Free"
        for table in tables:
            if self.position in table.seats_cells:
                self.table: Table = table
        self._size = size

    def render(self, display):
        self._seat_image = imgFreeSeat if self.status == "Free" else imgTakenSeat
        display.blit(
            self._seat_image,
            (self.position.x * self._size, self.position.y * self._size)
        )



