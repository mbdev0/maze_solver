from dis import dis
import pygame 
import time
class Cell:
    def __init__(self,x,y,w,display):
        self.x = x
        self.y = y
        self.w = w
        self.display = display
        self.walls = [True,True,True,True] #Left Right Up Down

    def displayCell(self):
        x_coord = self.x*self.w
        y_coord = self.y*self.w
        
        if self.walls[0]:
            pygame.draw.line(display, (255,255,255), (x_coord,y_coord), (x_coord + self.w, y_coord), 1)
        if self.walls[1]:
            pygame.draw.line(display, (255,255,255), (x_coord,y_coord + self.w),(x_coord + self.w, y_coord + self.w), 1)
        if self.walls[2]:
            pygame.draw.line(display, (255,255,255), (x_coord,y_coord),(x_coord, y_coord+ self.w) , 1)
        if self.walls[3]:
            pygame.draw.line(display, (255,255,255), (x_coord + self.w, y_coord),(x_coord+self.w, y_coord+self.w) , 1)


if __name__ == '__main__':
    pygame.init()
    width = 500
    height = 500
    wOfCell = 50

    cols = int(width/wOfCell)
    rows = int(height/wOfCell)
    grid = []

    display = pygame.display.set_mode((width,height))


    for x in range(cols):
        for y in range(rows):
            grid.append(Cell(x,y,wOfCell,display))

    finished = False
    while not finished:
        for i in range(len(grid)):
            grid[i].displayCell()

        """
        DFS will go here
        """


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
        

        pygame.display.update()
        display.fill((0,0,0))
