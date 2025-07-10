'''不同分辨率、缩放率适配，贴图坐标、圣遗物坐标、截图坐标定位'''

import win32con, win32api, win32gui, win32print, time

# 基础分辨率，缩放信息获取
hDC = win32gui.GetDC(0)
width_r = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
height_r = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
width_s = win32api.GetSystemMetrics(0)
print(f'分辨率{width_r, height_r}')
SCALE = width_r / width_s

# 游戏窗口信息获取
window_sc = win32gui.FindWindow('UnityWndClass', '原神')
window_start = win32gui.FindWindow('START Cloud Game', 'START云游戏-Game')
window = window_sc or window_start
# 未检测到窗口时循环直到检测到窗口
# while(not window):
#     print('未找到游戏窗口，请启动游戏！')
#     window_sc = win32gui.FindWindow('UnityWndClass', '原神')
#     window_start = win32gui.FindWindow('START Cloud Game', 'START云游戏-Game')
#     time.sleep(5)
#     window = window_sc or window_start
# left, top, right, bottom = win32gui.GetWindowRect(window)
left, top, right, bottom = (0, 0, 2560, 1600) # 游戏窗口不打开时后门，测试用
print(f'修正前窗口left,top,right,bottom{left, top, right, bottom}')

# 缩放、标题栏修正
w_width = (right - left) * SCALE
if w_width > width_r - 10 and w_width < width_r + 10: # 兼容全屏无边框模式
    w_left = left * SCALE
    w_top = top * SCALE
    w_width = (right - left) * SCALE
    w_hight = (bottom - top) * SCALE
else:
    w_top = (top + 31) * SCALE
    w_left = (left + 7) * SCALE
    w_width = (right - left - 14) * SCALE
    w_hight = (bottom - top - 38) * SCALE
print(f'窗口x,y,w,h{w_left, w_top, w_width, w_hight}')
if w_hight != 0:
    ratio = w_width / w_hight
else:
    ratio = 1

# 分辨率适配，A代表背包面板，B代表角色面板
# 16:10窗口模式
if ratio > 1.55 and ratio < 1.65:
    x_initial_A, y_initial_A, x_offset_A, y_offset_A = (303 / 2560 * w_width + w_left, 424 / 1600 * w_hight + w_top, 195 / 2560 * w_width, 234 / 1600 * w_hight) # 第一个贴图坐标，y需要根据SCALE的标题栏高度做偏移
    x_left_A, x_right_A, y_top_A, y_bottom_A = (156 / 2560 * w_width + w_left, 321 / 2560 * w_width + w_left, 238 / 1600 * w_hight + w_top, 442 / 1600 * w_hight + w_top) # 第一个圣遗物坐标
    x_grab_A, y_grab_A, w_grab_A, h_grab_A = (1776 / 2560 * w_width + w_left, 169 / 1600 * w_hight + w_top, 602 / 2560 * w_width, 725 / 1600 * w_hight) # 截图x, y, w, h，y需要根据SCALE的标题栏高度做适配
    row_A, col_A = (5, 8) #圣遗物行列数

    x_initial_B, y_initial_B, x_offset_B, y_offset_B = (200 / 2560 * w_width + w_left, 355 / 1600 * w_hight + w_top, 189 / 2560 * w_width, 225 / 1600 * w_hight)
    x_left_B, x_right_B, y_top_B, y_bottom_B = (48 / 2560 * w_width + w_left, 216 / 2560 * w_width + w_left, 167 / 1600 * w_hight + w_top, 371 / 1600 * w_hight + w_top)
    x_grab_B, y_grab_B, w_grab_B, h_grab_B = (1947 / 2560 * w_width + w_left, 149 / 1600 * w_hight + w_top, 551 / 2560 * w_width, 504 / 1600 * w_hight)
    row_B, col_B = (6, 4)

