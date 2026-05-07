import pygame
import os
import data.config as config

pygame.init()
pygame.mixer.init()

class Level:
    def __init__(self, ecran):
        self.ecran = ecran







        image_path = os.path.join(os.path.dirname(__file__), "..", "images", "lvls-img.jpg")
        try:
            self.image_fond = pygame.image.load(image_path).convert()
            self.image_fond = pygame.transform.scale(self.image_fond, (config.WIDTH, config.HEIGHT))
        except Exception as e:
            print(f"Error : {e}")
            self.image_fond = pygame.Surface((config.WIDTH, config.HEIGHT))
            self.image_fond.fill((25, 25, 40))

        self.rect_level1 = pygame.Rect(270, 220, 100, 80)
        self.rect_level2 = pygame.Rect(430, 220, 100, 80)
        self.rect_level3 = pygame.Rect(590, 220, 100, 80)
        self.rect_level4 = pygame.Rect(750, 220, 100, 80)
        self.rect_level5 = pygame.Rect(910, 230, 100, 80)

        self.rect_level6 = pygame.Rect(270, 390, 100, 80)
        self.rect_level7 = pygame.Rect(430, 390, 100, 80)
        self.rect_level8 = pygame.Rect(590, 390, 100, 80)
        self.rect_level9 = pygame.Rect(750, 390, 100, 80)
        self.rect_level10 = pygame.Rect(900, 370, 120, 120)

        self.rect_aller_menu = pygame.Rect(450, 600, 400, 90)

    def run_level(self):
        clock = pygame.time.Clock()
        running = True


        f = open("src/data/data.txt", "r")
        niveau_max = int(f.read())
        f.close()

        while running:
            mouse_pos = pygame.mouse.get_pos()


            if self.rect_aller_menu.collidepoint(mouse_pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

            elif self.rect_level1.collidepoint(mouse_pos):
                if 1 <= niveau_max:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)

            elif self.rect_level2.collidepoint(mouse_pos):
                if 2 <= niveau_max:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)

            elif self.rect_level3.collidepoint(mouse_pos):
                if 3 <= niveau_max:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)

            elif self.rect_level4.collidepoint(mouse_pos):
                if 4 <= niveau_max:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)

            elif self.rect_level5.collidepoint(mouse_pos):
                if 5 <= niveau_max:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)

            elif self.rect_level6.collidepoint(mouse_pos):
                if 6 <= niveau_max:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)

            elif self.rect_level7.collidepoint(mouse_pos):
                if 7 <= niveau_max:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)

            elif self.rect_level8.collidepoint(mouse_pos):
                if 8 <= niveau_max:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)

            elif self.rect_level9.collidepoint(mouse_pos):
                if 9 <= niveau_max:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)

            elif self.rect_level10.collidepoint(mouse_pos):
                if 10 <= niveau_max:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        return "menu"

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                    if self.rect_aller_menu.collidepoint(event.pos):
                        return "menu"

                    if self.rect_level1.collidepoint(event.pos) and 1 <= niveau_max:
                        return "level1"

                    if self.rect_level2.collidepoint(event.pos) and 2 <= niveau_max:
                        return "level2"

                    if self.rect_level3.collidepoint(event.pos) and 3 <= niveau_max:
                        return "level3"

                    if self.rect_level4.collidepoint(event.pos) and 4 <= niveau_max:
                        return "level4"

                    if self.rect_level5.collidepoint(event.pos) and 5 <= niveau_max:
                        return "level5"

                    if self.rect_level6.collidepoint(event.pos) and 6 <= niveau_max:
                        return "level6"

                    if self.rect_level7.collidepoint(event.pos) and 7 <= niveau_max:
                        return "level7"

                    if self.rect_level8.collidepoint(event.pos) and 8 <= niveau_max:
                        return "level8"

                    if self.rect_level9.collidepoint(event.pos) and 9 <= niveau_max:
                        return "level9"

                    if self.rect_level10.collidepoint(event.pos) and 10 <= niveau_max:
                        return "level10"

            self.ecran.blit(self.image_fond, (0, 0))

            pygame.display.flip()
            clock.tick(config.FPS)