import pygame
import data.config as config
from data.config import PLAYER_SPEED, PLAYER_GRAVITY, PLAYER_JUMP


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
        self.gravite = PLAYER_GRAVITY  # Automatique par rapport Windows/Mac
        self.puissance_saut = PLAYER_JUMP  # Automatique par rapport Windows/Mac
        self.is_jumping = False

        self.player_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.son_jump = pygame.mixer.Sound("src/sounds/jump.wav")
        self.son_jump.set_volume(0.5)

        try :
            sprite_sheet = pygame.image.load("src/assets_img/Main Characters/Ninja Frog/Idle (32x32).png").convert_alpha()
            # L'image est une "spritesheet" (plusieurs images collées). On découpe juste la 1ère (32x32 pixels)
            rect_image = pygame.Rect(0, 0, 32, 32)
            self.image = sprite_sheet.subsurface(rect_image)
            # Puis on la redimensionne à la taille de ton personnage
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        except FileNotFoundError:
            print("Image personnage non trouvée")
            self.image = None
        
    def draw(self, ecran):
        if self.image is not None:
            ecran.blit(self.image, (self.x, self.y))
        else :
            pygame.draw.rect(ecran, self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        keys = pygame.key.get_pressed()
        
        # enfaite ici on prends les touches et puis on le transforme en chiffre comme ca pygame comprends ce qu on a fait
        touche_gauche = pygame.key.key_code(config.gauche)  # en gros la ce que user envoie on le change direct en chiffre qui pygame les comprend direct 
        touche_droite = pygame.key.key_code(config.droite)
        touche_haut = pygame.key.key_code(config.haut)
        touche_bas = pygame.key.key_code(config.bas)
        touche_saut = pygame.key.key_code(config.saut)
        
        if keys[touche_gauche]: 
            self.x -= self.speed
        
        if keys[touche_droite]:
            self.x += self.speed
        
        if keys[touche_haut]:
            self.jump()
        
        if keys[touche_bas]:
            self.y += self.speed
        
        if keys[touche_saut]:
            self.jump()
        

        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.jump()
        if keys[pygame.K_DOWN]:
            self.y += self.speed
        
        if keys[pygame.K_LSHIFT]:
            self.x += self.speed


        self.vitesse_verticale += self.gravite 
        self.y += self.vitesse_verticale
        
        self.player_rect.x = self.x
        self.player_rect.y = self.y
        
        ground_y = config.HEIGHT - 100 - self.height  # Le sol est à config.HEIGHT - 100 (dynamique)

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
        self.speed = PLAYER_SPEED 
        self.vitesse_verticale = 0
        self.is_jumping = False

    def verifier_platforme(self, plateformes):
        for plat in plateformes:
            if self.player_rect.colliderect(plat):
                
                # 1. Si on tombe (on atterrit SUR la plateforme)
                if self.vitesse_verticale > 0:
                    self.y = plat.y - self.height
                    self.vitesse_verticale = 0
                    self.is_jumping = False
                
                # 2. Si on saute (on tape la tête EN DESSOUS de la plateforme)
                elif self.vitesse_verticale < 0:
                    self.y = plat.y + plat.height
                    self.vitesse_verticale = 0
                
                self.player_rect.y = self.y