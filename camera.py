import pygame

class Camera():
    def __init__(self):
        self.offset = pygame.math.Vector2()
    def update_camera(self, offset):
        self.offset = offset