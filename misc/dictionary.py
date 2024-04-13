from pygame.math import Vector2
import pygame
pygame.mixer.init()

directions = [
        Vector2(0, 1), #s
        Vector2(-1, 0), #w
        Vector2(0, -1),  #n
        Vector2(1, 0)    #e
    ]
names = ["Jan", "Krzysztof", "Daniel", "Maciej", "Piotr"]
surnames = ["Kowalski", "Nowak", "Szymczak", "Polak", "Dabrowski"]
handledSound = pygame.mixer.Sound("sounds/handled.wav")
inKitchenSound = pygame.mixer.Sound("sounds/inKitchen.wav")
