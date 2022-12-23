import pygame
from config import *



def Main_menu(menu, play):
    
    while menu:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                play = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = pygame.mouse.get_pos()
            
        background.fill(black)
        pygame.display.update()

    return play
    


   


