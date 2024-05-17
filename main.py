import pygame
#import menu

# pygame setup
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
my_font = pygame.font.SysFont('Comic Sans MS', 30)

def menu(clock,colours,screen):
    # RENDER YOUR GAME HERE
    title = my_font.render("Raid Tower Legends II", False, colours[0])

    screen.blit(title, (SCREEN_WIDTH / 2 - title.get_width() / 2, 100))

    # debug
    version = my_font.render("0.0.1", False, colours[0])
    screen.blit(version, (SCREEN_WIDTH - version.get_width(), SCREEN_HEIGHT - version.get_height()))

    fps_counter = my_font.render(str(round(clock.get_fps(), 1)), False, colours[0])
    screen.blit(fps_counter, (0, 0))

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    menu()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(fps)  # limits FPS to fps

pygame.quit()

