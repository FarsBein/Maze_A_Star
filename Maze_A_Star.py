import pygame
import random
from queue import PriorityQueue

pygame.init()
WIDTH = 800
SCREEN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("Learing pygame")

BLACK = (0, 0, 0)
WHITE = (250, 250, 250)
RED = (255,0,0)
BLUE = (0,0,255)
LIGHT_BLUE = (173, 216, 230)
GREEN =(0,255,0)
GRAY = (220,220,220)
PINK = (255,182,193)
class Node:
    def __init__(self,row,col,size,total_row):
        self.row   = row
        self.col   = col
        self.size = size
        self.x   = size*row
        self.y   = size*col
        self.color = WHITE
        self.down  = True
        self.right = True
        self.neighbors = [] 
        self.total_row = total_row
    def get_pos(self):
        return self.row,self.col
    def get_pixel_pos(self):
        return self.x,self.y
    def draw(self,screen):
        pygame.draw.rect(screen,self.color,(self.x+4,self.y+4,self.size-6,self.size-6))
    def is_down(self):
        return self.down
    def is_right(self):
        return self.right
    def make_start(self):
        self.color = GREEN
    def make_end(self):
        self.color = RED
    def make_down(self,condition):
        self.down = condition
    def make_right(self,condition):
        self.right = condition
    def make_player(self):
        self.color = GRAY
    def make_empty(self):
        self.color = WHITE
    def make_open(self):
        self.color = LIGHT_BLUE
    def make_closed(self):
        self.color = BLUE
    def make_path(self):
        self.color = GREEN
    def update_neighbors(self, grid):
        self.neighbors=[]
        if self.row > 0 and not grid[self.row-1][self.col].is_right():
            self.neighbors.append(grid[self.row-1][self.col])
        if self.col > 0 and not grid[self.row][self.col-1].is_down():
            self.neighbors.append(grid[self.row][self.col-1])
        if self.row < self.total_row-1 and not grid[self.row][self.col].is_right():
            self.neighbors.append(grid[self.row+1][self.col])
        if self.col < self.total_row-1 and not grid[self.row][self.col].is_down():
            self.neighbors.append(grid[self.row][self.col+1])
    def __it__(self,other):
        return False
    

def draw_node(screen,grid):
    for row in grid:
        for node in row:
            node.draw(screen)
    pygame.display.update()
def h(pos_1,pos_2):
    y1,x1 = pos_1
    y2,x2 = pos_2
    return abs(x1-x2) + abs(y1-y2)

# def h_solver(draw,grid,start,end):
#     old_option=[]
#     current_path=[]
def draw_final_line(draw, came_from, current):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def a_star(draw,grid,start,end):
    print("a_Star starts")
    count = 0
    open_set = PriorityQueue()
    open_set.put((0,count, start))
    came_from = {}
    g_score = {node:float("inf") for row in grid for node in row}
    g_score[start]=0
    f_score = {node:float("inf") for row in grid for node in row}
    f_score[start]=h(start.get_pos(),end.get_pos())

    open_set_hash = {start}
    
    while not open_set.empty():
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
        current = open_set.get()[2] #current node
        open_set_hash.remove(current)
        if current == end:
            draw_final_line(draw,came_from, current)
            return True
        for neighbor in current.neighbors:
            # print(not neighbor.is_right(),not neighbor.is_down())
            
            temp_g_score = g_score[current]+1            
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor]   = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(),end.get_pos())
                if neighbor not in open_set_hash:
                    count+=1
                    open_set.put((f_score[neighbor],count,neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()        

    print("a_Star ends")
        
def make_grid(rows,width):
    size=width//rows
    grid=[]
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i,j,size,rows)
            grid[i].append(node)
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
                pygame.draw.line(screen,BLACK,[row,col+size],[row+size,col+size],3)
            if node.is_right():
                pygame.draw.line(screen,BLACK,[row+size,col],[row+size,col+size],3)
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
    while len(visited) < len_grid**2:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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

    start = grid[0][0]
    end = grid[ROWS-1][ROWS-1]
    
    while gameRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and made_grid:
                    # grid[5][5].make_open()
                    # grid[4][5].make_open()
                    # draw_node(screen,grid)
                    # print(grid[5][5],"is_down:",grid[5][5].is_down(),"is_right:",grid[5][5].is_right())
                    # print(grid[4][5],"is_down:",grid[4][5].is_down(),"is_right:",grid[4][5].is_right())
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    a_star(lambda: draw_node(screen,grid),grid,start,end)
            if event.type == pygame.K_r:
                gameRunning = False
                main(screen,width)
        if not made_grid:
            gen_maze(grid)
            start.make_start()
            end.make_end()
            start.draw(screen)
            end.draw(screen)
            draw_grid(screen,grid,size)
            pygame.display.update()
            made_grid = True
    pygame.quit()
    
                
main(SCREEN,WIDTH)
            