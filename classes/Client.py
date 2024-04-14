from pygame.math import Vector2
import pygame
import random
from classes.Seat import Seat
from typing import List
from classes.Meal import *
from classes.Table import Table
from misc.images import faces, imgWaiting, imgGiveMe

class Order:
    def __init__(self, client: 'Client', meal):
        self.client = client
        self.meal: Meal = meal
        self.status = 0 #0- ordered, 1- in waiter memory 2- in preparing 3-ready to take 4- in waiter hands 5-completed
        self.timePrepared = 0

class Client:
    def __init__(self, name, surname, map_grid, size: int, seats):
        self.name = name
        self.surname = surname
        self.order = None
        self.bill = 0
        self.map_grid = map_grid
        self.handled= 0
        self.position = self.get_random_seat_position(seats)
        self._client_image = random.choice(faces)
        self._size = size
        self.placeOrder(random.choice(menu))

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
    
    def placeOrder(self,meal: Meal):
        self.order = Order(self,meal)
        self.bill += meal.price

    def render(self, display,ticks):
        display.blit(
            self._client_image,
            (self.position.x * self._size, self.position.y * self._size)
        )
        if self.handled == 0 and ticks % 10 in (1,2,3,4,5):
            display.blit(
                imgWaiting,
                (self.position.x * self._size, self.position.y * self._size)
            )
        if self.order.status == 4 and ticks % 10 in (3,4,5,6,7,8):
            display.blit(
                imgGiveMe,
                (self.position.x * self._size, self.position.y * self._size)
            )

