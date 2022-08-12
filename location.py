'''不同分辨率、缩放率适配，贴图坐标、圣遗物坐标、截图坐标定位'''

import win32con, win32api, win32gui, win32print

# 基础分辨率，缩放信息获取
hDC = win32gui.GetDC(0)
width_r = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
height_r = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
width_s = win32api.GetSystemMetrics(0)
print(width_r, height_r)
SCALE = width_r / width_s

# 分辨率适配，A代表背包面板，B代表角色面板
# 2560*1600
if width_r == 2560 and height_r == 1600:
    x_initial_A, y_initial_A, x_offset_A, y_offset_A = (490, 320, 156, 188) # 第一个贴图坐标及偏移
    x_left_A, x_right_A, y_top_A, y_bottom_A = (382, 512, 182, 346) # 第一个圣遗物坐标
    x_grab_A, y_grab_A, w_grab_A, h_grab_A = (1684, 560, 350, 168) # 截图x, y, w, h
    row_A, col_A = (7, 8) #圣遗物行列数

    x_initial_B, y_initial_B, x_offset_B, y_offset_B = (400, 320, 150, 180)
    x_left_B, x_right_B, y_top_B, y_bottom_B = (295, 429, 188, 350)
    x_grab_B, y_grab_B, w_grab_B, h_grab_B = (1820, 422, 290, 152)
    row_B, col_B = (7, 4)

# 1920*1080 | 2560*1440
elif (width_r == 1920 and height_r == 1080) or (width_r == 2560 and height_r == 1440):
    x_initial_A, y_initial_A, x_offset_A, y_offset_A = (310 / 1920 * width_r, 242 / 1080 * height_r, 128 / 1920 * width_r, 152 / 1080 * height_r)
    x_left_A, x_right_A, y_top_A, y_bottom_A = (223 / 1920 * width_r, 333 / 1920 * width_r, 132 / 1080 * height_r, 267 / 1080 * height_r)
    x_grab_A, y_grab_A, w_grab_A, h_grab_A = (1283 / 1920 * width_r, 437 / 1080 * height_r, 308 / 1920 * width_r, 141 / 1080 * height_r)
    row_A, col_A = (6, 8)

    x_initial_B, y_initial_B, x_offset_B, y_offset_B = (236 / 1920 * width_r, 244 / 1080 * height_r, 123 / 1920 * width_r, 147 / 1080 * height_r)
    x_left_B, x_right_B, y_top_B, y_bottom_B = (152 / 1920 * width_r, 263 / 1920 * width_r, 135 / 1080 * height_r, 270 / 1080 * height_r)
    x_grab_B, y_grab_B, w_grab_B, h_grab_B = (1408 / 1920 * width_r, 332 / 1080 * height_r, 240 / 1920 * width_r, 118 / 1080 * height_r)
    row_B, col_B = (6, 4)
else:
    print('暂不支持该分辨率，请联系作者。')

