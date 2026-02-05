import pygame
# from data.config import WIDTH, HEIGHT, FPS
import data.config as config
from classes.personnage import Personnage
from classes.sol import Sol


pygame.init()
pygame.mixer.init()

class Gagner :
    def __init__(self, ecran) :
        self.ecran = ecran

        global police
        police = pygame.font.SysFont('comicsansms', 40, bold=True)

        self.finished_rect = pygame.Rect(config.WIDTH-100, config.HEIGHT-150, 50, 100)
        



        return
    

    def afficher_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        rect = img.get_rect(center=(x, y))
        self.ecran.blit(img, rect)

    def run_gagner(self, personnage):

        global police
        running = True

        memoire_bouton = ""

        rect_menu = pygame.Rect(config.WIDTH // 2 - 150, 330, 300, 70)
        rect_niveaux = pygame.Rect(config.WIDTH // 2 - 150, 430, 300, 70)
        rect_quitter = pygame.Rect(config.WIDTH // 2 - 150, 530, 300, 70)

        while running:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        return "menu"
                    elif event.key == pygame.K_l:
                        return "level"
                    elif event.key == pygame.K_END:
                        return "quit"

                # ============================================================
                #MOUSEBUTTONDOWN
                # Détecte le MOMENT EXACT du clic (1 seule fois)
                # ============================================================
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if rect_menu.collidepoint(event.pos):
                        print("menu clicked from gagner.py")
                        return "menu"
                    
                    if rect_niveaux.collidepoint(event.pos):
                        print("niveaux clicked from gagner.py")
                        print("return level")
                        return "level"
                    
                    if rect_quitter.collidepoint(event.pos):
                        print("quit clicked from gagner.py")
                        return "quit"

            self.ecran.fill((34, 139, 34))

            mouse_pos = pygame.mouse.get_pos()

            couleur_rect_menu = (46, 204, 113)      # Vert
            couleur_rect_niveaux = (155, 89, 182)    # Violet
            couleur_rect_quitter = (231, 76, 60)     # Rouge

            je_suis_sur_bouton = False

            if rect_menu.collidepoint(mouse_pos):
                couleur_rect_menu = (88, 214, 141)   # Vert clair
                je_suis_sur_bouton = True


            if rect_niveaux.collidepoint(mouse_pos):
                couleur_rect_niveaux = (187, 143, 206)  # Violet clair
                je_suis_sur_bouton = True



            if rect_quitter.collidepoint(mouse_pos):
                couleur_rect_quitter = (236, 112, 99)  # Rouge clair
                je_suis_sur_bouton = True



            if je_suis_sur_bouton == False :
                memoire_bouton = ""

            pygame.draw.rect(self.ecran, couleur_rect_menu, rect_menu, 0, 20)
            pygame.draw.rect(self.ecran, couleur_rect_niveaux, rect_niveaux, 0, 20)
            pygame.draw.rect(self.ecran, couleur_rect_quitter, rect_quitter, 0, 20)

            self.afficher_text("Félicitations !", police, (255, 215, 0), config.WIDTH // 2, 150)
            self.afficher_text("Vous avez gagné !", police, (255, 255, 255), config.WIDTH // 2, 220)

            # Texte centré dans les nouveaux boutons
            self.afficher_text("Retour au menu", police, (255, 255, 255), config.WIDTH // 2, 365)
            self.afficher_text("Niveaux", police, (255, 255, 255), config.WIDTH // 2, 465)
            self.afficher_text("Quitter", police, (255, 255, 255), config.WIDTH // 2, 565)

            
            
            
            pygame.display.flip()