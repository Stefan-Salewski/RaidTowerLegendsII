import random

import pygame

import Entity_Classes
from camera import Camera
from level_generation import level_generation
from menu import Menu
import menu
from Buttons import Button
from Entity_Classes import Player
from Entity_Classes import Wall
from Entity_Classes import Enemy
from Entity_Classes import Bullet

# pygame setup
pygame.init()

# window settings
pygame.display.set_caption('Raid Tower Legends II©')
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# clock
clock = pygame.time.Clock()
fps = 60
running = True
game_state = "menu" # default state is menu

# colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
colours = [WHITE, BLACK, RED, BLUE, GREEN]

# fonts
pygame.font.init()
REGULAR_FONT = pygame.font.Font('Born2bSportyFS.otf', 30)
TITLE_FONT = pygame.font.Font("Born2bSportyFS.otf", 70)
fonts = [REGULAR_FONT, TITLE_FONT]

# buttons graphics
start_img = pygame.image.load("Art/start.png").convert_alpha()
quit_img = pygame.image.load("Art/quit.png").convert_alpha()
start_img_hover = pygame.image.load("Art/start_select.png").convert_alpha()
quit_img_hover = pygame.image.load("Art/quit_select.png").convert_alpha()
settings_img = pygame.image.load("Art/settings.png").convert_alpha()
settings_img_hover = pygame.image.load("Art/settings_hover.png").convert_alpha()
back_img = pygame.image.load("Art/back.png").convert_alpha()
back_img_hover = pygame.image.load("Art/back_hover.png").convert_alpha()

bullet_img = pygame.image.load('Art/bullet.png').convert_alpha()

chest_open = pygame.image.load("Art/chest_open.png").convert_alpha()
chest_closed = pygame.image.load("Art/chest_closed.png").convert_alpha()

# initializing buttons outside the loop
start = Button(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.5, start_img, start_img_hover, 0.7)
quit = Button(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.8, quit_img, quit_img_hover,0.7)
settings = Button(SCREEN_WIDTH * 0.95, SCREEN_HEIGHT * 0.05, settings_img,settings_img_hover,0.1)

back_to_main_menu = Button(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.5, back_img, back_img_hover, 3)
# Get the dimensions of the settings button image
settings_width = settings_img_hover.get_width() * 0.05 # multiplied by scale
settings_height = settings_img_hover.get_height() * 0.05 # multiplied by scale

# Calculate the white rectangle for the settings button
settings_white_rect = pygame.Rect(0, 0, settings_width - 2, settings_height - 2)
settings_white_rect.center = (SCREEN_WIDTH * 0.95, SCREEN_HEIGHT * 0.05) # same placement as settings button

bullets = []
level_end = []
enemies = []
chests = []
powerups = []
# game  levels
level_generator = level_generation(pygame, screen, SCREEN_WIDTH, SCREEN_HEIGHT, chest_open, chest_closed, powerups)
room_list = []
offset = pygame.math.Vector2()



# Player initialization
player_entity = Player(SCREEN_WIDTH,SCREEN_HEIGHT, bullet_img, bullets, game_state)
pygame.mixer.init()
pygame.mixer.music.load("Sound/Music/Menu - Spaceship Hangar.wav")
pygame.mixer.music.set_volume(25)
pygame.mixer.music.play(-1)  # Play the music in a loop

getTicksLastFrame = 0

main_camera = Camera()

def new_level(level):
    player_entity.health = player_entity.max_health
    level_generator.level = level
    room_list.clear()
    enemies.clear()
    chests.clear()
    powerups.clear()
    player_entity.rect.topleft = 0,0
    level_generator.generate_level(10 + level, room_list, 0, [], [], random.randint(0, 3))
    level_generator.populate_room(room_list, enemies, "enemy")
    level_generator.populate_room(room_list, chests, "loot")


