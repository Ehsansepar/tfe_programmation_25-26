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

        self.player_rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            # self.y -= self.speed
            self.jump()
        if keys[pygame.K_DOWN]:
            self.y += self.speed
        if keys[pygame.K_SPACE]:
            self.jump()


        self.vitesse_verticale += self.gravite # Appliquer la gravité a chaque fois il augumente la vitesse verticale
        self.y += self.vitesse_verticale
        
        # mettre à jour player_rect avec la nouvelle position !
        self.player_rect.x = self.x
        self.player_rect.y = self.y
        
        ground_y = HEIGHT - 100 - self.height  # Le sol est à HEIGHT - 100

        if self.y >= ground_y:
            self.y = ground_y
            self.vitesse_verticale = 0
            self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.vitesse_verticale = self.puissance_saut
            self.is_jumping = True

    def mettre_a_pos_initiale(self):
        self.x = 100
        self.y = 300
        self.speed = 5
        self.vitesse_verticale = 0
        self.is_jumping = False

    def verifier_platforme(self, plateformes):
        for plat in plateformes:
            if self.player_rect.colliderect(plat):
                if self.vitesse_verticale > 0:
                    self.y = plat.y - self.height
                    self.vitesse_verticale = 0
                    self.is_jumping = False
                    self.player_rect.y = self.y