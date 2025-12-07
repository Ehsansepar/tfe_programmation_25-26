import pygame
from config import WIDTH, HEIGHT, FPS
from sol import Sol

class Lvl08:
    def __init__(self, ecran, personnage):
        self.ecran = ecran
        self.personnage = personnage
        self.police = pygame.font.SysFont('Arial', 30)
        
        self.sol = Sol(size=(150, 20), coulor=(193, 120, 90), pos_x=0, pos_y=HEIGHT-100)
        self.finished_rect = pygame.Rect(WIDTH-80, HEIGHT-150, 50, 100)
        
        # Petites plateformes
        self.plateformes = [
            pygame.Rect(180, 600, 80, 20),
            pygame.Rect(300, 500, 80, 20),
            pygame.Rect(420, 400, 80, 20),
            pygame.Rect(540, 300, 80, 20),
            pygame.Rect(660, 400, 80, 20),
            pygame.Rect(660, 550, 140, 20),
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
            self.ecran.fill((100, 80, 120))
            
            pygame.draw.rect(self.ecran, self.sol.color, self.sol.rect)
            for plat in self.plateformes:
                pygame.draw.rect(self.ecran, (139, 90, 43), plat)
            pygame.draw.rect(self.ecran, (138, 190, 185), self.finished_rect)
            pygame.draw.rect(self.ecran, self.personnage.color, 
                           (self.personnage.x, self.personnage.y, 
                            self.personnage.width, self.personnage.height))
            
            self.afficher_text("Niveau 8", self.police, (255, 255, 255), WIDTH // 2, 30)
            self.afficher_text("M = Menu | L = Niveaux", pygame.font.SysFont('Arial', 20), (200, 200, 200), WIDTH // 2, HEIGHT - 30)
            
            if self.personnage.x + self.personnage.width > self.finished_rect.x and self.personnage.x < self.finished_rect.x + self.finished_rect.width and self.personnage.y + self.personnage.height > self.finished_rect.y and self.personnage.y < self.finished_rect.y + self.finished_rect.height:
                return "win"
            
            pygame.display.flip()
            clock.tick(FPS)
