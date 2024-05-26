import pygame
import random
import camera

#COLOURS
RED = (255,0,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
RANDOM = ((random.randint(0,255)),(random.randint(0,255)),(random.randint(0,255)))
colours = [WHITE,BLACK,RED,BLUE,GREEN,RANDOM]

class Entity():
    def __init__(self,invulnerability,health,damage,cancolide):
        self.invulnerability = invulnerability
        self.health = health
        self.damage = damage
        self.cancollide = cancolide
        print("Entity spawning")

class Player(Entity):
    def __init__(self,SCREEN_WIDTH,SCREEN_HEIGHT,invulnerability = False, health = 100, damage = 0, cancollide = True):
        self.invulnerability = invulnerability
        self.health = health
        self.damage = damage
        self.offset = pygame.math.Vector2()
        self.cancollide = cancollide
        self.player = pygame.Rect((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2), 50, 50)
        self.player_speed = 5
        print("Player initialized")

    def player_movement(self,screen_instance):
        pygame.draw.rect(screen_instance, colours[5], self.player)

        key = pygame.key.get_pressed()

        player_moving = pygame.math.Vector2()  # creating a vector for player movement

        # setting direction of vector based on key inputs, both wasd and arrow keys work
        if (key[pygame.K_w]) or (key[pygame.K_UP]):
            player_moving.y -= 1
        if (key[pygame.K_s]) or (key[pygame.K_DOWN]):
            player_moving.y += 1
        if (key[pygame.K_a]) or (key[pygame.K_LEFT]):
            player_moving.x -= 1
        if (key[pygame.K_d]) or (key[pygame.K_RIGHT]):
            player_moving.x += 1
        # Use unit vectors to set directions and get consistent speed with diagonal and non-diagonal movement
        if (player_moving.length() > 0):  # if there's movement basically.
            player_moving = player_moving.normalize() * self.player_speed  # multiplying unit vector by speed

            #self.offset = (-1 * (player_moving.normalize() * self.player_speed)) # making sure camera follows

        self.player.move_ip(player_moving.x, player_moving.y)  # moving it by whatever the new vectors coordinates are

        # Making sure our player stays in screen, might remove later, also different ways of doing this.
        self.player.clamp_ip(screen_instance.get_rect())

        # setting the camera based on the players position
        # getting half width and height of the window
        self.half_w = pygame.display.get_window_size()[0] // 2
        self.half_h = pygame.display.get_window_size()[1] // 2
        # setting the x and y offset
        self.offset.x = self.player.centerx - self.half_w
        self.offset.y = self.player.centery - self.half_h
    def shoot_bullets(self):
        pass # coming soon
    def power_up(self):
        pass # coming soon



class Bullet(Entity):
    pass
class Enemy(Entity):
    pass
class Wall(Entity):
    def __init__(self,x,y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.create_rect()
    def create_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return self.rect

    def get_rect(self):
        return self.rect
    pass

