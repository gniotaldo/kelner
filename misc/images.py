from misc.config import TILE_SIZE
import pygame

size=TILE_SIZE

kelS=pygame.transform.scale(pygame.image.load("images/kelS.png"),(size, size))
kelW=pygame.transform.scale(pygame.image.load("images/kelW.png"),(size, size))
kelN=pygame.transform.scale(pygame.image.load("images/kelN.png"),(size, size))
kelE=pygame.transform.scale(pygame.image.load("images/kelE.png"),(size, size))
waiterImgs = [kelS, kelW, kelN, kelE]

imgWaiting = pygame.transform.scale(pygame.image.load("images/waiting.png"),(size, size))
imgClient = pygame.transform.scale(pygame.image.load("images/notemptyseat.png"),(size, size))
imgFreeSeat = pygame.transform.scale(pygame.image.load("images/seat.png"), (size, size))
imgTakenSeat = pygame.transform.scale(pygame.image.load("images/notemptyseat.png"),(size, size))
imgTable = pygame.transform.scale( pygame.image.load("images/krat_table.png"),  (size, size))
empty_cell = pygame.transform.scale(pygame.image.load("images/krat.png"),  (size, size))
kitchen_cell = pygame.transform.scale(pygame.image.load("images/kitchen.png"),  (size, size))

f1 = pygame.transform.scale(pygame.image.load("images/faces/f1.png"), (size, size))
f2 = pygame.transform.scale(pygame.image.load("images/faces/f2.png"), (size, size))
f3 = pygame.transform.scale(pygame.image.load("images/faces/f3.png"), (size, size))
f4 = pygame.transform.scale(pygame.image.load("images/faces/f4.png"), (size, size))
f5 = pygame.transform.scale(pygame.image.load("images/faces/f5.png"), (size, size))
f6 = pygame.transform.scale(pygame.image.load("images/faces/f6.png"), (size, size))
f7 = pygame.transform.scale(pygame.image.load("images/faces/f7.png"), (size, size))
f8 = pygame.transform.scale(pygame.image.load("images/faces/f8.png"), (size, size))
f9 = pygame.transform.scale(pygame.image.load("images/faces/f9.png"), (size, size))
f10 = pygame.transform.scale(pygame.image.load("images/faces/f10.png"), (size, size))
f11 = pygame.transform.scale(pygame.image.load("images/faces/f11.png"), (size, size))
f12 = pygame.transform.scale(pygame.image.load("images/faces/f12.png"), (size, size))


faces = [f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12]
