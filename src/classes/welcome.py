
# fait deux different page de connter et inscrire 
# et relis les deux ensemble
#


import pygame 
import data.config as config

class Welcome() :
    def __init__(self, ecran):
        self.ecran = ecran

        global h1_police, button_police
        h1_police = pygame.font.Font(None, 70)
        button_police = pygame.font.Font(None, 36)

        self.rect_connecter = pygame.Rect(config.WIDTH // 2 - 230, config.HEIGHT // 2, 200, 60)
        self.rect_inscrire = pygame.Rect(config.WIDTH // 2 + 30, config.HEIGHT // 2, 200, 60)

    def afficher_text(self, text, font, text_col, x, y) :
        img = font.render(text, True, text_col)
        rect = img.get_rect(center=(x, y))
        self.ecran.blit(img, rect)

    def run_welcome(self, personnage) :
        
        while True :
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    return "quit"
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
                    if self.rect_connecter.collidepoint(event.pos) :
                        print("button connecter pressed")
                    if self.rect_inscrire.collidepoint(event.pos) :
                        print("inscrire button pressed")
                

            self.ecran.fill((0, 119, 182))
            
            self.afficher_text("Bienvenue !", h1_police, (255, 215, 0), config.WIDTH // 2, 150)
            
            pygame.draw.rect(self.ecran, (0, 150, 80), self.rect_connecter, border_radius=10)
            pygame.draw.rect(self.ecran, (180, 80, 0), self.rect_inscrire, border_radius=10)
            

            self.afficher_text("Se connecter", button_police, (255, 255, 255), self.rect_connecter.centerx, self.rect_connecter.centery)
            self.afficher_text("S'inscrire", button_police, (255, 255, 255), self.rect_inscrire.centerx, self.rect_inscrire.centery)
            
            pygame.display.flip()