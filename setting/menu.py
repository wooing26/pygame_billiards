import pygame
#from setting.config import *
from config import *


pygame.init()

def Main_menu(menu, play):
    global back_size
    font6 = pygame.font.SysFont('notosansmonocjkkrregular',100)
    img6 = font6.render('Play',True,blue)
    mid = np.array([back_size[0] / 2, back_size[1] / 2])
    
    while menu:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_up = pygame.mouse.get_pos()
        
        background.fill(black)
        #if mouse_pos
        background.blit(img6, mid)
        pygame.display.update()

    return play
    
Main_menu(menu=True, play=False)
pygame.quit()

   


