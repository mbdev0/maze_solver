import pygame 
import random
import sys
class Cell:

    def __init__(self,x,y,w,display,cols, rows,grid):
        self.x = x
        self.y = y
        self.w = w
        self.display = display
        self.walls = {"N":True, "S":True, "W": True, "E":True}
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
            if not self.grid[right].visited:
                neighbours.append(self.grid[right])
        if left != -1:   
            if not self.grid[left].visited:
                neighbours.append(self.grid[left])
        if up != -1:
            if not self.grid[up].visited:
                neighbours.append(self.grid[up])
        if down != -1:
            if not self.grid[down].visited:
                neighbours.append(self.grid[down])

        if (neighbours):
            return neighbours[random.randint(0, len(neighbours)-1)]
        else: return None

    def showCurrent(self):
        x_coord = self.x*self.w
        y_coord = self.y*self.w

        pygame.draw.rect(self.display, (255,0,0), (x_coord,y_coord, self.w, self.w))
        
    def showStartorEnd(self, index):
        cell = self.grid[index]
        cell_x = cell.x*self.w
        cell_y = cell.y*self.w
        return (cell_x, cell_y,self.w,self.w)

    def showPath(self):
        x_coord = self.x*self.w
        y_coord = self.y*self.w
        outer = pygame.Rect(x_coord, y_coord, self.w, self.w)
        inner = pygame.Rect(x_coord*1.5,y_coord*1.5, self.w/1.5, self.w/1.5)
        inner.center = outer.center

        start = self.showStartorEnd(0)
        end = self.showStartorEnd(-1)
        
        pygame.draw.rect(self.display, (50, 168, 92), start)
        pygame.draw.rect(self.display, (168, 50, 50), end)
        
        pygame.draw.rect(self.display, (27, 94, 227), inner)
        pygame.display.flip()
        
    def showFinalPathHelper(self):
        x_coord = self.x*self.w
        y_coord = self.y*self.w
        outer = pygame.Rect(x_coord, y_coord, self.w, self.w)
        inner = pygame.Rect(x_coord*1.5,y_coord*1.5, self.w/1.5, self.w/1.5)
        inner.center = outer.center

        start = self.showStartorEnd(0)
        end = self.showStartorEnd(-1)
        
        pygame.draw.rect(self.display, (50, 168, 92), start)
        pygame.draw.rect(self.display, (168, 50, 50), end)

        pygame.draw.rect(self.display, (27, 140, 46), inner)
        
class Maze:
    def __init__(self,cols,rows,w,grid=[]) -> None:
        self.cols = cols
        self.rows = rows
        self.w = w 
        self.dfs_stack = []
        self.grid = grid
        self.curr = None
        self.clock = pygame.time.Clock()
        self.display = None
    def maze_generation(self,display):
        grid = []
        self.display = display
        for y in range(self.rows):
            for x in range(self.cols):
                grid.append(Cell(x,y,self.w,display, self.cols, self.rows, grid))

        self.curr = grid[0]
        self.dfs_stack.append(self.curr)
        self.grid = grid
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

    def DFS(self,showBuilding=True,fullSpeed = True):
        while self.dfs_stack:
            if showBuilding:
                self.refreshScreen(self.grid)
                self.curr.showCurrent()
                if not fullSpeed:
                    self.clock.tick(60)

            else:
                myfont = pygame.font.SysFont("monospace", 30)
                label = myfont.render("Loading...", 1, (255,255,0))
                self.display.blit(label, (250, 250))
            self.curr.visited = True
            next_n = self.curr.findNeighbours()
            if next_n:
                next_n.visited = True
                self.dfs_stack.append(self.curr)
                self.breakWalls(self.curr, next_n)
                self.curr = next_n
            elif self.dfs_stack:
                self.curr = self.dfs_stack.pop()
            pygame.display.flip()

    def BFS(self,grid,fullSpeed = True):
        START = grid[0]
        frontier = [START]
        explored = [START]
        finalCell = grid[-1]

        bfs_path = {}
        
        while frontier:
            currCell = frontier.pop(0)
            currCell.showPath()
            pygame.display.flip()
            if not fullSpeed:
                self.clock.tick(60)
            
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

        return finalPath
        
    def BFSfinalPath(self,finalPath,fullSpeed = True):
        startToEnd= dict(reversed(list(finalPath.items())))
        for cell in startToEnd.values():
            if not fullSpeed:
                self.clock.tick(60)
            cell.showFinalPathHelper()
            pygame.display.flip()

