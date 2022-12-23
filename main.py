import numpy as np
import pygame
from setting.Ball_class import *
from setting.config import *
from setting.menu import Main_menu
from setting.playing import Playing


# pygame 설정 
pygame.init()


# 공 초기 설정 (위치, 속도, 색)
ball_1 = Ball(midpoint[0], midpoint[1], 0.0, 0.0, 0.0, 0.0, 0.0, white)
ball_2 = Ball(midpoint[0] - 100 / screen_ratio, midpoint[1], 0.0, 0.0, 0.0, 0.0, 0.0, yellow)
ball_3 = Ball(x_lim[1] - 100 / screen_ratio, y_lim[0] + 100 / screen_ratio, 0.0, 0.0, 0.0, 0.0, 0.0, red)

# 게임 실행
menu, play, set = True, True, True
while True in (menu, play, set):
    menu, play = Main_menu(menu, play)
    if play:
        menu, play = Playing(ball_1, ball_2, ball_3, menu = menu, play = play)

pygame.quit()