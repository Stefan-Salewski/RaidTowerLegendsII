import pygame

from level_generation import level_generation
import menu
from Buttons import Button
from Entity_Classes import Player

# pygame setup
pygame.init()

# window settings
pygame.display.set_caption('Raid Tower Legends II: Mighty Morphin Edition©')
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
start_img = pygame.image.load("start.png").convert_alpha()
quit_img = pygame.image.load("quit.png").convert_alpha()
start_img_hover = pygame.image.load("start_select.png").convert_alpha()
quit_img_hover = pygame.image.load("quit_select.png").convert_alpha()
settings_img = pygame.image.load("settings.png").convert_alpha()
settings_img_hover = pygame.image.load("settings_hover.png").convert_alpha()

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
roomlist = []
offset = pygame.math.Vector2()

# Player initialization
player_entity = Player(SCREEN_WIDTH,SCREEN_HEIGHT) # dimensions are automatically halved in the function

# Load the menu music
pygame.mixer.init()
pygame.mixer.music.load("Menu - Spaceship Hangar.wav")
pygame.mixer.music.play(-1)  # Play the music in a loop

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_state == "menu":

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(colours[1])

        # Function to display menu
        menu.Menu(SCREEN_WIDTH, SCREEN_HEIGHT, clock, colours, screen, fonts)

        start.draw(screen)
        quit.draw(screen)
        pygame.draw.rect(screen, colours[0], settings_white_rect)
        settings.draw(screen)



        if start.function():
            # Stop menu music
            pygame.mixer.music.fadeout(500) # 0.5 seconds of fadeout
            # Load and play game music
            pygame.mixer.music.load("Game - Race Track Chimes.wav") # new music
            pygame.mixer.music.play(-1)  # Play the music in a loop

            # level generation
            roomlist = level_generator.generate_level(10, roomlist, 0, [],[])
            game_state = "playing"

        if quit.function():
            running = False

        if settings.function():
            game_state = "settings"





    elif game_state == "playing":

        screen.fill(colours[1])

        # draw the rooms
        for room in roomlist:
            for wall in room:
                pygame.draw.rect(screen, colours[0], wall)

        fps_counter = REGULAR_FONT.render(str(round(clock.get_fps(), 1)), True, colours[2])
        screen.blit(fps_counter, (0 , 0 ))

        # add player movement and other game logic here
        player_entity.player_movement(screen)

    elif game_state == "settings":

        screen.fill("black")

        settings_screen = menu.Settings(SCREEN_WIDTH, SCREEN_HEIGHT, clock, colours, screen, fonts)
        settings_buttons = settings_screen.settings_buttons(SCREEN_WIDTH, SCREEN_HEIGHT,screen)

        if (settings_buttons == 'menu'): # if the back button is pressed, menu is returned
            game_state = "menu"

        #add more settings buttons later, after camera






    # flip the display to put your work on screen
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
#