# 16:9窗口模式
elif ratio > 1.7 and ratio < 1.8:
    x_initial_A, y_initial_A, x_offset_A, y_offset_A = (226 / 1920 * w_width + w_left, 317 / 1080 * w_hight + w_top, 146 / 1920 * w_width, 175 / 1080 * w_hight)
    x_left_A, x_right_A, y_top_A, y_bottom_A = (117 / 1920 * w_width + w_left, 242 / 1920 * w_width + w_left, 179 / 1080 * w_hight + w_top, 333 / 1080 * w_hight + w_top)
    x_grab_A, y_grab_A, w_grab_A, h_grab_A = (1331 / 1920 * w_width + w_left, 120 / 1080 * w_hight + w_top, 450 / 1920 * w_width, 550 / 1080 * w_hight)
    row_A, col_A = (5, 8)

    x_initial_B, y_initial_B, x_offset_B, y_offset_B = (147 / 1920 * w_width + w_left, 261 / 1080 * w_hight + w_top, 142 / 1920 * w_width, 168 / 1080 * w_hight)
    x_left_B, x_right_B, y_top_B, y_bottom_B = (37 / 1920 * w_width + w_left, 164 / 1920 * w_width + w_left, 125 / 1080 * w_hight + w_top, 278 / 1080 * w_hight + w_top)
    x_grab_B, y_grab_B, w_grab_B, h_grab_B = (1461 / 1920 * w_width + w_left, 111 / 1080 * w_hight + w_top, 413 / 1920 * w_width, 378 / 1080 * w_hight)
    row_B, col_B = (5, 4)

# 3:2窗口模式
# elif ratio > 1.45 and ratio < 1.55:
#     x_initial_A, y_initial_A, x_offset_A, y_offset_A = (254 / 2160 * w_width + w_left, (318 - 36) / 1440 * w_hight + SCALE * 24 + w_top, 165 / 2160 * w_width, 197 / 1440 * w_hight)
#     x_left_A, x_right_A, y_top_A, y_bottom_A = (136 / 2160 * w_width + w_left, 276 / 2160 * w_width + w_left, (173 - 36) / 1440 * w_hight + SCALE * 24 + w_top, (344 - 36) / 1440 * w_hight + SCALE * 24 + w_top)
#     x_grab_A, y_grab_A, w_grab_A, h_grab_A = (1500 / 1920 * w_width + w_left, (175 - 36) / 1080 * w_hight + SCALE * 24 + w_top, (508 - 50) / 1920 * w_width, 571 / 1080 * w_hight)
#     row_A, col_A = (6, 8)

#     x_initial_B, y_initial_B, x_offset_B, y_offset_B = (160 / 2160 * w_width + w_left, (326 - 36) / 1440 *w_hight + SCALE * 24 + w_top, 160 / 2160 * w_width, 189 / 1440 * w_hight)
#     x_left_B, x_right_B, y_top_B, y_bottom_B = (43 / 2160 * w_width + w_left, 186 / 2160 * w_width + w_left, (178 - 36) / 1440 * w_hight + SCALE * 24 + w_top, (350 - 36) / 1440 * w_hight + SCALE * 24 + w_top)
#     x_grab_B, y_grab_B, w_grab_B, h_grab_B = (1649 / 1920 * w_width + w_left, (165 - 36) / 1080 * w_hight + SCALE * 24 + w_top, 461 / 1920 * w_width, 421 / 1080 * w_hight)
#     row_B, col_B = (6, 4)

else:
    print('请将游戏显示模式调至1920*1080窗口，然后重启软件')
    x_initial_A, y_initial_A, x_offset_A, y_offset_A = (226 / 1920 * w_width + w_left, 317 / 1080 * w_hight + w_top, 146 / 1920 * w_width, 175 / 1080 * w_hight)
    x_left_A, x_right_A, y_top_A, y_bottom_A = (117 / 1920 * w_width + w_left, 242 / 1920 * w_width + w_left, 179 / 1080 * w_hight + w_top, 333 / 1080 * w_hight + w_top)
    x_grab_A, y_grab_A, w_grab_A, h_grab_A = (1331 / 1920 * w_width + w_left, 125 / 1080 * w_hight + w_top, 450 / 1920 * w_width, 506 / 1080 * w_hight)
    row_A, col_A = (5, 8)

    x_initial_B, y_initial_B, x_offset_B, y_offset_B = (147 / 1920 * w_width + w_left, 261 / 1080 * w_hight + w_top, 142 / 1920 * w_width, 168 / 1080 * w_hight)
    x_left_B, x_right_B, y_top_B, y_bottom_B = (37 / 1920 * w_width + w_left, 164 / 1920 * w_width + w_left, 125 / 1080 * w_hight + w_top, 278 / 1080 * w_hight + w_top)
    x_grab_B, y_grab_B, w_grab_B, h_grab_B = (1461 / 1920 * w_width + w_left, 111 / 1080 * w_hight + w_top, 413 / 1920 * w_width, 378 / 1080 * w_hight)
    row_B, col_B = (5, 4)

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
