import pygame
from config import WIDTH, HEIGHT, FPS
from personnage import Personnage
from menu import *
from gagner import Gagner

from sol import Sol


pygame.init()
ecran = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mon Jeu Pygame")
clock = pygame.time.Clock()


sol = Sol(size=(WIDTH, 20), coulor=(193, 120, 90), pos_x=0, pos_y=HEIGHT-100)

personnage = Personnage(x=100, y=300, width=50, height=50, color=(0, 128, 255), speed=5)

finished_rect = pygame.Rect(pygame.Rect(WIDTH-100, HEIGHT-150, 50, 100))

def afficher_text(text, font, text_col, x, y) :
    img = font.render(text, True, text_col)
    ecran.blit(img, (x, y))


police = pygame.font.SysFont('Arial', 30)

police_pour_notre_cheat = pygame.font.SysFont('Arial', 20)

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

        # === CHEAT CODE ICI (dans le bon endroit) ===
        pos_souris = pygame.mouse.get_pos()
        souris_est_cliquee = pygame.mouse.get_pressed()

        if finished_block.collidepoint(pos_souris):
            pygame.draw.rect(ecran, (100, 255, 0), finished_block)
            afficher_text("Ne triche pas, flemmard ! ", police_pour_notre_cheat, (255, 100, 100), WIDTH // 2 - 150, HEIGHT // 2 - 50)
            afficher_text("c est just pour tester gagner.py j ai flemme de faire tout le temps gagner ! 🤣", police_pour_notre_cheat, (255, 100, 100), WIDTH // 2 - 350, HEIGHT // 2 - 100)
            if souris_est_cliquee[0]:
                page = "win"
        # === FIN DU CHEAT CODE ===

        if personnage.x + personnage.width > finished_rect.x and personnage.x < finished_rect.x + finished_rect.width and personnage.y + personnage.height > finished_rect.y and personnage.y < finished_rect.y + finished_rect.height :
            afficher_text("END = Quitter", police, (0, 255, 0), WIDTH // 2, HEIGHT // 2)
            print("done")
            personnage.speed = 0
            page = "win"

        pygame.display.flip()
        clock.tick(FPS)


# ------------------------------------------------------------------------------


    elif page == "win" :
        page_gagner = Gagner(ecran)
        result = page_gagner.run_gagner(personnage)
        if result == "quit":
            running = False
        elif result == "menu":
            page = "menu"


# ------------------------------------------------------------------------------


    elif page == "menu" :
        
        menu = Menu(ecran)
        page = menu.run_menu()


# ------------------------------------------------------------------------------


    elif page == "quit" :
        running = False

