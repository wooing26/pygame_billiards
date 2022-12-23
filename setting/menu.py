import pygame
from setting.config import *
#from config import *


#pygame.init()

def Main_menu(menu, play):
    global back_size
    mouse_up = (0, 0)

    pygame.display.set_caption("Main menu")

    font = pygame.font.SysFont('notosansmonocjkkrregular',100)
    img_play0 = font.render('Play', True, blue)
    img_play1 = font.render('Play', True, red)
    img_exit0 = font.render('Exit', True, blue)
    img_exit1 = font.render('Exit', True, red)

    mid = np.array([back_size[0] / 2, back_size[1] / 2])
    play_pos = [mid[0] - 65, mid[1] - 100]
    exit_pos = [mid[0] - 65, mid[1] + 100]
    
    while menu:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_up = pygame.mouse.get_pos()
        
        if (play_pos[0] <= mouse_up[0] <= play_pos[0] + 145) and (play_pos[1] <= mouse_up[1] <= play_pos[1] + 75):
            play = True
            menu = False
        if (exit_pos[0] <= mouse_up[0] <= exit_pos[0] + 145) and (exit_pos[1] <= mouse_up[1] <= exit_pos[1] + 75):
            play = False
            menu = False

        background.fill(black)
        #if mouse_pos
        play_rect = pygame.draw.rect(background, white, [play_pos[0], play_pos[1], 145, 75])
        exit_rect = pygame.draw.rect(background, white, [exit_pos[0], exit_pos[1], 145, 75])
        if (play_pos[0] <= mouse_pos[0] <= play_pos[0] + 145) and (play_pos[1] <= mouse_pos[1] <= play_pos[1] + 75):
            background.blit(img_play1, play_pos)
        else:
            background.blit(img_play0, play_pos)
        if (exit_pos[0] <= mouse_pos[0] <= exit_pos[0] + 145) and (exit_pos[1] <= mouse_pos[1] <= exit_pos[1] + 75):
            background.blit(img_exit1, exit_pos)
        else:
            background.blit(img_exit0, exit_pos)
        #pygame.draw.line(background, red, (mid[0], 0), (mid[0], back_size[1]))
        pygame.display.update()

    return play
    
#Main_menu(menu=True, play=False)
#pygame.quit()

   


