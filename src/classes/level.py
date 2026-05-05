import pygame
import os
import data.config as config

pygame.init()
pygame.mixer.init()

class Level:
    def __init__(self, ecran):
        self.ecran = ecran

        # Charger l'image de fond
        image_path = os.path.join(os.path.dirname(__file__), "..", "images", "lvls-img.jpg")
        try:
            self.image_fond = pygame.image.load(image_path).convert()
            self.image_fond = pygame.transform.scale(self.image_fond, (config.WIDTH, config.HEIGHT))
        except Exception as e:
            print(f"Erreur lors du chargement de l'image des niveaux : {e}")
            self.image_fond = pygame.Surface((config.WIDTH, config.HEIGHT))
            self.image_fond.fill((25, 25, 40))

        # Boutons (coordonnées directes alignées en grille 5x2 pour la résolution 1280x720)
        self.rect_level1 = pygame.Rect(270, 220, 100, 80)
        self.rect_level2 = pygame.Rect(430, 220, 100, 80)
        self.rect_level3 = pygame.Rect(590, 220, 100, 80)
        self.rect_level4 = pygame.Rect(750, 220, 100, 80)
        self.rect_level5 = pygame.Rect(910, 230, 100, 80) # Légèrement plus bas
        
        self.rect_level6 = pygame.Rect(270, 390, 100, 80) # Ligne du bas descendue
        self.rect_level7 = pygame.Rect(430, 390, 100, 80)
        self.rect_level8 = pygame.Rect(590, 390, 100, 80)
        self.rect_level9 = pygame.Rect(750, 390, 100, 80)
        self.rect_level10 = pygame.Rect(900, 370, 120, 120)
        
        self.rect_aller_menu = pygame.Rect(450, 600, 400, 90) # Menu descendu


        # Liste des boutons et de l'action associée
        self.levels_rects = [
            (self.rect_level1, "level1"),
            (self.rect_level2, "level2"),
            (self.rect_level3, "level3"),
            (self.rect_level4, "level4"),
            (self.rect_level5, "level5"),
            (self.rect_level6, "level6"),
            (self.rect_level7, "level7"),
            (self.rect_level8, "level8"),
            (self.rect_level9, "level9"),
            (self.rect_level10, "level10"),
            (self.rect_aller_menu, "menu")
        ]

    def run_level(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            # Changer le curseur en petite main quand on survole un bouton
            mouse_pos = pygame.mouse.get_pos()
            is_hovering = any(rect.collidepoint(mouse_pos) for rect, action in self.levels_rects)
            
            if is_hovering:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    return "quit"
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        return "menu"
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for rect, action in self.levels_rects:
                        if rect.collidepoint(event.pos):
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                            return action

            # Affichage de l'image de fond
            self.ecran.blit(self.image_fond, (0, 0))

            # (Optionnel) Décommenter ces lignes pour voir les zones de collision des boutons :
            # for rect, action in self.levels_rects:
            #     pygame.draw.rect(self.ecran, (255, 0, 0), rect, 2)

            pygame.display.flip()
            clock.tick(config.FPS)