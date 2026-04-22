import pygame

pygame.init()

class Projectil :
    def __init__(self, posX, posY):
        self.posX = posX
        self.posY = posY

        self.speed = 20
        self.rect = pygame.Rect(posX, posY, 10, 10)
        
    def bouger(self) :
        self.rect.x += self.speed

    def show_projectile(self, ecran) :
        pygame.draw.rect(ecran, (255, 0, 0), self.rect)