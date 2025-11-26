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


        # self.vitesse_verticale = 0 
        # self.gravite = 0.5 # en pixels par frame^2
        # self.puissance_saut = -15 # en pixels par frame
        # self.is_jumping = False

        self.en_saut = False
        self.compteur_saut = 0
        self.taille_saut = 20

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


        # self.vitesse_verticale += self.gravite # Appliquer la gravité a chaque fois il augumente la vitesse verticale
        # self.y += self.vitesse_verticale
        # ground_y = HEIGHT - self.height

        # if self.y >= ground_y:
        #     self.y = ground_y
        #     self.vitesse_verticale = 0
        #     self.is_jumping = False

        if self.en_saut:
            self.y -= 10
            self.compteur_saut += 1

            if self.compteur_saut < 0 :
                self.en_saut = False
        else : 
            self.y += 10
    
        sol = HEIGHT - self.height

        if self.y >= sol :
            self.y = sol

    def jump(self):
        # if not self.is_jumping:
        #     self.vitesse_verticale = self.puissance_saut
        #     self.is_jumping = True

        sol = HEIGHT - self.height

        if self.y >= sol :
            self.en_saut = True
            self.compteur_saut = - self.taille_saut