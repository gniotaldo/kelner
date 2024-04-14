import pygame
import random
import heapq # do metody 2 na znajdowanie najblizszego klienta
from typing import List
from pygame.math import Vector2
from pygame.locals import *
from misc.config import *
from misc.images import barImg
from classes.Map import Map
from classes.Agent import Agent
from classes.Client import Client
from classes.Table import Table
from classes.Seat import Seat
from classes.Meal import spaghetti, pizza, burger, menu
from misc.dictionary import names, surnames

def tick():
    CLOCK.tick(FRAMERATE)
    restaurant_map.render(DISPLAY)
    for table in tables:
        table.render(DISPLAY)
    for seat in seats:
        seat.render(DISPLAY)
    for client in clients:
        client.render(DISPLAY,ticks)
    agent.render(DISPLAY)
    DISPLAY.blit(barImg,(0,0))
    text_surface = font.render("Memory space: {}".format(agent.memorySize - agent.inMemory), True, (255, 255, 255))
    DISPLAY.blit(text_surface, (10, 10))
    text_surface = font.render("Orders in memory:", True, (255, 255, 255))
    DISPLAY.blit(text_surface, (10, 40))
    labelY=40
    for order in agent.ordersInMemory:
        labelY += 20
        text_surface = font.render("{}".format(order.meal.name), True, (255, 255, 255))
        DISPLAY.blit(text_surface, (20, labelY))

    labelY +=40
    text_surface = font.render("Orders in preparing:", True, (255, 255, 255))
    DISPLAY.blit(text_surface, (10, labelY))
    for order in agent.ordersInKitchen:
        labelY += 20
        if order.status == 2:
            label: any = order.meal.cookingTime - order.timePrepared
        else: label: any = "Done"
        text_surface = font.render("{} - {}".format(order.meal.name, label), True, (255, 255, 255))
        DISPLAY.blit(text_surface, (20, labelY))

    labelY +=40
    text_surface = font.render("Orders in Hands:", True, (255, 255, 255))
    DISPLAY.blit(text_surface, (10, labelY))
    for order in agent.ordersInHands:
        labelY += 20
        text_surface = font.render("{}".format(order.meal.name), True, (255, 255, 255))
        DISPLAY.blit(text_surface, (20, labelY))

    pygame.display.flip()
    pygame.display.update()
    

if __name__ == '__main__': 
    pygame.init()
    font = pygame.font.SysFont(None, 25)
    restaurant_map = Map(WIDTH, HEIGHT, TILE_SIZE)
    initial_position = restaurant_map.get_initial_posistion_for_waiter()
    agent = Agent(initial_position, TILE_SIZE,restaurant_map)
    restaurant_map.set_map()
    tables = [Table(Vector2(x, y), TILE_SIZE, WIDTH, HEIGHT) for (x, y) in restaurant_map.table_cells]
    seats: List[Seat] = []
    for table in tables:
        for (x,y) in table.seats_cells:
            seats.append(Seat(Vector2(x, y), TILE_SIZE,tables))
    
    num_clients = random.randint(7, 12)

    clients: List[Client] = []
    for _ in range(num_clients):
        name = random.choice(names)
        surname = random.choice(surnames)
        client = Client(name,surname,restaurant_map.map_grid, TILE_SIZE, seats)
        clients.append(client)

    is_running = True
    paused = False
    ticks = 0



    while is_running:
        unhandled_clients = [client for client in clients if client.handled == 0]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                else:
                    if event.key == pygame.K_w:
                        agent.move('W',restaurant_map)
                    elif event.key == pygame.K_s:
                        agent.move('S',restaurant_map)
                    elif event.key == pygame.K_a:
                        agent.move('A',restaurant_map)
                    elif event.key == pygame.K_d:
                        agent.move('D',restaurant_map)
                    for client in unhandled_clients:
                        if agent.facing == client.position:
                            if agent.inMemory == agent.memorySize:
                                break
                            agent.handle(client)
                            break
                    for client in clients:
                        if agent.facing == client.position and client.order in agent.ordersInHands:
                            agent.completeOrder(client.order)
                        
                        
                    if restaurant_map.map_grid[int(agent.facing.x)][int(agent.facing.y)] == restaurant_map.Cell.KitchenCell:
                        if agent.inMemory != 0:
                            agent.inKitchen()
                        for order in agent.ordersInKitchen:
                            if order.status == 3 and agent.inHands != agent.handsMax:
                                agent.ordersInHands.append(order)
                                agent.ordersInKitchen.remove(order)
                                agent.inHands += 1
                                order.status = 4

                    
        for order in agent.ordersInKitchen:
            if order.status == 2:
                if ticks%10 == 9: order.timePrepared += 1
                if order.timePrepared == order.meal.cookingTime:
                    order.status = 3


        if paused: continue
        if not(unhandled_clients):
            client = random.choice(clients)
            client.handled = 0
            client.placeOrder(random.choice(menu))
        tick()
        ticks += 1
    pygame.quit()
