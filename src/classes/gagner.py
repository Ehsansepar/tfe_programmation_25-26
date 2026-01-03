import pygame
from data.config import WIDTH, HEIGHT, FPS
from classes.personnage import Personnage
from classes.sol import Sol


pygame.init()
pygame.mixer.init()

class Gagner :
    def __init__(self, ecran) :
        self.ecran = ecran

        global police
        police = pygame.font.SysFont('comicsansms', 40, bold=True)

        self.finished_rect = pygame.Rect(WIDTH-100, HEIGHT-150, 50, 100)
        

        self.son_hover = pygame.mixer.Sound("src/sounds/gta-menu.wav")
        self.son_back = pygame.mixer.Sound("src/sounds/gta-menuOut.wav")

        self.son_back.set_volume(0.5)
        self.son_hover.set_volume(0.5)

        return
    

    def afficher_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        rect = img.get_rect(center=(x, y))
        self.ecran.blit(img, rect)

    def run_gagner(self, personnage):

        global police
        running = True

        memoire_bouton = ""

        rect_menu = pygame.Rect(WIDTH // 2 - 150, 330, 300, 70)
        rect_niveaux = pygame.Rect(WIDTH // 2 - 150, 430, 300, 70)
        rect_quitter = pygame.Rect(WIDTH // 2 - 150, 530, 300, 70)

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
                        self.son_back.play()
                        print("menu clicked from gagner.py")
                        return "menu"
                    
                    if rect_niveaux.collidepoint(event.pos):
                        self.son_back.play()
                        print("niveaux clicked from gagner.py")
                        print("return level")
                        return "level"
                    
                    if rect_quitter.collidepoint(event.pos):
                        self.son_back.play()
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
                if memoire_bouton != "menu": 
                    self.son_hover.play()
                    memoire_bouton = "menu"

            if rect_niveaux.collidepoint(mouse_pos):
                couleur_rect_niveaux = (187, 143, 206)  # Violet clair
                je_suis_sur_bouton = True

                if memoire_bouton != "niveau": 
                    self.son_hover.play()
                    memoire_bouton = "niveau"

            if rect_quitter.collidepoint(mouse_pos):
                couleur_rect_quitter = (236, 112, 99)  # Rouge clair
                je_suis_sur_bouton = True

                if memoire_bouton != "quit": 
                    self.son_hover.play()
                    memoire_bouton = "quit"

            if je_suis_sur_bouton == False :
                memoire_bouton = ""

            # ============================================================
            # ANCIENNE MÉTHODE (TA MÉTHODE) - NE FONCTIONNE PAS BIEN
            # Problème: get_pressed() détecte si le bouton est MAINTENU enfoncé
            # Donc le clic reste actif sur plusieurs frames et plusieurs pages
            # ============================================================
            # mouse_clicked = pygame.mouse.get_pressed()
            # if rect_menu.collidepoint(mouse_pos):
            #     if mouse_clicked[0]:
            #         mouse_clicked = [0, 0, 0]  # ça ne réinitialise pas vraiment le clic!
            #         return "menu"
            # ============================================================

            pygame.draw.rect(self.ecran, couleur_rect_menu, rect_menu, 0, 20)
            pygame.draw.rect(self.ecran, couleur_rect_niveaux, rect_niveaux, 0, 20)
            pygame.draw.rect(self.ecran, couleur_rect_quitter, rect_quitter, 0, 20)

            self.afficher_text("Félicitations !", police, (255, 215, 0), WIDTH // 2, 150)
            self.afficher_text("Vous avez gagné !", police, (255, 255, 255), WIDTH // 2, 220)

            # Texte centré dans les nouveaux boutons
            self.afficher_text("Retour au menu", police, (255, 255, 255), WIDTH // 2, 365)
            self.afficher_text("Niveaux", police, (255, 255, 255), WIDTH // 2, 465)
            self.afficher_text("Quitter", police, (255, 255, 255), WIDTH // 2, 565)

            
            
            
            pygame.display.flip()