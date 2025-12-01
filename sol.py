import pygame
from config import WIDTH, HEIGHT, FPS

class Sol :
    def __init__(self) :
        self.rect = pygame.Rect(0, HEIGHT-100, WIDTH, 20)

    def afficher(self, ecran) :
        ecran.blit(self.rect)