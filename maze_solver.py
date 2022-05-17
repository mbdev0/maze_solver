import pygame 
import time
import random

def breakWalls(curr,next):
    diff_x = curr.x - next.x
    if diff_x == -1:
        curr.walls[3] = False
        next.walls[2] = False
    elif diff_x == 1:
        curr.walls[2] = False
        next.walls[3] = False

    diff_y = curr.y - next.y
    if diff_y == -1:
        curr.walls[1] = False
        next.walls[0] = False
    elif diff_y == 1:
        curr.walls[0] = False
        next.walls[1] = False

class Cell:

    def __init__(self,x,y,w,display,cols, rows,grid):
        self.x = x
        self.y = y
        self.w = w
        self.display = display
        self.walls = [True,True,True,True] #Top Bottom Left Right
        self.visited = False
        self.cols = cols
        self.rows = rows
        self.grid = grid

    def displayCell(self):
        x_coord = self.x*self.w
        y_coord = self.y*self.w
        
        if self.visited:
            pygame.draw.rect(self.display, (0, 0, 255), (x_coord, y_coord,self.w,self.w))

        if self.walls[0]:
            pygame.draw.line(self.display, (255,255,255), (x_coord,y_coord), (x_coord + self.w, y_coord), 1)
        if self.walls[1]:
            pygame.draw.line(self.display, (255,255,255), (x_coord,y_coord + self.w),(x_coord + self.w, y_coord + self.w), 1)
        if self.walls[2]:
            pygame.draw.line(self.display, (255,255,255), (x_coord,y_coord),(x_coord, y_coord+ self.w) , 1)
        if self.walls[3]:
            pygame.draw.line(self.display, (255,255,255), (x_coord + self.w, y_coord),(x_coord+self.w, y_coord+self.w) , 1)

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

    def display_grid(self):
        for i in grid:
            i.displayCell()
    
    def DFS(self):

        self.curr.visited = True
        self.curr.showCurrent()
        next_n = self.curr.findNeighbours()

        if next_n:
            next_n.visited = True
            self.dfs_stack.append(self.curr)
            breakWalls(self.curr, next_n)
            self.curr = next_n
        elif self.dfs_stack:
            self.curr = self.dfs_stack.pop()

if __name__ == '__main__':
    pygame.init()
    width = 300
    height = 300
    wOfCell = 30

    display = pygame.display.set_mode((width,height))

    maze = Maze(height,width,wOfCell)
    grid = maze.maze_generation(display)

    finished = False
    clock = pygame.time.Clock()

    while not finished:
        maze.display_grid()
        maze.DFS()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
        
        clock.tick(80)
        pygame.display.update()

