from pygame.math import Vector2
import pygame

class Meal:
    def __init__(self, name, price, cookingTime):
        self.name = name
        self.price = price
        self.cookingTime = cookingTime #in seconds
    
spaghetti = Meal("spaghetti",10,10)
burger = Meal("burger",7,5)
pizza = Meal("pizza",12,8)


