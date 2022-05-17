import pygame 
import time
import random

def breakWalls(curr,next):
    """
    Pygame starts from the top left so 

    --------------
    |      |     |
    | 45y  |     |
    -------------
    |      |     |
    | 46y  |     |
    --------------
    The top left square has a lower y index than the bottom left

    Finds the difference between the current index and the next node index
    If the difference is -1 it means that next node is higher in the x value therefore
    is on the right. 

    So we break the current wall to the right and also break the next node wall to the left
    """
    diff_x = curr.x - next.x
    if diff_x == -1:
        curr.walls[3] = False
        next.walls[2] = False
    elif diff_x == 1:
        curr.walls[2] = False
        next.walls[3] = False
    
    """
    Same happens here for the rows index/y index, 
    If the current is on top of the next, we break the bottom wall of the current
    and top wall of the next node.

    However if the current is on the bottom, then the difference will be positive as the current node has a higher index than the next
    so we break the top of the current and bottom of the next node
    """
    diff_y = curr.y - next.y
    if diff_y == -1:
        curr.walls[1] = False
        next.walls[0] = False
    elif diff_y == 1:
        curr.walls[0] = False
        next.walls[1] = False

class Cell:
    """
    Initialising Values
    """

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
        """
        X and Y value will be the x multiplied by the width of the cell otherwise known as w

        If the current cell is visited we will colour it in white
        
        Otherwise draw the each of the squares on the grid

        Top left == x,y
        Top right == x + width of cell, y
        Bottom left = x, y + width of cell
        Bottom Right = x + width of cell, y + width of cell

              <-> = width of cell
        x,y --------
            |      | ^
            |      | | = width of cell   
            --------

        """

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
    
    """
    We use an index formula to find a certain index of a chosen cell within a 1d array of cells

    However we also say that if x or y is either smaller than 0 or larger than the amount of columns, it is invalid so we throw it away
    """
    def index(self,x ,y):
        if x < 0 or y < 0 or x>self.cols-1 or y>self.rows-1:
            return -1

        return (x + y * self.cols)

    """
    We use the index function to find each of the neighboring cells
    lets say we had 0,0, its neighbours would be 1,0 to the right and 0,1 on the bottom.
    But because we try to find the left and top as well those would be out of bounds
    So we use if statements to throw away the -1's returned from the index function and add all valid neighbours to the array

    After that we choose a random valid neighbour in the array to send back to the main program
    """
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

    """
    A function to generate a rectangle to help show the current square
    """
    def showCurrent(self):
        x_coord = self.x*self.w
        y_coord = self.y*self.w

        pygame.draw.rect(self.display, (255,0,0), (x_coord,y_coord, self.w, self.w))

if __name__ == '__main__':
    pygame.init()
    width = 300
    height = 300
    wOfCell = 30

    """
    The amount of columns and rows will be stored here, e.g height = 300 and width = 300, and width of a cell = 30, then it will be a 10x10 grid as
    300/30 = 10 for the height, and 300/30 = 10 for the width. Height = Y, Width = X
    """
    cols = int(width/wOfCell)
    rows = int(height/wOfCell)
    grid = []

    """
    Create the display with chosen width and height
    And start generating each of the individual cells, remember each individual cell will have its own property
    e.g the first cell will have an x = 0 and y = 0, the width of that cell will be the same as the variable wOfCell
    the next cell will have an x = 1 and y = 0 and so on
    """
    display = pygame.display.set_mode((width,height))

    for y in range(rows):
        for x in range(cols):
            grid.append(Cell(x,y,wOfCell,display, cols, rows,grid))

    """
    This is the start of the recursive backtracking DFS algorithm

    We set the current as any cell, we choose the top left otherwise known as the first element of the grid
    We also initialise a stack here for use in our backtracking method
        
    While pygame is running:
        for every cell in grid, we display it to the screen meaning we draw it out using the displayCell method

        We set the current cell/curr as visited
        We visualise the current cell to see how the program is running, this is completely optional

        We find the next node/valid neighbours to the current cell and store in next_n to loop over them
        
        If there are neighbours that we havent visited:
            set the new neighbour as visited
            push it to the array to be used in case there are no other unvisited neighbours after this loop
            we break the walls between the current cell and the next cell using the breakWalls function we discussed earlier
            we then set the current to the neighbour re igniting the loop

            Now if we've gone through all of the visited neighbours,
            We can use the stack to go back through the cells we have visited and find one that hasnt been visited
            hence our backtracking
    """

    curr = grid[0]
    stack = []
    finished = False
    clock = pygame.time.Clock()

    while not finished:
        for i in grid:
            i.displayCell()

        
        curr.visited = True
        curr.showCurrent()
        next_n = curr.findNeighbours()

        if next_n:
            next_n.visited = True
            stack.append(curr)
            breakWalls(curr, next_n)
            curr = next_n
        elif stack:
            curr = stack.pop()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
        
        clock.tick(80)
        pygame.display.update()

