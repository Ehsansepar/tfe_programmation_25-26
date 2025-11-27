import pygame
import os
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
        self.gravite = 0.8  # Gravité améliorée
        self.puissance_saut = -15
        self.is_jumping = False

        # Direction du personnage (True = droite, False = gauche)
        self.vers_droite = True
        
        # État du personnage pour l'animation
        self.etat = "idle"  # idle, run, jump, fall
        
        # Animation
        self.sprites = {}
        self.charger_sprites()
        self.animation_index = 0
        self.animation_speed = 0.2

    def charger_sprites(self):
        """Charge tous les sprites animés du Ninja Frog"""
        chemin = "assets/images/Main Characters/Ninja Frog"
        
        animations = {
            "idle": "Idle (32x32).png",
            "run": "Run (32x32).png",
            "jump": "Jump (32x32).png",
            "fall": "Fall (32x32).png"
        }
        
        for nom, fichier in animations.items():
            chemin_complet = os.path.join(chemin, fichier)
            if os.path.exists(chemin_complet):
                sprite_sheet = pygame.image.load(chemin_complet).convert_alpha()
                self.sprites[nom] = self.decouper_sprite_sheet(sprite_sheet, 32, 32)
    
    def decouper_sprite_sheet(self, sprite_sheet, largeur, hauteur):
        """Découpe un sprite sheet en frames individuelles"""
        frames = []
        sheet_width = sprite_sheet.get_width()
        nb_frames = sheet_width // largeur
        
        for i in range(nb_frames):
            frame = sprite_sheet.subsurface((i * largeur, 0, largeur, hauteur))
            frame = pygame.transform.scale(frame, (self.width, self.height))
            frames.append(frame)
        
        return frames

    def move(self):
        keys = pygame.key.get_pressed()
        
        moving = False
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.vers_droite = False
            moving = True
            
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.vers_droite = True
            moving = True
            
        if keys[pygame.K_SPACE]:
            self.jump()

        # Gravité
        self.vitesse_verticale += self.gravite
        self.y += self.vitesse_verticale
        
        # Le sol est à HEIGHT - 50, donc le personnage s'arrête à HEIGHT - 50 - height
        ground_y = HEIGHT - 50 - self.height

        if self.y >= ground_y:
            self.y = ground_y
            self.vitesse_verticale = 0
            self.is_jumping = False
        
        # Déterminer l'état pour l'animation
        if self.vitesse_verticale < 0:
            self.etat = "jump"
        elif self.vitesse_verticale > 1:
            self.etat = "fall"
        elif moving:
            self.etat = "run"
        else:
            self.etat = "idle"
        
        # Limiter le personnage à l'écran
        if self.x < 0:
            self.x = 0
        if self.x > WIDTH - self.width:
            self.x = WIDTH - self.width

    def jump(self):
        if not self.is_jumping:
            self.vitesse_verticale = self.puissance_saut
            self.is_jumping = True

    def get_sprite(self):
        """Retourne le sprite actuel à afficher"""
        if self.etat in self.sprites and len(self.sprites[self.etat]) > 0:
            # Avancer l'animation
            self.animation_index += self.animation_speed
            if self.animation_index >= len(self.sprites[self.etat]):
                self.animation_index = 0
            
            sprite = self.sprites[self.etat][int(self.animation_index)]
            
            # Retourner le sprite si le personnage va à gauche
            if not self.vers_droite:
                sprite = pygame.transform.flip(sprite, True, False)
            
            return sprite
        return None

    def afficher(self, ecran):
        sprite = self.get_sprite()
        if sprite:
            ecran.blit(sprite, (self.x, self.y))
        else:
            # Fallback: dessiner un rectangle
            pygame.draw.rect(ecran, self.color, (self.x, self.y, self.width, self.height))
