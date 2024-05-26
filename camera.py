import pygame

class Camera():
    def __init__(self):
        self.offset = pygame.math.Vector2()

    #update camera takes a pygame.math.Vector2(x,y)
    #offsets by the x and y provided
    def update_camera(self, offset):
        self.offset = offset