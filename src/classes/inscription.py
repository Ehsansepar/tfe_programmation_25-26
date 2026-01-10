import pygame


class Inscription :
    def __init__(self, ecran):
        self.ecran = ecran
        
        self.police = pygame.font.Font(None, 40)
        self.user_username = ''
        self.rect_username = pygame.Rect(233, 308, 353, 44)
        self.rect_username_color_border = (255, 255, 255)

        self.user_pass = ''
        self.rect_password = pygame.Rect(234, 407, 353, 44)
        self.rect_password_color_border = (255, 255, 255)
        
        self.rect_active_username = False
        self.rect_active_password = False
    

        self.rect_enter = pygame.Rect(295, 503, 219, 44)

    def afficher_text(self, text, font, text_col, x, y) :
        img = font.render(text, True, text_col)
        self.ecran.blit(img, (x, y))

    def run_inscription(self, ecran) :
        while True :
            for event in pygame.event.get() :
                if event.type == pygame.QUIT : 
                    return "quit"
                
                if event.type == pygame.MOUSEBUTTONDOWN :
                    if self.rect_username.collidepoint(event.pos) :
                        self.rect_active_username = True
                        self.rect_active_password = False

                    elif self.rect_password.collidepoint(event.pos) :
                        self.rect_active_password = True
                        self.rect_active_username = False

                    else :
                        self.rect_active_username = False
                        self.rect_active_password = False

                    if self.rect_enter.collidepoint(event.pos) :
                        print(f"""Username : {self.user_username}\nPassword : {self.user_pass}""")
                        self.user_username = ''
                        self.user_pass = ''

                

                
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_BACKSPACE :
                        if self.rect_active_username :
                            self.user_username = self.user_username[:-1]

                        elif self.rect_active_password :
                            self.user_pass = self.user_pass[:-1]

                    elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER :
                        if self.rect_active_username :
                            print("input user : ", self.user_username)
                        elif self.rect_active_password : 
                            print("input user : ", self.user_username)
                            
                    else : 
                        if self.rect_active_username :
                            self.user_username += event.unicode
                        elif self.rect_active_password :
                            self.user_pass += event.unicode


            self.ecran.fill((180, 80, 0))

            if self.rect_active_username :
                self.rect_username_color_border = (255, 255, 255)
            else : 
                self.rect_username_color_border = (190, 190, 190)

            if self.rect_active_password :
                self.rect_password_color_border = (255, 255, 255)
            else : 
                self.rect_password_color_border = (190, 190, 190)

            self.afficher_text("Username", self.police, (255, 255, 255), 236, 286)
            pygame.draw.rect(ecran, self.rect_username_color_border, self.rect_username, 2)
            text_surface = self.police.render(self.user_username, True, (255,255,255))
            ecran.blit(text_surface, (self.rect_username.x + 5, self.rect_username.y + 5))


            self.afficher_text("Password", self.police, (255, 255, 255), 237, 382)
            pygame.draw.rect(ecran, self.rect_password_color_border, self.rect_password, 2)
            password_masque = '*' * len(self.user_pass)  
            text_surface_password = self.police.render(password_masque, True, (255, 255, 255))
            ecran.blit(text_surface_password, (self.rect_password.x + 5, self.rect_password.y + 5))

            pygame.draw.rect(ecran, (50, 150, 50), self.rect_enter, 0, 20)
            self.afficher_text("S'inscrire", self.police, (255, 255, 255), 350, 515)

            pygame.display.flip()