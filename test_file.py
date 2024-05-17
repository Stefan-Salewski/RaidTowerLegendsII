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

    player_moving = pygame.Vector2()
    player_speed = 5

    if (key[pygame.K_w]) or (key[pygame.K_UP]):
        player_moving.y -= 1
    if (key[pygame.K_s]) or (key[pygame.K_DOWN]):
        player_moving.y += 1
    if (key[pygame.K_a]) or (key[pygame.K_LEFT]):
        player_moving.x -= 1
    if (key[pygame.K_d]) or (key[pygame.K_RIGHT]):
        player_moving.x += 1

    # Use unit vectors to set directions and get consistent speed with diagonal and non-diagonal movement
    if (player_moving.length() > 0) : #if there's movement basically.
        player_moving = player_moving.normalize() * player_speed #multiplying unit vector by speed
    player.move_ip(player_moving.x, player_moving.y) # moving it by whatever the new vectors coordinates are








    pygame.display.flip()
    clock.tick(fps)


pygame.quit()