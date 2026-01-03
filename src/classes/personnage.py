import pygame
from data.config import WIDTH, HEIGHT


pygame.init()
pygame.mixer.init()


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

        self.son_jump = pygame.mixer.Sound("src/sounds/jump.wav")
        self.son_jump.set_volume(0.5)

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

        if keys[pygame.K_LSHIFT]:
            self.x += self.speed  

        if keys[pygame.K_z]:
            self.jump()
        if keys[pygame.K_q]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed


        self.vitesse_verticale += self.gravite 
        self.y += self.vitesse_verticale
        
        self.player_rect.x = self.x
        self.player_rect.y = self.y
        
        ground_y = HEIGHT - 100 - self.height  # Le sol est à HEIGHT - 100

        if self.y >= ground_y:
            self.y = ground_y
            self.vitesse_verticale = 0
            self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.son_jump.play()
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