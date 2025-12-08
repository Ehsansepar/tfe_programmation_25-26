import pygame
from config import WIDTH, HEIGHT, FPS
from parametre import Parametre
from personnage import Personnage
from menu import *
from gagner import Gagner
from level import Level

# Import des niveaux
from lvl.lvl01 import Lvl01
from lvl.lvl02 import Lvl02
from lvl.lvl03 import Lvl03
from lvl.lvl04 import Lvl04
from lvl.lvl05 import Lvl05
from lvl.lvl06 import Lvl06
from lvl.lvl07 import Lvl07
from lvl.lvl08 import Lvl08
from lvl.lvl09 import Lvl09
from lvl.lvl10 import Lvl10

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

page = "menu"
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
                souris_est_cliquee = [0, 0, 0]
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
        elif result == "level" :
            page = "level"


# ------------------------------------------------------------------------------


    elif page == "menu" :
        
        menu = Menu(ecran)
        result = menu.run_menu()
        
        if result == "game":
            personnage.mettre_a_pos_initiale()
            page = "game"
        elif result == "quit":
            page = "quit"
        else:
            page = result

# ------------------------------------------------------------------------------

    
    elif page == "parametre" :
        parametre = Parametre(ecran)
        result = parametre.run_parametre()
        if result == "menu":
            page = "menu"
        elif result == "quit":
            running = False


# ------------------------------------------------------------------------------


    elif page == "level" :
        level = Level(ecran)
        result = level.run_level()
        if result == "menu":
            page = "menu"
        elif result == "quit":
            running = False
        # elif result.startswith("level"): #il charche le mots en premier de phrase 
        #     # https://www.w3schools.com/python/ref_string_startswith.asp
        #     personnage.mettre_a_pos_initiale()
        #     page = result
        else :
            personnage.mettre_a_pos_initiale()
            page = result

# ------------------------------------------------------------------------------

    elif page == "level1":
        lvl = Lvl01(ecran, personnage)
        result = lvl.run()
        if result == "menu":
            page = "menu"
        elif result == "level":
            page = "level"
        elif result == "quit":
            running = False
        elif result == "win":
            page = "win"

    elif page == "level2":
        lvl = Lvl02(ecran, personnage)
        result = lvl.run()
        if result == "menu":
            page = "menu"
        elif result == "level":
            page = "level"
        elif result == "quit":
            running = False
        elif result == "win":
            page = "win"

    elif page == "level3":
        lvl = Lvl03(ecran, personnage)
        result = lvl.run()
        if result == "menu":
            page = "menu"
        elif result == "level":
            page = "level"
        elif result == "quit":
            running = False
        elif result == "win":
            page = "win"

    elif page == "level4":
        lvl = Lvl04(ecran, personnage)
        result = lvl.run()
        if result == "menu":
            page = "menu"
        elif result == "level":
            page = "level"
        elif result == "quit":
            running = False
        elif result == "win":
            page = "win"

    elif page == "level5":
        lvl = Lvl05(ecran, personnage)
        result = lvl.run()
        if result == "menu":
            page = "menu"
        elif result == "level":
            page = "level"
        elif result == "quit":
            running = False
        elif result == "win":
            page = "win"

    elif page == "level6":
        lvl = Lvl06(ecran, personnage)
        result = lvl.run()
        if result == "menu":
            page = "menu"
        elif result == "level":
            page = "level"
        elif result == "quit":
            running = False
        elif result == "win":
            page = "win"

    elif page == "level7":
        lvl = Lvl07(ecran, personnage)
        result = lvl.run()
        if result == "menu":
            page = "menu"
        elif result == "level":
            page = "level"
        elif result == "quit":
            running = False
        elif result == "win":
            page = "win"

    elif page == "level8":
        lvl = Lvl08(ecran, personnage)
        result = lvl.run()
        if result == "menu":
            page = "menu"
        elif result == "level":
            page = "level"
        elif result == "quit":
            running = False
        elif result == "win":
            page = "win"

    elif page == "level9":
        lvl = Lvl09(ecran, personnage)
        result = lvl.run()
        if result == "menu":
            page = "menu"
        elif result == "level":
            page = "level"
        elif result == "quit":
            running = False
        elif result == "win":
            page = "win"

    elif page == "level10":
        lvl = Lvl10(ecran, personnage)
        result = lvl.run()
        if result == "menu":
            page = "menu"
        elif result == "level":
            page = "level"
        elif result == "quit":
            running = False
        elif result == "win":
            page = "win"

    elif page == "quit":
        running = False

pygame.quit()