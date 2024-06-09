import time

import pygame
import random
import camera

#COLOURS
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RANDOM = ((random.randint(0, 255)), (random.randint(0, 255)), (random.randint(0, 255)))
PURPLE = (128, 0, 128)
colours = [WHITE, BLACK, RED, BLUE, GREEN, RANDOM, PURPLE]


class Entity():
    def __init__(self, invulnerability, health, damage, cancollide, game_state):
        #invulnerability should be a true/false toggle, walls should be true for example
        self.invulnerability = invulnerability
        self.max_health = health
        self.health = self.max_health
        self.damage = damage
        self.cancollide = cancollide
        self.game_state = game_state
        self.offset = pygame.math.Vector2()

        print("Entity spawning")
    def Take_Damage(self, damage):
        self.health = self.health - damage
        if self.health <= 0:
            self.game_state = "dead"

    def movement(self, surface, rect, movement_vector, screen_instance, colorfill):
        rect.move_ip(movement_vector[0], movement_vector[1])  # moving it by whatever the new vectors coordinates are
        # setting the camera based on the players position
        # getting half width and height of the window
        half_w = pygame.display.get_window_size()[0] // 2
        half_h = pygame.display.get_window_size()[1] // 2
        # setting the x and y offset

        self.offset.x = rect.centerx - half_w
        self.offset.y = rect.centery - half_h

        # convert rect to a surface and draw to the screen
        if(colorfill):
            surface.fill(colours[5])
        screen_instance.blit(surface, rect.topleft - self.offset)


class Player(Entity):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, bullet_img, bullets, game_state, invulnerability=False, health=100, damage=25,firerate = 1, cancollide=True, ):
        self.bullet_img = bullet_img
        self.bullets = bullets
        self.invulnerability = invulnerability
        self.max_health = health
        self.health = self.max_health
        self.damage = damage
        self.game_state = game_state
        self.offset = pygame.math.Vector2()
        self.cancollide = cancollide
        self.firerate = firerate
        self.firecooldown = self.firerate
        self.rect = pygame.Rect(0, 0, 50, 50)
        self.player_speed = 5
        self.surface = pygame.Surface(self.rect.size)
        self.mask = pygame.mask.from_surface(self.surface)
        self.player_moving = pygame.math.Vector2()
        self.mousepos = pygame.math.Vector2()
        print("Player initialized")
    def player_input(self, screen_instance, deltaTime):
        #pygame.draw.rect(screen_instance, colours[5], self.player)
        self.mousepos = pygame.mouse.get_pos()

        key = pygame.key.get_pressed()
        self.player_moving = pygame.math.Vector2()
        # creating a vector for player movement

        # setting direction of vector based on key inputs, both wasd and arrow keys work
        if (key[pygame.K_w]) or (key[pygame.K_UP]):
            self.player_moving.y -= 1
        if (key[pygame.K_s]) or (key[pygame.K_DOWN]):
            self.player_moving.y += 1
        if (key[pygame.K_a]) or (key[pygame.K_LEFT]):
            self.player_moving.x -= 1
        if (key[pygame.K_d]) or (key[pygame.K_RIGHT]):
            self.player_moving.x += 1
        # Use unit vectors to set directions and get consistent speed with diagonal and non-diagonal movement
        if (self.player_moving.length() > 0):  # if there's movement basically.
            self.player_moving = self.player_moving.normalize() * self.player_speed  # multiplying unit vector by speed

        self.movement(self.surface, self.rect, self.player_moving, screen_instance, True)

        #calculating the world position of the mouse, then getting the direction vector between the mouse and player
        world_mouse_pos = self.mousepos + self.offset
        shoot_dir = world_mouse_pos - self.rect.center
        # drawing a line to test if the direction vector is correct
        pygame.draw.line(screen_instance, colours[5], self.rect.center - self.offset, world_mouse_pos - self.offset)
        #shooting behaviour
        if pygame.mouse.get_pressed()[0] and self.firecooldown <= 0:
              # Normalize and scale by bullet speed
            self.shoot_bullets(shoot_dir, screen_instance, 5, self.damage)
            self.firecooldown = self.firerate

        self.firecooldown -= 1 * deltaTime

    def shoot_bullets(self, movement_vector, screen_instance, speed, damage):
        #normalizing and multiplying by speed to get the right vector
        movement_vector = movement_vector.normalize() * speed
        new_bullet = Bullet(damage, speed, movement_vector, screen_instance, self.bullet_img, self.rect.centerx, self.rect.centery)
        self.bullets.append(new_bullet)

    def power_up(self):
        pass

class Bullet(Entity):
    def __init__(self, damage, speed, movement_vector, screen_instance,image, x, y):
        self.damage = damage
        self.speed = speed
        self.movement_vector = pygame.math.Vector2(movement_vector).normalize() * self.speed  # Normalize and apply speed
        self.position = pygame.math.Vector2(x, y)
        self.screen_instance = screen_instance
        self.offset = pygame.math.Vector2()
        self.sprite = image
        #self.surface = pygame.Surface(self.sprite.get_size())

        image_width = self.sprite.get_width()
        image_height = self.sprite.get_height()
        self.image = pygame.transform.scale(self.sprite, (int(image_width * 1), int(image_height * 1)))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def Update(self, main_camera):
        self.position += self.movement_vector

        # Calculate the screen position based on the camera's position
        screen_x = self.position.x - main_camera.offset[0]
        screen_y = self.position.y - main_camera.offset[1]

        # Update the rect for collision purposes
        self.rect.x = self.position.x
        self.rect.y = self.position.y

        # Draw the bullet at the calculated screen position
        self.screen_instance.blit(self.image, (screen_x, screen_y))

class Enemy(Entity):
    def __init__(self, health, damage, speed, cancollide, x, y, width, height):
        self.invulnerability = True
        self.max_health = health
        self.health = self.max_health
        self.damage = damage
        self.enemy_speed = speed
        self.cancollide = cancollide
        self.x = x
        self.y = y
        self.oldx = 0
        self.oldy = 0
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.surface = pygame.Surface(self.rect.size)
        self.mask = pygame.mask.from_surface(self.surface)
        self.enemy_moving = pygame.math.Vector2()

    def enemy_movement(self, screen_instance, player_ref, camera_offset):
        self.enemy_moving = pygame.math.Vector2(player_ref.rect.centerx - self.rect.centerx, (player_ref.rect.centery) - self.rect.centery)

        # Use unit vectors to set directions and get consistent speed with diagonal and non-diagonal movement
        if(self.enemy_moving.length() <= 1000 and self.enemy_moving.length() > 0):
            self.enemy_moving = self.enemy_moving.normalize() * self.enemy_speed
            self.rect.move_ip(self.enemy_moving.x, self.enemy_moving.y)  # moving it by whatever the new vectors coordinates are

        #convert rect to a surface and draw to the screen
        self.surface.fill(colours[2])
        offset = self.rect.topleft - camera_offset
        screen_instance.blit(self.surface, offset)

        return self.enemy_moving

class Level_End(Entity):
    def __init__(self, x, y, width, height):
        self.invulnerability = True
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.surface = pygame.Surface(self.rect.size)
        self.surface.fill(colours[6])
        self.mask = pygame.mask.from_surface(self.surface)
class Wall(Entity):
    def __init__(self, x, y, width, height):
        self.invulnerability = True
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.surface = pygame.Surface(self.rect.size)
        self.mask = pygame.mask.from_surface(self.surface)

    def get_rect(self):
        return self.rect

    pass
