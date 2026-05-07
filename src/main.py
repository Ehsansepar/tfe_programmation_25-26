import pygame
from data.config import WIDTH, HEIGHT, FPS, PLAYER_SPEED
from classes.parametre import Parametre
from classes.personnage import Personnage
from classes.menu import *
from classes.gagner import Gagner
from classes.level import Level
from classes.sol import Sol
from classes.welcome import Welcome
from classes.login import Login
from classes.inscription import Inscription


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


pygame.init()
ecran = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mon Jeu Pygame")
clock = pygame.time.Clock()



sol = Sol(size=(WIDTH, 20), coulor=(193, 120, 90), pos_x=0, pos_y=HEIGHT-100)

personnage = Personnage(x=100, y=300, width=50, height=50, color=(0, 128, 255), speed=PLAYER_SPEED)

finished_rect = pygame.Rect(pygame.Rect(WIDTH-100, HEIGHT-150, 50, 100))

def afficher_text(text, font, text_col, x, y) :
    img = font.render(text, True, text_col)
    ecran.blit(img, (x, y))

def verifier_et_sauvegarder_niveau(niveau_gagne):
    nouveau_niveau = niveau_gagne + 1
    
    f = open("src/data/data.txt", "r")
    niveau_max = int(f.read())
    f.close()
    
    if nouveau_niveau > niveau_max:
        f = open("src/data/data.txt", "w")
        f.write(str(nouveau_niveau))
        f.close()

police = pygame.font.SysFont('Arial', 30)

police_pour_notre_cheat = pygame.font.SysFont('Arial', 20)

page = "menu"
niveau_actuel = 1
running = True
while running:
    if page == "game" :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_h:
                    page = "welcome"
            
                

        keys = pygame.key.get_pressed()
        if keys[pygame.K_END] : 
            running = False
        elif keys[pygame.K_m] :
            page = "menu"

        personnage.move()
        ecran.fill((0, 0, 0))  
        
        personnage.draw(ecran)
        
        afficher_text("END = Quitter", police, (255, 0, 0), WIDTH // 2, 10)

        pygame.draw.rect(ecran, sol.color, sol.rect)
        finished_block = pygame.draw.rect(ecran, (138, 190, 185), finished_rect)

        if personnage.x + personnage.width > finished_rect.x and personnage.x < finished_rect.x + finished_rect.width and personnage.y + personnage.height > finished_rect.y and personnage.y < finished_rect.y + finished_rect.height :
            afficher_text("END = Quitter", police, (0, 255, 0), WIDTH // 2, HEIGHT // 2)
            print("done")
            personnage.speed = 0
            page = "win"

        pygame.display.flip()
        clock.tick(FPS)


# ------------------------------------------------------------------------------

    elif page == "welcome" :
        page_welcome = Welcome(ecran)
        result = page_welcome.run_welcome(personnage)
        if result == "quit" :
            running = False
        elif result == "back" :
            page = "menu"

        elif result == "login" :
            page = "login"
        elif result == "inscription" :
            page = "inscription"
    
    elif page == "login" :
        page_login = Login(ecran)
        result = page_login.run_login(personnage)
        if result == "quit" :
            running = False

    elif page == "inscription" :
        page_inscription = Inscription(ecran) 
        result = page_inscription.run_inscription(ecran)
        if result == "quit" :
            running = False
        elif result == "welcome" :
            page = "welcome"
        elif result == "menu" :
            page = "menu"
            

    elif page == "win" :
        page_gagner = Gagner(ecran, niveau_termine=niveau_actuel)
        result = page_gagner.run_gagner(personnage)
        if result == "quit":
            running = False
        elif result == "menu":
            page = "menu"
        elif result and result.startswith("level"):
            personnage.mettre_a_pos_initiale()
            page = result


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
        else :
            personnage.mettre_a_pos_initiale()
            niveau_actuel = int(result.replace("level", ""))
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
            verifier_et_sauvegarder_niveau(1)
            niveau_actuel = 1
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
            verifier_et_sauvegarder_niveau(2)
            niveau_actuel = 2
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
            verifier_et_sauvegarder_niveau(3)
            niveau_actuel = 3
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
            niveau_actuel = 4
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
            niveau_actuel = 5
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
            niveau_actuel = 6
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
            niveau_actuel = 7
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
            niveau_actuel = 8
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
            niveau_actuel = 9
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
            niveau_actuel = 10
            page = "win"

    elif page == "quit":
        running = False

pygame.quit()
