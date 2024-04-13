from pygame.math import Vector2
import pygame
from classes.Map import Map
from classes.BFS import State
from classes.Client import Client
from misc.config import HEIGHT,WIDTH
from misc.images import waiterImgs as dirImgs
from misc.dictionary import directions, handledSound, inKitchenSound



class Agent:


    def __init__(self, position: Vector2, size: int, restaurant_map: Map):
        self.position = position
        self.direction: Vector2 = Vector2(0,1)
        self._waiter_image = dirImgs[0]
        self._size = size
        self.map = restaurant_map
        self.status = 0 #0-idle, 1-going to client 2-idle but memory is full 3-going to kichen
        self.state = State(self.position, self.direction,"",None)
        self.memorySize = 5
        self.inMemory = 0

    def render(self, display):
        display.blit(
            self._waiter_image,
            (self.position.x * self._size, self.position.y * self._size)
        )
    
    def move(self,moveType):
        
        current_index = directions.index(self.direction)

        if moveType == 'L':
            new_index = (current_index - 1) % len(directions)
            self.direction = directions[new_index]
            self._waiter_image=dirImgs[new_index]
        elif moveType == 'R':
            new_index = (current_index + 1) % len(directions)
            self.direction = directions[new_index]
            self._waiter_image=dirImgs[new_index]
        
        elif moveType=='F':
            x = int(self.position.x + self.direction.x)
            y = int(self.position.y + self.direction.y)
            if (0<=x<WIDTH and 0<=y<HEIGHT):
                self.position = Vector2(x,y)
        self.state = State(self.position,self.direction,"",None)
    
    def handle(self, client: Client):
        client.handled = 1
        handledSound.play()
        self.inMemory += 1
        if(self.inMemory == self.memorySize): self.status = 2
        else: self.status = 0

    def inKitchen(self):
        self.inMemory = 0
        self.status = 0
        inKitchenSound.play()