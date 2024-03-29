import numpy as np
import pygame
from setting.Ball_class import *
from setting.config import *
from setting.menu import Main_menu
from setting.playing import Playing
from setting.playing_cpu1 import Playing_cpu1
from setting.playing_cpu2 import Playing_cpu2
from setting.playing_cpu12 import Playing_cpu12
from setting.setting import Setting


# pygame 설정 
pygame.init()


# 공 초기 설정 (위치, 속도, 색)
ball_1 = Ball(midpoint[0], midpoint[1], 0.0, 0.0, 0.0, 0.0, 0.0, white)
ball_2 = Ball(midpoint[0] - 100, midpoint[1], 0.0, 0.0, 0.0, 0.0, 0.0, yellow)
ball_3 = Ball(x_lim[1] - 100, y_lim[0] + 100, 0.0, 0.0, 0.0, 0.0, 0.0, red)

# 게임 실행
menu, play, set = True, True, False
screen_ratio = 1
com = 0

while True in (menu, play, set):
    menu, set, screen_ratio, com = Setting(menu, set, screen_ratio, com)
    menu, play, set = Main_menu(menu, play, set, screen_ratio)
    if com == 0:
        menu, play = Playing(ball_1, ball_2, ball_3, menu=menu, play=play, screen_ratio=screen_ratio)
    elif com == 1:
        menu, play = Playing_cpu1(ball_1, ball_2, ball_3, menu=menu, play=play, screen_ratio=screen_ratio)
    elif com == 2:
        menu, play = Playing_cpu2(ball_1, ball_2, ball_3, menu=menu, play=play, screen_ratio=screen_ratio)
    else:
        menu, play = Playing_cpu12(ball_1, ball_2, ball_3, menu=menu, play=play, screen_ratio=screen_ratio)

    # 위치 초기화 용
    if not play:
        ball_1.v = np.array([0.0, 0.0])
        ball_2.v = np.array([0.0, 0.0])
        ball_3.v = np.array([0.0, 0.0])
        ball_1.pos = np.array([midpoint[0], midpoint[1]])
        ball_2.pos = np.array([midpoint[0] - 100, midpoint[1]])
        ball_3.pos = np.array([x_lim[1] - 100, y_lim[0] + 100])

pygame.quit()