while running:
    # getting deltatime for fire rate cooldown
    t = pygame.time.get_ticks()
    deltaTime = (t - getTicksLastFrame) / 1000.0
    getTicksLastFrame = t
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_state == "menu":

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(colours[1])

        # Function to display menu
        Menu(SCREEN_WIDTH, SCREEN_HEIGHT, clock, colours, screen, fonts)

        start.draw_button(screen)
        quit.draw_button(screen)


        if start.function():
            # Stop menu music
            pygame.mixer.music.fadeout(500) # 0.5 seconds of fadeout
            # Load and play game music
            pygame.mixer.music.load("Sound/Music/Game - Race Track Chimes.wav") # new music
            pygame.mixer.music.play(-1)  # Play the music in a loop

            # level generation

            #spawn enemies and treasure in rooms
            new_level(0)
            player_entity.max_health = 100
            player_entity.health = 100
            player_entity.firerate = 1
            player_entity.damage = 25
            player_entity.player_speed = 5
            player_entity.money = 0
            player_entity.amount = 1
            game_state = "playing"

        if quit.function():
            running = False

        if settings.function():
            game_state = "settings"

    elif game_state == "settings":

        screen.fill("black")

        settings_screen = menu.Settings(SCREEN_WIDTH, SCREEN_HEIGHT, clock, colours, screen, fonts)
        settings_buttons = settings_screen.settings_buttons(SCREEN_WIDTH, SCREEN_HEIGHT, screen)

        if (settings_buttons == "menu"):
            game_state = "menu"


    elif game_state == "playing":
        #im normal during the day but at night turn to a sigma
        screen.fill(colours[1])

        # add player movement and other game logic here
        oldPlyerX, oldPlyerY = player_entity.rect.topleft
        player_entity.player_input(screen, deltaTime)
        for enemy in enemies:
            enemy.oldx, enemy.oldy = enemy.rect.topleft

            enemy.enemy_movement(screen, player_entity, main_camera.offset)
            enemy_health = REGULAR_FONT.render(str(enemy.max_health) + "/" + str(enemy.health), True,colours[2])
            text_pos = enemy.rect.center[0] - 50, enemy.rect.center[1] + 50
            screen.blit(enemy_health, text_pos - main_camera.offset)

            # Collision code
            for room in room_list:
                for wall in room:
                    collision_offset = (enemy.rect.x - wall.get_rect().x), (enemy.rect.y - wall.get_rect().y)
                    if wall.mask.overlap(enemy.mask, collision_offset):
                        enemy.rect.topleft = enemy.oldx, enemy.oldy

            bullets_to_remove = []
            enemies_to_remove = []

            for bullet in bullets:
                for enemy in enemies:
                    collision_offset = (enemy.rect.x - bullet.rect.x), (enemy.rect.y - bullet.rect.y)
                    if bullet.mask.overlap(enemy.mask, collision_offset):
                        bullets_to_remove.append(bullet)
                        enemy.Take_Damage(player_entity.damage)
                        if enemy.health <= 0:
                            player_entity.money += 4 + (2 * level_generator.level)
                            enemies_to_remove.append(enemy)

            # Remove the bullets and enemies marked for removal
            for bullet in bullets_to_remove:
                if bullet in bullets:  # Check if the bullet is still in the list
                    bullets.remove(bullet)

            for enemy in enemies_to_remove:
                if enemy in enemies:  # Check if the enemy is still in the list
                    enemies.remove(enemy)

            collision_offset = (enemy.rect.x - player_entity.rect.x), (enemy.rect.y - player_entity.rect.y)
            if player_entity.mask.overlap(enemy.mask, collision_offset):
                player_entity.rect.topleft = oldPlyerX, oldPlyerY
                player_entity.Take_Damage(enemy.damage)
                if player_entity.health <= 0:
                    game_state = "dead"
                enemy.rect.topleft = enemy.oldx,enemy.oldy

        for bullet in bullets:
            bullet.Update(main_camera)
        # draw the rooms
        for room in room_list:
            for wall in room:
                rect_surface = pygame.Surface(wall.get_rect().size, pygame.SRCALPHA)
                rect_surface.fill(colours[0])
                wall_offset = wall.get_rect().topleft - main_camera.offset
                screen.blit(rect_surface, wall_offset)

                #Collision code
                for bullet in bullets:
                    collision_offset = (wall.get_rect().x - bullet.rect.x), (wall.get_rect().y - bullet.rect.y)
                    if bullet.mask.overlap(wall.mask, collision_offset):
                        bullets.remove(bullet)

                collision_offset = (wall.get_rect().x - player_entity.rect.x), (wall.get_rect().y - player_entity.rect.y)
                if player_entity.mask.overlap(wall.mask, collision_offset):
                    player_entity.rect.topleft = oldPlyerX, oldPlyerY
        for chest in chests:
            chest_offset = chest.rect.topleft - main_camera.offset
            screen.blit(chest.image, chest_offset)
            chest_cost = REGULAR_FONT.render("$" + str(chest.cost), True,colours[0])
            screen.blit(chest_cost,pygame.math.Vector2(chest.rect.centerx - main_camera.offset.x - chest_cost.get_width()/2,chest.rect.centery - main_camera.offset.y) )
            collision_offset = (chest.rect.x - player_entity.rect.x), (chest.rect.y - player_entity.rect.y)
            if player_entity.mask.overlap(chest.mask, collision_offset) and player_entity.money >= chest.cost and chest.opened == False:
                chest.open_chest()
                player_entity.money -= chest.cost

        for powerup in powerups:
            powerup_offset = powerup.rect.topleft - main_camera.offset
            screen.blit(powerup.image, powerup_offset)
            collision_offset = (powerup.rect.x - player_entity.rect.x), (powerup.rect.y - player_entity.rect.y)
            if player_entity.mask.overlap(powerup.mask,collision_offset):
                powerup.power_up(player_entity)
                powerups.remove(powerup)

        # end level
        collision_offset = (level_generator.exit.rect.x - player_entity.rect.x), (level_generator.exit.rect.y - player_entity.rect.y)
        if player_entity.mask.overlap(level_generator.exit.mask, collision_offset):
            level_generator.level += 1
            new_level(level_generator.level)

        #setting camera offset
        main_camera.update_camera(player_entity.offset)

        #In game UI drawn last so its on top of everything
        fps_counter = REGULAR_FONT.render(str(round(clock.get_fps(), 1)), True, colours[2])
        screen.blit(fps_counter, (0 , 0 ))
        level_counter = REGULAR_FONT.render("Level " + str(level_generator.level), True, colours[4])
        screen.blit(level_counter, ((screen.get_width() /2) - level_counter.get_width() / 2, screen.get_height()- 1000))

        health_test = REGULAR_FONT.render(str(player_entity.max_health) + "/" + str(player_entity.health), True, colours[4])
        screen.blit(health_test,((screen.get_width() / 2) - level_counter.get_width() / 2, screen.get_height() / 1.75))

        money = REGULAR_FONT.render("$" + str(player_entity.money), True, colours[4])
        screen.blit(money, ((screen.get_width() / 12) - money.get_width() / 2, screen.get_height() / 1.1))

        screen.blit(level_generator.exit.surface, level_generator.exit.rect.topleft - main_camera.offset)

    elif game_state == "dead":
        screen.fill(colours[1])
        level_counter = REGULAR_FONT.render("You died on level " + str(level_generator.level), True, colours[4])
        screen.blit(level_counter,((screen.get_width() / 2) - level_counter.get_width() / 2, screen.get_height() - 1000))
        back_to_main_menu.draw_button(screen)
        if back_to_main_menu.function() == True:
            game_state = "menu"
    # flip the display to put your work on screen
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()