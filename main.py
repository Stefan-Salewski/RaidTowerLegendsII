import pygame

from level_generation import level_generation
from menu import Menu
from Buttons import Button
from Entity_Classes import Entity, Player

# pygame setup
pygame.init()

# window settings
pygame.display.set_caption('Raid Tower Legends II')
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# clock
clock = pygame.time.Clock()
fps = 60
running = True

# colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
colours = [WHITE, BLACK, RED, BLUE, GREEN]

# text
pygame.font.init()
REGULAR_FONT = pygame.font.SysFont('Baskerville', 30)
TITLE_FONT = pygame.font.SysFont("Baskerville", 70)
fonts = [REGULAR_FONT, TITLE_FONT]

# buttons graphics
start_img = pygame.image.load("Start.png").convert_alpha()
quit_img = pygame.image.load("Quit.png").convert_alpha()

# initializing buttons outside the loop
start = Button(SCREEN_WIDTH * 0.2, SCREEN_HEIGHT * 0.8, start_img, 0.9)
quit = Button(SCREEN_WIDTH * 0.8, SCREEN_HEIGHT * 0.8, quit_img, 0.85)

# game
level_generator = level_generation(pygame, screen, SCREEN_WIDTH, SCREEN_HEIGHT)
roomlist = []

# state variable
game_state = "menu"

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_state == "menu":
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")

        # Function to display menu
        Menu(SCREEN_WIDTH, SCREEN_HEIGHT, clock, colours, screen, fonts)

        start.draw(screen)
        quit.draw(screen)

        if start.function():
            # level generation
            roomlist = level_generator.generate_level(10, roomlist, 0)
            game_state = "playing"
        if quit.function():
            running = False

    elif game_state == "playing":
        screen.fill("purple")

        # draw the rooms
        for room in roomlist:
            pygame.draw.rect(screen, colours[0], room)

        # add player movement and other game logic here

    # flip the display to put your work on screen
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
