import numpy as np
import pygame
from setting.config import *


def Setting(menu, set):
    global back_size, screen_ratio

    pygame.display.set_caption("Setting menu")

    mid = np.array(back_size) / 2
    set_ratio = np.linspace(1, 2, 100)

    font = pygame.font.SysFont('notosansmonocjkkrregular', int(100 / screen_ratio))
    img_play0 = font.render('Back', True, blue)
    img_play1 = font.render('Back', True, red)

    exit_pos = np.array([mid[0] - 65 / screen_ratio, mid[1] + 100 / screen_ratio])

    while set:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                set = False
                menu = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = pygame.mouse.get_pos()


            background.fill(black)
            pygame.draw.rect(background, blue_green, [mid[0] / 2 - back_size[0] / screen_ratio, mid[1] / 2 - back_size[1] / screen_ratio,
            back_size[0] / screen_ratio, back_size[1] / screen_ratio])

            pygame.display.update()

    return menu, set

