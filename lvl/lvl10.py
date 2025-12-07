import pygame
from config import WIDTH, HEIGHT, FPS
from sol import Sol

class Lvl10:
    def __init__(self, ecran, personnage):
        self.ecran = ecran
        self.personnage = personnage
        self.police = pygame.font.SysFont('Arial', 30)
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
            self.ecran.fill((50, 20, 60))
            
            pygame.draw.rect(self.ecran, self.sol.color, self.sol.rect)
            for plat in self.plateformes:
                pygame.draw.rect(self.ecran, (139, 90, 43), plat)
            
            # Zone d'arrivée dorée pour le niveau final
            pygame.draw.rect(self.ecran, (255, 215, 0), self.finished_rect)
            pygame.draw.rect(self.ecran, (255, 255, 255), self.finished_rect, 3)
            
            pygame.draw.rect(self.ecran, self.personnage.color, 
                           (self.personnage.x, self.personnage.y, 
                            self.personnage.width, self.personnage.height))
            
            self.afficher_text("🔥 NIVEAU FINAL 🔥", self.police_titre, (255, 215, 0), WIDTH // 2, 30)
            self.afficher_text("M = Menu | L = Niveaux", pygame.font.SysFont('Arial', 20), (200, 200, 200), WIDTH // 2, HEIGHT - 30)
            
            if self.personnage.x + self.personnage.width > self.finished_rect.x and self.personnage.x < self.finished_rect.x + self.finished_rect.width and self.personnage.y + self.personnage.height > self.finished_rect.y and self.personnage.y < self.finished_rect.y + self.finished_rect.height:
                return "win"
            
            pygame.display.flip()
            clock.tick(FPS)
