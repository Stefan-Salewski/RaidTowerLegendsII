# Shadid 19-May-24
# Buttons

import pygame
class Button():
    def __init__(self,x,y,image,scale):
        # locking aspect ratio
        image_width = image.get_width()
        image_height = image.get_height()
        # creating image scaled to scale
        self.image = pygame.transform.scale(image,(int(image_width * scale), int(image_height * scale)))
        # turning image into rect object
        self.rect = image.get_rect()
        # location of rect centre
        self.rect.center = (x,y)
        self.clicked = False
    def draw(self,screen_instance):
        # draw button, centre at x,y
        screen_instance.blit(self.image,(self.rect.x,self.rect.y))
    def function(self):
        # get mouse position
        pos = pygame.mouse.get_pos()

        # checking if the cursor is colliding with rect obj.
        if (self.rect.collidepoint(pos)):
            # Checking if left click is happening, and  only registering it if it's a new click
            # since we don't want continuous holding of the left click button to count as multiple clicks
            if (pygame.mouse.get_pressed()[0] == True) and (self.clicked == False):
                self.clicked = True
                return True # boolean to compare to, action in the mainloop

            if (pygame.mouse.get_pressed()[0] == False):
                self.clicked = False


# buttons graphics
start_img = pygame.image.load("Start.png").convert_alpha()
quit_img = pygame.image.load("Quit.png").convert_alpha()

# initializing buttons outside the loop
start = Buttons.Button(SCREEN_WIDTH * 0.2, SCREEN_HEIGHT * 0.8, start_img, 0.9)
quit = Buttons.Button(SCREEN_WIDTH * 0.8, SCREEN_HEIGHT * 0.8, quit_img, 0.85)

# Make sure buttons do things
        if (start.function()):
            # level generation
            pass
        if (stop.function()):
            run = False