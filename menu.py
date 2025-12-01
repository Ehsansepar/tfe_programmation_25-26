import pygame

from config import *



# pygame.init()
# ecran = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Mon Jeu Pygame")
# clock = pygame.time.Clock()

class Menu :

    def __init__(self, ecran):
        self.ecran = ecran
        return

    def run_menu(self) :

        # police = pygame.font.SysFont('Arial', 30)

        # def afficher_text(text, font, text_col, x, y) :
        #     img = font.render(text, True, text_col)
        #     ecran.blit(img, (x, y))


        running = True



        while running :
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "game"

            self.ecran.fill((222, 0, 0)) 
            pygame.display.flip()

