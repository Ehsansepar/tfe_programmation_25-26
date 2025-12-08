import pygame
from config import WIDTH, HEIGHT, FPS
from sol import Sol
from personnage import Personnage
class Lvl02:
    def __init__(self, ecran, personnage):
        self.ecran = ecran
        self.personnage = personnage
        self.police = pygame.font.SysFont('Arial', 30)
        self.police = pygame.font.SysFont('Arial', 20, bold=True)
        self.police_titre = pygame.font.SysFont('Arial', 30, bold=True)
        
        self.sol = Sol(size=(WIDTH, 20), coulor=(193, 120, 90), pos_x=0, pos_y=HEIGHT-100)
        self.finished_rect = pygame.Rect(WIDTH-100, HEIGHT-150, 50, 100)
        
        
        self.plateformes = [
            pygame.Rect(300, 500, 200, 20),
            # pygame.Rect(200, 300, 100, 100)
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
            

            self.personnage.move()

            # player_rect = pygame.Rect(self.personnage.x, self.personnage.y, self.personnage.width, self.personnage.height)
            
            # for plat in self.plateformes:
            #     if player_rect.colliderect(plat):
            #         # On vérifie si on arrive par le HAUT (chute)
            #         # On regarde si les pieds étaient au-dessus du milieu de la plateforme
            #         if self.personnage.vitesse_verticale > 0 and self.personnage.y + self.personnage.height < plat.y + 35: 
            #             self.personnage.y = plat.y - self.personnage.height
            #             self.personnage.vitesse_verticale = 0  # Stop la gravité
            #             self.personnage.is_jumping = False
            

            self.personnage.verifier_platforme(self.plateformes)

            # for plat in self.plateformes:
            #     if self.personnage.player_rect.colliderect(plat):

            #         if self.personnage.vitesse_verticale > 0:
            #             self.personnage.y = plat.y - self.personnage.height
            #             self.personnage.vitesse_verticale = 0
            #             self.personnage.is_jumping = False


            self.ecran.fill((40, 30, 60)) # 
            
           #hover
            mouse_pos = pygame.mouse.get_pos()
            
            
            col_menu = (70, 70, 70)
            col_niveaux = (70, 70, 70)
            
            if self.rect_menu.collidepoint(mouse_pos):
                col_menu = (243, 156, 18)
            
            if self.rect_niveaux.collidepoint(mouse_pos):
                col_niveaux = (120, 120, 120)



            pygame.draw.rect(self.ecran, col_menu, self.rect_menu, border_radius=10)
            pygame.draw.rect(self.ecran, (241, 196, 15), self.rect_menu, 2, border_radius=10) # Contour
            self.afficher_text("MENU", self.police, (255, 255, 255), self.rect_menu.centerx, self.rect_menu.centery)


            pygame.draw.rect(self.ecran, col_niveaux, self.rect_niveaux, border_radius=10)
            pygame.draw.rect(self.ecran, (200, 200, 200), self.rect_niveaux, 2, border_radius=10) # Contour
            self.afficher_text("LEVELS", self.police, (255, 255, 255), self.rect_niveaux.centerx, self.rect_niveaux.centery)


            self.afficher_text("Niveau 2", self.police_titre, (255, 255, 255), WIDTH // 2, 40)


   
            pygame.draw.rect(self.ecran, self.sol.color, self.sol.rect)
            
            # Plateformes
            for plat in self.plateformes:
                pygame.draw.rect(self.ecran, (139, 90, 43), plat)
            
            #quand j arrive et je gagne
            pygame.draw.rect(self.ecran, (138, 190, 185), self.finished_rect)
            

            pygame.draw.rect(self.ecran, self.personnage.color, 
                           (self.personnage.x, self.personnage.y, 
                            self.personnage.width, self.personnage.height))
            
            # Vérifier victoire
            if self.personnage.x + self.personnage.width > self.finished_rect.x and self.personnage.x < self.finished_rect.x + self.finished_rect.width and self.personnage.y + self.personnage.height > self.finished_rect.y and self.personnage.y < self.finished_rect.y + self.finished_rect.height:
                return "win"
            
            pygame.display.flip()
            clock.tick(FPS)