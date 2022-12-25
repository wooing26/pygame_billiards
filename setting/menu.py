import pygame
from setting.config import *
#from config import *


#pygame.init()

def Main_menu(menu, play, set, screen_ratio):

    mouse_up = (0, 0)

    pygame.display.set_caption("Main menu")
    back_size = np.array([1500, 1000])

    back_size = back_size / screen_ratio
    background = pygame.display.set_mode(back_size)

    font = pygame.font.SysFont('notosansmonocjkkrregular', int(100 / screen_ratio))
    img_play0 = font.render('Play', True, blue)
    img_play1 = font.render('Play', True, red)
    img_set0 = font.render('Setting', True, blue)
    img_set1 = font.render('Setting', True, red)
    img_exit0 = font.render('Exit', True, blue)
    img_exit1 = font.render('Exit', True, red)

    mid = np.array([back_size[0] / 2, back_size[1] / 2])
    play_pos = np.array([mid[0] - 65 / screen_ratio, mid[1] - 100 / screen_ratio])
    setting_pos = np.array([mid[0] - 120 / screen_ratio, mid[1]])
    exit_pos = np.array([mid[0] - 65 / screen_ratio, mid[1] + 100 / screen_ratio])
    
    while menu:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                play = False
                set = False
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_up = pygame.mouse.get_pos()
        
        if (play_pos[0] <= mouse_up[0] <= play_pos[0] + 145 / screen_ratio) and (play_pos[1] <= mouse_up[1] <= play_pos[1] + 75 / screen_ratio):
            play = True
            menu = False
            set = False
        if (setting_pos[0] <= mouse_up[0] <= setting_pos[0] + 250 / screen_ratio) and (setting_pos[1] <= mouse_up[1] <= setting_pos[1] + 75 / screen_ratio):
            set = True
            menu = False
            play = False
        if (exit_pos[0] <= mouse_up[0] <= exit_pos[0] + 145 / screen_ratio) and (exit_pos[1] <= mouse_up[1] <= exit_pos[1] + 75 / screen_ratio):
            play = False
            menu = False
            set = False
        

        background.fill(black)
        #if mouse_pos
        play_rect = pygame.draw.rect(background, white, [play_pos[0], play_pos[1], 145 / screen_ratio, 75 / screen_ratio])
        set_rect = pygame.draw.rect(background, white, [setting_pos[0], setting_pos[1], 250 / screen_ratio, 75 / screen_ratio])
        exit_rect = pygame.draw.rect(background, white, [exit_pos[0], exit_pos[1], 145 / screen_ratio, 75 / screen_ratio])
        if (play_pos[0] <= mouse_pos[0] <= play_pos[0] + 145 / screen_ratio) and (play_pos[1] <= mouse_pos[1] <= play_pos[1] + 75 / screen_ratio):
            background.blit(img_play1, play_pos)
        else:
            background.blit(img_play0, play_pos)
        if (setting_pos[0] <= mouse_pos[0] <= setting_pos[0] + 250 / screen_ratio) and (setting_pos[1] <= mouse_pos[1] <= setting_pos[1] + 75 / screen_ratio):
            background.blit(img_set1, setting_pos)
        else:
            background.blit(img_set0, setting_pos)
        if (exit_pos[0] <= mouse_pos[0] <= exit_pos[0] + 145 / screen_ratio) and (exit_pos[1] <= mouse_pos[1] <= exit_pos[1] + 75 / screen_ratio):
            background.blit(img_exit1, exit_pos)
        else:
            background.blit(img_exit0, exit_pos)
        pygame.draw.line(background, red, (mid[0], 0), (mid[0], back_size[1]))
        pygame.display.update()
    

    return menu, play, set

    
#Main_menu(menu=True, play=False, set=False, screen_ratio=1)
#pygame.quit()

   


