'''不同分辨率、缩放率适配，贴图坐标、圣遗物坐标、截图坐标定位'''

import win32con, win32api, win32gui, win32print

# 基础分辨率，缩放信息获取
hDC = win32gui.GetDC(0)
width_r = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
height_r = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
width_s = win32api.GetSystemMetrics(0)
print(f'分辨率{width_r, height_r}')
SCALE = width_r / width_s

# 游戏窗口信息获取
window_title = '原神'
window = win32gui.FindWindow(None, window_title)
left, top, right, bottom = win32gui.GetWindowRect(window)
print(f'窗口坐标{left, top, right, bottom}')
w_left = left * SCALE
w_top = top * SCALE
w_width = (right - left - 3) * SCALE
w_hight = (bottom - top - 26) * SCALE
print(f'窗口x,y,w,h{w_left, w_top, w_width, w_hight}')
ratio = w_width / w_hight

# 分辨率适配，A代表背包面板，B代表角色面板
# 2560*1600 | 3840*2400 | 1280 * 800
# if (width_r == 2560 and height_r == 1600) or (width_r == 1280 and height_r == 800) or (width_r == 3840 and height_r == 2400):
#     x_initial_A, y_initial_A, x_offset_A, y_offset_A = (300 / 2560 * width_r, (386 - 50) / 1600 * height_r + SCALE * 25, 195 / 2560 * width_r, 234 / 1600 * height_r) # 第一个贴图坐标，y需要根据SCALE的标题栏高度做偏移
#     x_left_A, x_right_A, y_top_A, y_bottom_A = (161 / 2560 * width_r, 326 / 2560 * width_r, (208 - 50) / 1600 * height_r + SCALE * 25, (412 - 50) / 1600 * height_r + SCALE * 25) # 第一个圣遗物坐标
#     x_grab_A, y_grab_A, w_grab_A, h_grab_A = (1808 / 2560 * width_r, (677 - 50) / 1600 * height_r + SCALE * 25, 377 / 2560 * width_r, 220 / 1600 * height_r) # 截图x, y, w, h，y需要根据SCALE的标题栏高度做适配
#     row_A, col_A = (6, 8) #圣遗物行列数

#     x_initial_B, y_initial_B, x_offset_B, y_offset_B = (198 / 2560 * width_r, (397 - 50) / 1600 * height_r + SCALE * 25, 189 / 2560 * width_r, 225 / 1600 * height_r)
#     x_left_B, x_right_B, y_top_B, y_bottom_B = (52 / 2560 * width_r, 220 / 2560 * width_r, (215 -50) / 1600 * height_r + SCALE * 25, (419 - 50) / 1600 * height_r + SCALE * 25)
#     x_grab_B, y_grab_B, w_grab_B, h_grab_B = (1983 / 2560 * width_r, (510 - 50) / 1600 * height_r + SCALE * 25, 334 / 2560 * width_r, 200 / 1600 * height_r)
#     row_B, col_B = (6, 4)

