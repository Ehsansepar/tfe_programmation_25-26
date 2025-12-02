import pygame
from config import *


pygame.init()

global police

class Menu :

    def __init__(self, ecran):
        self.ecran = ecran

        global police
        police = pygame.font.SysFont('comicsansms', 40, bold=True)


        self.rect_jouer = pygame.Rect(WIDTH // 2 - 100, 325, 200, 50)
        self.rect_parametres = pygame.Rect(WIDTH // 2 - 100, 425, 200, 50)
        self.rect_quitter = pygame.Rect(WIDTH // 2 - 100, 525, 200, 50)


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

            mouse_pos = pygame.mouse.get_pos()
            

            if self.rect_jouer.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    return "game"
            if self.rect_parametres.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    return "settings"
            if self.rect_quitter.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    return "quit"

            pygame.draw.rect(self.ecran, (200, 200, 200), self.rect_jouer)
            pygame.draw.rect(self.ecran, (200, 200, 200), self.rect_parametres)
            pygame.draw.rect(self.ecran, (200, 200, 200), self.rect_quitter)

            self.ecran.fill((0, 129, 167)) 


            self.afficher_text("Bonjour et Bienvenue !", police, (253, 252, 220), WIDTH // 2, 150)
            self.afficher_text("1 - Jouer", police, (0, 175, 185), WIDTH // 2, 350)
            self.afficher_text("2 - Paramètres", police, (254, 217, 183), WIDTH // 2, 450)
            self.afficher_text("3 - Quitter", police, (240, 113, 103), WIDTH // 2, 550)



            pygame.display.flip()