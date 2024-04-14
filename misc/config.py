import pygame

TILE_SIZE = 40
WIDTH = 30
HEIGHT = 20
FRAMERATE = 10
BAR=5


DISPLAY = pygame.display.set_mode((WIDTH * TILE_SIZE, HEIGHT * TILE_SIZE))
CLOCK = pygame.time.Clock()
pygame.display.set_caption('Kelner')