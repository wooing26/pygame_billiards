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
ball_2 = Ball(midpoint[0] - 100, midpoint[1], 0.0, 0.0, 0.0, 0.0, 0.0, yellow)
ball_3 = Ball(x_lim[1] - 100, y_lim[0] + 100, 0.0, 0.0, 0.0, 0.0, 0.0, red)







menu, play = True, False

play = Main_menu(menu, play)
Playing(ball_1, ball_2, ball_3, play = play)

pygame.quit()