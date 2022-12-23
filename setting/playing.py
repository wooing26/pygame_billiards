import numpy as np
import pygame
from setting.config import *
from setting.Ball_class import *
from setting.spin import *


def Playing(*ball, menu, play):
    global count, count_num, distance_2, buttonup, buttonup2, player_turn
    
    pygame.display.set_caption("Billiard")

    while play:
        deltaTime = fps.tick(60)

        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
                menu = True
                #ball[0].pos = np.array([midpoint])
                #ball[1].pos = np.array([midpoint[0] - 100 / screen_ratio, midpoint[1]])
                #ball[2].pos = np.array([x_lim[1] - 100 / screen_ratio, y_lim[0] + 100 / screen_ratio])
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                distance_0 = np.hypot((click[0] - ball_sum_pos[player_turn][0]), (click[1] - ball_sum_pos[player_turn][1]))
                distance_1 = np.hypot((click[0] - spin_ball[0]), (click[1] - spin_ball[1]))
                if distance_0 < ball[0].r:
                    buttonup = (0, 0)
            if event.type == pygame.MOUSEBUTTONUP:
                if distance_0 < ball[0].r:
                    buttonup = pygame.mouse.get_pos()
                    distance_2 = np.hypot((click[0] - buttonup[0]), (click[1] - buttonup[1]))
                elif distance_1 < spin_radius and np.all([ball[0].v, ball[1].v, ball[2].v] == np.array([0, 0])) and buttonup != (0, 0):
                    buttonup2 = pygame.mouse.get_pos()
            

        # 모든 공 정지 상황 
        if np.all([ball[0].v, ball[1].v, ball[2].v] == np.array([0, 0])):
            
            ball_sum_v = [ball[0].v, ball[1].v]
            ball_sum_pos = [ball[0].pos, ball[1].pos]
            ball_sum_spin = [ball[0].spin, ball[1].spin]

            if count == [1, 1, 3]:      # 점수 +1 상황, 턴이 바뀌지 않음
                count_score[player_turn] += 1
                distance_2 = 0
                count = [0, 0, 0]       # 충돌 초기화
                count_num = 0
                buttonup = (0, 0)
                buttonup2 = (0, 0)

                
            # 초기 플레이어 공 속도 입력
            if distance_2 != 0 and count_num == 0:
                if distance_2 >= speed_limit:
                    distance_2 = speed_limit

                v_0 = (ball_sum_pos[player_turn] - buttonup) / np.linalg.norm(ball_sum_pos[player_turn] - buttonup) * distance_2
                if buttonup2 != (0, 0):
                    r_imp = Get_spin(buttonup2, v_0)
                    ball_sum_spin[player_turn] += np.cross(r_imp, v_0) * ball[0].r / spin_radius / 8 #상수추가 필요할 수도 있음
                    ball_sum_v[player_turn] += np.array(v_0) / 15   #초기 속도 줄이기
                    count_num = 1
                    
                    '''
                    #과하게 스핀을 주려하면 중심속도를 감소시키는 부분
                    if np.linalg.norm(r_imp) / spin_radius > 0.7:
                        ball_sum_v[player_turn] /= (np.linalg.norm(r_imp) / spin_radius * 5)
                    '''

            # 턴 바뀌는 용도
            elif count_num == 1 and count != [1, 1, 3]:
                if count[:2] == [0, 0] and count_score[player_turn] != 0:   # 점수 빼는 상황
                    count_score[player_turn] -= 1
                player_turn += 1
                player_turn %= 2        # 턴 바뀜 (0 -> 1, 1 -> 0)
                distance_2 = 0
                count_num = 0
                count = [0, 0, 0]       # 충돌 초기화
                buttonup = (0, 0)
                buttonup2 = (0, 0)

        # 바닥과 상호작용
        ball[0].rolling()
        ball[1].rolling()
        ball[2].rolling()


        # 공 움직임 (벽 충돌 포함)
        ball[0].advance()
        ball[1].advance()
        ball[2].advance()

        

        # 공끼리 충돌시 움직임
        if frame_count[0] == 0 and ball[0].overlaps(ball[1]):
            ball[0].collision(ball[1])
            frame_count[0] = frame_skip
        elif frame_count[0] != 0:
            frame_count[0] -= 1
        if frame_count[1] == 0 and ball[1].overlaps(ball[2]):
            ball[1].collision(ball[2])
            frame_count[1] = frame_skip
        elif frame_count[1] != 0:
            frame_count[1] -= 1
        if frame_count[2] == 0 and ball[2].overlaps(ball[0]):    
            ball[2].collision(ball[0])
            frame_count[2] = frame_skip
        elif frame_count[2] != 0:
            frame_count[2] -= 1
        
        # 공끼리 충돌 횟수 세기
        if player_turn == 0:
            ball[0].count_score(ball[1], ball[2], count)
        elif player_turn == 1:
            ball[1].count_score(ball[0], ball[2], count)


        


        # 그림 그려주기
        background.fill(black)
        pool_outside = pygame.draw.rect(background, coffee_brown,
        [x_out[0], y_out[0], x_out[1] - x_out[0], y_out[1] - y_out[0]])
        pool_table = pygame.draw.rect(background, green,
        [x_lim[0], y_lim[0], x_lim[1] - x_lim[0], y_lim[1] - y_lim[0]])
        
        # velocity input UI
        if np.all([ball[0].v, ball[1].v, ball[2].v] == np.array([0, 0])) and count_num == 0:
            if buttonup == (0, 0):
                pygame.draw.line(background, red, ball_sum_pos[player_turn], mouse_pos, width=4)
            else:
                pygame.draw.line(background, red, ball_sum_pos[player_turn], buttonup, width=4)
        
        # spin input UI
        pygame.draw.circle(background, white, spin_ball, spin_radius)
        pygame.draw.circle(background, red, spin_ball, 10 / screen_ratio, 2)
        if np.hypot((spin_ball[0] - mouse_pos[0]), (spin_ball[1] - mouse_pos[1])) <= spin_radius:
            pygame.draw.circle(background, blue, mouse_pos, 10 / screen_ratio, 2)
        if np.any([ball[0].v, ball[1].v, ball[2].v] != np.array([0, 0])):
            pygame.draw.circle(background, blue, buttonup2, 10 / screen_ratio, 2)

        # 공
        ball[0].draw()
        ball[1].draw()
        ball[2].draw()
        
        Score(count_score[0], count_score[1])       # 스코어 보드
        pygame.display.update()

    return menu, play