import pygame
import sys
import math
from win32api import GetSystemMetrics


pygame.init()
pygame.display.set_caption("A* Mańczak")
myfont = pygame.font.SysFont('Arial', 30)
pygame.mouse.set_visible(1)

window_size = window_width, window_height = int(
    GetSystemMetrics(0)/2), int(GetSystemMetrics(0)/2)

screen = pygame.display.set_mode(window_size)
gridDimension = cols, rows = 50, 50
gridSize = gridSizeWidth, girdSizeHeight = int(window_width /
                                               cols), int(window_height/rows)
startNode = x, y = 0, 0
endNode = x, y = cols-1, rows-1
# endNode = x, y = 0, 0
##########################################################################


class Node:
    def __init__(self, colNum, rowNum):
        # A* variables
        self.colNum = colNum
        self.rowNum = rowNum
        self.isStartNode = False
        self.isEndNode = False
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighborNodes = []
        self.parentNode = None
        # Drawing variables
        self.posX = colNum*gridSizeWidth
        self.posY = rowNum*girdSizeHeight
        self.inFillColour = (255, 255, 255)
        self.outlineColour = (0)
        self.rectOutline = pygame.Rect(self.posX, self.posY,
                                       gridSizeWidth, girdSizeHeight)
        self.rectInner = pygame.Rect(self.posX+1, self.posY+1,
                                     gridSizeWidth-2, girdSizeHeight-2)

    def select(self):
        if not self.isStartNode and not self.isEndNode:
            self.inFillColour = (0)
            self.outlineColour = (0, 0, 0)

    def unselect(self):
        if not self.isStartNode and not self.isEndNode:
            self.inFillColour = (255, 255, 255)
            self.outlineColour = (0)

    def addNeighbours(self, grid):

        if self.inFillColour != (0):
            # left border
            if self.colNum > 0 and grid[self.colNum-1][self.rowNum].inFillColour != (0):
                self.neighborNodes.append(grid[self.colNum-1][self.rowNum])

            # right border
            if self.colNum < gridDimension[0]-1 and grid[self.colNum+1][self.rowNum].inFillColour != (0):
                self.neighborNodes.append(grid[self.colNum+1][self.rowNum])

            # celing
            if self.rowNum > 0 and grid[self.colNum][self.rowNum-1].inFillColour != (0):
                self.neighborNodes.append(grid[self.colNum][self.rowNum-1])

            # floor
            if self.rowNum < gridDimension[1]-1 and grid[self.colNum][self.rowNum+1].inFillColour != (0):
                self.neighborNodes.append(grid[self.colNum][self.rowNum+1])

            """# left uo
            if self.colNum > 0 and self.rowNum > 0 and grid[self.colNum-1][self.rowNum-1].inFillColour != (0):
                self.neighborNodes.append(grid[self.colNum-1][self.rowNum-1])

            # right up
            if self.colNum < gridDimension[0]-1 and self.rowNum > 0 and grid[self.colNum+1][self.rowNum-1].inFillColour != (0):
                self.neighborNodes.append(grid[self.colNum+1][self.rowNum-1])

            # left down
            if self.colNum > 0 and self.rowNum < gridDimension[1]-1 and grid[self.colNum-1][self.rowNum+1].inFillColour != (0):
                self.neighborNodes.append(grid[self.colNum-1][self.rowNum+1])

            if self.colNum < gridDimension[0]-1 and self.rowNum < gridDimension[1]-1 and grid[self.colNum+1][self.rowNum+1].inFillColour != (0):
                self.neighborNodes.append(grid[self.colNum+1][self.rowNum+1])"""

    def draw(self):
        pygame.draw.rect(screen, self.outlineColour, self.rectOutline)
        pygame.draw.rect(screen, self.inFillColour, self.rectInner)


def heuristic(start, stop):
    d = abs(start.colNum-stop[0])+abs(start.rowNum-stop[1])
    #d = math.sqrt(abs(start.colNum-stop[0])**2+abs(start.rowNum-stop[1])**2)
    return d


grid = [[Node(i, j)
         for j in range(rows)]for i in range(cols)]

grid[startNode[0]][startNode[1]].isStartNode = True
grid[endNode[0]][endNode[1]].isEndNode = True
grid[startNode[0]][startNode[1]].inFillColour = (0, 255, 255)
grid[endNode[0]][endNode[1]].inFillColour = (255, 255, 0)
lmbHolding = False
drawingPhase = True
isLookinForNeigbours = True
openSet = []
closedSet = []
openSet.append(grid[startNode[0]][startNode[1]])
path = []
######################################################################
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and drawingPhase:
                for i in range(len(grid)):
                    for j in range(len(grid[0])):
                        grid[i][j].unselect()
            if event.key == pygame.K_q:
                drawingPhase = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            lmbHolding = True
        if event.type == pygame.MOUSEBUTTONUP:
            lmbHolding = False
        if lmbHolding and drawingPhase:
            mousePos = pygame.mouse.get_pos()
            try:
                grid[int(mousePos[0]/girdSizeHeight)
                     ][int(mousePos[1]/gridSizeWidth)].select()
            except:
                pass
    ###############################################################
    if not drawingPhase:

        if isLookinForNeigbours:
            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    grid[i][j].addNeighbours(grid)
            isLookinForNeigbours = False
            print(grid[2][2].neighborNodes)

        if len(openSet) > 0:  # There are still spots to evaleute

            winnerIndex = 0
            for i in range(len(openSet)):
                if openSet[i].f < openSet[winnerIndex].f:
                    winnerIndex = i
            current = openSet[winnerIndex]

            if current == grid[endNode[0]][endNode[1]]:  # Found the Solution

                print("Found a Path!")
                break

            openSet.remove(current)
            closedSet.append(current)

            neighbors = current.neighborNodes

            for i in range(len(neighbors)):
                curNeighbor = neighbors[i]

                if not curNeighbor in closedSet:

                    tempG = current.g + 1

                    if curNeighbor in openSet:

                        if tempG < curNeighbor.g:
                            curNeighbor.g = tempG
                            newPath = True
                    else:
                        curNeighbor.g = tempG
                        openSet.append(curNeighbor)
                        newPath = True

                    if newPath:
                        curNeighbor.h = heuristic(curNeighbor, endNode)
                        curNeighbor.f = curNeighbor.g + curNeighbor.h
                        curNeighbor.parentNode = current

                    path = []
                    temp = current
                    path.append(temp)
                    while temp.parentNode:
                        path.append(temp.parentNode)
                        temp = temp.parentNode

        else:  # No solution
            print("No path!")
            break

            ######################################################################
    for i in range(len(closedSet)):
        closedSet[i].inFillColour = (255, 0, 0)
    for i in range(len(openSet)):
        openSet[i].inFillColour = (0, 255, 0)

    for i in range(len(path)):
        path[i].inFillColour = (0, 0, 255)

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            grid[i][j].draw()

    pygame.display.flip()
    screen.fill((255, 255, 255))

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    for i in range(len(closedSet)):
        closedSet[i].inFillColour = (255, 0, 0)
    for i in range(len(openSet)):
        openSet[i].inFillColour = (0, 255, 0)

    for i in range(len(path)):
        path[i].inFillColour = (0, 0, 255)
    grid[startNode[0]][startNode[1]].inFillColour = (0, 255, 255)
    grid[endNode[0]][endNode[1]].inFillColour = (255, 255, 0)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            grid[i][j].draw()

    pygame.display.flip()
    screen.fill((255, 255, 255))

# Mańczak
