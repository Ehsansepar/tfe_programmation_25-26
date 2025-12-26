import pygame
from data.config import WIDTH, HEIGHT, FPS
from classes.sol import Sol
from classes.personnage import Personnage


pygame.init()

class Lvl02:
    def __init__(self, ecran, personnage):
        self.ecran = ecran
        self.personnage = personnage
        self.police = pygame.font.SysFont('Arial', 20, bold=True)
        self.police_titre = pygame.font.SysFont('Arial', 30, bold=True)
    
        self.sol = Sol(size=(3000, 20), coulor=(193, 120, 90), pos_x=0, pos_y=HEIGHT-100)
        
        self.finished_rect = pygame.Rect(2500, HEIGHT-150, 50, 100)

        self.plateformes = [
            pygame.Rect(300, 500, 200, 20),
            pygame.Rect(700, 450, 200, 20),
            pygame.Rect(1100, 400, 200, 20),
            pygame.Rect(1500, 350, 200, 20),
            pygame.Rect(1900, 300, 200, 20),
        ]
        

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

            # player_rect = pygame.Rect(self.personnage.x, self.personnage.y, self.personnage.width, self.personnage.height)
            
            # for plat in self.plateformes:
            #     if player_rect.colliderect(plat):
            #         # On vérifie si on arrive par le HAUT (chute)
            #         # On regarde si les pieds étaient au-dessus du milieu de la plateforme
            #         if self.personnage.vitesse_verticale > 0 and self.personnage.y + self.personnage.height < plat.y + 35: 
            #             self.personnage.y = plat.y - self.personnage.height
            #             self.personnage.vitesse_verticale = 0  # Stop la gravité
            #             self.personnage.is_jumping = False
            

            self.personnage.move()
            self.personnage.verifier_platforme(self.plateformes)

            self.milieu_ecran = WIDTH // 2
            self.decalage = 0
            
            if self.personnage.x > self.milieu_ecran :
                self.decalage = self.personnage.x - self.milieu_ecran
                self.personnage.x = self.milieu_ecran
            
            elif self.personnage.x < self.milieu_ecran and self.sol.rect.x < 0:
                self.decalage = self.personnage.x - self.milieu_ecran
                self.personnage.x = self.milieu_ecran

            if self.decalage != 0 :
                self.finished_rect.x -= self.decalage
                self.sol.rect.x -= self.decalage

                for plat in self.plateformes:
                    plat.x = plat.x - self.decalage

            self.ecran.fill((40, 30, 60)) 

            self.afficher_text("Niveau 2", self.police_titre, (255, 255, 255), WIDTH // 2, 40)


            pygame.draw.rect(self.ecran, self.sol.color, self.sol.rect)
            
            for plat in self.plateformes:
                pygame.draw.rect(self.ecran, (139, 90, 43), plat)
    

            pygame.draw.rect(self.ecran, (138, 190, 185), self.finished_rect)
            
            
            
            pygame.draw.rect(self.ecran, self.personnage.color, (self.personnage.x, self.personnage.y, self.personnage.width, self.personnage.height))

            player_rect = pygame.Rect(self.personnage.x, self.personnage.y, self.personnage.width, self.personnage.height)

            if player_rect.colliderect(self.finished_rect):
                return "win"
            
            print(self.sol.rect.x)

            pygame.display.flip()
            clock.tick(FPS)