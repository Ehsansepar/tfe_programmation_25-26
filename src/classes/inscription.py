import pygame

class Inscription :
    def __init__(self, ecran):
        self.ecran = ecran
    
    def run_inscription(self, ecran) :
        while True :
            for event in pygame.event.get() :
                if event.type == pygame.QUIT : 
                    return "quit"
            
            self.ecran.fill((180, 80, 0))
            pygame.display.flip()