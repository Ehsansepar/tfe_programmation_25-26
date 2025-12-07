

from os import name

import pygame

from config import WIDTH, HEIGHT, FPS

class Level:
    def __init__(self, ecran):
        self.ecran = ecran

        global police
        police = pygame.font.SysFont('comicsansms', 40, bold=True)

        # Ligne 1 (niveaux 1-5)
        self.rect_level1 = pygame.Rect(WIDTH // 2 - 270, HEIGHT // 2 - 80, 80, 80)
        self.rect_level2 = pygame.Rect(WIDTH // 2 - 170, HEIGHT // 2 - 80, 80, 80)
        self.rect_level3 = pygame.Rect(WIDTH // 2 - 70, HEIGHT // 2 - 80, 80, 80)
        self.rect_level4 = pygame.Rect(WIDTH // 2 + 30, HEIGHT // 2 - 80, 80, 80)
        self.rect_level5 = pygame.Rect(WIDTH // 2 + 130, HEIGHT // 2 - 80, 80, 80)
        
        # Ligne 2 (niveaux 6-10)
        self.rect_level6 = pygame.Rect(WIDTH // 2 - 270, HEIGHT // 2 + 20, 80, 80)
        self.rect_level7 = pygame.Rect(WIDTH // 2 - 170, HEIGHT // 2 + 20, 80, 80)
        self.rect_level8 = pygame.Rect(WIDTH // 2 - 70, HEIGHT // 2 + 20, 80, 80)
        self.rect_level9 = pygame.Rect(WIDTH // 2 + 30, HEIGHT // 2 + 20, 80, 80)
        self.rect_level10 = pygame.Rect(WIDTH // 2 + 130, HEIGHT // 2 + 20, 80, 80)

        self.rect_aller_menu = pygame.Rect(WIDTH // 2 - 150, HEIGHT - 100, 300, 60)
        
        # Couleurs différentes pour chaque niveau
        self.couleur1 = (46, 204, 113)    # Vert
        self.couleur2 = (52, 152, 219)    # Bleu
        self.couleur3 = (155, 89, 182)    # Violet
        self.couleur4 = (241, 196, 15)    # Jaune
        self.couleur5 = (230, 126, 34)    # Orange
        self.couleur6 = (231, 76, 60)     # Rouge
        self.couleur7 = (26, 188, 156)    # Turquoise
        self.couleur8 = (149, 165, 166)   # Gris
        self.couleur9 = (142, 68, 173)    # Violet foncé
        self.couleur10 = (192, 57, 43)    # Rouge foncé


        self.couleur_aller_menu = (241, 196, 15)   # Jaune
        return

    def afficher_text(self, text, font, text_col, x, y) :
        img = font.render(text, True, text_col)
        rect = img.get_rect(center=(x, y))
        self.ecran.blit(img, rect)

    def run_level(self):
        clock = pygame.time.Clock()
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        return "menu"

                # ============================================================
                # BONNE MÉTHODE - MOUSEBUTTONDOWN
                # Détecte le MOMENT EXACT du clic (1 seule fois)
                # ============================================================
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.rect_level1.collidepoint(event.pos):
                        return "level1"
                    if self.rect_level2.collidepoint(event.pos):
                        return "level2"
                    if self.rect_level3.collidepoint(event.pos):
                        return "level3"
                    if self.rect_level4.collidepoint(event.pos):
                        return "level4"
                    if self.rect_level5.collidepoint(event.pos):
                        return "level5"
                    if self.rect_level6.collidepoint(event.pos):
                        return "level6"
                    if self.rect_level7.collidepoint(event.pos):
                        return "level7"
                    if self.rect_level8.collidepoint(event.pos):
                        return "level8"
                    if self.rect_level9.collidepoint(event.pos):
                        return "level9"
                    if self.rect_level10.collidepoint(event.pos):
                        return "level10"
                    
                    if self.rect_aller_menu.collidepoint(event.pos):
                        return "menu"
                    
            self.ecran.fill((25, 25, 40))  # Fond sombre


            mouse_pos = pygame.mouse.get_pos()

            # Couleurs de base
            c1, c2, c3, c4, c5 = self.couleur1, self.couleur2, self.couleur3, self.couleur4, self.couleur5
            c6, c7, c8, c9, c10, c_menu = self.couleur6, self.couleur7, self.couleur8, self.couleur9, self.couleur10, self.couleur_aller_menu

            # bouton_menu_hover_color = (243, 156, 18)

            #hover
            if self.rect_level1.collidepoint(mouse_pos):
                c1 = (88, 214, 141)  # Vert clair
            elif self.rect_level2.collidepoint(mouse_pos):
                c2 = (93, 173, 226)  # Bleu clair
            elif self.rect_level3.collidepoint(mouse_pos):
                c3 = (187, 143, 206)  # Violet clair
            elif self.rect_level4.collidepoint(mouse_pos):
                c4 = (247, 220, 111)  # Jaune clair
            elif self.rect_level5.collidepoint(mouse_pos):
                c5 = (245, 176, 65)  # Orange clair
            elif self.rect_level6.collidepoint(mouse_pos):
                c6 = (236, 112, 99)  # Rouge clair
            elif self.rect_level7.collidepoint(mouse_pos):
                c7 = (72, 201, 176)  # Turquoise clair
            elif self.rect_level8.collidepoint(mouse_pos):
                c8 = (189, 195, 199)  # Gris clair
            elif self.rect_level9.collidepoint(mouse_pos):
                c9 = (175, 122, 197)  # Violet clair
            elif self.rect_level10.collidepoint(mouse_pos):
                c10 = (217, 136, 128)  # Rouge clair

            elif self.rect_aller_menu.collidepoint(mouse_pos):
                c_menu = (243, 156, 18)  # Jaune clair

            # ============================================================
            # ANCIENNE MÉTHODE (TA MÉTHODE) - NE FONCTIONNE PAS BIEN
            # Problème: get_pressed() détecte si le bouton est MAINTENU enfoncé
            # Donc le clic reste actif sur plusieurs frames et plusieurs pages
            # ============================================================
            # mouse_clicked = pygame.mouse.get_pressed()
            # if self.rect_level1.collidepoint(mouse_pos):
            #     if mouse_clicked[0]:
            #         mouse_clicked = (0, 0, 0)  # ça ne réinitialise pas vraiment le clic!
            #         return "level1"
            # ============================================================


            pygame.draw.rect(self.ecran, c1, self.rect_level1, 0, 15)
            pygame.draw.rect(self.ecran, c2, self.rect_level2, 0, 15)
            pygame.draw.rect(self.ecran, c3, self.rect_level3, 0, 15)
            pygame.draw.rect(self.ecran, c4, self.rect_level4, 0, 15)
            pygame.draw.rect(self.ecran, c5, self.rect_level5, 0, 15)
            pygame.draw.rect(self.ecran, c6, self.rect_level6, 0, 15)
            pygame.draw.rect(self.ecran, c7, self.rect_level7, 0, 15)
            pygame.draw.rect(self.ecran, c8, self.rect_level8, 0, 15)
            pygame.draw.rect(self.ecran, c9, self.rect_level9, 0, 15)
            pygame.draw.rect(self.ecran, c10, self.rect_level10, 0, 15)

            pygame.draw.rect(self.ecran, c_menu, self.rect_aller_menu, 0, 20)


            self.afficher_text("Choisis ton niveau", police, (255, 255, 255), WIDTH // 2, 80)
            # self.afficher_text("M = Retour au menu", pygame.font.SysFont('Arial', 25), (200, 200, 200), WIDTH // 2, HEIGHT - 50)

            

            # Textes centrés dans les boutons (ligne 1)
            self.afficher_text("1", police, (255, 255, 255), WIDTH // 2 - 230, HEIGHT // 2 - 40)
            self.afficher_text("2", police, (255, 255, 255), WIDTH // 2 - 130, HEIGHT // 2 - 40)
            self.afficher_text("3", police, (255, 255, 255), WIDTH // 2 - 30, HEIGHT // 2 - 40)
            self.afficher_text("4", police, (255, 255, 255), WIDTH // 2 + 70, HEIGHT // 2 - 40)
            self.afficher_text("5", police, (255, 255, 255), WIDTH // 2 + 170, HEIGHT // 2 - 40)
            # Textes centrés dans les boutons (ligne 2)
            self.afficher_text("6", police, (255, 255, 255), WIDTH // 2 - 230, HEIGHT // 2 + 60)
            self.afficher_text("7", police, (255, 255, 255), WIDTH // 2 - 130, HEIGHT // 2 + 60)
            self.afficher_text("8", police, (255, 255, 255), WIDTH // 2 - 30, HEIGHT // 2 + 60)
            self.afficher_text("9", police, (255, 255, 255), WIDTH // 2 + 70, HEIGHT // 2 + 60)
            self.afficher_text("10", police, (255, 255, 255), WIDTH // 2 + 170, HEIGHT // 2 + 60)

            self.afficher_text("Retour au menu", police, (255, 255, 255), WIDTH // 2, HEIGHT - 70)

            pygame.display.flip()
            clock.tick(FPS)