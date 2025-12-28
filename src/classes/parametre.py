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


        self.resulo_panel_ouvert = False

    def afficher_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        rect = img.get_rect(center=(x, y))
        self.ecran.blit(img, rect)

    def run_parametre(self):
        clock = pygame.time.Clock()

        memoire_bouton = ""

        
        while True:
            mouse_pos = pygame.mouse.get_pos()

            rect_resolution = pygame.Rect(config.WIDTH // 2 - 150, 300, 300, 70)
            rect_retour = pygame.Rect(config.WIDTH // 2 - 150, 400, 300, 70)


            # le truc de popup pour les fenetre de reso
            fenetre_fond = pygame.Rect(config.WIDTH // 2 - 200, 150, 400, 400)
            
            # ca c est les option on va dire
            opt_1 = pygame.Rect(config.WIDTH // 2 - 150, 200, 300, 50) 
            opt_2 = pygame.Rect(config.WIDTH // 2 - 150, 280, 300, 50) 
            opt_3 = pygame.Rect(config.WIDTH // 2 - 150, 360, 300, 50) 
            opt_fermer = pygame.Rect(config.WIDTH // 2 - 150, 460, 300, 50) 


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_m:
                        return "menu"
                    if event.key == pygame.K_END:
                        return "quit"

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.resulo_panel_ouvert:
                        if opt_1.collidepoint(event.pos):
                            config.WIDTH, config.HEIGHT = 800, 800
                            self.ecran = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
                            self.resulo_panel_ouvert = False

                        elif opt_2.collidepoint(event.pos):
                            config.WIDTH, config.HEIGHT = 1280, 720
                            self.ecran = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
                            self.resulo_panel_ouvert = False
                        
                        elif opt_3.collidepoint(event.pos):
                            config.WIDTH, config.HEIGHT = 1920, 1080
                            self.ecran = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
                            self.resulo_panel_ouvert = False
                        
                        elif opt_fermer.collidepoint(event.pos):
                            self.resulo_panel_ouvert = False

                    else:
                        if rect_retour.collidepoint(event.pos):
                            self.son_back.play()
                            return "menu"

                        if rect_resolution.collidepoint(event.pos):
                            self.resulo_panel_ouvert = True

                        

                    


                    # if rect_resolution.collidepoint(event.pos):
                    #     if config.WIDTH == 800:
                    #         config.WIDTH = 1024
                    #         config.HEIGHT = 768

                    #     elif config.WIDTH == 1024:
                    #         config.WIDTH = 1280
                    #         config.HEIGHT = 720

                    #     elif config.WIDTH == 1280:
                    #         config.WIDTH = 1366
                    #         config.HEIGHT = 768

                    #     elif config.WIDTH == 1366:
                    #         config.WIDTH = 1600
                    #         config.HEIGHT = 900
                        
                    #     elif config.WIDTH == 1600:
                    #         config.WIDTH = 1920
                    #         config.HEIGHT = 1080
                        
                    #     elif config.WIDTH == 1920:
                    #         config.WIDTH = 2560
                    #         config.HEIGHT = 1440
                        
                    #     else:
                    #         config.WIDTH = 800
                    #         config.HEIGHT = 800

                    #     self.ecran = pygame.display.set_mode((config.WIDTH, config.HEIGHT))



            
            self.ecran.fill((0, 129, 167))

            couleur_retour = (231, 76, 60)
            if rect_retour.collidepoint(mouse_pos):
                couleur_retour = (236, 112, 99)

                if memoire_bouton != "retour" : 
                    self.son_hover.play()
                    memoire_bouton = "retour"
            
            couleur_resolution = (52, 152, 219)
            if rect_resolution.collidepoint(mouse_pos):
                couleur_resolution = (93, 173, 226)

                if memoire_bouton != "resolution" : 
                    self.son_hover.play()
                    memoire_bouton = "resolution"

            if not (rect_retour.collidepoint(mouse_pos) or rect_resolution.collidepoint(mouse_pos)):
                memoire_bouton = ""


            pygame.draw.rect(self.ecran, couleur_retour, rect_retour, 0, 20)
            pygame.draw.rect(self.ecran, couleur_resolution, rect_resolution, 0, 50)

            # Textes
            self.afficher_text("Paramètres", self.police_titre, (253, 252, 220), config.WIDTH // 2, 80)
            

            self.afficher_text(f"Taille actuelle : {config.WIDTH}x{config.HEIGHT}", self.police_option, (200, 200, 200), config.WIDTH // 2, 200)

            self.afficher_text("Changer Résolution", self.police_option, (255, 255, 255), config.WIDTH // 2, 335)
            self.afficher_text("Retour au menu", self.police_option, (255, 255, 255), config.WIDTH // 2, 435)


            # pour le popup 
            if self.resulo_panel_ouvert:
                pygame.draw.rect(self.ecran, (44, 62, 80), fenetre_fond, 0, 10)
                pygame.draw.rect(self.ecran, (255, 255, 255), fenetre_fond, 2, 10) # Bordure blanche

                # options
                pygame.draw.rect(self.ecran, (52, 152, 219), opt_1, 0, 10)
                pygame.draw.rect(self.ecran, (255, 255, 255), opt_1, 2, 10)
                self.afficher_text("800 x 800", self.police_option, (255,255,255), config.WIDTH//2, 225)

                pygame.draw.rect(self.ecran, (52, 152, 219), opt_2, 0, 10)
                pygame.draw.rect(self.ecran, (255, 255, 255), opt_2, 2, 10)
                self.afficher_text("1280 x 720", self.police_option, (255,255,255), config.WIDTH//2, 305)


                pygame.draw.rect(self.ecran, (52, 152, 219), opt_3, 0, 10)
                pygame.draw.rect(self.ecran, (255, 255, 255), opt_3, 2, 10)
                self.afficher_text("1920 x 1080", self.police_option, (255,255,255), config.WIDTH//2, 385)

                # annulé
                pygame.draw.rect(self.ecran, (231, 76, 60), opt_fermer,0, 10)
                pygame.draw.rect(self.ecran, (255, 255, 255), opt_fermer, 2, 10)
                self.afficher_text("Fermer", self.police_option, (255,255,255), config.WIDTH//2, 485)

            pygame.display.flip()
            clock.tick(config.FPS)
