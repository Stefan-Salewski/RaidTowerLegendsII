import pygame
import random

#INITIALIZING WINDOW
pygame.init()
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 600

#CREATING DISPLAY,PLAYER, AND FPS COMMANDS
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
player = pygame.Rect((SCREEN_WIDTH/2), (SCREEN_HEIGHT/2), 50, 50)
clock = pygame.time.Clock()
fps = 60

#COLOURS
RED = (255,0,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
RANDOM = ((random.randint(0,255)),(random.randint(0,255)),(random.randint(0,255)))
colours = [WHITE,BLACK,RED,BLUE,GREEN,RANDOM]

# MAIN LOOP
run = True
while run:
    #filling bg and drawing our player
    screen.fill(colours[0])
    pygame.draw.rect(screen,colours[5], player)

    #making sure X'ing the window closes the program
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # two different configurations, wasd or arrow keys
    key = pygame.key.get_pressed()

    speed = pygame.Vector2()

    speed.x = 5
    speed.y = 5
    if key[pygame.K_w] or key[pygame.K_UP]:
        player.move_ip(speed)








    pygame.display.flip()
    clock.tick(fps)


pygame.quit()