# 贴图坐标组
position_A = [(x_initial_A, y_initial_A), (x_initial_A + x_offset_A, y_initial_A), (x_initial_A + 2 * x_offset_A, y_initial_A), (x_initial_A + 3 * x_offset_A, y_initial_A), (x_initial_A + 4 * x_offset_A, y_initial_A), (x_initial_A + 5 * x_offset_A, y_initial_A), (x_initial_A + 6 * x_offset_A, y_initial_A), (x_initial_A + 7 * x_offset_A, y_initial_A),
                (x_initial_A, y_initial_A + y_offset_A), (x_initial_A + x_offset_A, y_initial_A + y_offset_A), (x_initial_A + 2 * x_offset_A, y_initial_A + y_offset_A), (x_initial_A + 3 * x_offset_A, y_initial_A + y_offset_A), (x_initial_A + 4 * x_offset_A, y_initial_A + y_offset_A), (x_initial_A + 5 * x_offset_A, y_initial_A + y_offset_A), (x_initial_A + 6 * x_offset_A, y_initial_A + y_offset_A), (x_initial_A + 7 * x_offset_A, y_initial_A + y_offset_A),
                (x_initial_A, y_initial_A + 2 * y_offset_A), (x_initial_A + x_offset_A, y_initial_A + 2 * y_offset_A), (x_initial_A + 2 * x_offset_A, y_initial_A + 2 * y_offset_A), (x_initial_A + 3 * x_offset_A, y_initial_A + 2 * y_offset_A), (x_initial_A + 4 * x_offset_A, y_initial_A + 2 * y_offset_A), (x_initial_A + 5 * x_offset_A, y_initial_A + 2 * y_offset_A), (x_initial_A + 6 * x_offset_A, y_initial_A + 2 * y_offset_A), (x_initial_A + 7 * x_offset_A, y_initial_A + 2 * y_offset_A),
                (x_initial_A, y_initial_A + 3 * y_offset_A), (x_initial_A + x_offset_A, y_initial_A + 3 * y_offset_A), (x_initial_A + 2 * x_offset_A, y_initial_A + 3 * y_offset_A), (x_initial_A + 3 * x_offset_A, y_initial_A + 3 * y_offset_A), (x_initial_A + 4 * x_offset_A, y_initial_A + 3 * y_offset_A), (x_initial_A + 5 * x_offset_A, y_initial_A + 3 * y_offset_A), (x_initial_A + 6 * x_offset_A, y_initial_A + 3 * y_offset_A), (x_initial_A + 7 * x_offset_A, y_initial_A + 3 * y_offset_A),
                (x_initial_A, y_initial_A + 4 * y_offset_A), (x_initial_A + x_offset_A, y_initial_A + 4 * y_offset_A), (x_initial_A + 2 * x_offset_A, y_initial_A + 4 * y_offset_A), (x_initial_A + 3 * x_offset_A, y_initial_A + 4 * y_offset_A), (x_initial_A + 4 * x_offset_A, y_initial_A + 4 * y_offset_A), (x_initial_A + 5 * x_offset_A, y_initial_A + 4 * y_offset_A), (x_initial_A + 6 * x_offset_A, y_initial_A + 4 * y_offset_A), (x_initial_A + 7 * x_offset_A, y_initial_A + 4 * y_offset_A),
                (x_initial_A, y_initial_A + 5 * y_offset_A), (x_initial_A + x_offset_A, y_initial_A + 5 * y_offset_A), (x_initial_A + 2 * x_offset_A, y_initial_A + 5 * y_offset_A), (x_initial_A + 3 * x_offset_A, y_initial_A + 5 * y_offset_A), (x_initial_A + 4 * x_offset_A, y_initial_A + 5 * y_offset_A), (x_initial_A + 5 * x_offset_A, y_initial_A + 5 * y_offset_A), (x_initial_A + 6 * x_offset_A, y_initial_A + 5 * y_offset_A), (x_initial_A + 7 * x_offset_A, y_initial_A + 5 * y_offset_A),
                (x_initial_A, y_initial_A + 6 * y_offset_A), (x_initial_A + x_offset_A, y_initial_A + 6 * y_offset_A), (x_initial_A + 2 * x_offset_A, y_initial_A + 6 * y_offset_A), (x_initial_A + 3 * x_offset_A, y_initial_A + 6 * y_offset_A), (x_initial_A + 4 * x_offset_A, y_initial_A + 6 * y_offset_A), (x_initial_A + 5 * x_offset_A, y_initial_A + 6 * y_offset_A), (x_initial_A + 6 * x_offset_A, y_initial_A + 6 * y_offset_A), (x_initial_A + 7 * x_offset_A, y_initial_A + 6 * y_offset_A)]

