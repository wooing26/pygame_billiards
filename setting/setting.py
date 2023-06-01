import numpy as np
import pygame
from setting.config import *
#from config import *


def Setting(menu, set, screen_ratio, com):
    global back_size
    mouse_up = (0, 0)
    mouse_down = (0, 0)
    drag = (0, 0)

    pygame.display.set_caption("Setting menu")
    background = pygame.display.set_mode(back_size)

    # 중간 지점
    mid = np.array(back_size) / 2

    # 폰트
    font = pygame.font.SysFont('notosansmonocjkkrregular', 100)
    font_com = pygame.font.SysFont('notosansmonocjkkrregular', 50)
    img_back0 = font.render('Back', True, blue)
    img_back1 = font.render('Back', True, red)
    img_CPU = font.render('CPU', True, white)
    img_1p = font_com.render('1P', True, white)
    img_2p = font_com.render('2P', True, white)

    # 그림 좌표
    line = [mid[0] - 500, mid[0] + 500]
    back_pos = np.array([mid[0] - 85, mid[1] + 200])
    ratio_pos = np.array([line[1], mid[1] - 150])
    CPU_pos = np.array([mid[0] - 75, mid[1] -50])

    while set:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                set = False
                menu = False
                play = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_up = pygame.mouse.get_pos()
                mouse_down = (0, 0)
                drag = (0, 0)

        # 마우스 드래그 값 받기
        if np.any(mouse_down) != 0:
            drag = pygame.mouse.get_pos()

        # Back 버튼 누르는 상황
        if (back_pos[0] <= mouse_up[0] <= back_pos[0] + 165) and (back_pos[1] <= mouse_up[1] <= back_pos[1] + 60):
            set = False
            menu = True
            play = False

        # 화면비율 상자 좌우 이동
        if (ratio_pos[0] - 15 <= mouse_down[0] <= ratio_pos[0] + 15) and (ratio_pos[1] <= mouse_down[1] <= ratio_pos[1] + 70):
            mouse_down = np.array(mouse_down)
            ratio_pos[0] = drag[0]
            if ratio_pos[0] <= line[0]:
                ratio_pos[0] = line[0]
            elif ratio_pos[0] >= line[1]:
                ratio_pos[0] = line[1]
            mouse_down[0] = ratio_pos[0]

        # 화면 비율 계산
        screen_ratio = (line[1] - ratio_pos[0]) / (line[1] - line[0]) + 1

        # 컴퓨터 설정
        # 1p
        if (mid[0] - 150 <= mouse_up[0] <= mid[0] - 100) and (CPU_pos[1] + 150 <= mouse_up[1] <= CPU_pos[1] + 200):
            if com & 1 == 1:
                com -= 1
            else:
                com += 1
            mouse_up = (0, 0)
        # 2p
        if (mid[0] + 100 <= mouse_up[0] <= mid[0] + 150) and (CPU_pos[1] + 150 <= mouse_up[1] <= CPU_pos[1] + 200):
            if com & 2 == 2:
                com -= 2
            else:
                com += 2
            mouse_up = (0, 0)
            

        background.fill(black)

        # 화면 크기 실제 사이즈 박스 그리기
        pygame.draw.rect(background, blue_green, [mid[0] - back_size[0] / screen_ratio / 2, mid[1] - back_size[1] / screen_ratio / 2,
        back_size[0] / screen_ratio, back_size[1] / screen_ratio], width=5)
        
        back_rect = pygame.draw.rect(background, white, [back_pos[0], back_pos[1], 165, 60])
        
        # Back 버튼 범위 별로 색 다르게
        if (back_pos[0] <= mouse_pos[0] <= back_pos[0] + 165) and (back_pos[1] <= mouse_pos[1] <= back_pos[1] + 60):
            background.blit(img_back1, back_pos)
        else:
            background.blit(img_back0, back_pos)
        
        # 컴퓨터 박스 그림
        background.blit(img_CPU, CPU_pos)
        # 1p
        background.blit(img_1p, [mid[0] - 145, CPU_pos[1] + 100])
        if ((mid[0] - 150 <= mouse_pos[0] <= mid[0] - 100) and (CPU_pos[1] + 150 <= mouse_pos[1] <= CPU_pos[1] + 200)) or (com & 1== 1):
            pygame.draw.rect(background, moon_glow, [mid[0] - 150, CPU_pos[1] + 150, 50, 50])
        else:
            pygame.draw.rect(background, moon_glow, [mid[0] - 150, CPU_pos[1] + 150, 50, 50], width=5)
        # 2p
        background.blit(img_2p, [mid[0] + 105, CPU_pos[1] + 100])
        if ((mid[0] + 100 <= mouse_pos[0] <= mid[0] + 150) and (CPU_pos[1] + 150 <= mouse_pos[1] <= CPU_pos[1] + 200)) or (com & 2 == 2):
            pygame.draw.rect(background, moon_glow, [mid[0] + 100, CPU_pos[1] + 150, 50, 50])
        else:
            pygame.draw.rect(background, moon_glow, [mid[0] + 100, CPU_pos[1] + 150, 50, 50], width=5)
        

        # 설정 바
        pygame.draw.line(background, light_gray, (line[0], ratio_pos[1] + 35), (line[1], ratio_pos[1] + 35), width=4)
        pygame.draw.rect(background, orange, [ratio_pos[0] - 15, ratio_pos[1], 30, 70])

        pygame.display.update()

    
    return menu, set, screen_ratio, com


"""
pygame.init()
menu, set, screen_ratio, com = Setting(menu=True, set=True, screen_ratio=1, com=0)

pygame.quit()
"""