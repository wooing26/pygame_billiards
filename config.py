import numpy as np


# 당구대 설정
height = 1422 / 3
width = 2844 / 3
height_out = 1730 / 3
width_out = 3120 / 3
midpoint = [back_size[0] / 2, back_size[1] * 2 / 3]

# 당구대 안에서만 공이 움직이게 크기 설정
x_lim = np.array([midpoint[0] - width / 2, midpoint[0] + width / 2])
y_lim = np.array([midpoint[1] - height / 2, midpoint[1] + height / 2])
x_out = np.array([midpoint[0] - width_out / 2, midpoint[0] + width_out / 2])
y_out = np.array([midpoint[1] - height_out / 2, midpoint[1] + height_out / 2])

# 당구대
pool_wall = np.array([x_lim, y_lim])