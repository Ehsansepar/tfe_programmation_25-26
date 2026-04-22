import pygame

pygame.init()
ecran = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Joueur (position dans le MONDE)
joueur_x = 100
joueur_y = 400

# Camera
camera_x = 0

# Sol (très long !)
sol = pygame.Rect(0, 500, 3000, 20)

# Arrivée (très loin)
finish = pygame.Rect(2500, 450, 50, 50)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Mouvement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        joueur_x -= 5
    if keys[pygame.K_RIGHT]:
        joueur_x += 5
    
    # === LA MAGIE : Camera suit le joueur ===
    camera_x = joueur_x - 400  # 400 = milieu de l'écran (800/2)
    if camera_x < 0:
        camera_x = 0
    
    # Dessin
    ecran.fill((50, 50, 80))
    
    # Sol (position - camera)
    pygame.draw.rect(ecran, (139, 90, 43), (sol.x - camera_x, sol.y, sol.width, sol.height))
    
    # Arrivée (position - camera)
    pygame.draw.rect(ecran, (0, 255, 0), (finish.x - camera_x, finish.y, finish.width, finish.height))
    
    # Joueur (position - camera)
    pygame.draw.rect(ecran, (0, 128, 255), (joueur_x - camera_x, joueur_y, 50, 50))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
