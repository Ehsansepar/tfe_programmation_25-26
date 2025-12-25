import pygame
from data.config import *


pygame.init()
pygame.mixer.init()

global police

class Menu :

    def __init__(self, ecran):
        self.ecran = ecran

        global police
        police = pygame.font.SysFont('comicsansms', 40, bold=True)


        self.rect_jouer = pygame.Rect(WIDTH // 2 - 150, 275, 300, 60)
        self.rect_niveaux = pygame.Rect(WIDTH // 2 - 150, 365, 300, 60)
        self.rect_parametres = pygame.Rect(WIDTH // 2 - 150, 455, 300, 60)
        self.rect_quitter = pygame.Rect(WIDTH // 2 - 150, 545, 300, 60)


        self.son_hover = pygame.mixer.Sound("src/sounds/gta-menu.wav")
        

        self.son_hover.set_volume(0.5) # 50% le sons 
        return
    
    def afficher_text(self, text, font, text_col, x, y) :
        img = font.render(text, True, text_col)
        rect = img.get_rect(center=(x, y))
        self.ecran.blit(img, rect)
    
    def run_menu(self) :

        global police
        running = True

        memoire_bouton = ""

        while running :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.KEYDOWN:
 
                    if event.key in [pygame.K_1, pygame.K_KP1] or event.unicode in ['&', '1']:
                        return "game"
                    elif event.key in [pygame.K_2, pygame.K_KP2] or event.unicode in ['é', '2']:
                        return "level"
                    elif event.key in [pygame.K_3, pygame.K_KP3] or event.unicode in ['"', '3']:
                        return "parametre"
                    elif event.key in [pygame.K_4, pygame.K_KP4] or event.unicode in ["'", '4']:
                        return "quit"

                # ============================================================
                # BONNE MÉTHODE - MOUSEBUTTONDOWN
                # Détecte le MOMENT EXACT du clic (1 seule fois)
                # Le clic est un ÉVÉNEMENT, pas un état continu
                # ============================================================
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.rect_jouer.collidepoint(event.pos):
                        return "game"
                    if self.rect_niveaux.collidepoint(event.pos):
                        return "level"
                    if self.rect_parametres.collidepoint(event.pos):
                        return "parametre"
                    if self.rect_quitter.collidepoint(event.pos):
                        return "quit"

            
            self.ecran.fill((0, 129, 167)) 


            mouse_pos = pygame.mouse.get_pos()

            couleur_jouer = (46, 204, 113)       # Vert
            couleur_niveaux = (155, 89, 182)     # Violet
            couleur_param = (52, 152, 219)       # Bleu
            couleur_quitter = (231, 76, 60)      # Rouge


            #  hover 

            je_suis_sur_un_bouton = False

            if self.rect_jouer.collidepoint(mouse_pos):
                couleur_jouer = (88, 214, 141)   # Vert clair
                je_suis_sur_un_bouton = True
                if memoire_bouton != "jouer" :
                    self.son_hover.play()   
                    memoire_bouton = "jouer"

            if self.rect_niveaux.collidepoint(mouse_pos):
                couleur_niveaux = (187, 143, 206) # Violet clair
                je_suis_sur_un_bouton = True

                if memoire_bouton != "niveau" :
                    self.son_hover.play()
                    memoire_bouton = "niveau"

                    
            if self.rect_parametres.collidepoint(mouse_pos):
                couleur_param = (93, 173, 226)   # Bleu clair
                je_suis_sur_un_bouton = True

                if memoire_bouton != "parametre" :
                    self.son_hover.play()
                    memoire_bouton = "parametre"

                    
            if self.rect_quitter.collidepoint(mouse_pos):
                couleur_quitter = (236, 112, 99) # Rouge clair
                je_suis_sur_un_bouton = True

                if memoire_bouton != "quit" :
                    self.son_hover.play()
                    memoire_bouton = "quit"


            if je_suis_sur_un_bouton == False : 
                memoire_bouton = ""


            pygame.draw.rect(self.ecran, couleur_jouer, self.rect_jouer, 0, 15)
            pygame.draw.rect(self.ecran, couleur_niveaux, self.rect_niveaux, 0, 15)
            pygame.draw.rect(self.ecran, couleur_param, self.rect_parametres, 0, 15)
            pygame.draw.rect(self.ecran, couleur_quitter, self.rect_quitter, 0, 15)

            # Bordure blanche autour des boutons
            # pygame.draw.rect(self.ecran, (255, 255, 255), self.rect_jouer, 3, 15)
            # pygame.draw.rect(self.ecran, (255, 255, 255), self.rect_parametres, 3, 15)
            # pygame.draw.rect(self.ecran, (255, 255, 255), self.rect_quitter, 3, 15)

            # Titreee
            self.afficher_text("Bonjour et Bienvenue !", police, (253, 252, 220), WIDTH // 2, 150)
            

            self.afficher_text("1 - Jouer", police, (255, 255, 255), WIDTH // 2, 305)
            self.afficher_text("2 - Niveaux", police, (255, 255, 255), WIDTH // 2, 395)
            self.afficher_text("3 - Paramètres", police, (255, 255, 255), WIDTH // 2, 485)
            self.afficher_text("4 - Quitter", police, (255, 255, 255), WIDTH // 2, 575)

            pygame.display.flip()