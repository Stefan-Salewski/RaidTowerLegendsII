import pygame
from menu import menu

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
#COLOURS sdf
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

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    menu(SCREEN_WIDTH,SCREEN_HEIGHT,clock,fps,colours,screen,fonts)

    # flip() the display to put your work on screen

    pygame.display.flip()
    clock.tick(fps)  # limits FPS to fps

pygame.quit()