class MenuSelection:
    def __init__(self):
        self.maze_gen_fullspeed = True
        self.maze_gen_showBuilding = True
        self.bfs_search_fullspeed = True
        self.final_path_fullspeed = True

    def MainMenu(self):
        print("""
        
  __  __                  _____       _                                         
 |  \/  |                / ____|     | |                                        
 | \  / | __ _ _______  | (___   ___ | |_   _____ _ __                          
 | |\/| |/ _` |_  / _ \  \___ \ / _ \| \ \ / / _ \ '__|                         
 | |  | | (_| |/ /  __/  ____) | (_) | |\ V /  __/ |                            
 |_|  |_|\__,_/___\___| |_____/ \___/|_| \_/ \___|_|         _             ___  
                          |  _ \                  | |       | |           / _ \ 
                          | |_) |_   _   _ __ ___ | |__   __| | _____   _| | | |
                          |  _ <| | | | | '_ ` _ \| '_ \ / _` |/ _ \ \ / / | | |
                          | |_) | |_| | | | | | | | |_) | (_| |  __/\ V /| |_| |
                          |____/ \__, | |_| |_| |_|_.__/ \__,_|\___| \_/  \___/ 
                                  __/ |                                         
                                 |___/                                          

        """)


        self.currentOptions()

        print("""
        1. Start Maze
        2. Options
        3. Exit
    """)

        self.menu = int(input("Choose an Option: "))

        if self.menu == 1:
            self.StartMaze()
        if self.menu == 2:
            self.options()
        if self.menu == 3:
            sys.exit()

    def StartMaze(self):
        width = 500
        height = 500

        cols = int(input("How Many Columns?: "))
        rows = int(input("How Many Rows?: "))
        wOfCell = 0
        
        if cols>rows:
            wOfCell = width/cols
        elif cols<rows:
            wOfCell = height/rows
        else:
            wOfCell = height/rows

        display = pygame.display.set_mode((width,height))
        maze = Maze(cols,rows,wOfCell)
        grid = maze.maze_generation(display)
        maze.DFS(showBuilding = self.maze_gen_showBuilding,fullSpeed = self.maze_gen_fullspeed)
        maze.refreshScreen(grid)
        solution = maze.BFS(grid,fullSpeed = self.bfs_search_fullspeed)
        maze.BFSfinalPath(solution, fullSpeed = self.final_path_fullspeed)
    
    def currentOptions(self):
        maze_gen_speed = ""
        bfs_search_speed = ""
        final_path_speed = ""

        if self.maze_gen_fullspeed and self.maze_gen_showBuilding:
            maze_gen_speed = "Full Speed"
        elif (not self.maze_gen_fullspeed) and self.maze_gen_showBuilding:
            maze_gen_speed = "Default Speed (60fps)"
        else: maze_gen_speed = "You won't be seeing the generation so dont worry about the speed!"

        if self.bfs_search_fullspeed:
            bfs_search_speed = "Full Speed"
        else: bfs_search_speed = "Default Speed (60fps)"

        if self.final_path_fullspeed:
            final_path_speed = "Full Speed"
        else:  final_path_speed = "Default Speed (60fps)"

        print(f"""
            Current Options:

                Maze Generation Show Building: {self.maze_gen_showBuilding}
                Maze Generation Speed: {maze_gen_speed}

                Breadth First Search Visual Speed: {bfs_search_speed}

                Final Path Speed: {final_path_speed}
        """)
    def options(self):
        
        self.currentOptions()

        print("""
  
            1. Maze Generation options
            2. Breadth First Search Algorithm options
            3. Final Path options
            4. Exit

        """)
        
        selection = int(input("Choose an Option: "))

        if selection == 1:
            print("""
            How would you like to watch the maze generation?

            Warning, for bigger mazes i'd advise to not see the maze generation unless you like how pretty it looks!

            1. Full Speed
            2. Default Speed
            3. Not See It ----> You will get a loading screen instead
            4. See It
            """)
            option = int(input("Option: "))
            if option == 1:
                self.maze_gen_fullspeed = True
                self.options()
            elif option == 2:
                self.maze_gen_fullspeed = False
                self.options()
            elif option == 3:
                self.maze_gen_showBuilding = False
                self.options()
            elif option == 4:
                self.maze_gen_showBuilding = True
                self.options()

        elif selection == 2:
            print("""
            How would you like to watch the breadth first search?

            1. Full Speed
            2. Default Speed
            """)
            option = int(input("Option: "))

            if option == 1:
                self.bfs_search_fullspeed = True
                self.options()
            elif option == 2:
                self.bfs_search_fullspeed = False
                self.options()
            else: print("Wrong input... Aborting"); self.options()

        elif selection == 3:
            print("""
            How would you like to watch the final successful path?

            1. Full Speed
            2. Default Speed
            """)
            option = int(input("Option: "))

            if option == 1:
                self.final_path_fullspeed = True
                self.options()
            elif option == 2:
                self.final_path_fullspeed = False
                self.options()
            else: print("Wrong input... Aborting"); self.options()

        elif selection == 4:
            print("Redirecting to main menu")
            self.MainMenu()
        else: print("That input doesn't exist"); self.options();

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()


    mainMenu = MenuSelection()
    selection = mainMenu.MainMenu()

    finished = False
    while not finished:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
                pygame.quit()
                exit()

