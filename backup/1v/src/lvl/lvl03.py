import pygame
from data.config import WIDTH, HEIGHT, FPS
from classes.sol import Sol
from classes.personnage import Personnage


class Lvl03:
    def __init__(self, ecran, personnage):
        self.ecran = ecran
        self.personnage = personnage
        self.police = pygame.font.SysFont('Arial', 20, bold=True)
        self.police_titre = pygame.font.SysFont('Arial', 30, bold=True)
        
        self.sol = Sol(size=(3000, 20), coulor=(193, 120, 90), pos_x=0, pos_y=HEIGHT-100)
        self.finished_rect = pygame.Rect(3000-100, HEIGHT-200, 50, 100)
        


        # Escalier
        self.plateformes = [
            pygame.Rect(200, 550, 150, 20),
            pygame.Rect(400, 450, 150, 20),
            pygame.Rect(550, 350, 150, 20),
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
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.rect_menu.collidepoint(event.pos):
                        return "menu"
                    if self.rect_niveaux.collidepoint(event.pos):
                        return "level"
            
            self.personnage.move()
            self.personnage.verifier_platforme(self.plateformes)
            

            self.milieu_ecran = WIDTH // 2
            self.decalage = 0

            if self.personnage.x > self.milieu_ecran:
                self.decalage = self.personnage.x - self.milieu_ecran
                self.personnage.x = self.milieu_ecran

                # for plat in self.plateformes:
                #     plat.x = plat.x - self.decalage

            elif self.personnage.x < self.milieu_ecran and self.sol.rect.x < 0:
                self.decalage = self.personnage.x - self.milieu_ecran
                self.personnage.x = self.milieu_ecran


                # for plat in self.plateformes:
                #     plat.x = plat.x - self.decalage
            
            if self.decalage != 0 :
                self.finished_rect.x -= self.decalage
                self.sol.rect.x -= self.decalage

                for plat in self.plateformes:
                    plat.x = plat.x - self.decalage

                
            self.ecran.fill((50, 30, 70))


            # Titre
            self.afficher_text("Niveau 3", self.police_titre, (255, 255, 255), WIDTH // 2, 40)
            
            pygame.draw.rect(self.ecran, self.sol.color, self.sol.rect)


            for plat in self.plateformes:
                pygame.draw.rect(self.ecran, (139, 90, 43), plat)
            
            pygame.draw.rect(self.ecran, (138, 190, 185), self.finished_rect)
            

            pygame.draw.rect(self.ecran, self.personnage.color, 
                           (self.personnage.x, self.personnage.y, 
                            self.personnage.width, self.personnage.height))
            
            rect_personnage = pygame.Rect(self.personnage.x, self.personnage.y, self.personnage.width, self.personnage.height)
            
            if rect_personnage.colliderect(self.finished_rect):
                return "win"
            
            pygame.display.flip()
            clock.tick(FPS)
