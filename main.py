import pygame

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


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # RENDER YOUR GAME HERE
    title = my_font.render("Raid Tower Legends II", False, WHITE)

    screen.blit(title, (width/2 - title.get_width()/2, 100))

    #debug
    fps_counter = my_font.render(str(round(clock.get_fps(), 1)), False, WHITE)
    screen.blit(fps_counter, (0, 0))


    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60
    print(clock.get_fps())

pygame.quit()