import pygame
from config import WIDTH, HEIGHT, FPS
from personnage import Personnage
from menu import *

from sol import Sol


pygame.init()
ecran = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mon Jeu Pygame")
clock = pygame.time.Clock()


sol = Sol(size=(WIDTH, 20), coulor=(193, 120, 90), pos_x=0, pos_y=HEIGHT-100)

personnage = Personnage(x=100, y=300, width=50, height=50, color=(0, 128, 255), speed=5)

# sol_bla = pygame.Rect(pygame.Rect(0, HEIGHT-100, WIDTH, 20))

finished_rect = pygame.Rect(pygame.Rect(WIDTH-100, HEIGHT-150, 50, 100))

def afficher_text(text, font, text_col, x, y) :
    img = font.render(text, True, text_col)
    ecran.blit(img, (x, y))


police = pygame.font.SysFont('Arial', 30)

page = "game"
running = True
while running:
    if page == "game" :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_END] : 
            running = False
        elif keys[pygame.K_m] :
            page = "menu"

        personnage.move()
        ecran.fill((0, 0, 0))  

        pygame.draw.rect(ecran, personnage.color, (personnage.x, personnage.y, personnage.width, personnage.height))


        afficher_text("END = Quitter", police, (255, 0, 0), WIDTH // 2, 10)


        pygame.draw.rect(ecran, sol.color, sol.rect)
        finished_block = pygame.draw.rect(ecran, (138, 190, 185), finished_rect)


        # if personnage.x == WIDTH-145 or personnage.y == HEIGHT-150  :
        if personnage.x + personnage.width > finished_rect.x and personnage.x < finished_rect.x + finished_rect.width and personnage.y + personnage.height > finished_rect.y and personnage.y < finished_rect.y + finished_rect.height :
            afficher_text("END = Quitter", police, (0, 255, 0), WIDTH // 2, HEIGHT // 2)
            print("done")
            personnage.speed = 0
            page = "win"
            # exit()
        # ecran.blit()

        pygame.display.flip()
        clock.tick(FPS)

    elif page == "win" :
        ecran.fill((222, 0, 0)) 
        pygame.display.flip()

        for event in pygame.event.get(): # coix pour quitter 
            if event.type == pygame.QUIT:
                running = False
        
        key = pygame.key.get_pressed()

        if key[pygame.K_END] : 
            running = False

    elif page == "menu" :
        
        menu = Menu(ecran)
        key = pygame.key.get_pressed()
        
        if key[pygame.K_m] : 
            # running = False
            page = menu.run_menu()




