import pygame
from config import *


pygame.init()

global police

class Menu :

    def __init__(self, ecran):
        self.ecran = ecran

        global police
        police = pygame.font.SysFont('comicsansms', 40, bold=True)
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
                    # Chiffres: pavé numérique + touches AZERTY (&, é, ")
                    if event.key in [pygame.K_1, pygame.K_KP1] or event.unicode in ['&', '1']:
                        return "game"
                    elif event.key in [pygame.K_2, pygame.K_KP2] or event.unicode in ['é', '2']:
                        return "settings"
                    elif event.key in [pygame.K_3, pygame.K_KP3] or event.unicode in ['"', '3']:
                        return "quit"

            # Fond d'écran : Cerulean (Bleu océan)
            self.ecran.fill((0, 129, 167)) 

            # Titre : Light Yellow (Jaune pâle) - Position Y = 150
            self.afficher_text("Bonjour et Bienvenue !", police, (253, 252, 220), WIDTH // 2, 150)
            
            # Option 1 : Tropical Teal (Bleu/Vert d'eau) - Position Y = 350
            self.afficher_text("1 - Jouer", police, (0, 175, 185), WIDTH // 2, 350)

            # Option 2 : Soft Apricot (Orange doux) - Position Y = 450
            self.afficher_text("2 - Paramètres", police, (254, 217, 183), WIDTH // 2, 450)

            # Option 3 : Vibrant Coral (Corail/Rouge) - Position Y = 550
            self.afficher_text("3 - Quitter", police, (240, 113, 103), WIDTH // 2, 550)





            pygame.display.flip()