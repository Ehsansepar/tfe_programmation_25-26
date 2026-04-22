import pygame
import os
from data.config import WIDTH, HEIGHT, FPS
from test_personnage import Personnage

pygame.init()
ecran = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test - Mon Jeu Pygame")
clock = pygame.time.Clock()

# Background - créer une surface répétée
background = pygame.image.load("images/Background/Blue.png").convert()
fond = pygame.Surface((WIDTH, HEIGHT))
for x in range(0, WIDTH, background.get_width()):
    for y in range(0, HEIGHT, background.get_height()):
        fond.blit(background, (x, y))

# Sol avec tuiles de terrain
sol_hauteur = 50
terrain_tileset = pygame.image.load("images/Terrain/Terrain (16x16).png").convert_alpha()
# Extraire une tuile (position 96, 0 pour une belle tuile de sol)
tile_sol = terrain_tileset.subsurface((96, 0, 16, 16))
tile_sol = pygame.transform.scale(tile_sol, (50, 50))

# Personnage
personnage = Personnage(x=100, y=300, width=64, height=64, color=(0, 128, 255), speed=5)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    personnage.move()

    # Afficher le background
    ecran.blit(fond, (0, 0))

    # Afficher le personnage
    personnage.afficher(ecran)

    # Afficher le sol avec les tuiles
    for x in range(0, WIDTH, 50):
        ecran.blit(tile_sol, (x, HEIGHT - sol_hauteur))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
