import pygame
import data.config as config


pygame.init()

class Personnage:
    def __init__(self, x, y, width, height, color, speed):
        self.x = float(x)   # On utilise float pour la précision du delta time
        self.y = float(y)
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed  # Ignoré maintenant, on utilise config.PLAYER_SPEED

        self.vitesse_verticale = 0.0
        self.is_jumping = False

        self.player_rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)

        try:
            self.son_jump = pygame.mixer.Sound("src/sounds/jump.wav")
            self.son_jump.set_volume(0.5)
        except:
            self.son_jump = None

    def move(self, dt=0.016):
        """
        dt = delta time en secondes (temps depuis la dernière frame).
        Toutes les vitesses sont en PIXELS PAR SECONDE.
        Résultat : le jeu est identique sur Windows, Mac et Linux !
        """
        keys = pygame.key.get_pressed()

        # Conversion des touches configurables en codes pygame
        try:
            touche_gauche = pygame.key.key_code(config.gauche)
            touche_droite = pygame.key.key_code(config.droite)
            touche_haut   = pygame.key.key_code(config.haut)
            touche_bas    = pygame.key.key_code(config.bas)
            touche_saut   = pygame.key.key_code(config.saut)
        except:
            touche_gauche = pygame.K_q
            touche_droite = pygame.K_d
            touche_haut   = pygame.K_z
            touche_bas    = pygame.K_s
            touche_saut   = pygame.K_SPACE

        # Mouvement horizontal (pixels/s * secondes = pixels)
        if keys[touche_gauche] or keys[pygame.K_LEFT]:
            self.x -= config.PLAYER_SPEED * dt
        if keys[touche_droite] or keys[pygame.K_RIGHT]:
            self.x += config.PLAYER_SPEED * dt

        # Saut
        if keys[touche_haut] or keys[touche_saut] or keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            self.jump()

        # Gravité (accélération : pixels/s² * secondes = pixels/s)
        self.vitesse_verticale += config.PLAYER_GRAVITY * dt
        self.y += self.vitesse_verticale * dt

        # Sol
        ground_y = config.HEIGHT - 100 - self.height
        if self.y >= ground_y:
            self.y = ground_y
            self.vitesse_verticale = 0
            self.is_jumping = False

        self.player_rect.x = int(self.x)
        self.player_rect.y = int(self.y)

    def jump(self):
        if not self.is_jumping:
            if self.son_jump:
                self.son_jump.play()
            self.vitesse_verticale = config.PLAYER_JUMP
            self.is_jumping = True

    def mettre_a_pos_initiale(self):
        self.x = 100.0
        self.y = 300.0
        self.vitesse_verticale = 0
        self.is_jumping = False

    def verifier_platforme(self, plateformes):
        for plat in plateformes:
            if self.player_rect.colliderect(plat):
                if self.vitesse_verticale > 0:
                    self.y = plat.y - self.height
                    self.vitesse_verticale = 0
                    self.is_jumping = False
                    self.player_rect.y = int(self.y)