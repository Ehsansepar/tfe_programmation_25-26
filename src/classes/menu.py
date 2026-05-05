import pygame
import os
import data.config as config

pygame.init()
pygame.mixer.init()

class Menu:
    def __init__(self, ecran):
        self.ecran = ecran
        
        # Charger l'image de fond
        image_path = os.path.join(os.path.dirname(__file__), "..", "images", "menu_img.jpeg")
        try:
            self.image_fond = pygame.image.load(image_path).convert()
            self.image_fond = pygame.transform.scale(self.image_fond, (config.WIDTH, config.HEIGHT))
        except Exception as e:
            print(f"Erreur lors du chargement de l'image du menu : {e}")
            self.image_fond = pygame.Surface((config.WIDTH, config.HEIGHT))
            self.image_fond.fill((0, 0, 0))

        # Nouvelles zones de clics basées sur l'image
        self.rect_jouer = pygame.Rect(505, 275, 310, 70)
        self.rect_niveaux = pygame.Rect(505, 365, 310, 70)
        self.rect_parametres = pygame.Rect(505, 455, 310, 70)
        self.rect_quitter = pygame.Rect(505, 545, 310, 70)

    def run_menu(self):
        running = True

        while running:
            # Changer le curseur en petite main quand on survole un bouton
            mouse_pos = pygame.mouse.get_pos()
            if (self.rect_jouer.collidepoint(mouse_pos) or 
                self.rect_niveaux.collidepoint(mouse_pos) or 
                self.rect_parametres.collidepoint(mouse_pos) or 
                self.rect_quitter.collidepoint(mouse_pos)):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    return "quit"

                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_KP1] or event.unicode in ['&', '1']:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        return "game"
                    elif event.key in [pygame.K_2, pygame.K_KP2] or event.unicode in ['é', '2']:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        return "level"
                    elif event.key in [pygame.K_3, pygame.K_KP3] or event.unicode in ['"', '3']:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        return "parametre"
                    elif event.key in [pygame.K_4, pygame.K_KP4] or event.unicode in ["'", '4']:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        return "quit"
                    elif event.key == pygame.K_h:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        return "welcome"
                    
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.rect_jouer.collidepoint(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        return "game"
                    if self.rect_niveaux.collidepoint(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        return "level"
                    if self.rect_parametres.collidepoint(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        return "parametre"
                    if self.rect_quitter.collidepoint(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        return "quit"

            # Afficher l'image de fond
            self.ecran.blit(self.image_fond, (0, 0))

            pygame.display.flip()