position_B = [(x_initial_B, y_initial_B), (x_initial_B + x_offset_B, y_initial_B), (x_initial_B + 2 * x_offset_B, y_initial_B), (x_initial_B + 3 * x_offset_B, y_initial_B),
                (x_initial_B, y_initial_B + y_offset_B), (x_initial_B + x_offset_B, y_initial_B + y_offset_B), (x_initial_B + 2 * x_offset_B, y_initial_B + y_offset_B), (x_initial_B + 3 * x_offset_B, y_initial_B + y_offset_B),
                (x_initial_B, y_initial_B + 2 * y_offset_B), (x_initial_B + x_offset_B, y_initial_B + 2 * y_offset_B), (x_initial_B + 2 * x_offset_B, y_initial_B + 2 * y_offset_B), (x_initial_B + 3 * x_offset_B, y_initial_B + 2 * y_offset_B),
                (x_initial_B, y_initial_B + 3 * y_offset_B), (x_initial_B + x_offset_B, y_initial_B + 3 * y_offset_B), (x_initial_B + 2 * x_offset_B, y_initial_B + 3 * y_offset_B), (x_initial_B + 3 * x_offset_B, y_initial_B + 3 * y_offset_B),
                (x_initial_B, y_initial_B + 4 * y_offset_B), (x_initial_B + x_offset_B, y_initial_B + 4 * y_offset_B), (x_initial_B + 2 * x_offset_B, y_initial_B + 4 * y_offset_B), (x_initial_B + 3 * x_offset_B, y_initial_B + 4 * y_offset_B),
                (x_initial_B, y_initial_B + 5 * y_offset_B), (x_initial_B + x_offset_B, y_initial_B + 5 * y_offset_B), (x_initial_B + 2 * x_offset_B, y_initial_B + 5 * y_offset_B), (x_initial_B + 3 * x_offset_B, y_initial_B + 5 * y_offset_B),
                (x_initial_B, y_initial_B + 6 * y_offset_B), (x_initial_B + x_offset_B, y_initial_B + 6 * y_offset_B), (x_initial_B + 2 * x_offset_B, y_initial_B + 6 * y_offset_B), (x_initial_B + 3 * x_offset_B, y_initial_B + 6 * y_offset_B)]

# 鼠标事件有效坐标区间
xarray_A = [(x_left_A, x_right_A), (x_left_A + x_offset_A, x_right_A + x_offset_A), (x_left_A + 2 * x_offset_A, x_right_A + 2 * x_offset_A), (x_left_A + 3 * x_offset_A, x_right_A + 3 * x_offset_A), (x_left_A + 4 * x_offset_A, x_right_A + 4 * x_offset_A), (x_left_A + 5 * x_offset_A, x_right_A + 5 * x_offset_A), (x_left_A + 6 * x_offset_A, x_right_A + 6 * x_offset_A), (x_left_A + 7 * x_offset_A, x_right_A + 7 * x_offset_A)]
yarray_A = [(y_top_A, y_bottom_A), (y_top_A + y_offset_A, y_bottom_A + y_offset_A), (y_top_A + 2 * y_offset_A, y_bottom_A + 2 * y_offset_A), (y_top_A + 3 * y_offset_A, y_bottom_A + 3 * y_offset_A), (y_top_A + 4 * y_offset_A, y_bottom_A + 4 * y_offset_A), (y_top_A + 5 * y_offset_A, y_bottom_A + 5 * y_offset_A), (y_top_A + 6 * y_offset_A, y_bottom_A + 6 * y_offset_A), (y_top_A + 7 * y_offset_A, y_bottom_A + 7 * y_offset_A)]

xarray_B = [(x_left_B, x_right_B), (x_left_B + x_offset_B, x_right_B + x_offset_B), (x_left_B + 2 * x_offset_B, x_right_B + 2 * x_offset_B), (x_left_B + 3 * x_offset_B, x_right_B + 3 * x_offset_B)]
yarray_B = [(y_top_B, y_bottom_B), (y_top_B + y_offset_B, y_bottom_B + y_offset_B), (y_top_B + 2 * y_offset_B, y_bottom_B + 2 * y_offset_B), (y_top_B + 3 * y_offset_B, y_bottom_B + 3 * y_offset_B), (y_top_B + 4 * y_offset_B, y_bottom_B + 4 * y_offset_B), (y_top_B + 5 * y_offset_B, y_bottom_B + 5 * y_offset_B), (y_top_B + 6 * y_offset_B, y_bottom_B + 6 * y_offset_B), (y_top_B + 7 * y_offset_B, y_bottom_B + 7 * y_offset_B)]

# 数值返回
def get_scale():
    return SCALE

# 背包
def get_position_A():
    return position_A

def get_row_col_A():
    return row_A, col_A

def get_xarray_yarray_A():
    return xarray_A, yarray_A

def get_x_y_w_h_A():
    return x_grab_A, y_grab_A, w_grab_A, h_grab_A

# 角色
def get_position_B():
    return position_B

def get_row_col_B():
    return row_B, col_B

def get_xarray_yarray_B():
    return xarray_B, yarray_B

def get_x_y_w_h_B():
    return x_grab_B, y_grab_B, w_grab_B, h_grab_B