import pygame
import sys,random,socket,json
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



pygame.init()

WINDOW_SIZE = [(WIDTH + MARGIN) * GRID_SIZE + MARGIN + 2 * BOARD_MARGIN,
               (HEIGHT + MARGIN) * GRID_SIZE + MARGIN]#1295,695
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame_icon= pygame.image.load("assets/d20.jpg")
pygame.display.set_icon(pygame_icon)
pygame.display.set_caption("DnD")

attack_animation=(None,None)
counter= 0
pick=0
anims = []
for i in range(1,3):
    anims.append([pygame.image.load(f"assets/attacks/{i}/{j}.png") for j in range(1,7)])

class Player(pygame.sprite.Sprite):
    def __init__(self, color, row, col,sheet,type,character):
        super().__init__()
        self.sheet=sheet
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
for conection,charr in get_connections().items():
    players[conection]=Player(*charr)
    all_sprites_group.add(players[conection])

for player,ob in players.items():
    grid[ob.row][ob.col]=player


rock=pygame.image.load(f"assets/Rock Pile.png")
done = False
buttons=[]
inventory = dict()
for i in players[MY_PLAYER].sheet.inventory:
    if i.equipment_category['index'] == "weapon":
        buttons.append(Button(image=None, pos=((WIDTH + MARGIN) * GRID_SIZE + MARGIN + BOARD_MARGIN*1.5,
                            (HEIGHT + MARGIN)), 
                            text_input=i.name, font=get_font(30), base_color="Gray", hovering_color="White"))
        inventory[i.name] = i
buttons.append(Button(image=None, pos=((WIDTH + MARGIN) * GRID_SIZE + MARGIN + 2 * BOARD_MARGIN,
               (HEIGHT + MARGIN) * GRID_SIZE + MARGIN), 
                            text_input="pass turn", font=get_font(30), base_color="Gray", hovering_color="Red"))

clock = pygame.time.Clock()

damage,at_range=(0,-1)
HOST=""
PORT=8080
user_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
user_socket.connect((HOST,PORT))

for t in user_socket.recv(1024).decode("utf-8").split("."):
    n,m=map(int,t.split(","))
    grid[n][m]="obj" if grid[n][m]==" " else grid[n][m]
data = 0 
while not done:
    for i in user_socket.recv(2048).split(b"split"):
        if i!=b"":
            data = json.loads(i)
            print(grid)
            for name,charac in data.items():
                players[name].sheet.current_hp=charac[1]
                players[name].row=charac[0][0]
                players[name].col=charac[0][1]
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for thing in buttons:
                if thing.checkForInput(pos):
                    attacking=False if attacking else True
                    if thing.text_input=="pass turn":
                        exit_flag=True
                    else:
                        damage,at_range = attack((inventory[thing.text_input].damage["damage_dice"],inventory[thing.text_input].range["normal"]))
            
            col = (pos[0] - BOARD_MARGIN) // (WIDTH + MARGIN)
            row = (pos[1]) // (HEIGHT + MARGIN)
            
            
            if get_turn() == MY_PLAYER:
                
                if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                    if grid[row][col] not in {" ", "obj",MY_PLAYER} and attacking == True and ((players[MY_PLAYER].row - at_range-1)<row<(players[MY_PLAYER].row + at_range+1) and (players[MY_PLAYER].col - at_range-1)<col<(players[MY_PLAYER].col + at_range+1)):
                        opponent= grid[row][col]
                        players[opponent].sheet.current_hp=players[opponent].sheet.current_hp-damage
                        attack_animation=(BOARD_MARGIN+col*0.5+col*(HEIGHT+MARGIN),row*0.5+row*(HEIGHT+MARGIN))
                        if players[opponent].sheet.current_hp == 0:
                            players.pop(opponent)
                            grid[row][col] = 20
                        attacking=False
                    else:
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
            if type(grid[row][col]) == int:
                cell_color = RED if grid[row][col]%2==0 else GRAY
                grid[row][col]-=1
                if grid[row][col]==0:
                    grid[row][col] = " "
                
            elif (row, col) == (last_row,last_col):
                cell_color = WHITE
            elif attacking==True and((players[MY_PLAYER].row - at_range-1)<row<(players[MY_PLAYER].row + at_range+1) and (players[MY_PLAYER].col - at_range-1)<col<(players[MY_PLAYER].col + at_range+1)):
                cell_color = RED
            pygame.draw.rect(screen, cell_color, [(MARGIN + WIDTH) * col + MARGIN + BOARD_MARGIN,
                                                  (MARGIN + HEIGHT) * row + MARGIN,
                                                  WIDTH, HEIGHT])
            font = pygame.font.SysFont(None, 30)
            if grid[row][col] =="obj":
                screen.blit(rock, ((MARGIN + WIDTH) * col + MARGIN + BOARD_MARGIN,
                               (MARGIN + HEIGHT) * row + MARGIN))
            elif  grid[row][col] != ' ' and type(grid[row][col])!= int:
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
    if attack_animation!=(None,None):
        counter+=0.5
        screen.blit(anims[pick][int(counter//1)],attack_animation)
        if int(counter//1) >= 2:
            counter=0
            pick=0
            attack_animation=(None,None)
       
    
    pygame.display.flip()

    clock.tick(60)
    sendable_data={name:((obj.row,obj.col),obj.sheet.current_hp)for name,obj in players.items()}
    user_socket.send(json.dumps(sendable_data).encode('utf-8')+b"split")

pygame.quit()
sys.exit()
