import pygame

from level_generation import level_generation
from menu import Menu
from Buttons import Button
from Entity_Classes import Player

# pygame setup
pygame.init()

# window settings
pygame.display.set_caption('Raid Tower Legends II')
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 600
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

# initializing buttons outside the loop
start = Button(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.5, start_img, start_img_hover, 0.7)
quit = Button(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.8, quit_img, quit_img_hover,0.7)

# game  levels
level_generator = level_generation(pygame, screen, SCREEN_WIDTH, SCREEN_HEIGHT)
roomlist = []

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
        Menu(SCREEN_WIDTH, SCREEN_HEIGHT, clock, colours, screen, fonts)

        start.draw(screen)
        quit.draw(screen)


        if start.function():
            # Stop menu music
            pygame.mixer.music.fadeout(3000) # 3 seconds of fadeout
            # Load and play game music
            pygame.mixer.music.load("Game - Race Track Chimes.wav") # new music
            pygame.mixer.music.play(-1)  # Play the music in a loop

            # level generation
            roomlist = level_generator.generate_level(10, roomlist, 0)
            game_state = "playing"

        if quit.function():
            running = False

    elif game_state == "playing":

        screen.fill(colours[1])

        # draw the rooms
        for room in roomlist:
            pygame.draw.rect(screen, colours[0], room)
            fps_counter = REGULAR_FONT.render(str(round(clock.get_fps(), 1)), True, colours[0])
            screen.blit(fps_counter, (0, 0))

        # add player movement and other game logic here
        player_entity.player_movement(screen)

    elif game_state == "settings":

        screen.fill("purple")



    # flip the display to put your work on screen
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
