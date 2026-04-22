# source https://www.youtube.com/watch?v=Rvcyf4HsWiw
#adapted on my way

import pygame

pygame.init()

ecran = pygame.display.set_mode([800, 800])
police = pygame.font.Font(None, 32)

user_text = ''
rect_input = pygame.Rect(200, 200, 140, 32)
color = (255, 255, 255)

WHITE = (255, 255, 255)
couleur_active = (255, 0, 0)

rect_input_active = False

while True :
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            pygame.quit()
        
        if event.type == pygame.MOUSEBUTTONDOWN :
            if rect_input.collidepoint(event.pos) :
                rect_input_active = True
            else :
                rect_input_active = False
                

        if event.type == pygame.KEYDOWN :
            if rect_input_active == True :

                if event.key == pygame.K_BACKSPACE :
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER :
                    print('enter pressed', user_text)
                    user_text = ''
                else :
                    user_text += event.unicode
    if user_text == 'exit' :
        pygame.quit() 

        
    ecran.fill((0, 0, 0))

    if rect_input_active :
        color = couleur_active
    else :
        color = WHITE
    
    pygame.draw.rect(ecran, color, rect_input, 3)

 
    text_surface = police.render(user_text, True, (255, 255, 255))
    ecran.blit(text_surface, (rect_input.x + 5, rect_input.y + 5))

    rect_input.width = max(100, text_surface.get_width() + 30)

    pygame.display.flip()