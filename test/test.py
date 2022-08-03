import win32con, win32api, win32gui, win32print

hDC = win32gui.GetDC(0)
width_r = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
width_s = win32api.GetSystemMetrics(0)

print(width_r / width_s)