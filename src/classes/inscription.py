import pygame


class Inscription :
    def __init__(self, ecran):
        self.ecran = ecran
        
        self.police = pygame.font.Font(None, 40)
        self.user_username = ''
        self.rect_username = pygame.Rect(233, 311, 353, 44)
        self.rect_username_color_border = (255, 255, 255)

        self.user_pass = ''
        self.rect_password = pygame.Rect(233, 370, 353, 44)
        self.rect_password_color_border = (255, 255, 255)
        
        self.rect_active_username = False
        self.rect_active_password = False

    def run_inscription(self, ecran) :
        while True :
            for event in pygame.event.get() :
                if event.type == pygame.QUIT : 
                    return "quit"
                
                if event.type == pygame.MOUSEBUTTONDOWN :
                    if self.rect_username.collidepoint(event.pos) :
                        self.rect_active_username = True

                    elif self.rect_password.collidepoint(event.pos) :
                        self.rect_active_password = True

                    else :
                        self.rect_active_username = False
                        self.rect_active_password = False
                
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_BACKSPACE :
                        if self.rect_active_username :
                            self.user_username = self.user_username[:-1]
                        
                        elif self.rect_active_password :
                            self.user_pass = self.user_pass[:-1]

                    elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER :
                        print("input user : ", self.user_username)

                    else : 
                        self.user_username += event.unicode
            self.ecran.fill((180, 80, 0))

            if self.rect_active :
                self.rect_username_color_border = (255, 255, 255)
                self.rect_password_color_border = (255, 255, 255)
            else : 
                self.rect_username_color_border = (190, 190, 190)
                self.rect_password_color_border = (190, 190, 190)

            pygame.draw.rect(ecran, self.rect_username_color_border, self.rect_username, 3)
            
            text_surface = self.police.render(self.user_username, True, (255,255,255))
            ecran.blit(text_surface, (self.rect_username.x + 5, self.rect_username.y + 5))

            pygame.draw.rect(ecran, self.rect_password_color_border, self.rect_password)

            pygame.display.flip()