import pygame
from config import WIDTH, HEIGHT, FPS

class Sol :
    def __init__(self) :
        self.rect = pygame.Rect(0,500, WIDTH, 50)

    def afficher(self, ecran) :
        pygame.draw.rect(ecran, (100, 50, 0), self.rect)