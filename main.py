import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
WHITE = (255, 255 , 255)
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

pygame.display.set_caption('Raid Tower Legends II')

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    text_surface = my_font.render(str(round(clock.get_fps(),1)), False, WHITE)
    screen.blit(text_surface, (0, 0))

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60
    print(clock.get_fps())

pygame.quit()