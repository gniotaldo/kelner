from pygame.math import Vector2
import pygame
import random
from classes.Seat import Seat
from typing import List
from classes.Meal import Meal
from classes.Table import Table
from misc.images import faces, imgWaiting

class Order:
    def __init__(self, client: 'Client', meals: List[Meal]):
        self.client = client
        self.meals = meals
        self.total_price = 0
        for meal in meals:
            self.total_price += meal.price

class Client:
    def __init__(self, name, surname, map_grid, size: int, seats):
        self.name = name
        self.surname = surname
        self.orders = []
        self.bill = 0
        self.map_grid = map_grid
        self.handled= 0
        self.position = self.get_random_seat_position(seats)
        self._client_image = random.choice(faces)
        self._size = size

    def get_random_seat_position(self, seats: List[Seat]):
        empty_seats = []
        for seat in seats:
            if seat.status == "Free":
                empty_seats.append(seat)

        if empty_seats:
            randSeat: Seat = random.choice(empty_seats)
            randSeat.status = "Taken"
            self.seat: Seat = randSeat
            self.table: Table = randSeat.table
            return randSeat.position
        else:

            return Vector2(0, 0)
    
    def order(self,order: Order):
        self.orders.append(order)
        self.bill += order.total_price

    def render(self, display,ticks):
        display.blit(
            self._client_image,
            (self.position.x * self._size, self.position.y * self._size)
        )
        if self.handled == 0 and ticks in(1,2,3,4,5):
            display.blit(
                imgWaiting,
                (self.position.x * self._size, self.position.y * self._size)
            )

