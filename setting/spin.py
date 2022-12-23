import numpy as np
import pygame
from setting.config import *

# 스핀용 공 설정 (UI)
spin_ball = [x_out[0] + 150, y_out[0] - 200]
spin_radius = 150

# 스핀 입력
def Get_spin(mouse_pos, v_cm):
    r_impact = [0, 0, 0]
    v_cm = v_cm / np.linalg.norm(v_cm)
    r_hat = [mouse_pos[0] - spin_ball[0], mouse_pos[1] - spin_ball[1]]
    r_impact[2] = r_hat[1]
    r_impact[0], r_impact[1] = -r_hat[0] * v_cm[1], r_hat[0] * v_cm[0]
    return np.array(r_impact) #r_impact는 큰 값