import pygame
import data.config as config
from classes.session import Session

pygame.init()
pygame.mixer.init()

class Menu:
    def __init__(self, ecran):
        self.ecran = ecran
        try:
            self.police_titre = pygame.font.SysFont('impact', 65, bold=True)
            self.police_btn = pygame.font.SysFont('consolas', 28, bold=True)
            self.police_info = pygame.font.SysFont('consolas', 20)
        except:
            self.police_titre = pygame.font.Font(None, 70)
            self.police_btn = pygame.font.Font(None, 40)
            self.police_info = pygame.font.Font(None, 28)

    def afficher_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        rect = img.get_rect(center=(x, y))
        self.ecran.blit(img, rect)

    def draw_neon_rect(self, surface, color, rect, width=0, border_radius=15, neon_strength=4):
        # Effet d'ombre / lueur néon
        glow_rect = rect.inflate(neon_strength*2, neon_strength*2)
        pygame.draw.rect(surface, (max(0, color[0]-150), max(0, color[1]-150), max(0, color[2]-150)), glow_rect, border_radius=border_radius+2)
        
        if width > 0:
            # Intérieur sombre
            pygame.draw.rect(surface, (15, 20, 30), rect, border_radius=border_radius)
            # Bordure néon
            pygame.draw.rect(surface, color, rect, width, border_radius=border_radius)
        else:
            # Remplissage total quand survolé
            pygame.draw.rect(surface, color, rect, border_radius=border_radius)

    def run_menu(self):
        running = True
        
        btn_width = 340
        btn_height = 60
        center_x = config.WIDTH // 2
        
        # Couleurs style "Cyber Néon" !
        color_jouer = (57, 255, 20)      # Vert Néon
        color_niveaux = (213, 0, 249)    # Violet Néon
        color_param = (0, 229, 255)      # Cyan Néon
        color_quitter = (255, 23, 68)    # Rouge Néon
        
        color_connecter = (255, 196, 0)  # Jaune Doré
        color_inscrire = (255, 109, 0)   # Orange Néon

        while running:
            is_connected = Session.username != ''
            
            # Reconstruction des boutons en temps réel pour cacher login/signup si connecté
            buttons = []
            if not is_connected:
                buttons.append({"text": "1 - Se connecter", "y": 230, "color": color_connecter, "action": "login", "rect": pygame.Rect(center_x - btn_width//2, 230, btn_width, btn_height)})
                buttons.append({"text": "2 - S'inscrire", "y": 305, "color": color_inscrire, "action": "inscription", "rect": pygame.Rect(center_x - btn_width//2, 305, btn_width, btn_height)})
            else:
                buttons.append({"text": "1 - Se déconnecter", "y": 230, "color": color_connecter, "action": "logout", "rect": pygame.Rect(center_x - btn_width//2, 230, btn_width, btn_height)})
                
            buttons.append({"text": "3 - Jouer", "y": 380, "color": color_jouer, "action": "game", "rect": pygame.Rect(center_x - btn_width//2, 380, btn_width, btn_height)})
            buttons.append({"text": "4 - Niveaux", "y": 455, "color": color_niveaux, "action": "level", "rect": pygame.Rect(center_x - btn_width//2, 455, btn_width, btn_height)})
            buttons.append({"text": "5 - Paramètres", "y": 530, "color": color_param, "action": "parametre", "rect": pygame.Rect(center_x - btn_width//2, 530, btn_width, btn_height)})
            buttons.append({"text": "6 - Quitter", "y": 605, "color": color_quitter, "action": "quit", "rect": pygame.Rect(center_x - btn_width//2, 605, btn_width, btn_height)})

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_KP1] or event.unicode in ['&', '1']:
                        if is_connected:
                            Session.username = ""
                        else:
                            return "login"
                    elif event.key in [pygame.K_2, pygame.K_KP2] or event.unicode in ['é', '2']:
                        if not is_connected: return "inscription"
                    elif event.key in [pygame.K_3, pygame.K_KP3] or event.unicode in ['"', '3']:
                        return "game"
                    elif event.key in [pygame.K_4, pygame.K_KP4] or event.unicode in ["'", '4']:
                        return "level"
                    elif event.key in [pygame.K_5, pygame.K_KP5] or event.unicode in ['(', '5']:
                        return "parametre"
                    elif event.key in [pygame.K_6, pygame.K_KP6] or event.unicode in ['-', '6']:
                        return "quit"

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for btn in buttons:
                        if btn["rect"].collidepoint(event.pos):
                            if btn["action"] == "logout":
                                Session.username = "" # On déconnecte !
                            else:
                                return btn["action"]

            # --- DESSIN DU MENU ---
            # Fond sombre style Cyberpunk
            self.ecran.fill((15, 20, 30))

            mouse_pos = pygame.mouse.get_pos()

            # Textes du haut
            self.afficher_text("PROJET TFE", self.police_titre, (255, 255, 255), center_x, 90)
            
            if is_connected:
                self.afficher_text(f">>> ONLINE : {Session.username} <<<", self.police_info, (0, 255, 255), center_x, 150)
            else:
                self.afficher_text(">>> OFFLINE <<<", self.police_info, (100, 100, 120), center_x, 150)

            # Dessin de chaque bouton
            for btn in buttons:
                hover = btn["rect"].collidepoint(mouse_pos)
                
                base_col = btn["color"]
                if hover:
                    # Bouton Rempli quand survolé
                    draw_col = (min(255, int(base_col[0] * 1.1)), min(255, int(base_col[1] * 1.1)), min(255, int(base_col[2] * 1.1)))
                    self.draw_neon_rect(self.ecran, draw_col, btn["rect"], width=0, neon_strength=6)
                    text_col = (15, 20, 30) # Texte sombre
                else:
                    # Seulement les bordures quand pas survolé (style néon)
                    draw_col = base_col
                    self.draw_neon_rect(self.ecran, draw_col, btn["rect"], width=3, neon_strength=3)
                    text_col = draw_col
                
                self.afficher_text(btn["text"], self.police_btn, text_col, btn["rect"].centerx, btn["rect"].centery)

            pygame.display.flip()