import pygame

# --- CONSTANTES ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Couleurs
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)      # Le Joueur
BLACK = (0, 0, 0)       # Le décor
RED = (255, 0, 0)       # Ennemi
GREEN = (0, 255, 0)     # Arrivée

# --- CLASSES ---

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Remplacer plus tard par : pygame.image.load("mario.png")
        self.image = pygame.Surface((30, 50)) 
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # Vitesse
        self.vel_y = 0
        self.speed = 5
        self.jump_power = -12
        self.gravity = 0.5
        
    def move(self, tiles):
        # On gère le mouvement et les collisions ici
        keys = pygame.key.get_pressed()
        dx = 0
        
        # 1. Mouvement horizontal
        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed
            
        self.rect.x += dx
        
        # Collision horizontale (Murs)
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if dx > 0: # J'allais vers la droite
                    self.rect.right = tile.rect.left
                if dx < 0: # J'allais vers la gauche
                    self.rect.left = tile.rect.right

        # 2. Mouvement Vertical (Saut/Gravité)
        self.vel_y += self.gravity
        self.rect.y += self.vel_y
        
        # Collision verticale (Sol/Plafond)
        self.on_ground = False
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.vel_y > 0: # Je tombe
                    self.rect.bottom = tile.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0: # Je saute et cogne le plafond
                    self.rect.top = tile.rect.bottom
                    self.vel_y = 0

    def jump(self):
        if self.on_ground:
            self.vel_y = self.jump_power

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect(topleft=(x, y))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, distance):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.start_x = x
        self.max_dist = distance
        self.direction = 1
        self.speed = 2
        
    def update(self):
        self.rect.x += self.speed * self.direction
        # Aller-retour simple
        if abs(self.rect.x - self.start_x) > self.max_dist:
            self.direction *= -1

# --- CONFIG DU NIVEAU ---
# Tu dessines ton niveau ici avec du code (C'est facile à comprendre)
# P = Player, E = Enemy, W = Wall (Mur), G = Goal (Arrivée)
LEVEL_MAP = [
    "                           ",
    "                           ",
    "                       G   ",
    "               WWW   WWWWW ",
    "             WW            ",
    " P         WW      E       ",
    "WWWWWW    WWWWWWWWWWWWWWWW ",
    "      W  W                 ",
    "      WWWW                 "
]

# --- MAIN ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Groupes de sprites
all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player = None
goal_rect = None

# Lecture de la "Carte" ci-dessus pour créer le monde
tile_size = 40
for row_index, row in enumerate(LEVEL_MAP):
    for col_index, char in enumerate(row):
        x = col_index * tile_size
        y = row_index * tile_size
        
        if char == "W":
            block = Block(x, y, tile_size, tile_size)
            walls.add(block)
            all_sprites.add(block)
        elif char == "P":
            player = Player(x, y)
            all_sprites.add(player)
        elif char == "E":
            enemy = Enemy(x, y + 10, 100) # Ennemi avec patrouille de 100px
            enemies.add(enemy)
            all_sprites.add(enemy)
        elif char == "G":
            # Juste un rect vert pour l'arrivée
            goal = Block(x, y, tile_size, tile_size)
            goal.image.fill(GREEN)
            goal_rect = goal # On garde une ref
            all_sprites.add(goal)

running = True
while running:
    clock.tick(FPS)
    
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    # Update
    player.move(walls) # On passe les murs au joueur pour qu'il vérifie les collisions
    enemies.update()
    
    # Game Logic
    if pygame.sprite.spritecollide(player, enemies, False):
        print("GAME OVER ! Toujours pas Mario...")
        player.rect.topleft = (50, 200) # Reset position

    if goal_rect and player.rect.colliderect(goal_rect.rect):
        print("GAGNÉ ! NIVEAU TERMINÉ")
        running = False

    # Draw
    screen.fill((135, 206, 235)) # Bleu ciel
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()