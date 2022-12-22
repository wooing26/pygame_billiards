import numpy as np
import pygame
from Ball_class import *
from config import *


# pygame 설정 
pygame.init()






# 초기 스코어 [1플레이어, 2플레이어], 충돌 횟수 [공1이랑, 공2이랑, 벽이랑]
count_score = [0, 0]
count = [0, 0, 0]


# 공 초기 설정 (위치, 속도, 색)
ball_1 = Ball(midpoint[0], midpoint[1], 0.0, 0.0, 0.0, 0.0, 0.0, white)
ball_2 = Ball(midpoint[0] - 100, midpoint[1], 0.0, 0.0, 0.0, 0.0, 0.0, yellow)
ball_3 = Ball(x_lim[1] - 100, y_lim[0] + 100, 0.0, 0.0, 0.0, 0.0, 0.0, red)


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


# 플레이어 턴 변경 용
player_turn = 0     # 0 : 흰공, 1 : 노란공
distance_2 = 0
buttonup = (0, 0)
buttonup2 = (0, 0)
count_num = 0


# overlap 상황 해결 프레임 조정
frame_count = [0, 0, 0]
frame_skip = 3

# 초기 속력 제한
speed_limit = 250


#게임 실행
play = True
while play:
    deltaTime = fps.tick(60)

    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = pygame.mouse.get_pos()
            distance_0 = np.hypot((click[0] - ball_sum_pos[player_turn][0]), (click[1] - ball_sum_pos[player_turn][1]))
            distance_1 = np.hypot((click[0] - spin_ball[0]), (click[1] - spin_ball[1]))
        if event.type == pygame.MOUSEBUTTONUP:
            if distance_0 < ball_1.r:
                buttonup = pygame.mouse.get_pos()
                distance_2 = np.hypot((click[0] - buttonup[0]), (click[1] - buttonup[1]))
            elif distance_1 < spin_radius and np.all([ball_1.v, ball_2.v, ball_3.v] == np.array([0, 0])) and buttonup != (0, 0):
                buttonup2 = pygame.mouse.get_pos()
            else:
                distance_2 = 0
        

    # 모든 공 정지 상황 
    if np.all([ball_1.v, ball_2.v, ball_3.v] == np.array([0, 0])):
        
        ball_sum_v = [ball_1.v, ball_2.v]
        ball_sum_pos = [ball_1.pos, ball_2.pos]
        ball_sum_spin = [ball_1.spin, ball_2.spin]

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
                ball_sum_spin[player_turn] += np.cross(r_imp, v_0) * ball_1.r / spin_radius / 8 #상수추가 필요할 수도 있음
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
    ball_1.rolling()
    ball_2.rolling()
    ball_3.rolling()


    # 공 움직임 (벽 충돌 포함)
    ball_1.advance()
    ball_2.advance()
    ball_3.advance()

    

    # 공끼리 충돌시 움직임
    if frame_count[0] == 0 and ball_1.overlaps(ball_2):
        ball_1.collision(ball_2)
        frame_count[0] = frame_skip
    elif frame_count[0] != 0:
        frame_count[0] -= 1
    if frame_count[1] == 0 and ball_2.overlaps(ball_3):
        ball_2.collision(ball_3)
        frame_count[1] = frame_skip
    elif frame_count[1] != 0:
        frame_count[1] -= 1
    if frame_count[2] == 0 and ball_3.overlaps(ball_1):    
        ball_3.collision(ball_1)
        frame_count[2] = frame_skip
    elif frame_count[2] != 0:
        frame_count[2] -= 1
    
    # 공끼리 충돌 횟수 세기
    if player_turn == 0:
        ball_1.count_score(ball_2, ball_3, count)
    elif player_turn == 1:
        ball_2.count_score(ball_1, ball_3, count)


    


    # 그림 그려주기
    background.fill(black)
    pool_outside = pygame.draw.rect(background, coffee_brown,
     [x_out[0], y_out[0], x_out[1] - x_out[0], y_out[1] - y_out[0]])
    pool_table = pygame.draw.rect(background, green,
     [x_lim[0], y_lim[0], x_lim[1] - x_lim[0], y_lim[1] - y_lim[0]])
    
    # velocity input UI
    if np.all([ball_1.v, ball_2.v, ball_3.v] == np.array([0, 0])) and count_num == 0:
        if buttonup == (0, 0):
            pygame.draw.line(background, red, ball_sum_pos[player_turn], mouse_pos, width=4)
        else:
            pygame.draw.line(background, red, ball_sum_pos[player_turn], buttonup, width=4)
    
    # spin input UI
    pygame.draw.circle(background, white, spin_ball, 150)
    pygame.draw.circle(background, red, spin_ball, 10, 2)
    if np.hypot((spin_ball[0] - mouse_pos[0]), (spin_ball[1] - mouse_pos[1])) <= spin_radius:
        pygame.draw.circle(background, blue, mouse_pos, 10, 2)
    if np.any([ball_1.v, ball_2.v, ball_3.v] != np.array([0, 0])):
        pygame.draw.circle(background, blue, buttonup2, 10, 2)

    # 공
    ball_1.draw()
    ball_2.draw()
    ball_3.draw()
    
    Score(count_score[0], count_score[1])       # 스코어 보드
    pygame.display.update()

pygame.quit()