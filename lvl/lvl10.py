import pygame
from config import WIDTH, HEIGHT, FPS
from classes.sol import Sol
from classes.personnage import Personnage

class Lvl10:
    def __init__(self, ecran, personnage):
        self.ecran = ecran
        self.personnage = personnage
        self.police = pygame.font.SysFont('Arial', 20, bold=True)
        self.police_titre = pygame.font.SysFont('comicsansms', 40, bold=True)
        
        self.sol = Sol(size=(80, 20), coulor=(255, 100, 100), pos_x=0, pos_y=HEIGHT-100)
        self.finished_rect = pygame.Rect(WIDTH//2 - 25, 50, 50, 100)
        
        # FINAL LEVEL
        self.plateformes = [
            pygame.Rect(100, 650, 50, 20),
            pygame.Rect(200, 580, 50, 20),
            pygame.Rect(100, 510, 50, 20),
            pygame.Rect(200, 440, 50, 20),
            pygame.Rect(300, 370, 50, 20),
            pygame.Rect(400, 300, 50, 20),
            pygame.Rect(500, 230, 50, 20),
            pygame.Rect(350, 160, 200, 20),
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
            self.ecran.fill((50, 20, 60))
            
            # Hover boutons
            mouse_pos = pygame.mouse.get_pos()
            col_menu = (255, 215, 0)  # Or
            col_niveaux = (192, 57, 43)  # Rouge foncé
            if self.rect_menu.collidepoint(mouse_pos):
                col_menu = (255, 235, 100)
            if self.rect_niveaux.collidepoint(mouse_pos):
                col_niveaux = (217, 136, 128)
            
            # Dessiner boutons
            pygame.draw.rect(self.ecran, col_menu, self.rect_menu, border_radius=10)
            pygame.draw.rect(self.ecran, (255, 255, 255), self.rect_menu, 2, border_radius=10)
            self.afficher_text("MENU", self.police, (50, 50, 50), self.rect_menu.centerx, self.rect_menu.centery)
            
            pygame.draw.rect(self.ecran, col_niveaux, self.rect_niveaux, border_radius=10)
            pygame.draw.rect(self.ecran, (255, 255, 255), self.rect_niveaux, 2, border_radius=10)
            self.afficher_text("LEVELS", self.police, (255, 255, 255), self.rect_niveaux.centerx, self.rect_niveaux.centery)
            
            pygame.draw.rect(self.ecran, self.sol.color, self.sol.rect)
            for plat in self.plateformes:
                pygame.draw.rect(self.ecran, (139, 90, 43), plat)
            
            # Zone d'arrivée dorée pour le niveau final
            pygame.draw.rect(self.ecran, (255, 215, 0), self.finished_rect)
            pygame.draw.rect(self.ecran, (255, 255, 255), self.finished_rect, 3)
            
            pygame.draw.rect(self.ecran, self.personnage.color, 
                           (self.personnage.x, self.personnage.y, 
                            self.personnage.width, self.personnage.height))
            
            # Titre au centre
            self.afficher_text("🔥 NIVEAU FINAL 🔥", self.police_titre, (255, 215, 0), WIDTH // 2, 40)
            
            if self.personnage.x + self.personnage.width > self.finished_rect.x and self.personnage.x < self.finished_rect.x + self.finished_rect.width and self.personnage.y + self.personnage.height > self.finished_rect.y and self.personnage.y < self.finished_rect.y + self.finished_rect.height:
                return "win"
            
            pygame.display.flip()
            clock.tick(FPS)
