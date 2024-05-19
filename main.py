import pygame

from level_generation import level_generation
from menu import Menu
from Entity_Classes import Entity,Player

#pygame setup
pygame.init()

#window settings
pygame.display.set_caption('Raid Tower Legends II')
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#clock
clock = pygame.time.Clock()
fps = 60
running = True

#colors
#COLOURS
RED = (255,0,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
colours = [WHITE,BLACK,RED,BLUE,GREEN]

#text
pygame.font.init()
REGULAR_FONT = pygame.font.SysFont('Baskerville', 30)
TITLE_FONT = pygame.font.SysFont("Baskerville", 70)
fonts = [REGULAR_FONT, TITLE_FONT]

#game
level_generator = level_generation(pygame, screen, SCREEN_WIDTH, SCREEN_HEIGHT)
roomlist = []

#debug below
roomlist = level_generator.generate_level(10, roomlist, 0)

# Player initialization, move this to menu so that it only happens at start of game
# player_entity = Player(SCREEN_WIDTH,SCREEN_HEIGHT)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    #draw some rooms

    for i in range(len(roomlist)):
        pygame.draw.rect(screen, WHITE, roomlist[i])

    # Function to display menu
    Menu(SCREEN_WIDTH,SCREEN_HEIGHT,clock,colours,screen,fonts)

    # function to move the player, it works, but deactivated for now
    # player_entity.player_movement(screen)

    # flip() the display to put your work on screen

    pygame.display.flip()
    clock.tick(fps)  # limits FPS to fps

pygame.quit()
