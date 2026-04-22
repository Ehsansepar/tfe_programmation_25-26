import pygame


class Login :
    def __init__(self, ecran) :
        self.ecran = ecran

    def run_login(self, ecran) :

        while True :
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    return "quit"


            self.ecran.fill((0, 150, 80))
            pygame.display.flip()
        
        