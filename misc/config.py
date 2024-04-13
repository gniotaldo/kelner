import pygame

TILE_SIZE = 40
WIDTH = 25
HEIGHT = 25
FRAMERATE = 10


DISPLAY = pygame.display.set_mode((WIDTH * TILE_SIZE, HEIGHT * TILE_SIZE))
CLOCK = pygame.time.Clock()
pygame.display.set_caption('Kelner')