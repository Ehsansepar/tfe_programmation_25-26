import pygame
from config import WIDTH, HEIGHT
class Personnage:
    def __init__(self, x, y, width, height, color, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed


        self.vitesse_verticale = 0 
        self.gravite = 0.5 # en pixels par frame^2
        self.puissance_saut = -15 # en pixels par frame
        self.is_jumping = False


    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed
        if keys[pygame.K_SPACE]:
            self.jump()


        self.vitesse_verticale += self.gravite # Appliquer la gravité a chaque fois il augumente la vitesse verticale
        self.y += self.vitesse_verticale
        ground_y = HEIGHT - 100 - self.height  # Le sol est à HEIGHT - 100

        if self.y >= ground_y:
            self.y = ground_y
            self.vitesse_verticale = 0
            self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.vitesse_verticale = self.puissance_saut
            self.is_jumping = True
