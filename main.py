import pygame
from config import WIDTH, HEIGHT, FPS
from personnage import Personnage
from sol import Sol


pygame.init()
ecran = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mon Jeu Pygame")
clock = pygame.time.Clock()
sol = Sol()
# --- LES VARIABLES DU JOUEUR ---
# On définit le joueur par des simples variables

personnage = Personnage(x=100, y=300, width=50, height=50, color=(0, 128, 255), speed=5)




running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    personnage.move()
    ecran.fill((0, 0, 0))  

    pygame.draw.rect(ecran, personnage.color, (personnage.x, personnage.y, personnage.width, personnage.height))

    sol.afficher(ecran)

    pygame.display.flip()
    clock.tick(FPS)