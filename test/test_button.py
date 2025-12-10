import pygame
import sys

# 1. Initialisation de base
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Mon Premier Bouton")

# 2. Définition des couleurs (Rouge, Vert, Blanc)
BLANC = (255, 255, 255)
GRIS = (200, 200, 200)
ROUGE = (255, 0, 0)
NOIR = (0, 0, 0)

# 3. Police d'écriture pour le texte du bouton
font = pygame.font.SysFont('Arial', 40)

# --- CRÉATION DU BOUTON ---
# On crée un rectangle invisible (x=300, y=250, largeur=200, hauteur=100)
bouton_rect = pygame.Rect(300, 250, 200, 100)
texte_bouton = font.render('Clique !', True, NOIR)

# Pour centrer le texte dans le bouton (un peu de maths auto)
texte_rect = texte_bouton.get_rect(center=bouton_rect.center)

running = True
while running:
    screen.fill(BLANC) # Fond blanc

    # --- LOGIQUE DU BOUTON ---
    # On récupère la position de la souris
    mouse_pos = pygame.mouse.get_pos()

    # On vérifie si la souris touche le rectangle du bouton
    # collidepoint = "est-ce que le point touche ?"
    if bouton_rect.collidepoint(mouse_pos):
        couleur_bouton = ROUGE # Si on survole, il devient rouge
        
        # On vérifie si on clique (0 = clic gauche)
        if pygame.mouse.get_pressed()[0]:
            print("BRAVO ! Tu as cliqué sur le bouton !")
    else:
        couleur_bouton = GRIS # Sinon il reste gris

    # --- DESSIN ---
    # 1. On dessine le rectangle
    pygame.draw.rect(screen, couleur_bouton, bouton_rect)
    # 2. On dessine le texte par-dessus
    screen.blit(texte_bouton, texte_rect)

    # Gestion de la fermeture de la fenêtre
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
sys.exit()