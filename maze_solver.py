from inspect import formatannotationrelativeto
import pygame 
import time
import random


class Cell:

    def __init__(self,x,y,w,display,cols, rows,grid):
        self.x = x
        self.y = y
        self.w = w
        self.display = display
        self.walls = {"N":True, "S":True, "W": True, "E":True}
        #self.walls = [True,True,True,True] #Top Bottom Left Right
        self.visited = False
        self.cols = cols
        self.rows = rows
        self.grid = grid

    def displayCell(self):
        x_coord = self.x*self.w
        y_coord = self.y*self.w
        
        if self.visited:
            pygame.draw.rect(self.display, (255, 255, 255), (x_coord, y_coord,self.w,self.w))

        if self.walls["N"]:
            pygame.draw.line(self.display, (0,0,0), (x_coord,y_coord), (x_coord + self.w, y_coord), 1)
        if self.walls["S"]:
            pygame.draw.line(self.display, (0,0,0), (x_coord,y_coord + self.w),(x_coord + self.w, y_coord + self.w), 1)
        if self.walls["W"]:
            pygame.draw.line(self.display, (0,0,0), (x_coord,y_coord),(x_coord, y_coord+ self.w) , 1)
        if self.walls["E"]:
            pygame.draw.line(self.display, (0,0,0), (x_coord + self.w, y_coord),(x_coord+self.w, y_coord+self.w) , 1)

    def index(self,x ,y):
        if x < 0 or y < 0 or x>self.cols-1 or y>self.rows-1:
            return -1

        return (x + y * self.cols)

    def findNeighbours(self):
        neighbours = []

        right = self.index(self.x+1, self.y)
        left = self.index(self.x-1, self.y)
        up = self.index(self.x, self.y+1)
        down = self.index(self.x, self.y-1)

        if right != -1:
            if not grid[right].visited:
                neighbours.append(grid[right])
        if left != -1:   
            if not grid[left].visited:
                neighbours.append(grid[left])
        if up != -1:
            if not grid[up].visited:
                neighbours.append(grid[up])
        if down != -1:
            if not grid[down].visited:
                neighbours.append(grid[down])

        if (neighbours):
            return neighbours[random.randint(0, len(neighbours)-1)]
        else: return None

    def showCurrent(self):
        x_coord = self.x*self.w
        y_coord = self.y*self.w

        pygame.draw.rect(self.display, (255,0,0), (x_coord,y_coord, self.w, self.w))
    
    def showStartorEnd(self, index):
            cell = grid[index]
            cell_x = cell.x*self.w
            cell_y = cell.y*self.w
            return (cell_x, cell_y,self.w,self.w)

    def showPath(self):
        x_coord = self.x*self.w
        y_coord = self.y*self.w
        

        start = self.showStartorEnd(0)
        end = self.showStartorEnd(-1)
        
        pygame.draw.rect(self.display, (50, 168, 92), start)
        pygame.draw.rect(self.display, (168, 50, 50), end)
        
        pygame.draw.rect(self.display, (27, 94, 227), (x_coord+10,y_coord+10, self.w-20, self.w-20))
        time.sleep(0.2)
        pygame.display.flip()
        
    def showFinalPath(self):
        x_coord = self.x*self.w
        y_coord = self.y*self.w
        
        start = self.showStartorEnd(0)
        end = self.showStartorEnd(-1)
        
        pygame.draw.rect(self.display, (50, 168, 92), start)
        pygame.draw.rect(self.display, (168, 50, 50), end)

        pygame.draw.rect(self.display, (27, 140, 46), (x_coord+10,y_coord+10, self.w-20, self.w-20))
        time.sleep(0.05)
        pygame.display.flip()


class Maze:
    def __init__(self,height,width,w) -> None:
        self.height = height
        self.width = width
        self.w = w 
        self.dfs_stack = []
        self.grid = []
        self.curr = None
    
    def maze_generation(self,display):
        cols = int(self.width/self.w)
        rows = int(self.height/self.w)
        grid = []

        for y in range(rows):
            for x in range(cols):
                grid.append(Cell(x,y,self.w,display, cols, rows, grid))

        self.curr = grid[0]
        return grid

    def breakWalls(self, curr, next):
        diff_x = curr.x - next.x
        if diff_x == -1:
            curr.walls["E"] = False
            next.walls["W"] = False
        elif diff_x == 1:
            curr.walls["W"] = False
            next.walls["E"] = False

        diff_y = curr.y - next.y
        if diff_y == -1:
            curr.walls["S"] = False
            next.walls["N"] = False
        elif diff_y == 1:
            curr.walls["N"] = False
            next.walls["S"] = False

    def refreshScreen(self,grid):
        for cell in grid:
                cell.displayCell()

    def DFS(self):
        self.curr.visited = True
        self.curr.showCurrent()
        next_n = self.curr.findNeighbours()

        if next_n:
            next_n.visited = True
            self.dfs_stack.append(self.curr)
            self.breakWalls(self.curr, next_n)
            self.curr = next_n
        elif self.dfs_stack:
            self.curr = self.dfs_stack.pop()

        return self.curr

    def BFS(self,grid):
        START = grid[0]
        frontier = [START]
        explored = [START]
        finalCell = grid[-1]

        bfs_path = {}
        
        while frontier:
            currCell = frontier.pop(0)
            currCell.showPath()
            if currCell == finalCell:
                self.refreshScreen(grid)
                break
            
            for direction in "ESNW":
                if currCell.walls[direction] ==False:
                    if direction == 'E':
                        childCell = grid[currCell.index(currCell.x+1, currCell.y)]
                    elif direction == 'S':
                        childCell = grid[currCell.index(currCell.x, currCell.y+1)]
                    elif direction == 'N':
                        childCell = grid[currCell.index(currCell.x, currCell.y-1)]
                    elif direction == 'W':
                        childCell = grid[currCell.index(currCell.x-1, currCell.y)]

                    if childCell in explored:
                        continue

                    frontier.append(childCell)
                    explored.append(childCell)
                    bfs_path[childCell] = currCell


        finalPath={}
        while START!=finalCell: 
            finalPath[bfs_path[finalCell]]=finalCell
            finalCell = bfs_path[finalCell]
        

        startToEnd= dict(reversed(list(finalPath.items())))
        for cell in startToEnd.values():
            cell.showFinalPath()

        return finalPath

if __name__ == '__main__':
    pygame.init()
    width = 900
    height = 900
    wOfCell = 100

    display = pygame.display.set_mode((width,height))
    path = None
    maze = Maze(height,width,wOfCell)
    grid = maze.maze_generation(display)

    finished = False
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        if not finished:
            maze.refreshScreen(grid)
            
            current = maze.DFS()
            if current == grid[0]:
                maze.refreshScreen(grid)

                maze.BFS(grid)

                finished=True
            
            pygame.display.update()
