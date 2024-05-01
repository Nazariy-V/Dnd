import pygame
import sys,random
from connect import *
from settings import *
from tiling import *
from button import *
from attacks import *

grid = [[' ' for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]

players=dict()
player_row = START_ROW
player_col = START_COL
last_row = None
last_col = None
row=None
col=None
d_row=0
d_col=0
target_row=None
target_col=None
move_time=0
attacking=False
visited_cell = (None,None)

buttons=[]

buttons.append(Button(image=None, pos=((WIDTH + MARGIN) * GRID_SIZE + MARGIN + BOARD_MARGIN*1.5,
               (HEIGHT + MARGIN)), 
                            text_input="shortsword", font=get_font(30), base_color="Gray", hovering_color="White"))
buttons.append(Button(image=None, pos=((WIDTH + MARGIN) * GRID_SIZE + MARGIN + BOARD_MARGIN*1.5,
               (HEIGHT + MARGIN)*2), 
                            text_input="shortbow", font=get_font(30), base_color="Gray", hovering_color="White"))

pygame.init()

WINDOW_SIZE = [(WIDTH + MARGIN) * GRID_SIZE + MARGIN + 2 * BOARD_MARGIN,
               (HEIGHT + MARGIN) * GRID_SIZE + MARGIN]#1295,695
screen = pygame.display.set_mode(WINDOW_SIZE)

pygame.display.set_caption("DnD")

class Player(pygame.sprite.Sprite):
    def __init__(self, color, row, col,type,character):
        super().__init__()
        self.row=row
        self.col=col
        self.color=color
        self.character= character
        self.type=type
        self.pos=0
        self.image = pygame.transform.scale(get_standing(type,character),(WIDTH,HEIGHT))
    def standing(self):
        self.image = pygame.transform.scale(get_standing(self.type,self.character),(WIDTH,HEIGHT))
        self.pos=0
    def moving(self,rotation):
        self.image = pygame.transform.scale(get_moving(self.type,self.character,rotation)[self.pos],(WIDTH,HEIGHT))
        self.pos=1 if self.pos==0 else 0
all_sprites_group = pygame.sprite.Group()
for conection in get_connections():
    players[conection]=Player(GREEN,player_row,player_col,"soldier",(0,0))
    all_sprites_group.add(players[conection])

players["2"]=Player(GREEN,player_row+1,player_col+1,"soldier",(1,0))
all_sprites_group.add(players["2"])

for player,ob in players.items():
    grid[ob.row][ob.col]=player
for i in range(OBJECTS):
    n=random.randint(1,GRID_SIZE-2)
    m=random.randint(1,GRID_SIZE-2)
    grid[n][m]="obj" if grid[n][m]==" " else grid[n][m]
del n
del m
rock=pygame.image.load(f"assets/Rock Pile.png")
done = False

clock = pygame.time.Clock()

damage,at_range=(0,-1)

while not done:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for thing in buttons:
                if thing.checkForInput(pos):
                    attacking=False if attacking else True
                    damage,at_range = attack(eval(thing.text_input)())
            
            col = (pos[0] - BOARD_MARGIN) // (WIDTH + MARGIN)
            row = (pos[1]) // (HEIGHT + MARGIN)
            
            
            if get_turn() == MY_PLAYER:
                
                if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                    if grid[row][col] != " " and attacking == True and ((players[MY_PLAYER].row - at_range-1)<row<(players[MY_PLAYER].row + at_range+1) and (players[MY_PLAYER].col - at_range-1)<col<(players[MY_PLAYER].col + at_range+1)):
                        opponent= grid[row][col]
                        print(f"{opponent} damaged for {damage}")
                        attacking=False
                    if last_row==row and last_col==col:
                        grid[player_row][player_col] = ' '
                        d_row= 1 if players[MY_PLAYER].row<row else -1
                        d_col= 1 if players[MY_PLAYER].col<col else -1
                        target_row=row
                        target_col=col
                        damage,at_range=(0,-1)
                        grid[players[MY_PLAYER].row][players[MY_PLAYER].col] = MY_PLAYER
                        last_col=None
                        last_row=None
                        attacking=False
                    else:
                    
                        last_row=row
                        last_col=col
            
    if move_time==2 and (d_row!=0 or d_col!=0):
        if d_row==0:
            players[MY_PLAYER].moving(2 if d_col==1 else 1)
        else:
            players[MY_PLAYER].moving(0 if d_row==1 else 3)
    elif d_row==0 and d_col==0:
        players[MY_PLAYER].standing()
    if move_time==5:
        grid[players[MY_PLAYER].row][players[MY_PLAYER].col]=" "
        if players[MY_PLAYER].row!=target_row and players[MY_PLAYER].col!=target_col and grid[players[MY_PLAYER].row+d_row][players[MY_PLAYER].col+d_col]==" ":
            
            players[MY_PLAYER].col+=d_col
            players[MY_PLAYER].row+=d_row
            
        elif players[MY_PLAYER].row!=target_row and grid[players[MY_PLAYER].row+d_row][players[MY_PLAYER].col]==" ":
            players[MY_PLAYER].row+=d_row
        
            

        elif players[MY_PLAYER].col!=target_col and grid[players[MY_PLAYER].row][players[MY_PLAYER].col+d_col]==" ":
            players[MY_PLAYER].col+=d_col

        move_time=0
        grid[players[MY_PLAYER].row][players[MY_PLAYER].col] = MY_PLAYER
    
    else:
        move_time+=1
    if players[MY_PLAYER].row==target_row:
        d_row=0
        target_row=None
    if players[MY_PLAYER].col==target_col:
        d_col=0
        players[MY_PLAYER].image
        target_col=None
    
    
    screen.fill(BLACK)


    
   
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            cell_color = GRAY
            if (row, col) == (last_row,last_col):
                cell_color = WHITE
            if attacking==True and((players[MY_PLAYER].row - at_range-1)<row<(players[MY_PLAYER].row + at_range+1) and (players[MY_PLAYER].col - at_range-1)<col<(players[MY_PLAYER].col + at_range+1)):
                cell_color = RED
            pygame.draw.rect(screen, cell_color, [(MARGIN + WIDTH) * col + MARGIN + BOARD_MARGIN,
                                                  (MARGIN + HEIGHT) * row + MARGIN,
                                                  WIDTH, HEIGHT])
            font = pygame.font.SysFont(None, 30)
            text = font.render(grid[row][col], True, GREEN)
            if grid[row][col] =="obj":
                screen.blit(rock, ((MARGIN + WIDTH) * col + MARGIN + BOARD_MARGIN,
                               (MARGIN + HEIGHT) * row + MARGIN))
            elif  grid[row][col] != ' ':
                current=players[grid[row][col]]
                screen.blit(current.image, ((MARGIN + WIDTH) * current.col + MARGIN + BOARD_MARGIN,
                               (MARGIN + HEIGHT) * current.row + MARGIN))
    
    
    if last_col!=None and last_row!=None:
        current_cell = (players[MY_PLAYER].row, players[MY_PLAYER].col)
        next_cell = (last_row,last_col)
        pygame.draw.line(screen, players[MY_PLAYER].color, [(MARGIN + WIDTH) * current_cell[1] + MARGIN + WIDTH // 2 + BOARD_MARGIN,
                                         (MARGIN + HEIGHT) * current_cell[0] + MARGIN + HEIGHT // 2],
                         [(MARGIN + WIDTH) * next_cell[1] + MARGIN + WIDTH // 2 + BOARD_MARGIN,
                          (MARGIN + HEIGHT) * next_cell[0] + MARGIN + HEIGHT // 2], 5)
    for button in buttons:
        button.changeColor(pygame.mouse.get_pos())
        button.update(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()
