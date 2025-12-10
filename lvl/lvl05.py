import pygame
from config import WIDTH, HEIGHT, FPS
from classes.sol import Sol
from classes.personnage import Personnage

class Lvl05:
    def __init__(self, ecran, personnage):
        self.ecran = ecran
        self.personnage = personnage
        self.police = pygame.font.SysFont('Arial', 20, bold=True)
        self.police_titre = pygame.font.SysFont('Arial', 30, bold=True)
        
        # Sol coupé (trou au milieu)
        self.sol = Sol(size=(300, 20), coulor=(193, 120, 90), pos_x=0, pos_y=HEIGHT-100)
        self.finished_rect = pygame.Rect(WIDTH-100, HEIGHT-150, 50, 100)
        
        # Le grand saut
        self.plateformes = [
            pygame.Rect(500, HEIGHT-100, 300, 20),
        ]
        
        # Boutons Menu et Niveaux
        self.rect_menu = pygame.Rect(20, 20, 100, 40)
        self.rect_niveaux = pygame.Rect(WIDTH - 120, 20, 100, 40)
    
    def afficher_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        rect = img.get_rect(center=(x, y))
        self.ecran.blit(img, rect)
    
    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        return "menu"
                    if event.key == pygame.K_l:
                        return "level"
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.rect_menu.collidepoint(event.pos):
                        return "menu"
                    if self.rect_niveaux.collidepoint(event.pos):
                        return "level"
            
            self.personnage.move()
            self.personnage.verifier_platforme(self.plateformes)
            self.ecran.fill((70, 50, 90))
            
            # Hover boutons
            mouse_pos = pygame.mouse.get_pos()
            col_menu = (231, 76, 60)  # Rouge
            col_niveaux = (26, 188, 156)  # Turquoise
            if self.rect_menu.collidepoint(mouse_pos):
                col_menu = (236, 112, 99)
            if self.rect_niveaux.collidepoint(mouse_pos):
                col_niveaux = (72, 201, 176)
            
            # Dessiner boutons
            pygame.draw.rect(self.ecran, col_menu, self.rect_menu, border_radius=10)
            pygame.draw.rect(self.ecran, (255, 255, 255), self.rect_menu, 2, border_radius=10)
            self.afficher_text("MENU", self.police, (255, 255, 255), self.rect_menu.centerx, self.rect_menu.centery)
            
            pygame.draw.rect(self.ecran, col_niveaux, self.rect_niveaux, border_radius=10)
            pygame.draw.rect(self.ecran, (255, 255, 255), self.rect_niveaux, 2, border_radius=10)
            self.afficher_text("LEVELS", self.police, (255, 255, 255), self.rect_niveaux.centerx, self.rect_niveaux.centery)
            
            # Titre
            self.afficher_text("Niveau 5 - Le Grand Saut", self.police_titre, (255, 255, 255), WIDTH // 2, 40)
            
            pygame.draw.rect(self.ecran, self.sol.color, self.sol.rect)
            for plat in self.plateformes:
                pygame.draw.rect(self.ecran, (193, 120, 90), plat)
            pygame.draw.rect(self.ecran, (138, 190, 185), self.finished_rect)
            pygame.draw.rect(self.ecran, self.personnage.color, 
                           (self.personnage.x, self.personnage.y, 
                            self.personnage.width, self.personnage.height))
            
            if self.personnage.x + self.personnage.width > self.finished_rect.x and self.personnage.x < self.finished_rect.x + self.finished_rect.width and self.personnage.y + self.personnage.height > self.finished_rect.y and self.personnage.y < self.finished_rect.y + self.finished_rect.height:
                return "win"
            
            pygame.display.flip()
            clock.tick(FPS)
