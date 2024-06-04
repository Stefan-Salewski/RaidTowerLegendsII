import random

import pygame

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

bullet_img = pygame.image.load('Art/bullet.png').convert_alpha()

# initializing buttons outside the loop
start = Button(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.5, start_img, start_img_hover, 0.7)
quit = Button(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.8, quit_img, quit_img_hover,0.7)
settings = Button(SCREEN_WIDTH * 0.95, SCREEN_HEIGHT * 0.05, settings_img,settings_img_hover,0.1)
# Get the dimensions of the settings button image
settings_width = settings_img_hover.get_width() * 0.05 # multiplied by scale
settings_height = settings_img_hover.get_height() * 0.05 # multiplied by scale

# Calculate the white rectangle for the settings button
settings_white_rect = pygame.Rect(0, 0, settings_width - 2, settings_height - 2)
settings_white_rect.center = (SCREEN_WIDTH * 0.95, SCREEN_HEIGHT * 0.05) # same placement as settings button

# game  levels
level_generator = level_generation(pygame, screen, SCREEN_WIDTH, SCREEN_HEIGHT)
room_list = []
offset = pygame.math.Vector2()

bullets = []

temp_enemy = Enemy(100, 10, 5, True, 50,50,50,50)

# Player initialization
player_entity = Player(SCREEN_WIDTH,SCREEN_HEIGHT, bullet_img, bullets)
pygame.mixer.init()
pygame.mixer.music.load("Sound/Music/Menu - Spaceship Hangar.wav")
pygame.mixer.music.set_volume(0)
pygame.mixer.music.play(-1)  # Play the music in a loop

getTicksLastFrame = 0

main_camera = Camera()

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
        pygame.draw.rect(screen, colours[0], settings_white_rect)
        settings.draw_button(screen)


        if start.function():
            # Stop menu music
            pygame.mixer.music.fadeout(500) # 0.5 seconds of fadeout
            # Load and play game music
            pygame.mixer.music.load("Sound/Music/Game - Race Track Chimes.wav") # new music
            pygame.mixer.music.play(-1)  # Play the music in a loop

            # level generation
            room_list = level_generator.generate_level(10, room_list, 0, [], [], random.randint(0, 3))
            #spawn enemies and treasure in rooms
            level_generator.populate_room(room_list)

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
        temp_enemy.enemy_movement(screen, player_entity,main_camera.offset)
        for bullet in bullets:
            bullet.Update(main_camera)
        # draw the rooms
        for room in room_list:
            for wall in room:
                rect_surface = pygame.Surface(wall.get_rect().size, pygame.SRCALPHA)
                rect_surface.fill(colours[0])
                wall_offset = wall.get_rect().topleft - main_camera.offset
                screen.blit(rect_surface, wall_offset)
                for bullet in bullets:
                    collision_offset = (wall.get_rect().x - bullet.rect.x), (wall.get_rect().y - bullet.rect.y)
                    if bullet.mask.overlap(wall.mask, collision_offset):
                        bullets.remove(bullet)
                # collision
                collision_offset = (wall.get_rect().x - player_entity.rect.x), (wall.get_rect().y - player_entity.rect.y)
                if player_entity.mask.overlap(wall.mask, collision_offset):
                    player_entity.rect.topleft = oldPlyerX, oldPlyerY

        #bullets = player_entity.bullets

        #printing player cords for debug

        #temp_enemy_offset = temp_enemy.rect.topleft - main_camera.offset
        #temp_enemy.enemy_movement(screen, player_entity, temp_enemy_offset)
        #setting camera offset
        main_camera.update_camera(player_entity.offset)

        #In game UI drawn last so its on top of everything
        player_cords = REGULAR_FONT.render(str(("X:", player_entity.rect.x, "Y:", player_entity.rect.y)), True,colours[2])
        screen.blit(player_cords, (screen.get_width() - 200, screen.get_height() - 50))
        fps_counter = REGULAR_FONT.render(str(round(clock.get_fps(), 1)), True, colours[2])
        screen.blit(fps_counter, (0 , 0 ))

    # flip the display to put your work on screen
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
