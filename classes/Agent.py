from pygame.math import Vector2
import pygame
from classes.Client import Client, Order
from typing import List
from classes.Map import Map
from classes.Client import Client
from misc.config import HEIGHT,WIDTH,BAR
from misc.images import waiterImgs as dirImgs
from misc.dictionary import directions, handledSound, inKitchenSound



class Agent:


    def __init__(self, position: Vector2, size: int, restaurant_map: Map):
        self.position = position
        self.facing = Vector2(self.position.x,self.position.y+1)
        self._waiter_image = dirImgs[0]
        self._size = size
        self.map = restaurant_map
        self.status = 0 #0-idle, 1-going to client 2-idle but memory is full 3-going to kichen
        self.memorySize = 5
        self.inMemory = 0
        self.inHands = 0
        self.handsMax = 3
        self.ordersInMemory: List[Order] = []
        self.ordersInHands: List[Order] = []
        self.ordersInKitchen: List[Order] = []

    def render(self, display):
        display.blit(
            self._waiter_image,
            (self.position.x * self._size, self.position.y * self._size)
        )
    
    def move(self,moveType, map: Map):
        
        if moveType=='W':
            self._waiter_image = dirImgs[2]
            if (self.position.y>0 and map.map_grid[int(self.position.x)][int(self.position.y-1)] == map.Cell.EmptyCell):
                self.position.y -= 1
            self.facing = Vector2(self.position.x,self.position.y-1)
            if self.position.y == 0:
                self.facing = Vector2(self.position.x,self.position.y)
        elif moveType=='S':
            self._waiter_image = dirImgs[0]
            if (self.position.y<HEIGHT-1 and map.map_grid[int(self.position.x)][int(self.position.y+1)] == map.Cell.EmptyCell):
                self.position.y += 1
            self.facing = Vector2(self.position.x,self.position.y+1)
            if self.position.y == HEIGHT-1:
                self.facing = Vector2(self.position.x,self.position.y)
        elif moveType=='A':
            self._waiter_image = dirImgs[1]
            if (self.position.x>BAR and map.map_grid[int(self.position.x-1)][int(self.position.y)] == map.Cell.EmptyCell):
                self.position.x -= 1
            self.facing = Vector2(self.position.x-1,self.position.y)
            if self.position.x == 0:
                self.facing = Vector2(self.position.x,self.position.y)
        elif moveType=='D':
            self._waiter_image = dirImgs[3]
            if (self.position.x<WIDTH-1 and map.map_grid[int(self.position.x+1)][int(self.position.y)] == map.Cell.EmptyCell):
                self.position.x += 1
            self.facing = Vector2(self.position.x+1,self.position.y)
            if self.position.x == WIDTH-1:
                self.facing = Vector2(self.position.x,self.position.y)
    
    def handle(self, client: Client):
        client.handled = 1
        handledSound.play()
        self.inMemory += 1
        self.ordersInMemory.append(client.order)
        client.order.status = 1

    def inKitchen(self):
        self.inMemory = 0
        for order in self.ordersInMemory:
            self.ordersInKitchen.append(order)
            order.status = 2
        self.ordersInMemory.clear()
        inKitchenSound.play()
    def completeOrder(self, order: Order):
        order.status = 5
        self.ordersInHands.remove(order)
        inKitchenSound.play()
        self.inHands -= 1
