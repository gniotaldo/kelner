
from pygame.math import Vector2
import pygame
from misc.dictionary import directions
from classes.Map import Map
from misc.config import HEIGHT,WIDTH
from collections import deque

class State:
    def __init__(self, position: Vector2, direction: Vector2, move: str, parent=None):
        self.position = position
        self.direction = direction
        self.move = move
        self.parent = parent
        self.facing = Vector2(int(self.position.x + self.direction.x),int(self.position.y + self.direction.y))

    def treeMove(self, moveType, map: Map):
        tempPosition = self.position
        tempDirection = self.direction
        parent = self
        currentIndex = directions.index(tempDirection)

        if moveType == 'L':
            newIndex = (currentIndex - 1) % len(directions)
            tempDirection = directions[newIndex]

        elif moveType == 'R':
            newIndex = (currentIndex + 1) % len(directions)
            tempDirection = directions[newIndex]
        
        elif moveType == 'F':
            tempDirection = self.direction
            x = int(self.position.x + self.direction.x)
            y = int(self.position.y + self.direction.y)
            if (0 <= x < WIDTH and 0 <= y < HEIGHT and map.map_grid[x][y] == map.Cell.EmptyCell):
                tempPosition = Vector2(x, y)

        newState = State(tempPosition, tempDirection, moveType, parent)
        return newState

    def treeSearch(self, goal: Vector2,map):
        def distance(tile1: Vector2, tile2: Vector2):
            deltaX = abs(tile1.x - tile2.x)
            deltaY = abs(tile1.y - tile2.y)
            dist = deltaX + deltaY
            return dist
        
        toVisit = deque()
        visited = deque()
        searching = True
        if self.facing == goal: 
            return[]
        toVisit.append(self)
        stateParity = 0
        while searching and toVisit:
            currentState: State = toVisit.popleft()
            if stateParity == 0: oldDistance = distance(currentState.position,goal)
            stateParity = (stateParity + 1) % 15
            for move in ('F','L', 'R'):
                newState: State = currentState.treeMove(move,map)
                progress = oldDistance - distance(newState.position, goal)
                if stateParity == 0: 
                    if   progress < 1: #sprawdza tylko te poddrzewa ktore w ciagu 15 ruchow sa o 1 jednostke blizej celu
                        print(f"slaby progress: {progress}")
                        continue
                    else:
                        print(f"dobry progress: {progress}")
                if progress < -2: #sprawdzamy tylko te poddrzewa ktore nigdy nie oddalaja sie o 2 jednostki od celu 
                        print(f"slaby progress: {progress}")
                        continue
                if (newState.position, newState.direction) not in visited: 
                    toVisit.append(newState)
                else: continue
                if newState.facing  == goal:
                    searching = False
                    path = newState.getPath()
                    break
            visited.append((newState.position, newState.direction))
        if searching: return []
        else: return path
    def getPath(self) :
        if self.parent is None:
            return []
        else:
            parentPath= self.parent.getPath()
            parentPath.append(self.move)
            return parentPath