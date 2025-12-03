import pygame
from config import *


pygame.init()

global police

class Menu :

    def __init__(self, ecran):
        self.ecran = ecran

        global police
        police = pygame.font.SysFont('comicsansms', 40, bold=True)


        self.rect_jouer = pygame.Rect(WIDTH // 2 - 150, 325, 300, 60)
        self.rect_parametres = pygame.Rect(WIDTH // 2 - 150, 425, 300, 60)
        self.rect_quitter = pygame.Rect(WIDTH // 2 - 150, 525, 300, 60)


        return
    
    def afficher_text(self, text, font, text_col, x, y) :
        img = font.render(text, True, text_col)
        rect = img.get_rect(center=(x, y))
        self.ecran.blit(img, rect)

    def run_menu(self) :

        global police
        running = True

        while running :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.KEYDOWN:
 
                    if event.key in [pygame.K_1, pygame.K_KP1] or event.unicode in ['&', '1']:
                        return "game"
                    elif event.key in [pygame.K_2, pygame.K_KP2] or event.unicode in ['é', '2']:
                        return "parametre"
                    elif event.key in [pygame.K_3, pygame.K_KP3] or event.unicode in ['"', '3']:
                        return "quit"

            
            self.ecran.fill((0, 129, 167)) 


            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = pygame.mouse.get_pressed()

            couleur_jouer = (46, 204, 113)       # Vert
            couleur_param = (52, 152, 219)       # Bleu
            couleur_quitter = (231, 76, 60)      # Rouge

            #  hover 
            if self.rect_jouer.collidepoint(mouse_pos):
                couleur_jouer = (88, 214, 141)   # Vert clair
                if mouse_clicked[0]:
                    return "game"
                    
            if self.rect_parametres.collidepoint(mouse_pos):
                couleur_param = (93, 173, 226)   # Bleu clair
                if mouse_clicked[0]:
                    return "parametre"
                    
            if self.rect_quitter.collidepoint(mouse_pos):
                couleur_quitter = (236, 112, 99) # Rouge clair
                if mouse_clicked[0]:
                    return "quit"

            #  (border_radius=15)
            pygame.draw.rect(self.ecran, couleur_jouer, self.rect_jouer, 0, 15)
            pygame.draw.rect(self.ecran, couleur_param, self.rect_parametres, 0, 15)
            pygame.draw.rect(self.ecran, couleur_quitter, self.rect_quitter, 0, 15)

            # Bordure blanche autour des boutons
            # pygame.draw.rect(self.ecran, (255, 255, 255), self.rect_jouer, 3, 15)
            # pygame.draw.rect(self.ecran, (255, 255, 255), self.rect_parametres, 3, 15)
            # pygame.draw.rect(self.ecran, (255, 255, 255), self.rect_quitter, 3, 15)

            # Titreee
            self.afficher_text("Bonjour et Bienvenue !", police, (253, 252, 220), WIDTH // 2, 150)
            

            self.afficher_text("1 - Jouer", police, (255, 255, 255), WIDTH // 2, 355)
            self.afficher_text("2 - Paramètres", police, (255, 255, 255), WIDTH // 2, 455)
            self.afficher_text("3 - Quitter", police, (255, 255, 255), WIDTH // 2, 555)

            pygame.display.flip()