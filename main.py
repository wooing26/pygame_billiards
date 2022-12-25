import numpy as np
import pygame
from setting.Ball_class import *
from setting.config import *
from setting.menu import Main_menu
from setting.playing import Playing
from setting.setting import Setting


# pygame 설정 
pygame.init()


# 공 초기 설정 (위치, 속도, 색)
ball_1 = Ball(midpoint[0], midpoint[1], 0.0, 0.0, 0.0, 0.0, 0.0, white)
ball_2 = Ball(midpoint[0] - 100 / screen_ratio, midpoint[1], 0.0, 0.0, 0.0, 0.0, 0.0, yellow)
ball_3 = Ball(x_lim[1] - 100 / screen_ratio, y_lim[0] + 100 / screen_ratio, 0.0, 0.0, 0.0, 0.0, 0.0, red)

# 게임 실행
menu, play, set = True, True, False

while True in (menu, play, set):
    print("1", menu, play, set)
    menu, play, set = Main_menu(menu, play, set, screen_ratio)
    menu, set, screen_ratio = Setting(menu, set)
    menu, play = Playing(ball_1, ball_2, ball_3, menu=menu, play=play, screen_ratio=screen_ratio)
    print("3", menu, play, set)

    # 위치 초기화 용
    if not play:
        ball_1.v = np.array([0.0, 0.0])
        ball_2.v = np.array([0.0, 0.0])
        ball_3.v = np.array([0.0, 0.0])
        ball_1.pos = np.array([midpoint[0], midpoint[1]])
        ball_2.pos = np.array([midpoint[0] - 100 / screen_ratio, midpoint[1]])
        ball_3.pos = np.array([x_lim[1] - 100 / screen_ratio, y_lim[0] + 100 / screen_ratio])

pygame.quit()