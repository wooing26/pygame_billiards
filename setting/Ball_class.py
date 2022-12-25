from setting.config import *
import numpy as np

# 공별 설정
class Ball:
    def __init__(self, x, y, vx, vy, spin_x, spin_y, spin_z, color,
     radius = 61.5 / 3 / screen_ratio, frict = 0.02, mass = 210 / 27 / (screen_ratio**3)):
        
        self.pos = np.array([x, y])
        self.v = np.array([vx, vy])
        self.spin = np.array([spin_x, spin_y, spin_z])
        self.col = color
        self.r = radius
        self.frict = frict
        self.m = mass
        self.I = 2 / 5 * self.m * self.r**2
    
    # property 이용 값  getter, setter 편하게 설정
    @property
    def x(self):
        return self.pos[0]
    @x.setter
    def x(self, value):
        self.pos[0] = value
    
    @property
    def y(self):
        return self.pos[1]
    @y.setter
    def y(self, value):
        self.pos[1] = value

    @property
    def vx(self):
        return self.v[0]
    @vx.setter
    def vx(self, value):
        self.v[0] = value
    
    @property
    def vy(self):
        return self.v[1]
    @vy.setter
    def vy(self, value):
        self.v[1] = value

    @property
    def spin_x(self):
        return self.spin[0]
    @spin_x.setter
    def spin_x(self, value):
        self.spin[0] = value

    @property
    def spin_y(self):
        return self.spin[1]
    @spin_y.setter
    def spin_y(self, value):
        self.spin[1] = value

    @property
    def spin_z(self):
        return self.spin[2]
    @spin_z.setter
    def spin_z(self, value):
        self.spin[2] = value


    # 공 그리기
    def draw(self, background):
        
        circle = pygame.draw.circle(background, self.col, self.pos, self.r)
        return circle
    
    # 벽 충돌 상황
    def limit_x0(self):
        return self.x - self.r <= pool_wall[0][0]
    def limit_x1(self):
        return self.x + self.r >= pool_wall[0][1]
    def limit_y0(self):
        return self.y - self.r <= pool_wall[1][0]
    def limit_y1(self):
        return self.y + self.r >= pool_wall[1][1]
    


    # 공의 움직임 (공끼리 충돌 제외)
    def advance(self, e_w = 0.8):

        # 마찰에 의한 속도 감소
        if np.all(self.v != 0):
            self.v -= self.v / np.linalg.norm(self.v) * self.frict
            if np.hypot(*(self.v)) < 0.1:
                self.v = np.array([0.0, 0.0])
        self.pos += self.v

        # 벽과 충돌시 각속도 이용 움직임 변화
        def change_velocity(n_hat, e = 0.8, u = 0.2):   # e, u 변화 시키면 움직임이 변함
            vi = self.v - np.cross(self.spin, n_hat)[:2]
            vi = np.append(vi, 0)
            j = (-(1 + e) * np.dot(vi, n_hat)) * self.m       # 충격량, cross(r,n_hat) = 0
            t_hat = np.cross(self.spin, n_hat)             # t_hat = 충돌 후 마찰 , t_hat_n = t_hat normalized
            t_hat_n = t_hat / np.linalg.norm(t_hat)
            j_t = -np.dot(vi, t_hat_n) * self.m
            if np.abs(j_t) > u * j:
                if j_t > u * j:
                    j_t = u * j    # u = 마찰계수
                else:
                    j_t = -u * j
            
            delta = (j * n_hat + j_t * t_hat_n) / self.m
            self.v = self.v + delta[:2]
            self.spin = self.spin + j_t * np.cross(-n_hat, t_hat_n) / self.I


        # 벽과 충돌 상황
        if self.limit_x0():
            self.x = pool_wall[0][0] + self.r
            change_velocity(np.array([1, 0, 0]))

        if self.limit_x1():
            self.x = pool_wall[0][1] - self.r
            change_velocity(np.array([-1, 0, 0]))

        if self.limit_y0():
            self.y = pool_wall[1][0] + self.r
            change_velocity(np.array([0, 1, 0]))
            
        if self.limit_y1():
            self.y = pool_wall[1][1] - self.r
            change_velocity(np.array([0, -1, 0]))
    
    # 바닥과의 상호작용 (백스핀)
    def rolling(self, c = 0.0003, mu = 0.0005):
        # 각속도 감소
        if np.any(self.spin != 0):
            self.spin -= self.spin / np.linalg.norm(self.spin) * 5  #프레임마다 일정 각속도 계속 감소
            if np.linalg.norm(self.spin) < 5:
                self.spin = np.array([0.0, 0.0, 0.0])

        #각속도 추가 항
        n_hat = np.array([0, 0, 1])
        self.spin -= c * np.cross(self.v, n_hat)

        #각속도에 의한 중심속도 변화
        dv = -mu * np.cross(self.spin, n_hat)
        self.v[0] += dv[0]
        self.v[1] += dv[1]
        

    # 공끼리 충돌 상황
    def overlaps(self, other):

        return np.hypot(*(self.pos - other.pos)) <= self.r + other.r


    # 공끼리 충돌시 움직임 
    def collision(self, other, e_b = 0.95): #공사이 반발계수
        # 충돌했을 때의 속도 변화 함수 작성
        def change_velocity():
            m1, m2 = self.m, other.m
            M = m1 + m2
            p1, p2 = self.pos, other.pos
            dis = np.linalg.norm(p1 - p2)
            pos_diff = p2 - p1
            n_hat = pos_diff / dis #충돌면 단위 벡터
            v1, v2 = self.v, other.v
            j = -(1+e_b) * np.dot((v1 - v2), n_hat) / (1 / m1 + 1 / m2) #충격량
            u1 = v1 + j / m1 * n_hat
            u2 = v2 - j / m2 * n_hat
            self.v = u1
            other.v = u2
        
        # 충돌시 움직임 변화
        if self.overlaps(other):
            change_velocity()


    # 충돌 횟수 세기 (3구의 3쿠션)
    def count_score(self, other1, other2, count):
        
        if self.overlaps(other1) and count[0] == 0:
            count[0] += 1
        if self.overlaps(other2) and count[1] == 0:
            count[1] += 1
        if self.limit_x0() and count[2] < 3 and count[:2] != [1, 1]:
            count[2] += 1
        if self.limit_x1() and count[2] < 3 and count[:2] != [1, 1]:
            count[2] += 1
        if self.limit_y0() and count[2] < 3 and count[:2] != [1, 1]:
            count[2] += 1
        if self.limit_y1() and count[2] < 3 and count[:2] != [1, 1]:
            count[2] += 1
