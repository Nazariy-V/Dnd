import pygame
import sys

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRAY = (192, 192, 192)

# Set the width and height of each grid cell
WIDTH = 50
HEIGHT = 50

# Set the margin between each cell
MARGIN = 5

# Set the size of the grid
GRID_SIZE = 10

# Add space around the board
BOARD_MARGIN = 50

START_ROW=0
START_COL=0

# Initialize the grid with empty spaces
grid = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Set the initial position of the player
player_row = START_ROW
player_col = START_COL
last_row = None
last_col = None
grid[player_row][player_col] = 'P'

# List to store visited cells
visited_cell = (None,None)

# Initialize Pygame
pygame.init()

# Set the width and height of the screen [width, height]
WINDOW_SIZE = [(WIDTH + MARGIN) * GRID_SIZE + MARGIN + 2 * BOARD_MARGIN,
               (HEIGHT + MARGIN) * GRID_SIZE + MARGIN + 2 * BOARD_MARGIN]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set the title of the window
pygame.display.set_caption("Grid Movement")

# Define the player class
class Player(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

# Create the player
player = Player(GREEN, WIDTH, HEIGHT)

# Create a group to hold the sprites
all_sprites_group = pygame.sprite.Group()
all_sprites_group.add(player)

# Loop until the user clicks the close button
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse position
            pos = pygame.mouse.get_pos()

            # Change the x/y screen coordinates to grid coordinates
            col = (pos[0] - BOARD_MARGIN) // (WIDTH + MARGIN)
            row = (pos[1] - BOARD_MARGIN) // (HEIGHT + MARGIN)

            # Move the player to the clicked position if it's within the grid
            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                if last_row==row and last_col==col:
                    grid[player_row][player_col] = ' '
                    player_row = row
                    player_col = col
                    grid[player_row][player_col] = 'P'
                    last_col=None
                    last_row=None
                else:
                    
                    last_row=row
                    last_col=col
    # --- Drawing code should go here

    # First, clear the screen to white.
    screen.fill(WHITE)

    # Draw the grid
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            cell_color = BLACK
            if (row, col) == (last_row,last_col):
                cell_color = GRAY
            pygame.draw.rect(screen, cell_color, [(MARGIN + WIDTH) * col + MARGIN + BOARD_MARGIN,
                                                  (MARGIN + HEIGHT) * row + MARGIN + BOARD_MARGIN,
                                                  WIDTH, HEIGHT])
            font = pygame.font.SysFont(None, 30)
            text = font.render(grid[row][col], True, GREEN)
            screen.blit(text, ((MARGIN + WIDTH) * col + MARGIN + 10 + BOARD_MARGIN,
                               (MARGIN + HEIGHT) * row + MARGIN + 10 + BOARD_MARGIN))

    # Draw the path between the last two visited cells
    if last_col!=None and last_row!=None:
        current_cell = (player_row, player_col)
        next_cell = (last_row,last_col)
        pygame.draw.line(screen, GREEN, [(MARGIN + WIDTH) * current_cell[1] + MARGIN + WIDTH // 2 + BOARD_MARGIN,
                                         (MARGIN + HEIGHT) * current_cell[0] + MARGIN + HEIGHT // 2 + BOARD_MARGIN],
                         [(MARGIN + WIDTH) * next_cell[1] + MARGIN + WIDTH // 2 + BOARD_MARGIN,
                          (MARGIN + HEIGHT) * next_cell[0] + MARGIN + HEIGHT // 2 + BOARD_MARGIN], 5)

    # Draw all the sprites
    all_sprites_group.draw(screen)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()
sys.exit()
