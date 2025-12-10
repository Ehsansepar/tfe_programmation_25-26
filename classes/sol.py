import pygame
from config import WIDTH, HEIGHT, FPS

class Sol :
    def __init__(self, size, coulor, pos_x=0, pos_y=HEIGHT-100) :
        self.size = size
        self.color = coulor
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = pygame.Rect(pos_x, pos_y, size[0], size[1])