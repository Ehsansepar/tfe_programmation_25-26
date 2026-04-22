import pygame
import data.config as config
from classes.session import Session
import data.save_manager as save_manager

class Level:
    def __init__(self, ecran):
        self.ecran = ecran
        try:
            self.police_titre = pygame.font.SysFont('impact', 65, bold=True)
            self.police_btn = pygame.font.SysFont('consolas', 28, bold=True)
            self.police_cadenas = pygame.font.SysFont('consolas', 45, bold=True)
        except:
            self.police_titre = pygame.font.Font(None, 70)
            self.police_btn = pygame.font.Font(None, 40)
            self.police_cadenas = pygame.font.Font(None, 60)

    def afficher_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        rect = img.get_rect(center=(x, y))
        self.ecran.blit(img, rect)

    def draw_neon_rect(self, surface, color, rect, width=0, border_radius=15, neon_strength=4):
        glow_rect = rect.inflate(neon_strength*2, neon_strength*2)
        pygame.draw.rect(surface, (max(0, color[0]-150), max(0, color[1]-150), max(0, color[2]-150)), glow_rect, border_radius=border_radius+2)
        if width > 0:
            pygame.draw.rect(surface, (15, 20, 30), rect, border_radius=border_radius)
            pygame.draw.rect(surface, color, rect, width, border_radius=border_radius)
        else:
            pygame.draw.rect(surface, color, rect, border_radius=border_radius)

    def run_level(self):
        clock = pygame.time.Clock()
        running = True
        
        # Le système lit ici le fichier JSON pour savoir à quel niveau on est
        if Session.username != '':
            user_data = save_manager.get_user_data(Session.username)
            niveau_max = user_data.get("niveau_debloque", 1) if user_data else 1
        else:
            # Si le joueur n'est pas connecté, il n'a accès qu'au niveau 1 !
            niveau_max = 1

        color_locked = (60, 60, 60)
        color_unlocked = (0, 229, 255) # Cyan neon
        color_hover = (213, 0, 249)    # Violet neon hover
        
        level_buttons = []
        # On calcule les coordonnées
        start_x = config.WIDTH // 2 - 250
        start_y = config.HEIGHT // 2 - 80
        
        for i in range(1, 11):
            row = (i - 1) // 5
            col = (i - 1) % 5
            x = start_x + col * 100
            y = start_y + row * 100
            rect = pygame.Rect(x, y, 80, 80)
            level_buttons.append({"num": i, "rect": rect})

        rect_menu = pygame.Rect(config.WIDTH // 2 - 150, config.HEIGHT - 100, 300, 60)

        while running:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        return "menu"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for btn in level_buttons:
                        if btn["rect"].collidepoint(event.pos):
                            # On autorise le clic UNIQUEMENT si le niveau est débloqué !
                            if btn["num"] <= niveau_max:
                                return f"level{btn['num']}"
                    
                    if rect_menu.collidepoint(event.pos):
                        return "menu"

            self.ecran.fill((15, 20, 30))

            self.afficher_text("SÉLECTION DE NIVEAU", self.police_titre, (255, 255, 255), config.WIDTH // 2, 80)

            if Session.username == '':
                self.afficher_text("Connectez-vous pour sauvegarder votre progression !", self.police_btn, (255, 100, 100), config.WIDTH // 2, 140)

            for btn in level_buttons:
                is_unlocked = btn["num"] <= niveau_max
                hover = btn["rect"].collidepoint(mouse_pos)
                
                if not is_unlocked:
                    # Niveau verrouillé (Grisé avec une Croix/Cadenas)
                    self.draw_neon_rect(self.ecran, color_locked, btn["rect"], width=3, neon_strength=1)
                    self.afficher_text("X", self.police_cadenas, (100, 100, 100), btn["rect"].centerx, btn["rect"].centery)
                else:
                    # Niveau déverrouillé
                    if hover:
                        self.draw_neon_rect(self.ecran, color_hover, btn["rect"], width=0, neon_strength=6)
                        self.afficher_text(str(btn["num"]), self.police_btn, (15, 20, 30), btn["rect"].centerx, btn["rect"].centery)
                    else:
                        self.draw_neon_rect(self.ecran, color_unlocked, btn["rect"], width=3, neon_strength=3)
                        self.afficher_text(str(btn["num"]), self.police_btn, color_unlocked, btn["rect"].centerx, btn["rect"].centery)

            # Bouton retour
            hover_menu = rect_menu.collidepoint(mouse_pos)
            col_menu = (255, 196, 0)
            if hover_menu:
                self.draw_neon_rect(self.ecran, (255, 255, 200), rect_menu, width=0, neon_strength=6)
                self.afficher_text("Retour au menu", self.police_btn, (15, 20, 30), rect_menu.centerx, rect_menu.centery)
            else:
                self.draw_neon_rect(self.ecran, col_menu, rect_menu, width=3, neon_strength=3)
                self.afficher_text("Retour au menu", self.police_btn, col_menu, rect_menu.centerx, rect_menu.centery)

            pygame.display.flip()
            clock.tick(config.FPS)