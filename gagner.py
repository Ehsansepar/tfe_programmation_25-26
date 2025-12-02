import pygame
from config import WIDTH, HEIGHT, FPS
from personnage import Personnage
from sol import Sol

class Gagner :
    def __init__(self, ecran) :
        self.ecran = ecran

        global police
        police = pygame.font.SysFont('comicsansms', 40, bold=True)

        self.finished_rect = pygame.Rect(WIDTH-100, HEIGHT-150, 50, 100)
        
        self.rect_meunu = pygame.Rect(WIDTH // 2 - 100, 400, 200, 50)
        self.rect_quitter = pygame.Rect(WIDTH // 2 - 100, 500, 200, 50)

        self.couleur_hover = (200, 200, 200)
        return
    

    def afficher_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        rect = img.get_rect(center=(x, y))
        self.ecran.blit(img, rect)

    def run_gagner(self, personnage):

        global police
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        personnage.speed = 5
                        personnage.x = 100
                        personnage.y = 300
                        return "menu"
                    elif event.key == pygame.K_END:
                        return "quit"
            
            mouse_pos = pygame.mouse.get_pos()

            if self.rect_meunu.collidepoint(mouse_pos):

                if pygame.mouse.get_pressed()[0]:
                    personnage.speed = 5
                    personnage.x = 100
                    personnage.y = 300
                    return "menu"
                
            if self.rect_quitter.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    return "quit"
                
                elif not self.rect_meunu.collidepoint(mouse_pos) and not self.rect_quitter.collidepoint(mouse_pos):
                    print("not hover")
                    
            pygame.draw.rect(self.ecran, self.couleur_hover, self.rect_meunu)
            pygame.draw.rect(self.ecran, self.couleur_hover, self.rect_quitter)

            self.ecran.fill((34, 139, 34))


            self.afficher_text("Félicitations !", police, (255, 215, 0), WIDTH // 2, 150)
            self.afficher_text("Vous avez gagné !", police, (255, 255, 255), WIDTH // 2, 220)

            self.afficher_text("M - Retour au menu", police, (200, 200, 200), WIDTH // 2, 400)
            self.afficher_text("END - Quitter", police, (240, 113, 103), WIDTH // 2, 500)

            pygame.display.flip()