import pygame

print("Hello")

WHITE = (255, 255 , 255)

#text
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
my_font_pos = (0,5)

# RENDER YOUR GAME HERE
title = my_font.render("Raid Tower Legends II", False, WHITE)

#screen.blit(title, (width / 2 - title.get_width() / 2, 100))

    # debug
version = my_font.render("0.0.1", False, WHITE)
#screen.blit(version, (width - version.get_width(), height - version.get_height()))

fps_counter = my_font.render(str(round(clock.get_fps(), 1)), False, WHITE)
#screen.blit(fps_counter, (0, 0))