import pygame
import menu

# pygame setup
pygame.init()

#window settings
pygame.display.set_caption('Raid Tower Legends II')
width = 1280
height = 720
screen = pygame.display.set_mode((width, height))

#clock
clock = pygame.time.Clock()
running = True

#colors
WHITE = (255, 255 , 255)

#text
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

main_menu = menu

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

    clock.tick(240)  # limits FPS to 60

pygame.quit()

