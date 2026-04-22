import pygame
from classes.session import Session
import data.save_manager as save_manager
import data.config as config

class Login:
    def __init__(self, ecran):
        self.ecran = ecran
        try:
            self.police_titre = pygame.font.SysFont('impact', 50, bold=True)
            self.police = pygame.font.SysFont('consolas', 30, bold=True)
            self.button_police = pygame.font.SysFont('consolas', 25, bold=True)
        except:
            self.police_titre = pygame.font.Font(None, 60)
            self.police = pygame.font.Font(None, 40)
            self.button_police = pygame.font.Font(None, 36)

        self.user_username = ''
        self.user_pass = ''
        
        self.rect_username = pygame.Rect(config.WIDTH // 2 - 175, 300, 350, 50)
        self.rect_password = pygame.Rect(config.WIDTH // 2 - 175, 400, 350, 50)
        self.rect_enter = pygame.Rect(config.WIDTH // 2 - 110, 500, 220, 50)
        self.rect_back = pygame.Rect(40, 40, 120, 40)

        self.rect_active_username = False
        self.rect_active_password = False
        self.show_error = False

    def afficher_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        rect = img.get_rect(center=(x, y))
        self.ecran.blit(img, rect)

    def draw_neon_rect(self, surface, color, rect, width=0, border_radius=10, neon_strength=3):
        glow_rect = rect.inflate(neon_strength*2, neon_strength*2)
        pygame.draw.rect(surface, (max(0, color[0]-150), max(0, color[1]-150), max(0, color[2]-150)), glow_rect, border_radius=border_radius+2)
        if width > 0:
            pygame.draw.rect(surface, (15, 20, 30), rect, border_radius=border_radius)
            pygame.draw.rect(surface, color, rect, width, border_radius=border_radius)
        else:
            pygame.draw.rect(surface, color, rect, border_radius=border_radius)

    def run_login(self, *args):
        clock = pygame.time.Clock()
        while True:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect_username.collidepoint(event.pos):
                        self.rect_active_username = True
                        self.rect_active_password = False
                    elif self.rect_password.collidepoint(event.pos):
                        self.rect_active_password = True
                        self.rect_active_username = False
                    else:
                        self.rect_active_username = False
                        self.rect_active_password = False

                    if self.rect_enter.collidepoint(event.pos):
                        if self.user_username != '' and self.user_pass != '':
                            if save_manager.login_user(self.user_username, self.user_pass):
                                Session.username = self.user_username
                                return "menu"
                            else:
                                self.show_error = True
                    
                    if self.rect_back.collidepoint(event.pos):
                        return "menu"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if self.rect_active_username:
                            self.user_username = self.user_username[:-1]
                        elif self.rect_active_password:
                            self.user_pass = self.user_pass[:-1]
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        if self.user_username != '' and self.user_pass != '':
                            if save_manager.login_user(self.user_username, self.user_pass):
                                Session.username = self.user_username
                                return "menu"
                            else:
                                self.show_error = True
                        else:
                            self.show_error = True
                    else:
                        if self.rect_active_username:
                            self.user_username += event.unicode
                        elif self.rect_active_password:
                            self.user_pass += event.unicode

            self.ecran.fill((15, 20, 30))

            self.afficher_text("CONNEXION", self.police_titre, (0, 255, 255), config.WIDTH // 2, 100)

            col_user = (0, 255, 255) if self.rect_active_username else (100, 100, 100)
            col_pass = (0, 255, 255) if self.rect_active_password else (100, 100, 100)

            self.afficher_text("Username", self.police, (200, 200, 200), config.WIDTH // 2, 275)
            self.draw_neon_rect(self.ecran, col_user, self.rect_username, width=3, neon_strength=3 if self.rect_active_username else 1)
            # Text uses simple blit to align left
            text_u = self.police.render(self.user_username, True, (255, 255, 255))
            self.ecran.blit(text_u, (self.rect_username.x + 10, self.rect_username.y + 10))

            self.afficher_text("Password", self.police, (200, 200, 200), config.WIDTH // 2, 375)
            self.draw_neon_rect(self.ecran, col_pass, self.rect_password, width=3, neon_strength=3 if self.rect_active_password else 1)
            password_masque = '*' * len(self.user_pass)
            text_p = self.police.render(password_masque, True, (255, 255, 255))
            self.ecran.blit(text_p, (self.rect_password.x + 10, self.rect_password.y + 10))

            # Enter Button
            hover_enter = self.rect_enter.collidepoint(mouse_pos)
            col_enter = (57, 255, 20)
            if hover_enter:
                self.draw_neon_rect(self.ecran, (200, 255, 100), self.rect_enter, width=0, neon_strength=6)
                self.afficher_text("Se connecter", self.button_police, (15, 20, 30), self.rect_enter.centerx, self.rect_enter.centery)
            else:
                self.draw_neon_rect(self.ecran, col_enter, self.rect_enter, width=3, neon_strength=3)
                self.afficher_text("Se connecter", self.button_police, col_enter, self.rect_enter.centerx, self.rect_enter.centery)

            if self.show_error:
                self.afficher_text("Identifiant ou mdp incorrect", self.button_police, (255, 23, 68), config.WIDTH // 2, 580)

            # Back Button
            hover_back = self.rect_back.collidepoint(mouse_pos)
            col_back = (255, 23, 68)
            if hover_back:
                self.draw_neon_rect(self.ecran, (255, 100, 100), self.rect_back, width=0, neon_strength=6)
                self.afficher_text("Back", self.button_police, (15, 20, 30), self.rect_back.centerx, self.rect_back.centery)
            else:
                self.draw_neon_rect(self.ecran, col_back, self.rect_back, width=3, neon_strength=2)
                self.afficher_text("Back", self.button_police, col_back, self.rect_back.centerx, self.rect_back.centery)

            pygame.display.flip()
            clock.tick(config.FPS)