# 16:10窗口模式
if ratio > 1.55 and ratio < 1.65:
    x_initial_A, y_initial_A, x_offset_A, y_offset_A = (300 / 2560 * w_width + w_left, (386 - 48) / 1600 * w_hight + SCALE * 24 + w_top, 195 / 2560 * w_width, 234 / 1600 * w_hight) # 第一个贴图坐标，y需要根据SCALE的标题栏高度做偏移
    x_left_A, x_right_A, y_top_A, y_bottom_A = (161 / 2560 * w_width + w_left, 326 / 2560 * w_width + w_left, (208 - 48) / 1600 * w_hight + SCALE * 24 + w_top, (412 - 48) / 1600 * w_hight + SCALE * 24 + w_top) # 第一个圣遗物坐标
    x_grab_A, y_grab_A, w_grab_A, h_grab_A = (1808 / 2560 * w_width + w_left, (677 - 48) / 1600 * w_hight + SCALE * 24 + w_top, 377 / 2560 * w_width, 214 / 1600 * w_hight) # 截图x, y, w, h，y需要根据SCALE的标题栏高度做适配
    row_A, col_A = (6, 8) #圣遗物行列数

    x_initial_B, y_initial_B, x_offset_B, y_offset_B = (198 / 2560 * w_width + w_left, (397 - 48) / 1600 * w_hight + SCALE * 24 + w_top, 189 / 2560 * w_width, 225 / 1600 * w_hight)
    x_left_B, x_right_B, y_top_B, y_bottom_B = (52 / 2560 * w_width + w_left, 220 / 2560 * w_width + w_left, (215 -48) / 1600 * w_hight + SCALE * 24 + w_top, (419 - 48) / 1600 * w_hight + SCALE * 24 + w_top)
    x_grab_B, y_grab_B, w_grab_B, h_grab_B = (1983 / 2560 * w_width + w_left, (510 - 48) / 1600 * w_hight + SCALE * 24 + w_top, 334 / 2560 * w_width, 190 / 1600 * w_hight)
    row_B, col_B = (6, 4)

# 1920*1080 | 2560*1440 | 3840*2160
# elif (width_r == 1920 and height_r == 1080) or (width_r == 2560 and height_r == 1440) or (width_r == 3840 and height_r == 2160):
#     x_initial_A, y_initial_A, x_offset_A, y_offset_A = (224 / 1920 * width_r, (289 - 36) / 1080 * height_r + SCALE * 25, 146 / 1920 * width_r, 175 / 1080 * height_r)
#     x_left_A, x_right_A, y_top_A, y_bottom_A = (121 / 1920 * width_r, 246 / 1920 * width_r, (157 - 36) / 1080 * height_r + SCALE * 25, (311 - 36) / 1080 * height_r + SCALE * 25)
#     x_grab_A, y_grab_A, w_grab_A, h_grab_A = (1359 / 1920 * width_r, (511 - 36) / 1080 * height_r + SCALE * 25, 271 / 1920 * width_r, 156 / 1080 * height_r)
#     row_A, col_A = (5, 8)

#     x_initial_B, y_initial_B, x_offset_B, y_offset_B = (144 / 1920 * width_r, (293 - 36) / 1080 * height_r + SCALE * 25, 142 / 1920 * width_r, 168 / 1080 * height_r)
#     x_left_B, x_right_B, y_top_B, y_bottom_B = (39 / 1920 * width_r, 166 / 1920 * width_r, (162 - 36) / 1080 * height_r + SCALE * 25, (315 - 36) / 1080 * height_r + SCALE * 25)
#     x_grab_B, y_grab_B, w_grab_B, h_grab_B = (1490 / 1920 * width_r, (384 - 36) / 1080 * height_r + SCALE * 25, 257 / 1920 * width_r, 141 / 1080 * height_r)
#     row_B, col_B = (5, 4)

# 16:9窗口模式
elif ratio > 1.7 and ratio < 1.8:
    x_initial_A, y_initial_A, x_offset_A, y_offset_A = (224 / 1920 * w_width + w_left, (289 - 36) / 1080 * w_hight + SCALE * 24 + w_top, 146 / 1920 * w_width, 175 / 1080 * w_hight)
    x_left_A, x_right_A, y_top_A, y_bottom_A = (121 / 1920 * w_width + w_left, 246 / 1920 * w_width + w_left, (157 - 36) / 1080 * w_hight + SCALE * 24 + w_top, (311 - 36) / 1080 * w_hight + SCALE * 24 + w_top)
    x_grab_A, y_grab_A, w_grab_A, h_grab_A = (1359 / 1920 * w_width + w_left, (511 - 36) / 1080 * w_hight + SCALE * 24 + w_top, 271 / 1920 * w_width, 156 / 1080 * w_hight)
    row_A, col_A = (5, 8)

    x_initial_B, y_initial_B, x_offset_B, y_offset_B = (144 / 1920 * w_width + w_left, (293 - 36) / 1080 * w_hight + SCALE * 24 + w_top, 142 / 1920 * w_width, 168 / 1080 * w_hight)
    x_left_B, x_right_B, y_top_B, y_bottom_B = (39 / 1920 * w_width + w_left, 166 / 1920 * w_width + w_left, (162 - 36) / 1080 * w_hight + SCALE * 24 + w_top, (315 - 36) / 1080 * w_hight + SCALE * 24 + w_top)
    x_grab_B, y_grab_B, w_grab_B, h_grab_B = (1490 / 1920 * w_width + w_left, (384 - 36) / 1080 * w_hight + SCALE * 24 + w_top, 257 / 1920 * w_width, 141 / 1080 * w_hight)
    row_B, col_B = (5, 4)

