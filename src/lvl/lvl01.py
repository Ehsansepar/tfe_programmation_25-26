import pygame
from data.config import WIDTH, HEIGHT, FPS
from classes.sol import Sol
from classes.personnage import Personnage
import data.config as config

class Lvl01:
    def __init__(self, ecran, personnage):
        self.ecran = ecran
        self.personnage = personnage
        self.police = pygame.font.SysFont('Arial', 20, bold=True)
        self.police_titre = pygame.font.SysFont('Arial', 30, bold=True)

        self.sol = Sol(size=(3000, 20), coulor=(193, 120, 90), pos_x=0, pos_y=HEIGHT-100)

        self.finished_rect = pygame.Rect(3000-100, HEIGHT-150, 50, 100)
        
        self.decalage = 0

        self.plateformes = [
            pygame.Rect(300, 500, 200, 20),
            pygame.Rect(700, 450, 200, 20),
            pygame.Rect(1100, 400, 200, 20),
            pygame.Rect(1500, 350, 200, 20),
            pygame.Rect(1900, 300, 200, 20),
        ]

    def afficher_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        rect = img.get_rect(center=(x, y))
        self.ecran.blit(img, rect)

    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            dt = clock.tick(FPS) / 1000.0  # delta time en secondes

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        return "menu"
                    if event.key == pygame.K_l:
                        return "level"

            self.personnage.move(dt)

            self.personnage.verifier_platforme(self.plateformes)

            # Système de caméra (scrolling)
            self.milieu_ecran = WIDTH // 2
            self.decalage = 0

            if self.personnage.x > self.milieu_ecran:
                self.decalage = self.personnage.x - self.milieu_ecran
                self.personnage.x = self.milieu_ecran
                # Déplacer tout le décor vers la gauche
                self.sol.rect.x -= self.decalage
                for plat in self.plateformes:
                    plat.x -= self.decalage
                self.finished_rect.x -= self.decalage

            self.ecran.fill((30, 30, 50))
            
            self.afficher_text("Niveau 1", self.police_titre, (255, 255, 255), WIDTH // 2, 40)

            pygame.draw.rect(self.ecran, self.sol.color, self.sol.rect)
            
            for plateforme in self.plateformes:
                pygame.draw.rect(self.ecran, (100, 100, 100), plateforme)

            pygame.draw.rect(self.ecran, (138, 190, 185), self.finished_rect)
            
            pygame.draw.rect(self.ecran, self.personnage.color, 
                           (int(self.personnage.x), int(self.personnage.y), 
                            self.personnage.width, self.personnage.height))
            
            personnage_rect = pygame.Rect(int(self.personnage.x), int(self.personnage.y), 
                                         self.personnage.width, self.personnage.height)
            if personnage_rect.colliderect(self.finished_rect):
                return "win"
            
            pygame.display.flip()
