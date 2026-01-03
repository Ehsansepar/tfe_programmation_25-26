import pygame
import sys

# Initialisation
pygame.init()
WIDTH, HEIGHT = 800, 600
ecran = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test Camera - Scrolling")
clock = pygame.time.Clock()

# === JOUEUR ===
joueur_x = 100          # Position DANS LE MONDE (pas sur l'écran)
joueur_y = 400
joueur_width = 50
joueur_height = 50
joueur_speed = 5

# === CAMERA ===
camera_x = 0            # Décalage de la caméra

# === LE MONDE (plateformes, sol, etc.) ===
# Ces positions sont dans le MONDE, pas sur l'écran
plateformes = [
    pygame.Rect(0, 500, 800, 20),      # Sol début
    pygame.Rect(800, 500, 800, 20),    # Sol suite
    pygame.Rect(1600, 500, 800, 20),   # Sol suite
    pygame.Rect(300, 400, 150, 20),    # Plateforme 1
    pygame.Rect(600, 300, 150, 20),    # Plateforme 2
    pygame.Rect(1000, 350, 150, 20),   # Plateforme 3
    pygame.Rect(1400, 250, 150, 20),   # Plateforme 4
]

# Zone d'arrivée (très loin !)
finish = pygame.Rect(2000, 450, 50, 50)

# === GRAVITÉ ===
vitesse_verticale = 0
gravite = 0.5
puissance_saut = -12
is_jumping = False

running = True
while running:
    # === EVENTS ===
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # === MOUVEMENT ===
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        joueur_x -= joueur_speed
    if keys[pygame.K_RIGHT]:
        joueur_x += joueur_speed
    if keys[pygame.K_SPACE] and not is_jumping:
        vitesse_verticale = puissance_saut
        is_jumping = True
    
    # Gravité
    vitesse_verticale += gravite
    joueur_y += vitesse_verticale
    
    # Collision avec plateformes
    joueur_rect = pygame.Rect(joueur_x, joueur_y, joueur_width, joueur_height)
    for plat in plateformes:
        if joueur_rect.colliderect(plat):
            if vitesse_verticale > 0:  # On tombe
                joueur_y = plat.y - joueur_height
                vitesse_verticale = 0
                is_jumping = False
    
    # === CAMERA : Suivre le joueur ! ===
    # La caméra se centre sur le joueur
    camera_x = joueur_x - WIDTH // 2 + joueur_width // 2
    
    # Empêcher la caméra d'aller trop à gauche
    if camera_x < 0:
        camera_x = 0
    
    # === DESSIN ===
    ecran.fill((50, 50, 80))  # Fond
    
    # Dessiner les plateformes (position MONDE - camera)
    for plat in plateformes:
        # On soustrait camera_x pour "décaler" tout
        ecran_x = plat.x - camera_x
        pygame.draw.rect(ecran, (139, 90, 43), (ecran_x, plat.y, plat.width, plat.height))
    
    # Dessiner la zone d'arrivée
    ecran_finish_x = finish.x - camera_x
    pygame.draw.rect(ecran, (0, 255, 100), (ecran_finish_x, finish.y, finish.width, finish.height))
    
    # Dessiner le joueur (position MONDE - camera)
    ecran_joueur_x = joueur_x - camera_x
    pygame.draw.rect(ecran, (0, 128, 255), (ecran_joueur_x, joueur_y, joueur_width, joueur_height))
    
    # Afficher info
    font = pygame.font.SysFont('Arial', 20)
    info = font.render(f"Position dans le monde: x={joueur_x:.0f}  |  Camera: {camera_x:.0f}", True, (255, 255, 255))
    ecran.blit(info, (10, 10))
    
    # Victoire ?
    if joueur_rect.colliderect(finish):
        win = font.render("🎉 GAGNÉ ! Tu as atteint la fin !", True, (255, 255, 0))
        ecran.blit(win, (WIDTH//2 - 150, HEIGHT//2))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
