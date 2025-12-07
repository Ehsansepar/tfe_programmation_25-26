import pygame
from config import WIDTH, HEIGHT, FPS
from sol import Sol

class Lvl07:
    def __init__(self, ecran, personnage):
        self.ecran = ecran
        self.personnage = personnage
        self.police = pygame.font.SysFont('Arial', 30)
        
        self.sol = Sol(size=(WIDTH, 20), coulor=(193, 120, 90), pos_x=0, pos_y=HEIGHT-100)
        self.finished_rect = pygame.Rect(50, 50, 50, 100)
        
        # Labyrinthe vertical
        self.plateformes = [
            pygame.Rect(0, 550, 600, 20),
            pygame.Rect(200, 450, 600, 20),
            pygame.Rect(0, 350, 600, 20),
            pygame.Rect(200, 250, 600, 20),
            pygame.Rect(0, 150, 600, 20),
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
            
            self.personnage.move()
            self.ecran.fill((90, 70, 110))
            
            pygame.draw.rect(self.ecran, self.sol.color, self.sol.rect)
            for plat in self.plateformes:
                pygame.draw.rect(self.ecran, (139, 90, 43), plat)
            pygame.draw.rect(self.ecran, (138, 190, 185), self.finished_rect)
            pygame.draw.rect(self.ecran, self.personnage.color, 
                           (self.personnage.x, self.personnage.y, 
                            self.personnage.width, self.personnage.height))
            
            self.afficher_text("Niveau 7 - Labyrinthe", self.police, (255, 255, 255), WIDTH // 2, 30)
            self.afficher_text("M = Menu | L = Niveaux", pygame.font.SysFont('Arial', 20), (200, 200, 200), WIDTH // 2, HEIGHT - 30)
            
            if self.personnage.x + self.personnage.width > self.finished_rect.x and self.personnage.x < self.finished_rect.x + self.finished_rect.width and self.personnage.y + self.personnage.height > self.finished_rect.y and self.personnage.y < self.finished_rect.y + self.finished_rect.height:
                return "win"
            
            pygame.display.flip()
            clock.tick(FPS)
