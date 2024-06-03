import Buttons
import pygame
class Menu():
    def __init__(self,SCREEN_WIDTH,SCREEN_HEIGHT,clock,colours,screen_instance, fonts):

        # making code for stuff like the title, fps counter, and Version number to show up.
        REGULAR_FONT = fonts[0]
        TITLE_FONT = fonts[1]
        title_display = TITLE_FONT.render("Raid Tower Legends II", True, colours[0])

        screen_instance.blit(title_display, (SCREEN_WIDTH / 2 - title_display.get_width() / 2, 100))

        # debug
        version = REGULAR_FONT.render("0.0.3", True, colours[2])
        screen_instance.blit(version, (SCREEN_WIDTH - version.get_width(), SCREEN_HEIGHT - version.get_height()))

        fps_counter = REGULAR_FONT.render(str(round(clock.get_fps(), 1)), True, colours[2])
        screen_instance.blit(fps_counter, (0, 0))

class Settings(Menu):
    def __init__(self,SCREEN_WIDTH,SCREEN_HEIGHT,clock,colours,screen_instance, fonts):
        # Typical menu stuff like version # and fps.
        # making code for stuff like the title, fps counter, and Version number to show up.
        REGULAR_FONT = fonts[0]
        TITLE_FONT = fonts[1]
        title_display = TITLE_FONT.render("Settings", True, colours[0])

        screen_instance.blit(title_display, (SCREEN_WIDTH / 2 - title_display.get_width() / 2, 100))


        # debug
        version = REGULAR_FONT.render("0.0.3", True, colours[2])
        screen_instance.blit(version, (SCREEN_WIDTH - version.get_width(), SCREEN_HEIGHT - version.get_height()))

        fps_counter = REGULAR_FONT.render(str(round(clock.get_fps(), 1)), True, colours[2])
        screen_instance.blit(fps_counter, (0, 0))

    def settings_buttons(self,SCREEN_WIDTH,SCREEN_HEIGHT,screen):
        # Back to menu button
        back_img = pygame.image.load("Art/back.png").convert_alpha()
        back_img_hover = pygame.image.load("Art/back_hover.png").convert_alpha()
        back = Buttons.Button(SCREEN_WIDTH * 0.09, SCREEN_HEIGHT * 0.09, back_img, back_img_hover, 1)
        back.draw_button(screen)
        # if the back button is pressed, menu is returned
        if (back.function() == True):
            return ("menu")