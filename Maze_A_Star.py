import pygame

pygame.init()
WIDTH = 800
SCREEN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("Learing pygame")

BLACK = (0, 0, 0)
WHITE = (250, 250, 250)
RED = (255,0,0)
BLUE = (0,0,255)
class Node:
    def __init__(self,row,col,width):
        self.row = row
        self.col = col
        self.color = WHITE
        self.width = width
    def get_pos(self):
        return self.row,self.col
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
            node = Node(i*size,j*size,width)
            grid[-1].append(node)
    return grid

def draw_grid(screen,grid,size):
    for i in range(len(grid)):
        for j in range(len(grid)):
            row,col = grid[i][j].get_pos()
            pygame.draw.line(screen,BLACK,[row,col],[row,col+size],1)
            pygame.draw.line(screen,BLACK,[row,col],[row+size,col],1)
            pygame.draw.line(screen,BLACK,[row,col+size],[row+size,col+size],1)
            pygame.draw.line(screen,BLACK,[row+size,col],[row+size,col+size],1)
            pygame.display.update()

def main(screen,width):
    ROWS=10
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
                
main(SCREEN,WIDTH)
            