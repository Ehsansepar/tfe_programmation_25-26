

from os import name

import pygame

from config import WIDTH, HEIGHT, FPS

class Level:
    def __init__(self, ecran):
        self.ecran = ecran

        global police
        police = pygame.font.SysFont('comicsansms', 40, bold=True)

        #essaye de mettre des position bien pour les niveaux

        self.rect_level1 = pygame.Rect(WIDTH // 2 - 550, HEIGHT // 2 - 25, 100, 50)
        self.rect_level2 = pygame.Rect(WIDTH // 2 - 450, HEIGHT // 2 - 25, 100, 50)
        self.rect_level3 = pygame.Rect(WIDTH // 2 - 350, HEIGHT // 2 - 25, 100, 50)
        self.rect_level4 = pygame.Rect(WIDTH // 2 - 250, HEIGHT // 2 - 25, 100, 50)
        self.rect_level5 = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 25, 100, 50)
        self.rect_level6 = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50)
        self.rect_level7 = pygame.Rect(WIDTH // 2 + 50, HEIGHT // 2 - 25, 100, 50)
        self.rect_level8 = pygame.Rect(WIDTH // 2 + 150, HEIGHT // 2 - 25, 100, 50)
        self.rect_level9 = pygame.Rect(WIDTH // 2 + 250, HEIGHT // 2 - 25, 100, 50)
        self.rect_level10 = pygame.Rect(WIDTH // 2 + 350, HEIGHT // 2 - 25, 100, 50)

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
                    
            self.ecran.fill((135, 206, 235))  # Couleur de fond (ciel bleu)


            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = pygame.mouse.get_pressed()

            couleuir_level = (100, 149, 237)  # Bleu clair


            #hover
            if self.rect_level1.collidepoint(mouse_pos):
                couleuir_level = (65, 105, 225)  # Bleu plus foncé
                if mouse_clicked[0]:
                    mouse_clicked = (0, 0, 0)
                    return "level1"
            elif self.rect_level2.collidepoint(mouse_pos):
                couleuir_level = (65, 105, 225)  # Bleu plus foncé
                if mouse_clicked[0]:
                    mouse_clicked = (0, 0, 0)
                    return "level2"
            elif self.rect_level3.collidepoint(mouse_pos):
                couleuir_level = (65, 105, 225)  # Bleu plus foncé
                if mouse_clicked[0]:
                    mouse_clicked = (0, 0, 0)
                    return "level3"
            elif self.rect_level4.collidepoint(mouse_pos):
                couleuir_level = (65, 105, 225)  # Bleu plus foncé
                if mouse_clicked[0]:
                    mouse_clicked = (0, 0, 0)
                    return "level4"
            elif self.rect_level5.collidepoint(mouse_pos):
                couleuir_level = (65, 105, 225)  # Bleu plus foncé
                if mouse_clicked[0]:
                    mouse_clicked = (0, 0, 0)
                    return "level5"
            elif self.rect_level6.collidepoint(mouse_pos):
                couleuir_level = (65, 105, 225)  # Bleu plus foncé
                if mouse_clicked[0]:
                    mouse_clicked = (0, 0, 0)
                    return "level6"
            elif self.rect_level7.collidepoint(mouse_pos):
                couleuir_level = (65, 105, 225)  # Bleu plus foncé
                if mouse_clicked[0]:
                    mouse_clicked = (0, 0, 0)
                    return "level7"
            elif self.rect_level8.collidepoint(mouse_pos):
                couleuir_level = (65, 105, 225)  # Bleu plus foncé
                if mouse_clicked[0]:
                    mouse_clicked = (0, 0, 0)
                    return "level8"
            elif self.rect_level9.collidepoint(mouse_pos):
                couleuir_level = (65, 105, 225)  # Bleu plus foncé
                if mouse_clicked[0]:
                    mouse_clicked = (0, 0, 0)
                    return "level9"
            elif self.rect_level10.collidepoint(mouse_pos):
                couleuir_level = (65, 105, 225)  # Bleu plus foncé
                if mouse_clicked[0]:
                    mouse_clicked = (0, 0, 0)
                    return "level10"


            pygame.draw.rect(self.ecran, couleuir_level, self.rect_level1)
            pygame.draw.rect(self.ecran, couleuir_level, self.rect_level2)
            pygame.draw.rect(self.ecran, couleuir_level, self.rect_level3)
            pygame.draw.rect(self.ecran, couleuir_level, self.rect_level4)
            pygame.draw.rect(self.ecran, couleuir_level, self.rect_level5)
            pygame.draw.rect(self.ecran, couleuir_level, self.rect_level6)
            pygame.draw.rect(self.ecran, couleuir_level, self.rect_level7)
            pygame.draw.rect(self.ecran, couleuir_level, self.rect_level8)
            pygame.draw.rect(self.ecran, couleuir_level, self.rect_level9)
            pygame.draw.rect(self.ecran, couleuir_level, self.rect_level10)


            self.afficher_text("Appuyez sur M pour retourner au menu", police, (255, 0, 0), WIDTH // 2, 10)

        #essaye de mettre des position bien pour les niveaux

            self.afficher_text("1", police, (0, 0, 0), WIDTH // 2 - 550, HEIGHT // 2)
            self.afficher_text("2", police, (0, 0, 0), WIDTH // 2 - 450, HEIGHT // 2)
            self.afficher_text("3", police, (0, 0, 0), WIDTH // 2 - 350, HEIGHT // 2)
            self.afficher_text("4", police, (0, 0, 0), WIDTH // 2 - 250, HEIGHT // 2)
            self.afficher_text("5", police, (0, 0, 0), WIDTH // 2 - 150, HEIGHT // 2)
            self.afficher_text("6", police, (0, 0, 0), WIDTH // 2 - 50, HEIGHT // 2)
            self.afficher_text("7", police, (0, 0, 0), WIDTH // 2 + 50, HEIGHT // 2)
            self.afficher_text("8", police, (0, 0, 0), WIDTH // 2 + 150, HEIGHT // 2)
            self.afficher_text("9", police, (0, 0, 0), WIDTH // 2 + 250, HEIGHT // 2)
            self.afficher_text("10", police, (0, 0, 0), WIDTH // 2 + 350, HEIGHT // 2)

            pygame.display.flip()
            clock.tick(FPS)