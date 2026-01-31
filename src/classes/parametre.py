import pygame  
import data.config as config
import os


pygame.init()
pygame.mixer.init()


class Parametre:
    def __init__(self, ecran):
        self.ecran = ecran
        self.police_titre = pygame.font.SysFont('Arial', 50, bold=True)
        self.police_option = pygame.font.SysFont('Arial', 30)

        self.son_hover = pygame.mixer.Sound("src/sounds/gta-menu.wav")
        self.son_back = pygame.mixer.Sound("src/sounds/gta-menuOut.wav")

        self.taille_ecran_actuelle = pygame.display.get_desktop_sizes()
        # print(self.taille) 

        self.resulo_panel_ouvert = False

    def afficher_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        rect = img.get_rect(center=(x, y))
        self.ecran.blit(img, rect)

    def run_parametre(self):
        clock = pygame.time.Clock()

        memoire_bouton = ""
        is_fullScreen = False
        
        while True:
            mouse_pos = pygame.mouse.get_pos()

            rect_resolution = pygame.Rect(config.WIDTH // 2 - 150, 300, 300, 70)
            rect_retour = pygame.Rect(config.WIDTH // 2 - 150, 400, 300, 70)
            


            # le truc de popup pour les fenetre de reso
            fenetre_fond = pygame.Rect(config.WIDTH // 2 - 200, 100, 400, 660) 
            
            
            # ca c est les option on va dire
            opt_1 = pygame.Rect(config.WIDTH // 2 - 150, 140, 300, 50)   # 800x600
            opt_2 = pygame.Rect(config.WIDTH // 2 - 150, 200, 300, 50)   # 1024x768
            opt_3 = pygame.Rect(config.WIDTH // 2 - 150, 260, 300, 50)   # 1280x720
            opt_4 = pygame.Rect(config.WIDTH // 2 - 150, 320, 300, 50)   # 1366x768
            opt_5 = pygame.Rect(config.WIDTH // 2 - 150, 380, 300, 50)   # 1600x900
            opt_6 = pygame.Rect(config.WIDTH // 2 - 150, 440, 300, 50)   # 1920x1080
            opt_7 = pygame.Rect(config.WIDTH // 2 - 150, 500, 300, 50)   # 2560x1440
            opt_fullscreen = pygame.Rect(config.WIDTH // 2 - 150, 560, 300, 50) 
            opt_your_reso = pygame.Rect(config.WIDTH // 2 - 150, 620, 300, 50) # t as vu on prends direct la reso de ton ecran

            opt_fermer = pygame.Rect(config.WIDTH // 2 - 150, 690, 300, 50) 



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
                            config.WIDTH, config.HEIGHT = 800, 600
                            os.environ['SDL_VIDEO_CENTERED'] = '1' # pour centrer la fenetre https://stackoverflow.com/questions/38703791/how-do-i-place-the-pygame-screen-in-the-middle
                            self.ecran = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
                            self.resulo_panel_ouvert = False

                            if memoire_bouton != "opt_1" : 
                                self.son_hover.play()
                                memoire_bouton = "opt_1"

                        elif opt_2.collidepoint(event.pos):
                            config.WIDTH, config.HEIGHT = 1024, 768
                            os.environ['SDL_VIDEO_CENTERED'] = '1' # pour centrer la fenetre
                            self.ecran = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
                            self.resulo_panel_ouvert = False
                            is_fullScreen = False
                        
                        elif opt_3.collidepoint(event.pos):
                            config.WIDTH, config.HEIGHT = 1280, 720
                            os.environ['SDL_VIDEO_CENTERED'] = '1' # pour centrer la fenetre
                            self.ecran = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
                            self.resulo_panel_ouvert = False
                            is_fullScreen = False

                        elif opt_4.collidepoint(event.pos):
                            config.WIDTH, config.HEIGHT = 1366, 768
                            os.environ['SDL_VIDEO_CENTERED'] = '1' # pour centrer la fenetre    
                            self.ecran = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
                            self.resulo_panel_ouvert = False
                            is_fullScreen = False

                        elif opt_5.collidepoint(event.pos):
                            config.WIDTH, config.HEIGHT = 1600, 900
                            os.environ['SDL_VIDEO_CENTERED'] = '1' # pour centrer la fenetre
                            self.ecran = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
                            self.resulo_panel_ouvert = False
                            is_fullScreen = False

                        elif opt_6.collidepoint(event.pos):
                            config.WIDTH, config.HEIGHT = 1920, 1080
                            os.environ['SDL_VIDEO_CENTERED'] = '1' # pour centrer la fenetre
                            self.ecran = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
                            self.resulo_panel_ouvert = False
                            is_fullScreen = False

                        elif opt_7.collidepoint(event.pos):
                            config.WIDTH, config.HEIGHT = 2560, 1440
                            os.environ['SDL_VIDEO_CENTERED'] = '1'# pour centrer la fenetre
                            self.ecran = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
                            self.resulo_panel_ouvert = False
                            is_fullScreen = False
                        
                        elif opt_your_reso.collidepoint(event.pos):
                            config.WIDTH, config.HEIGHT = self.taille[0]
                            os.environ['SDL_VIDEO_CENTERED'] = '1'# pour centrer la fenetre
                            self.ecran = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
                            self.resulo_panel_ouvert = False
                            is_fullScreen = False

                        elif opt_fullscreen.collidepoint(event.pos) :
                            if is_fullScreen:
                                # windowed
                                os.environ['SDL_VIDEO_CENTERED'] = '1' # pour centrer la fenetre
                                self.ecran = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
                                is_fullScreen = False
                            else:
                                # fullscreen
                                self.ecran = pygame.display.set_mode((config.WIDTH, config.HEIGHT), pygame.FULLSCREEN)
                                is_fullScreen = True
                            self.resulo_panel_ouvert = False
                        
                        elif opt_fermer.collidepoint(event.pos):
                            self.resulo_panel_ouvert = False

                    else:
                        if rect_retour.collidepoint(event.pos):
                            self.son_back.play()
                            return "menu"

                        if rect_resolution.collidepoint(event.pos):
                            self.resulo_panel_ouvert = True




            
            self.ecran.fill((0, 129, 167))


        # ------------------------------------ hors de popup ca--------------------------------------------------------------------------
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
            

            self.afficher_text(f"Taille actuelle : {self.taille_ecran_actuelle[0]}x{self.taille_ecran_actuelle[1]}", self.police_option, (200, 200, 200), config.WIDTH // 2, 200)

            self.afficher_text("Changer Résolution", self.police_option, (255, 255, 255), config.WIDTH // 2, 335)
            self.afficher_text("Retour au menu", self.police_option, (255, 255, 255), config.WIDTH // 2, 435)


            # pour le popup 
            if self.resulo_panel_ouvert:

                pygame.draw.rect(self.ecran, (44, 62, 80), fenetre_fond, 0, 10)
                pygame.draw.rect(self.ecran, (255, 255, 255), fenetre_fond, 2, 10) # Bordure blanche

                # options
                pygame.draw.rect(self.ecran, (52, 152, 219), opt_1, 0, 10)
                pygame.draw.rect(self.ecran, (255, 255, 255), opt_1, 2, 10)
                self.afficher_text("800 x 600", self.police_option, (255,255,255), config.WIDTH//2, 165)

                pygame.draw.rect(self.ecran, (52, 152, 219), opt_2, 0, 10)
                pygame.draw.rect(self.ecran, (255, 255, 255), opt_2, 2, 10)
                self.afficher_text("1024 x 768", self.police_option, (255,255,255), config.WIDTH//2, 225)

                pygame.draw.rect(self.ecran, (52, 152, 219), opt_3, 0, 10)
                pygame.draw.rect(self.ecran, (255, 255, 255), opt_3, 2, 10)
                self.afficher_text("1280 x 720", self.police_option, (255,255,255), config.WIDTH//2, 285)

                pygame.draw.rect(self.ecran, (52, 152, 219), opt_4, 0, 10)
                pygame.draw.rect(self.ecran, (255, 255, 255), opt_4, 2, 10)
                self.afficher_text("1366 x 768", self.police_option, (255,255,255), config.WIDTH//2, 345)

                pygame.draw.rect(self.ecran, (52, 152, 219), opt_5, 0, 10)
                pygame.draw.rect(self.ecran, (255, 255, 255), opt_5, 2, 10)
                self.afficher_text("1600 x 900", self.police_option, (255,255,255), config.WIDTH//2, 405)

                pygame.draw.rect(self.ecran, (52, 152, 219), opt_6, 0, 10)
                pygame.draw.rect(self.ecran, (255, 255, 255), opt_6, 2, 10)
                self.afficher_text("1920 x 1080", self.police_option, (255,255,255), config.WIDTH//2, 465)

                pygame.draw.rect(self.ecran, (52, 152, 219), opt_7, 0, 10)
                pygame.draw.rect(self.ecran, (255, 255, 255), opt_7, 2, 10)
                self.afficher_text("2560 x 1440", self.police_option, (255,255,255), config.WIDTH//2, 525)
                
                pygame.draw.rect(self.ecran, (52, 152, 219), opt_your_reso, 0, 10)
                pygame.draw.rect(self.ecran, (255, 255, 255), opt_your_reso, 2, 10)
                self.afficher_text("Your resolution", self.police_option, (255, 255, 255), config.WIDTH//2, 645)

                # annulé
                pygame.draw.rect(self.ecran, (231, 76, 60), opt_fermer, 0, 10)
                pygame.draw.rect(self.ecran, (255, 255, 255), opt_fermer, 2, 10)
                self.afficher_text("Fermer", self.police_option, (255,255,255), config.WIDTH//2, 715)

            if self.resulo_panel_ouvert == True and is_fullScreen == False :
                pygame.draw.rect(self.ecran, (52, 152, 219), opt_fullscreen, 0, 10)
                pygame.draw.rect(self.ecran, (255, 255, 255), opt_fullscreen, 2, 10)
                self.afficher_text("Full Screen", self.police_option, (255, 255, 255), config.WIDTH//2, 585)
            
            elif self.resulo_panel_ouvert == True and is_fullScreen == True :
                pygame.draw.rect(self.ecran, (52, 152, 219), opt_fullscreen, 0, 10)
                pygame.draw.rect(self.ecran, (255, 255, 255), opt_fullscreen, 2, 10)
                self.afficher_text("Windowed", self.police_option, (255, 255, 255), config.WIDTH//2, 585)

                


            if self.resulo_panel_ouvert == True :
                self.son_back.set_volume(0)
                self.son_hover.set_volume(0)
            else : 
                self.son_back.set_volume(0.5)
                self.son_hover.set_volume(0.5)

            pygame.display.flip()
            clock.tick(config.FPS)