import numpy as np
import pygame
from setting.config import *
#from config import *



def Setting(menu, set):
    global back_size, screen_ratio
    mouse_up = (0, 0)
    mouse_down = (0, 0)
    drag = (0, 0)

    pygame.display.set_caption("Setting menu")
    background = pygame.display.set_mode(back_size)

    mid = np.array(back_size) / 2
    set_ratio = np.linspace(1, 2, 100)

    font = pygame.font.SysFont('notosansmonocjkkrregular', 100)
    img_back0 = font.render('Back', True, blue)
    img_back1 = font.render('Back', True, red)

    line = [mid[0] - 500, mid[0] + 500]
    back_pos = np.array([mid[0] - 85, mid[1] + 100])
    ratio_pos = np.array([line[1], mid[1] - 100])

    while set:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                set = False
                menu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_up = pygame.mouse.get_pos()
                mouse_down = (0, 0)
                drag = (0, 0)

        if np.any(mouse_down) != 0:
            drag = pygame.mouse.get_pos()

        if (back_pos[0] <= mouse_up[0] <= back_pos[0] + 165) and (back_pos[1] <= mouse_up[1] <= back_pos[1] + 60):
            set = False
            menu = True

        if (ratio_pos[0] - 15 <= mouse_down[0] <= ratio_pos[0] + 15) and (ratio_pos[1] <= mouse_down[1] <= ratio_pos[1] + 70):
            mouse_down = np.array(mouse_down)
            ratio_pos[0] = drag[0]
            if ratio_pos[0] <= line[0]:
                ratio_pos[0] = line[0]
            elif ratio_pos[0] >= line[1]:
                ratio_pos[0] = line[1]
            mouse_down[0] = ratio_pos[0]

        screen_ratio = (line[1] - ratio_pos[0]) / (line[1] - line[0]) + 1

        background.fill(black)
        pygame.draw.rect(background, blue_green, [mid[0] - back_size[0] / screen_ratio / 2, mid[1] - back_size[1] / screen_ratio / 2,
        back_size[0] / screen_ratio, back_size[1] / screen_ratio], width=5)
        
        back_rect = pygame.draw.rect(background, white, [back_pos[0], back_pos[1], 165, 60])
        
        if (back_pos[0] <= mouse_pos[0] <= back_pos[0] + 165) and (back_pos[1] <= mouse_pos[1] <= back_pos[1] + 60):
            background.blit(img_back1, back_pos)
        else:
            background.blit(img_back0, back_pos)
        
        pygame.draw.rect(background, orange, [ratio_pos[0] - 15, ratio_pos[1], 30, 70])
        pygame.draw.line(background, light_gray, (mid[0] - 500, ratio_pos[1] + 35), (mid[0] + 500, ratio_pos[1] + 35), width=4)
        pygame.draw.line(background, red, (mid[0], 0), (mid[0], back_size[1]))
        pygame.display.update()

    back_size = back_size / screen_ratio
    return menu, set, screen_ratio

#pygame.init()
#menu, set, screen_ratio = Setting(menu=True, set=True)

#pygame.quit()