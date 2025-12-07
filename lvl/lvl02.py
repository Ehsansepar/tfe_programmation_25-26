import pygame
from config import WIDTH, HEIGHT, FPS
from sol import Sol

class Lvl02:
    def __init__(self, ecran, personnage):
        self.ecran = ecran
        self.personnage = personnage
        self.police = pygame.font.SysFont('Arial', 30)
        
        # Sol
        self.sol = Sol(size=(WIDTH, 20), coulor=(193, 120, 90), pos_x=0, pos_y=HEIGHT-100)
        
        # Zone d'arrivée
        self.finished_rect = pygame.Rect(WIDTH-100, HEIGHT-150, 50, 100)
        
        # Plateformes du niveau 2
        self.plateformes = [
            pygame.Rect(300, 500, 200, 20),
        ]
    
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
            
            # Mouvement
            self.personnage.move()
            
            # Affichage
            self.ecran.fill((40, 30, 60))
            
            # Sol
            pygame.draw.rect(self.ecran, self.sol.color, self.sol.rect)
            
            # Plateformes
            for plat in self.plateformes:
                pygame.draw.rect(self.ecran, (139, 90, 43), plat)
            
            # Zone d'arrivée
            pygame.draw.rect(self.ecran, (138, 190, 185), self.finished_rect)
            
            # Personnage
            pygame.draw.rect(self.ecran, self.personnage.color, 
                           (self.personnage.x, self.personnage.y, 
                            self.personnage.width, self.personnage.height))
            
            # Texte
            self.afficher_text("Niveau 2", self.police, (255, 255, 255), WIDTH // 2, 30)
            self.afficher_text("M = Menu | L = Niveaux", pygame.font.SysFont('Arial', 20), (200, 200, 200), WIDTH // 2, HEIGHT - 30)
            
            # Vérifier victoire
            if self.personnage.x + self.personnage.width > self.finished_rect.x and self.personnage.x < self.finished_rect.x + self.finished_rect.width and self.personnage.y + self.personnage.height > self.finished_rect.y and self.personnage.y < self.finished_rect.y + self.finished_rect.height:
                return "win"
            
            pygame.display.flip()
            clock.tick(FPS)
