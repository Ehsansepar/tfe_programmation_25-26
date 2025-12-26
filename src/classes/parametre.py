import pygame  
import data.config as config


pygame.init()
pygame.mixer.init()


class Parametre:
    def __init__(self, ecran):
        self.ecran = ecran
        self.police_titre = pygame.font.SysFont('Arial', 50, bold=True)
        self.police_option = pygame.font.SysFont('Arial', 30)

        self.son_hover = pygame.mixer.Sound("src/sounds/gta-menu.wav")
        self.son_back = pygame.mixer.Sound("src/sounds/gta-menuOut.wav")


    def afficher_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        rect = img.get_rect(center=(x, y))
        self.ecran.blit(img, rect)

    def run_parametre(self):
        clock = pygame.time.Clock()

        memoire_bouton = ""

        
        while True:
            mouse_pos = pygame.mouse.get_pos()

            # On utilise config.WIDTH pour que les boutons restent centrés si on change la taille
            rect_resolution = pygame.Rect(config.WIDTH // 2 - 150, 300, 300, 70)
            rect_retour = pygame.Rect(config.WIDTH // 2 - 150, 400, 300, 70)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_m:
                        return "menu"
                    if event.key == pygame.K_END:
                        return "quit"

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if rect_retour.collidepoint(event.pos) :
                        self.son_back.play()
                        return "menu"
                    
                    
                    if rect_resolution.collidepoint(event.pos):
                        if config.WIDTH == 800:
                            config.WIDTH = 1280
                            config.HEIGHT = 720

                        elif config.WIDTH == 1280 :

                            config.WIDTH = 1920
                            config.HEIGHT = 1080
                        else:
                            
                            config.WIDTH = 800
                            config.HEIGHT = 800

                        self.ecran = pygame.display.set_mode((config.WIDTH, config.HEIGHT))

            
            self.ecran.fill((30, 30, 50))

            couleur_retour = (100, 100, 100)
            if rect_retour.collidepoint(mouse_pos):
                couleur_retour = (150, 150, 150)

                if memoire_bouton != "retour" : 
                    self.son_hover.play()
                    memoire_bouton = "retour"
            else:
                memoire_bouton = ""


            pygame.draw.rect(self.ecran, couleur_retour, rect_retour, 0, 20)
            pygame.draw.rect(self.ecran, (255,0,0), rect_resolution, 0, 50)

            # Textes
            self.afficher_text("Paramètres", self.police_titre, (255, 255, 255), config.WIDTH // 2, 80)
            

            self.afficher_text(f"Taille actuelle : {config.WIDTH}x{config.HEIGHT}", self.police_option, (200, 200, 200), config.WIDTH // 2, 200)

            self.afficher_text("Changer Résolution", self.police_option, (255, 255, 255), config.WIDTH // 2, 335)
            self.afficher_text("Retour au menu", self.police_option, (255, 255, 255), config.WIDTH // 2, 435)

            pygame.display.flip()
            clock.tick(config.FPS)
