import pygame
class Button ():
    def __init__ (self,x,y,image,hover_image,scale):
        # locking aspect ratio
        image_width = image.get_width ()
        image_height = image.get_height ()

        image_hover_width = hover_image.get_width ()
        image_hover_height = hover_image.get_height ()
        # creating image scaled to scale
        self.image = pygame.transform.scale (image,
                                             (int (image_width * scale),
                                              int (image_height * scale)))
        self.image_hover = pygame.transform.scale (hover_image,
                                                   (int (image_hover_width * scale),
                                                    int (image_hover_height * scale)))
        # turning image into rect object
        self.rect = self.image.get_rect ()
        # location of rect centre
        self.rect.center = (x,y)
        self.clicked = False

    def draw_button (self, screen_instance):
        # get mouse position
        pos = pygame.mouse.get_pos ()

        # check if mouse is hovering over the button
        if self.rect.collidepoint (pos):
            # draw the hover image
            screen_instance.blit (self.image_hover,
                                  (self.rect.x, self.rect.y))
        else:
            # draw the normal image
            screen_instance.blit (self.image,
                                  (self.rect.x, self.rect.y))

    def function (self):
        # get mouse position
        pos = pygame.mouse.get_pos ()

        # checking if the cursor is colliding with rect obj.
        if (self.rect.collidepoint (pos)):


            # Checking if left click is happening, and  only
            # registering it if it's a new click
            # since we don't want continuous holding of the left
            # click button to count as multiple clicks
            if ( (pygame.mouse.get_pressed () [0] == True) and (self.clicked == False)):
                self.clicked = True
                return True # boolean to compare to, action in the mainloop

            if (pygame.mouse.get_pressed () [0] == False):
                self.clicked = False