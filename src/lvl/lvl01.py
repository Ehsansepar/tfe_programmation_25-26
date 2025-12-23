import pygame
from data.config import WIDTH, HEIGHT, FPS
from classes.sol import Sol
from classes.personnage import Personnage
class Lvl01:
    def __init__(self, ecran, personnage):
        self.ecran = ecran
        self.personnage = personnage
        self.police = pygame.font.SysFont('Arial', 20, bold=True)
        self.police_titre = pygame.font.SysFont('Arial', 30, bold=True)
        
        # Sol
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
        
        self.camera_x = 0
    
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

                self.finished_rect.x = self.finished_rect.x - self.decalage


            self.ecran.fill((30, 30, 50))
            
            # Titre
            self.afficher_text("Niveau 1", self.police_titre, (255, 255, 255), WIDTH // 2, 40)
            

# ------------------------------------------------------------------------------------------------------------------

            # --- VISUALISATION DES ÉCRANS (POUR COMPRENDRE) ---
            # On dessine des cadres rouges pour montrer les "écrans" virtuels
            couleur_debug = (255, 0, 0) # Rouge
            for i in range(5): # On affiche 5 écrans
                pos_x_ecran = i * WIDTH # 0, 800, 1600, 2400...
                
                # Dessiner le cadre de l'écran
                pygame.draw.rect(self.ecran, couleur_debug, 
                               (pos_x_ecran - self.camera_x, 0, WIDTH, HEIGHT), 5) # 5 = épaisseur du trait
                
                # Écrire le numéro de l'écran
                self.afficher_text(f"ECRAN {i+1}", self.police_titre, couleur_debug, 
                                 pos_x_ecran - self.camera_x + WIDTH // 2, 100)
            # --------------------------------------------------

# ------------------------------------------------------------------------------------------------------------------



            # Sol
            pygame.draw.rect(self.ecran, self.sol.color, (self.sol.rect.x - self.decalage, self.sol.rect.y, 
                                                   self.sol.rect.width, self.sol.rect.height))
            
            # Plateformes
            for plateforme in self.plateformes:
                pygame.draw.rect(self.ecran, (100, 100, 100), 
                               (plateforme.x, plateforme.y, 
                                plateforme.width, plateforme.height))

            # Zone d'arrivée
            pygame.draw.rect(self.ecran, (138, 190, 185), (self.finished_rect.x - self.decalage, self.finished_rect.y, 
                                                   self.finished_rect.width, self.finished_rect.height))
            
            # Personnage
            pygame.draw.rect(self.ecran, self.personnage.color, 
                           (self.personnage.x - self.camera_x, self.personnage.y, 
                            self.personnage.width, self.personnage.height))
            
            
            # Vérifier victoire
            personnage_rect = pygame.Rect(self.personnage.x, self.personnage.y, 
                                         self.personnage.width, self.personnage.height)
            if personnage_rect.colliderect(self.finished_rect):
                return "win"
            
            
            pygame.display.flip()
            clock.tick(FPS)
