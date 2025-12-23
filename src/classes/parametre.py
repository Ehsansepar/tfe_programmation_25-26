import pygame  
from data.config import WIDTH, HEIGHT, FPS

class Parametre:
    def __init__(self, ecran):
        self.ecran = ecran
        self.police_titre = pygame.font.SysFont('Arial', 50, bold=True)
        self.police_option = pygame.font.SysFont('Arial', 30)

    def afficher_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        rect = img.get_rect(center=(x, y))
        self.ecran.blit(img, rect)

    def run_parametre(self):
        clock = pygame.time.Clock()

        while True:
            mouse_pos = pygame.mouse.get_pos()

            # Bouton retour
            rect_retour = pygame.Rect(WIDTH // 2 - 150, 400, 300, 70)

            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_m:
                        return "menu"
                    if event.key == pygame.K_END:
                        return "quit"

                # Clic souris
                # if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                #     if rect_retour.collidepoint(mouse_pos):
                #         return "menu"

            # Affichage
            self.ecran.fill((30, 30, 50))


            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = pygame.mouse.get_pressed()

            if rect_retour.collidepoint(mouse_pos):
                if mouse_clicked[0]:
                    mouse_clicked = (0, 0, 0)
                    return "menu"


            # Couleur du bouton
            couleur_retour = (100, 100, 100)
            if rect_retour.collidepoint(mouse_pos):
                couleur_retour = (150, 150, 150)

            # Dessiner le bouton
            pygame.draw.rect(self.ecran, couleur_retour, rect_retour, 0, 20)

            # Textes
            self.afficher_text("Paramètres", self.police_titre, (255, 255, 255), WIDTH // 2, 80)
            self.afficher_text("Rien pour l'instant...", self.police_option, (200, 200, 200), WIDTH // 2, 200)
            self.afficher_text("Retour au menu", self.police_option, (255, 255, 255), WIDTH // 2, 435)

            pygame.display.flip()
            clock.tick(FPS)
