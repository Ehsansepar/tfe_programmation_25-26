from pygame.draw import rect
import pygame
import os
import data.config as config

pygame.init()

class Gagner:
    def __init__(self, ecran, niveau_termine=1):
        self.ecran = ecran
        self.niveau_termine = niveau_termine 

        image_path = os.path.join(os.path.dirname(__file__), "..", "images", "img_win.jpg")
        try:
            self.image_fond = pygame.image.load(image_path).convert()
            self.image_fond = pygame.transform.scale(self.image_fond, (config.WIDTH, config.HEIGHT))
        except Exception as e:
            print(f"Erreur lors du chargement de l'image de victoire : {e}")
            self.image_fond = pygame.Surface((config.WIDTH, config.HEIGHT))
            self.image_fond.fill((34, 139, 34))

        self.rect_continuer = pygame.Rect(145, 635, 318, 70)
        self.rect_reessayer = pygame.Rect(490, 635, 318, 70)
        self.rect_menu = pygame.Rect(825, 635, 318, 70)
        

    def run_gagner(self, personnage):
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()

            if (self.rect_continuer.collidepoint(mouse_pos) or
                self.rect_reessayer.collidepoint(mouse_pos) or
                self.rect_menu.collidepoint(mouse_pos)):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.rect_continuer.collidepoint(event.pos):
                        # aller niv suivant
                        niveau_suivant = self.niveau_termine + 1
                        return f"level{niveau_suivant}"
                    if self.rect_reessayer.collidepoint(event.pos):
                        # rejou mm niveau
                        return f"level{self.niveau_termine}"
                    if self.rect_menu.collidepoint(event.pos):
                        return "menu"

            self.ecran.blit(self.image_fond, (0, 0))

            # pygame.draw.rect(self.ecran, (255, 255, 255), self.rect_continuer, 2)
            # pygame.draw.rect(self.ecran, (255, 255, 255), self.rect_reessayer, 2)
            # pygame.draw.rect(self.ecran, (255, 255, 255), self.rect_menu, 2)

            pygame.display.flip()