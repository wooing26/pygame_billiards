import numpy as np
import pygame


# 배경 기본 설정
screen_ratio = 1
back_size = np.array([1500, 1000]) / screen_ratio


# 게임 프레임 설정
fps = pygame.time.Clock()

# 색
white = ((255,255,255))
blue = ((0,0,255))
green = ((0,255,0))
red = ((255,0,0))
black = ((0,0,0))
orange = ((255,100,10))
yellow = ((255,255,0))
blue_green = ((0,255,170))
coffee_brown =((200,190,140))
moon_glow = ((235,245,255))
light_gray = ((200,200,200))
dark_gray = ((50,50,50))




# 당구대 설정
height = 1422 / 3 / screen_ratio
width = 2844 / 3 / screen_ratio
height_out = 1730 / 3 / screen_ratio
width_out = 3120 / 3 / screen_ratio
midpoint = [back_size[0] / 2, back_size[1] * 2 / 3]


# 당구대 안에서만 공이 움직이게 크기 설정
x_lim = np.array([midpoint[0] - width / 2, midpoint[0] + width / 2])
y_lim = np.array([midpoint[1] - height / 2, midpoint[1] + height / 2])
x_out = np.array([midpoint[0] - width_out / 2, midpoint[0] + width_out / 2])
y_out = np.array([midpoint[1] - height_out / 2, midpoint[1] + height_out / 2])


# 당구대
pool_wall = np.array([x_lim, y_lim])


# 스코어 출력함수
def Score(player1, player2):
    position = [[(3 * midpoint[0] + x_out[1]) / 4, y_out[0] - 150 / screen_ratio],
     [(midpoint[0] + 3 * x_out[1]) / 4, y_out[0] - 150 / screen_ratio]]

    font = pygame.font.SysFont('notosanscjkkrblack', int(100 / screen_ratio))
    dashboard = font.render("SCORE", True, red)
    player1_score = font.render(str(player1), True, red)
    player2_score = font.render(str(player2), True, red)
    background.blit(dashboard, ((position[0][0] + position[1][0]) / 2 -100 / screen_ratio, position[0][1] - 100 / screen_ratio))
    background.blit(player1_score, (position[0]))
    background.blit(player2_score, (position[1]))



# overlap 상황 해결 프레임 조정
frame_count = [0, 0, 0]
frame_skip = 3


# 초기 속력 제한
speed_limit = 250 / screen_ratio