import pygame
import random
import heapq # do metody 2 na znajdowanie najblizszego klienta
from typing import List
from pygame.math import Vector2
from pygame.locals import *
from misc.config import *
from classes.Map import Map
from classes.Agent import Agent
from classes.Client import Client
from classes.Table import Table
from classes.Seat import Seat
from classes.Meal import spaghetti, pizza, burger
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
    pygame.display.flip()
    pygame.display.update()
    

if __name__ == '__main__': 
    pygame.init()
    restaurant_map = Map(WIDTH, HEIGHT, TILE_SIZE)
    initial_position = restaurant_map.get_initial_posistion_for_waiter()
    agent = Agent(initial_position, TILE_SIZE,restaurant_map)
    table_cells = restaurant_map.set_map()
    tables = [Table(Vector2(x, y), TILE_SIZE, WIDTH, HEIGHT) for (x, y) in table_cells]
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
    ticks=0
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
        if paused: continue
        ticks = (ticks+1)%10
        unhandled_clients = [client for client in clients if client.handled == 0]
        
        if unhandled_clients and agent.status == 0:
            #metody na znajdowanie najblizszego/najblizszych klientow
            
            #metoda 1 (najblizszy klient po przekatnej)- wydajna, lecz czasem mowi nieprawde
            closest_client = min(unhandled_clients, key=lambda client: agent.position.distance_to(client.position))
            closestClients = [closest_client] #to jest tylko po to zeby latwiej przelaczac sie miedzy metoda 1 i 2
            
            #metoda 2 - mniej wydajna (zazwyczaj musi obliczyc przez BFS droge do 2 klientow i wybrac ktorsza), raczej zawsze mowi prawde
            '''
            closestClients = heapq.nsmallest(2, unhandled_clients, key=lambda client: agent.position.distance_to(client.position))
            if len(closestClients) == 2:
                if (abs(agent.position.distance_to(closestClients[0].position) - agent.position.distance_to(closestClients[1].position)) > 4):
                    closestClients.pop(1)
                    print("drugi najblizszy klient jest zbyt daleko, nie szukam sciezki BFS")
            '''
            isFirst = True  
            for client in closestClients:
                path = agent.state.treeSearch(client.position, restaurant_map)
                if isFirst:
                    shortestPath = path
                    closestClient = client
                    isFirst = False
                elif len(path) < len(shortestPath):
                    shortestPath = path
                    closestClient = client
            print("ide do klienta")
            print(shortestPath)
            agent.status = 1
        if agent.status == 1:
            if shortestPath != []:
                move = shortestPath.pop(0)
                agent.move(move)
            else:
                agent.handle(closestClient)
        if agent.status == 2:
            kitchenCells = [Vector2(x, y) for (x, y) in restaurant_map.kitchen_cells]
            closest_kitchenCell = min(kitchenCells, key=lambda cell: agent.position.distance_to(cell))
            shortestPath = agent.state.treeSearch(closest_kitchenCell, restaurant_map)
            print("ide do kuchni")
            print(shortestPath)
            agent.status = 3
        if agent.status == 3:
            if shortestPath != []:
                move = shortestPath.pop(0)
                agent.move(move)
            else:
                agent.inKitchen()

        if not(unhandled_clients):
            random.choice(clients).handled = 0
        tick()
    pygame.quit()
