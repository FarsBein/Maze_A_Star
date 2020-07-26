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
class Node:
    def __init__(self,row,col,size):
        self.row   = row
        self.col   = col
        self.size = size
        self.x   = size*row
        self.y   = size*col
        self.color = WHITE
        self.up    = True
        self.down  = True
        self.left  = True
        self.right = True
    def get_pos(self):
        return self.row,self.col
    def get_pixel_pos(self):
        return self.x,self.y
    def draw(self,screen):
        pygame.draw.rect(screen,self.color,(self.x,self.y,self.size,self.size))
    def is_up(self):
        return self.up
    def is_down(self):
        return self.down
    def is_left(self):
        return self.left
    def is_right(self):
        return self.right
    def make_up(self,condition):
        self.up = condition
    def make_down(self,condition):
        self.down = condition
    def make_left(self,condition):
        self.left = condition
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
    grid[5][5].make_down(False)
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

def random_direction(row,col,visited):
    x=0
    y=0
    possible_directions = [] # 0 is up, 1 is right, 2 is down, 3 is left
    
    if row - 1 >= 0 and gird[row-1][col] not in visited:
        possible_directions.append(0)
    if col + 1 < len_grid and gird[row][col+1] not in visited:
        possible_directions.append(1)
    if row + 1 < len_grid and gird[row+1][col] not in visited:
        possible_directions.append(2)
    if col - 1 >= 0 and gird[row][col-1] not in visited:
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
    visited = []
    row = 0
    col = 0
    
    while len(visited) != len_grid**2:
        y,x = random_direction(row,col,visited)
        if y == 0 and x == 0:
            visited.insert(0,visited.pop())
        row,col = visited[-1].get_pos()
        gird[row][col]

        

def main(screen,width):
    ROWS=20
    gameRunning = True
    grid = make_grid(ROWS,width)
    size=width//ROWS
    
    screen.fill(WHITE)
    pygame.display.update()
    draw_grid(screen,grid,size)
    
    while gameRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                gameRunning = False
            if pygame.mouse.get_pressed()[0]:
                row,col = pygame.mouse.get_pos()
                row = row//size
                col = col//size
                # grid[row][col].make_down(False)
                # draw_grid(screen,grid,size)
                # grid[row][col].make_player()
                # grid[row][col].draw(screen)
                # pygame.display.update()
                
main(SCREEN,WIDTH)
            