# 3:2窗口模式
elif ratio > 1.45 and ratio < 1.55:
    x_initial_A, y_initial_A, x_offset_A, y_offset_A = (254 / 2160 * w_width + w_left, (318 - 36) / 1440 * w_hight + SCALE * 24 + w_top, 165 / 2160 * w_width, 197 / 1440 * w_hight)
    x_left_A, x_right_A, y_top_A, y_bottom_A = (136 / 2160 * w_width + w_left, 276 / 2160 * w_width + w_left, (173 - 36) / 1440 * w_hight + SCALE * 24 + w_top, (344 - 36) / 1440 * w_hight + SCALE * 24 + w_top)
    x_grab_A, y_grab_A, w_grab_A, h_grab_A = (1528 / 2160 * w_width + w_left, (564 - 36) / 1440 * w_hight + SCALE * 24 + w_top, 297 / 2160 * w_width, 186 / 1440 * w_hight)
    row_A, col_A = (6, 8)

    x_initial_B, y_initial_B, x_offset_B, y_offset_B = (160 / 2160 * w_width + w_left, (326 - 36) / 1440 *w_hight + SCALE * 24 + w_top, 160 / 2160 * w_width, 189 / 1440 * w_hight)
    x_left_B, x_right_B, y_top_B, y_bottom_B = (43 / 2160 * w_width + w_left, 186 / 2160 * w_width + w_left, (178 - 36) / 1440 * w_hight + SCALE * 24 + w_top, (350 - 36) / 1440 * w_hight + SCALE * 24 + w_top)
    x_grab_B, y_grab_B, w_grab_B, h_grab_B = (1676 / 2160 * w_width + w_left, (429 - 36) / 1440 * w_hight + SCALE * 24 + w_top, 321 / 2160 * w_width, 160 / 1440 * w_hight)
    row_B, col_B = (6, 4)

else:
    print('请将游戏显示模式调至1920*1080窗口，然后重启软件')    

# 贴图坐标组
position_A = []
for i in range(row_A):
    for j in range(col_A):
        position = x_initial_A + j * x_offset_A, y_initial_A + i * y_offset_A
        position_A.append(position)

position_B = []
for i in range(row_B):
    for j in range(col_B):
        position = x_initial_B + j * x_offset_B, y_initial_B + i * y_offset_B
        position_B.append(position)

# 鼠标事件有效坐标区间
xarray_A = []
for i in range(col_A):
    position = x_left_A + i * x_offset_A, x_right_A + i * x_offset_A
    xarray_A.append(position)
yarray_A = []
for i in range(row_A):
    position = y_top_A + i * y_offset_A, y_bottom_A + i * y_offset_A
    yarray_A.append(position)

xarray_B = []
for i in range(col_B):
    position = x_left_B + i * x_offset_B, x_right_B + i * x_offset_B
    xarray_B.append(position)
yarray_B = []
for i in range(row_B):
    position = y_top_B + i * y_offset_B, y_bottom_B + i * y_offset_B
    yarray_B.append(position)
