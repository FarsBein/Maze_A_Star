import pygame
import random

pygame.init()
WIDTH = 800
SCREEN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("Learing pygame")

BLACK = (0, 0, 0)
WHITE = (250, 250, 250)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN =(0,255,0)
class Node:
    def __init__(self,row,col,size):
        self.row   = row
        self.col   = col
        self.size = size
        self.x   = size*row
        self.y   = size*col
        self.color = WHITE
        self.down  = True
        self.right = True
    def get_pos(self):
        return self.row,self.col
    def get_pixel_pos(self):
        return self.x,self.y
    def draw(self,screen):
        pygame.draw.rect(screen,self.color,(self.x+self.size/4,self.y+self.size/4,self.size/2,self.size/2))
    def is_up(self):
        return self.up
    def is_down(self):
        return self.down
    def is_left(self):
        return self.left
    def is_right(self):
        return self.right
    def make_start(self):
        self.color = GREEN
    def make_end(self):
        self.color = BLUE
    def make_down(self,condition):
        self.down = condition
    def make_right(self,condition):
        self.right = condition
    def make_player(self):
        self.color = RED
    def make_end(self):
        self.color = BLUE
    def make_empty(self):
        self.color = WHITE
        
def make_grid(rows,width):
    size=width//rows
    grid=[]
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i,j,size)
            grid[-1].append(node)
    return grid

def draw_grid(screen,grid,size):
    for i in range(len(grid)):
        for j in range(len(grid)):
            node = grid[i][j]
            row,col = node.get_pixel_pos()
            # if node.is_left():
            #     pygame.draw.line(screen,BLACK,[row,col],[row,col+size],1)
            # if node.is_up():
            #     pygame.draw.line(screen,BLACK,[row,col],[row+size,col],1)
            if node.is_down():
                pygame.draw.line(screen,BLACK,[row,col+size],[row+size,col+size],1)
            if node.is_right():
                pygame.draw.line(screen,BLACK,[row+size,col],[row+size,col+size],1)
    pygame.display.update()

def random_direction(row,col,len_grid,grid,visited):
    x=0
    y=0
    possible_directions = [] # 0 is up, 1 is right, 2 is down, 3 is left
    
    if row - 1 >= 0 and grid[row-1][col] not in visited:
        possible_directions.append(0)
    if col + 1 < len_grid and grid[row][col+1] not in visited:
        possible_directions.append(1)
    if row + 1 < len_grid and grid[row+1][col] not in visited:
        possible_directions.append(2)
    if col - 1 >= 0 and grid[row][col-1] not in visited:
        possible_directions.append(3)
    
    if len(possible_directions) == 0:
        return y,x
    
    rand_dir = possible_directions[random.randrange(len(possible_directions))]
    
    if rand_dir == 0:
        y-=1
    if rand_dir == 1:
        x+=1
    if rand_dir == 2:
        y+=1
    if rand_dir == 3:
        x-=1
    return y,x
    

def gen_maze(grid):
    len_grid = len(grid)
    visited = [grid[0][0]]
    row = 0
    col = 0
    grid[3][0].make_right(False)
    # for idasd in range(5):
    while len(visited) < len_grid**2:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
                
        y,x = random_direction(row,col,len_grid,grid,visited)
        if y == 0 and x == 0:
            visited.insert(0,visited.pop())
        else:
            if y != 0:
                if row > row+y:
                    grid[row+y][col].make_right(False)
                else:
                    grid[row][col].make_right(False)
                visited.append(grid[row+y][col])
            if x != 0:
                if col > col+x:
                    grid[row][col+x].make_down(False)
                else:
                    grid[row][col].make_down(False)
                visited.append(grid[row][col+x])
        row,col = visited[-1].get_pos() 
        

def main(screen,width):
    ROWS=20
    gameRunning = True
    grid = make_grid(ROWS,width)
    size=width//ROWS
    
    screen.fill(WHITE)
    pygame.display.update()
    
    made_grid = False

    
    while gameRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()       
                gameRunning = False
            if pygame.mouse.get_pressed()[0]:
                row,col = pygame.mouse.get_pos()
                row = row//size
                col = col//size
                if (row == 0 and col == 0 ) or (row == ROWS-1 and col == ROWS-1):
                    pass
                else:
                    grid[row][col].make_player()
                    grid[row][col].draw(screen)
                    pygame.display.update()
            if pygame.mouse.get_pressed()[2]:
                row,col = pygame.mouse.get_pos()
                row = row//size
                col = col//size
                if (row == 0 and col == 0 ) or (row == ROWS-1 and col == ROWS-1):
                    pass
                else:
                    grid[row][col].make_empty()
                    grid[row][col].draw(screen)
                    pygame.display.update()
            if event.type == pygame.K_r:
                gameRunning = False
                main(screen,width)
        if not made_grid:
            gen_maze(grid)
            grid[0][0].make_start()
            grid[ROWS-1][ROWS-1].make_end()
            draw_grid(screen,grid,size)
            pygame.display.update()
            made_grid = True
                
main(SCREEN,WIDTH)
            