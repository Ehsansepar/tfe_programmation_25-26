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
        
        # self.rect_meunu = pygame.Rect(WIDTH // 2 - 100, 400, 200, 50)
        # self.rect_quitter = pygame.Rect(WIDTH // 2 - 100, 500, 200, 50)

        # self.couleur_hover = (200, 200, 200)
        return
    

    def afficher_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        rect = img.get_rect(center=(x, y))
        self.ecran.blit(img, rect)

    def run_gagner(self, personnage):

        global police
        running = True

        while running:

            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = pygame.mouse.get_pressed()

            rect_menu = pygame.Rect(WIDTH // 2 - 100, 400, 200, 50)
            rect_quitter = pygame.Rect(WIDTH // 2 - 100, 500, 200, 50)
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        return "menu"
                    
                    elif event.key == pygame.K_END:
                        return "quit"

            self.ecran.fill((34, 139, 34))

            couleur_rect_menu = (0, 0, 0)
            couleur_rect_quitter = (255, 0, 0)


            if rect_menu.collidepoint(mouse_pos):
                couleur_rect_menu = (100, 100, 100)
                if mouse_clicked[0]:
                    print("menu clicked from gagner.py")
                    return "menu"
            
            if rect_quitter.collidepoint(mouse_pos):
                couleur_rect_quitter = (200, 0, 0)
                if mouse_clicked[0]:
                    print("quit clicked from gagner.py")
                    return "quit"


                    

            pygame.draw.rect(self.ecran, couleur_rect_menu, rect_menu)
            pygame.draw.rect(self.ecran, couleur_rect_quitter, rect_quitter)



            self.afficher_text("Félicitations !", police, (255, 215, 0), WIDTH // 2, 150)
            self.afficher_text("Vous avez gagné !", police, (255, 255, 255), WIDTH // 2, 220)

            self.afficher_text("M - Retour au menu", police, (200, 200, 200), WIDTH // 2, 400)
            self.afficher_text("END - Quitter", police, (240, 113, 103), WIDTH // 2, 500)

            
            
            
            pygame.display.flip()